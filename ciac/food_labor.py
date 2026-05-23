from __future__ import annotations

import math
from typing import Any


TOTAL_LABOR_REVIEW_THRESHOLD = 40.0


def generate_food_labor_report(
    module_registry: dict[str, Any],
    patterns: dict[str, dict[str, Any]] | list[dict[str, Any]],
    slot_id: str = "food_production",
    extra_people: list[int] | None = None,
) -> dict[str, Any]:
    pattern_by_id = patterns if isinstance(patterns, dict) else {pattern.get("id", ""): pattern for pattern in patterns}
    slot = _slot(module_registry, slot_id)
    related_ids = [*slot.get("default_patterns", []), *slot.get("accepted_patterns", [])]
    related_patterns = [pattern_by_id[pattern_id] for pattern_id in related_ids if pattern_id in pattern_by_id]
    modeled_patterns = [pattern for pattern in related_patterns if pattern.get("labor_model")]
    unmodeled_patterns = [pattern for pattern in related_patterns if not pattern.get("labor_model")]
    primary = modeled_patterns[0] if modeled_patterns else None

    if primary is None:
        return _missing_model_report(module_registry, slot_id, related_ids)

    labor_model = _combined_labor_model(modeled_patterns)
    categories = _category_results(labor_model)
    base_hours = sum(category["hours_per_week"] for category in categories)
    metric_hours = sum(float(pattern.get("metrics", {}).get("recurring_labor_hours_per_week", 0) or 0) for pattern in modeled_patterns)
    target_population = int(labor_model["target_population"])
    thresholds = labor_model["thresholds"]
    scaling_targets = _scaling_targets(module_registry, target_population, extra_people)
    scaling_results = [_scale_result(labor_model, target) for target in scaling_targets]
    hotspots = _hotspots(primary, categories, base_hours, metric_hours, target_population, thresholds, scaling_results)
    status = _status(hotspots)

    return {
        "kind": "FoodLaborReport",
        "id": f"{module_registry.get('id', 'module_registry')}_{slot_id}_food_labor",
        "generated_by": "ciac.food_labor.v0",
        "provisional": True,
        "status": status,
        "module_registry": module_registry.get("id", ""),
        "slot": slot_id,
        "primary_pattern": primary["id"],
        "modeled_patterns": [pattern.get("id", "") for pattern in modeled_patterns],
        "related_patterns": [pattern.get("id", "") for pattern in related_patterns],
        "unmodeled_patterns": [pattern.get("id", "") for pattern in unmodeled_patterns],
        "summary": {
            "target_population": target_population,
            "base_hours_per_week": round(base_hours, 3),
            "metrics_recurring_labor_hours_per_week": round(metric_hours, 3),
            "hours_per_resident_per_week": round(base_hours / target_population, 3),
            "linear_labor_share": round(_linear_share(categories), 3),
            "single_largest_category_hours": round(max(category["hours_per_week"] for category in categories), 3),
            "replication_strategy": labor_model["replication"]["above_max_strategy"],
            "provisional": True,
        },
        "category_results": categories,
        "scaling_results": scaling_results,
        "hotspots": hotspots,
        "recommendations": _recommendations(hotspots),
        "unknowns": [
            "Food labor is modeled from authored category estimates, not measured resident time-use data.",
            "Nutrition, crop calendar, food safety, procurement volatility, and resident preference models remain provisional.",
            "The 5-household demo should use small seed patterns; the hybrid food commons is intended for village-node scale.",
        ],
    }


def _combined_labor_model(patterns: list[dict[str, Any]]) -> dict[str, Any]:
    primary = patterns[0]["labor_model"]
    categories = []
    for pattern in patterns:
        pattern_id = pattern.get("id", "pattern")
        for category in pattern.get("labor_model", {}).get("categories", []):
            merged = dict(category)
            merged["id"] = f"{pattern_id}_{category['id']}"
            merged["label"] = f"{pattern_id}: {category['label']}"
            categories.append(merged)
    return {
        **primary,
        "categories": categories,
    }


def _missing_model_report(module_registry: dict[str, Any], slot_id: str, related_ids: list[str]) -> dict[str, Any]:
    return {
        "kind": "FoodLaborReport",
        "id": f"{module_registry.get('id', 'module_registry')}_{slot_id}_food_labor",
        "generated_by": "ciac.food_labor.v0",
        "provisional": True,
        "status": "fail",
        "module_registry": module_registry.get("id", ""),
        "slot": slot_id,
        "primary_pattern": "",
        "related_patterns": related_ids,
        "unmodeled_patterns": related_ids,
        "summary": {
            "target_population": 0,
            "base_hours_per_week": 0,
            "metrics_recurring_labor_hours_per_week": 0,
            "hours_per_resident_per_week": 0,
            "linear_labor_share": 0,
            "single_largest_category_hours": 0,
            "replication_strategy": "",
            "provisional": True,
        },
        "category_results": [],
        "scaling_results": [],
        "hotspots": [
            {
                "kind": "missing_labor_model",
                "severity": "fail",
                "subject": slot_id,
                "evidence": "No related food pattern declares labor_model categories.",
                "provisional": True,
            }
        ],
        "recommendations": ["Add labor_model categories before claiming food-system scalability."],
        "unknowns": ["No category-level food labor model is available."],
    }


def _slot(module_registry: dict[str, Any], slot_id: str) -> dict[str, Any]:
    for slot in module_registry.get("slots", []):
        if slot.get("id") == slot_id:
            return slot
    return {"id": slot_id, "default_patterns": [], "accepted_patterns": []}


def _category_results(labor_model: dict[str, Any]) -> list[dict[str, Any]]:
    total = sum(float(category["hours_per_week"]) for category in labor_model.get("categories", []))
    results = []
    for category in labor_model.get("categories", []):
        hours = float(category["hours_per_week"])
        results.append(
            {
                "id": category["id"],
                "label": category["label"],
                "hours_per_week": round(hours, 3),
                "share": round(hours / total, 3) if total else 0,
                "scaling_mode": category["scaling_mode"],
                "role": category["role"],
                "reduction_strategy": category["reduction_strategy"],
                "provisional": True,
            }
        )
    return results


def _scaling_targets(module_registry: dict[str, Any], target_population: int, extra_people: list[int] | None = None) -> list[int]:
    targets = {target_population}
    for target in module_registry.get("scaling_policy", {}).get("required_targets", []):
        targets.add(int(target))
    for target in extra_people or []:
        targets.add(int(target))
    return sorted(targets)


def _scale_result(labor_model: dict[str, Any], population: int) -> dict[str, Any]:
    base_population = int(labor_model["target_population"])
    replication = labor_model["replication"]
    max_node_population = int(replication["max_population_per_node"])
    preferred_node_population = int(replication["preferred_population_per_node"])
    nodes = max(1, math.ceil(population / max_node_population))
    population_per_node = population / nodes
    per_node_categories = [
        _scaled_category(category, population_per_node / base_population)
        for category in labor_model.get("categories", [])
    ]
    per_node_hours = sum(category["hours_per_week"] for category in per_node_categories)
    max_category_hours = max(category["hours_per_week"] for category in per_node_categories)
    total_hours = per_node_hours * nodes
    threshold = float(labor_model["thresholds"]["max_hours_per_resident_per_week"])
    category_threshold = float(labor_model["thresholds"]["max_single_category_hours_per_week"])
    hours_per_resident = total_hours / population if population else 0
    status = "pass" if hours_per_resident <= threshold else "warn"
    if population < preferred_node_population or max_category_hours > category_threshold:
        status = "warn"
    return {
        "target_population": population,
        "nodes": nodes,
        "population_per_node": round(population_per_node, 3),
        "per_node_hours_per_week": round(per_node_hours, 3),
        "total_hours_per_week": round(total_hours, 3),
        "hours_per_resident_per_week": round(hours_per_resident, 3),
        "max_category_hours_per_node": round(max_category_hours, 3),
        "status": status,
        "notes": _scale_notes(
            population,
            preferred_node_population,
            max_node_population,
            nodes,
            replication["above_max_strategy"],
            max_category_hours,
            category_threshold,
        ),
        "provisional": True,
    }


def _scaled_category(category: dict[str, Any], ratio: float) -> dict[str, Any]:
    base_hours = float(category["hours_per_week"])
    mode = category["scaling_mode"]
    if mode == "fixed":
        hours = base_hours
    elif mode == "sublinear":
        hours = base_hours * max(0.25, ratio**0.75)
    elif mode == "batch":
        hours = base_hours * max(0.25, math.ceil(ratio * 4) / 4)
    elif mode == "threshold":
        hours = base_hours if ratio <= 1.0 else base_hours * math.ceil(ratio)
    else:
        hours = base_hours * ratio
    return {
        "id": category["id"],
        "hours_per_week": hours,
        "scaling_mode": mode,
    }


def _scale_notes(
    population: int,
    preferred_node_population: int,
    max_node_population: int,
    nodes: int,
    strategy: str,
    max_category_hours: float,
    category_threshold: float,
) -> str:
    if population < preferred_node_population:
        return "Below preferred village-node scale; use smaller food patterns rather than carrying full food-commons overhead."
    if max_category_hours > category_threshold:
        return "Per-node category labor exceeds threshold; split roles, simplify menus, reduce common-meal frequency, or add another food node."
    if population > max_node_population:
        return f"Use {nodes} replicated food node(s): {strategy}."
    return "Within the modeled village-node range."


def _hotspots(
    pattern: dict[str, Any],
    categories: list[dict[str, Any]],
    base_hours: float,
    metric_hours: float,
    target_population: int,
    thresholds: dict[str, Any],
    scaling_results: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    hotspots: list[dict[str, Any]] = []
    if base_hours > TOTAL_LABOR_REVIEW_THRESHOLD:
        hotspots.append(
            _hotspot(
                "total_food_labor_surface",
                "warn",
                pattern["id"],
                f"{base_hours:.1f} hours/week exceeds the {TOTAL_LABOR_REVIEW_THRESHOLD:.1f} hour review threshold, but equals {base_hours / target_population:.2f} hours/resident/week at target scale.",
            )
        )
    if abs(base_hours - metric_hours) > 0.01:
        hotspots.append(
            _hotspot(
                "labor_metric_mismatch",
                "warn",
                pattern["id"],
                f"Labor categories sum to {base_hours:.1f} hours/week while metrics declare {metric_hours:.1f}.",
            )
        )
    max_category = float(thresholds["max_single_category_hours_per_week"])
    for category in categories:
        if category["hours_per_week"] > max_category:
            hotspots.append(
                _hotspot(
                    "category_labor_concentration",
                    "warn",
                    category["id"],
                    f"{category['hours_per_week']:.1f} hours/week exceeds the {max_category:.1f} single-category threshold.",
                )
            )
    linear_share = _linear_share(categories)
    max_linear_share = float(thresholds["max_linear_labor_share"])
    if linear_share > max_linear_share:
        hotspots.append(
            _hotspot(
                "linear_labor_share",
                "warn",
                pattern["id"],
                f"{linear_share:.2f} of food labor scales linearly, above the {max_linear_share:.2f} threshold.",
            )
        )
    for result in scaling_results:
        if result["status"] == "warn":
            hotspots.append(
                _hotspot(
                    "scale_fit_warning",
                    "warn",
                    str(result["target_population"]),
                    result["notes"],
                )
            )
    return hotspots


def _hotspot(kind: str, severity: str, subject: str, evidence: str) -> dict[str, Any]:
    return {
        "kind": kind,
        "severity": severity,
        "subject": subject,
        "evidence": evidence,
        "provisional": True,
    }


def _recommendations(hotspots: list[dict[str, Any]]) -> list[str]:
    recommendations = [
        "Treat food labor as a first-class dignity constraint alongside servings, storage, water, energy, and food safety.",
        "Keep common meals opt-in and batch-oriented; do not let the food commons become an uncounted daily service job.",
        "Replicate food nodes above village scale instead of centralizing one large institutional kitchen.",
    ]
    if any(hotspot["kind"] == "scale_fit_warning" and hotspot["subject"] == "12" for hotspot in hotspots):
        recommendations.append("Use the smaller kitchen, greenhouse, and staple reserve defaults for the 5-household demo scale.")
    if any(hotspot["kind"] == "total_food_labor_surface" for hotspot in hotspots):
        recommendations.append("Run menu simplification, cleanup flow, and garden-crop selection against total weekly food labor before adding food amenities.")
    return recommendations


def _linear_share(categories: list[dict[str, Any]]) -> float:
    total = sum(float(category["hours_per_week"]) for category in categories)
    if not total:
        return 0.0
    linear = sum(float(category["hours_per_week"]) for category in categories if category["scaling_mode"] == "linear")
    return linear / total


def _status(hotspots: list[dict[str, Any]]) -> str:
    if any(hotspot["severity"] == "fail" for hotspot in hotspots):
        return "fail"
    if hotspots:
        return "warn"
    return "pass"
