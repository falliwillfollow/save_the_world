from __future__ import annotations

import hashlib
import json
from typing import Any


SURVIVAL_CRITICAL_KINDS = {
    "GateReport",
    "SimulationRun",
    "NutritionReport",
    "WaterReport",
    "EnergyReport",
    "RoleReport",
    "ScenarioRun",
}


def evaluate_audit(
    compiled_plan: dict[str, Any],
    reports: dict[str, Any],
    scenarios: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    scenario_reports = scenarios or []
    subsystem_statuses = _subsystem_statuses(reports, scenario_reports)
    blockers = _survival_critical_blockers(reports, scenario_reports)
    warnings = _noncritical_warnings(reports, scenario_reports)
    redesigns = _required_redesigns(reports, scenario_reports, blockers)
    top_risks = _top_risks(reports, scenario_reports)
    recommendations = _next_sprint_recommendations(blockers, warnings, top_risks)
    overall_status = _overall_status(blockers, warnings, subsystem_statuses)
    promotion_decision = _promotion_decision(overall_status)

    return {
        "kind": "AuditReport",
        "id": f"{compiled_plan['id']}_audit_{_evidence_hash(compiled_plan, reports, scenario_reports)}",
        "compiled_plan": compiled_plan["id"],
        "generated_by": "ciac.audit.v0",
        "provisional": True,
        "overall_status": overall_status,
        "promotion_decision": promotion_decision,
        "confidence": "low",
        "subsystem_statuses": subsystem_statuses,
        "survival_critical_blockers": blockers,
        "noncritical_warnings": warnings,
        "required_redesigns": redesigns,
        "top_risks": top_risks,
        "next_sprint_recommendations": recommendations,
        "inputs": _inputs(compiled_plan, reports, scenario_reports),
        "unknowns": [
            "Audit output is an evidence summary, not approval for real-world construction or occupation.",
            "All subsystem reports remain provisional and depend on seed assumptions.",
            "A candidate_for_review decision would still require professional, legal, health, engineering, and resident governance review.",
        ],
    }


def _subsystem_statuses(
    reports: dict[str, Any],
    scenarios: list[dict[str, Any]],
) -> dict[str, dict[str, Any]]:
    statuses: dict[str, dict[str, Any]] = {}
    for name, report in sorted(reports.items()):
        if report is None:
            continue
        statuses[name] = {
            "kind": report.get("kind", "Unknown"),
            "status": _status_of(report),
            "survival_critical": report.get("kind") in SURVIVAL_CRITICAL_KINDS,
        }
    for report in scenarios:
        name = f"scenario:{report.get('scenario', report.get('id', 'unknown'))}"
        statuses[name] = {
            "kind": report.get("kind", "ScenarioRun"),
            "status": _status_of(report),
            "survival_critical": True,
        }
    return statuses


def _survival_critical_blockers(
    reports: dict[str, Any],
    scenarios: list[dict[str, Any]],
) -> list[str]:
    blockers: list[str] = []
    gates = reports.get("gates")
    if gates:
        for result in gates.get("results", []):
            if result.get("survival_critical") and result.get("status") == "fail":
                blockers.append(f"gate:{result['gate']} failed")

    for key in ("simulation", "nutrition", "water", "energy", "roles"):
        report = reports.get(key)
        if report and _status_of(report) == "fail":
            blockers.append(f"{key}:{report.get('id', report.get('kind'))} failed")

    for report in scenarios:
        if _status_of(report) == "fail":
            blockers.append(f"scenario:{report.get('scenario', report.get('id'))} failed")
        for gate in report.get("survival_critical_gate_failures", []):
            blockers.append(f"scenario:{report.get('scenario', report.get('id'))} failed {gate}")

    return sorted(set(blockers))


def _noncritical_warnings(
    reports: dict[str, Any],
    scenarios: list[dict[str, Any]],
) -> list[str]:
    warnings: list[str] = []
    for key, report in sorted(reports.items()):
        if not report:
            continue
        status = _status_of(report)
        if status == "warn":
            warnings.append(f"{key}:{report.get('id', report.get('kind'))} is warning")
        warnings.extend(f"{key}:{item}" for item in _extract_warnings(report))
    for report in scenarios:
        if _status_of(report) == "warn":
            warnings.append(f"scenario:{report.get('scenario', report.get('id'))} is warning")
        warnings.extend(f"scenario:{report.get('scenario', report.get('id'))}:{item}" for item in report.get("bottlenecks", []))
    return sorted(set(warnings))


def _required_redesigns(
    reports: dict[str, Any],
    scenarios: list[dict[str, Any]],
    blockers: list[str],
) -> list[str]:
    redesigns: list[str] = []
    for key, report in sorted(reports.items()):
        if not report:
            continue
        redesigns.extend(f"{key}:{item}" for item in _extract_recommendations(report))
    for report in scenarios:
        redesigns.extend(
            f"scenario:{report.get('scenario', report.get('id'))}:{item}"
            for item in report.get("recommended_redesigns", [])
        )
    if blockers and not redesigns:
        redesigns.append("Resolve all survival-critical blockers before any pilot review.")
    return sorted(set(redesigns))


def _top_risks(reports: dict[str, Any], scenarios: list[dict[str, Any]]) -> list[str]:
    risks: list[str] = []
    for key in ("water", "energy", "roles", "nutrition", "simulation"):
        report = reports.get(key)
        if not report:
            continue
        for item in report.get("bottlenecks", [])[:3]:
            risks.append(f"{key}:{item}")
        for item in report.get("burnout_warnings", [])[:3]:
            risks.append(f"{key}:{item}")
        for item in report.get("water_safety_warnings", [])[:3]:
            risks.append(f"{key}:{item}")
        for item in report.get("energy_safety_warnings", [])[:3]:
            risks.append(f"{key}:{item}")
        for item in report.get("dietary_risk_warnings", [])[:3]:
            risks.append(f"{key}:{item}")
    for report in scenarios:
        for item in report.get("bottlenecks", [])[:2]:
            risks.append(f"scenario:{report.get('scenario', report.get('id'))}:{item}")
    return list(dict.fromkeys(risks))[:12]


def _next_sprint_recommendations(blockers: list[str], warnings: list[str], top_risks: list[str]) -> list[str]:
    recommendations: list[str] = []
    joined = " ".join(blockers + warnings + top_risks).lower()
    if "water" in joined or "drought" in joined:
        recommendations.append("Prioritize redesigning water storage, backup supply, and drought demand reduction.")
    if "energy" in joined or "outage" in joined:
        recommendations.append("Prioritize battery, backup energy, and critical-load reduction planning.")
    if "role" in joined or "burnout" in joined or "steward" in joined:
        recommendations.append("Prioritize training backups and rebalancing role rotation before adding new infrastructure.")
    if "food" in joined or "nutrition" in joined:
        recommendations.append("Improve local food share and fallback procurement evidence.")
    if not recommendations:
        recommendations.append("Add jurisdictional compliance and professional review evidence before pilot consideration.")
    return recommendations


def _inputs(
    compiled_plan: dict[str, Any],
    reports: dict[str, Any],
    scenarios: list[dict[str, Any]],
) -> dict[str, Any]:
    return {
        "compiled_plan": compiled_plan.get("id"),
        "reports": {key: value.get("id") if value else None for key, value in sorted(reports.items())},
        "scenarios": [report.get("id") for report in scenarios],
    }


def _evidence_hash(
    compiled_plan: dict[str, Any],
    reports: dict[str, Any],
    scenarios: list[dict[str, Any]],
) -> str:
    payload = _inputs(compiled_plan, reports, scenarios)
    serialized = json.dumps(payload, sort_keys=True)
    return hashlib.sha1(serialized.encode("utf-8")).hexdigest()[:8]


def _overall_status(
    blockers: list[str],
    warnings: list[str],
    subsystem_statuses: dict[str, dict[str, Any]],
) -> str:
    if blockers or any(item["status"] == "fail" and item["survival_critical"] for item in subsystem_statuses.values()):
        return "fail"
    if warnings or any(item["status"] == "warn" for item in subsystem_statuses.values()):
        return "warn"
    return "pass"


def _promotion_decision(overall_status: str) -> str:
    if overall_status == "fail":
        return "do_not_promote"
    if overall_status == "warn":
        return "revise_before_pilot"
    return "candidate_for_review"


def _status_of(report: dict[str, Any]) -> str:
    if report.get("kind") == "GateReport":
        return "pass" if report.get("promotion_allowed") else "fail"
    return report.get("status", "unknown")


def _extract_warnings(report: dict[str, Any]) -> list[str]:
    values: list[str] = []
    for field in (
        "bottlenecks",
        "dietary_risk_warnings",
        "water_safety_warnings",
        "energy_safety_warnings",
        "burnout_warnings",
        "noncritical_warnings",
    ):
        values.extend(str(item) for item in report.get(field, []))
    return values


def _extract_recommendations(report: dict[str, Any]) -> list[str]:
    values: list[str] = []
    for field in (
        "gate_recommendations",
        "fallback_procurement_needs",
        "redesign_recommendations",
        "recommended_redesigns",
        "next_sprint_recommendations",
    ):
        values.extend(str(item) for item in report.get(field, []))
    return values
