from __future__ import annotations

from typing import Any


def evaluate_water(compiled_plan: dict[str, Any], water_plan: dict[str, Any]) -> dict[str, Any]:
    population = int(water_plan["population"])
    demand = _demand(water_plan, population)
    normal_yield = _source_yield(water_plan["sources"], mode="normal", drought_assumptions=water_plan["drought_assumptions"])
    drought_yield = _source_yield(water_plan["sources"], mode="drought", drought_assumptions=water_plan["drought_assumptions"])
    reduced_demand = _reduced_demand(demand, water_plan["drought_assumptions"]["demand_reduction_percent"])
    storage = _storage(water_plan, demand)
    normal_balance = _balance(normal_yield, demand, water_plan["days"])
    drought_balance = _balance(drought_yield, reduced_demand, int(water_plan["targets"]["drought_days"]))
    contamination = _contamination_response(water_plan, demand)
    testing = _testing_summary(water_plan)
    reduction_needed = _demand_reduction_needed(drought_yield, demand)
    warnings = _warnings(compiled_plan, water_plan, storage, normal_balance, drought_balance, contamination, testing)
    bottlenecks = _bottlenecks(storage, normal_balance, drought_balance, contamination, testing)
    recommendations = _recommendations(storage, normal_balance, drought_balance, contamination, reduction_needed, warnings)
    status = _status(normal_balance, drought_balance, contamination, storage, water_plan["targets"], warnings)

    return {
        "kind": "WaterReport",
        "id": f"{compiled_plan['id']}_{water_plan['id']}_water",
        "compiled_plan": compiled_plan["id"],
        "water_plan": water_plan["id"],
        "generated_by": "ciac.water.v0",
        "days": water_plan["days"],
        "population": population,
        "provisional": True,
        "status": status,
        "storage": storage,
        "normal_balance": normal_balance,
        "drought_balance": drought_balance,
        "contamination_response": contamination,
        "testing": testing,
        "demand_reduction_needed": reduction_needed,
        "water_safety_warnings": warnings,
        "redesign_recommendations": recommendations,
        "bottlenecks": bottlenecks,
        "unknowns": [
            "Water values are provisional and not hydrology, engineering, health, or legal advice.",
            "No aquifer recharge, rainfall sequence, seasonal storage drawdown, water quality chemistry, or pathogen model exists yet.",
            "Potable/nonpotable separation is modeled as planning logic only, not as plumbing design.",
            water_plan["notes"],
        ],
    }


def _demand(water_plan: dict[str, Any], population: int) -> dict[str, float]:
    potable = float(water_plan["demand"]["potable_liters_per_person_per_day"]) * population
    nonpotable = float(water_plan["demand"]["nonpotable_liters_per_person_per_day"]) * population
    return {
        "potable_liters_per_day": potable,
        "nonpotable_liters_per_day": nonpotable,
        "total_liters_per_day": potable + nonpotable,
    }


def _source_yield(
    sources: list[dict[str, Any]],
    mode: str,
    drought_assumptions: dict[str, Any],
) -> dict[str, float]:
    potable = 0.0
    nonpotable = 0.0
    total = 0.0
    for source in sources:
        yield_liters = float(source["normal_yield_liters_per_day"])
        if mode == "drought":
            if source["kind"] == "well":
                yield_liters *= float(drought_assumptions["well_yield_multiplier"])
            elif source["kind"] == "rainwater":
                yield_liters *= float(drought_assumptions["rainwater_yield_multiplier"])
            else:
                yield_liters *= float(source["drought_yield_multiplier"])
        if source["potable"]:
            potable += yield_liters
        else:
            nonpotable += yield_liters
        total += yield_liters
    return {
        "potable_liters_per_day": potable,
        "nonpotable_liters_per_day": nonpotable,
        "total_liters_per_day": total,
    }


def _reduced_demand(demand: dict[str, float], reduction_percent: float) -> dict[str, float]:
    factor = max(0.0, 1.0 - (float(reduction_percent) / 100.0))
    return {
        "potable_liters_per_day": demand["potable_liters_per_day"] * factor,
        "nonpotable_liters_per_day": demand["nonpotable_liters_per_day"] * factor,
        "total_liters_per_day": demand["total_liters_per_day"] * factor,
    }


def _storage(water_plan: dict[str, Any], demand: dict[str, float]) -> dict[str, Any]:
    potable_storage = float(water_plan["storage"]["potable_liters"])
    nonpotable_storage = float(water_plan["storage"]["nonpotable_liters"])
    potable_days = _safe_div(potable_storage, demand["potable_liters_per_day"])
    nonpotable_days = _safe_div(nonpotable_storage, demand["nonpotable_liters_per_day"])
    total_days = _safe_div(potable_storage + nonpotable_storage, demand["total_liters_per_day"])
    return {
        "potable_liters": potable_storage,
        "nonpotable_liters": nonpotable_storage,
        "potable_days": round(potable_days, 3),
        "nonpotable_days": round(nonpotable_days, 3),
        "total_storage_days": round(total_days, 3),
    }


def _balance(yield_liters: dict[str, float], demand: dict[str, float], days: int) -> dict[str, Any]:
    potable_net = yield_liters["potable_liters_per_day"] - demand["potable_liters_per_day"]
    nonpotable_net = yield_liters["nonpotable_liters_per_day"] - demand["nonpotable_liters_per_day"]
    total_net = yield_liters["total_liters_per_day"] - demand["total_liters_per_day"]
    status = "pass"
    if potable_net < 0 or total_net < 0:
        status = "fail"
    return {
        "days": days,
        "yield_liters_per_day": {key: round(value, 3) for key, value in yield_liters.items()},
        "demand_liters_per_day": {key: round(value, 3) for key, value in demand.items()},
        "net_liters_per_day": {
            "potable": round(potable_net, 3),
            "nonpotable": round(nonpotable_net, 3),
            "total": round(total_net, 3),
        },
        "ending_balance_liters": round(total_net * days, 3),
        "status": status,
    }


def _contamination_response(water_plan: dict[str, Any], demand: dict[str, float]) -> dict[str, Any]:
    response = water_plan["contamination_response"]
    sources_by_id = {source["id"]: source for source in water_plan["sources"]}
    backup_yield = 0.0
    missing_sources: list[str] = []
    for source_id in response["backup_sources"]:
        source = sources_by_id.get(source_id)
        if source is None:
            missing_sources.append(source_id)
        elif source["contamination_available"]:
            backup_yield += float(source["normal_yield_liters_per_day"])
    potable_storage = float(water_plan["storage"]["potable_liters"])
    fallback_days = _safe_div(potable_storage, demand["potable_liters_per_day"])
    backup_total_net = backup_yield - demand["total_liters_per_day"]
    status = "pass"
    if missing_sources or not response["isolate_primary_source"] or not response["boil_or_treat_notice"]:
        status = "fail"
    elif fallback_days < water_plan["targets"]["contamination_fallback_days"] or backup_total_net < 0:
        status = "warn"
    return {
        "isolate_primary_source": response["isolate_primary_source"],
        "backup_sources": response["backup_sources"],
        "missing_backup_sources": missing_sources,
        "backup_yield_liters_per_day": round(backup_yield, 3),
        "potable_storage_fallback_days": round(fallback_days, 3),
        "backup_total_net_liters_per_day": round(backup_total_net, 3),
        "boil_or_treat_notice": response["boil_or_treat_notice"],
        "minimum_retest_count": response["minimum_retest_count"],
        "status": status,
    }


def _testing_summary(water_plan: dict[str, Any]) -> dict[str, Any]:
    testing = water_plan["testing"]
    cadence = float(testing["cadence_days"])
    status = "pass"
    if cadence > 30:
        status = "warn"
    if not testing["requires_lab_confirmation"]:
        status = "warn"
    return {
        "cadence_days": cadence,
        "responsible_role": testing["responsible_role"],
        "requires_lab_confirmation": testing["requires_lab_confirmation"],
        "status": status,
    }


def _demand_reduction_needed(drought_yield: dict[str, float], demand: dict[str, float]) -> dict[str, Any]:
    if demand["total_liters_per_day"] <= 0:
        required_percent = 0.0
    else:
        required_percent = max(0.0, (1.0 - (drought_yield["total_liters_per_day"] / demand["total_liters_per_day"])) * 100.0)
    potable_required = 0.0
    if demand["potable_liters_per_day"] > 0:
        potable_required = max(0.0, (1.0 - (drought_yield["potable_liters_per_day"] / demand["potable_liters_per_day"])) * 100.0)
    return {
        "total_percent_needed_for_drought_balance": round(required_percent, 3),
        "potable_percent_needed_for_drought_balance": round(potable_required, 3),
    }


def _warnings(
    compiled_plan: dict[str, Any],
    water_plan: dict[str, Any],
    storage: dict[str, Any],
    normal_balance: dict[str, Any],
    drought_balance: dict[str, Any],
    contamination: dict[str, Any],
    testing: dict[str, Any],
) -> list[str]:
    warnings: list[str] = []
    if "well_house" not in compiled_plan.get("selected_patterns", []):
        warnings.append("Compiled plan does not include well_house; well source assumptions may be unsupported.")
    if "rainwater_capture" not in compiled_plan.get("selected_patterns", []):
        warnings.append("Compiled plan does not include rainwater_capture; backup water assumptions may be unsupported.")
    if storage["total_storage_days"] < water_plan["targets"]["emergency_reserve_days"]:
        warnings.append("Total water storage is below emergency reserve target.")
    if normal_balance["status"] != "pass":
        warnings.append("Normal water balance does not pass.")
    if drought_balance["status"] != "pass":
        warnings.append("Drought water balance does not pass.")
    if contamination["status"] != "pass":
        warnings.append("Contamination fallback is incomplete or too short.")
    if testing["status"] != "pass":
        warnings.append("Water testing cadence or lab confirmation is weaker than the current conservative default.")
    if not water_plan["treatment_methods"]:
        warnings.append("No water treatment method is declared.")
    return warnings


def _bottlenecks(
    storage: dict[str, Any],
    normal_balance: dict[str, Any],
    drought_balance: dict[str, Any],
    contamination: dict[str, Any],
    testing: dict[str, Any],
) -> list[str]:
    bottlenecks: list[str] = []
    if normal_balance["status"] != "pass":
        bottlenecks.append("normal water balance is insufficient")
    if drought_balance["status"] != "pass":
        bottlenecks.append("drought water balance is insufficient")
    if contamination["status"] != "pass":
        bottlenecks.append("contamination fallback window is insufficient")
    if testing["status"] != "pass":
        bottlenecks.append("water testing protocol is incomplete")
    if storage["potable_days"] < 7:
        bottlenecks.append("potable storage is below seven days")
    return bottlenecks


def _recommendations(
    storage: dict[str, Any],
    normal_balance: dict[str, Any],
    drought_balance: dict[str, Any],
    contamination: dict[str, Any],
    reduction_needed: dict[str, Any],
    warnings: list[str],
) -> list[str]:
    recommendations: list[str] = []
    if normal_balance["status"] != "pass":
        recommendations.append("Increase normal source yield, reduce demand, or add storage before promotion.")
    if drought_balance["status"] != "pass":
        recommendations.append(
            f"Drought balance needs about {reduction_needed['total_percent_needed_for_drought_balance']}% total demand reduction or equivalent backup supply."
        )
    if contamination["status"] != "pass":
        recommendations.append("Add potable backup storage, verified backup source, and retesting workflow for contamination events.")
    if storage["potable_days"] < 7:
        recommendations.append("Increase potable storage to at least seven days before treating the plan as resilient.")
    if any("testing" in warning.lower() for warning in warnings):
        recommendations.append("Keep water testing at least monthly with lab confirmation until local rules specify otherwise.")
    if not recommendations:
        recommendations.append("Keep water plan as a regression case while adding seasonal rainfall and storage drawdown modeling.")
    return recommendations


def _status(
    normal_balance: dict[str, Any],
    drought_balance: dict[str, Any],
    contamination: dict[str, Any],
    storage: dict[str, Any],
    targets: dict[str, Any],
    warnings: list[str],
) -> str:
    if normal_balance["status"] == "fail" or contamination["status"] == "fail":
        return "fail"
    if drought_balance["status"] == "fail":
        return "fail"
    if storage["total_storage_days"] < targets["emergency_reserve_days"] or warnings:
        return "warn"
    return "pass"


def _safe_div(numerator: float, denominator: float) -> float:
    if denominator <= 0:
        return 0.0
    return numerator / denominator
