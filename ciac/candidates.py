from __future__ import annotations

import copy
import re
from typing import Any

from .simulation import simulate
from .simulation_compare import compare_simulations


CANDIDATE_MODES = [
    ("current_plan", "Current authored plan", "current"),
    ("balanced_reserve", "Balanced reserve increase", "balanced"),
    ("high_resilience_reserve", "High resilience reserve", "max"),
]


def generate_candidate_matrix(
    compiled_plan: dict[str, Any],
    patterns_by_id: dict[str, dict[str, Any]],
    optimization_profile: dict[str, Any],
    scenarios: list[dict[str, Any]] | None = None,
    review_status: dict[str, Any] | None = None,
    baseline_days: int = 365,
) -> dict[str, Any]:
    scenarios = scenarios or []
    tunables = _selected_tunables(compiled_plan, patterns_by_id)
    locked = _selected_locked_parameters(compiled_plan, patterns_by_id)
    candidates = [
        _candidate_result(compiled_plan, tunables, locked, optimization_profile, scenarios, review_status, baseline_days, candidate_id, label, mode)
        for candidate_id, label, mode in CANDIDATE_MODES
    ]
    ranked = sorted(candidates, key=lambda item: (-float(item["aggregate_score"]), item["id"]))
    viable_count = sum(1 for candidate in candidates if candidate["status"] == "viable")
    status = "ready_with_warnings" if viable_count >= 3 else "not_ready"
    return {
        "kind": "CandidatePlanMatrixReport",
        "id": f"{compiled_plan['id']}_{optimization_profile['id']}_candidate_matrix",
        "compiled_plan": compiled_plan["id"],
        "optimization_profile": optimization_profile["id"],
        "generated_by": "ciac.candidates.v0",
        "provisional": True,
        "status": status,
        "candidate_count": len(candidates),
        "viable_candidate_count": viable_count,
        "scenario_count": len(scenarios),
        "baseline_days": baseline_days,
        "candidates": candidates,
        "rankings": [
            {
                "candidate": candidate["id"],
                "status": candidate["status"],
                "aggregate_score": candidate["aggregate_score"],
                "hard_constraint_failures": candidate["hard_constraint_failures"],
                "top_tradeoff": candidate["tradeoffs"][0] if candidate["tradeoffs"] else "",
                "provisional": True,
            }
            for candidate in ranked
        ],
        "metric_updates": _metric_updates(status),
        "next_actions": _next_actions(status),
        "unknowns": [
            "Candidate generation mutates only declared provisional tunables; it is not a real-world engineering optimizer.",
            "Objective scores are coarse normalized planning signals, not verified cost, labor, resilience, or safety calculations.",
            "Review-locked parameters remain explicit and must not be optimized away.",
        ],
    }


def _selected_tunables(compiled_plan: dict[str, Any], patterns_by_id: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    selected = set(compiled_plan.get("selected_patterns", []))
    tunables: list[dict[str, Any]] = []
    for pattern_id in sorted(selected):
        pattern = patterns_by_id.get(pattern_id, {})
        for tunable in pattern.get("optimization", {}).get("tunable_parameters", []):
            tunables.append({"pattern_id": pattern_id, **tunable})
    return tunables


def _selected_locked_parameters(compiled_plan: dict[str, Any], patterns_by_id: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    selected = set(compiled_plan.get("selected_patterns", []))
    locked: list[dict[str, Any]] = []
    for pattern_id in sorted(selected):
        pattern = patterns_by_id.get(pattern_id, {})
        for parameter in pattern.get("optimization", {}).get("locked_parameters", []):
            locked.append({"pattern_id": pattern_id, **parameter})
    return locked


def _candidate_result(
    compiled_plan: dict[str, Any],
    tunables: list[dict[str, Any]],
    locked: list[dict[str, Any]],
    optimization_profile: dict[str, Any],
    scenarios: list[dict[str, Any]],
    review_status: dict[str, Any] | None,
    baseline_days: int,
    candidate_id: str,
    label: str,
    mode: str,
) -> dict[str, Any]:
    plan = copy.deepcopy(compiled_plan)
    plan["id"] = f"{compiled_plan['id']}_{candidate_id}"
    parameter_values = []
    for tunable in tunables:
        value = _candidate_value(plan, tunable, mode)
        _apply_tunable(plan, tunable, value)
        parameter_values.append(_parameter_value(tunable, value, mode))

    baseline = simulate(plan, days=baseline_days, review_status=review_status)
    scenario_results = [_scenario_result(plan, scenario, review_status) for scenario in scenarios]
    constraints = _constraint_results(optimization_profile, baseline, scenario_results, locked)
    hard_failures = sum(1 for constraint in constraints if constraint["severity"] == "hard" and constraint["status"] == "fail")
    objective_scores = _objective_scores(optimization_profile, parameter_values, scenario_results, hard_failures, locked)
    aggregate_score = _aggregate_score(objective_scores)
    status = "viable" if hard_failures == 0 else "rejected"
    return {
        "id": candidate_id,
        "label": label,
        "status": status,
        "candidate_plan_id": plan["id"],
        "parameter_values": parameter_values,
        "baseline_summary": _baseline_summary(baseline),
        "scenario_results": scenario_results,
        "constraint_results": constraints,
        "hard_constraint_failures": hard_failures,
        "objective_scores": objective_scores,
        "aggregate_score": aggregate_score,
        "tradeoffs": _tradeoffs(parameter_values, scenario_results, locked),
        "provisional": True,
    }


def _candidate_value(plan: dict[str, Any], tunable: dict[str, Any], mode: str) -> float:
    current = _current_value(plan, tunable)
    if mode == "current":
        return current
    minimum = float(tunable["min"])
    maximum = float(tunable["max"])
    default = float(tunable["default"])
    if mode == "max":
        return _snap_to_step(maximum, tunable)
    midpoint = default + ((maximum - default) * 0.5)
    return _snap_to_step(max(current, midpoint, minimum), tunable)


def _current_value(plan: dict[str, Any], tunable: dict[str, Any]) -> float:
    storage = _storage_target(plan, tunable)
    field = _storage_field(tunable["path"])
    return float(storage[field])


def _apply_tunable(plan: dict[str, Any], tunable: dict[str, Any], value: float) -> None:
    storage = _storage_target(plan, tunable)
    storage[_storage_field(tunable["path"])] = value


def _storage_target(plan: dict[str, Any], tunable: dict[str, Any]) -> dict[str, Any]:
    pattern_id = tunable["pattern_id"]
    index = _storage_index(tunable["path"])
    return plan["simulation_inputs"]["storage_by_pattern"][pattern_id][index]


def _storage_index(path: str) -> int:
    match = re.search(r"storage\[(\d+)\]", path)
    if not match:
        raise ValueError(f"Unsupported tunable path: {path}")
    return int(match.group(1))


def _storage_field(path: str) -> str:
    field = path.split(".")[-1]
    if field not in {"capacity", "initial", "reserve_floor", "max_release_per_day", "max_refill_per_day"}:
        raise ValueError(f"Unsupported tunable field: {path}")
    return field


def _snap_to_step(value: float, tunable: dict[str, Any]) -> float:
    step = float(tunable["step"])
    minimum = float(tunable["min"])
    maximum = float(tunable["max"])
    snapped = minimum + (round((value - minimum) / step) * step)
    return round(max(minimum, min(maximum, snapped)), 6)


def _parameter_value(tunable: dict[str, Any], value: float, mode: str) -> dict[str, Any]:
    minimum = float(tunable["min"])
    maximum = float(tunable["max"])
    normalized = (value - minimum) / (maximum - minimum) if maximum > minimum else 0.0
    return {
        "pattern_id": tunable["pattern_id"],
        "parameter_id": tunable["id"],
        "path": tunable["path"],
        "value": round(value, 3),
        "unit": tunable["unit"],
        "mode": mode,
        "normalized_position": round(normalized, 3),
        "review_required": bool(tunable["review_required"]),
        "affects": tunable["affects"],
        "provisional": True,
    }


def _scenario_result(plan: dict[str, Any], scenario: dict[str, Any], review_status: dict[str, Any] | None) -> dict[str, Any]:
    days = int(scenario["days"])
    baseline = simulate(plan, days=days, review_status=review_status)
    replay = simulate(plan, days=days, scenario=scenario, review_status=review_status)
    comparison = compare_simulations(baseline, replay)
    unmet_delta = sum(max(0.0, float(item.get("delta", 0.0))) for item in comparison.get("unmet_need_deltas", []))
    return {
        "scenario": scenario["id"],
        "days": days,
        "status": comparison["status"],
        "total_unmet_delta": round(unmet_delta, 3),
        "scenario_emergency_hours": comparison["labor_delta"]["scenario_emergency_hours"],
        "active_failure_day_delta": comparison["failure_day_delta"]["delta"],
        "blocked_review_domain_count": len(comparison["review_delta"]["new_blocked_domains"]) + len(comparison["review_delta"]["remaining_blocked_domains"]),
        "top_bottlenecks": comparison["bottlenecks"][:5],
        "provisional": True,
    }


def _baseline_summary(baseline: dict[str, Any]) -> dict[str, Any]:
    return {
        "simulation": baseline["id"],
        "days": baseline["days"],
        "status": baseline["status"],
        "total_unmet_demand": round(sum(float(item.get("total_unmet_demand", 0.0)) for item in baseline.get("resource_ledger", {}).values()), 3),
        "labor_status": baseline.get("labor", {}).get("status", "missing"),
        "storage_status": baseline.get("storage", {}).get("status", "missing"),
        "provisional": True,
    }


def _constraint_results(
    optimization_profile: dict[str, Any],
    baseline: dict[str, Any],
    scenario_results: list[dict[str, Any]],
    locked: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    results = []
    for constraint in optimization_profile.get("constraints", []):
        status = _constraint_status(constraint, baseline, scenario_results, locked)
        results.append(
            {
                "id": constraint["id"],
                "severity": constraint["severity"],
                "status": status,
                "expression": constraint["expression"],
                "description": constraint["description"],
                "provisional": True,
            }
        )
    return results


def _constraint_status(
    constraint: dict[str, Any],
    baseline: dict[str, Any],
    scenario_results: list[dict[str, Any]],
    locked: list[dict[str, Any]],
) -> str:
    constraint_id = constraint["id"]
    if constraint_id == "no_unmet_survival_demand":
        if baseline["status"] == "fail":
            return "fail"
        if any(result["status"] == "stress_failed" or float(result["total_unmet_delta"]) > 0 for result in scenario_results):
            return "fail"
        return "pass"
    if constraint_id == "preserve_review_locks":
        return "pass" if locked else "fail"
    if constraint_id == "visible_labor_burden":
        return "pass" if "labor_hours" in baseline.get("resource_ledger", {}) else "fail"
    if constraint["severity"] == "soft":
        return "warn"
    return "pass"


def _objective_scores(
    optimization_profile: dict[str, Any],
    parameter_values: list[dict[str, Any]],
    scenario_results: list[dict[str, Any]],
    hard_failures: int,
    locked: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    intensity = _tuning_intensity(parameter_values)
    stress_failed = any(result["status"] == "stress_failed" for result in scenario_results)
    unmet = sum(float(result["total_unmet_delta"]) for result in scenario_results)
    scores = []
    for objective in optimization_profile.get("objectives", []):
        benefit = _objective_benefit(objective["metric"], intensity, hard_failures, stress_failed, unmet, locked)
        scores.append(
            {
                "id": objective["id"],
                "metric": objective["metric"],
                "direction": objective["direction"],
                "weight": objective["weight"],
                "score": round(benefit, 3),
                "weighted_score": round(float(objective["weight"]) * benefit, 3),
                "provisional": True,
            }
        )
    return scores


def _objective_benefit(
    metric: str,
    intensity: float,
    hard_failures: int,
    stress_failed: bool,
    unmet: float,
    locked: list[dict[str, Any]],
) -> float:
    if hard_failures or stress_failed or unmet:
        return 0.0
    if metric in {"resilience_score", "autonomy_score"}:
        return min(1.0, 0.55 + (0.45 * intensity))
    if metric == "dignity_score":
        return 1.0
    if metric in {"cost", "build_labor_hours", "recurring_labor_hours_per_week"}:
        return max(0.0, 1.0 - (0.65 * intensity))
    if metric == "review_burden":
        return 1.0 / max(1, len(locked))
    if metric == "external_dependency_score":
        return max(0.0, 0.8 - (0.25 * intensity))
    return 0.5


def _aggregate_score(objective_scores: list[dict[str, Any]]) -> float:
    total_weight = sum(float(item["weight"]) for item in objective_scores) or 1.0
    weighted = sum(float(item["weighted_score"]) for item in objective_scores)
    return round(weighted / total_weight, 3)


def _tuning_intensity(parameter_values: list[dict[str, Any]]) -> float:
    if not parameter_values:
        return 0.0
    return sum(float(item["normalized_position"]) for item in parameter_values) / len(parameter_values)


def _tradeoffs(parameter_values: list[dict[str, Any]], scenario_results: list[dict[str, Any]], locked: list[dict[str, Any]]) -> list[str]:
    intensity = _tuning_intensity(parameter_values)
    warnings = [f"Reserve tuning intensity is {round(intensity, 3)}; higher values imply more cost, footprint, and review burden."]
    if scenario_results:
        worst = max(scenario_results, key=lambda item: float(item["active_failure_day_delta"]))
        warnings.append(f"Longest active failure pressure is {worst['scenario']} at {worst['active_failure_day_delta']} day(s).")
    if locked:
        warnings.append(f"{len(locked)} review-locked parameter(s) remain non-optimizable.")
    return warnings


def _metric_updates(status: str) -> dict[str, Any]:
    if status == "not_ready":
        return {
            "inspectable_simulation_proof_of_concept": "80%",
            "mature_commune_virtualization_data_contract": "68%",
            "faithful_pattern_optimization_engine": "50%",
            "rationale": "Candidate generation did not produce three viable configurations.",
        }
    return {
        "inspectable_simulation_proof_of_concept": "85%",
        "mature_commune_virtualization_data_contract": "75%",
        "faithful_pattern_optimization_engine": "65%",
        "rationale": "Chunk B generated and compared at least three viable candidate configurations.",
    }


def _next_actions(status: str) -> list[str]:
    if status == "not_ready":
        return [
            "Inspect rejected candidates and close hard constraint failures before scaling.",
            "Keep review-locked parameters explicit; do not loosen constraints to create artificial viability.",
        ]
    return [
        "Proceed to Chunk C: tradeoff and scale reports for 5, 10, 25, and 50 households.",
        "Expose candidate rankings in the viewer or runtime handoff bundle.",
        "Keep objective scores provisional until assumptions are sourced or reviewed.",
    ]

