from __future__ import annotations

from copy import deepcopy
from typing import Any

from .research import evaluate_scalability_gate
from .simulation import simulate
from .simulation_compare import compare_simulations


RESOURCE_EFFECT_KEYS = ("water_liters_per_day", "energy_kwh_per_day", "food_servings_per_day")


def implement_technology_module(
    compiled_plan: dict[str, Any],
    technology_module: dict[str, Any],
    module_registry: dict[str, Any] | None = None,
    days: int = 365,
    review_status: dict[str, Any] | None = None,
) -> dict[str, Any]:
    scalability_gate = evaluate_scalability_gate(compiled_plan, technology_module, module_registry)
    effects = _resource_effects(technology_module)
    blockers = _effect_blockers(effects)

    if not scalability_gate["passes_scalability_gate"]:
        return _blocked_report(
            "blocked_by_scalability_gate",
            compiled_plan,
            technology_module,
            module_registry,
            days,
            scalability_gate,
            effects,
            scalability_gate["next_actions"],
        )
    if blockers:
        return _blocked_report(
            "blocked_by_effects",
            compiled_plan,
            technology_module,
            module_registry,
            days,
            scalability_gate,
            effects,
            blockers,
        )

    implemented_plan = _implemented_plan(compiled_plan, technology_module, effects)
    baseline = simulate(compiled_plan, days=days, review_status=review_status)
    implemented = simulate(implemented_plan, days=days, review_status=review_status)
    comparison = compare_simulations(baseline, implemented)
    status = "implemented"
    if comparison["status"] == "stress_failed":
        status = "implemented_with_regression"
    elif comparison["status"] == "stress_warn":
        status = "implemented_with_warnings"

    return {
        "kind": "ModuleImplementationReport",
        "id": f"{compiled_plan['id']}_{technology_module['id']}_module_implementation",
        "generated_by": "ciac.module_implementation.v0",
        "provisional": True,
        "status": status,
        "compiled_plan": compiled_plan["id"],
        "technology_module": technology_module["id"],
        "module_registry": module_registry.get("id", "") if module_registry else "",
        "days": days,
        "scalability_gate": scalability_gate,
        "applied_effects": effects,
        "implemented_plan": implemented_plan,
        "baseline_simulation": baseline,
        "implemented_simulation": implemented,
        "comparison_report": comparison,
        "next_actions": _implemented_next_actions(status),
        "unknowns": [
            *technology_module.get("unknowns", []),
            "Module implementation is a provisional simulator materialization, not real-world technology approval.",
            "Only explicit direct CIaC resource effects are applied; prose claims and unmodeled costs remain excluded.",
            "Passing this step does not satisfy resident consent, professional review, sourcing, permitting, or safety duties.",
        ],
    }


def _blocked_report(
    status: str,
    compiled_plan: dict[str, Any],
    technology_module: dict[str, Any],
    module_registry: dict[str, Any] | None,
    days: int,
    scalability_gate: dict[str, Any],
    effects: dict[str, float],
    next_actions: list[str],
) -> dict[str, Any]:
    return {
        "kind": "ModuleImplementationReport",
        "id": f"{compiled_plan['id']}_{technology_module['id']}_module_implementation",
        "generated_by": "ciac.module_implementation.v0",
        "provisional": True,
        "status": status,
        "compiled_plan": compiled_plan["id"],
        "technology_module": technology_module["id"],
        "module_registry": module_registry.get("id", "") if module_registry else "",
        "days": days,
        "scalability_gate": scalability_gate,
        "applied_effects": effects,
        "implemented_plan": None,
        "baseline_simulation": None,
        "implemented_simulation": None,
        "comparison_report": None,
        "next_actions": next_actions,
        "unknowns": [
            *technology_module.get("unknowns", []),
            "Blocked modules do not alter the compiled plan or simulation.",
            "The module must pass CIaC interface, evidence, labor, and dignity-floor checks before implementation.",
        ],
    }


def _resource_effects(module: dict[str, Any]) -> dict[str, float]:
    direct = module.get("modeled_impacts", {}).get("direct_resource_effects", {})
    return {key: float(direct.get(key, 0) or 0) for key in RESOURCE_EFFECT_KEYS}


def _effect_blockers(effects: dict[str, float]) -> list[str]:
    blockers = []
    if not any(value != 0 for value in effects.values()):
        blockers.append("Declare at least one nonzero direct CIaC resource effect before implementation.")
    for key, value in effects.items():
        if value < 0:
            blockers.append(f"{key} effect {value} would reduce a dignity-floor resource.")
    return blockers


def _implemented_plan(compiled_plan: dict[str, Any], module: dict[str, Any], effects: dict[str, float]) -> dict[str, Any]:
    plan = deepcopy(compiled_plan)
    module_pattern_id = f"module_{module['id']}"
    plan["id"] = f"{compiled_plan['id']}_{module['id']}_implemented"
    plan["selected_patterns"] = [*plan.get("selected_patterns", []), module_pattern_id]
    plan.setdefault("implemented_modules", []).append(
        {
            "module": module["id"],
            "name": module.get("name", module["id"]),
            "source_status": module.get("status", "unknown"),
            "applied_as_pattern": module_pattern_id,
            "applied_effects": effects,
            "provisional": True,
        }
    )
    simulation_inputs = plan["simulation_inputs"]
    simulation_inputs["resource_effects_by_pattern"][module_pattern_id] = effects
    simulation_inputs["critical_resources_by_pattern"][module_pattern_id] = [
        key.replace("_per_day", "")
        for key, value in effects.items()
        if value > 0
    ]
    simulation_inputs["storage_by_pattern"][module_pattern_id] = []
    return plan


def _implemented_next_actions(status: str) -> list[str]:
    if status == "implemented_with_regression":
        return [
            "Do not promote this module candidate.",
            "Inspect the comparison report and rewrite the module effects or interfaces before another implementation attempt.",
        ]
    if status == "implemented_with_warnings":
        return [
            "Inspect warning deltas before ranking this implemented module.",
            "Run stress replays before using this implemented plan as an optimizer candidate.",
        ]
    return [
        "Run stress replays for the implemented module candidate.",
        "Use the implemented plan as a provisional optimizer candidate only while review and governance blockers stay visible.",
    ]
