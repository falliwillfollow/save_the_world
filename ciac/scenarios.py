from __future__ import annotations

from typing import Any

from .simulation import simulate


SURVIVAL_RESOURCES = {
    "water_liters": "water_gate",
    "energy_kwh": "energy_gate",
    "food_servings": "food_gate",
}


def run_scenario(compiled_plan: dict[str, Any], scenario: dict[str, Any]) -> dict[str, Any]:
    days = int(scenario["days"])
    baseline = simulate(compiled_plan, days=days)
    runtime = simulate(compiled_plan, days=days, scenario=scenario)
    resource_balance = _scenario_resource_balance(baseline["resource_balance"], runtime.get("storage", {}), scenario, days)
    emergency_labor = _emergency_labor(compiled_plan, runtime["maintenance"], runtime["runtime_failures"], scenario, days)
    review_context = _review_context(scenario, runtime["runtime_failures"])
    triggered_risks = _scenario_triggered_risks(compiled_plan, baseline["triggered_risks"], scenario)
    affected_resources = _affected_resources(scenario, resource_balance)
    failure_timeline = _failure_timeline(resource_balance, emergency_labor, review_context, triggered_risks, runtime["runtime_failures"], scenario)
    gate_failures = _survival_critical_gate_failures(resource_balance, emergency_labor)
    bottlenecks = _bottlenecks(resource_balance, emergency_labor, review_context, triggered_risks, scenario)
    recommended_redesigns = _recommended_redesigns(resource_balance, emergency_labor, review_context, triggered_risks, scenario)
    status = _status(gate_failures, emergency_labor, review_context, triggered_risks)

    return {
        "kind": "ScenarioRun",
        "id": f"{compiled_plan['id']}_{scenario['id']}_{days}d",
        "compiled_plan": compiled_plan["id"],
        "scenario": scenario["id"],
        "generated_by": "ciac.scenarios.v0",
        "days": days,
        "provisional": True,
        "status": status,
        "baseline_status": baseline["status"],
        "runtime_failures": runtime["runtime_failures"],
        "failure_timeline": failure_timeline,
        "affected_resources": affected_resources,
        "resource_balance": resource_balance,
        "emergency_labor": emergency_labor,
        "review_context": review_context,
        "triggered_risks": triggered_risks,
        "bottlenecks": bottlenecks,
        "survival_critical_gate_failures": gate_failures,
        "recommended_redesigns": recommended_redesigns,
        "unknowns": [
            "Scenario modifiers are provisional and deterministic.",
            "Scenario storage use is a simple linear drawdown/refill approximation; no weather sequence, contamination transport, medical outcome, or behavior model is included.",
            "Scenario review context is a stress input, not an actual professional review or legal determination.",
            "Scenario output identifies design pressure points; it is not a real-world safety certification.",
            scenario["notes"],
        ],
    }


def _scenario_resource_balance(
    baseline_balance: dict[str, dict[str, Any]],
    storage: dict[str, Any],
    scenario: dict[str, Any],
    days: int,
) -> dict[str, dict[str, Any]]:
    multipliers = scenario["resource_multipliers"]
    deltas = scenario["resource_deltas"]
    adjusted: dict[str, dict[str, Any]] = {}
    storage_resources = storage.get("resources", {})
    for resource, baseline in baseline_balance.items():
        net = float(baseline["net_per_day"])
        modified_net = (net * float(multipliers.get(resource, 1))) + float(deltas.get(resource, 0))
        stored = storage_resources.get(resource, {})
        baseline_ending = float(baseline["ending_balance"])
        baseline_minimum = float(baseline["minimum_balance"])
        reserve_floor = float(stored.get("reserve_floor", 0.0))
        scenario_delta = (modified_net - net) * days
        ending = baseline_ending + scenario_delta
        minimum = min(baseline_minimum, ending)
        status = "pass"
        if ending < 0 or minimum < 0:
            status = "fail"
        elif modified_net == 0 or (reserve_floor and ending <= reserve_floor):
            status = "warn"
        adjusted[resource] = {
            "baseline_net_per_day": round(net, 3),
            "scenario_net_per_day": round(modified_net, 3),
            "baseline_ending_buffer": round(baseline_ending, 3),
            "reserve_floor": round(reserve_floor, 3),
            "ending_balance": round(ending, 3),
            "minimum_balance": round(minimum, 3),
            "status": status,
        }
    return adjusted


def _emergency_labor(
    compiled_plan: dict[str, Any],
    baseline_maintenance: dict[str, Any],
    runtime_failures: list[dict[str, Any]],
    scenario: dict[str, Any],
    days: int,
) -> dict[str, Any]:
    population = int(compiled_plan["site_summary"]["population_target"])
    baseline_hours = float(baseline_maintenance["total_estimated_hours"])
    emergency_tasks = scenario["emergency_tasks"]
    emergency_hours = sum(float(task["total_hours"]) for task in emergency_tasks)
    runtime_failure_hours = sum(float(failure["response_hours_per_day"]) * days for failure in runtime_failures)
    total_hours = baseline_hours + emergency_hours + runtime_failure_hours
    capacity_multiplier = float(scenario["labor_capacity_multiplier"])
    effective_population = max(population * capacity_multiplier, 0.001)
    weeks = days / 7
    hours_per_resident_per_week = total_hours / weeks / effective_population
    status = "pass"
    if hours_per_resident_per_week > 12:
        status = "fail"
    elif hours_per_resident_per_week > 8:
        status = "warn"
    return {
        "population": population,
        "labor_capacity_multiplier": capacity_multiplier,
        "effective_population": round(effective_population, 3),
        "baseline_maintenance_hours": round(baseline_hours, 3),
        "emergency_hours": round(emergency_hours, 3),
        "runtime_failure_response_hours": round(runtime_failure_hours, 3),
        "total_hours": round(total_hours, 3),
        "hours_per_resident_per_week": round(hours_per_resident_per_week, 3),
        "status": status,
        "emergency_tasks": emergency_tasks,
    }


def _scenario_triggered_risks(
    compiled_plan: dict[str, Any],
    baseline_triggered: list[dict[str, Any]],
    scenario: dict[str, Any],
) -> list[dict[str, Any]]:
    risk_modes = set(scenario["triggered_risk_modes"])
    triggered = {
        (risk["pattern_id"], risk["mode"]): dict(risk)
        for risk in baseline_triggered
    }
    for risk in compiled_plan.get("risk_register", []):
        if risk["mode"] in risk_modes:
            triggered[(risk["pattern_id"], risk["mode"])] = {
                "pattern_id": risk["pattern_id"],
                "mode": risk["mode"],
                "severity": risk["severity"],
                "likelihood": risk["likelihood"],
                "reason": f"Triggered by scenario: {scenario['id']}.",
                "mitigation": risk["mitigation"],
            }
    return sorted(triggered.values(), key=lambda item: (item["pattern_id"], item["mode"]))


def _affected_resources(scenario: dict[str, Any], resource_balance: dict[str, dict[str, Any]]) -> list[str]:
    resources = set()
    for resource, multiplier in scenario["resource_multipliers"].items():
        if float(multiplier) != 1:
            resources.add(resource)
    for resource, delta in scenario["resource_deltas"].items():
        if float(delta) != 0:
            resources.add(resource)
    for resource, summary in resource_balance.items():
        if summary["status"] != "pass":
            resources.add(resource)
    return sorted(resources)


def _review_context(scenario: dict[str, Any], runtime_failures: list[dict[str, Any]]) -> dict[str, Any]:
    overrides = scenario.get("review_context_overrides", [])
    dependency_domains = {
        failure["unresolved_review_dependency"]
        for failure in runtime_failures
        if failure.get("unresolved_review_dependency")
    }
    override_domains = {override["domain"] for override in overrides}
    blocked = sorted(
        override["domain"]
        for override in overrides
        if override["effect"] in {"blocks_recovery", "requires_external_review"}
    )
    temporary = sorted(
        override["domain"]
        for override in overrides
        if override["effect"] == "allows_temporary_recovery"
    )
    events = [
        {
            "domain": override["domain"],
            "status": override["status"],
            "effect": override["effect"],
            "day": override["day"],
            "notes": override["notes"],
            "provisional": True,
        }
        for override in overrides
    ]
    return {
        "status": "impacted" if overrides else "not_modeled",
        "required_domains": sorted(dependency_domains | override_domains),
        "blocked_domains": blocked,
        "temporary_domains": temporary,
        "events": sorted(events, key=lambda item: (item["day"], item["domain"], item["status"])),
        "provisional": True,
    }


def _failure_timeline(
    resource_balance: dict[str, dict[str, Any]],
    emergency_labor: dict[str, Any],
    review_context: dict[str, Any],
    triggered_risks: list[dict[str, Any]],
    runtime_failures: list[dict[str, Any]],
    scenario: dict[str, Any],
) -> list[dict[str, Any]]:
    timeline: list[dict[str, Any]] = [
        {
            "day": 1,
            "event": "scenario_started",
            "severity": "info",
            "description": scenario["description"],
        }
    ]
    for task in scenario["emergency_tasks"]:
        timeline.append(
            {
                "day": task["day"],
                "event": f"emergency_task:{task['id']}",
                "severity": "warning",
                "description": task["description"],
            }
        )
    for resource, summary in resource_balance.items():
        if summary["status"] == "fail":
            timeline.append(
                {
                    "day": 1,
                    "event": f"resource_failure:{resource}",
                    "severity": "error",
                    "description": f"{resource} balance becomes negative under scenario assumptions.",
                }
            )
    if emergency_labor["status"] != "pass":
        timeline.append(
            {
                "day": 1,
                "event": "labor_overload",
                "severity": "error" if emergency_labor["status"] == "fail" else "warning",
                "description": "Emergency and maintenance work exceeds fair labor threshold.",
            }
        )
    for risk in triggered_risks:
        timeline.append(
            {
                "day": 1,
                "event": f"risk_triggered:{risk['mode']}",
                "severity": "error" if risk["severity"] == "catastrophic" else "warning",
                "description": risk["mitigation"],
            }
        )
    for failure in runtime_failures:
        timeline.append(
            {
                "day": failure["start_day"],
                "event": f"runtime_failure:{failure['mode']}",
                "severity": "error" if failure["severity"] == "catastrophic" else "warning",
                "description": f"{failure['pattern_id']} failure active; review dependency: {failure['unresolved_review_dependency']}.",
            }
        )
    for event in review_context.get("events", []):
        timeline.append(
            {
                "day": event["day"],
                "event": f"review_context:{event['domain']}",
                "severity": "error" if event["effect"] == "blocks_recovery" else "warning",
                "description": f"{event['status']} -> {event['effect']}: {event['notes']}",
            }
        )
    return sorted(timeline, key=lambda item: (item["day"], item["event"]))


def _survival_critical_gate_failures(
    resource_balance: dict[str, dict[str, Any]],
    emergency_labor: dict[str, Any],
) -> list[str]:
    failures: list[str] = []
    for resource, gate in SURVIVAL_RESOURCES.items():
        if resource_balance[resource]["status"] == "fail":
            failures.append(gate)
    if emergency_labor["status"] == "fail":
        failures.append("labor_gate")
    return failures


def _bottlenecks(
    resource_balance: dict[str, dict[str, Any]],
    emergency_labor: dict[str, Any],
    review_context: dict[str, Any],
    triggered_risks: list[dict[str, Any]],
    scenario: dict[str, Any],
) -> list[str]:
    bottlenecks: list[str] = []
    for resource, summary in resource_balance.items():
        if summary["status"] == "fail":
            bottlenecks.append(f"{scenario['id']} drives {resource} negative")
        elif summary["status"] == "warn":
            bottlenecks.append(f"{scenario['id']} leaves {resource} with no modeled buffer")
    if emergency_labor["status"] != "pass":
        bottlenecks.append(f"{scenario['id']} overloads available labor capacity")
    for domain in review_context.get("blocked_domains", []):
        bottlenecks.append(f"{scenario['id']} blocks recovery review for {domain}")
    if triggered_risks:
        bottlenecks.append(f"{len(triggered_risks)} risk mode(s) require explicit response planning")
    return bottlenecks


def _recommended_redesigns(
    resource_balance: dict[str, dict[str, Any]],
    emergency_labor: dict[str, Any],
    review_context: dict[str, Any],
    triggered_risks: list[dict[str, Any]],
    scenario: dict[str, Any],
) -> list[str]:
    recommendations: list[str] = []
    if resource_balance["water_liters"]["status"] != "pass":
        recommendations.append("Increase water redundancy, emergency storage, demand reduction, or backup supply.")
    if resource_balance["energy_kwh"]["status"] != "pass":
        recommendations.append("Add critical-load shedding, storage reserve, backup generation, or lower demand.")
    if resource_balance["food_servings"]["status"] != "pass":
        recommendations.append("Add crop diversity, preserved food reserve, nutrition planning, and procurement fallback.")
    if emergency_labor["status"] != "pass":
        recommendations.append("Add backup stewards, reduce scenario response workload, or define mutual-aid support.")
    if review_context.get("blocked_domains"):
        recommendations.append("Add scenario-specific review fallback, retest pathway, or mutual-aid reviewer before treating recovery as resolvable.")
    if triggered_risks:
        recommendations.append("Create scenario-specific standard operating procedures for triggered high-consequence risks.")
    if not recommendations:
        recommendations.append(f"Keep {scenario['id']} as a regression scenario while adding richer storage and seasonality models.")
    return recommendations


def _status(
    gate_failures: list[str],
    emergency_labor: dict[str, Any],
    review_context: dict[str, Any],
    triggered_risks: list[dict[str, Any]],
) -> str:
    if gate_failures:
        return "fail"
    if emergency_labor["status"] == "warn" or review_context.get("status") == "impacted" or triggered_risks:
        return "warn"
    return "pass"
