from __future__ import annotations

from typing import Any


SURVIVAL_RESOURCE_KEYS = {
    "food_servings": "food_servings_per_day",
    "water_liters": "water_liters_per_day",
    "energy_kwh": "energy_kwh_per_day",
}


def generate_research_needs(
    compiled_plan: dict[str, Any],
    simulation_run: dict[str, Any],
    module_registry: dict[str, Any] | None = None,
) -> dict[str, Any]:
    needs = []
    food_need = _food_production_need(compiled_plan, simulation_run, module_registry)
    if food_need:
        needs.append(food_need)
    status = "needs_research" if needs else "no_research_needed"
    if any(need["model_gap_severity"] == "blocking" for need in needs):
        status = "blocked_by_model_gap"
    return {
        "kind": "ResearchNeedReport",
        "id": f"{compiled_plan['id']}_{simulation_run['id']}_research_needs",
        "generated_by": "ciac.research.v0",
        "provisional": True,
        "status": status,
        "compiled_plan": compiled_plan["id"],
        "simulation_run": simulation_run["id"],
        "needs": needs,
        "next_actions": _research_next_actions(needs),
        "unknowns": [
            "Research needs are search briefs for evidence gathering, not endorsements of any technology.",
            "Planning-phase evidence review must preserve citations, study context, performance statistics, limitations, and uncertainty.",
            "Preauthored or researched modules must pass scalability gates before they can affect optimization.",
        ],
    }


def evaluate_scalability_gate(
    compiled_plan: dict[str, Any],
    technology_module: dict[str, Any],
    module_registry: dict[str, Any] | None = None,
) -> dict[str, Any]:
    targets = _scaling_targets(compiled_plan, module_registry)
    gate_results = [
        _dignity_floor_gate(technology_module),
        _evidence_gate(technology_module),
        _interface_gate(technology_module, module_registry),
        _labor_gate(technology_module),
        _automation_gate(technology_module),
        _transferability_gate(technology_module),
    ]
    status = _gate_status(gate_results)
    return {
        "kind": "ScalabilityGateReport",
        "id": f"{compiled_plan['id']}_{technology_module['id']}_scalability_gate",
        "generated_by": "ciac.research.v0",
        "provisional": True,
        "status": status,
        "compiled_plan": compiled_plan["id"],
        "technology_module": technology_module["id"],
        "passes_scalability_gate": status == "pass",
        "gate_results": gate_results,
        "scaling_targets": targets,
        "module_summary": {
            "name": technology_module["name"],
            "domain": technology_module.get("domain", []),
            "status": technology_module.get("status", "draft"),
            "target_slots": technology_module.get("applicability", {}).get("target_slots", []),
            "target_patterns": technology_module.get("applicability", {}).get("target_patterns", []),
            "provisional": True,
        },
        "next_actions": _scalability_next_actions(gate_results),
        "unknowns": [
            *technology_module.get("unknowns", []),
            "Scalability gates are simulation-readiness filters, not legal, engineering, safety, or construction approval.",
            "Passing the gate means the module can be compared in CIaC; it does not prove real-world suitability.",
        ],
    }


def _food_production_need(
    compiled_plan: dict[str, Any],
    simulation_run: dict[str, Any],
    module_registry: dict[str, Any] | None,
) -> dict[str, Any] | None:
    ledger = simulation_run.get("resource_ledger", {}).get("food_servings")
    if not ledger:
        return None
    days = max(1, int(simulation_run.get("days", 365)))
    production_per_day = float(ledger.get("total_production", 0.0)) / days
    consumption_per_day = float(ledger.get("total_consumption", 0.0)) / days
    if consumption_per_day <= 0 or production_per_day >= consumption_per_day:
        return None
    gap = max(0.0, consumption_per_day - production_per_day)
    coverage = production_per_day / consumption_per_day if consumption_per_day else 0.0
    greenhouse_effect = (
        compiled_plan.get("simulation_inputs", {})
        .get("resource_effects_by_pattern", {})
        .get("greenhouse", {})
        .get("food_servings_per_day", 0)
    )
    food_slot = _registry_slot(module_registry, "food_production")
    return {
        "id": "food_local_production_gap_v0",
        "domain": "food",
        "bottleneck": "Local food production is not sufficient to meet daily serving demand without drawing down staple reserves.",
        "model_gap_severity": "blocking",
        "evidence": [
            f"Modeled local food production averages {production_per_day:.2f} servings/day against {consumption_per_day:.2f} servings/day demand.",
            f"Greenhouse seed pattern contributes {float(greenhouse_effect):.2f} base servings/day before seasonal multipliers.",
            f"Food reserve ends at {float(ledger.get('ending_balance', 0.0)):.2f} servings after a net modeled drawdown of {gap * days:.2f} servings/year.",
        ],
        "target": {
            "resource": "food_servings",
            "required_delta_per_day": round(gap, 3),
            "current_local_production_per_day": round(production_per_day, 3),
            "current_consumption_per_day": round(consumption_per_day, 3),
            "current_local_coverage_ratio": round(coverage, 3),
            "scale_target_people": simulation_run.get("population", {}).get("population", compiled_plan.get("site_summary", {}).get("population_target", 0)),
            "provisional": True,
        },
        "constraints": {
            "preserve_dignity_floors": ["food_servings", "water_liters", "energy_kwh"],
            "must_reduce_or_not_increase_involuntary_labor": True,
            "must_expose_water_energy_land_and_skill_requirements": True,
            "must_include_failure_modes_and_storage_or_preservation_implications": True,
            "provisional": True,
        },
        "module_slot": food_slot.get("id", "food_production"),
        "accepted_module_domains": food_slot.get("accepted_module_domains", ["food"]),
        "search_queries": _food_queries(food_slot),
        "provisional": True,
    }


def _food_queries(food_slot: dict[str, Any]) -> list[str]:
    queries = list(food_slot.get("research_queries", []))
    queries.extend(
        [
            "peer reviewed low labor staple crop production small community yield water energy",
            "controlled environment agriculture labor productivity edible yield study",
            "passive greenhouse winter vegetable yield low energy peer reviewed",
            "food preservation storage loss reduction small community study",
        ]
    )
    return sorted(set(queries))


def _registry_slot(module_registry: dict[str, Any] | None, slot_id: str) -> dict[str, Any]:
    if not module_registry:
        return {}
    return next((slot for slot in module_registry.get("slots", []) if slot.get("id") == slot_id), {})


def _research_next_actions(needs: list[dict[str, Any]]) -> list[str]:
    if not needs:
        return ["No research need was generated from the current plan and simulation."]
    return [
        "Use the highest-priority ResearchNeed as a planning-phase evidence and module-interface brief.",
        "Convert promising papers into TechnologyModule drafts with citations, performance statistics, limitations, and uncertainty.",
        "Run scalability gates before allowing any discovered module to affect optimization.",
    ]


def _dignity_floor_gate(module: dict[str, Any]) -> dict[str, Any]:
    effects = module.get("modeled_impacts", {}).get("direct_resource_effects", {})
    regressions = [
        f"{resource} direct effect {value}"
        for resource, value in effects.items()
        if resource in {"food_servings_per_day", "water_liters_per_day", "energy_kwh_per_day"} and float(value or 0) < 0
    ]
    return _gate(
        "dignity_floor_protection",
        "fail" if regressions else "pass",
        regressions or ["No direct negative food, water, or critical energy effect is declared."],
        ["Reject or rewrite modules that reduce dignity-floor resources."] if regressions else [],
    )


def _evidence_gate(module: dict[str, Any]) -> dict[str, Any]:
    sources = module.get("source_evidence", [])
    stats = module.get("performance_statistics", [])
    status = "pass" if sources and stats and module.get("status") in {"evidence_seed", "candidate", "validated"} else "fail"
    return _gate(
        "evidence_traceability",
        status,
        [f"{len(sources)} source(s) and {len(stats)} performance statistic(s) are declared."],
        [] if status == "pass" else ["Add cited source evidence and extracted performance statistics before scalability review."],
    )


def _interface_gate(module: dict[str, Any], module_registry: dict[str, Any] | None) -> dict[str, Any]:
    target_slots = module.get("applicability", {}).get("target_slots", [])
    missing = []
    for slot_id in target_slots:
        slot = _registry_slot(module_registry, slot_id)
        missing.extend(_missing_required_interfaces(module, slot))
    if not target_slots:
        missing.append("No target module slot is declared.")
    status = "pass" if not missing else "fail"
    return _gate(
        "scalable_interface",
        status,
        ["Required slot interfaces are present."] if not missing else sorted(set(missing)),
        [] if status == "pass" else ["Add adapter fields for edible output, labor, water, energy, failure sensitivity, and other slot interfaces."],
    )


def _missing_required_interfaces(module: dict[str, Any], slot: dict[str, Any]) -> list[str]:
    impacts = module.get("modeled_impacts", {})
    direct = impacts.get("direct_resource_effects", {})
    modifiers = impacts.get("candidate_modifiers", {})
    missing = []
    for interface in slot.get("required_interfaces", []):
        if interface.startswith("resource_effects."):
            key = interface.split(".", 1)[1]
            if key not in direct:
                missing.append(interface)
        elif interface in {"edible_servings_per_day", "water_liters_per_serving", "labor_hours_per_week", "crop_failure_sensitivity"}:
            if interface not in direct and interface not in modifiers:
                missing.append(interface)
        elif interface not in direct and interface not in modifiers:
            missing.append(interface)
    return missing


def _labor_gate(module: dict[str, Any]) -> dict[str, Any]:
    impacts = module.get("modeled_impacts", {})
    direct = impacts.get("direct_resource_effects", {})
    modifiers = impacts.get("candidate_modifiers", {})
    has_labor = "labor_hours_per_week" in direct or "labor_hours_per_week" in modifiers or "maintenance_labor_hours" in direct or "maintenance_labor_hours" in modifiers
    return _gate(
        "labor_visibility",
        "pass" if has_labor else "fail",
        ["Labor burden interface is declared."] if has_labor else ["No labor-hours interface is declared."],
        [] if has_labor else ["Declare build, operating, maintenance, and automation-supervision labor before scaling."],
    )


def _automation_gate(module: dict[str, Any]) -> dict[str, Any]:
    requirements = " ".join(module.get("integration_requirements", [])).lower()
    unknowns = " ".join(module.get("unknowns", [])).lower()
    mentions_automation = "automation" in requirements or "automation" in unknowns or "robot" in requirements or "robot" in unknowns
    return _gate(
        "automation_dependency",
        "warn" if mentions_automation else "pass",
        ["Automation dependency is not declared as required."] if not mentions_automation else ["Automation or robotics dependency is mentioned and needs explicit reliability/labor modeling."],
        [] if not mentions_automation else ["Add automation uptime, repair, spare parts, fallback mode, and supervision labor before promotion."],
    )


def _transferability_gate(module: dict[str, Any]) -> dict[str, Any]:
    unknowns = module.get("unknowns", [])
    exclusions = module.get("applicability", {}).get("excludes", [])
    status = "warn" if unknowns or exclusions else "pass"
    return _gate(
        "context_transferability",
        status,
        [f"{len(unknowns)} unknown(s) and {len(exclusions)} exclusion(s) are declared."],
        [] if status == "pass" else ["Keep module in evidence-seed status until crop, climate, scale, legal, and operational fit are modeled."],
    )


def _scaling_targets(compiled_plan: dict[str, Any], module_registry: dict[str, Any] | None) -> list[dict[str, Any]]:
    population = int(compiled_plan.get("site_summary", {}).get("population_target", 0))
    targets = module_registry.get("scaling_policy", {}).get("required_targets", []) if module_registry else []
    if not targets:
        targets = [population] if population else [5, 10, 25, 50]
    return [
        {
            "people": int(target),
            "relative_to_current_population": round(int(target) / population, 3) if population else 0,
            "requires_explicit_resource_scaling": True,
            "provisional": True,
        }
        for target in targets
    ]


def _gate(identifier: str, status: str, evidence: list[str], remediation: list[str]) -> dict[str, Any]:
    return {
        "id": identifier,
        "status": status,
        "evidence": evidence,
        "remediation": remediation,
        "provisional": True,
    }


def _gate_status(gate_results: list[dict[str, Any]]) -> str:
    if any(result["status"] == "fail" for result in gate_results):
        return "fail"
    if any(result["status"] == "warn" for result in gate_results):
        return "warn"
    return "pass"


def _scalability_next_actions(gate_results: list[dict[str, Any]]) -> list[str]:
    failed = [result for result in gate_results if result["status"] == "fail"]
    warned = [result for result in gate_results if result["status"] == "warn"]
    if failed:
        return [
            "Do not let this module alter optimization yet.",
            "Resolve failed scalability gates by adding adapter models and explicit labor/resource interfaces.",
        ]
    if warned:
        return [
            "Keep this module provisional and run stress replays before ranking it against defaults.",
            "Resolve warning gates before any promotion beyond simulation.",
        ]
    return ["Module can enter provisional simulation comparison against the default posture."]
