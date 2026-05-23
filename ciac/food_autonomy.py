from __future__ import annotations

from collections import defaultdict
from typing import Any


LEDGER_RESOURCES = ["food_servings", "water_liters", "energy_kwh"]


def generate_food_autonomy_report(
    cycle_iteration: dict[str, Any],
    scenarios: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    simulation = cycle_iteration.get("applied_simulation", {})
    population_context = cycle_iteration.get("viewer_population_context", {})
    population = int(population_context.get("population") or simulation.get("population", {}).get("population", 0))
    food = _food_autonomy(simulation, population)
    smoothing = _seasonal_smoothing(simulation)
    risk_coverage = _risk_scenario_coverage(simulation, scenarios or [], cycle_iteration.get("applied_scenarios", []))
    hotspots = _hotspots(food, smoothing, risk_coverage)
    status = _status(hotspots)
    return {
        "kind": "FoodAutonomyReport",
        "id": f"{cycle_iteration.get('id', 'cycle_iteration')}_food_autonomy",
        "generated_by": "ciac.food_autonomy.v0",
        "provisional": True,
        "status": status,
        "source_cycle_iteration": cycle_iteration.get("id", ""),
        "population": population,
        "food_autonomy": food,
        "seasonal_smoothing": smoothing,
        "risk_scenario_coverage": risk_coverage,
        "hotspots": hotspots,
        "recommendations": _recommendations(hotspots),
        "unknowns": [
            "Food autonomy uses simulation ledger flows; it is not a diet, procurement contract, crop plan, or food-safety approval.",
            "Storage release is treated as dependency pressure even when reserves are intentionally abundant.",
            "Seasonal smoothing is inferred from provisional seasonal multipliers and modeled curtailment, not measured weather, harvest, or demand data.",
            "Risk coverage checks whether high-consequence modes have named stress scenarios; it does not prove those scenarios are sufficient.",
        ],
    }


def _food_autonomy(simulation: dict[str, Any], population: int) -> dict[str, Any]:
    ledger = simulation.get("resource_ledger", {}).get("food_servings", {})
    annual_consumption = float(ledger.get("total_consumption", 0.0))
    annual_production = float(ledger.get("total_production", 0.0))
    reserve_release = float(ledger.get("total_storage_release", 0.0))
    reserve_refill = float(ledger.get("total_storage_refill", 0.0))
    net_drawdown = max(0.0, reserve_release - reserve_refill)
    production_ratio = annual_production / annual_consumption if annual_consumption else 0.0
    reserve_release_ratio = reserve_release / annual_consumption if annual_consumption else 0.0
    procurement_dependency_ratio = max(0.0, 1.0 - production_ratio)
    drawdown_per_resident = net_drawdown / population if population else 0.0
    status = "pass"
    if production_ratio < 0.75 or reserve_release_ratio > 0.35:
        status = "fail"
    elif production_ratio < 0.9 or reserve_release_ratio > 0.1:
        status = "warn"
    return {
        "annual_consumption_servings": round(annual_consumption, 3),
        "annual_modeled_production_servings": round(annual_production, 3),
        "annual_storage_release_servings": round(reserve_release, 3),
        "annual_storage_refill_servings": round(reserve_refill, 3),
        "net_reserve_drawdown_servings": round(net_drawdown, 3),
        "production_ratio": round(production_ratio, 3),
        "reserve_release_ratio": round(reserve_release_ratio, 3),
        "procurement_dependency_ratio": round(procurement_dependency_ratio, 3),
        "reserve_drawdown_per_resident_servings": round(drawdown_per_resident, 3),
        "status": status,
        "provisional": True,
    }


def _seasonal_smoothing(simulation: dict[str, Any]) -> dict[str, Any]:
    resources = []
    hotspots = []
    for resource in LEDGER_RESOURCES:
        ledger = simulation.get("resource_ledger", {}).get(resource, {})
        rows = _season_rows(ledger.get("entries", []))
        total_curtailment = float(ledger.get("total_curtailment", 0.0))
        total_consumption = float(ledger.get("total_consumption", 0.0))
        total_release = float(ledger.get("total_storage_release", 0.0))
        deficit_seasons = [row["season"] for row in rows if row["raw_net"] < 0]
        surplus_seasons = [row["season"] for row in rows if row["raw_net"] > 0]
        curtailment_ratio = total_curtailment / total_consumption if total_consumption else 0.0
        resources.append(
            {
                "resource": resource,
                "status": ledger.get("status", "pass"),
                "total_curtailment": round(total_curtailment, 3),
                "total_storage_release": round(total_release, 3),
                "curtailment_ratio": round(curtailment_ratio, 3),
                "deficit_seasons": deficit_seasons,
                "surplus_seasons": surplus_seasons,
                "season_rows": rows,
                "provisional": True,
            }
        )
        if curtailment_ratio > 0.1:
            hotspots.append(
                _hotspot(
                    "seasonal_curtailment",
                    "warn",
                    resource,
                    f"{resource} curtails {total_curtailment:.1f} units/year while other resources may still draw storage.",
                )
            )
        if len(deficit_seasons) >= 2:
            hotspots.append(
                _hotspot(
                    "multi_season_deficit",
                    "warn" if ledger.get("status") == "pass" else "fail",
                    resource,
                    f"{resource} has modeled seasonal deficits in {', '.join(deficit_seasons)}.",
                )
            )
    return {
        "status": _status(hotspots),
        "resources": resources,
        "hotspots": hotspots,
        "recommendations": [
            "Use curtailed water and energy windows to test preservation, batch processing, storage refill, and low-labor seasonal production.",
            "Track whether food reserve release is caused by winter/summer production gaps or by insufficient annual production.",
            "Prefer smoothing moves that reduce reserve drawdown without increasing per-resident labor or water intensity.",
        ],
        "provisional": True,
    }


def _season_rows(entries: list[dict[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[str, dict[str, float]] = defaultdict(lambda: {"days": 0, "production": 0.0, "consumption": 0.0, "raw_net": 0.0, "curtailment": 0.0, "storage_release": 0.0, "storage_refill": 0.0, "unmet_demand": 0.0})
    order: list[str] = []
    for entry in entries:
        season = str(entry.get("season", "unknown"))
        if season not in grouped:
            order.append(season)
        row = grouped[season]
        row["days"] += 1
        for key in ["production", "consumption", "raw_net", "curtailment", "storage_release", "storage_refill", "unmet_demand"]:
            row[key] += float(entry.get(key, 0.0) or 0.0)
    return [
        {
            "season": season,
            **{key: round(value, 3) for key, value in grouped[season].items()},
            "provisional": True,
        }
        for season in order
    ]


def _risk_scenario_coverage(
    simulation: dict[str, Any],
    scenarios: list[dict[str, Any]],
    applied_scenarios: list[dict[str, Any]],
) -> dict[str, Any]:
    triggered_modes = sorted({risk.get("mode", "") for risk in simulation.get("triggered_risks", []) if risk.get("mode")})
    covered_modes = sorted({mode for scenario in scenarios for mode in scenario.get("triggered_risk_modes", [])})
    uncovered = [mode for mode in triggered_modes if mode not in covered_modes]
    scenario_status = {row.get("scenario"): row.get("status", "unknown") for row in applied_scenarios}
    rows = [
        {
            "scenario": scenario.get("id", ""),
            "status": scenario_status.get(scenario.get("id", ""), "not_run"),
            "covered_modes": scenario.get("triggered_risk_modes", []),
            "provisional": True,
        }
        for scenario in scenarios
    ]
    status = "pass"
    if uncovered:
        status = "warn"
    if triggered_modes and not rows:
        status = "fail"
    return {
        "status": status,
        "triggered_risk_count": len(triggered_modes),
        "covered_risk_modes": [mode for mode in triggered_modes if mode in covered_modes],
        "uncovered_risk_modes": uncovered,
        "scenario_rows": rows,
        "provisional": True,
    }


def _hotspots(food: dict[str, Any], smoothing: dict[str, Any], risk_coverage: dict[str, Any]) -> list[dict[str, Any]]:
    hotspots = []
    if food["status"] != "pass":
        hotspots.append(
            _hotspot(
                "food_procurement_dependency",
                food["status"],
                "food_servings",
                f"Modeled production ratio is {food['production_ratio']}; reserve release ratio is {food['reserve_release_ratio']}.",
            )
        )
    hotspots.extend(smoothing.get("hotspots", []))
    if risk_coverage["status"] != "pass":
        hotspots.append(
            _hotspot(
                "risk_scenario_gap",
                risk_coverage["status"],
                "high_consequence_risks",
                f"Uncovered high-consequence modes: {', '.join(risk_coverage['uncovered_risk_modes']) or 'none'}.",
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
        "Treat food autonomy as a reserve-drawdown problem before adding more production surface.",
        "Use seasonal smoothing experiments to convert existing surplus windows into lower food drawdown.",
        "Add explicit stress scenarios for every catastrophic risk mode before treating baseline warnings as resolved.",
    ]
    if any(hotspot["kind"] == "food_procurement_dependency" for hotspot in hotspots):
        recommendations.append("Test preservation, procurement scheduling, crop mix, and low-water protein assumptions against reserve drawdown per resident.")
    if any(hotspot["kind"] == "risk_scenario_gap" for hotspot in hotspots):
        recommendations.append("Add missing potable contamination, cross-connection, and battery fire/fault scenario coverage before promotion.")
    return recommendations


def _status(hotspots: list[dict[str, Any]]) -> str:
    if any(hotspot["severity"] == "fail" for hotspot in hotspots):
        return "fail"
    if hotspots:
        return "warn"
    return "pass"
