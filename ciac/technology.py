from __future__ import annotations

from typing import Any


SURVIVAL_RESOURCES = {"food_servings_per_day", "water_liters_per_day", "energy_kwh_per_day"}


def pressure_test_technology_module(compiled_plan: dict[str, Any], technology_module: dict[str, Any]) -> dict[str, Any]:
    gaps = _integration_gaps(technology_module)
    coexistence = _coexistence_checks(compiled_plan, technology_module)
    floor_effect = _dignity_floor_effect(technology_module)
    status = _status(gaps, coexistence, floor_effect)
    return {
        "kind": "TechnologyPressureTestReport",
        "id": f"{compiled_plan['id']}_{technology_module['id']}_pressure_test",
        "generated_by": "ciac.technology.v0",
        "provisional": True,
        "status": status,
        "compiled_plan": compiled_plan["id"],
        "technology_module": technology_module["id"],
        "operator_summary": _operator_summary(status, technology_module),
        "dignity_floor_effect": floor_effect,
        "evidence_summary": _evidence_summary(technology_module),
        "modeled_impacts": technology_module.get("modeled_impacts", {}),
        "integration_gaps": gaps,
        "coexistence_checks": coexistence,
        "next_actions": _next_actions(status),
        "unknowns": [
            *technology_module.get("unknowns", []),
            "Technology pressure tests are model-readiness checks, not proof of real-world performance.",
        ],
    }


def evaluate_module_compatibility(
    compiled_plan: dict[str, Any],
    module_registry: dict[str, Any],
    technology_modules: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    modules = technology_modules or []
    slot_results = [_slot_result(compiled_plan, slot, modules) for slot in module_registry.get("slots", [])]
    drag_and_drop = [
        candidate
        for result in slot_results
        for candidate in result["candidate_modules"]
        if candidate["compatibility"] == "drag_and_drop"
    ]
    adapter_required = [
        candidate
        for result in slot_results
        for candidate in result["candidate_modules"]
        if candidate["compatibility"] == "adapter_required"
    ]
    not_applicable = [
        candidate
        for result in slot_results
        for candidate in result["candidate_modules"]
        if candidate["compatibility"] == "not_applicable"
    ]
    research_backlog = [
        {
            "slot": result["slot"],
            "domain": result["domain"],
            "queries": result["research_queries"],
            "reason": "No drag-and-drop module is currently available for this slot.",
            "provisional": True,
        }
        for result in slot_results
        if not any(candidate["compatibility"] == "drag_and_drop" for candidate in result["candidate_modules"])
    ]
    status = "ready_with_warnings" if drag_and_drop else "needs_research"
    if not slot_results:
        status = "not_ready"
    return {
        "kind": "ModuleCompatibilityReport",
        "id": f"{compiled_plan['id']}_{module_registry['id']}_module_compatibility",
        "generated_by": "ciac.technology.v0",
        "provisional": True,
        "status": status,
        "compiled_plan": compiled_plan["id"],
        "module_registry": module_registry["id"],
        "slot_results": slot_results,
        "drag_and_drop_candidates": drag_and_drop,
        "adapter_required": adapter_required,
        "not_applicable": not_applicable,
        "research_backlog": research_backlog,
        "next_actions": _compatibility_next_actions(drag_and_drop, adapter_required, research_backlog),
        "unknowns": [
            "Module compatibility is simulation-interface compatibility only.",
            "AI tooling may propose modules, but source extraction, performance mapping, and uncertainty must remain visible.",
            "Scaling requires explicit module interfaces at each household target.",
        ],
    }


def _dignity_floor_effect(module: dict[str, Any]) -> dict[str, Any]:
    effects = module.get("modeled_impacts", {}).get("direct_resource_effects", {})
    resource_effects = {
        resource: float(effects.get(resource, 0) or 0)
        for resource in SURVIVAL_RESOURCES
    }
    regressions = [
        f"{resource} has negative direct effect {value}"
        for resource, value in resource_effects.items()
        if value < 0
    ]
    return {
        "policy": module.get("modeled_impacts", {}).get("dignity_floor_policy", "unknown"),
        "direct_resource_effects": resource_effects,
        "regressions": regressions,
        "safe_for_operator_iteration": not regressions,
        "provisional": True,
    }


def _slot_result(compiled_plan: dict[str, Any], slot: dict[str, Any], modules: list[dict[str, Any]]) -> dict[str, Any]:
    selected = set(compiled_plan.get("selected_patterns", []))
    defaults = slot.get("default_patterns", [])
    default_present = sorted(selected.intersection(defaults))
    candidates = [_module_candidate(slot, module) for module in modules]
    return {
        "slot": slot["id"],
        "domain": slot["domain"],
        "role": slot["role"],
        "default_patterns": defaults,
        "default_patterns_present": default_present,
        "default_posture_ready": set(defaults).issubset(selected),
        "swap_policy": slot["swap_policy"],
        "scaling_basis": slot.get("scaling_basis", ""),
        "candidate_modules": candidates,
        "research_queries": slot.get("research_queries", []),
        "provisional": True,
    }


def _module_candidate(slot: dict[str, Any], module: dict[str, Any]) -> dict[str, Any]:
    module_domains = set(module.get("domain", []))
    accepted = set(slot.get("accepted_module_domains", []))
    target_slots = set(module.get("applicability", {}).get("target_slots", []))
    floor_effect = _dignity_floor_effect(module)
    gaps = _module_interface_gaps(slot, module)
    if target_slots and slot["id"] not in target_slots:
        compatibility = "not_applicable"
    elif not module_domains.intersection(accepted):
        compatibility = "not_applicable"
    elif gaps or slot.get("swap_policy") == "adapter_required":
        compatibility = "adapter_required"
    elif floor_effect["safe_for_operator_iteration"]:
        compatibility = "drag_and_drop"
    else:
        compatibility = "not_applicable"
    return {
        "module": module["id"],
        "name": module["name"],
        "compatibility": compatibility,
        "interface_gaps": gaps,
        "safe_for_operator_iteration": floor_effect["safe_for_operator_iteration"],
        "evidence_status": module.get("status", "draft"),
        "provisional": True,
    }


def _module_interface_gaps(slot: dict[str, Any], module: dict[str, Any]) -> list[str]:
    impacts = module.get("modeled_impacts", {})
    direct = impacts.get("direct_resource_effects", {})
    gaps = []
    for interface in slot.get("required_interfaces", []):
        if interface.startswith("resource_effects."):
            key = interface.split(".", 1)[1]
            if key not in direct:
                gaps.append(interface)
        elif interface.startswith("storage."):
            gaps.append(interface)
        elif interface not in impacts.get("candidate_modifiers", {}):
            gaps.append(interface)
    return gaps


def _compatibility_next_actions(
    drag_and_drop: list[dict[str, Any]],
    adapter_required: list[dict[str, Any]],
    research_backlog: list[dict[str, Any]],
) -> list[str]:
    actions = []
    if drag_and_drop:
        actions.append("Pressure-test drag-and-drop modules in normal-year and stress scenario simulations.")
    if adapter_required:
        actions.append("Build adapter models for promising modules before letting them affect resource flows.")
    if research_backlog:
        actions.append("Use AI-assisted literature scans for slots without drag-and-drop candidates.")
    return actions or ["Define module slots before attempting research-backed swapping."]


def _evidence_summary(module: dict[str, Any]) -> list[dict[str, Any]]:
    rows = []
    for stat in module.get("performance_statistics", []):
        rows.append(
            {
                "metric": stat.get("metric", ""),
                "value": stat.get("value", ""),
                "unit": stat.get("unit", ""),
                "comparator": stat.get("comparator", ""),
                "ciac_use": stat.get("ciac_use", "evidence_only"),
                "evidence_status": stat.get("evidence_status", "unknown"),
                "provisional": bool(stat.get("provisional", True)),
            }
        )
    return rows


def _integration_gaps(module: dict[str, Any]) -> list[str]:
    gaps = list(module.get("integration_requirements", []))
    effects = module.get("modeled_impacts", {}).get("direct_resource_effects", {})
    if not any(float(effects.get(resource, 0) or 0) for resource in SURVIVAL_RESOURCES):
        gaps.append("No direct CIaC survival-resource effect is modeled yet.")
    return sorted(set(gaps))


def _coexistence_checks(compiled_plan: dict[str, Any], module: dict[str, Any]) -> list[dict[str, Any]]:
    selected = set(compiled_plan.get("selected_patterns", []))
    targets = set(module.get("applicability", {}).get("target_patterns", []))
    present = sorted(selected.intersection(targets))
    return [
        {
            "id": "target_pattern_presence",
            "status": "pass" if present else "warn",
            "evidence": f"Target pattern(s) present: {', '.join(present) if present else 'none'}.",
            "provisional": True,
        },
        {
            "id": "dignity_floor_policy",
            "status": "pass" if module.get("modeled_impacts", {}).get("dignity_floor_policy") == "additive_only" else "warn",
            "evidence": f"Policy: {module.get('modeled_impacts', {}).get('dignity_floor_policy', 'unknown')}.",
            "provisional": True,
        },
    ]


def _status(gaps: list[str], coexistence: list[dict[str, Any]], floor_effect: dict[str, Any]) -> str:
    if floor_effect["regressions"]:
        return "blocked"
    if any(check["status"] == "warn" for check in coexistence):
        return "not_applicable"
    if gaps:
        return "needs_modeling"
    return "candidate_for_simulation"


def _operator_summary(status: str, module: dict[str, Any]) -> str:
    name = module.get("name", module.get("id", "technology module"))
    if status == "blocked":
        return f"{name} is blocked because it would reduce a dignity-floor resource."
    if status == "not_applicable":
        return f"{name} has evidence, but the current compiled plan lacks a compatible target pattern."
    if status == "needs_modeling":
        return f"{name} is promising evidence, but needs conversion rules before it can change simulation resources."
    return f"{name} is ready for provisional simulation as an additive technology module."


def _next_actions(status: str) -> list[str]:
    if status == "blocked":
        return ["Reject or rewrite the module so it cannot reduce food, water, or critical energy dignity floors."]
    if status == "not_applicable":
        return ["Add a compatible target pattern or mark the module as a future-site option."]
    if status == "needs_modeling":
        return [
            "Add conversion rules from published metrics into CIaC resource effects.",
            "Add scenario replay hypotheses before allowing the module to affect optimization.",
        ]
    return ["Run the module through normal-year and stress scenario simulation before ranking it against alternatives."]
