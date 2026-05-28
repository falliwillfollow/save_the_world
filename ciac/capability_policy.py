from __future__ import annotations

from pathlib import Path
from typing import Any, Iterable

from .io import load_data
from .validation import validate_data


DEFAULT_CAPABILITY_POLICY_PATH = Path("capability_policies/ciac_capability_policy_v0.yaml")
STATUS_PRIORITY = ["pass", "warn", "fail", "promotion_blocked"]


def load_capability_policy(path: str | Path | None = None) -> dict[str, Any]:
    policy_path = Path(path or DEFAULT_CAPABILITY_POLICY_PATH)
    policy = load_data(policy_path)
    report = validate_data(policy, str(policy_path))
    if not report.ok:
        raise ValueError("; ".join(f"{issue.path}: {issue.message}" for issue in report.issues))
    return policy


def get_domain_policy(policy: dict[str, Any], domain: str) -> dict[str, Any]:
    return policy.get("domains", {}).get(domain, {})


def iter_gates(policy: dict[str, Any], domain: str | None = None) -> Iterable[dict[str, Any]]:
    domains = policy.get("domains", {})
    if domain:
        yield from domains.get(domain, {}).get("gates", [])
        return
    for domain_policy in domains.values():
        yield from domain_policy.get("gates", [])


def get_promotion_blockers(policy: dict[str, Any]) -> list[dict[str, Any]]:
    return list(policy.get("promotion_blockers", []))


def get_required_scenarios(policy: dict[str, Any], domain: str | None = None) -> list[str]:
    requirements = policy.get("scenario_requirements", {})
    if domain:
        return list(requirements.get(domain, {}).get("required", []))
    scenarios: list[str] = []
    for requirement in requirements.values():
        scenarios.extend(requirement.get("required", []))
    return sorted(set(scenarios))


def get_ui_warning(policy: dict[str, Any], warning_id: str) -> dict[str, Any] | None:
    warning = policy.get("ui_warnings", {}).get(warning_id)
    return dict(warning) if isinstance(warning, dict) else None


def evaluate_policy_gates(
    capability_state: dict[str, Any],
    policy: dict[str, Any] | None = None,
    *,
    mode: str = "simulation",
) -> dict[str, Any]:
    policy = policy or load_capability_policy()
    domains = capability_state.get("domains", {})
    domain_statuses: dict[str, Any] = {}
    warnings: list[str] = []
    failures: list[str] = []
    promotion_blockers: list[str] = []
    unknowns: list[str] = []
    source_ids: set[str] = set()

    for domain, domain_policy in policy.get("domains", {}).items():
        gate_results = []
        for gate in domain_policy.get("gates", []):
            result = _evaluate_gate(gate, domains, mode)
            gate_results.append(result)
            source_ids.update(result["source_ids"])
            if result["status"] == "promotion_blocked":
                promotion_blockers.append(result["message"])
            elif result["status"] == "fail":
                failures.append(result["message"])
            elif result["status"] == "warn":
                warnings.append(result["message"])
            if result.get("unknown"):
                unknowns.append(result["message"])
        status = _worst_status(result["status"] for result in gate_results)
        domain_statuses[domain] = {
            "status": status,
            "messages": [result["message"] for result in gate_results if result["status"] != "pass"],
            "gates": gate_results,
            "external_review_blockers": domain_policy.get("external_review_blockers", []),
            "required_structures": domain_policy.get("required_structures", []),
            "required_protocols": domain_policy.get("required_protocols", []),
            "source_ids": sorted({source for result in gate_results for source in result["source_ids"]}),
            "provisional": True,
        }

    status = _worst_status(status["status"] for status in domain_statuses.values())
    if mode == "simulation" and status == "promotion_blocked":
        status = "warn"
    promotion_mode = _promotion_mode(status, promotion_blockers, mode)
    report = {
        "kind": "CapabilityPolicyGateReport",
        "id": f"{policy['policy_id']}_{mode}_gate_report",
        "generated_by": "ciac.capability_policy.v0",
        "policy_id": policy["policy_id"],
        "version": policy["version"],
        "mode": mode,
        "provisional": True,
        "status": status,
        "promotion_mode": promotion_mode,
        "domain_statuses": domain_statuses,
        "warnings": sorted(set(warnings)),
        "failures": sorted(set(failures)),
        "promotion_blockers": sorted(set(promotion_blockers)),
        "unknowns": sorted(set([*unknowns, *policy.get("unknowns", [])])),
        "source_ids": sorted(source_ids),
        "source_registry": policy.get("source_registry", []),
    }
    validation = validate_data(report, report["id"])
    if not validation.ok:
        raise ValueError("; ".join(f"{issue.path}: {issue.message}" for issue in validation.issues))
    return report


def _evaluate_gate(gate: dict[str, Any], domains: dict[str, Any], mode: str) -> dict[str, Any]:
    promotion_match = _condition_matches(gate.get("promotion_block_condition", {}), domains)
    fail_match = _condition_matches(gate.get("fail_condition", {}), domains)
    pass_match = _condition_matches(gate.get("pass_condition", {}), domains)
    warn_match = _condition_matches(gate.get("warn_condition", {}), domains)
    unknown = _condition_unknown(gate.get("pass_condition", {}), domains)

    if mode == "promotion" and promotion_match:
        status = "promotion_blocked"
    elif fail_match:
        status = "fail"
    elif pass_match:
        status = "pass"
    elif warn_match or unknown:
        status = "warn"
    else:
        status = "warn"
        unknown = True

    messages = gate.get("messages", {})
    message = messages.get(status) or messages.get("unknown") or f"{gate['gate_id']} is {status}."
    return {
        "gate_id": gate["gate_id"],
        "capability_field": gate["capability_field"],
        "status": status,
        "message": message,
        "unknown": bool(unknown),
        "source_ids": list(gate.get("source_ids", [])),
        "evidence_quality": gate.get("evidence_quality", "mixed"),
        "translation_confidence": gate.get("translation_confidence", "low"),
        "regulatory_strength": gate.get("regulatory_strength", "heuristic"),
        "provisional": True,
    }


def _condition_matches(condition: dict[str, Any], domains: dict[str, Any]) -> bool:
    if not condition:
        return False
    all_clauses = condition.get("all")
    if isinstance(all_clauses, list):
        return bool(all_clauses) and all(_clause_matches(clause, domains) for clause in all_clauses)
    any_clauses = condition.get("any")
    if isinstance(any_clauses, list):
        return any(_clause_matches(clause, domains) for clause in any_clauses)
    return False


def _condition_unknown(condition: dict[str, Any], domains: dict[str, Any]) -> bool:
    clauses = []
    if isinstance(condition.get("all"), list):
        clauses.extend(condition["all"])
    if isinstance(condition.get("any"), list):
        clauses.extend(condition["any"])
    return any(_field_value(clause.get("field", ""), domains)[1] for clause in clauses)


def _clause_matches(clause: dict[str, Any], domains: dict[str, Any]) -> bool:
    value, missing = _field_value(clause.get("field", ""), domains)
    if "missing" in clause:
        return missing is bool(clause["missing"])
    if missing:
        return False
    if "equals" in clause and value != clause["equals"]:
        return False
    if "not_equals" in clause and value == clause["not_equals"]:
        return False
    if "in" in clause and value not in clause["in"]:
        return False
    numeric = _number(value)
    if "min" in clause and (numeric is None or numeric < float(clause["min"])):
        return False
    if "max" in clause and (numeric is None or numeric > float(clause["max"])):
        return False
    if "above" in clause and (numeric is None or numeric <= float(clause["above"])):
        return False
    if "below" in clause and (numeric is None or numeric >= float(clause["below"])):
        return False
    if "between" in clause:
        low, high = clause["between"]
        if numeric is None or numeric < float(low) or numeric > float(high):
            return False
    return True


def _field_value(field: str, domains: dict[str, Any]) -> tuple[Any, bool]:
    parts = field.split(".")
    if len(parts) < 2:
        return None, True
    value: Any = domains
    for part in parts:
        if not isinstance(value, dict) or part not in value:
            return None, True
        value = value[part]
    return value, False


def _number(value: Any) -> float | None:
    if isinstance(value, bool):
        return 1.0 if value else 0.0
    if isinstance(value, (int, float)):
        return float(value)
    try:
        return float(str(value))
    except (TypeError, ValueError):
        return None


def _worst_status(statuses: Iterable[str]) -> str:
    result = "pass"
    for status in statuses:
        if STATUS_PRIORITY.index(status) > STATUS_PRIORITY.index(result):
            result = status
    return result


def _promotion_mode(status: str, promotion_blockers: list[str], mode: str) -> str:
    if mode == "simulation":
        return "simulation_only"
    if mode == "promotion" and (status == "promotion_blocked" or promotion_blockers):
        return "review_blocked"
    if status == "pass" and not promotion_blockers:
        return "promotion_ready"
    return "simulation_only"
