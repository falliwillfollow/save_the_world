from __future__ import annotations

import math
from typing import Any


PROVISIONALITY_NOTE = (
    "This is a provisional civic simulation. It visualizes model assumptions and stress tests. It does not certify "
    "real-world safety, legality, affordability, engineering, public health, accessibility, resident consent, or buildability."
)

VILLAGE_BLOCK_PREFERRED = 80
VILLAGE_BLOCK_MAX = 150


MODULE_DEFS = [
    ("housing.dignified_village_block.v0_1", "dignified_village_block", "floor_systems", "housing"),
    ("food.hybrid_food_commons.v0_1", "hybrid_food_commons", "floor_systems", "food"),
    ("food.protein_commons_supplement.v0_1", "protein_commons_supplement", "capacity_systems", "food"),
    ("water.resilient_water_commons.v0_1", "resilient_water_commons", "floor_systems", "water"),
    ("energy.critical_load_energy_commons.v0_1", "critical_load_energy_commons", "floor_systems", "energy"),
    ("sanitation.hygienic_circular_commons.v0_1", "hygienic_circular_commons", "floor_systems", "sanitation"),
    ("maintenance.maintainable_commons_spine.v0_1", "maintainable_commons_spine", "operating_systems", "maintenance"),
    ("governance.commons_stewardship_protocol.v0_1", "commons_stewardship_protocol", "meta_systems", "governance"),
    ("labor_time.life_burden_ledger.v0_1", "life_burden_ledger", "meta_systems", "labor_time"),
    ("legal_land_finance.anti_speculative_civic_floor.v0_1", "anti_speculative_civic_floor", "meta_systems", "legal_land_finance"),
    ("mobility_access.pedestrian_first_access_commons.v0_1", "pedestrian_first_access_commons", "operating_systems", "mobility"),
    ("education_skill.civic_skill_lattice.v0_1", "civic_skill_lattice", "operating_systems", "education"),
    ("social_cultural_commons.belonging_without_coercion.v0_1", "belonging_without_coercion_commons", "operating_systems", "social"),
    ("risk_resilience.graceful_degradation_engine.v0_1", "graceful_degradation_engine", "meta_systems", "risk"),
]

STRUCTURE_MODULE_TARGETS = {
    "care_health": "structure_care_room",
    "risk_resilience": "structure_care_room",
    "social_cultural": "structure_social_cultural",
    "mobility_access": "zone_mobility_loop",
    "labor_time": "structure_quiet_studio",
    "maintenance_repair": "structure_maintenance_shop",
    "maintenance": "structure_maintenance_shop",
    "education_skill": "structure_maintenance_shop",
    "food": "structure_food_commons",
    "water": "node_water_reserve",
    "water_public_health": "node_water_reserve",
    "governance": "structure_common_house",
    "governance_anticapture": "structure_common_house",
}


def build_world_manifest(
    runtime_bundle: dict[str, Any],
    population: int | None = None,
    runtime_bundle_path: str | None = None,
    world_id: str | None = None,
) -> dict[str, Any]:
    resolved_population = int(population or _runtime_population(runtime_bundle) or 80)
    scale = infer_scale(resolved_population)
    modules = build_modules(runtime_bundle)
    layout = build_proxy_layout(resolved_population, scale, modules)
    zones = build_zones(layout, runtime_bundle)
    structures = build_structures(layout, runtime_bundle)
    paths = build_paths(layout, runtime_bundle)
    infrastructure_nodes = build_infrastructure_nodes(layout, runtime_bundle)
    residents = build_resident_archetypes(resolved_population)
    daily_events = build_daily_events(residents, layout, runtime_bundle)
    scenario_states = build_scenario_states(runtime_bundle)
    overlays = build_overlays(runtime_bundle)
    resource_telemetry = build_resource_telemetry(runtime_bundle)
    evidence_cards = build_evidence_cards(
        {
            "zones": zones,
            "structures": structures,
            "infrastructure_nodes": infrastructure_nodes,
            "paths": paths,
        },
        runtime_bundle,
    )
    failures = sorted(set(runtime_bundle.get("capabilities", {}).get("failures", [])))
    warnings = sorted(set([PROVISIONALITY_NOTE, *runtime_bundle.get("manifest", {}).get("warnings", []), *runtime_bundle.get("capabilities", {}).get("warnings", [])]))
    return {
        "kind": "CivicFloorWorldManifest",
        "version": "v0",
        "world_id": world_id or f"civic_floor_{resolved_population}_v0",
        "generated_at": None,
        "source": {
            "runtime_bundle_path": runtime_bundle_path,
            "simulation_id": runtime_bundle.get("manifest", {}).get("simulation_run"),
            "profile_id": runtime_bundle.get("manifest", {}).get("compiled_plan"),
            "provisional": True,
        },
        "population": {
            "residents": resolved_population,
            "households": max(1, math.ceil(resolved_population / 2)),
            "active_scale_slider_value": resolved_population,
        },
        "scale": scale,
        "modules": modules,
        "zones": zones,
        "structures": structures,
        "paths": paths,
        "infrastructure_nodes": infrastructure_nodes,
        "residents": residents,
        "daily_events": daily_events,
        "scenario_states": scenario_states,
        "overlays": overlays,
        "resource_telemetry": resource_telemetry,
        "evidence_cards": evidence_cards,
        "warnings": warnings,
        "failures": failures,
        "unknowns": sorted(set([*runtime_bundle.get("unknowns", []), "Proxy geometry is deterministic and symbolic; it is not a site plan or architectural design."])),
    }


def infer_scale(population: int) -> dict[str, Any]:
    people = max(1, int(population))
    village_blocks = max(1, math.ceil(people / VILLAGE_BLOCK_MAX))
    topology_counts = _topology_counts(people, village_blocks)
    if people <= 20:
        return {
            "scale_class": "micro_commons",
            "recommended_unit_size": 12,
            "implied_village_blocks": 1,
            "scaling_mode": "seed",
            "active_layers": ["micro_commons"],
            "topology_policy_id": "ciac_scaling_policy_v0",
            "topology_counts": topology_counts,
        }
    if people <= 150:
        return {
            "scale_class": "village_block",
            "recommended_unit_size": VILLAGE_BLOCK_PREFERRED,
            "implied_village_blocks": 1,
            "scaling_mode": "single_node",
            "active_layers": ["village_block"],
            "topology_policy_id": "ciac_scaling_policy_v0",
            "topology_counts": topology_counts,
        }
    if people <= 750:
        return {
            "scale_class": "multi_block_district",
            "recommended_unit_size": VILLAGE_BLOCK_PREFERRED,
            "implied_village_blocks": village_blocks,
            "scaling_mode": "mixed_topology",
            "active_layers": ["village_block", "district_capability"],
            "topology_policy_id": "ciac_scaling_policy_v0",
            "topology_counts": topology_counts,
        }
    if people <= 1500:
        return {
            "scale_class": "town_city_layer",
            "recommended_unit_size": VILLAGE_BLOCK_PREFERRED,
            "implied_village_blocks": village_blocks,
            "scaling_mode": "federated_layers",
            "active_layers": ["village_block", "district_capability", "town_city_capability"],
            "topology_policy_id": "ciac_scaling_policy_v0",
            "topology_counts": topology_counts,
        }
    return {
        "scale_class": "regional_membrane",
        "recommended_unit_size": VILLAGE_BLOCK_PREFERRED,
        "implied_village_blocks": village_blocks,
        "scaling_mode": "federated_layers",
        "active_layers": ["village_block", "district_capability", "town_city_capability", "regional_membrane"],
        "topology_policy_id": "ciac_scaling_policy_v0",
        "topology_counts": topology_counts,
    }


def _topology_counts(people: int, village_blocks: int) -> dict[str, int]:
    return {
        "village_blocks": village_blocks,
        "residential_pods": max(1, math.ceil(people / 20)),
        "common_houses": max(1, math.ceil(people / 100)),
        "food_commons": max(1, math.ceil(people / 100)),
        "protein_commons": max(1, math.ceil(people / 150)),
        "care_rooms": max(1, math.ceil(people / 100)),
        "quiet_rooms": max(village_blocks, math.ceil(people / 80)),
        "water_reserves": village_blocks,
        "sanitation_cells": village_blocks,
        "local_tool_caches": village_blocks,
    }


def build_modules(runtime_bundle: dict[str, Any]) -> list[dict[str, Any]]:
    connected_patterns = {system.get("pattern_id") for system in runtime_bundle.get("systems", [])}
    modules = []
    known_patterns = set()
    for module_id, pattern_id, tier, domain in MODULE_DEFS:
        known_patterns.add(pattern_id)
        connected = pattern_id in connected_patterns
        modules.append(
            {
                "module_id": module_id,
                "pattern_id": pattern_id,
                "tier": tier,
                "domain": domain,
                "status": "simulation_connected" if connected else "contract_defined",
                "review_status": "review_required",
                "label": _title(pattern_id),
                "summary": f"{_title(domain)} model layer.",
                "placement_target_id": _placement_target_for_domain(domain),
                "provisional": True,
            }
        )
    for system in runtime_bundle.get("systems", []):
        pattern_id = str(system.get("pattern_id", ""))
        if not pattern_id or pattern_id in known_patterns:
            continue
        domain = _domain_for_pattern(pattern_id, system)
        modules.append(
            {
                "module_id": _module_id(domain, pattern_id),
                "pattern_id": pattern_id,
                "tier": _tier_for_domain(domain),
                "domain": domain,
                "status": "simulation_connected",
                "review_status": "review_required",
                "label": _title(pattern_id),
                "summary": _module_summary(domain, pattern_id),
                "placement_target_id": _placement_target_for_domain(domain),
                "critical_resources": system.get("critical_resources", []),
                "failure_modes": system.get("failure_modes", []),
                "active_failure_count": system.get("active_failure_count", 0),
                "provisional": True,
            }
        )
    return modules


def build_proxy_layout(population: int, scale: dict[str, Any], modules: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "population": int(population),
        "scale": scale,
        "center": _v(0, 0, 0),
        "positions": {
            "common_house": _v(0, 0, 0),
            "food_commons": _v(0, 0, 15),
            "protein_commons": _v(16, 0, 20),
            "care_room": _v(-14, 0, 0),
            "social_cultural": _v(14, 0, 0),
            "maintenance_shop": _v(20, 0, -20),
            "water_node": _v(-24, 0, 18),
            "energy_node": _v(0, 0, -24),
            "sanitation_node": _v(26, 0, -2),
            "garden": _v(0, 0, 28),
            "pod_1": _v(-24, 0, 10),
            "pod_2": _v(24, 0, 10),
            "pod_3": _v(-24, 0, -12),
            "pod_4": _v(24, 0, -12),
            "quiet_studio": _v(-12, 0, -18),
            "west_walk": _v(-18, 0, 0),
            "east_walk": _v(18, 0, 0),
            "north_walk": _v(0, 0, 18),
            "south_walk": _v(0, 0, -18),
        },
    }


def build_zones(layout: dict[str, Any], runtime_bundle: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        _zone("zone_common_core", "common_core", "Common Core", _v(0, -0.03, 0), _v(32, 0.05, 22), "common_core", ["housing.dignified_village_block.v0_1", "governance.commons_stewardship_protocol.v0_1"], "evidence_common_core"),
        _zone("zone_residential_ring", "residential", "Residential Ring", _v(0, -0.04, 0), _v(62, 0.05, 42), "housing", ["housing.dignified_village_block.v0_1"], "evidence_residential_pods"),
        _zone("zone_food_garden", "food", "Food Garden", _v(0, -0.05, 25), _v(42, 0.05, 22), "food", ["food.hybrid_food_commons.v0_1", "food.protein_commons_supplement.v0_1"], "evidence_food_commons"),
        _zone("zone_service_edge", "service_edge", "Service Edge", _v(4, -0.06, -20), _v(54, 0.05, 18), "service_edge", ["water.resilient_water_commons.v0_1", "energy.critical_load_energy_commons.v0_1", "sanitation.hygienic_circular_commons.v0_1"], "evidence_service_edge"),
        _zone("zone_mobility_loop", "mobility", "Mobility Loop", _v(0, -0.07, 0), _v(68, 0.04, 58), "mobility", ["mobility_access.pedestrian_first_access_commons.v0_1"], "evidence_primary_paths"),
    ]


def build_structures(layout: dict[str, Any], runtime_bundle: dict[str, Any]) -> list[dict[str, Any]]:
    positions = layout["positions"]
    module_refs_by_structure = _module_refs_by_structure(runtime_bundle)
    return [
        _structure("structure_common_house", "common_house", "Common House", positions["common_house"], _v(13, 4, 9), "proxy_common_house", _with_dynamic_refs(["housing.dignified_village_block.v0_1", "social_cultural_commons.belonging_without_coercion.v0_1", "governance.commons_stewardship_protocol.v0_1"], module_refs_by_structure, "structure_common_house"), ["food", "social", "governance"], "normal", "evidence_common_house", 18),
        _structure("structure_food_commons", "food_commons", "Hybrid Food Commons", positions["food_commons"], _v(12, 3.5, 7), "proxy_food_commons", _with_dynamic_refs(["food.hybrid_food_commons.v0_1"], module_refs_by_structure, "structure_food_commons"), ["food", "labor_time"], "normal", "evidence_food_commons", 10),
        _structure("structure_protein_commons", "protein_commons", "Protein Commons", positions["protein_commons"], _v(9, 3, 6), "proxy_protein_commons", _with_dynamic_refs(["food.protein_commons_supplement.v0_1"], module_refs_by_structure, "structure_protein_commons"), ["food"], "warning", "evidence_protein_commons", 3),
        _structure("structure_care_room", "care_room", "Care Room", positions["care_room"], _v(7, 3, 6), "proxy_care_room", _with_dynamic_refs(["risk_resilience.graceful_degradation_engine.v0_1"], module_refs_by_structure, "structure_care_room"), ["care", "risk_resilience"], _care_room_status(runtime_bundle), "evidence_care_room", 2),
        _structure("structure_social_cultural", "social_cultural", "Social Commons", positions["social_cultural"], _v(10, 3, 6), "proxy_social_cultural", _with_dynamic_refs(["social_cultural_commons.belonging_without_coercion.v0_1"], module_refs_by_structure, "structure_social_cultural"), ["social"], "normal", "evidence_social_cultural", 8),
        _structure("structure_maintenance_shop", "maintenance_shop", "Maintenance Shop", positions["maintenance_shop"], _v(11, 3, 7), "proxy_maintenance_shop", _with_dynamic_refs(["maintenance.maintainable_commons_spine.v0_1"], module_refs_by_structure, "structure_maintenance_shop"), ["maintenance"], "normal", "evidence_maintenance_shop", 3),
        _structure("structure_quiet_studio", "quiet_studio", "Quiet Studio", positions["quiet_studio"], _v(8, 3, 6), "proxy_quiet_studio", _with_dynamic_refs(["labor_time.life_burden_ledger.v0_1"], module_refs_by_structure, "structure_quiet_studio"), ["labor_time", "dignity_privacy"], "normal", "evidence_quiet_studio", 3),
        *[
            _structure(f"structure_residential_pod_{index}", "residential_pod", f"Residential Pod {index}", positions[f"pod_{index}"], _v(10, 3.2, 8), "proxy_residential_pod", ["housing.dignified_village_block.v0_1"], ["housing", "dignity_privacy"], "normal", "evidence_residential_pods", 12)
            for index in range(1, 5)
        ],
    ]


def build_paths(layout: dict[str, Any], runtime_bundle: dict[str, Any]) -> list[dict[str, Any]]:
    positions = layout["positions"]
    module_refs = ["mobility_access.pedestrian_first_access_commons.v0_1"]
    return [
        _path("path_primary_ring", "primary_access", "Residential Ring", [positions["pod_1"], positions["north_walk"], positions["pod_2"], positions["east_walk"], positions["pod_4"], positions["south_walk"], positions["pod_3"], positions["west_walk"], positions["pod_1"]], module_refs),
        _path("path_daily_spine", "primary_access", "Daily Life Spine", [positions["south_walk"], positions["common_house"], positions["food_commons"], positions["garden"]], module_refs),
        _path("path_common_services", "service", "Service Spine", [positions["water_node"], positions["common_house"], positions["energy_node"], positions["maintenance_shop"], positions["sanitation_node"]], module_refs),
        _path("path_care_quiet", "secondary_social", "Care + Quiet Link", [positions["care_room"], positions["common_house"], positions["quiet_studio"]], module_refs),
        _path("path_social_loop", "secondary_social", "Social Link", [positions["social_cultural"], positions["common_house"], positions["food_commons"], positions["protein_commons"]], module_refs),
    ]


def build_infrastructure_nodes(layout: dict[str, Any], runtime_bundle: dict[str, Any]) -> list[dict[str, Any]]:
    positions = layout["positions"]
    resources = runtime_bundle.get("timeline", {}).get("resource_balance", {})
    storage = runtime_bundle.get("timeline", {}).get("storage", {}).get("resources", {})
    module_refs_by_structure = _module_refs_by_structure(runtime_bundle)
    return [
        _node("node_water_reserve", "water", "Water Source + Reserve", positions["water_node"], "proxy_water_node", _with_dynamic_refs(["water.resilient_water_commons.v0_1"], module_refs_by_structure, "node_water_reserve"), {"daily_net": resources.get("water_liters", {}).get("net_per_day", 0), "stored": storage.get("water_liters", {}).get("ending_total", 0), "status": resources.get("water_liters", {}).get("status", "provisional")}, "evidence_water_node"),
        _node("node_solar_battery", "energy", "Solar + Critical Battery", positions["energy_node"], "proxy_solar_battery", ["energy.critical_load_energy_commons.v0_1"], {"daily_net": resources.get("energy_kwh", {}).get("net_per_day", 0), "stored": storage.get("energy_kwh", {}).get("ending_total", 0), "critical_load_runtime_hours": 72, "status": resources.get("energy_kwh", {}).get("status", "provisional")}, "evidence_solar_battery"),
        _node("node_sanitation_waste", "sanitation", "Sanitation + Waste", positions["sanitation_node"], "proxy_sanitation_node", ["sanitation.hygienic_circular_commons.v0_1"], {"status": resources.get("sanitation_capacity", {}).get("status", "provisional")}, "evidence_sanitation_node"),
        _node("node_risk_governance", "risk", "Risk + Governance Board", _v(-6, 0, -8), "proxy_risk_board", ["governance.commons_stewardship_protocol.v0_1", "risk_resilience.graceful_degradation_engine.v0_1"], {"capability_status": _capability_status(runtime_bundle)}, "evidence_risk_governance"),
    ]


def build_resident_archetypes(population: int) -> list[dict[str, Any]]:
    archetypes = [
        ("artist", "Artist", "structure_residential_pod_1", -26, 0, 12),
        ("elder", "Elder", "structure_residential_pod_1", -22, 0, 8),
        ("caregiver", "Caregiver", "structure_residential_pod_2", 22, 0, 12),
        ("student", "Apprentice", "structure_residential_pod_2", 26, 0, 8),
        ("maintenance_steward", "Maintenance Steward", "structure_residential_pod_3", -26, 0, -14),
        ("food_steward", "Food Steward", "structure_residential_pod_4", 22, 0, -10),
        ("researcher", "Researcher", "structure_residential_pod_3", -22, 0, -10),
        ("child", "Child", "structure_residential_pod_2", 27, 0, 14),
        ("governance_steward", "Governance Steward", "structure_residential_pod_1", -20, 0, 12),
        ("visitor", "Visitor", "structure_common_house", 5, 0, 8),
        ("water_energy_steward", "Water/Energy Steward", "structure_residential_pod_4", 26, 0, -14),
        ("resting_resident", "Resting Resident", "structure_residential_pod_3", -20, 0, -14),
    ]
    return [
        {
            "id": f"resident_{archetype}_{index:02d}",
            "archetype": archetype,
            "label": label,
            "home_structure_id": home,
            "daily_profile_id": f"day_{archetype}_balanced",
            "privacy": "archetype_only",
            "position": _v(x, y, z),
        }
        for index, (archetype, label, home, x, y, z) in enumerate(archetypes, start=1)
    ]


def build_daily_events(residents: list[dict[str, Any]], layout: dict[str, Any], runtime_bundle: dict[str, Any]) -> list[dict[str, Any]]:
    plan = [
        ("artist", "10:00", 120, "passion_time", "Studio practice", "structure_quiet_studio", ["labor_time.life_burden_ledger.v0_1"], "studio"),
        ("elder", "11:30", 60, "social", "Low-pressure common meal", "structure_common_house", ["social_cultural_commons.belonging_without_coercion.v0_1"], "meal"),
        ("caregiver", "08:30", 90, "care", "Care continuity check", "structure_care_room", ["risk_resilience.graceful_degradation_engine.v0_1"], "care"),
        ("student", "14:00", 90, "learning", "Skill lattice practice", "structure_maintenance_shop", ["education_skill.civic_skill_lattice.v0_1"], "learn"),
        ("maintenance_steward", "09:00", 75, "maintenance", "Asset registry round", "structure_maintenance_shop", ["maintenance.maintainable_commons_spine.v0_1"], "tool"),
        ("food_steward", "09:30", 90, "commons_labor", "Garden commons shift", "structure_food_commons", ["food.hybrid_food_commons.v0_1"], "garden"),
        ("researcher", "15:00", 120, "passion_time", "Evidence review", "structure_quiet_studio", ["risk_resilience.graceful_degradation_engine.v0_1"], "research"),
        ("child", "16:00", 45, "rest", "Protected play/rest", "structure_social_cultural", ["social_cultural_commons.belonging_without_coercion.v0_1"], "play"),
        ("governance_steward", "17:30", 45, "governance", "Decision log review", "structure_common_house", ["governance.commons_stewardship_protocol.v0_1"], "governance"),
        ("water_energy_steward", "07:45", 45, "maintenance", "Water and energy check", "node_solar_battery", ["water.resilient_water_commons.v0_1", "energy.critical_load_energy_commons.v0_1"], "energy"),
        ("resting_resident", "13:00", 120, "rest", "Quiet recovery block", "structure_quiet_studio", ["labor_time.life_burden_ledger.v0_1"], "rest"),
        ("visitor", "12:30", 60, "social", "Hosted introduction", "structure_common_house", ["social_cultural_commons.belonging_without_coercion.v0_1"], "visit"),
    ]
    by_archetype = {resident["archetype"]: resident for resident in residents}
    events = []
    for index, (archetype, time, duration, event_type, label, location, refs, icon) in enumerate(plan, start=1):
        resident = by_archetype.get(archetype)
        if not resident:
            continue
        events.append(
            {
                "id": f"event_{index:02d}_{archetype}",
                "resident_id": resident["id"],
                "time": time,
                "duration_minutes": duration,
                "type": event_type,
                "label": label,
                "location_id": location,
                "module_refs": refs,
                "visual": {
                    "animation_hint": "walk_work_idle",
                    "icon": icon,
                },
            }
        )
    return events


def build_resource_telemetry(runtime_bundle: dict[str, Any]) -> dict[str, Any]:
    resource_balance = runtime_bundle.get("timeline", {}).get("resource_balance", {})
    storage_resources = runtime_bundle.get("timeline", {}).get("storage", {}).get("resources", {})
    labor = runtime_bundle.get("timeline", {}).get("labor", {})
    horizon_days = max(1.0, _number(labor.get("weeks", 52.143)) * 7)
    resources = [
        _resource_metric("water", "Water", "liters", resource_balance.get("water_liters", {}), storage_resources.get("water_liters", {})),
        _resource_metric("food", "Food", "servings", resource_balance.get("food_servings", {}), storage_resources.get("food_servings", {})),
        _resource_metric("energy", "Energy", "kWh", resource_balance.get("energy_kwh", {}), storage_resources.get("energy_kwh", {})),
    ]
    return {
        "resources": resources,
        "horizon_days": _round(horizon_days),
        "labor": {
            "status": labor.get("status", "provisional"),
            "required_minutes_per_resident_per_day": _round(labor.get("modeled_required_commons_minutes_per_resident_per_day")),
            "available_hours_per_resident_per_day": _round(labor.get("modeled_available_commons_hours_per_resident_per_day")),
            "utilization": _round(labor.get("labor_utilization")),
            "maintenance_hours_per_week": _round(labor.get("estimated_maintenance_hours_per_week")),
            "care_hours_per_week": _round(labor.get("care_hours_per_week")),
            "basis": labor.get("involuntary_labor_basis"),
        },
        "provisional": True,
    }


def build_scenario_states(runtime_bundle: dict[str, Any]) -> list[dict[str, Any]]:
    states = [
        {
            "id": "scenario_normal_day",
            "label": "Normal Day",
            "type": "normal",
            "timeline": [
                {
                    "timestep": 0,
                    "label": "Normal operations",
                    "affected_objects": [],
                    "overlays": {},
                    "warnings": [],
                }
            ],
            "status": "modeled",
        }
    ]
    for scenario in runtime_bundle.get("scenarios", []):
        affected = _affected_objects_for_scenario(scenario)
        states.append(
            {
                "id": f"scenario_{scenario.get('scenario', 'stress')}",
                "label": _title(scenario.get("scenario", "Stress Scenario")),
                "type": scenario.get("scenario", "stress"),
                "timeline": [
                    {
                        "timestep": 0,
                        "label": "Scenario begins",
                        "affected_objects": affected,
                        "overlays": {
                            resource: {"status": scenario.get("resource_balance", {}).get(resource, {}).get("status", scenario.get("status", "modeled"))}
                            for resource in scenario.get("affected_resources", [])
                        },
                        "warnings": scenario.get("survival_critical_gate_failures", []),
                    }
                ],
                "status": "modeled",
            }
        )
    states.extend(
        [
            _placeholder_scenario("scenario_illness_wave", "Illness Wave", "illness_wave", ["structure_care_room", "structure_common_house"]),
            _placeholder_scenario("scenario_financial_shock", "Financial Shock", "financial_shock", ["node_risk_governance", "structure_common_house"]),
        ]
    )
    return states


def build_overlays(runtime_bundle: dict[str, Any]) -> dict[str, Any]:
    resource_balance = runtime_bundle.get("timeline", {}).get("resource_balance", {})
    domain_statuses = runtime_bundle.get("capabilities", {}).get("domain_statuses", {})
    overlays = {
        "food": _overlay("food", resource_balance.get("food_servings", {}).get("status", "provisional"), "Food commons and reserve state."),
        "water": _overlay("water", resource_balance.get("water_liters", {}).get("status", "provisional"), "Water source, storage, and recovery state."),
        "energy": _overlay("energy", resource_balance.get("energy_kwh", {}).get("status", "provisional"), "Critical-load supply and storage state."),
        "sanitation": _overlay("sanitation", resource_balance.get("sanitation_capacity", {}).get("status", "provisional"), "Sanitation and waste continuity."),
    }
    for domain in ("labor_time", "governance_anticapture", "care_health", "mobility_access", "legal_land_finance", "risk_resilience"):
        overlays[domain] = _overlay(domain, domain_statuses.get(domain, {}).get("status", "provisional"), f"{_title(domain)} capability status.")
    return overlays


def build_evidence_cards(world_objects: dict[str, list[dict[str, Any]]], runtime_bundle: dict[str, Any]) -> list[dict[str, Any]]:
    module_refs_by_structure = _module_refs_by_structure(runtime_bundle)
    care_modules = module_refs_by_structure.get("structure_care_room", [])
    water_modules = module_refs_by_structure.get("node_water_reserve", [])
    cards = {
        "evidence_common_core": _card("evidence_common_core", "Common Core", "Shared daily-life center for meals, governance, care access, and social contact.", ["housing.dignified_village_block.v0_1"], ["Common-core geometry is proxy only."], ["building code", "accessibility", "fire/life safety"]),
        "evidence_residential_pods": _card("evidence_residential_pods", "Residential Pods", "Archetypal private retreat pods around the common core.", ["housing.dignified_village_block.v0_1"], ["Pods represent privacy need, not a final plan."], ["housing code", "privacy review", "accessibility"]),
        "evidence_service_edge": _card("evidence_service_edge", "Service Edge", "Water, energy, sanitation, and maintenance sit on a visible service edge.", ["water.resilient_water_commons.v0_1", "energy.critical_load_energy_commons.v0_1"], ["Service adjacency is symbolic."], ["engineering", "public health", "electrical"]),
        "evidence_primary_paths": _card("evidence_primary_paths", "Primary Paths", "Accessible loop and radial paths make daily routes visible.", ["mobility_access.pedestrian_first_access_commons.v0_1"], ["Grades and surfaces are not surveyed."], ["civil engineering", "accessibility", "emergency access"]),
        "evidence_common_house": _card("evidence_common_house", "Common House", "Shared third place, dining, social, and governance interface.", ["housing.dignified_village_block.v0_1", "social_cultural_commons.belonging_without_coercion.v0_1"], ["Common space ratio is provisional."], ["building code", "accessibility", "fire/life safety"]),
        "evidence_food_commons": _card("evidence_food_commons", "Hybrid Food Commons", "Food hub for common meals, storage, garden coordination, and procurement visibility.", ["food.hybrid_food_commons.v0_1"], ["Food servings are not a complete nutrition plan."], ["food safety", "nutrition", "procurement"]),
        "evidence_protein_commons": _card("evidence_protein_commons", "Protein Commons", "Supplemental protein layer for duckweed, fermentation, or equivalent reviewed systems.", ["food.protein_commons_supplement.v0_1"], ["Acceptance, digestibility, inputs, and safety are provisional."], ["food safety", "nutrition", "resident acceptance"]),
        "evidence_care_room": _card("evidence_care_room", "Care Room", "Visible care continuity point without exposing personal health data.", _with_dynamic_refs(["risk_resilience.graceful_degradation_engine.v0_1"], {"structure_care_room": care_modules}, "structure_care_room"), ["Aggregate care state is modeled through modules attached to this room."], ["health", "privacy", "accessibility"]),
        "evidence_social_cultural": _card("evidence_social_cultural", "Social Commons", "Optional cultural and social space with opt-out protection.", ["social_cultural_commons.belonging_without_coercion.v0_1"], ["Belonging cannot be proven by a score."], ["resident consent", "safeguarding", "accessibility"]),
        "evidence_maintenance_shop": _card("evidence_maintenance_shop", "Maintenance Shop", "Work orders, tools, spares, and professional handoff made visible.", ["maintenance.maintainable_commons_spine.v0_1"], ["Maintenance labor is provisional."], ["worker safety", "tool safety", "professional review"]),
        "evidence_quiet_studio": _card("evidence_quiet_studio", "Quiet Studio", "Protected quiet, recovery, and passion-time space.", ["labor_time.life_burden_ledger.v0_1"], ["Passion time is represented, not guaranteed."], ["privacy", "labor fairness"]),
        "evidence_water_node": _card("evidence_water_node", "Water Node", "Water source, reserve, testing, and recovery assumptions.", _with_dynamic_refs(["water.resilient_water_commons.v0_1"], {"node_water_reserve": water_modules}, "node_water_reserve"), ["Water storage values are planning assumptions.", "Water public-health modules attach here as aggregate operating protocols, not as certification."], ["public health", "plumbing", "water testing"]),
        "evidence_solar_battery": _card("evidence_solar_battery", "Critical Load Energy Commons", "Solar and battery proxy for critical load protection.", ["energy.critical_load_energy_commons.v0_1"], ["Runtime hours are provisional."], ["electrical", "battery/fire", "interconnection"]),
        "evidence_sanitation_node": _card("evidence_sanitation_node", "Sanitation + Waste", "Conservative sanitation and waste continuity node.", ["sanitation.hygienic_circular_commons.v0_1"], ["Blackwater remains review-bound."], ["public health", "wastewater", "worker safety"]),
        "evidence_risk_governance": _card("evidence_risk_governance", "Risk + Governance Board", "Governance, anti-capture, dependency, and scenario visibility.", ["governance.commons_stewardship_protocol.v0_1", "risk_resilience.graceful_degradation_engine.v0_1"], ["Authority and trust are not automated."], ["legal", "governance", "resident consent"]),
    }
    used = {
        item.get("evidence_card_id")
        for group in world_objects.values()
        for item in group
        if item.get("evidence_card_id")
    }
    return [card for card_id, card in sorted(cards.items()) if card_id in used or card_id in {"evidence_protein_commons", "evidence_common_house", "evidence_solar_battery"}]


def _runtime_population(runtime_bundle: dict[str, Any]) -> int:
    return int(runtime_bundle.get("site", {}).get("summary", {}).get("population_target") or 0)


def _zone(identifier: str, zone_type: str, label: str, position: dict[str, float], size: dict[str, float], color_token: str, module_refs: list[str], evidence_card_id: str) -> dict[str, Any]:
    return {
        "id": identifier,
        "type": zone_type,
        "label": label,
        "position": position,
        "size": size,
        "color_token": color_token,
        "module_refs": module_refs,
        "evidence_card_id": evidence_card_id,
    }


def _structure(identifier: str, structure_type: str, label: str, position: dict[str, float], size: dict[str, float], asset_key: str, module_refs: list[str], systems: list[str], status: str, evidence_card_id: str, occupancy: int) -> dict[str, Any]:
    return {
        "id": identifier,
        "type": structure_type,
        "label": label,
        "position": position,
        "rotation": _v(0, 0, 0),
        "size": size,
        "asset_key": asset_key,
        "module_refs": module_refs,
        "systems": systems,
        "state": {
            "status": status,
            "occupancy": occupancy,
        },
        "evidence_card_id": evidence_card_id,
    }


def _path(identifier: str, path_type: str, label: str, points: list[dict[str, float]], module_refs: list[str]) -> dict[str, Any]:
    return {
        "id": identifier,
        "type": path_type,
        "label": label,
        "points": points,
        "accessibility": {
            "accessible": True,
            "grade_status": "review_required",
        },
        "module_refs": module_refs,
        "evidence_card_id": "evidence_primary_paths",
    }


def _node(identifier: str, node_type: str, label: str, position: dict[str, float], asset_key: str, module_refs: list[str], metrics: dict[str, Any], evidence_card_id: str) -> dict[str, Any]:
    return {
        "id": identifier,
        "type": node_type,
        "label": label,
        "position": position,
        "asset_key": asset_key,
        "module_refs": module_refs,
        "metrics": metrics,
        "evidence_card_id": evidence_card_id,
    }


def _card(identifier: str, title: str, summary: str, module_refs: list[str], assumptions: list[str], review_required: list[str]) -> dict[str, Any]:
    return {
        "id": identifier,
        "title": title,
        "summary": summary,
        "module_refs": module_refs,
        "assumptions": assumptions,
        "review_required": review_required,
        "status": "provisional",
    }


def _module_refs_by_structure(runtime_bundle: dict[str, Any]) -> dict[str, list[str]]:
    refs: dict[str, list[str]] = {}
    module_by_pattern = {module["pattern_id"]: module for module in build_modules(runtime_bundle)}
    for system in runtime_bundle.get("systems", []):
        pattern_id = str(system.get("pattern_id", ""))
        module = module_by_pattern.get(pattern_id)
        if not module:
            continue
        target_id = str(module.get("placement_target_id") or "")
        if target_id:
            refs.setdefault(target_id, []).append(module["module_id"])
    return {target: sorted(set(module_refs)) for target, module_refs in refs.items()}


def _with_dynamic_refs(base_refs: list[str], refs_by_structure: dict[str, list[str]], structure_id: str) -> list[str]:
    return list(dict.fromkeys([*base_refs, *refs_by_structure.get(structure_id, [])]))


def _care_room_status(runtime_bundle: dict[str, Any]) -> str:
    care_status = runtime_bundle.get("capabilities", {}).get("domain_statuses", {}).get("care_health", {}).get("status")
    return {"pass": "normal", "warn": "warning", "fail": "failed"}.get(care_status, "warning")


def _module_id(domain: str, pattern_id: str) -> str:
    return f"{domain}.{pattern_id}.active"


def _domain_for_pattern(pattern_id: str, system: dict[str, Any]) -> str:
    if pattern_id.startswith("care_health_") or "medication" in pattern_id or "care_" in pattern_id:
        return "care_health"
    if pattern_id.startswith("mobility_access_") or "accessible_route" in pattern_id:
        return "mobility_access"
    if pattern_id.startswith("water_public_health_") or "water_reserve_sanitation" in pattern_id or "water_recovery" in pattern_id:
        return "water_public_health"
    if pattern_id.startswith("water_"):
        return "water"
    if pattern_id.startswith("energy_"):
        return "energy"
    if pattern_id.startswith("food_") or "protein" in pattern_id:
        return "food"
    if pattern_id.startswith("labor_"):
        return "labor_time"
    if pattern_id.startswith("governance_"):
        return "governance_anticapture"
    critical = set(system.get("critical_resources", []))
    if "maintenance" in critical:
        return "maintenance_repair"
    return "risk_resilience"


def _tier_for_domain(domain: str) -> str:
    if domain in {"care_health", "water_public_health", "maintenance_repair", "labor_time", "mobility", "mobility_access", "education_skill", "social_cultural"}:
        return "operating_systems"
    if domain in {"governance_anticapture", "risk_resilience"}:
        return "meta_systems"
    return "floor_systems"


def _placement_target_for_domain(domain: str) -> str:
    return STRUCTURE_MODULE_TARGETS.get(domain, "")


def _module_summary(domain: str, pattern_id: str) -> str:
    if domain == "care_health":
        return "Care continuity operating module attached to the Care Room."
    if domain == "water_public_health":
        return "Water reserve sanitation and recovery protocol attached to the water node."
    if domain == "labor_time":
        return "Labor visibility and burden-tracking module."
    if domain == "mobility_access":
        return "Accessible route survey and daily-need mobility visibility module."
    return f"{_title(pattern_id)} active module."


def _placeholder_scenario(identifier: str, label: str, scenario_type: str, affected_objects: list[str]) -> dict[str, Any]:
    return {
        "id": identifier,
        "label": label,
        "type": scenario_type,
        "timeline": [
            {
                "timestep": 0,
                "label": f"{label} placeholder",
                "affected_objects": affected_objects,
                "overlays": {},
                "warnings": ["Scenario state placeholder; future exports should connect this to simulation output."],
            }
        ],
        "status": "placeholder",
    }


def _overlay(name: str, status: str, summary: str) -> dict[str, Any]:
    return {
        "enabled": True,
        "status": status,
        "summary": summary,
        "provisional": True,
    }


def _resource_metric(identifier: str, label: str, unit: str, balance: dict[str, Any], storage: dict[str, Any]) -> dict[str, Any]:
    capacity = _number(storage.get("capacity"))
    current = _number(storage.get("ending_total", balance.get("ending_balance")))
    minimum = _number(storage.get("minimum_total", balance.get("minimum_balance")))
    reserve_floor = _number(storage.get("reserve_floor"))
    drawdown = max(0.0, capacity - minimum) if capacity else 0.0
    return {
        "id": identifier,
        "label": label,
        "unit": unit,
        "status": balance.get("status", storage.get("status", "provisional")),
        "capacity": _round(capacity),
        "current": _round(current),
        "minimum": _round(minimum),
        "reserve_floor": _round(reserve_floor),
        "net_per_day": _round(balance.get("net_per_day")),
        "drawdown": _round(drawdown),
        "current_ratio": _ratio(current, capacity),
        "minimum_ratio": _ratio(minimum, capacity),
        "reserve_floor_ratio": _ratio(reserve_floor, capacity),
        "total_released": _round(storage.get("total_released")),
        "total_refilled": _round(storage.get("total_refilled")),
        "total_curtailed": _round(storage.get("total_curtailed")),
        "quality_status": storage.get("quality_status", "provisional"),
        "provisional": True,
    }


def _affected_objects_for_scenario(scenario: dict[str, Any]) -> list[str]:
    scenario_id = str(scenario.get("scenario", "")).lower()
    if "water" in scenario_id or "drought" in scenario_id:
        return ["node_water_reserve", "structure_common_house", "structure_food_commons"]
    if "energy" in scenario_id or "outage" in scenario_id:
        return ["node_solar_battery", "structure_common_house", "structure_care_room"]
    if "crop" in scenario_id or "food" in scenario_id:
        return ["structure_food_commons", "structure_protein_commons", "zone_food_garden"]
    return ["node_risk_governance"]


def _capability_status(runtime_bundle: dict[str, Any]) -> str:
    statuses = [value.get("status") for value in runtime_bundle.get("capabilities", {}).get("domain_statuses", {}).values()]
    if "fail" in statuses:
        return "fail"
    if "warn" in statuses:
        return "warn"
    if "pass" in statuses:
        return "pass"
    return "provisional"


def _v(x: float, y: float, z: float) -> dict[str, float]:
    return {"x": float(x), "y": float(y), "z": float(z)}


def _number(value: Any) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return 0.0


def _round(value: Any) -> float:
    return round(_number(value), 3)


def _ratio(numerator: float, denominator: float) -> float:
    if not denominator:
        return 0.0
    return round(max(0.0, min(1.0, numerator / denominator)), 3)


def _title(value: str) -> str:
    return str(value).replace("_", " ").title()
