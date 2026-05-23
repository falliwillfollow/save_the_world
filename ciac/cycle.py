from __future__ import annotations

import copy
from typing import Any

from .runtime_export import build_runtime_bundle
from .scenarios import run_scenario
from .search_optimizer import optimize_search
from .simulation import simulate


def materialize_search_candidate(
    compiled_plan: dict[str, Any],
    search_optimizer_report: dict[str, Any],
    candidate_id: str | None = None,
    review_status: dict[str, Any] | None = None,
    scenarios: list[dict[str, Any]] | None = None,
    days: int = 365,
    cycle_index: int = 1,
    target_playback_seconds: int = 20,
    authority_mode: str = "operator_directed",
    patterns_by_id: dict[str, dict[str, Any]] | None = None,
    optimization_profile: dict[str, Any] | None = None,
    top_count: int = 10,
) -> dict[str, Any]:
    candidate = _selected_candidate(search_optimizer_report, candidate_id)
    applied_plan = copy.deepcopy(compiled_plan)
    applied_plan["id"] = candidate.get("candidate_plan_id") or f"{compiled_plan['id']}_{candidate['id']}"
    applied_plan.setdefault("metadata", {})
    applied_plan["metadata"]["applied_search_candidate"] = {
        "search_optimizer_report": search_optimizer_report["id"],
        "candidate": candidate["id"],
        "family_levels": candidate.get("family_levels", {}),
        "provisional": True,
    }
    for parameter in candidate.get("parameter_values", []):
        _apply_parameter(applied_plan, parameter)

    baseline = simulate(compiled_plan, days=days, review_status=review_status)
    applied = simulate(applied_plan, days=days, review_status=review_status)
    scenario_runs = _scenario_runs(applied_plan, scenarios or [])
    next_search = _next_search_report(
        applied_plan,
        patterns_by_id,
        optimization_profile,
        scenarios or [],
        review_status,
        days,
        top_count,
    )
    before_after = _before_after(baseline, applied)
    operator_acceptance = _operator_acceptance(candidate, before_after)
    viewer_population_context = _viewer_population_context(compiled_plan, applied_plan)
    runtime = build_runtime_bundle(
        applied_plan,
        applied,
        scenario_runs,
        {
            "compiled_plan": f"{applied_plan['id']}.json",
            "simulation": f"{applied['id']}.json",
            "scenarios": [scenario.get("id", "") for scenario in scenario_runs or []],
        },
    )
    return {
        "kind": "CycleIterationReport",
        "id": f"{compiled_plan['id']}_{candidate['id']}_cycle_{cycle_index:03d}",
        "generated_by": "ciac.cycle.v0",
        "provisional": True,
        "status": _cycle_status(candidate, operator_acceptance),
        "source_compiled_plan": compiled_plan["id"],
        "search_optimizer_report": search_optimizer_report["id"],
        "selected_candidate": candidate["id"],
        "authority": _authority(authority_mode, candidate, operator_acceptance),
        "viewer_population_context": viewer_population_context,
        "cycle": {
            "index": cycle_index,
            "simulated_days": days,
            "target_playback_seconds": target_playback_seconds,
            "provisional": True,
        },
        "artifacts": {
            "applied_plan_id": applied_plan["id"],
            "applied_simulation_id": applied["id"],
            "runtime_bundle_id": runtime["id"],
            "provisional": True,
        },
        "change_summary": _change_summary(candidate),
        "before_after": before_after,
        "operator_acceptance": operator_acceptance,
        "applied_scenarios": _applied_scenario_summary(scenario_runs),
        "review_gates": _review_gates(candidate),
        "applied_plan": applied_plan,
        "applied_simulation": applied,
        "runtime_bundle": runtime,
        "next_search_optimizer_report": next_search,
        "viewer_next_actions": _viewer_next_actions(candidate),
        "unknowns": [
            "Cycle materialization applies declared optimizer parameters only; it is not autonomous construction guidance.",
            "The regenerated runtime bundle is still provisional and must not be treated as legal, engineering, health, safety, or consent approval.",
            "Operator-directed iteration may reduce oversight inside the simulator, but it does not remove real-world review, consent, or safety duties.",
        ],
    }


def _viewer_population_context(compiled_plan: dict[str, Any], applied_plan: dict[str, Any]) -> dict[str, Any]:
    population_context = applied_plan.get("simulation_inputs", {}).get("population_context") or compiled_plan.get("simulation_inputs", {}).get("population_context") or {}
    viewer_context = applied_plan.get("metadata", {}).get("viewer_run_context", {}) or compiled_plan.get("metadata", {}).get("viewer_run_context", {}) or {}
    return {
        "source": str(population_context.get("source") or viewer_context.get("source") or "compiled_plan"),
        "population": int(population_context.get("population", applied_plan.get("site_summary", {}).get("population_target", 0))),
        "household_count": int(population_context.get("household_count", applied_plan.get("site_summary", {}).get("households", 0))),
        "daily_resource_demand_adjustments": {
            "water_liters": round(float(population_context.get("daily_resource_demand_adjustments", {}).get("water_liters", 0.0)), 3),
            "energy_kwh": round(float(population_context.get("daily_resource_demand_adjustments", {}).get("energy_kwh", 0.0)), 3),
            "food_servings": round(float(population_context.get("daily_resource_demand_adjustments", {}).get("food_servings", 0.0)), 3),
        },
        "capacity_multiplier": round(float(viewer_context.get("capacity_multiplier", 1.0)), 6),
        "active_node_patterns": list(viewer_context.get("active_node_patterns", [])),
        "pattern_node_multipliers": dict(viewer_context.get("pattern_node_multipliers", {})),
        "provisional": True,
    }


def _selected_candidate(search_optimizer_report: dict[str, Any], candidate_id: str | None) -> dict[str, Any]:
    selected = candidate_id or search_optimizer_report.get("selected_candidate", "")
    candidates = search_optimizer_report.get("top_candidates", [])
    candidate = next((item for item in candidates if item.get("id") == selected), None)
    if not candidate:
        raise ValueError(f"Candidate not available in top_candidates: {selected}")
    return candidate


def _apply_parameter(plan: dict[str, Any], parameter: dict[str, Any]) -> None:
    pattern_id = parameter["pattern_id"]
    path = parameter["path"]
    storage_index = _storage_index(path)
    field = _storage_field(path)
    plan["simulation_inputs"]["storage_by_pattern"][pattern_id][storage_index][field] = float(parameter["value"])


def _scenario_runs(applied_plan: dict[str, Any], scenarios: list[dict[str, Any]]) -> list[dict[str, Any]]:
    runs = []
    for scenario in scenarios:
        if scenario.get("kind") == "Scenario":
            runs.append(run_scenario(applied_plan, scenario))
        elif scenario.get("kind") == "ScenarioRun":
            runs.append(scenario)
    return runs


def _next_search_report(
    applied_plan: dict[str, Any],
    patterns_by_id: dict[str, dict[str, Any]] | None,
    optimization_profile: dict[str, Any] | None,
    scenarios: list[dict[str, Any]],
    review_status: dict[str, Any] | None,
    days: int,
    top_count: int,
) -> dict[str, Any] | None:
    if not patterns_by_id or not optimization_profile:
        return None
    scenario_inputs = [scenario for scenario in scenarios if scenario.get("kind") == "Scenario"]
    return optimize_search(
        applied_plan,
        patterns_by_id,
        optimization_profile,
        scenario_inputs,
        review_status,
        days,
        top_count,
    )


def _authority(authority_mode: str, candidate: dict[str, Any], operator_acceptance: dict[str, Any]) -> dict[str, Any]:
    operator_directed = authority_mode == "operator_directed"
    simulation_submit_allowed = (
        operator_directed
        and candidate.get("status") == "viable"
        and operator_acceptance["status"] in {"improved", "converged"}
    )
    return {
        "mode": authority_mode,
        "simulation_submit_allowed": simulation_submit_allowed,
        "promotion_allowed": False,
        "oversight_policy": (
            "Single operator may apply provisional model changes to pursue objective improvement inside simulation."
            if operator_directed
            else "Model changes are prepared for external review before iteration."
        ),
        "blocked_from_real_world_use": True,
        "provisional": True,
    }


def _storage_index(path: str) -> int:
    start = path.find("storage[")
    if start == -1:
        raise ValueError(f"Unsupported candidate parameter path: {path}")
    start += len("storage[")
    end = path.find("]", start)
    if end == -1:
        raise ValueError(f"Unsupported candidate parameter path: {path}")
    return int(path[start:end])


def _storage_field(path: str) -> str:
    field = path.split(".")[-1]
    if field not in {"capacity", "initial", "reserve_floor", "max_release_per_day", "max_refill_per_day"}:
        raise ValueError(f"Unsupported candidate parameter field: {path}")
    return field


def _change_summary(candidate: dict[str, Any]) -> dict[str, Any]:
    changed = [item for item in candidate.get("parameter_deltas", []) if float(item.get("delta", 0)) != 0]
    return {
        "candidate_plan_id": candidate.get("candidate_plan_id", ""),
        "family_levels": candidate.get("family_levels", {}),
        "parameter_delta_count": len(changed),
        "parameter_deltas": changed,
        "aggregate_score": candidate.get("aggregate_score", 0),
        "hard_constraint_failures": candidate.get("hard_constraint_failures", 0),
        "selection_rationale": candidate.get("selection_rationale", ""),
        "tradeoffs": candidate.get("tradeoffs", []),
        "provisional": True,
    }


def _cycle_status(candidate: dict[str, Any], operator_acceptance: dict[str, Any]) -> str:
    if candidate.get("status") != "viable" or not operator_acceptance.get("simulation_submit_allowed"):
        return "blocked"
    return "materialized"


def _before_after(before: dict[str, Any], after: dict[str, Any]) -> dict[str, Any]:
    return {
        "baseline_status": before["status"],
        "applied_status": after["status"],
        "resource_delta": _resource_delta(before, after),
        "storage_delta": _storage_delta(before, after),
        "failure_delta": len(after.get("runtime_failures", [])) - len(before.get("runtime_failures", [])),
        "bottleneck_delta": len(after.get("bottlenecks", [])) - len(before.get("bottlenecks", [])),
        "provisional": True,
    }


def _operator_acceptance(candidate: dict[str, Any], before_after: dict[str, Any]) -> dict[str, Any]:
    blockers: list[str] = []
    improvements: list[str] = []
    regressions: list[str] = []
    if candidate.get("status") != "viable" or int(candidate.get("hard_constraint_failures", 0)) > 0:
        blockers.append("Candidate has hard constraint failures.")
    if before_after.get("applied_status") == "fail":
        blockers.append("Applied simulation status is fail.")

    for row in before_after.get("resource_delta", []):
        before_rank = _status_rank(row.get("before_status", "missing"))
        after_rank = _status_rank(row.get("after_status", "missing"))
        resource = row.get("resource", "resource")
        if after_rank < before_rank:
            regressions.append(f"{resource} status regressed from {row.get('before_status')} to {row.get('after_status')}.")
        elif after_rank > before_rank:
            improvements.append(f"{resource} status improved from {row.get('before_status')} to {row.get('after_status')}.")

    for row in before_after.get("storage_delta", []):
        before_rank = _status_rank(row.get("before_status", "missing"))
        after_rank = _status_rank(row.get("after_status", "missing"))
        resource = row.get("resource", "storage")
        if after_rank < before_rank:
            regressions.append(f"{resource} storage regressed from {row.get('before_status')} to {row.get('after_status')}.")
        elif after_rank > before_rank:
            improvements.append(f"{resource} storage improved from {row.get('before_status')} to {row.get('after_status')}.")

    if int(before_after.get("failure_delta", 0)) > 0:
        regressions.append("Applied plan increases runtime failure count.")
    elif int(before_after.get("failure_delta", 0)) < 0:
        improvements.append("Applied plan reduces runtime failure count.")
    if int(before_after.get("bottleneck_delta", 0)) > 0:
        regressions.append("Applied plan increases modeled bottlenecks.")
    elif int(before_after.get("bottleneck_delta", 0)) < 0:
        improvements.append("Applied plan reduces modeled bottlenecks.")

    if blockers:
        status = "blocked"
    elif regressions:
        status = "regressed"
    elif improvements:
        status = "improved"
    else:
        status = "converged"

    return {
        "status": status,
        "simulation_submit_allowed": status in {"improved", "converged"},
        "objective_regressions": regressions,
        "objective_improvements": improvements,
        "blockers": blockers,
        "rationale": _operator_acceptance_rationale(status),
        "provisional": True,
    }


def _status_rank(status: str) -> int:
    return {"missing": 0, "fail": 1, "warn": 2, "pass": 3}.get(str(status), 0)


def _operator_acceptance_rationale(status: str) -> str:
    if status == "blocked":
        return "Operator-directed simulation blocks candidates with hard constraint failures or failed applied simulations."
    if status == "regressed":
        return "Operator-directed simulation blocks objective regressions even when review oversight is reduced."
    if status == "improved":
        return "Operator-directed simulation may submit this provisional model change because tracked objective evidence improved without regressions."
    return "No further tracked improvement was found; the loop appears converged under the current search space."


def _applied_scenario_summary(scenario_runs: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "scenario": run.get("scenario", ""),
            "status": run.get("status", "unknown"),
            "survival_critical_gate_failures": run.get("survival_critical_gate_failures", []),
            "bottlenecks": run.get("bottlenecks", [])[:5],
            "provisional": True,
        }
        for run in scenario_runs
    ]


def _resource_delta(before: dict[str, Any], after: dict[str, Any]) -> list[dict[str, Any]]:
    resources = sorted(set(before.get("resource_balance", {})) | set(after.get("resource_balance", {})))
    rows = []
    for resource in resources:
        before_summary = before.get("resource_balance", {}).get(resource, {})
        after_summary = after.get("resource_balance", {}).get(resource, {})
        rows.append(
            {
                "resource": resource,
                "before_net_per_day": before_summary.get("net_per_day", 0),
                "after_net_per_day": after_summary.get("net_per_day", 0),
                "before_status": before_summary.get("status", "missing"),
                "after_status": after_summary.get("status", "missing"),
                "provisional": True,
            }
        )
    return rows


def _storage_delta(before: dict[str, Any], after: dict[str, Any]) -> list[dict[str, Any]]:
    before_storage = before.get("storage", {}).get("resources", {})
    after_storage = after.get("storage", {}).get("resources", {})
    resources = sorted(set(before_storage) | set(after_storage))
    return [
        {
            "resource": resource,
            "before_capacity": before_storage.get(resource, {}).get("capacity", 0),
            "after_capacity": after_storage.get(resource, {}).get("capacity", 0),
            "before_reserve_floor": before_storage.get(resource, {}).get("reserve_floor", 0),
            "after_reserve_floor": after_storage.get(resource, {}).get("reserve_floor", 0),
            "before_status": before_storage.get(resource, {}).get("status", "missing"),
            "after_status": after_storage.get(resource, {}).get("status", "missing"),
            "provisional": True,
        }
        for resource in resources
    ]


def _review_gates(candidate: dict[str, Any]) -> dict[str, Any]:
    blocked = candidate.get("status") != "viable" or int(candidate.get("hard_constraint_failures", 0)) > 0
    return {
        "promotion_allowed": False,
        "materialization_allowed": not blocked,
        "blockers": [] if not blocked else ["Candidate has hard constraint failures and should not be promoted."],
        "required_review": [
            "resident governance consent",
            "professional review for any affected water, energy, sanitation, structural, legal, or food-safety claims",
            "objective weight ratification before treating score as authoritative",
        ],
        "provisional": True,
    }


def _viewer_next_actions(candidate: dict[str, Any]) -> list[str]:
    if candidate.get("status") != "viable":
        return [
            "Do not submit this candidate as a next-cycle baseline.",
            "Inspect hard constraint failures before re-running search.",
        ]
    return [
        "Load the generated applied runtime bundle to inspect the changed cycle.",
        "Use the next generated search report to continue objective improvement from the applied plan.",
        "Keep the change marked provisional until governance and professional review gates are resolved.",
    ]
