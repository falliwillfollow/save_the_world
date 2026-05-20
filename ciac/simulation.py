from __future__ import annotations

import math
from collections import defaultdict
from typing import Any


RESOURCE_KEYS = {
    "water_liters_per_day": "water_liters",
    "energy_kwh_per_day": "energy_kwh",
    "food_servings_per_day": "food_servings",
}

LEDGER_RESOURCES = [
    "water_liters",
    "energy_kwh",
    "food_servings",
    "sanitation_capacity",
    "labor_hours",
    "procurement_units",
]

INTERVAL_DAYS = {
    "daily": 1,
    "weekly": 7,
    "monthly": 30,
    "seasonal": 91,
    "annual": 365,
}


def simulate(
    compiled_plan: dict[str, Any],
    days: int = 365,
    scenario: dict[str, Any] | None = None,
    review_status: dict[str, Any] | None = None,
) -> dict[str, Any]:
    if days < 1:
        raise ValueError("Simulation days must be at least 1")

    population = _population_context(compiled_plan)
    scenario_context = _scenario_context(scenario)
    runtime_failures = _runtime_failures(compiled_plan, scenario, days)
    daily_states = _daily_states(compiled_plan, days, runtime_failures, review_status, scenario)
    resource_ledger = _resource_ledger(daily_states)
    resource_balance = _resource_balance(resource_ledger, days)
    storage = _storage_summary(daily_states)
    maintenance = _maintenance_summary(compiled_plan, daily_states, days)
    labor = _labor_summary(compiled_plan, maintenance, daily_states, days)
    triggered_risks = _triggered_risks(compiled_plan)
    timeline = _timeline(daily_states, resource_balance, labor, triggered_risks, scenario_context)
    bottlenecks = _bottlenecks(resource_balance, labor, maintenance, compiled_plan)
    gate_recommendations = _gate_recommendations(resource_balance, labor, maintenance, triggered_risks)
    unknowns = _unknowns(compiled_plan, scenario_context)
    status = _status(resource_balance, labor, maintenance, triggered_risks)

    return {
        "kind": "SimulationRun",
        "id": _simulation_id(compiled_plan, scenario_context, days),
        "compiled_plan": compiled_plan["id"],
        "generated_by": "ciac.simulation.v0",
        "days": days,
        "provisional": True,
        "status": status,
        "population": population,
        "runtime_failures": runtime_failures,
        "review_context": _review_context(review_status, scenario_context),
        "scenario_context": scenario_context,
        "daily_states": daily_states,
        "resource_ledger": resource_ledger,
        "timeline": timeline,
        "resource_balance": resource_balance,
        "storage": storage,
        "labor": labor,
        "maintenance": maintenance,
        "triggered_risks": triggered_risks,
        "bottlenecks": bottlenecks,
        "gate_recommendations": gate_recommendations,
        "confidence": "low" if unknowns else "medium",
        "unknowns": unknowns,
    }


def _daily_states(
    compiled_plan: dict[str, Any],
    days: int,
    runtime_failures: list[dict[str, Any]] | None = None,
    review_status: dict[str, Any] | None = None,
    scenario: dict[str, Any] | None = None,
) -> list[dict[str, Any]]:
    pattern_flows = _daily_pattern_flows(compiled_plan)
    storage_specs = _storage_specs(compiled_plan)
    storage_specs_by_resource = _storage_specs_by_resource(storage_specs)
    storage_balances = {spec["storage_id"]: float(spec["initial"]) for spec in storage_specs}
    storage_quality = {spec["storage_id"]: 0 for spec in storage_specs}
    population_context = _population_context(compiled_plan)
    scheduled_maintenance = _scheduled_maintenance_by_day(compiled_plan, days)
    balances = {resource: 0.0 for resource in LEDGER_RESOURCES}
    for resource in storage_specs_by_resource:
        balances[resource] = _storage_total(resource, storage_specs_by_resource, storage_balances)
    population = int(population_context["population"])
    states: list[dict[str, Any]] = []
    maintenance_backlog: list[dict[str, Any]] = []
    recovery_state: dict[str, dict[str, Any]] = {}

    for day in range(1, days + 1):
        scenario_day = _scenario_day_context(scenario, day)
        day_population_context = _population_context_for_scenario_day(population_context, scenario_day)
        active_failures = _active_failures_for_day(runtime_failures or [], day)
        seasonal_profile = compiled_plan.get("simulation_inputs", {}).get("seasonal_profile")
        season = _season_for_day(day, seasonal_profile)
        season_multipliers = _seasonal_multipliers(seasonal_profile, day)
        degradation_by_pattern = _degradation_by_pattern(maintenance_backlog)
        resource_state: dict[str, dict[str, Any]] = {}
        maintenance_multiplier = float(season_multipliers.get("maintenance_labor_multiplier", 1.0))
        maintenance_events = _maintenance_due_today(scheduled_maintenance.get(day, []), maintenance_backlog, day, maintenance_multiplier)
        maintenance_state = _resolve_maintenance_day(maintenance_events, day_population_context)
        maintenance_backlog = maintenance_state["deferred_events"]
        quality_losses = _advance_storage_quality(storage_specs, storage_balances, storage_quality, maintenance_state)
        daily_flows = _daily_resource_flows(pattern_flows, degradation_by_pattern, day_population_context, active_failures)
        unmet_needs: list[str] = []
        storage_activity: dict[str, dict[str, Any]] = {}
        scenario_emergency_hours = _scenario_emergency_hours(scenario_day)

        for resource in LEDGER_RESOURCES:
            has_storage = resource in storage_specs_by_resource
            opening = _storage_total(resource, storage_specs_by_resource, storage_balances) if has_storage else balances[resource]
            production = daily_flows.get(resource, {}).get("production", 0.0)
            consumption = daily_flows.get(resource, {}).get("consumption", 0.0)
            resource_multipliers = season_multipliers.get("resource_multipliers", {}).get(resource, {})
            production *= float(resource_multipliers.get("production", 1.0))
            consumption *= float(resource_multipliers.get("consumption", 1.0))
            if resource == "labor_hours":
                production = _available_labor_hours(day_population_context)
                consumption = maintenance_state["required_hours"] + _failure_response_hours(active_failures) + scenario_emergency_hours
            production, consumption = _apply_scenario_resource_modifier(resource, production, consumption, scenario_day)
            raw_net = production - consumption
            storage_release = 0.0
            storage_refill = 0.0
            curtailment = 0.0
            if has_storage:
                if raw_net < 0:
                    storage_release = _release_from_storage(resource, storage_specs_by_resource, storage_balances, abs(raw_net))
                elif raw_net > 0:
                    storage_refill = _refill_storage(resource, storage_specs_by_resource, storage_balances, raw_net)
                    curtailment = max(0.0, raw_net - storage_refill)
                ending = _storage_total(resource, storage_specs_by_resource, storage_balances)
                net = ending - opening
                storage_activity[resource] = _storage_resource_state(resource, storage_specs_by_resource, storage_balances, storage_quality, quality_losses, opening, storage_release, storage_refill, curtailment)
            else:
                net = raw_net
                ending = opening + net
            unmet = abs(ending) if ending < 0 else 0.0
            if has_storage and raw_net < 0:
                unmet = max(0.0, abs(raw_net) - storage_release)
            if unmet:
                unmet_needs.append(resource)
            balances[resource] = ending
            resource_state[resource] = {
                "opening_balance": round(opening, 3),
                "production": round(production, 3),
                "consumption": round(consumption, 3),
                "raw_net": round(raw_net, 3),
                "storage_release": round(storage_release, 3),
                "storage_refill": round(storage_refill, 3),
                "curtailment": round(curtailment, 3),
                "net": round(net, 3),
                "ending_balance": round(ending, 3),
                "unmet_demand": round(unmet, 3),
                "status": _daily_resource_status(ending, unmet, storage_activity.get(resource)),
                "provisional": True,
            }

        recovery_tasks = _advance_storage_recovery(
            storage_activity,
            recovery_state,
            storage_quality,
            day,
            population_context,
            maintenance_state,
            active_failures,
            review_status,
            scenario_day,
        )
        recovery_hours = _storage_recovery_hours(recovery_tasks)
        labor_hours = maintenance_state["required_hours"] + _failure_response_hours(active_failures) + scenario_emergency_hours + recovery_hours

        states.append(
            {
                "day": day,
                "season": season,
                "population": population,
                "population_context": day_population_context,
                "scenario_events": scenario_day["events"],
                "resources": resource_state,
                "storage_state": {
                    "resources": storage_activity,
                    "recovery_tasks": recovery_tasks,
                    "status": _storage_day_status(storage_activity),
                    "provisional": True,
                },
                "maintenance_events": maintenance_events,
                "maintenance_state": {
                    key: value
                    for key, value in maintenance_state.items()
                    if key != "deferred_events"
                },
                "active_failures": active_failures,
                "labor": {
                    "maintenance_hours": round(labor_hours, 3),
                    "storage_recovery_hours": round(recovery_hours, 3),
                    "scenario_emergency_hours": round(scenario_emergency_hours, 3),
                    "maintenance_labor_multiplier": round(maintenance_multiplier, 3),
                    "available_commons_hours": round(_available_labor_hours(day_population_context), 3),
                    "hours_per_resident": round(labor_hours / population, 3)
                    if population
                    else round(labor_hours, 3),
                    "status": _daily_labor_status(labor_hours, day_population_context),
                },
                "system_degradation": {
                    "patterns": {pattern: round(value, 3) for pattern, value in sorted(degradation_by_pattern.items())},
                    "max_degradation_factor": round(max(degradation_by_pattern.values(), default=0.0), 3),
                    "provisional": True,
                },
                "active_risks": _active_maintenance_risks(maintenance_backlog, degradation_by_pattern) + _active_failure_risks(active_failures),
                "unmet_needs": sorted(unmet_needs),
            }
        )
    return states


def _daily_pattern_flows(compiled_plan: dict[str, Any]) -> dict[str, dict[str, dict[str, float]]]:
    effects = compiled_plan.get("simulation_inputs", {}).get("resource_effects_by_pattern", {})
    pattern_flows: dict[str, dict[str, dict[str, float]]] = {}
    for pattern_id, pattern_effects in effects.items():
        flows = {resource: {"production": 0.0, "consumption": 0.0} for resource in LEDGER_RESOURCES}
        for source_key, resource_key in RESOURCE_KEYS.items():
            value = float(pattern_effects.get(source_key, 0))
            if value >= 0:
                flows[resource_key]["production"] += value
            else:
                flows[resource_key]["consumption"] += abs(value)
        pattern_flows[pattern_id] = flows
    return pattern_flows


def _daily_resource_flows(
    pattern_flows: dict[str, dict[str, dict[str, float]]],
    degradation_by_pattern: dict[str, float],
    population_context: dict[str, Any],
    active_failures: list[dict[str, Any]] | None = None,
) -> dict[str, dict[str, float]]:
    flows = {resource: {"production": 0.0, "consumption": 0.0} for resource in LEDGER_RESOURCES}
    for pattern_id, resources in pattern_flows.items():
        degradation = degradation_by_pattern.get(pattern_id, 0.0)
        failure_effect = _failure_effect_for_pattern(active_failures or [], pattern_id)
        for resource, values in resources.items():
            resource_effect = failure_effect.get(resource, {})
            production_factor = 1 - degradation - float(resource_effect.get("production_loss_factor", 0.0))
            consumption_factor = 1 + (degradation * 0.5) + float(resource_effect.get("consumption_increase_factor", 0.0))
            flows[resource]["production"] += values["production"] * max(0.0, production_factor)
            flows[resource]["consumption"] += values["consumption"] * consumption_factor
    for resource, demand in population_context["daily_resource_demand_adjustments"].items():
        if resource in flows:
            flows[resource]["consumption"] += float(demand)
    return flows


def _storage_specs(compiled_plan: dict[str, Any]) -> list[dict[str, Any]]:
    specs: list[dict[str, Any]] = []
    storage_by_pattern = compiled_plan.get("simulation_inputs", {}).get("storage_by_pattern", {})
    for pattern_id, pattern_specs in sorted(storage_by_pattern.items()):
        for index, spec in enumerate(pattern_specs):
            capacity = float(spec["capacity"])
            initial = min(float(spec["initial"]), capacity)
            reserve_floor = min(float(spec["reserve_floor"]), capacity)
            specs.append(
                {
                    "storage_id": f"{pattern_id}:{spec['resource']}:{index + 1}",
                    "pattern_id": pattern_id,
                    "resource": spec["resource"],
                    "capacity": capacity,
                    "initial": initial,
                    "reserve_floor": reserve_floor,
                    "max_release_per_day": float(spec["max_release_per_day"]),
                    "max_refill_per_day": float(spec["max_refill_per_day"]),
                    "refill_mode": spec["refill_mode"],
                    "quality": spec["quality"],
                    "access_rule": spec["access_rule"],
                    "notes": spec["notes"],
                    "provisional": spec.get("provisional", True),
                }
            )
    return specs


def _storage_specs_by_resource(storage_specs: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    by_resource: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for spec in storage_specs:
        by_resource[spec["resource"]].append(spec)
    return {
        resource: sorted(specs, key=lambda item: (item["pattern_id"], item["storage_id"]))
        for resource, specs in by_resource.items()
    }


def _storage_total(
    resource: str,
    storage_specs_by_resource: dict[str, list[dict[str, Any]]],
    storage_balances: dict[str, float],
) -> float:
    return sum(float(storage_balances[spec["storage_id"]]) for spec in storage_specs_by_resource.get(resource, []))


def _release_from_storage(
    resource: str,
    storage_specs_by_resource: dict[str, list[dict[str, Any]]],
    storage_balances: dict[str, float],
    requested: float,
) -> float:
    remaining = requested
    released = 0.0
    for spec in storage_specs_by_resource.get(resource, []):
        if remaining <= 0:
            break
        available = max(0.0, float(storage_balances[spec["storage_id"]]))
        amount = min(remaining, available, float(spec["max_release_per_day"]))
        storage_balances[spec["storage_id"]] = round(available - amount, 6)
        released += amount
        remaining -= amount
    return released


def _refill_storage(
    resource: str,
    storage_specs_by_resource: dict[str, list[dict[str, Any]]],
    storage_balances: dict[str, float],
    surplus: float,
) -> float:
    remaining = surplus
    refilled = 0.0
    for spec in storage_specs_by_resource.get(resource, []):
        if remaining <= 0:
            break
        current = float(storage_balances[spec["storage_id"]])
        capacity_left = max(0.0, float(spec["capacity"]) - current)
        amount = min(remaining, capacity_left, float(spec["max_refill_per_day"]))
        storage_balances[spec["storage_id"]] = round(current + amount, 6)
        refilled += amount
        remaining -= amount
    return refilled


def _advance_storage_quality(
    storage_specs: list[dict[str, Any]],
    storage_balances: dict[str, float],
    storage_quality: dict[str, int],
    maintenance_state: dict[str, Any],
) -> dict[str, float]:
    completed_patterns = {
        event["pattern_id"]
        for event in maintenance_state.get("completed_events", [])
    }
    losses: dict[str, float] = {}
    for spec in storage_specs:
        storage_id = spec["storage_id"]
        storage_quality[storage_id] = int(storage_quality.get(storage_id, 0)) + 1
        if spec["pattern_id"] in completed_patterns:
            storage_quality[storage_id] = 0
        quality = spec["quality"]
        if storage_quality[storage_id] <= int(quality["unsafe_after_days"]):
            losses[storage_id] = 0.0
            continue
        current = float(storage_balances[storage_id])
        loss = current * float(quality["loss_per_day_after_unsafe"])
        storage_balances[storage_id] = round(max(0.0, current - loss), 6)
        losses[storage_id] = loss
    return losses


def _storage_resource_state(
    resource: str,
    storage_specs_by_resource: dict[str, list[dict[str, Any]]],
    storage_balances: dict[str, float],
    storage_quality: dict[str, int],
    quality_losses: dict[str, float],
    opening_total: float,
    released: float,
    refilled: float,
    curtailed: float,
) -> dict[str, Any]:
    specs = storage_specs_by_resource.get(resource, [])
    capacity = sum(float(spec["capacity"]) for spec in specs)
    reserve_floor = sum(float(spec["reserve_floor"]) for spec in specs)
    ending_total = _storage_total(resource, storage_specs_by_resource, storage_balances)
    quality_status = _storage_quality_status(specs, storage_quality)
    quantity_status = _storage_resource_status(ending_total, reserve_floor, capacity)
    return {
        "resource": resource,
        "opening_total": round(opening_total, 3),
        "released": round(released, 3),
        "refilled": round(refilled, 3),
        "quality_loss": round(sum(float(quality_losses.get(spec["storage_id"], 0.0)) for spec in specs), 3),
        "curtailed": round(curtailed, 3),
        "ending_total": round(ending_total, 3),
        "capacity": round(capacity, 3),
        "reserve_floor": round(reserve_floor, 3),
        "percent_full": round((ending_total / capacity) * 100, 3) if capacity else 0.0,
        "status": _worst_status([quantity_status, quality_status]),
        "quantity_status": quantity_status,
        "quality_status": quality_status,
        "stores": [
            {
                "storage_id": spec["storage_id"],
                "pattern_id": spec["pattern_id"],
                "ending_balance": round(float(storage_balances[spec["storage_id"]]), 3),
                "capacity": round(float(spec["capacity"]), 3),
                "reserve_floor": round(float(spec["reserve_floor"]), 3),
                "max_release_per_day": round(float(spec["max_release_per_day"]), 3),
                "max_refill_per_day": round(float(spec["max_refill_per_day"]), 3),
                "refill_mode": spec["refill_mode"],
                "quality": {
                    "days_since_check": int(storage_quality.get(spec["storage_id"], 0)),
                    "check_interval_days": int(spec["quality"]["check_interval_days"]),
                    "unsafe_after_days": int(spec["quality"]["unsafe_after_days"]),
                    "loss_today": round(float(quality_losses.get(spec["storage_id"], 0.0)), 3),
                    "status": _storage_quality_status([spec], storage_quality),
                    "risk": spec["quality"]["risk"],
                    "recovery_action": spec["quality"]["recovery_action"],
                    "recovery_role": spec["quality"]["recovery_role"],
                    "recovery_labor_hours": round(float(spec["quality"]["recovery_labor_hours"]), 3),
                    "recovery_duration_days": int(spec["quality"]["recovery_duration_days"]),
                    "review_dependency": spec["quality"]["review_dependency"],
                    "provisional": spec["quality"].get("provisional", True),
                },
                "access_rule": spec["access_rule"],
                "provisional": spec.get("provisional", True),
            }
            for spec in specs
        ],
        "provisional": True,
    }


def _storage_resource_status(ending_total: float, reserve_floor: float, capacity: float) -> str:
    if capacity <= 0:
        return "fail"
    if ending_total <= 0:
        return "fail"
    if ending_total <= reserve_floor:
        return "warn"
    return "pass"


def _storage_quality_status(specs: list[dict[str, Any]], storage_quality: dict[str, int]) -> str:
    statuses: list[str] = []
    for spec in specs:
        days_since_check = int(storage_quality.get(spec["storage_id"], 0))
        quality = spec["quality"]
        if days_since_check > int(quality["unsafe_after_days"]):
            statuses.append("fail")
        elif days_since_check > int(quality["check_interval_days"]):
            statuses.append("warn")
        else:
            statuses.append("pass")
    return _worst_status(statuses)


def _worst_status(statuses: list[str]) -> str:
    if any(status == "fail" for status in statuses):
        return "fail"
    if any(status == "warn" for status in statuses):
        return "warn"
    return "pass"


def _storage_day_status(storage_activity: dict[str, dict[str, Any]]) -> str:
    return _worst_status([state["status"] for state in storage_activity.values()])


def _storage_recovery_candidates(storage_activity: dict[str, dict[str, Any]], day: int) -> list[dict[str, Any]]:
    tasks: list[dict[str, Any]] = []
    for resource, summary in sorted(storage_activity.items()):
        for store in summary.get("stores", []):
            quality = store.get("quality", {})
            if quality.get("status") != "fail":
                continue
            tasks.append(
                {
                    "day": day,
                    "storage_id": store["storage_id"],
                    "pattern_id": store["pattern_id"],
                    "resource": resource,
                    "role": quality["recovery_role"],
                    "estimated_hours": round(float(quality["recovery_labor_hours"]), 3),
                    "duration_days": int(quality["recovery_duration_days"]),
                    "action": quality["recovery_action"],
                    "review_dependency": quality["review_dependency"],
                    "status": "open",
                    "provisional": True,
                }
            )
    return tasks


def _advance_storage_recovery(
    storage_activity: dict[str, dict[str, Any]],
    recovery_state: dict[str, dict[str, Any]],
    storage_quality: dict[str, int],
    day: int,
    population_context: dict[str, Any],
    maintenance_state: dict[str, Any],
    active_failures: list[dict[str, Any]],
    review_status: dict[str, Any] | None,
    scenario_day: dict[str, Any],
) -> list[dict[str, Any]]:
    for candidate in _storage_recovery_candidates(storage_activity, day):
        task_id = candidate["storage_id"]
        if task_id not in recovery_state:
            recovery_state[task_id] = {
                **candidate,
                "opened_day": day,
                "last_seen_day": day,
                "worked_hours_total": 0.0,
                "worked_hours_today": 0.0,
                "remaining_hours": float(candidate["estimated_hours"]),
                "days_active": 1,
                "status": "open",
            }
        else:
            recovery_state[task_id].update(
                {
                    "day": day,
                    "last_seen_day": day,
                    "resource": candidate["resource"],
                    "action": candidate["action"],
                    "review_dependency": candidate["review_dependency"],
                }
            )

    for task in recovery_state.values():
        task["worked_hours_today"] = 0.0
        task["days_active"] = max(1, int(task.get("last_seen_day", day)) - int(task["opened_day"]) + 1)
        task["review_state"] = _review_dependency_state(review_status, task["review_dependency"], scenario_day)

    spare_labor = max(
        0.0,
        _available_labor_hours(population_context)
        - float(maintenance_state["completed_hours"])
        - _failure_response_hours(active_failures)
        - _scenario_emergency_hours(scenario_day),
    )
    active_tasks = sorted(
        recovery_state.values(),
        key=lambda item: (item["opened_day"], item["storage_id"]),
    )
    for task in active_tasks:
        if task["status"] in {"blocked_review", "resolved"}:
            if task["status"] == "blocked_review" and _review_is_accepted(task["review_state"]):
                task["status"] = "resolved"
                storage_quality[task["storage_id"]] = 0
            continue
        if float(task["remaining_hours"]) <= 0:
            task["status"] = "resolved" if _review_is_accepted(task["review_state"]) else "blocked_review"
            if task["status"] == "resolved":
                storage_quality[task["storage_id"]] = 0
            continue
        worked = min(spare_labor, float(task["remaining_hours"]))
        task["worked_hours_today"] = round(worked, 3)
        task["worked_hours_total"] = round(float(task["worked_hours_total"]) + worked, 3)
        task["remaining_hours"] = round(max(0.0, float(task["remaining_hours"]) - worked), 3)
        spare_labor -= worked
        if task["remaining_hours"] <= 0:
            task["status"] = "resolved" if _review_is_accepted(task["review_state"]) else "blocked_review"
            if task["status"] == "resolved":
                storage_quality[task["storage_id"]] = 0
        elif worked > 0:
            task["status"] = "in_progress"
        else:
            task["status"] = "stalled_labor"

    return [
        {
            "day": day,
            "storage_id": task["storage_id"],
            "pattern_id": task["pattern_id"],
            "resource": task["resource"],
            "role": task["role"],
            "estimated_hours": round(float(task["estimated_hours"]), 3),
            "worked_hours_today": round(float(task["worked_hours_today"]), 3),
            "worked_hours_total": round(float(task["worked_hours_total"]), 3),
            "remaining_hours": round(float(task["remaining_hours"]), 3),
            "duration_days": int(task["duration_days"]),
            "days_active": int(task["days_active"]),
            "action": task["action"],
            "review_dependency": task["review_dependency"],
            "review_state": task["review_state"],
            "status": task["status"],
            "provisional": True,
        }
        for task in active_tasks
        if int(task.get("last_seen_day", day)) == day or task["status"] in {"blocked_review", "resolved"}
    ]


def _storage_recovery_hours(recovery_tasks: list[dict[str, Any]]) -> float:
    return sum(float(task.get("worked_hours_today", 0.0)) for task in recovery_tasks)


def _review_context(review_status: dict[str, Any] | None, scenario_context: dict[str, Any] | None = None) -> dict[str, Any]:
    scenario_context = scenario_context or _scenario_context(None)
    scenario_blocked = set(scenario_context.get("blocked_review_domains", []))
    scenario_temporary = set(scenario_context.get("temporary_review_domains", []))
    if not review_status:
        return {
            "source": "",
            "status": "impacted" if scenario_blocked or scenario_temporary else "not_provided",
            "accepted_domains": [],
            "blocked_domains": sorted(scenario_blocked),
            "temporary_domains": sorted(scenario_temporary),
            "scenario_events": scenario_context.get("review_events", []),
            "provisional": True,
        }
    domains = review_status.get("review_status_by_domain", {})
    accepted = [
        domain
        for domain in sorted(domains)
        if domain not in scenario_blocked and _review_is_accepted(_review_dependency_state(review_status, domain))
    ]
    blocked = sorted((set(domains) - set(accepted)) | scenario_blocked)
    return {
        "source": review_status.get("id", ""),
        "status": "impacted" if scenario_blocked else review_status.get("status", "unknown"),
        "accepted_domains": accepted,
        "blocked_domains": blocked,
        "temporary_domains": sorted(scenario_temporary),
        "scenario_events": scenario_context.get("review_events", []),
        "provisional": True,
    }


def _review_dependency_state(
    review_status: dict[str, Any] | None,
    dependency: str,
    scenario_day: dict[str, Any] | None = None,
) -> dict[str, Any]:
    scenario_override = _scenario_review_override_for_dependency(scenario_day or {}, dependency)
    if scenario_override:
        if scenario_override["effect"] == "allows_temporary_recovery":
            return {
                "dependency": dependency,
                "status": scenario_override["status"],
                "accepted": True,
                "reason": f"Scenario override allows temporary recovery: {scenario_override['notes']}",
                "provisional": True,
            }
        return {
            "dependency": dependency,
            "status": scenario_override["status"],
            "accepted": False,
            "reason": f"Scenario override blocks recovery: {scenario_override['notes']}",
            "provisional": True,
        }
    if not review_status:
        return {
            "dependency": dependency,
            "status": "not_provided",
            "accepted": False,
            "reason": "No review-status report was provided to the simulation.",
            "provisional": True,
        }
    domain_status = review_status.get("review_status_by_domain", {}).get(dependency)
    if not domain_status:
        return {
            "dependency": dependency,
            "status": "missing",
            "accepted": False,
            "reason": "Review dependency is absent from the review-status report.",
            "provisional": True,
        }
    expired_or_rejected = review_status.get("expired_or_rejected_evidence", [])
    has_expired_or_rejected = any(item == f"{dependency}:rejected" or item.startswith(f"{dependency}:expired:") for item in expired_or_rejected)
    unresolved_count = int(domain_status.get("unresolved_issue_count", 0))
    accepted = domain_status.get("status") == "accepted" and unresolved_count == 0 and not has_expired_or_rejected
    reasons: list[str] = []
    if domain_status.get("status") != "accepted":
        reasons.append(f"status is {domain_status.get('status')}")
    if unresolved_count:
        reasons.append(f"{unresolved_count} unresolved issue(s)")
    if has_expired_or_rejected:
        reasons.append("expired or rejected evidence")
    return {
        "dependency": dependency,
        "status": domain_status.get("status", "unknown"),
        "accepted": accepted,
        "reason": "accepted, current, and unresolved-issue-free" if accepted else "; ".join(reasons),
        "provisional": True,
    }


def _review_is_accepted(review_state: dict[str, Any]) -> bool:
    return bool(review_state.get("accepted"))


def _scheduled_maintenance_by_day(compiled_plan: dict[str, Any], days: int) -> dict[int, list[dict[str, Any]]]:
    scheduled: dict[int, list[dict[str, Any]]] = defaultdict(list)
    for task in compiled_plan.get("maintenance_calendar", []):
        interval_days = INTERVAL_DAYS.get(task["interval"])
        if interval_days is None:
            continue
        day = 1
        while day <= days:
            scheduled[day].append(
                {
                    "pattern_id": task["pattern_id"],
                    "task_id": task["task_id"],
                    "description": task["description"],
                    "role": task["role"],
                    "estimated_hours": round(float(task["estimated_hours"]), 3),
                    "base_estimated_hours": round(float(task["estimated_hours"]), 3),
                    "interval": task["interval"],
                    "due_day": day,
                    "days_overdue": 0,
                    "provisional": task.get("provisional", True),
                }
            )
            day += interval_days
    return {day: sorted(tasks, key=lambda item: (item["role"], item["task_id"])) for day, tasks in scheduled.items()}


def _maintenance_due_today(
    scheduled_tasks: list[dict[str, Any]],
    backlog: list[dict[str, Any]],
    day: int,
    maintenance_multiplier: float,
) -> list[dict[str, Any]]:
    due: list[dict[str, Any]] = []
    for task in backlog:
        due.append({**task, "days_overdue": int(task["days_overdue"]) + 1})
    for task in scheduled_tasks:
        due.append(
            {
                **task,
                "due_day": day,
                "estimated_hours": round(float(task["base_estimated_hours"]) * maintenance_multiplier, 3),
                "days_overdue": 0,
            }
        )
    return sorted(due, key=lambda item: (-int(item["days_overdue"]), item["due_day"], item["role"], item["task_id"]))


def _resolve_maintenance_day(maintenance_events: list[dict[str, Any]], population_context: dict[str, Any]) -> dict[str, Any]:
    capacity = _available_labor_hours(population_context)
    completed: list[dict[str, Any]] = []
    deferred: list[dict[str, Any]] = []
    completed_hours = 0.0
    required_hours = sum(float(task["estimated_hours"]) for task in maintenance_events)

    for task in maintenance_events:
        task_hours = float(task["estimated_hours"])
        if completed_hours + task_hours <= capacity:
            completed.append({**task, "status": "completed"})
            completed_hours += task_hours
        else:
            deferred.append({**task, "status": "deferred"})

    deferred_hours = sum(float(task["estimated_hours"]) for task in deferred)
    return {
        "required_hours": round(required_hours, 3),
        "completed_hours": round(completed_hours, 3),
        "deferred_hours": round(deferred_hours, 3),
        "capacity_hours": round(capacity, 3),
        "scheduled_count": len(maintenance_events),
        "completed_count": len(completed),
        "deferred_count": len(deferred),
        "backlog_count": len(deferred),
        "backlog_hours": round(deferred_hours, 3),
        "max_days_overdue": max((int(task["days_overdue"]) for task in deferred), default=0),
        "completed_events": completed,
        "deferred_events": deferred,
        "status": _maintenance_state_status(deferred, required_hours, capacity),
        "provisional": True,
    }


def _resource_ledger(daily_states: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    ledger: dict[str, dict[str, Any]] = {}
    for resource in LEDGER_RESOURCES:
        entries = [
            {
                "day": state["day"],
                "season": state["season"],
                "opening_balance": state["resources"][resource]["opening_balance"],
                "production": state["resources"][resource]["production"],
                "consumption": state["resources"][resource]["consumption"],
                "raw_net": state["resources"][resource]["raw_net"],
                "storage_release": state["resources"][resource]["storage_release"],
                "storage_refill": state["resources"][resource]["storage_refill"],
                "curtailment": state["resources"][resource]["curtailment"],
                "net": state["resources"][resource]["net"],
                "ending_balance": state["resources"][resource]["ending_balance"],
                "unmet_demand": state["resources"][resource]["unmet_demand"],
                "status": state["resources"][resource]["status"],
            }
            for state in daily_states
        ]
        ledger[resource] = {
            "entries": entries,
            "total_production": round(sum(float(entry["production"]) for entry in entries), 3),
            "total_consumption": round(sum(float(entry["consumption"]) for entry in entries), 3),
            "total_storage_release": round(sum(float(entry["storage_release"]) for entry in entries), 3),
            "total_storage_refill": round(sum(float(entry["storage_refill"]) for entry in entries), 3),
            "total_curtailment": round(sum(float(entry["curtailment"]) for entry in entries), 3),
            "ending_balance": entries[-1]["ending_balance"],
            "minimum_balance": round(min(float(entry["ending_balance"]) for entry in entries), 3),
            "total_unmet_demand": round(sum(float(entry["unmet_demand"]) for entry in entries), 3),
            "status": _ledger_status(entries),
            "provisional": True,
        }
    return ledger


def _resource_balance(resource_ledger: dict[str, dict[str, Any]], days: int) -> dict[str, dict[str, Any]]:
    balances: dict[str, dict[str, Any]] = {}
    for resource in RESOURCE_KEYS.values():
        summary = resource_ledger[resource]
        net_per_day = (float(summary["total_production"]) - float(summary["total_consumption"])) / days
        ending = float(summary["ending_balance"])
        status = summary["status"]
        balances[resource] = {
            "net_per_day": round(net_per_day, 3),
            "ending_balance": round(ending, 3),
            "minimum_balance": round(float(summary["minimum_balance"]), 3),
            "status": status,
        }
    return balances


def _storage_summary(daily_states: list[dict[str, Any]]) -> dict[str, Any]:
    resource_days: dict[str, list[dict[str, Any]]] = defaultdict(list)
    recovery_tasks: list[dict[str, Any]] = []
    for state in daily_states:
        for resource, summary in state.get("storage_state", {}).get("resources", {}).items():
            resource_days[resource].append(summary)
        recovery_tasks.extend(state.get("storage_state", {}).get("recovery_tasks", []))

    resources: dict[str, dict[str, Any]] = {}
    latest_recovery_tasks = {
        task["storage_id"]: task
        for task in recovery_tasks
    }
    for resource, entries in sorted(resource_days.items()):
        resources[resource] = {
            "capacity": entries[-1]["capacity"],
            "reserve_floor": entries[-1]["reserve_floor"],
            "ending_total": entries[-1]["ending_total"],
            "minimum_total": round(min(float(entry["ending_total"]) for entry in entries), 3),
            "total_released": round(sum(float(entry["released"]) for entry in entries), 3),
            "total_refilled": round(sum(float(entry["refilled"]) for entry in entries), 3),
            "total_quality_loss": round(sum(float(entry["quality_loss"]) for entry in entries), 3),
            "total_curtailed": round(sum(float(entry["curtailed"]) for entry in entries), 3),
            "quality_status": _storage_entries_status([{"status": entry["quality_status"]} for entry in entries]),
            "status": _storage_entries_status(entries),
            "provisional": True,
        }
    return {
        "resources": resources,
        "recovery": {
            "active_task_count": len(latest_recovery_tasks),
            "total_estimated_hours": round(sum(float(task["estimated_hours"]) for task in latest_recovery_tasks.values()), 3),
            "total_worked_hours": round(sum(float(task.get("worked_hours_today", 0.0)) for task in recovery_tasks), 3),
            "total_remaining_hours": round(sum(float(task["remaining_hours"]) for task in latest_recovery_tasks.values()), 3),
            "blocked_review_count": sum(1 for task in latest_recovery_tasks.values() if task["status"] == "blocked_review"),
            "resolved_count": sum(1 for task in latest_recovery_tasks.values() if task["status"] == "resolved"),
            "stalled_labor_days": sum(1 for task in recovery_tasks if task["status"] == "stalled_labor"),
            "tasks": sorted(latest_recovery_tasks.values(), key=lambda item: item["storage_id"]),
            "status": _recovery_summary_status(list(latest_recovery_tasks.values())),
            "provisional": True,
        },
        "status": _storage_entries_status([entry for entries in resource_days.values() for entry in entries]),
        "provisional": True,
    }


def _storage_entries_status(entries: list[dict[str, Any]]) -> str:
    return _worst_status([entry["status"] for entry in entries])


def _recovery_summary_status(tasks: list[dict[str, Any]]) -> str:
    if not tasks:
        return "pass"
    if all(task["status"] == "resolved" for task in tasks):
        return "pass"
    if any(task["status"] in {"stalled_labor", "blocked_review"} for task in tasks):
        return "warn"
    return "warn"


def _maintenance_summary(compiled_plan: dict[str, Any], daily_states: list[dict[str, Any]], days: int) -> dict[str, Any]:
    scheduled_tasks: list[dict[str, Any]] = []
    hours_by_role: dict[str, float] = defaultdict(float)
    unknown_intervals: list[str] = []

    for task in compiled_plan.get("maintenance_calendar", []):
        interval = task["interval"]
        interval_days = INTERVAL_DAYS.get(interval)
        if interval_days is None:
            unknown_intervals.append(f"{task['pattern_id']}:{task['task_id']} uses unsupported interval {interval}")
            runs = 0
        else:
            runs = max(1, math.ceil(days / interval_days))

        total_hours = float(task["estimated_hours"]) * runs
        hours_by_role[task["role"]] += total_hours
        scheduled_tasks.append(
            {
                "pattern_id": task["pattern_id"],
                "task_id": task["task_id"],
                "interval": interval,
                "runs": runs,
                "estimated_total_hours": round(total_hours, 3),
                "role": task["role"],
                "provisional": task.get("provisional", True),
            }
        )

    total_hours = sum(hours_by_role.values())
    max_backlog_count = max((state["maintenance_state"]["backlog_count"] for state in daily_states), default=0)
    max_backlog_hours = max((state["maintenance_state"]["backlog_hours"] for state in daily_states), default=0.0)
    max_days_overdue = max((state["maintenance_state"]["max_days_overdue"] for state in daily_states), default=0)
    deferred_event_count = sum(state["maintenance_state"]["deferred_count"] for state in daily_states)
    completed_event_count = sum(state["maintenance_state"]["completed_count"] for state in daily_states)
    max_degradation = max((state["system_degradation"]["max_degradation_factor"] for state in daily_states), default=0.0)
    return {
        "scheduled_task_count": len(scheduled_tasks),
        "scheduled_tasks": scheduled_tasks,
        "total_estimated_hours": round(total_hours, 3),
        "hours_by_role": {role: round(hours, 3) for role, hours in sorted(hours_by_role.items())},
        "unsupported_intervals": unknown_intervals,
        "overdue_task_count": max_backlog_count,
        "max_backlog_hours": round(max_backlog_hours, 3),
        "max_days_overdue": max_days_overdue,
        "completed_event_count": completed_event_count,
        "deferred_event_count": deferred_event_count,
        "max_degradation_factor": round(max_degradation, 3),
        "status": _maintenance_summary_status(max_backlog_count, max_days_overdue, unknown_intervals),
    }


def _labor_summary(compiled_plan: dict[str, Any], maintenance: dict[str, Any], daily_states: list[dict[str, Any]], days: int) -> dict[str, Any]:
    population_context = _population_context(compiled_plan)
    population = int(population_context["population"])
    weeks = days / 7
    storage_recovery_hours = sum(
        float(task.get("worked_hours_today", 0.0))
        for state in daily_states
        for task in state.get("storage_state", {}).get("recovery_tasks", [])
    )
    scenario_emergency_hours = sum(float(state.get("labor", {}).get("scenario_emergency_hours", 0.0)) for state in daily_states)
    runtime_failure_response_hours = sum(_failure_response_hours(state.get("active_failures", [])) for state in daily_states)
    total_labor_hours = (
        float(maintenance["total_estimated_hours"])
        + storage_recovery_hours
        + scenario_emergency_hours
        + runtime_failure_response_hours
    )
    weekly_hours = total_labor_hours / weeks if weeks else 0
    per_resident = weekly_hours / population if population else weekly_hours
    average_available_daily = sum(float(state["labor"]["available_commons_hours"]) for state in daily_states) / days if days else 0.0
    available_weekly = average_available_daily * 7
    utilization = weekly_hours / available_weekly if available_weekly else 999.0
    status = "pass"
    if per_resident > 12 or utilization > 1:
        status = "fail"
    elif per_resident > 8 or utilization > 0.75:
        status = "warn"
    return {
        "population": population,
        "household_count": population_context["household_count"],
        "weeks": round(weeks, 3),
        "estimated_maintenance_hours_per_week": round(weekly_hours, 3),
        "scheduled_maintenance_hours": round(float(maintenance["total_estimated_hours"]), 3),
        "storage_recovery_hours": round(storage_recovery_hours, 3),
        "scenario_emergency_hours": round(scenario_emergency_hours, 3),
        "runtime_failure_response_hours": round(runtime_failure_response_hours, 3),
        "available_commons_labor_hours_per_week": round(available_weekly, 3),
        "labor_utilization": round(utilization, 3),
        "care_hours_per_week": population_context["care_hours_per_week"],
        "protected_labor_hours_per_week": population_context["protected_labor_hours_per_week"],
        "estimated_hours_per_resident_per_week": round(per_resident, 3),
        "status": status,
        "thresholds": {
            "warn_above_hours_per_resident_per_week": 8,
            "fail_above_hours_per_resident_per_week": 12,
        },
    }


def _triggered_risks(compiled_plan: dict[str, Any]) -> list[dict[str, Any]]:
    triggered: list[dict[str, Any]] = []
    for risk in compiled_plan.get("risk_register", []):
        if risk["severity"] == "catastrophic" or risk["likelihood"] == "high":
            triggered.append(
                {
                    "pattern_id": risk["pattern_id"],
                    "mode": risk["mode"],
                    "severity": risk["severity"],
                    "likelihood": risk["likelihood"],
                    "reason": "High-consequence risk requires explicit stress simulation before promotion.",
                    "mitigation": risk["mitigation"],
                }
            )
    return triggered


def _runtime_failures(compiled_plan: dict[str, Any], scenario: dict[str, Any] | None, days: int) -> list[dict[str, Any]]:
    if not scenario:
        return []
    triggered_modes = set(scenario.get("triggered_risk_modes", []))
    overrides = {
        override["mode"]: override
        for override in scenario.get("runtime_failure_overrides", [])
    }
    failures: list[dict[str, Any]] = []
    for risk in compiled_plan.get("risk_register", []):
        if risk["mode"] not in triggered_modes:
            continue
        effect = _failure_effect_template(risk["mode"])
        override = overrides.get(risk["mode"], {})
        start_day = min(max(1, int(override.get("start_day", 1))), days)
        duration_days = min(max(1, int(override.get("duration_days", days))), days - start_day + 1)
        response_hours = float(override.get("response_hours_per_day", effect["response_hours_per_day"]))
        failures.append(
            {
                "pattern_id": risk["pattern_id"],
                "mode": risk["mode"],
                "severity": risk["severity"],
                "likelihood": risk["likelihood"],
                "start_day": start_day,
                "recovery_day": start_day + duration_days,
                "duration_days": duration_days,
                "resource_effects": effect["resource_effects"],
                "response_hours_per_day": response_hours,
                "response_role": effect["response_role"],
                "mitigation": risk["mitigation"],
                "unresolved_review_dependency": _review_dependency_for_mode(risk["mode"]),
                "override_notes": override.get("notes", ""),
                "provisional": True,
            }
        )
    return sorted(failures, key=lambda item: (item["pattern_id"], item["mode"]))


def _failure_effect_template(mode: str) -> dict[str, Any]:
    templates: dict[str, dict[str, Any]] = {
        "battery_fault": {
            "resource_effects": {"energy_kwh": {"production_loss_factor": 0.65, "consumption_increase_factor": 0.05}},
            "response_hours_per_day": 2.0,
            "response_role": "energy_steward",
        },
        "stored_water_contamination": {
            "resource_effects": {"water_liters": {"production_loss_factor": 0.8, "consumption_increase_factor": 0.1}},
            "response_hours_per_day": 2.0,
            "response_role": "water_steward",
        },
        "contaminated_source": {
            "resource_effects": {"water_liters": {"production_loss_factor": 1.0, "consumption_increase_factor": 0.1}},
            "response_hours_per_day": 3.0,
            "response_role": "water_steward",
        },
        "crop_failure": {
            "resource_effects": {"food_servings": {"production_loss_factor": 0.85, "consumption_increase_factor": 0.0}},
            "response_hours_per_day": 1.5,
            "response_role": "food_steward",
        },
        "foodborne_illness": {
            "resource_effects": {"food_servings": {"production_loss_factor": 0.35, "consumption_increase_factor": 0.1}},
            "response_hours_per_day": 2.0,
            "response_role": "kitchen_steward",
        },
        "pathogen_exposure": {
            "resource_effects": {"water_liters": {"production_loss_factor": 0.15, "consumption_increase_factor": 0.15}},
            "response_hours_per_day": 2.0,
            "response_role": "sanitation_steward",
        },
        "pathogen_persistence": {
            "resource_effects": {"water_liters": {"production_loss_factor": 0.0, "consumption_increase_factor": 0.05}},
            "response_hours_per_day": 1.5,
            "response_role": "sanitation_steward",
        },
        "tool_capture": {
            "resource_effects": {"labor_hours": {"production_loss_factor": 0.1, "consumption_increase_factor": 0.05}},
            "response_hours_per_day": 1.0,
            "response_role": "tool_steward",
        },
    }
    return templates.get(
        mode,
        {
            "resource_effects": {
                "labor_hours": {"production_loss_factor": 0.0, "consumption_increase_factor": 0.05},
            },
            "response_hours_per_day": 1.0,
            "response_role": "maintenance_steward",
        },
    )


def _review_dependency_for_mode(mode: str) -> str:
    if "water" in mode or "contamin" in mode or "pathogen" in mode:
        return "water_public_health"
    if "battery" in mode or "energy" in mode:
        return "electrical"
    if "crop" in mode or "food" in mode:
        return "food_safety"
    if "tool" in mode:
        return "workshop_safety"
    return "professional_review"


def _active_failures_for_day(runtime_failures: list[dict[str, Any]], day: int) -> list[dict[str, Any]]:
    return [
        failure
        for failure in runtime_failures
        if int(failure["start_day"]) <= day < int(failure["recovery_day"])
    ]


def _failure_effect_for_pattern(active_failures: list[dict[str, Any]], pattern_id: str) -> dict[str, dict[str, float]]:
    effect: dict[str, dict[str, float]] = {}
    for failure in active_failures:
        if failure["pattern_id"] != pattern_id:
            continue
        for resource, values in failure["resource_effects"].items():
            current = effect.setdefault(resource, {"production_loss_factor": 0.0, "consumption_increase_factor": 0.0})
            current["production_loss_factor"] += float(values.get("production_loss_factor", 0.0))
            current["consumption_increase_factor"] += float(values.get("consumption_increase_factor", 0.0))
    return effect


def _failure_response_hours(active_failures: list[dict[str, Any]]) -> float:
    return sum(float(failure["response_hours_per_day"]) for failure in active_failures)


def _active_failure_risks(active_failures: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "type": "runtime_failure",
            "pattern_id": failure["pattern_id"],
            "mode": failure["mode"],
            "severity": failure["severity"],
            "response_role": failure["response_role"],
            "response_hours_per_day": failure["response_hours_per_day"],
            "unresolved_review_dependency": failure["unresolved_review_dependency"],
            "provisional": True,
        }
        for failure in active_failures
    ]


def _timeline(
    daily_states: list[dict[str, Any]],
    resource_balance: dict[str, dict[str, Any]],
    labor: dict[str, Any],
    triggered_risks: list[dict[str, Any]],
    scenario_context: dict[str, Any],
) -> list[dict[str, Any]]:
    events: list[dict[str, Any]] = [
        {
            "day": 1,
            "event": "simulation_started",
            "severity": "info",
            "description": "Deterministic daily simulation state initialized.",
        }
    ]
    if scenario_context.get("active"):
        events.append(
            {
                "day": 1,
                "event": f"scenario_replay_started:{scenario_context['id']}",
                "severity": "warning",
                "description": "Scenario modifiers are applied inside the daily simulation loop.",
            }
        )
    for state in daily_states:
        for scenario_event in state.get("scenario_events", []):
            event_type = scenario_event["type"]
            if event_type == "emergency_task":
                events.append(
                    {
                        "day": state["day"],
                        "event": f"scenario_emergency_task:{scenario_event['id']}",
                        "severity": "warning",
                        "description": scenario_event["description"],
                    }
                )
            if event_type == "review_context":
                events.append(
                    {
                        "day": state["day"],
                        "event": f"scenario_review_context:{scenario_event['id']}",
                        "severity": "error" if scenario_event["effect"] == "blocks_recovery" else "warning",
                        "description": f"{scenario_event['status']} -> {scenario_event['effect']}: {scenario_event['description']}",
                    }
                )
        if state["maintenance_events"]:
            events.append(
                {
                    "day": state["day"],
                    "event": "maintenance_scheduled",
                    "severity": "info",
                    "description": f"{len(state['maintenance_events'])} maintenance task(s) scheduled.",
                }
            )
        if state["maintenance_state"]["deferred_count"]:
            events.append(
                {
                    "day": state["day"],
                    "event": "maintenance_deferred",
                    "severity": "error" if state["maintenance_state"]["status"] == "fail" else "warning",
                    "description": f"{state['maintenance_state']['deferred_count']} maintenance task(s) deferred.",
                }
            )
        if state["active_failures"]:
            events.append(
                {
                    "day": state["day"],
                    "event": "runtime_failure_active",
                    "severity": "error" if any(failure["severity"] == "catastrophic" for failure in state["active_failures"]) else "warning",
                    "description": ", ".join(failure["mode"] for failure in state["active_failures"]),
                }
            )
        if state["system_degradation"]["max_degradation_factor"] > 0:
            events.append(
                {
                    "day": state["day"],
                    "event": "maintenance_degradation_active",
                    "severity": "warning",
                    "description": f"Max provisional degradation factor: {state['system_degradation']['max_degradation_factor']}.",
                }
            )
        if state["unmet_needs"]:
            events.append(
                {
                    "day": state["day"],
                    "event": "unmet_need",
                    "severity": "error",
                    "description": ", ".join(state["unmet_needs"]),
                }
            )
        if state["storage_state"]["status"] != "pass":
            events.append(
                {
                    "day": state["day"],
                    "event": "storage_quality_or_reserve_warning",
                    "severity": "error" if state["storage_state"]["status"] == "fail" else "warning",
                    "description": ", ".join(
                        resource
                        for resource, summary in state["storage_state"]["resources"].items()
                        if summary["status"] != "pass"
                    ),
                }
            )
        if state["storage_state"].get("recovery_tasks"):
            events.append(
                {
                    "day": state["day"],
                    "event": "storage_recovery_required",
                    "severity": "error",
                    "description": f"{len(state['storage_state']['recovery_tasks'])} storage recovery task(s) required.",
                }
            )
    for resource, summary in resource_balance.items():
        if summary["status"] == "fail":
            events.append(
                {
                    "day": 1,
                    "event": f"resource_deficit:{resource}",
                    "severity": "error",
                    "description": f"{resource} has negative modeled daily balance.",
                }
            )
    if labor["status"] != "pass":
        events.append(
            {
                "day": 1,
                "event": "labor_burden",
                "severity": "error" if labor["status"] == "fail" else "warning",
                "description": "Recurring maintenance labor exceeds a fair-work threshold.",
            }
        )
    if triggered_risks:
        events.append(
            {
                "day": 1,
                "event": "high_consequence_risks_identified",
                "severity": "warning",
                "description": f"{len(triggered_risks)} high-consequence risk mode(s) require scenario testing.",
            }
        )
    return sorted(events, key=lambda item: (item["day"], item["event"]))


def _bottlenecks(
    resource_balance: dict[str, dict[str, Any]],
    labor: dict[str, Any],
    maintenance: dict[str, Any],
    compiled_plan: dict[str, Any],
) -> list[str]:
    bottlenecks: list[str] = []
    for resource, summary in resource_balance.items():
        if summary["status"] == "fail":
            bottlenecks.append(f"{resource} has negative daily balance")
        elif summary["status"] == "warn":
            bottlenecks.append(f"{resource} has no modeled daily buffer")
    if labor["status"] != "pass":
        bottlenecks.append("maintenance labor burden exceeds fair-work threshold")
    if maintenance["unsupported_intervals"]:
        bottlenecks.append("one or more maintenance intervals cannot be scheduled")
    if maintenance["overdue_task_count"]:
        bottlenecks.append("maintenance backlog is degrading one or more systems")
    if "greenhouse" in compiled_plan.get("selected_patterns", []):
        bottlenecks.append("food model is partial: greenhouse output is not a complete nutrition plan")
    return bottlenecks


def _gate_recommendations(
    resource_balance: dict[str, dict[str, Any]],
    labor: dict[str, Any],
    maintenance: dict[str, Any],
    triggered_risks: list[dict[str, Any]],
) -> list[str]:
    recommendations: list[str] = []
    if resource_balance["water_liters"]["status"] != "pass":
        recommendations.append("Revise water supply, demand, storage, or redundancy before promotion.")
    if resource_balance["energy_kwh"]["status"] != "pass":
        recommendations.append("Revise critical-load energy supply, demand, or storage before promotion.")
    if resource_balance["food_servings"]["status"] != "pass":
        recommendations.append("Add full nutrition, crop, storage, preservation, and procurement modeling.")
    if labor["status"] != "pass":
        recommendations.append("Reduce recurring labor or add trained participants before promotion.")
    if maintenance["unsupported_intervals"]:
        recommendations.append("Normalize all maintenance intervals to supported simulation intervals.")
    if maintenance["overdue_task_count"]:
        recommendations.append("Reduce maintenance load, add trained capacity, or redesign systems to clear backlog.")
    if triggered_risks:
        recommendations.append("Run scarcity, disaster, and social stress simulations for high-consequence risks.")
    return recommendations


def _unknowns(compiled_plan: dict[str, Any], scenario_context: dict[str, Any] | None = None) -> list[str]:
    unknowns = [
        "Daily state uses deterministic provisional flows; no stochastic failure model exists.",
        "Seasonal multipliers are authored planning assumptions, not site-specific weather or crop calendars.",
        "Storage capacities, reserve floors, release rates, refill rates, and quality clocks are provisional planning assumptions, not engineered tank, battery, pantry, public-health, or sanitation designs.",
        "Maintenance degradation is a provisional penalty model, not measured equipment reliability.",
        "Household labor and demand profiles are provisional examples, not resident commitments.",
        "No jurisdiction-specific legal, engineering, health, or building code validation exists.",
        "Food servings are not nutrition, crop diversity, preservation, or procurement plans.",
    ]
    if compiled_plan.get("simulation_inputs", {}).get("provisional"):
        unknowns.append("All resource effects are provisional seed assumptions from pattern data.")
    if scenario_context and scenario_context.get("active"):
        unknowns.append("Scenario replay applies authored stress modifiers deterministically; it is not a weather, epidemiology, outage, logistics, or public-health model.")
    return unknowns


def _status(
    resource_balance: dict[str, dict[str, Any]],
    labor: dict[str, Any],
    maintenance: dict[str, Any],
    triggered_risks: list[dict[str, Any]],
) -> str:
    if any(summary["status"] == "fail" for summary in resource_balance.values()):
        return "fail"
    if labor["status"] == "fail" or maintenance["unsupported_intervals"] or maintenance["max_days_overdue"] > 7:
        return "fail"
    if (
        triggered_risks
        or labor["status"] == "warn"
        or maintenance["overdue_task_count"]
        or any(summary["status"] == "warn" for summary in resource_balance.values())
    ):
        return "warn"
    return "pass"


def _population_context(compiled_plan: dict[str, Any]) -> dict[str, Any]:
    household_profile = compiled_plan.get("simulation_inputs", {}).get("household_profile")
    if not household_profile:
        population = int(compiled_plan["site_summary"]["population_target"])
        weekly_labor = population * 14.0
        return {
            "source": "site_population_target",
            "population": population,
            "household_count": int(compiled_plan["site_summary"].get("households", 0)),
            "available_commons_labor_hours_per_week": round(weekly_labor, 3),
            "available_commons_labor_hours_per_day": round(weekly_labor / 7, 3),
            "care_hours_per_week": 0.0,
            "protected_labor_hours_per_week": 0.0,
            "daily_resource_demand_adjustments": {
                "water_liters": 0.0,
                "energy_kwh": 0.0,
                "food_servings": 0.0,
            },
            "provisional": True,
        }
    households = household_profile["households"]
    population = sum(int(h["adults"]) + int(h["children"]) + int(h["elders"]) for h in households)
    weekly_labor = sum(float(h["available_commons_labor_hours_per_week"]) for h in households)
    care_hours = sum(float(h["care_hours_per_week"]) for h in households)
    protected_hours = sum(float(h["protected_labor_hours_per_week"]) for h in households)
    return {
        "source": household_profile["id"],
        "population": population,
        "household_count": len(households),
        "available_commons_labor_hours_per_week": round(weekly_labor, 3),
        "available_commons_labor_hours_per_day": round(weekly_labor / 7, 3),
        "care_hours_per_week": round(care_hours, 3),
        "protected_labor_hours_per_week": round(protected_hours, 3),
        "daily_resource_demand_adjustments": {
            resource: round(float(value), 3)
            for resource, value in household_profile["daily_resource_demand_adjustments"].items()
        },
        "provisional": household_profile.get("provisional", True),
    }


def _simulation_id(compiled_plan: dict[str, Any], scenario_context: dict[str, Any], days: int) -> str:
    if scenario_context["active"]:
        return f"{compiled_plan['id']}_{scenario_context['id']}_replay_{days}d"
    return f"{compiled_plan['id']}_normal_year_{days}d"


def _scenario_context(scenario: dict[str, Any] | None) -> dict[str, Any]:
    if not scenario:
        return {
            "active": False,
            "id": "",
            "name": "",
            "days": 0,
            "resource_multipliers": {},
            "resource_deltas": {},
            "labor_capacity_multiplier": 1.0,
            "emergency_tasks": [],
            "labor_support": [],
            "triggered_risk_modes": [],
            "review_events": [],
            "blocked_review_domains": [],
            "temporary_review_domains": [],
            "provisional": True,
        }
    review_events = [
        {
            "domain": item["domain"],
            "status": item["status"],
            "effect": item["effect"],
            "day": int(item["day"]),
            "notes": item["notes"],
            "provisional": True,
        }
        for item in scenario.get("review_context_overrides", [])
    ]
    return {
        "active": True,
        "id": scenario["id"],
        "name": scenario.get("name", scenario["id"]),
        "days": int(scenario.get("days", 0)),
        "resource_multipliers": scenario.get("resource_multipliers", {}),
        "resource_deltas": scenario.get("resource_deltas", {}),
        "labor_capacity_multiplier": float(scenario.get("labor_capacity_multiplier", 1.0)),
        "emergency_tasks": scenario.get("emergency_tasks", []),
        "labor_support": scenario.get("labor_support", []),
        "triggered_risk_modes": scenario.get("triggered_risk_modes", []),
        "review_events": sorted(review_events, key=lambda item: (item["day"], item["domain"], item["status"])),
        "blocked_review_domains": sorted(
            item["domain"]
            for item in review_events
            if item["effect"] in {"blocks_recovery", "requires_external_review"}
        ),
        "temporary_review_domains": sorted(
            item["domain"]
            for item in review_events
            if item["effect"] == "allows_temporary_recovery"
        ),
        "provisional": scenario.get("provisional", True),
    }


def _scenario_day_context(scenario: dict[str, Any] | None, day: int) -> dict[str, Any]:
    context = _scenario_context(scenario)
    if not context["active"] or day > int(context["days"]):
        return {**_scenario_context(None), "day": day, "events": []}
    events: list[dict[str, Any]] = []
    for task in context["emergency_tasks"]:
        if int(task["day"]) == day:
            events.append(
                {
                    "type": "emergency_task",
                    "id": task["id"],
                    "description": task["description"],
                    "role": task["role"],
                    "hours": round(float(task["total_hours"]), 3),
                    "provisional": True,
                }
            )
    for event in context["review_events"]:
        if int(event["day"]) == day:
            events.append(
                {
                    "type": "review_context",
                    "id": event["domain"],
                    "description": event["notes"],
                    "status": event["status"],
                    "effect": event["effect"],
                    "provisional": True,
                }
            )
    for support in context.get("labor_support", []):
        start = int(support["start_day"])
        end = start + int(support["duration_days"])
        if start <= day < end:
            events.append(
                {
                    "type": "labor_support",
                    "id": support["id"],
                    "description": support["notes"],
                    "source": support["source"],
                    "hours": round(float(support["hours_per_day"]), 3),
                    "provisional": True,
                }
            )
    return {**context, "day": day, "events": events}


def _population_context_for_scenario_day(
    population_context: dict[str, Any],
    scenario_day: dict[str, Any],
) -> dict[str, Any]:
    multiplier = float(scenario_day.get("labor_capacity_multiplier", 1.0))
    support_hours = _scenario_labor_support_hours(scenario_day)
    if multiplier == 1.0 and not support_hours:
        return population_context
    adjusted = dict(population_context)
    adjusted["available_commons_labor_hours_per_week"] = round(
        float(population_context["available_commons_labor_hours_per_week"]) * multiplier,
        3,
    )
    adjusted["available_commons_labor_hours_per_day"] = round(
        float(population_context["available_commons_labor_hours_per_day"]) * multiplier,
        3,
    )
    if support_hours:
        adjusted["available_commons_labor_hours_per_day"] = round(
            float(adjusted["available_commons_labor_hours_per_day"]) + support_hours,
            3,
        )
        adjusted["available_commons_labor_hours_per_week"] = round(
            float(adjusted["available_commons_labor_hours_per_week"]) + (support_hours * 7),
            3,
        )
        adjusted["scenario_labor_support_hours_per_day"] = round(support_hours, 3)
    adjusted["scenario_labor_capacity_multiplier"] = round(multiplier, 3)
    return adjusted


def _apply_scenario_resource_modifier(
    resource: str,
    production: float,
    consumption: float,
    scenario_day: dict[str, Any],
) -> tuple[float, float]:
    if not scenario_day.get("active"):
        return production, consumption
    multiplier = float(scenario_day.get("resource_multipliers", {}).get(resource, 1.0))
    delta = float(scenario_day.get("resource_deltas", {}).get(resource, 0.0))
    production *= multiplier
    if delta >= 0:
        production += delta
    else:
        consumption += abs(delta)
    return production, consumption


def _scenario_emergency_hours(scenario_day: dict[str, Any]) -> float:
    return sum(float(event.get("hours", 0.0)) for event in scenario_day.get("events", []) if event.get("type") == "emergency_task")


def _scenario_labor_support_hours(scenario_day: dict[str, Any]) -> float:
    return sum(float(event.get("hours", 0.0)) for event in scenario_day.get("events", []) if event.get("type") == "labor_support")


def _scenario_review_override_for_dependency(
    scenario_day: dict[str, Any],
    dependency: str,
) -> dict[str, Any] | None:
    if not scenario_day.get("active"):
        return None
    current_day = int(scenario_day.get("day", 0))
    candidates = [
        event
        for event in scenario_day.get("review_events", [])
        if event["domain"] == dependency and int(event["day"]) <= current_day
    ]
    if not candidates:
        return None
    return sorted(candidates, key=lambda item: int(item["day"]))[-1]


def _available_labor_hours(population_context: dict[str, Any]) -> float:
    return float(population_context["available_commons_labor_hours_per_day"])


def _daily_resource_status(ending_balance: float, unmet_demand: float, storage_state: dict[str, Any] | None = None) -> str:
    if unmet_demand > 0:
        return "fail"
    if storage_state and storage_state["status"] != "pass":
        return storage_state["status"]
    if ending_balance == 0:
        return "warn"
    return "pass"


def _ledger_status(entries: list[dict[str, Any]]) -> str:
    if any(entry["status"] == "fail" for entry in entries):
        return "fail"
    if any(entry["status"] == "warn" for entry in entries):
        return "warn"
    return "pass"


def _maintenance_state_status(deferred: list[dict[str, Any]], required_hours: float, capacity: float) -> str:
    if any(int(task["days_overdue"]) > 7 for task in deferred):
        return "fail"
    if deferred or required_hours > capacity:
        return "warn"
    return "pass"


def _maintenance_summary_status(max_backlog_count: int, max_days_overdue: int, unknown_intervals: list[str]) -> str:
    if unknown_intervals or max_days_overdue > 7:
        return "fail"
    if max_backlog_count:
        return "warn"
    return "pass"


def _degradation_by_pattern(backlog: list[dict[str, Any]]) -> dict[str, float]:
    by_pattern: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for task in backlog:
        by_pattern[task["pattern_id"]].append(task)
    degradation: dict[str, float] = {}
    for pattern_id, tasks in by_pattern.items():
        max_days = max(int(task["days_overdue"]) for task in tasks)
        value = min(0.5, (0.02 * max_days) + (0.03 * len(tasks)))
        if value > 0:
            degradation[pattern_id] = value
    return degradation


def _active_maintenance_risks(backlog: list[dict[str, Any]], degradation_by_pattern: dict[str, float]) -> list[dict[str, Any]]:
    if not backlog:
        return []
    risks: list[dict[str, Any]] = []
    for pattern_id, degradation in sorted(degradation_by_pattern.items()):
        overdue_tasks = [task for task in backlog if task["pattern_id"] == pattern_id]
        risks.append(
            {
                "type": "maintenance_backlog",
                "pattern_id": pattern_id,
                "task_count": len(overdue_tasks),
                "max_days_overdue": max(int(task["days_overdue"]) for task in overdue_tasks),
                "degradation_factor": round(degradation, 3),
                "severity": "warning" if degradation < 0.25 else "error",
                "provisional": True,
            }
        )
    return risks


def _daily_labor_status(maintenance_hours: float, population_context: dict[str, Any]) -> str:
    population = int(population_context["population"])
    available = _available_labor_hours(population_context)
    if population <= 0 or available <= 0:
        return "fail"
    hours_per_resident_per_week = (maintenance_hours / population) * 7
    utilization = maintenance_hours / available
    if hours_per_resident_per_week > 12 or utilization > 1:
        return "fail"
    if hours_per_resident_per_week > 8 or utilization > 0.75:
        return "warn"
    return "pass"


def _season_for_day(day: int, seasonal_profile: dict[str, Any] | None = None) -> str:
    season = _season_for_profile_day(seasonal_profile, day)
    if season:
        return season["id"]
    normalized = ((day - 1) % 365) + 1
    if normalized <= 59:
        return "winter"
    if normalized <= 151:
        return "spring"
    if normalized <= 243:
        return "summer"
    if normalized <= 334:
        return "fall"
    return "winter"


def _seasonal_multipliers(seasonal_profile: dict[str, Any] | None, day: int) -> dict[str, Any]:
    season = _season_for_profile_day(seasonal_profile, day)
    if not season:
        return {}
    return {
        "resource_multipliers": season.get("resource_multipliers", {}),
        "maintenance_labor_multiplier": season.get("maintenance_labor_multiplier", 1.0),
    }


def _season_for_profile_day(seasonal_profile: dict[str, Any] | None, day: int) -> dict[str, Any] | None:
    if not seasonal_profile:
        return None
    normalized = ((day - 1) % 365) + 1
    for season in seasonal_profile.get("seasons", []):
        if int(season["start_day"]) <= normalized <= int(season["end_day"]):
            return season
    return None
