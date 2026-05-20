from __future__ import annotations

from typing import Any

from .models import GateResult


def evaluate_gates(compiled_plan: dict[str, Any]) -> dict[str, Any]:
    selected = set(compiled_plan.get("selected_patterns", []))
    missing = compiled_plan.get("missing_dependencies", [])
    results = [
        _water_gate(selected, missing),
        _sanitation_gate(selected, missing),
        _energy_gate(selected),
        _labor_gate(compiled_plan),
        _food_gate(selected),
        _governance_gate(compiled_plan),
        _maintainability_gate(compiled_plan),
    ]
    return {
        "kind": "GateReport",
        "compiled_plan": compiled_plan.get("id"),
        "promotion_allowed": not any(result.status == "fail" and result.survival_critical for result in results),
        "results": [result.to_dict() for result in results],
    }


def _water_gate(selected: set[str], missing: list[dict[str, Any]]) -> GateResult:
    water_sources = {"well_house", "rainwater_capture"} & selected
    missing_water = [dep for dep in missing if "water" in dep["dependency_id"] or dep["dependency_id"] in {"well_house", "rainwater_capture"}]
    if not water_sources or any(dep["critical"] for dep in missing_water):
        return GateResult(
            "water_gate",
            "fail",
            ["No complete selected water stack is available."],
            ["Select and resolve well_house or rainwater_capture with testing, storage, and stewardship prerequisites."],
            True,
        )
    if len(water_sources) == 1:
        return GateResult(
            "water_gate",
            "warn",
            [f"Selected water source: {sorted(water_sources)[0]}."],
            ["Add a redundant water source or emergency storage before promotion."],
            True,
        )
    return GateResult("water_gate", "pass", ["Well and rainwater capture are both selected."], [], True)


def _sanitation_gate(selected: set[str], missing: list[dict[str, Any]]) -> GateResult:
    if {"shared_bathhouse", "composting_system"}.issubset(selected) and not any(
        dep["critical"] and dep["dependency_id"] in {"shared_bathhouse", "composting_system"} for dep in missing
    ):
        return GateResult("sanitation_gate", "pass", ["Shared bathhouse and composting system are selected."], [], True)
    return GateResult(
        "sanitation_gate",
        "fail",
        ["Sanitation stack is incomplete."],
        ["Select shared_bathhouse and composting_system, then resolve local sanitation code review."],
        True,
    )


def _energy_gate(selected: set[str]) -> GateResult:
    if "solar_shed" in selected:
        return GateResult("energy_gate", "pass", ["Solar shed is selected for basic critical loads."], [], True)
    return GateResult("energy_gate", "fail", ["No basic energy pattern is selected."], ["Select solar_shed or another critical-load energy pattern."], True)


def _labor_gate(compiled_plan: dict[str, Any]) -> GateResult:
    hours = float(compiled_plan.get("role_burden", {}).get("recurring_hours_per_resident_per_week", 0))
    evidence = [f"Recurring maintenance burden is {hours:.2f} hours per resident per week."]
    if hours <= 8:
        return GateResult("labor_gate", "pass", evidence, [], True)
    if hours <= 12:
        return GateResult("labor_gate", "warn", evidence, ["Reduce recurring tasks or increase trained participants before promotion."], True)
    return GateResult("labor_gate", "fail", evidence, ["Redesign to lower recurring labor below 8 hours per resident per week."], True)


def _food_gate(selected: set[str]) -> GateResult:
    if {"greenhouse", "community_kitchen"}.issubset(selected):
        return GateResult(
            "food_gate",
            "warn",
            ["Greenhouse and community kitchen are selected, but full nutrition is not simulated in Sprint 1."],
            ["Add nutrition targets, crop plans, storage, preservation, and fallback procurement in the simulation sprint."],
            True,
        )
    return GateResult(
        "food_gate",
        "fail",
        ["Food production or preparation pattern is missing."],
        ["Select greenhouse and community_kitchen as a minimum draft food stack."],
        True,
    )


def _governance_gate(compiled_plan: dict[str, Any]) -> GateResult:
    missing_critical = [dep for dep in compiled_plan.get("missing_dependencies", []) if dep.get("critical")]
    if missing_critical:
        return GateResult(
            "governance_gate",
            "fail",
            [f"{len(missing_critical)} critical dependency or governance prerequisite(s) are unresolved."],
            ["Resolve all critical dependencies before promotion."],
            True,
        )
    return GateResult(
        "governance_gate",
        "pass",
        ["No unresolved critical dependencies remain in the compiled plan."],
        [],
        True,
    )


def _maintainability_gate(compiled_plan: dict[str, Any]) -> GateResult:
    calendar = compiled_plan.get("maintenance_calendar", [])
    risks = compiled_plan.get("risk_register", [])
    if calendar and risks:
        return GateResult(
            "maintainability_gate",
            "pass",
            [f"{len(calendar)} maintenance tasks and {len(risks)} failure modes are declared."],
            [],
            False,
        )
    return GateResult(
        "maintainability_gate",
        "fail",
        ["Maintenance calendar or risk register is empty."],
        ["Ensure every selected pattern declares maintenance tasks and failure modes."],
        False,
    )

