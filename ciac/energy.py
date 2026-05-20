from __future__ import annotations

from typing import Any


def evaluate_energy(compiled_plan: dict[str, Any], energy_plan: dict[str, Any]) -> dict[str, Any]:
    loads = energy_plan["loads"]
    targets = energy_plan["targets"]
    generation = _generation(energy_plan)
    total_load = sum(float(load["kwh_per_day"]) for load in loads)
    critical_load = sum(float(load["kwh_per_day"]) for load in loads if load["critical"])
    noncritical_load = total_load - critical_load
    reserve_factor = max(0.0, 1.0 - (float(targets["reserve_percent"]) / 100.0))
    usable_after_reserve = float(energy_plan["storage"]["battery_usable_kwh"]) * reserve_factor

    normal_balance = _normal_balance(generation, total_load, critical_load, noncritical_load, energy_plan["days"])
    autonomy = _critical_load_autonomy(usable_after_reserve, critical_load, targets)
    outage = _outage_survival(usable_after_reserve, critical_load, targets)
    shedding = _load_shedding_plan(energy_plan, generation)
    solar_reduction = _solar_reduction(energy_plan, total_load, critical_load, usable_after_reserve)
    refrigeration = _refrigeration_risk(loads, usable_after_reserve, targets)
    backup_gap = _backup_gap(energy_plan, outage, solar_reduction)
    maintenance = _maintenance_summary(energy_plan)
    warnings = _warnings(compiled_plan, energy_plan, normal_balance, autonomy, outage, solar_reduction, refrigeration, backup_gap, maintenance)
    bottlenecks = _bottlenecks(normal_balance, autonomy, outage, solar_reduction, refrigeration, backup_gap, maintenance)
    recommendations = _recommendations(normal_balance, autonomy, outage, solar_reduction, refrigeration, backup_gap, maintenance, warnings)
    status = _status(normal_balance, autonomy, outage, solar_reduction, refrigeration, maintenance, warnings)

    return {
        "kind": "EnergyReport",
        "id": f"{compiled_plan['id']}_{energy_plan['id']}_energy",
        "compiled_plan": compiled_plan["id"],
        "energy_plan": energy_plan["id"],
        "generated_by": "ciac.energy.v0",
        "days": energy_plan["days"],
        "provisional": True,
        "status": status,
        "normal_balance": normal_balance,
        "critical_load_autonomy": autonomy,
        "outage_survival": outage,
        "load_shedding_plan": shedding,
        "solar_reduction": solar_reduction,
        "refrigeration_risk": refrigeration,
        "backup_energy_gap": backup_gap,
        "maintenance": maintenance,
        "energy_safety_warnings": warnings,
        "redesign_recommendations": recommendations,
        "bottlenecks": bottlenecks,
        "unknowns": [
            "Energy values are provisional and not electrical design, engineering review, or code compliance.",
            "No hourly solar curve, battery degradation, inverter limits, surge loads, wiring design, or thermal model exists yet.",
            "Refrigeration risk is estimated from energy autonomy only, not food temperature dynamics.",
            energy_plan["notes"],
        ],
    }


def _generation(energy_plan: dict[str, Any]) -> float:
    return float(energy_plan["generation"]["solar_kwh_per_day"]) + float(energy_plan["generation"]["other_kwh_per_day"])


def _normal_balance(
    generation: float,
    total_load: float,
    critical_load: float,
    noncritical_load: float,
    days: int,
) -> dict[str, Any]:
    net = generation - total_load
    status = "pass" if net >= 0 else "fail"
    return {
        "generation_kwh_per_day": round(generation, 3),
        "total_load_kwh_per_day": round(total_load, 3),
        "critical_load_kwh_per_day": round(critical_load, 3),
        "noncritical_load_kwh_per_day": round(noncritical_load, 3),
        "net_kwh_per_day": round(net, 3),
        "ending_balance_kwh": round(net * days, 3),
        "status": status,
    }


def _critical_load_autonomy(usable_battery_kwh: float, critical_load: float, targets: dict[str, Any]) -> dict[str, Any]:
    hours = _hours_of_autonomy(usable_battery_kwh, critical_load)
    status = "pass" if hours >= float(targets["critical_autonomy_target_hours"]) else "warn"
    return {
        "usable_battery_after_reserve_kwh": round(usable_battery_kwh, 3),
        "critical_load_kwh_per_day": round(critical_load, 3),
        "autonomy_hours": round(hours, 3),
        "target_hours": targets["critical_autonomy_target_hours"],
        "status": status,
    }


def _outage_survival(usable_battery_kwh: float, critical_load: float, targets: dict[str, Any]) -> dict[str, Any]:
    hours = _hours_of_autonomy(usable_battery_kwh, critical_load)
    target = float(targets["outage_target_hours"])
    gap = max(0.0, target - hours)
    status = "pass" if gap == 0 else "fail"
    return {
        "critical_load_only_hours": round(hours, 3),
        "target_hours": target,
        "gap_hours": round(gap, 3),
        "status": status,
    }


def _load_shedding_plan(energy_plan: dict[str, Any], generation: float) -> list[dict[str, Any]]:
    loads_by_id = {load["id"]: load for load in energy_plan["loads"]}
    active_load = sum(float(load["kwh_per_day"]) for load in energy_plan["loads"])
    plan: list[dict[str, Any]] = []
    for load_id in energy_plan["load_shedding_priority"]:
        load = loads_by_id[load_id]
        if active_load <= generation:
            break
        active_load -= float(load["kwh_per_day"])
        plan.append(
            {
                "shed_load_id": load_id,
                "name": load["name"],
                "kwh_per_day_removed": load["kwh_per_day"],
                "remaining_load_kwh_per_day": round(active_load, 3),
                "critical": load["critical"],
            }
        )
    return plan


def _solar_reduction(
    energy_plan: dict[str, Any],
    total_load: float,
    critical_load: float,
    usable_battery_kwh: float,
) -> dict[str, Any]:
    scenario = energy_plan["solar_reduction_scenario"]
    reduced_generation = (
        float(energy_plan["generation"]["solar_kwh_per_day"]) * float(scenario["solar_multiplier"])
        + float(energy_plan["generation"]["other_kwh_per_day"])
    )
    total_net = reduced_generation - total_load
    critical_net = reduced_generation - critical_load
    days = int(scenario["days"])
    critical_gap = max(0.0, -critical_net * days)
    status = "pass"
    if critical_gap > usable_battery_kwh:
        status = "fail"
    elif total_net < 0:
        status = "warn"
    return {
        "name": scenario["name"],
        "days": days,
        "generation_kwh_per_day": round(reduced_generation, 3),
        "total_net_kwh_per_day": round(total_net, 3),
        "critical_net_kwh_per_day": round(critical_net, 3),
        "critical_gap_kwh": round(critical_gap, 3),
        "status": status,
    }


def _refrigeration_risk(loads: list[dict[str, Any]], usable_battery_kwh: float, targets: dict[str, Any]) -> dict[str, Any]:
    refrigeration_load = sum(float(load["kwh_per_day"]) for load in loads if load["refrigeration"])
    hours = _hours_of_autonomy(usable_battery_kwh, refrigeration_load)
    target = min(float(targets["outage_target_hours"]), 48.0)
    status = "pass" if hours >= target else "warn"
    return {
        "refrigeration_load_kwh_per_day": round(refrigeration_load, 3),
        "battery_only_hours": round(hours, 3),
        "target_hours": target,
        "status": status,
    }


def _backup_gap(energy_plan: dict[str, Any], outage: dict[str, Any], solar_reduction: dict[str, Any]) -> dict[str, Any]:
    backup = energy_plan["backup"]
    outage_gap_kwh = max(0.0, float(outage["gap_hours"]) / 24.0 * _critical_load_per_day(energy_plan))
    solar_gap_kwh = max(0.0, float(solar_reduction["critical_gap_kwh"]) - float(energy_plan["storage"]["battery_usable_kwh"]))
    available_kwh = float(backup["kwh_per_day"]) * max(1.0, float(energy_plan["solar_reduction_scenario"]["days"]))
    required = max(outage_gap_kwh, solar_gap_kwh)
    remaining_gap = max(0.0, required - available_kwh)
    status = "pass" if remaining_gap == 0 else ("warn" if backup["available"] else "fail")
    return {
        "backup_available": backup["available"],
        "backup_kwh_per_day": backup["kwh_per_day"],
        "hours_to_activate": backup["hours_to_activate"],
        "required_backup_kwh": round(required, 3),
        "available_backup_kwh_for_solar_reduction_window": round(available_kwh, 3),
        "remaining_gap_kwh": round(remaining_gap, 3),
        "status": status,
        "notes": backup["notes"],
    }


def _maintenance_summary(energy_plan: dict[str, Any]) -> dict[str, Any]:
    maintenance = energy_plan["maintenance"]
    status = "pass"
    if float(maintenance["test_cadence_days"]) > 30 or not maintenance["requires_qualified_review"]:
        status = "warn"
    return {
        "test_cadence_days": maintenance["test_cadence_days"],
        "responsible_role": maintenance["responsible_role"],
        "requires_qualified_review": maintenance["requires_qualified_review"],
        "status": status,
    }


def _warnings(
    compiled_plan: dict[str, Any],
    energy_plan: dict[str, Any],
    normal_balance: dict[str, Any],
    autonomy: dict[str, Any],
    outage: dict[str, Any],
    solar_reduction: dict[str, Any],
    refrigeration: dict[str, Any],
    backup_gap: dict[str, Any],
    maintenance: dict[str, Any],
) -> list[str]:
    warnings: list[str] = []
    if "solar_shed" not in compiled_plan.get("selected_patterns", []):
        warnings.append("Compiled plan does not include solar_shed; solar energy assumptions may be unsupported.")
    if normal_balance["status"] != "pass":
        warnings.append("Normal energy balance does not pass.")
    if autonomy["status"] != "pass":
        warnings.append("Critical-load battery autonomy is below target.")
    if outage["status"] != "pass":
        warnings.append("Outage survival target is not met.")
    if solar_reduction["status"] != "pass":
        warnings.append("Solar reduction scenario exposes an energy shortfall.")
    if refrigeration["status"] != "pass":
        warnings.append("Refrigeration autonomy is below target.")
    if backup_gap["status"] != "pass":
        warnings.append("Backup energy is unavailable or insufficient.")
    if maintenance["status"] != "pass":
        warnings.append("Energy maintenance cadence or qualified review is weaker than the current conservative default.")
    if any(step["critical"] for step in _load_shedding_plan(energy_plan, _generation(energy_plan))):
        warnings.append("Load shedding plan removes at least one critical load under normal assumptions.")
    return warnings


def _bottlenecks(
    normal_balance: dict[str, Any],
    autonomy: dict[str, Any],
    outage: dict[str, Any],
    solar_reduction: dict[str, Any],
    refrigeration: dict[str, Any],
    backup_gap: dict[str, Any],
    maintenance: dict[str, Any],
) -> list[str]:
    bottlenecks: list[str] = []
    if normal_balance["status"] != "pass":
        bottlenecks.append("normal daily generation is below modeled load")
    if autonomy["status"] != "pass":
        bottlenecks.append("critical-load autonomy is below target")
    if outage["status"] != "pass":
        bottlenecks.append("battery storage does not meet outage target")
    if solar_reduction["status"] != "pass":
        bottlenecks.append("solar reduction scenario is not resilient")
    if refrigeration["status"] != "pass":
        bottlenecks.append("refrigeration autonomy is below target")
    if backup_gap["status"] != "pass":
        bottlenecks.append("backup energy gap remains unresolved")
    if maintenance["status"] != "pass":
        bottlenecks.append("energy maintenance protocol is incomplete")
    return bottlenecks


def _recommendations(
    normal_balance: dict[str, Any],
    autonomy: dict[str, Any],
    outage: dict[str, Any],
    solar_reduction: dict[str, Any],
    refrigeration: dict[str, Any],
    backup_gap: dict[str, Any],
    maintenance: dict[str, Any],
    warnings: list[str],
) -> list[str]:
    recommendations: list[str] = []
    if normal_balance["status"] != "pass":
        recommendations.append("Increase generation, reduce noncritical loads, or revise load estimates before promotion.")
    if autonomy["status"] != "pass" or outage["status"] != "pass":
        recommendations.append("Increase usable battery storage or reduce critical loads to meet outage autonomy targets.")
    if solar_reduction["status"] != "pass":
        recommendations.append("Add cloudy-weather reserve, backup generation, mutual-aid charging, or deeper load shedding.")
    if refrigeration["status"] != "pass":
        recommendations.append("Add refrigeration reserve, thermal storage, preservation fallback, or priority backup power.")
    if backup_gap["status"] != "pass":
        recommendations.append("Secure backup energy or mutual-aid capacity for the modeled emergency window.")
    if maintenance["status"] != "pass":
        recommendations.append("Keep energy inspections at least monthly and require qualified review for electrical safety.")
    if any("critical load" in warning.lower() for warning in warnings):
        recommendations.append("Revise load shedding order so critical systems are protected until explicit emergency thresholds.")
    if not recommendations:
        recommendations.append("Keep energy plan as a regression case while adding hourly solar, battery degradation, and inverter limits.")
    return recommendations


def _status(
    normal_balance: dict[str, Any],
    autonomy: dict[str, Any],
    outage: dict[str, Any],
    solar_reduction: dict[str, Any],
    refrigeration: dict[str, Any],
    maintenance: dict[str, Any],
    warnings: list[str],
) -> str:
    if normal_balance["status"] == "fail" or outage["status"] == "fail" or solar_reduction["status"] == "fail":
        return "fail"
    if autonomy["status"] == "warn" or refrigeration["status"] == "warn" or maintenance["status"] == "warn" or warnings:
        return "warn"
    return "pass"


def _hours_of_autonomy(usable_battery_kwh: float, load_kwh_per_day: float) -> float:
    if load_kwh_per_day <= 0:
        return 0.0
    return usable_battery_kwh / load_kwh_per_day * 24.0


def _critical_load_per_day(energy_plan: dict[str, Any]) -> float:
    return sum(float(load["kwh_per_day"]) for load in energy_plan["loads"] if load["critical"])

