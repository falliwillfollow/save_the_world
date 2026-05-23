from __future__ import annotations

import copy
import math
from pathlib import Path
from typing import Any

from .compiler import load_patterns
from .cycle import materialize_search_candidate
from .io import load_data, write_json


GENERATED_DIR = Path("examples/generated")
COMPILED_PLAN_PATH = GENERATED_DIR / "micro_commons_plan.json"
SEARCH_OPTIMIZER_PATH = GENERATED_DIR / "micro_commons_search_optimizer_report.json"
REVIEW_STATUS_PATH = GENERATED_DIR / "micro_commons_review_status.json"
CYCLE_ITERATION_PATH = GENERATED_DIR / "micro_commons_cycle_iteration.json"
OPTIMIZATION_PROFILE_PATH = Path("optimization_profiles/minimum_dignity_v0.yaml")
DEFAULT_SCENARIO_PATHS = [
    Path("scenarios/water_contamination_response_v2.yaml"),
    Path("scenarios/crop_failure.yaml"),
    Path("scenarios/energy_outage_reserve_v2.yaml"),
]
MODULE_REGISTRY_PATH = Path("module_registries/micro_commons_default_v0.yaml")


def regenerate_viewer_cycle_reports(
    repo_root: str | Path,
    population: int,
    *,
    days: int = 365,
    cycle_index: int = 1,
    candidate_id: str | None = None,
    playback_seconds: int = 20,
    node_scaling_report: dict[str, Any] | None = None,
) -> dict[str, Any]:
    root = Path(repo_root)
    generated_dir = root / GENERATED_DIR
    base_plan = load_data(root / COMPILED_PLAN_PATH)
    module_registry = load_data(root / MODULE_REGISTRY_PATH)
    search = load_data(root / SEARCH_OPTIMIZER_PATH)
    patterns = load_patterns(root / "patterns")
    plan = adapt_compiled_plan_for_population(base_plan, int(population), node_scaling_report, module_registry, patterns)
    search_patterns = {
        pattern_id: patterns[pattern_id]
        for pattern_id in base_plan.get("selected_patterns", [])
        if pattern_id in patterns
    }
    search = adapt_search_report_for_population(
        search,
        float(plan.get("metadata", {}).get("viewer_run_context", {}).get("capacity_multiplier", 1.0)),
    )
    review_status = load_data(root / REVIEW_STATUS_PATH) if (root / REVIEW_STATUS_PATH).exists() else None
    scenarios = [load_data(root / path) for path in DEFAULT_SCENARIO_PATHS if (root / path).exists()]
    optimization_profile = load_data(root / OPTIMIZATION_PROFILE_PATH)

    cycle_report = materialize_search_candidate(
        plan,
        search,
        candidate_id,
        review_status=review_status,
        scenarios=scenarios,
        days=int(days),
        cycle_index=int(cycle_index),
        target_playback_seconds=int(playback_seconds),
        authority_mode="operator_directed",
        patterns_by_id=search_patterns,
        optimization_profile=optimization_profile,
    )
    write_json(generated_dir / CYCLE_ITERATION_PATH.name, cycle_report)
    return {
        "status": "regenerated",
        "population": int(population),
        "artifacts": {
            "cycle_iteration": str(GENERATED_DIR / CYCLE_ITERATION_PATH.name),
        },
        "cycle_iteration": cycle_report,
        "runtime_bundle": cycle_report["runtime_bundle"],
        "search_optimizer": cycle_report.get("next_search_optimizer_report"),
    }


def adapt_compiled_plan_for_population(
    compiled_plan: dict[str, Any],
    population: int,
    node_scaling_report: dict[str, Any] | None = None,
    module_registry: dict[str, Any] | None = None,
    patterns_by_id: dict[str, dict[str, Any]] | None = None,
) -> dict[str, Any]:
    plan = copy.deepcopy(compiled_plan)
    population = max(1, int(population))
    base_population = max(1, int(compiled_plan.get("site_summary", {}).get("population_target", population)))
    base_households = max(1, int(compiled_plan.get("site_summary", {}).get("households", 1)))
    household_size = base_population / base_households
    households = max(1, math.ceil(population / household_size))
    plan["id"] = f"{compiled_plan['id']}_p{population}"
    plan["site_summary"]["population_target"] = population
    plan["site_summary"]["households"] = households
    plan.setdefault("metadata", {})
    plan["metadata"]["viewer_run_context"] = {
        "population": population,
        "base_compiled_plan": compiled_plan["id"],
        "source": "webapp_population_slider",
        "provisional": True,
    }
    plan.setdefault("simulation_inputs", {})
    plan["simulation_inputs"]["population_context"] = _population_context(compiled_plan, population, households, base_population)
    active_patterns = _active_patterns_for_population(population, node_scaling_report, {"food_production", "potable_water_source", "critical_energy"})
    if active_patterns and patterns_by_id:
        _materialize_active_patterns(plan, active_patterns, patterns_by_id)
    multipliers = _pattern_multipliers(plan, population, node_scaling_report, module_registry)
    capacity_multiplier = max(1.0, population / base_population)
    _apply_pattern_multipliers(plan, multipliers, capacity_multiplier, set(active_patterns))
    plan["metadata"]["viewer_run_context"]["pattern_node_multipliers"] = multipliers
    plan["metadata"]["viewer_run_context"]["capacity_multiplier"] = round(capacity_multiplier, 6)
    plan["metadata"]["viewer_run_context"]["active_node_patterns"] = active_patterns
    plan["role_burden"]["recurring_hours_per_resident_per_week"] = round(
        float(plan["role_burden"].get("total_recurring_hours_per_week", 0.0)) / population,
        3,
    )
    return plan


def _active_patterns_for_population(
    population: int,
    node_scaling_report: dict[str, Any] | None,
    slot_ids: set[str] | None = None,
) -> list[str]:
    if not node_scaling_report:
        return []
    target = next(
        (row for row in node_scaling_report.get("target_results", []) if int(row.get("people", 0)) == int(population)),
        None,
    )
    if not target:
        return []
    active: list[str] = []
    for row in target.get("slot_results", []):
        if slot_ids is not None and row.get("slot") not in slot_ids:
            continue
        for pattern_id in row.get("active_patterns", []):
            if pattern_id not in active:
                active.append(pattern_id)
    return active


def _materialize_active_patterns(plan: dict[str, Any], active_patterns: list[str], patterns_by_id: dict[str, dict[str, Any]]) -> None:
    selected = list(plan.get("selected_patterns", []))
    phase_by_id = {phase["phase"]: phase for phase in plan.get("phases", [])}
    role_hours = dict(plan.get("role_burden", {}).get("weekly_hours_by_role", {}))
    for pattern_id in active_patterns:
        if pattern_id in selected or pattern_id not in patterns_by_id:
            continue
        pattern = patterns_by_id[pattern_id]
        selected.append(pattern_id)
        plan.setdefault("dependency_order", []).append(pattern_id)
        phase_key = f"phase_{pattern['build_phase']}"
        phase = phase_by_id.setdefault(phase_key, {"phase": phase_key, "patterns": []})
        phase["patterns"].append(
            {
                "pattern_id": pattern_id,
                "purpose": pattern["purpose"],
                "build_labor_hours": pattern["metrics"]["build_labor_hours"],
                "provisional": pattern["provisional"],
            }
        )
        for task in pattern["lifecycle"]["maintenance"]:
            event = {
                "pattern_id": pattern_id,
                "task_id": task["id"],
                "description": task["description"],
                "interval": task["interval"],
                "role": task["role"],
                "estimated_hours": task["estimated_hours"],
                "provisional": task.get("provisional", True),
            }
            plan.setdefault("maintenance_calendar", []).append(event)
            role_hours[task["role"]] = role_hours.get(task["role"], 0.0) + float(task["estimated_hours"])
        for mode in pattern.get("failure_modes", []):
            plan.setdefault("risk_register", []).append(
                {
                    "pattern_id": pattern_id,
                    "mode": mode["mode"],
                    "likelihood": mode["likelihood"],
                    "severity": mode["severity"],
                    "detection_method": mode["detection_method"],
                    "mitigation": mode["mitigation"],
                }
            )
        plan.setdefault("simulation_inputs", {}).setdefault("resource_effects_by_pattern", {})[pattern_id] = copy.deepcopy(pattern["simulation"]["resource_effects"])
        plan.setdefault("simulation_inputs", {}).setdefault("critical_resources_by_pattern", {})[pattern_id] = copy.deepcopy(pattern["simulation"]["critical_resources"])
        if pattern["simulation"].get("storage"):
            plan.setdefault("simulation_inputs", {}).setdefault("storage_by_pattern", {})[pattern_id] = copy.deepcopy(pattern["simulation"]["storage"])
    plan["selected_patterns"] = selected
    plan["phases"] = sorted(phase_by_id.values(), key=lambda item: item["phase"])
    plan["maintenance_calendar"] = sorted(
        plan.get("maintenance_calendar", []),
        key=lambda item: (item["role"], item["pattern_id"], item["task_id"]),
    )
    plan["role_burden"]["weekly_hours_by_role"] = dict(sorted((role, round(hours, 6)) for role, hours in role_hours.items()))
    plan["role_burden"]["total_recurring_hours_per_week"] = round(sum(role_hours.values()), 6)


def adapt_search_report_for_population(search_report: dict[str, Any], capacity_multiplier: float) -> dict[str, Any]:
    report = copy.deepcopy(search_report)
    if capacity_multiplier <= 1:
        return report
    report.setdefault("viewer_population_context", {})
    report["viewer_population_context"] = {
        "storage_parameter_multiplier": round(capacity_multiplier, 6),
        "source": "webapp_population_context",
        "provisional": True,
    }
    for candidate in report.get("top_candidates", []):
        for parameter in candidate.get("parameter_values", []):
            if _is_storage_parameter(parameter):
                parameter["value"] = round(float(parameter["value"]) * capacity_multiplier, 6)
        for delta in candidate.get("parameter_deltas", []):
            if _is_storage_parameter(delta):
                for key in ["from_value", "to_value", "delta"]:
                    if key in delta and isinstance(delta[key], (int, float)):
                        delta[key] = round(float(delta[key]) * capacity_multiplier, 6)
    return report


def _is_storage_parameter(parameter: dict[str, Any]) -> bool:
    return "storage[" in str(parameter.get("path", ""))


def _pattern_multipliers(
    compiled_plan: dict[str, Any],
    population: int,
    node_scaling_report: dict[str, Any] | None,
    module_registry: dict[str, Any] | None,
) -> dict[str, int]:
    selected = set(compiled_plan.get("selected_patterns", []))
    if not node_scaling_report or not module_registry:
        return {pattern_id: 1 for pattern_id in sorted(selected)}
    target = next(
        (row for row in node_scaling_report.get("target_results", []) if int(row.get("people", 0)) == int(population)),
        None,
    )
    if not target:
        return {pattern_id: 1 for pattern_id in sorted(selected)}
    slots = {slot.get("id"): slot for slot in module_registry.get("slots", [])}
    multipliers = {pattern_id: 1 for pattern_id in sorted(selected)}
    for row in target.get("slot_results", []):
        slot = slots.get(row.get("slot"), {})
        desired_nodes = max(1, int(row.get("desired_nodes", 1)))
        for pattern_id in [*slot.get("default_patterns", []), *slot.get("accepted_patterns", [])]:
            if pattern_id in multipliers:
                multipliers[pattern_id] = max(multipliers[pattern_id], desired_nodes)
    return multipliers


def _apply_pattern_multipliers(
    plan: dict[str, Any],
    multipliers: dict[str, int],
    capacity_multiplier: float,
    active_patterns: set[str] | None = None,
) -> None:
    resource_effects = plan.get("simulation_inputs", {}).get("resource_effects_by_pattern", {})
    storage_by_pattern = plan.get("simulation_inputs", {}).get("storage_by_pattern", {})
    active_patterns = active_patterns or set()
    for pattern_id, multiplier in multipliers.items():
        pattern_capacity_multiplier = float(multiplier if pattern_id in active_patterns else capacity_multiplier)
        if multiplier <= 1 and pattern_capacity_multiplier <= 1:
            continue
        if pattern_id in resource_effects:
            for key, value in resource_effects[pattern_id].items():
                resource_effects[pattern_id][key] = round(float(value) * pattern_capacity_multiplier, 6)
        if pattern_id in storage_by_pattern:
            for spec in storage_by_pattern[pattern_id]:
                for key in ["capacity", "initial", "reserve_floor", "max_release_per_day", "max_refill_per_day"]:
                    if key in spec and isinstance(spec[key], (int, float)):
                        spec[key] = round(float(spec[key]) * pattern_capacity_multiplier, 6)
    for event in plan.get("maintenance_calendar", []):
        multiplier = multipliers.get(event.get("pattern_id", ""), 1)
        if multiplier > 1:
            event["estimated_hours"] = round(float(event["estimated_hours"]) * multiplier, 6)
    for phase in plan.get("phases", []):
        for pattern in phase.get("patterns", []):
            multiplier = multipliers.get(pattern.get("pattern_id", ""), 1)
            if multiplier > 1:
                pattern["build_labor_hours"] = round(float(pattern["build_labor_hours"]) * multiplier, 6)
    role_hours: dict[str, float] = {}
    for event in plan.get("maintenance_calendar", []):
        role = event.get("role", "")
        role_hours[role] = role_hours.get(role, 0.0) + float(event.get("estimated_hours", 0.0))
    if role_hours:
        plan["role_burden"]["weekly_hours_by_role"] = dict(sorted((role, round(hours, 6)) for role, hours in role_hours.items()))
        plan["role_burden"]["total_recurring_hours_per_week"] = round(sum(role_hours.values()), 6)


def _population_context(compiled_plan: dict[str, Any], population: int, households: int, base_population: int) -> dict[str, Any]:
    base_context = _base_population_context(compiled_plan, base_population)
    demand = {
        resource: round(float(value) * population / base_population, 3)
        for resource, value in base_context["daily_resource_demand_adjustments"].items()
    }
    weekly_labor = float(base_context["available_commons_labor_hours_per_week"]) * population / base_population
    care_hours = float(base_context["care_hours_per_week"]) * population / base_population
    protected_hours = float(base_context["protected_labor_hours_per_week"]) * population / base_population
    return {
        "source": "webapp_population_context",
        "population": population,
        "household_count": households,
        "available_commons_labor_hours_per_week": round(weekly_labor, 3),
        "available_commons_labor_hours_per_day": round(weekly_labor / 7, 3),
        "care_hours_per_week": round(care_hours, 3),
        "protected_labor_hours_per_week": round(protected_hours, 3),
        "daily_resource_demand_adjustments": demand,
        "provisional": True,
    }


def _base_population_context(compiled_plan: dict[str, Any], base_population: int) -> dict[str, Any]:
    household_profile = compiled_plan.get("simulation_inputs", {}).get("household_profile")
    if not household_profile:
        weekly_labor = base_population * 14.0
        return {
            "available_commons_labor_hours_per_week": weekly_labor,
            "care_hours_per_week": 0.0,
            "protected_labor_hours_per_week": 0.0,
            "daily_resource_demand_adjustments": {
                "water_liters": 0.0,
                "energy_kwh": 0.0,
                "food_servings": 0.0,
            },
        }
    households = household_profile.get("households", [])
    return {
        "available_commons_labor_hours_per_week": sum(float(item["available_commons_labor_hours_per_week"]) for item in households),
        "care_hours_per_week": sum(float(item["care_hours_per_week"]) for item in households),
        "protected_labor_hours_per_week": sum(float(item["protected_labor_hours_per_week"]) for item in households),
        "daily_resource_demand_adjustments": {
            "water_liters": float(household_profile.get("daily_resource_demand_adjustments", {}).get("water_liters", 0.0)),
            "energy_kwh": float(household_profile.get("daily_resource_demand_adjustments", {}).get("energy_kwh", 0.0)),
            "food_servings": float(household_profile.get("daily_resource_demand_adjustments", {}).get("food_servings", 0.0)),
        },
    }
