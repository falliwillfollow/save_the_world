from __future__ import annotations

from typing import Any


def evaluate_nutrition(compiled_plan: dict[str, Any], food_plan: dict[str, Any]) -> dict[str, Any]:
    population = int(food_plan["population"])
    days = int(food_plan["days"])
    targets = food_plan["targets"]
    foods = food_plan["foods"]
    total_calories = sum(float(food["calories_per_day"]) for food in foods)
    total_protein = sum(float(food["protein_grams_per_day"]) for food in foods)
    local_calories = sum(float(food["calories_per_day"]) for food in foods if food["source"] == "local")
    stored_calorie_days = _stored_calorie_days(foods, targets, population)

    calories_per_person = total_calories / population
    protein_per_person = total_protein / population
    local_percent = (local_calories / total_calories * 100) if total_calories else 0.0
    calorie_gap = max(0.0, (targets["calories_per_person_per_day"] * population) - total_calories)
    protein_gap = max(0.0, (targets["protein_grams_per_person_per_day"] * population) - total_protein)
    shortage_timeline = _shortage_timeline(food_plan, calorie_gap, protein_gap, stored_calorie_days)
    fallback_needs = _fallback_procurement_needs(food_plan, calorie_gap, protein_gap, stored_calorie_days)
    warnings = _dietary_risk_warnings(compiled_plan, food_plan, calories_per_person, protein_per_person, local_percent, stored_calorie_days)
    bottlenecks = _bottlenecks(calorie_gap, protein_gap, local_percent, stored_calorie_days, targets, warnings)
    status = _status(calorie_gap, protein_gap, stored_calorie_days, targets, warnings)

    return {
        "kind": "NutritionReport",
        "id": f"{compiled_plan['id']}_{food_plan['id']}_nutrition",
        "compiled_plan": compiled_plan["id"],
        "food_plan": food_plan["id"],
        "generated_by": "ciac.nutrition.v0",
        "days": days,
        "population": population,
        "provisional": True,
        "status": status,
        "nutrition": {
            "calories_per_day": round(total_calories, 3),
            "calories_per_person_per_day": round(calories_per_person, 3),
            "calorie_target_per_person_per_day": targets["calories_per_person_per_day"],
            "calorie_gap_per_day": round(calorie_gap, 3),
            "protein_grams_per_day": round(total_protein, 3),
            "protein_grams_per_person_per_day": round(protein_per_person, 3),
            "protein_target_grams_per_person_per_day": targets["protein_grams_per_person_per_day"],
            "protein_gap_grams_per_day": round(protein_gap, 3),
        },
        "local_food": {
            "local_calories_per_day": round(local_calories, 3),
            "local_food_percent": round(local_percent, 3),
            "target_percent": targets["local_food_percent_target"],
            "status": "pass" if local_percent >= targets["local_food_percent_target"] else "warn",
        },
        "storage": {
            "stored_calorie_days": round(stored_calorie_days, 3),
            "target_days": targets["storage_days_target"],
            "status": "pass" if stored_calorie_days >= targets["storage_days_target"] else "warn",
        },
        "shortage_timeline": shortage_timeline,
        "fallback_procurement_needs": fallback_needs,
        "dietary_risk_warnings": warnings,
        "bottlenecks": bottlenecks,
        "unknowns": [
            "Food plan values are provisional and not dietician-reviewed.",
            "No micronutrient, allergy, cultural diet, food safety, spoilage, or crop calendar model exists yet.",
            "Local food production is annualized and does not include weather, pests, labor peaks, or storage losses.",
            food_plan["notes"],
        ],
    }


def _stored_calorie_days(foods: list[dict[str, Any]], targets: dict[str, Any], population: int) -> float:
    target_daily_calories = float(targets["calories_per_person_per_day"]) * population
    stored_calories = 0.0
    for food in foods:
        stored_days = min(float(food["stored_days"]), float(food["storage_life_days"]))
        stored_calories += float(food["calories_per_day"]) * stored_days
    if target_daily_calories <= 0:
        return 0.0
    return stored_calories / target_daily_calories


def _shortage_timeline(
    food_plan: dict[str, Any],
    calorie_gap: float,
    protein_gap: float,
    stored_calorie_days: float,
) -> list[dict[str, Any]]:
    timeline: list[dict[str, Any]] = []
    if calorie_gap > 0:
        timeline.append(
            {
                "day": 1,
                "event": "calorie_shortage",
                "severity": "error",
                "description": f"Daily plan is short by {round(calorie_gap, 3)} calories.",
            }
        )
    if protein_gap > 0:
        timeline.append(
            {
                "day": 1,
                "event": "protein_shortage",
                "severity": "error",
                "description": f"Daily plan is short by {round(protein_gap, 3)} grams of protein.",
            }
        )
    storage_target = float(food_plan["targets"]["storage_days_target"])
    if stored_calorie_days < storage_target:
        timeline.append(
            {
                "day": max(1, int(stored_calorie_days) + 1),
                "event": "storage_target_missed",
                "severity": "warning",
                "description": f"Stored calories cover {round(stored_calorie_days, 1)} target days, below {storage_target}.",
            }
        )
    return timeline


def _fallback_procurement_needs(
    food_plan: dict[str, Any],
    calorie_gap: float,
    protein_gap: float,
    stored_calorie_days: float,
) -> list[str]:
    fallback = food_plan["fallback_procurement"]
    needs: list[str] = []
    if calorie_gap > 0:
        if fallback["available"] and fallback["calories_per_day"] >= calorie_gap:
            needs.append("Fallback procurement can cover the modeled calorie gap if lead time is acceptable.")
        else:
            needs.append("Secure fallback calories before promotion.")
    if protein_gap > 0:
        if fallback["available"] and fallback["protein_grams_per_day"] >= protein_gap:
            needs.append("Fallback procurement can cover the modeled protein gap if lead time is acceptable.")
        else:
            needs.append("Secure fallback protein before promotion.")
    if stored_calorie_days < food_plan["targets"]["storage_days_target"]:
        needs.append("Increase stored staples or preservation capacity to meet storage target.")
    if fallback["available"] and fallback["lead_time_days"] > stored_calorie_days:
        needs.append("Fallback lead time exceeds stored calorie buffer.")
    return needs


def _dietary_risk_warnings(
    compiled_plan: dict[str, Any],
    food_plan: dict[str, Any],
    calories_per_person: float,
    protein_per_person: float,
    local_percent: float,
    stored_calorie_days: float,
) -> list[str]:
    targets = food_plan["targets"]
    warnings: list[str] = []
    if "greenhouse" not in compiled_plan.get("selected_patterns", []):
        warnings.append("Compiled plan does not include greenhouse; local fresh-food assumptions may be unsupported.")
    if calories_per_person < targets["calories_per_person_per_day"]:
        warnings.append("Calories per person are below target.")
    if protein_per_person < targets["protein_grams_per_person_per_day"]:
        warnings.append("Protein per person is below target.")
    if local_percent < targets["local_food_percent_target"]:
        warnings.append("Local food percentage is below target.")
    if stored_calorie_days < targets["storage_days_target"]:
        warnings.append("Stored food buffer is below target.")
    if any(food["water_sensitivity"] == "high" and food["source"] == "local" for food in food_plan["foods"]):
        warnings.append("At least one local food source is highly water-sensitive.")
    if any(food["source"] == "external" for food in food_plan["foods"]):
        warnings.append("Diet still depends on external procurement.")
    return warnings


def _bottlenecks(
    calorie_gap: float,
    protein_gap: float,
    local_percent: float,
    stored_calorie_days: float,
    targets: dict[str, Any],
    warnings: list[str],
) -> list[str]:
    bottlenecks: list[str] = []
    if calorie_gap > 0:
        bottlenecks.append("daily calories are below target")
    if protein_gap > 0:
        bottlenecks.append("daily protein is below target")
    if local_percent < targets["local_food_percent_target"]:
        bottlenecks.append("local food share is below target")
    if stored_calorie_days < targets["storage_days_target"]:
        bottlenecks.append("stored calorie buffer is below target")
    if "Diet still depends on external procurement." in warnings:
        bottlenecks.append("external procurement remains survival-critical")
    return bottlenecks


def _status(
    calorie_gap: float,
    protein_gap: float,
    stored_calorie_days: float,
    targets: dict[str, Any],
    warnings: list[str],
) -> str:
    if calorie_gap > 0 or protein_gap > 0:
        return "fail"
    if stored_calorie_days < targets["storage_days_target"] or warnings:
        return "warn"
    return "pass"

