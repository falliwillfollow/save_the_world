from __future__ import annotations

from typing import Any


SUBSYSTEM_ORDER = ["water", "energy", "roles", "nutrition", "scenario", "simulation", "gates"]


def generate_redesign(audit_report: dict[str, Any], compiled_plan: dict[str, Any]) -> dict[str, Any]:
    blockers = _blockers_by_subsystem(audit_report)
    candidates = _candidates(blockers, audit_report)
    priority_order = [candidate["id"] for candidate in sorted(candidates, key=lambda item: item["priority"])]

    return {
        "kind": "RedesignReport",
        "id": f"{compiled_plan['id']}_redesign",
        "compiled_plan": compiled_plan["id"],
        "audit_report": audit_report["id"],
        "generated_by": "ciac.redesign.v0",
        "provisional": True,
        "status": "ready_for_iteration" if candidates else "draft",
        "blockers_by_subsystem": blockers,
        "redesign_candidates": sorted(candidates, key=lambda item: item["priority"]),
        "priority_order": priority_order,
        "next_actions": _next_actions(priority_order),
        "unknowns": [
            "Redesign candidates are planning proposals, not engineering approval or legal compliance.",
            "Expected effects must be verified by editing source plans and rerunning compile, reports, scenarios, and audit.",
            "Candidates intentionally prefer auditable changes over aesthetic or visualization work.",
        ],
    }


def _blockers_by_subsystem(audit_report: dict[str, Any]) -> dict[str, list[str]]:
    grouped: dict[str, list[str]] = {subsystem: [] for subsystem in SUBSYSTEM_ORDER}
    evidence = (
        audit_report.get("survival_critical_blockers", [])
        + audit_report.get("noncritical_warnings", [])
        + audit_report.get("top_risks", [])
    )
    for item in evidence:
        subsystem = _subsystem_for(item)
        grouped.setdefault(subsystem, []).append(item)
    return {key: sorted(set(values)) for key, values in grouped.items() if values}


def _subsystem_for(item: str) -> str:
    prefix = item.split(":", 1)[0]
    if prefix in SUBSYSTEM_ORDER:
        return prefix
    if prefix == "scenario":
        return "scenario"
    for subsystem in SUBSYSTEM_ORDER:
        if subsystem in item.lower():
            return subsystem
    return "other"


def _candidates(blockers: dict[str, list[str]], audit_report: dict[str, Any]) -> list[dict[str, Any]]:
    candidates: list[dict[str, Any]] = []
    if "water" in blockers or _mentions(audit_report, "drought"):
        candidates.extend(_water_candidates())
    if "energy" in blockers or _mentions(audit_report, "outage"):
        candidates.extend(_energy_candidates())
    if "roles" in blockers or _mentions(audit_report, "steward"):
        candidates.extend(_role_candidates())
    if "nutrition" in blockers or _mentions(audit_report, "food"):
        candidates.extend(_nutrition_candidates())
    if "scenario" in blockers:
        candidates.extend(_scenario_candidates())
    return _renumber(candidates)


def _water_candidates() -> list[dict[str, Any]]:
    return [
        {
            "id": "water_storage_and_drought_reserve",
            "subsystem": "water",
            "priority": 10,
            "title": "Increase water storage and drought reserve",
            "proposal": "Raise potable and nonpotable storage and increase drought demand reduction so the 90-day drought balance no longer goes negative.",
            "expected_effect": [
                "Improves drought water balance.",
                "Extends emergency reserve days.",
                "Reduces water_gate failure risk in drought scenarios.",
            ],
            "tradeoffs": [
                "Higher tank cost and footprint.",
                "More maintenance and freeze/contamination detailing.",
                "Demand reduction may affect comfort if not paired with efficient fixtures.",
            ],
            "new_assumptions": [
                "Additional storage space is physically and legally available.",
                "Residents can accept higher drought conservation targets.",
            ],
            "files_to_edit": ["water_plans/micro_commons_basic.yaml", "scenarios/drought.yaml"],
            "acceptance_criteria": [
                "ciac water returns non-fail status for the updated water plan.",
                "drought_balance.status is not fail.",
                "ciac scenario drought no longer fails water_gate.",
            ],
        },
        {
            "id": "water_verified_backup_source",
            "subsystem": "water",
            "priority": 20,
            "title": "Add verified backup water source",
            "proposal": "Add a contamination-available backup source or hauled-water/mutual-aid source with explicit yield and retesting workflow.",
            "expected_effect": [
                "Improves contamination fallback window.",
                "Reduces dependence on the primary well.",
                "Makes water contamination response auditable.",
            ],
            "tradeoffs": [
                "May introduce external dependency.",
                "Requires storage, contracts, testing, and access logistics.",
            ],
            "new_assumptions": [
                "A backup source or supplier is available within acceptable lead time.",
                "Backup water can be tested or treated before use.",
            ],
            "files_to_edit": ["water_plans/micro_commons_basic.yaml", "scenarios/water_contamination.yaml"],
            "acceptance_criteria": [
                "contamination_response.status is pass or warn with no missing backup sources.",
                "potable_storage_fallback_days meets target.",
                "water contamination scenario no longer fails water_gate.",
            ],
        },
    ]


def _energy_candidates() -> list[dict[str, Any]]:
    return [
        {
            "id": "energy_battery_and_backup",
            "subsystem": "energy",
            "priority": 30,
            "title": "Increase battery and secure backup energy",
            "proposal": "Increase usable battery capacity and add backup generation or mutual-aid charging for the modeled outage and cloudy-weather windows.",
            "expected_effect": [
                "Raises critical-load autonomy toward 72-hour outage target.",
                "Reduces cloudy-weather backup gap.",
                "Protects refrigeration, water pumping, communications, and clinic loads.",
            ],
            "tradeoffs": [
                "Higher cost, embodied carbon, and battery maintenance.",
                "Backup generation may add fuel dependency or noise.",
            ],
            "new_assumptions": [
                "Battery expansion is electrically feasible.",
                "Qualified review is available before any real installation.",
                "Backup energy source can be maintained and safely operated.",
            ],
            "files_to_edit": ["energy_plans/micro_commons_basic.yaml", "scenarios/energy_outage.yaml"],
            "acceptance_criteria": [
                "critical_load_autonomy.status is pass.",
                "outage_survival.status is pass.",
                "backup_energy_gap.status is not fail.",
            ],
        },
        {
            "id": "energy_critical_load_reduction",
            "subsystem": "energy",
            "priority": 40,
            "title": "Reduce critical-load demand",
            "proposal": "Review each critical load and reduce daily kWh through efficient equipment, thermal storage, manual fallback, or stricter emergency load shedding.",
            "expected_effect": [
                "Improves autonomy without only adding hardware.",
                "Reduces outage and cloudy-weather failure risk.",
            ],
            "tradeoffs": [
                "May reduce comfort or convenience during emergency mode.",
                "Manual fallback can shift burden into labor and role schedules.",
            ],
            "new_assumptions": [
                "Lower-demand equipment or workflows are acceptable to residents.",
            ],
            "files_to_edit": ["energy_plans/micro_commons_basic.yaml", "role_plans/micro_commons_basic.yaml"],
            "acceptance_criteria": [
                "critical_load_kwh_per_day decreases.",
                "ciac energy returns improved autonomy hours.",
                "ciac roles does not gain new overload failures from manual fallback work.",
            ],
        },
    ]


def _role_candidates() -> list[dict[str, Any]]:
    return [
        {
            "id": "roles_train_second_energy_steward",
            "subsystem": "roles",
            "priority": 50,
            "title": "Train second energy steward",
            "proposal": "Add at least one more participant eligible for energy_steward with energy_ops and electrical_awareness skills.",
            "expected_effect": [
                "Removes energy_steward single point of failure.",
                "Improves backup coverage for a survival-critical system.",
            ],
            "tradeoffs": [
                "Training takes time and may require external qualified support.",
                "More responsibility may increase load for another participant.",
            ],
            "new_assumptions": [
                "A participant consents to training and has capacity.",
                "Training materials and qualified escalation path exist.",
            ],
            "files_to_edit": ["role_plans/micro_commons_basic.yaml"],
            "acceptance_criteria": [
                "energy_steward is absent from single_point_of_failure_roles.",
                "energy_steward has a named backup.",
                "ciac roles no longer fails backup_coverage for energy_steward.",
            ],
        },
        {
            "id": "roles_rebalance_care_and_fairness",
            "subsystem": "roles",
            "priority": 60,
            "title": "Rebalance care-loaded participants",
            "proposal": "Adjust assignments, care allowance, and eligible backups so residents with high care work are not overloaded or invisible in labor accounting.",
            "expected_effect": [
                "Improves fairness score.",
                "Reduces burnout warnings.",
                "Makes care work visible in governance evidence.",
            ],
            "tradeoffs": [
                "May require lowering optional work or adding participants.",
                "Could reveal that infrastructure maintenance burden is too high for current staffing.",
            ],
            "new_assumptions": [
                "Care work declarations are accurate enough for planning.",
                "Residents consent to revised rotation rules.",
            ],
            "files_to_edit": ["role_plans/micro_commons_basic.yaml", "patterns/*.yaml"],
            "acceptance_criteria": [
                "overloaded_residents is empty.",
                "fairness.status is not fail.",
                "care_work_accounting.status is not fail.",
            ],
        },
    ]


def _nutrition_candidates() -> list[dict[str, Any]]:
    return [
        {
            "id": "food_local_share_and_staple_dependency",
            "subsystem": "nutrition",
            "priority": 70,
            "title": "Clarify local food share and staple dependency",
            "proposal": "Either raise local calorie production or explicitly model external staples as a survival-critical dependency with storage and procurement contracts.",
            "expected_effect": [
                "Turns vague food warnings into an auditable dependency.",
                "Improves local food percentage or makes external reliance explicit.",
            ],
            "tradeoffs": [
                "More local production increases land, water, labor, and storage burden.",
                "External staples preserve realism but reduce autonomy.",
            ],
            "new_assumptions": [
                "Staple suppliers or crop plans can be documented.",
                "Nutrition goals remain provisional until reviewed.",
            ],
            "files_to_edit": ["food_plans/micro_commons_basic.yaml", "water_plans/micro_commons_basic.yaml", "role_plans/micro_commons_basic.yaml"],
            "acceptance_criteria": [
                "local_food.status is pass or external dependency is explicitly accepted as a blocker-free design choice.",
                "stored_calorie_days remains at or above target.",
                "ciac nutrition does not fail calorie or protein targets.",
            ],
        }
    ]


def _scenario_candidates() -> list[dict[str, Any]]:
    return [
        {
            "id": "scenario_response_sops",
            "subsystem": "scenario",
            "priority": 80,
            "title": "Add scenario response procedures",
            "proposal": "Define standard operating procedures for drought, water contamination, and energy outage response before adding visual-world work.",
            "expected_effect": [
                "Reduces scenario ambiguity.",
                "Links emergency tasks to roles, storage, and backup resources.",
            ],
            "tradeoffs": [
                "More procedural overhead.",
                "May reveal additional training and inventory requirements.",
            ],
            "new_assumptions": [
                "Residents can review and practice emergency procedures.",
            ],
            "files_to_edit": ["scenarios/*.yaml", "role_plans/micro_commons_basic.yaml"],
            "acceptance_criteria": [
                "Scenario reports include fewer survival-critical gate failures.",
                "Emergency tasks do not create role overload.",
                "Audit top risks shrink after rerun.",
            ],
        }
    ]


def _renumber(candidates: list[dict[str, Any]]) -> list[dict[str, Any]]:
    ordered = sorted(candidates, key=lambda item: item["priority"])
    for index, candidate in enumerate(ordered, start=1):
        candidate["priority"] = index
    return ordered


def _mentions(audit_report: dict[str, Any], text: str) -> bool:
    haystack = " ".join(
        audit_report.get("survival_critical_blockers", [])
        + audit_report.get("noncritical_warnings", [])
        + audit_report.get("top_risks", [])
        + audit_report.get("required_redesigns", [])
    ).lower()
    return text.lower() in haystack


def _next_actions(priority_order: list[str]) -> list[str]:
    if not priority_order:
        return ["No redesign candidates were generated; add more audit evidence or subsystem reports."]
    return [
        f"Implement candidate {priority_order[0]} first.",
        "Rerun compile and all affected subsystem reports.",
        "Rerun ciac audit and compare blocker count before moving to visualization or Unreal work.",
    ]

