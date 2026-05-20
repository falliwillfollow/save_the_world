from __future__ import annotations

from typing import Any


REQUIRED_OPTIMIZATION_PATTERNS = {
    "water": "emergency_water_reserve",
    "food": "staple_food_reserve",
    "energy": "critical_load_reserve",
}


def evaluate_optimization_readiness(
    patterns_by_id: dict[str, dict[str, Any]],
    optimization_profile: dict[str, Any],
) -> dict[str, Any]:
    pattern_readiness = [_pattern_readiness(domain, pattern_id, patterns_by_id.get(pattern_id)) for domain, pattern_id in REQUIRED_OPTIMIZATION_PATTERNS.items()]
    locked_parameters = [
        {
            "pattern_id": pattern_id,
            "parameter_id": locked["id"],
            "path": locked["path"],
            "review_dependency": locked["review_dependency"],
            "reason": locked["reason"],
            "provisional": True,
        }
        for pattern_id, pattern in sorted(patterns_by_id.items())
        for locked in pattern.get("optimization", {}).get("locked_parameters", [])
    ]
    gaps = _readiness_gaps(pattern_readiness, optimization_profile, locked_parameters)
    status = _status(gaps, locked_parameters)
    tunable_pattern_count = sum(1 for item in pattern_readiness if item["status"] in {"ready", "ready_with_warnings"})
    return {
        "kind": "OptimizationReadinessReport",
        "id": f"{optimization_profile['id']}_optimization_readiness",
        "generated_by": "ciac.optimization_readiness.v0",
        "provisional": True,
        "status": status,
        "pattern_count": len(patterns_by_id),
        "tunable_pattern_count": tunable_pattern_count,
        "objective_count": len(optimization_profile.get("objectives", [])),
        "constraint_count": len(optimization_profile.get("constraints", [])),
        "pattern_readiness": pattern_readiness,
        "locked_parameters": locked_parameters,
        "readiness_gaps": gaps,
        "metric_updates": _metric_updates(status),
        "next_actions": _next_actions(status, gaps),
        "unknowns": [
            "Optimization readiness is a data-contract check, not an optimizer or a real-world recommendation.",
            "Tunable parameters are provisional search bounds; they are not engineering, public-health, legal, or cost estimates.",
            "Locked parameters must stay explicit until qualified review evidence exists.",
        ],
    }


def _pattern_readiness(domain: str, pattern_id: str, pattern: dict[str, Any] | None) -> dict[str, Any]:
    if pattern is None:
        return {
            "domain": domain,
            "pattern_id": pattern_id,
            "status": "not_ready",
            "tunable_parameter_count": 0,
            "locked_parameter_count": 0,
            "objectives": [],
            "scaling_mode": "missing",
            "evidence": "Required pattern is missing.",
            "provisional": True,
        }
    optimization = pattern.get("optimization", {})
    tunables = optimization.get("tunable_parameters", [])
    locked = optimization.get("locked_parameters", [])
    scaling = optimization.get("scaling", {})
    issues = []
    if not tunables:
        issues.append("no tunable parameters")
    if not locked:
        issues.append("no locked review-bound parameters")
    if not scaling:
        issues.append("no scaling metadata")
    status = "not_ready" if issues else "ready_with_warnings"
    evidence = "; ".join(issues) if issues else f"{len(tunables)} tunable parameter(s), {len(locked)} locked parameter(s), {scaling.get('mode')} scaling."
    return {
        "domain": domain,
        "pattern_id": pattern_id,
        "status": status,
        "tunable_parameter_count": len(tunables),
        "locked_parameter_count": len(locked),
        "objectives": optimization.get("objectives", []),
        "scaling_mode": scaling.get("mode", "missing"),
        "evidence": evidence,
        "provisional": True,
    }


def _readiness_gaps(
    pattern_readiness: list[dict[str, Any]],
    optimization_profile: dict[str, Any],
    locked_parameters: list[dict[str, Any]],
) -> list[str]:
    gaps = []
    for item in pattern_readiness:
        if item["status"] == "not_ready":
            gaps.append(f"{item['pattern_id']} is not optimization-ready: {item['evidence']}")
    if not optimization_profile.get("objectives"):
        gaps.append("Optimization profile has no objectives.")
    if not optimization_profile.get("constraints"):
        gaps.append("Optimization profile has no constraints.")
    hard_constraints = [constraint for constraint in optimization_profile.get("constraints", []) if constraint.get("severity") == "hard"]
    if not hard_constraints:
        gaps.append("Optimization profile has no hard constraints.")
    if not locked_parameters:
        gaps.append("No locked review-bound parameters were found.")
    return gaps


def _status(gaps: list[str], locked_parameters: list[dict[str, Any]]) -> str:
    if gaps:
        return "not_ready"
    if locked_parameters:
        return "ready_with_warnings"
    return "ready"


def _metric_updates(status: str) -> dict[str, Any]:
    if status == "not_ready":
        return {
            "inspectable_simulation_proof_of_concept": "75%",
            "mature_commune_virtualization_data_contract": "60%",
            "faithful_pattern_optimization_engine": "35-45%",
            "rationale": "Readiness gaps remain before optimization metrics can advance.",
        }
    return {
        "inspectable_simulation_proof_of_concept": "80%",
        "mature_commune_virtualization_data_contract": "68%",
        "faithful_pattern_optimization_engine": "50%",
        "rationale": "Chunk A readiness metadata exists for the minimum water, food, and energy reserve patterns.",
    }


def _next_actions(status: str, gaps: list[str]) -> list[str]:
    if status == "not_ready":
        return [f"Close readiness gap: {gap}" for gap in gaps[:4]]
    return [
        "Proceed to Chunk B: generate a small candidate plan matrix from declared pattern variants.",
        "Keep locked review-bound parameters visible in every generated candidate.",
        "Do not treat readiness metadata as real-world engineering or cost optimization.",
    ]

