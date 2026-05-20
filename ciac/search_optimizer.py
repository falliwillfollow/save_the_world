from __future__ import annotations

import copy
from itertools import product
from typing import Any

from .candidates import (
    _aggregate_score,
    _apply_tunable,
    _baseline_summary,
    _candidate_value,
    _constraint_results,
    _objective_scores,
    _parameter_value,
    _scenario_result,
    _selected_locked_parameters,
    _selected_tunables,
    _tradeoffs,
)
from .optimizer import _constraint_explanations, _sensitivity_checks
from .simulation import simulate


SEARCH_LEVELS = ("lean", "current", "balanced", "max")


def optimize_search(
    compiled_plan: dict[str, Any],
    patterns_by_id: dict[str, dict[str, Any]],
    optimization_profile: dict[str, Any],
    scenarios: list[dict[str, Any]] | None = None,
    review_status: dict[str, Any] | None = None,
    baseline_days: int = 365,
    top_count: int = 10,
) -> dict[str, Any]:
    scenarios = scenarios or []
    tunables = _selected_tunables(compiled_plan, patterns_by_id)
    locked = _selected_locked_parameters(compiled_plan, patterns_by_id)
    families = _family_tunables(tunables)
    candidate_vectors = _candidate_vectors(families)
    candidates = [
        _search_candidate(
            compiled_plan,
            family_tunables=families,
            locked=locked,
            optimization_profile=optimization_profile,
            scenarios=scenarios,
            review_status=review_status,
            baseline_days=baseline_days,
            sequence=index,
            vector=vector,
        )
        for index, vector in enumerate(candidate_vectors, start=1)
    ]
    ranked = sorted(candidates, key=lambda item: (item["hard_constraint_failures"], -float(item["aggregate_score"]), item["id"]))
    viable = [candidate for candidate in ranked if candidate["status"] == "viable"]
    rejected = [candidate for candidate in ranked if candidate["status"] == "rejected"]
    selected = viable[0]["id"] if viable else ""
    top_candidates = ranked[:top_count]
    status = "ready_with_warnings" if selected else "not_ready"
    optimized_for_explanations = [
        {
            "candidate": candidate["id"],
            "status": candidate["status"],
            "hard_constraint_failures": candidate["hard_constraint_failures"],
            "soft_constraint_warnings": sum(
                1
                for constraint in candidate.get("constraint_results", [])
                if constraint.get("severity") == "soft" and constraint.get("status") != "pass"
            ),
            "constraint_results": candidate.get("constraint_results", []),
        }
        for candidate in top_candidates
    ]
    return {
        "kind": "SearchOptimizerReport",
        "id": f"{compiled_plan['id']}_{optimization_profile['id']}_search_optimizer",
        "compiled_plan": compiled_plan["id"],
        "optimization_profile": optimization_profile["id"],
        "generated_by": "ciac.search_optimizer.v0",
        "provisional": True,
        "status": status,
        "search_space": _search_space(families),
        "candidate_count": len(candidates),
        "viable_candidate_count": len(viable),
        "rejected_candidate_count": len(rejected),
        "selected_candidate": selected,
        "top_candidates": top_candidates,
        "binding_constraints": _binding_constraints(candidates),
        "locked_assumptions": locked,
        "sensitivity_checks": _sensitivity_checks(top_candidates, optimization_profile, selected),
        "constraint_explanations": _constraint_explanations(optimized_for_explanations),
        "metric_updates": _metric_updates(status),
        "next_actions": _next_actions(status),
        "unknowns": [
            "Search optimizer explores declared reserve-family parameter levels only; it is not a full solver or technology recommender.",
            "Objective scores remain provisional planning signals and are not sourced engineering, cost, labor, legal, or health calculations.",
            "Locked assumptions identify claims CIaC must not optimize away without review evidence.",
        ],
    }


def _family_tunables(tunables: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    families: dict[str, list[dict[str, Any]]] = {}
    for tunable in tunables:
        families.setdefault(tunable["pattern_id"], []).append(tunable)
    return {family: sorted(items, key=lambda item: item["id"]) for family, items in sorted(families.items())}


def _candidate_vectors(families: dict[str, list[dict[str, Any]]]) -> list[dict[str, str]]:
    family_ids = list(families)
    vectors = []
    for levels in product(SEARCH_LEVELS, repeat=len(family_ids)):
        vectors.append(dict(zip(family_ids, levels)))
    return vectors


def _search_candidate(
    compiled_plan: dict[str, Any],
    family_tunables: dict[str, list[dict[str, Any]]],
    locked: list[dict[str, Any]],
    optimization_profile: dict[str, Any],
    scenarios: list[dict[str, Any]],
    review_status: dict[str, Any] | None,
    baseline_days: int,
    sequence: int,
    vector: dict[str, str],
) -> dict[str, Any]:
    plan = copy.deepcopy(compiled_plan)
    candidate_id = f"search_{sequence:03d}"
    plan["id"] = f"{compiled_plan['id']}_{candidate_id}"
    parameter_values = []
    for family, level in vector.items():
        for tunable in family_tunables[family]:
            value = _level_value(plan, tunable, level)
            _apply_tunable(plan, tunable, value)
            parameter_values.append(_parameter_value(tunable, value, level))

    baseline = simulate(plan, days=baseline_days, review_status=review_status)
    scenario_results = [_scenario_result(plan, scenario, review_status) for scenario in scenarios]
    constraints = _constraint_results(optimization_profile, baseline, scenario_results, locked)
    hard_failures = sum(1 for constraint in constraints if constraint["severity"] == "hard" and constraint["status"] == "fail")
    objective_scores = _objective_scores(optimization_profile, parameter_values, scenario_results, hard_failures, locked)
    aggregate_score = _aggregate_score(objective_scores)
    status = "viable" if hard_failures == 0 else "rejected"
    return {
        "id": candidate_id,
        "label": _label(vector),
        "status": status,
        "candidate_plan_id": plan["id"],
        "family_levels": vector,
        "parameter_values": parameter_values,
        "parameter_deltas": _parameter_deltas(compiled_plan, parameter_values, family_tunables),
        "baseline_summary": _baseline_summary(baseline),
        "scenario_results": scenario_results,
        "constraint_results": constraints,
        "hard_constraint_failures": hard_failures,
        "objective_scores": objective_scores,
        "aggregate_score": aggregate_score,
        "selection_rationale": _selection_rationale(vector, aggregate_score, hard_failures),
        "tradeoffs": _tradeoffs(parameter_values, scenario_results, locked),
        "provisional": True,
    }


def _level_value(plan: dict[str, Any], tunable: dict[str, Any], level: str) -> float:
    if level == "lean":
        minimum = float(tunable["min"])
        current = float(_candidate_value(plan, tunable, "current"))
        return min(current, minimum)
    if level in {"current", "balanced", "max"}:
        return _candidate_value(plan, tunable, level)
    raise ValueError(f"Unsupported search level: {level}")


def _parameter_deltas(
    compiled_plan: dict[str, Any],
    parameter_values: list[dict[str, Any]],
    family_tunables: dict[str, list[dict[str, Any]]],
) -> list[dict[str, Any]]:
    tunables_by_key = {
        (tunable["pattern_id"], tunable["id"]): tunable
        for tunables in family_tunables.values()
        for tunable in tunables
    }
    deltas = []
    for parameter in parameter_values:
        tunable = tunables_by_key[(parameter["pattern_id"], parameter["parameter_id"])]
        baseline_plan = copy.deepcopy(compiled_plan)
        current = _candidate_value(baseline_plan, tunable, "current")
        value = float(parameter["value"])
        deltas.append(
            {
                "pattern_id": parameter["pattern_id"],
                "parameter_id": parameter["parameter_id"],
                "from_value": round(current, 3),
                "to_value": round(value, 3),
                "delta": round(value - current, 3),
                "unit": parameter["unit"],
                "provisional": True,
            }
        )
    return deltas


def _search_space(families: dict[str, list[dict[str, Any]]]) -> dict[str, Any]:
    return {
        "family_count": len(families),
        "levels": list(SEARCH_LEVELS),
        "families": [
            {
                "pattern_id": family,
                "tunable_parameters": [tunable["id"] for tunable in tunables],
                "level_count": len(SEARCH_LEVELS),
                "provisional": True,
            }
            for family, tunables in families.items()
        ],
        "candidate_count": len(SEARCH_LEVELS) ** len(families),
        "provisional": True,
    }


def _label(vector: dict[str, str]) -> str:
    return " | ".join(f"{family}:{level}" for family, level in vector.items())


def _selection_rationale(vector: dict[str, str], aggregate_score: float, hard_failures: int) -> str:
    if hard_failures:
        return "Rejected because hard constraints failed under this family-level parameter combination."
    return f"Viable family-level combination scored {aggregate_score}: {_label(vector)}."


def _binding_constraints(candidates: list[dict[str, Any]]) -> list[dict[str, Any]]:
    constraints: dict[str, dict[str, Any]] = {}
    for candidate in candidates:
        for constraint in candidate.get("constraint_results", []):
            if constraint.get("status") == "pass":
                continue
            constraint_id = constraint["id"]
            current = constraints.setdefault(
                constraint_id,
                {
                    "constraint": constraint_id,
                    "severity": constraint["severity"],
                    "status_counts": {},
                    "candidate_count": 0,
                    "description": constraint["description"],
                    "provisional": True,
                },
            )
            current["candidate_count"] += 1
            current["status_counts"][constraint["status"]] = current["status_counts"].get(constraint["status"], 0) + 1
    return sorted(constraints.values(), key=lambda item: (item["severity"] != "hard", item["constraint"]))


def _metric_updates(status: str) -> dict[str, Any]:
    if status == "not_ready":
        return {
            "inspectable_simulation_proof_of_concept": "100%",
            "mature_commune_virtualization_data_contract": "100%",
            "faithful_pattern_optimization_engine": "95%",
            "rationale": "Bounded search could not select a viable candidate without hard constraint failure.",
        }
    return {
        "inspectable_simulation_proof_of_concept": "100%",
        "mature_commune_virtualization_data_contract": "100%",
        "faithful_pattern_optimization_engine": "98%",
        "rationale": "Sprint 47 adds deterministic family-level search across water, food, and energy reserve tunables.",
    }


def _next_actions(status: str) -> list[str]:
    if status == "not_ready":
        return [
            "Inspect rejected family-level combinations before expanding the search space.",
            "Do not relax survival-critical constraints to manufacture a winner.",
        ]
    return [
        "Use the search report to decide whether the authored current plan remains preferable under broader reserve-family combinations.",
        "Add sourced objective calibration before claiming optimization beyond provisional planning signals.",
        "Expand from reserve-family tuning to optional pattern families only when the bundle contract can preserve the added complexity.",
    ]
