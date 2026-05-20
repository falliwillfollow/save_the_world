from __future__ import annotations

import math
from typing import Any


def generate_tradeoff_scale_report(
    compiled_plan: dict[str, Any],
    candidate_matrix: dict[str, Any],
    patterns_by_id: dict[str, dict[str, Any]],
    scale_profile: dict[str, Any],
) -> dict[str, Any]:
    base_households = int(scale_profile.get("base_households", compiled_plan.get("site_summary", {}).get("households", 1)))
    base_population = int(compiled_plan.get("site_summary", {}).get("population_target", base_households * 2))
    scale_targets = [_scale_target(target, base_households, base_population) for target in scale_profile["targets"]]
    candidate_results = [
        _candidate_scale_result(candidate, scale_targets, patterns_by_id)
        for candidate in candidate_matrix.get("candidates", [])
    ]
    status = "ready_with_warnings" if candidate_results and scale_targets else "not_ready"
    return {
        "kind": "TradeoffScaleReport",
        "id": f"{compiled_plan['id']}_{scale_profile['id']}_tradeoff_scale",
        "compiled_plan": compiled_plan["id"],
        "candidate_matrix": candidate_matrix["id"],
        "scale_profile": scale_profile["id"],
        "generated_by": "ciac.scale.v0",
        "provisional": True,
        "status": status,
        "scale_targets": scale_targets,
        "objective_leaders": _objective_leaders(candidate_matrix.get("candidates", [])),
        "candidate_scale_results": candidate_results,
        "viewer_candidate_summary": _viewer_candidate_summary(candidate_results),
        "metric_updates": _metric_updates(status),
        "next_actions": _next_actions(status),
        "unknowns": [
            "Scale results multiply declared provisional parameters; they are not site plans, engineering estimates, or procurement quotes.",
            "Step and shared-capacity scaling are topology hints for visualization and later optimization, not proof of buildability.",
            *scale_profile.get("unknowns", []),
        ],
    }


def _scale_target(target: dict[str, Any], base_households: int, base_population: int) -> dict[str, Any]:
    households = int(target["households"])
    factor = households / max(1, base_households)
    return {
        "households": households,
        "label": target["label"],
        "scale_factor": round(factor, 3),
        "estimated_population": int(round(base_population * factor)),
        "notes": target["notes"],
        "provisional": True,
    }


def _candidate_scale_result(
    candidate: dict[str, Any],
    scale_targets: list[dict[str, Any]],
    patterns_by_id: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    parameter_results = [
        _scale_parameter(parameter, scale_targets, patterns_by_id)
        for parameter in candidate.get("parameter_values", [])
    ]
    return {
        "candidate": candidate["id"],
        "status": candidate["status"],
        "aggregate_score": candidate["aggregate_score"],
        "objective_summary": _objective_summary(candidate),
        "tradeoffs": candidate.get("tradeoffs", []),
        "scale_parameters": parameter_results,
        "scale_pressure": _scale_pressure(parameter_results),
        "best_for": _best_for(candidate),
        "provisional": True,
    }


def _scale_parameter(
    parameter: dict[str, Any],
    scale_targets: list[dict[str, Any]],
    patterns_by_id: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    pattern = patterns_by_id.get(parameter["pattern_id"], {})
    scaling = pattern.get("optimization", {}).get("scaling", {})
    scaling_mode = scaling.get("mode", "manual_review")
    values = []
    for target in scale_targets:
        scaled_value, repeat_units = _scaled_value(float(parameter["value"]), float(target["scale_factor"]), scaling_mode)
        values.append(
            {
                "households": target["households"],
                "scale_factor": target["scale_factor"],
                "scaled_value": round(scaled_value, 3),
                "repeat_units": repeat_units,
                "unit": parameter["unit"],
                "provisional": True,
            }
        )
    return {
        "pattern_id": parameter["pattern_id"],
        "parameter_id": parameter["parameter_id"],
        "base_value": parameter["value"],
        "unit": parameter["unit"],
        "scaling_mode": scaling_mode,
        "review_required": parameter["review_required"],
        "affects": parameter["affects"],
        "values": values,
        "provisional": True,
    }


def _scaled_value(base_value: float, factor: float, scaling_mode: str) -> tuple[float, int]:
    if scaling_mode == "step":
        repeat_units = max(1, math.ceil(factor))
        return base_value * repeat_units, repeat_units
    if scaling_mode in {"linear", "shared_capacity"}:
        return base_value * factor, 1
    return base_value, 1


def _objective_summary(candidate: dict[str, Any]) -> dict[str, Any]:
    return {
        item["metric"]: {
            "score": item["score"],
            "weighted_score": item["weighted_score"],
            "direction": item["direction"],
        }
        for item in candidate.get("objective_scores", [])
    }


def _objective_leaders(candidates: list[dict[str, Any]]) -> list[dict[str, Any]]:
    metrics = sorted({score["metric"] for candidate in candidates for score in candidate.get("objective_scores", [])})
    leaders = []
    for metric in metrics:
        scored = [
            (candidate["id"], next(score for score in candidate.get("objective_scores", []) if score["metric"] == metric))
            for candidate in candidates
            if any(score["metric"] == metric for score in candidate.get("objective_scores", []))
        ]
        if not scored:
            continue
        best_candidate, best_score = max(scored, key=lambda item: (float(item[1]["score"]), item[0]))
        leaders.append(
            {
                "metric": metric,
                "candidate": best_candidate,
                "score": best_score["score"],
                "direction": best_score["direction"],
                "provisional": True,
            }
        )
    return leaders


def _scale_pressure(parameter_results: list[dict[str, Any]]) -> list[dict[str, Any]]:
    pressures = []
    for parameter in parameter_results:
        final = parameter["values"][-1] if parameter["values"] else {}
        pressures.append(
            {
                "pattern_id": parameter["pattern_id"],
                "parameter_id": parameter["parameter_id"],
                "households": final.get("households", 0),
                "scaled_value": final.get("scaled_value", 0),
                "unit": parameter["unit"],
                "review_required": parameter["review_required"],
                "provisional": True,
            }
        )
    return pressures


def _viewer_candidate_summary(candidate_results: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "candidate": result["candidate"],
            "status": result["status"],
            "aggregate_score": result["aggregate_score"],
            "best_for": result["best_for"],
            "max_scale_households": max((item["households"] for pressure in result["scale_pressure"] for item in [pressure]), default=0),
            "top_tradeoff": result["tradeoffs"][0] if result["tradeoffs"] else "",
            "review_required_parameter_count": sum(1 for item in result["scale_pressure"] if item["review_required"]),
            "provisional": True,
        }
        for result in candidate_results
    ]


def _best_for(candidate: dict[str, Any]) -> list[str]:
    strong = [
        score["metric"]
        for score in candidate.get("objective_scores", [])
        if float(score.get("score", 0.0)) >= 0.75
    ]
    return strong or ["balanced_visibility"]


def _metric_updates(status: str) -> dict[str, Any]:
    if status == "not_ready":
        return {
            "inspectable_simulation_proof_of_concept": "85%",
            "mature_commune_virtualization_data_contract": "75%",
            "faithful_pattern_optimization_engine": "65%",
            "rationale": "Scale and tradeoff report could not be generated from candidate matrix inputs.",
        }
    return {
        "inspectable_simulation_proof_of_concept": "90%",
        "mature_commune_virtualization_data_contract": "85%",
        "faithful_pattern_optimization_engine": "80%",
        "rationale": "Chunk C explains candidate tradeoffs and scale implications across the declared household targets.",
    }


def _next_actions(status: str) -> list[str]:
    if status == "not_ready":
        return ["Regenerate candidate matrix and scale profile before attempting optimizer-loop work."]
    return [
        "Proceed to Chunk D: deterministic optimizer loop over candidate configurations.",
        "Expose viewer_candidate_summary in the visualization layer before freezing the contract.",
        "Keep scale outputs provisional until topology, cost, engineering, and governance review exist.",
    ]

