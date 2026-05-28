from __future__ import annotations

import math
from typing import Any


PROVISIONALITY_NOTE = (
    "This is a provisional civic simulation. It visualizes model assumptions and stress tests. It does not certify "
    "real-world safety, legality, affordability, engineering, public health, accessibility, resident consent, or buildability."
)

VILLAGE_BLOCK_PREFERRED = 80
VILLAGE_BLOCK_MAX = 150
BLOCK_SPACING_X = 170
BLOCK_SPACING_Z = 145
VISIBLE_RESIDENT_ARCHETYPES = 12


SCALING_POLICY_ID = "ciac_scaling_policy_v0"


SCALING_POLICIES = {
    "residential_pod": {
        "policy_id": "residential_pod",
        "scale_action": "duplicate",
        "minimum": 12,
        "preferred": 12,
        "maximum": 20,
        "hard_max": 24,
        "human_factor_driver": "privacy, sleep, perceived crowding",
        "ui_warning": "Residential pod is beyond comfortable cluster size. Duplicate or subdivide.",
    },
    "common_house": {
        "policy_id": "common_house",
        "scale_action": "hybrid",
        "minimum": 30,
        "preferred": 80,
        "maximum": 100,
        "hard_max": 150,
        "human_factor_driver": "belonging, third-place comfort, institutional feel",
        "ui_warning": "One common house is serving too many residents as a single social heart. Add neighborhood commons.",
    },
    "food_commons": {
        "policy_id": "food_commons",
        "scale_action": "hybrid",
        "minimum": 50,
        "preferred": 80,
        "maximum": 100,
        "hard_max": 150,
        "human_factor_driver": "food safety, labor burden, scheduling",
        "ui_warning": "Food commons is approaching kitchen, dining, labor, or hygiene bottleneck. Duplicate pickup or kitchen capacity.",
    },
    "protein_commons": {
        "policy_id": "protein_commons",
        "scale_action": "hybrid",
        "minimum": 50,
        "preferred": 80,
        "maximum": 150,
        "hard_max": 150,
        "human_factor_driver": "food safety, acceptance, labor burden",
        "ui_warning": "Protein commons should not become one opaque technical bottleneck.",
    },
    "care_room": {
        "policy_id": "care_room",
        "scale_action": "hybrid",
        "minimum": 50,
        "preferred": 80,
        "maximum": 100,
        "hard_max": 150,
        "human_factor_driver": "privacy, illness separation, medication continuity",
        "ui_warning": "Care access, privacy, or illness separation may require another care room.",
    },
    "quiet_room": {
        "policy_id": "quiet_room",
        "scale_action": "duplicate",
        "minimum": 1,
        "preferred": 80,
        "maximum": 80,
        "hard_max": 80,
        "human_factor_driver": "mental health, privacy, sensory load",
        "ui_warning": "No low-social-energy retreat space is available at this scale.",
    },
    "maintenance_tool_cache": {
        "policy_id": "maintenance_tool_cache",
        "scale_action": "hybrid",
        "minimum": 50,
        "preferred": 80,
        "maximum": 150,
        "hard_max": 500,
        "human_factor_driver": "response time, autonomy, repairability",
        "ui_warning": "One workshop/tool node is serving too many residents. Add local tool cache or district workshop.",
    },
    "potable_water": {
        "policy_id": "potable_water",
        "scale_action": "hybrid",
        "minimum": 25,
        "preferred": 80,
        "maximum": 150,
        "hard_max": 150,
        "human_factor_driver": "public health, redundancy, emergency access",
        "ui_warning": "Population may trigger public-water-system review. Require legal and public-health review.",
    },
    "sanitation_access": {
        "policy_id": "sanitation_access",
        "scale_action": "hybrid",
        "minimum": 20,
        "preferred": 80,
        "maximum": 150,
        "hard_max": 150,
        "human_factor_driver": "hygiene, dignity, public health",
        "ui_warning": "Sanitation access is using emergency minimum logic. Add dignified local hygiene access.",
    },
    "risk_resilience_cell": {
        "policy_id": "risk_resilience_cell",
        "scale_action": "hybrid",
        "minimum": 50,
        "preferred": 80,
        "maximum": 150,
        "hard_max": 300,
        "human_factor_driver": "failure isolation, cascade prevention, recovery",
        "ui_warning": "Critical function depends on one node, role, or external provider.",
    },
    "governance_circle": {
        "policy_id": "governance_circle",
        "scale_action": "federate",
        "minimum": 30,
        "preferred": 80,
        "maximum": 80,
        "hard_max": 150,
        "human_factor_driver": "participation quality, legitimacy, meeting burden",
        "ui_warning": "Direct assembly burden rising. Federate into circles or delegated roles.",
    },
}


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
    "sanitation": "node_sanitation_waste",
}


def build_world_manifest(
    runtime_bundle: dict[str, Any],
    population: int | None = None,
    runtime_bundle_path: str | None = None,
    world_id: str | None = None,
    research_registry: dict[str, Any] | None = None,
) -> dict[str, Any]:
    resolved_population = int(population or _runtime_population(runtime_bundle) or 80)
    scale = infer_scale(resolved_population)
    modules = build_modules(runtime_bundle)
    layout = build_proxy_layout(resolved_population, scale, modules)
    zones = build_zones(layout, runtime_bundle)
    structures = build_structures(layout, runtime_bundle)
    infrastructure_nodes = build_infrastructure_nodes(layout, runtime_bundle)
    paths = build_paths(layout, runtime_bundle)
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
        research_registry,
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
        "linked_manifests": {
            "life_manifest": "examples/life_manifests/life_manifest_80_v0.json",
            "automation_manifest": "examples/life_manifests/automation_manifest_80_v0.json",
        },
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
        "residential_pods": _count_for_population(people, "residential_pod"),
        "common_houses": _count_for_population(people, "common_house", SCALING_POLICIES["common_house"]["maximum"]),
        "food_commons": _count_for_population(people, "food_commons", SCALING_POLICIES["food_commons"]["maximum"]),
        "protein_commons": _count_for_population(people, "protein_commons", SCALING_POLICIES["protein_commons"]["maximum"]),
        "care_rooms": _count_for_population(people, "care_room", SCALING_POLICIES["care_room"]["maximum"]),
        "quiet_rooms": max(village_blocks, _count_for_population(people, "quiet_room", SCALING_POLICIES["quiet_room"]["maximum"])),
        "social_commons": _count_for_population(people, "common_house", SCALING_POLICIES["common_house"]["maximum"]),
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
    block_centers = _block_offsets(int(scale.get("implied_village_blocks", 1)))
    first = block_centers[0]
    return {
        "population": int(population),
        "scale": scale,
        "center": _v(0, 0, 0),
        "block_centers": block_centers,
        "block_populations": _distribute_people(int(population), len(block_centers)),
        "positions": {
            "common_house": _translate(first, _v(0, 0, 8)),
            "food_commons": _translate(first, _v(-24, 0, 38)),
            "protein_commons": _translate(first, _v(24, 0, 38)),
            "care_room": _translate(first, _v(-32, 0, 4)),
            "social_cultural": _translate(first, _v(32, 0, 4)),
            "maintenance_shop": _translate(first, _v(24, 0, -44)),
            "water_node": _translate(first, _v(-48, 0, -44)),
            "energy_node": _translate(first, _v(0, 0, -52)),
            "sanitation_node": _translate(first, _v(48, 0, -42)),
            "garden": _translate(first, _v(0, 0, 50)),
            "pod_1": _translate(first, _v(-56, 0, 24)),
            "pod_2": _translate(first, _v(56, 0, 24)),
            "pod_3": _translate(first, _v(-56, 0, -24)),
            "pod_4": _translate(first, _v(56, 0, -24)),
            "quiet_studio": _translate(first, _v(-24, 0, -42)),
            "west_walk": _translate(first, _v(-32, 0, 0)),
            "east_walk": _translate(first, _v(32, 0, 0)),
            "north_walk": _translate(first, _v(0, 0, 28)),
            "south_walk": _translate(first, _v(0, 0, -28)),
        },
    }


def build_zones(layout: dict[str, Any], runtime_bundle: dict[str, Any]) -> list[dict[str, Any]]:
    people = int(layout.get("population", 80))
    centers = layout.get("block_centers", [_v(0, 0, 0)])
    bounds = _bounds_for_centers(centers)
    block_count = len(centers)
    return [
        _zone("zone_common_core", "common_core", "Commons Network" if people > VILLAGE_BLOCK_MAX else "Common Core", _v(0, -0.03, 8), _v(max(48, bounds["width"] + 56), 0.05, 36), "common_core", ["housing.dignified_village_block.v0_1", "governance.commons_stewardship_protocol.v0_1"], "evidence_common_core"),
        _zone("zone_residential_ring", "residential", f"{block_count} Residential Cell{'s' if block_count != 1 else ''}", _v(bounds["center_x"], -0.04, bounds["center_z"]), _v(max(128, bounds["width"] + 150), 0.05, max(112, bounds["depth"] + 130)), "housing", ["housing.dignified_village_block.v0_1"], "evidence_residential_pods"),
        _zone("zone_food_garden", "food", "Food + Garden Network" if people > VILLAGE_BLOCK_MAX else "Food Garden", _v(bounds["center_x"], -0.05, bounds["max_z"] + 56), _v(max(92, bounds["width"] + 90), 0.05, 46), "food", ["food.hybrid_food_commons.v0_1", "food.protein_commons_supplement.v0_1"], "evidence_food_commons"),
        _zone("zone_service_edge", "service_edge", "Federated Service Edge" if people > VILLAGE_BLOCK_MAX else "Service Edge", _v(bounds["center_x"], -0.06, bounds["min_z"] - 58), _v(max(118, bounds["width"] + 110), 0.05, 42), "service_edge", ["water.resilient_water_commons.v0_1", "energy.critical_load_energy_commons.v0_1", "sanitation.hygienic_circular_commons.v0_1"], "evidence_service_edge"),
        _zone("zone_mobility_loop", "mobility", "Accessible Daily Need Network", _v(bounds["center_x"], -0.07, bounds["center_z"]), _v(max(150, bounds["width"] + 190), 0.04, max(132, bounds["depth"] + 170)), "mobility", ["mobility_access.pedestrian_first_access_commons.v0_1"], "evidence_primary_paths"),
    ]


def build_structures(layout: dict[str, Any], runtime_bundle: dict[str, Any]) -> list[dict[str, Any]]:
    people = int(layout.get("population", 80))
    scale = layout.get("scale", {})
    counts = scale.get("topology_counts", {})
    block_centers = layout.get("block_centers", [_v(0, 0, 0)])
    block_populations = layout.get("block_populations", _distribute_people(people, len(block_centers)))
    module_refs_by_structure = _module_refs_by_structure(runtime_bundle)
    structures: list[dict[str, Any]] = []

    pod_count = int(counts.get("residential_pods", _count_for_population(people, "residential_pod")))
    residents_per_pod = _distribute_people(people, pod_count)
    for index in range(pod_count):
        block_index = index % len(block_centers)
        local_index = index // len(block_centers)
        served = residents_per_pod[index]
        position = _translate(block_centers[block_index], _pod_offset(local_index, pod_count, len(block_centers)))
        size_factor = _size_factor_for("residential_pod", served, 1.0, 1.18)
        structures.append(
            _with_layout_metadata(
                _structure(
                    f"structure_residential_pod_{index + 1}",
                    "residential_pod",
                    f"Residential Pod {index + 1}",
                    position,
                    _scaled_size(_v(10, 3.2, 8), size_factor),
                    "proxy_residential_pod",
                    ["housing.dignified_village_block.v0_1"],
                    ["housing", "dignity_privacy"],
                    _status_for_capacity("residential_pod", served),
                    "evidence_residential_pods",
                    served,
                ),
                f"cell_{block_index + 1}",
                "residential_pod",
                served,
            )
        )

    structures.extend(
        _build_cell_host_structures(
            "structure_common_house",
            "common_house",
            "Common House",
            int(counts.get("common_houses", 1)),
            block_populations,
            block_centers,
            _v(0, 0, 8),
            _v(13, 4, 9),
            "proxy_common_house",
            _with_dynamic_refs(["housing.dignified_village_block.v0_1", "social_cultural_commons.belonging_without_coercion.v0_1", "governance.commons_stewardship_protocol.v0_1"], module_refs_by_structure, "structure_common_house"),
            ["food", "social", "governance"],
            "evidence_common_house",
        )
    )
    structures.extend(
        _build_cell_host_structures(
            "structure_food_commons",
            "food_commons",
            "Hybrid Food Commons",
            int(counts.get("food_commons", 1)),
            block_populations,
            block_centers,
            _v(-24, 0, 38),
            _v(12, 3.5, 7),
            "proxy_food_commons",
            _with_dynamic_refs(["food.hybrid_food_commons.v0_1"], module_refs_by_structure, "structure_food_commons"),
            ["food", "labor_time"],
            "evidence_food_commons",
        )
    )
    structures.extend(
        _build_cell_host_structures(
            "structure_protein_commons",
            "protein_commons",
            "Protein Commons",
            int(counts.get("protein_commons", 1)),
            block_populations,
            block_centers,
            _v(24, 0, 38),
            _v(9, 3, 6),
            "proxy_protein_commons",
            _with_dynamic_refs(["food.protein_commons_supplement.v0_1"], module_refs_by_structure, "structure_protein_commons"),
            ["food"],
            "evidence_protein_commons",
        )
    )
    structures.extend(
        _build_cell_host_structures(
            "structure_care_room",
            "care_room",
            "Care Room",
            int(counts.get("care_rooms", 1)),
            block_populations,
            block_centers,
            _v(-32, 0, 4),
            _v(7, 3, 6),
            "proxy_care_room",
            _with_dynamic_refs(["risk_resilience.graceful_degradation_engine.v0_1"], module_refs_by_structure, "structure_care_room"),
            ["care", "risk_resilience"],
            "evidence_care_room",
            _care_room_status(runtime_bundle),
        )
    )
    structures.extend(
        _build_cell_host_structures(
            "structure_social_cultural",
            "common_house",
            "Social Commons",
            int(counts.get("social_commons", 1)),
            block_populations,
            block_centers,
            _v(32, 0, 4),
            _v(10, 3, 6),
            "proxy_social_cultural",
            _with_dynamic_refs(["social_cultural_commons.belonging_without_coercion.v0_1"], module_refs_by_structure, "structure_social_cultural"),
            ["social"],
            "evidence_social_cultural",
            structure_type="social_cultural",
        )
    )
    structures.extend(
        _build_cell_host_structures(
            "structure_quiet_studio",
            "quiet_room",
            "Quiet Studio",
            int(counts.get("quiet_rooms", 1)),
            block_populations,
            block_centers,
            _v(-24, 0, -42),
            _v(8, 3, 6),
            "proxy_quiet_studio",
            _with_dynamic_refs(["labor_time.life_burden_ledger.v0_1"], module_refs_by_structure, "structure_quiet_studio"),
            ["labor_time", "dignity_privacy"],
            "evidence_quiet_studio",
            structure_type="quiet_studio",
        )
    )

    if people < VILLAGE_BLOCK_MAX:
        structures.append(
            _with_layout_metadata(
                _structure(
                    "structure_maintenance_shop",
                    "maintenance_shop",
                    "Maintenance Shop",
                    _translate(block_centers[0], _v(24, 0, -44)),
                    _v(11, 3, 7),
                    "proxy_maintenance_shop",
                    _with_dynamic_refs(["maintenance.maintainable_commons_spine.v0_1", "education_skill.civic_skill_lattice.v0_1"], module_refs_by_structure, "structure_maintenance_shop"),
                    ["maintenance"],
                    "normal",
                    "evidence_maintenance_shop",
                    people,
                ),
                "cell_1",
                "maintenance_tool_cache",
                people,
            )
        )
    else:
        bounds = _bounds_for_centers(block_centers)
        structures.append(
            _with_layout_metadata(
                _structure(
                    "structure_maintenance_shop",
                    "maintenance_shop",
                    "District Workshop",
                    _v(bounds["center_x"], 0, bounds["min_z"] - 92),
                    _scaled_size(_v(11, 3, 7), 1.45 if people >= 500 else 1.22),
                    "proxy_maintenance_shop",
                    _with_dynamic_refs(["maintenance.maintainable_commons_spine.v0_1", "education_skill.civic_skill_lattice.v0_1"], module_refs_by_structure, "structure_maintenance_shop"),
                    ["maintenance"],
                    "normal",
                    "evidence_maintenance_shop",
                    people,
                ),
                "district",
                "maintenance_tool_cache",
                people,
            )
        )

    if people >= 300:
        district_count = max(1, math.ceil(people / 500))
        bounds = _bounds_for_centers(block_centers)
        for index in range(district_count):
            x = bounds["center_x"] + (index - (district_count - 1) / 2) * 42
            served = math.ceil(people / district_count)
            structures.append(
                _with_layout_metadata(
                    _structure(
                        f"structure_district_venue_{index + 1}",
                        "district_venue",
                        "District Commons" if district_count == 1 else f"District Commons {index + 1}",
                        _v(x, 0, bounds["min_z"] - 126),
                        _scaled_size(_v(13, 4, 9), 1.45),
                        "proxy_common_house",
                        ["social_cultural_commons.belonging_without_coercion.v0_1", "governance.commons_stewardship_protocol.v0_1"],
                        ["social", "governance"],
                        "normal",
                        "evidence_common_house",
                        served,
                    ),
                    "district",
                    "common_house",
                    served,
                )
            )

    layout["generated_structures"] = structures
    return structures


def build_paths(layout: dict[str, Any], runtime_bundle: dict[str, Any]) -> list[dict[str, Any]]:
    structures = layout.get("generated_structures", [])
    nodes = layout.get("generated_nodes", [])
    block_centers = layout.get("block_centers", [_v(0, 0, 0)])
    module_refs = ["mobility_access.pedestrian_first_access_commons.v0_1"]
    paths: list[dict[str, Any]] = []
    for index, center in enumerate(block_centers, start=1):
        cell_id = f"cell_{index}"
        cell_structures = [item for item in structures if item.get("display", {}).get("cell_id") == cell_id]
        cell_nodes = [item for item in nodes if item.get("display", {}).get("cell_id") == cell_id]
        pods = _nearest_points([item["position"] for item in cell_structures if item.get("type") == "residential_pod"], center, 10)
        common = _nearest_point([item["position"] for item in cell_structures if item.get("type") == "common_house"], center)
        food = _nearest_point([item["position"] for item in cell_structures if item.get("type") == "food_commons"], center)
        protein = _nearest_point([item["position"] for item in cell_structures if item.get("type") == "protein_commons"], center)
        care = _nearest_point([item["position"] for item in cell_structures if item.get("type") == "care_room"], center)
        social = _nearest_point([item["position"] for item in cell_structures if item.get("type") == "social_cultural"], center)
        quiet = _nearest_point([item["position"] for item in cell_structures if item.get("type") == "quiet_studio"], center)
        water = _nearest_point([item["position"] for item in cell_nodes if item.get("type") == "water"], center)
        energy = _nearest_point([item["position"] for item in cell_nodes if item.get("type") == "energy"], center)
        sanitation = _nearest_point([item["position"] for item in cell_nodes if item.get("type") == "sanitation"], center)
        if len(pods) >= 2:
            paths.append(_path(f"path_{cell_id}_pod_loop", "primary_access", f"Cell {index} Pod Loop", _loop_points(pods), module_refs))
        paths.append(_path(f"path_{cell_id}_daily_access", "primary_access", f"Cell {index} Daily Access", _compact_points([common, food, protein, care, social, quiet]), module_refs))
        paths.append(_path(f"path_{cell_id}_service_access", "service", f"Cell {index} Service Access", _compact_points([water, center, energy, sanitation]), module_refs))

    district_targets = _ordered_points(
        [
            *[item["position"] for item in structures if item.get("display", {}).get("cell_id") == "district"],
            *[item["position"] for item in nodes if item.get("display", {}).get("cell_id") == "district"],
        ]
    )
    if len(district_targets) >= 2:
        paths.append(_path("path_district_federation", "primary_access", "District Federation Spine", district_targets, module_refs))
    return [path for path in paths if len(path.get("points", [])) >= 2]


def build_infrastructure_nodes(layout: dict[str, Any], runtime_bundle: dict[str, Any]) -> list[dict[str, Any]]:
    people = int(layout.get("population", 80))
    block_centers = layout.get("block_centers", [_v(0, 0, 0)])
    resources = runtime_bundle.get("timeline", {}).get("resource_balance", {})
    storage = runtime_bundle.get("timeline", {}).get("storage", {}).get("resources", {})
    module_refs_by_structure = _module_refs_by_structure(runtime_bundle)
    block_count = len(block_centers)
    nodes: list[dict[str, Any]] = []
    for index, center in enumerate(block_centers, start=1):
        served = math.ceil(people / block_count)
        cell_id = f"cell_{index}"
        nodes.append(
            _with_node_layout_metadata(
                _node(
                    "node_water_reserve" if index == 1 else f"node_water_reserve_{index}",
                    "water",
                    "Water Source + Reserve" if block_count == 1 else f"Water Reserve {index}",
                    _translate(center, _v(-48, 0, -44)),
                    "proxy_water_node",
                    _with_dynamic_refs(["water.resilient_water_commons.v0_1"], module_refs_by_structure, "node_water_reserve"),
                    {"daily_net": resources.get("water_liters", {}).get("net_per_day", 0), "stored": storage.get("water_liters", {}).get("ending_total", 0), "status": resources.get("water_liters", {}).get("status", "provisional"), "residents_served": served},
                    "evidence_water_node",
                ),
                cell_id,
                "potable_water",
                served,
            )
        )
        nodes.append(
            _with_node_layout_metadata(
                _node(
                    "node_solar_battery" if index == 1 else f"node_solar_battery_{index}",
                    "energy",
                    "Solar + Critical Battery" if block_count == 1 else f"Critical Energy {index}",
                    _translate(center, _v(0, 0, -52)),
                    "proxy_solar_battery",
                    ["energy.critical_load_energy_commons.v0_1"],
                    {"daily_net": resources.get("energy_kwh", {}).get("net_per_day", 0), "stored": storage.get("energy_kwh", {}).get("ending_total", 0), "critical_load_runtime_hours": 72, "status": resources.get("energy_kwh", {}).get("status", "provisional"), "residents_served": served},
                    "evidence_solar_battery",
                ),
                cell_id,
                "risk_resilience_cell",
                served,
            )
        )
        nodes.append(
            _with_node_layout_metadata(
                _node(
                    "node_sanitation_waste" if index == 1 else f"node_sanitation_waste_{index}",
                    "sanitation",
                    "Sanitation + Waste" if block_count == 1 else f"Sanitation Access {index}",
                    _translate(center, _v(48, 0, -42)),
                    "proxy_sanitation_node",
                    _with_dynamic_refs(["sanitation.hygienic_circular_commons.v0_1"], module_refs_by_structure, "node_sanitation_waste"),
                    {"status": _sanitation_status(runtime_bundle), "fields": _sanitation_fields(runtime_bundle), "residents_served": served},
                    "evidence_sanitation_node",
                ),
                cell_id,
                "sanitation_access",
                served,
            )
        )

    bounds = _bounds_for_centers(block_centers)
    nodes.append(
        _with_node_layout_metadata(
            _node(
                "node_risk_governance",
                "risk",
                "Federated Governance Board" if people > VILLAGE_BLOCK_MAX else "Risk + Governance Board",
                _v(bounds["center_x"], 0, bounds["min_z"] - 126 if people > VILLAGE_BLOCK_MAX else bounds["center_z"] - 18),
                "proxy_risk_board",
                ["governance.commons_stewardship_protocol.v0_1", "risk_resilience.graceful_degradation_engine.v0_1"],
                {"capability_status": _capability_status(runtime_bundle), "residents_served": people},
                "evidence_risk_governance",
            ),
            "district",
            "governance_circle",
            people,
        )
    )
    layout["generated_nodes"] = nodes
    return nodes


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
    capability_state = runtime_bundle.get("capabilities", {}).get("state", {}).get("domains", {})
    domain_statuses = runtime_bundle.get("capabilities", {}).get("domain_statuses", {})
    policy_domain_statuses = runtime_bundle.get("capabilities", {}).get("policy_gate", {}).get("domain_statuses", {})
    overlays = {
        "food": _overlay("food", resource_balance.get("food_servings", {}).get("status", "provisional"), "Food commons and reserve state."),
        "water": _overlay("water", resource_balance.get("water_liters", {}).get("status", "provisional"), "Water source, storage, and recovery state."),
        "energy": _overlay("energy", resource_balance.get("energy_kwh", {}).get("status", "provisional"), "Critical-load supply and storage state."),
    }
    for domain in ("labor_time", "governance_anticapture", "care_health", "sanitation", "mobility_access", "legal_land_finance", "risk_resilience"):
        domain_status = policy_domain_statuses.get(domain) or domain_statuses.get(domain, {})
        overlays[domain] = _overlay(
            domain,
            domain_status.get("status", "provisional"),
            f"{_title(domain)} capability status.",
            messages=domain_status.get("messages", []),
            fields=capability_state.get(domain, {}),
            policy=domain_status if domain_status is policy_domain_statuses.get(domain) else {},
        )
    return overlays


def build_evidence_cards(
    world_objects: dict[str, list[dict[str, Any]]],
    runtime_bundle: dict[str, Any],
    research_registry: dict[str, Any] | None = None,
) -> list[dict[str, Any]]:
    module_refs_by_structure = _module_refs_by_structure(runtime_bundle)
    care_modules = module_refs_by_structure.get("structure_care_room", [])
    water_modules = module_refs_by_structure.get("node_water_reserve", [])
    module_by_ref = _module_lookup(runtime_bundle)
    sources_by_domain = _policy_sources_by_domain(runtime_bundle, research_registry)
    source_registry = _policy_source_registry(runtime_bundle, research_registry)
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
    resolved_cards = []
    for card_id, card in sorted(cards.items()):
        if card_id not in used and card_id not in {"evidence_protein_commons", "evidence_common_house", "evidence_solar_battery"}:
            continue
        resolved_cards.append(_with_sources(card, module_by_ref, sources_by_domain, source_registry))
    return resolved_cards


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


def _build_cell_host_structures(
    prototype_id: str,
    policy_id: str,
    label: str,
    total_units: int,
    block_populations: list[int],
    block_centers: list[dict[str, float]],
    offset: dict[str, float],
    base_size: dict[str, float],
    asset_key: str,
    module_refs: list[str],
    systems: list[str],
    evidence_card_id: str,
    forced_status: str | None = None,
    structure_type: str | None = None,
) -> list[dict[str, Any]]:
    units_by_cell = _distribute_units(max(total_units, len(block_centers)), len(block_centers))
    structures: list[dict[str, Any]] = []
    for index, center in enumerate(block_centers):
        unit_count = units_by_cell[index]
        served = block_populations[index]
        adjusted_policy = _scaled_policy(policy_id, unit_count)
        capacity = int(adjusted_policy.get("maximum", 1))
        status = forced_status or ("warning" if served > capacity else "normal")
        structure_id = prototype_id if index == 0 else f"{prototype_id}_cell_{index + 1}"
        unit_suffix = f" ({unit_count} modules)" if unit_count > 1 else ""
        structure = _structure(
            structure_id,
            structure_type or policy_id,
            label if len(block_centers) == 1 else f"{label} {index + 1}{unit_suffix}",
            _translate(center, offset),
            _scaled_size(base_size, _size_factor_for(policy_id, served, 1.0, 1.65, adjusted_policy)),
            asset_key,
            module_refs,
            systems,
            status,
            evidence_card_id,
            served,
        )
        structures.append(_with_layout_metadata(structure, f"cell_{index + 1}", policy_id, served, adjusted_policy, unit_count))
    return structures


def _with_layout_metadata(
    structure: dict[str, Any],
    cell_id: str,
    policy_id: str,
    residents_served: int,
    policy: dict[str, Any] | None = None,
    represented_units: int = 1,
) -> dict[str, Any]:
    effective_policy = policy or SCALING_POLICIES.get(policy_id)
    structure["display"] = {
        **structure.get("display", {}),
        "cell_id": cell_id,
        "position_authoritative": True,
        "represented_units": represented_units,
    }
    structure["scaling_policy"] = _object_policy(effective_policy, residents_served)
    structure.setdefault("state", {})["residents_served"] = residents_served
    return structure


def _with_node_layout_metadata(
    node: dict[str, Any],
    cell_id: str,
    policy_id: str,
    residents_served: int,
    policy: dict[str, Any] | None = None,
) -> dict[str, Any]:
    effective_policy = policy or SCALING_POLICIES.get(policy_id)
    node["display"] = {
        **node.get("display", {}),
        "cell_id": cell_id,
        "position_authoritative": True,
    }
    node["scaling_policy"] = _object_policy(effective_policy, residents_served)
    node.setdefault("metrics", {})["residents_served"] = residents_served
    return node


def _object_policy(policy: dict[str, Any] | None, residents_served: int) -> dict[str, Any] | None:
    if not policy:
        return None
    served = int(residents_served or 0)
    maximum = int(policy.get("maximum", 0) or 0)
    return {
        "policy_id": policy.get("policy_id"),
        "source_policy_id": SCALING_POLICY_ID,
        "scale_action": policy.get("scale_action"),
        "residents_served": served,
        "preferred_capacity": policy.get("preferred"),
        "soft_threshold": maximum,
        "hard_threshold": policy.get("hard_max"),
        "human_factor_driver": policy.get("human_factor_driver"),
        "ui_warning": policy.get("ui_warning") if maximum and served > maximum else "",
    }


def _scaled_policy(policy_id: str, unit_count: int) -> dict[str, Any]:
    policy = dict(SCALING_POLICIES.get(policy_id, {}))
    units = max(1, int(unit_count or 1))
    for key in ("preferred", "maximum", "hard_max"):
        if policy.get(key):
            policy[key] = int(policy[key]) * units
    return policy


def _status_for_capacity(policy_id: str, residents_served: int) -> str:
    policy = SCALING_POLICIES.get(policy_id, {})
    maximum = int(policy.get("maximum", 0) or 0)
    hard_max = int(policy.get("hard_max", 0) or 0)
    if hard_max and residents_served > hard_max:
        return "failed"
    if maximum and residents_served > maximum:
        return "warning"
    return "normal"


def _count_for_population(population: int, policy_id: str, capacity: Any | None = None) -> int:
    policy = SCALING_POLICIES.get(policy_id, {})
    resolved_capacity = int(capacity or policy.get("preferred") or policy.get("maximum") or 1)
    return max(1, math.ceil(max(1, int(population)) / max(1, resolved_capacity)))


def _block_offsets(count: int) -> list[dict[str, float]]:
    total = max(1, int(count))
    columns = math.ceil(math.sqrt(total))
    rows = math.ceil(total / columns)
    center_x = ((columns - 1) * BLOCK_SPACING_X) / 2
    center_z = ((rows - 1) * BLOCK_SPACING_Z) / 2
    return [
        _v((index % columns) * BLOCK_SPACING_X - center_x, 0, math.floor(index / columns) * BLOCK_SPACING_Z - center_z)
        for index in range(total)
    ]


def _bounds_for_centers(centers: list[dict[str, float]]) -> dict[str, float]:
    xs = [float(center.get("x", 0.0)) for center in centers] or [0.0]
    zs = [float(center.get("z", 0.0)) for center in centers] or [0.0]
    min_x = min(xs)
    max_x = max(xs)
    min_z = min(zs)
    max_z = max(zs)
    return {
        "min_x": min_x,
        "max_x": max_x,
        "min_z": min_z,
        "max_z": max_z,
        "center_x": (min_x + max_x) / 2,
        "center_z": (min_z + max_z) / 2,
        "width": max_x - min_x,
        "depth": max_z - min_z,
    }


def _distribute_people(people: int, count: int) -> list[int]:
    total = max(1, int(people))
    slots = max(1, int(count))
    base = total // slots
    remainder = total % slots
    return [base + (1 if index < remainder else 0) for index in range(slots)]


def _distribute_units(total_units: int, count: int) -> list[int]:
    total = max(1, int(total_units))
    slots = max(1, int(count))
    base = total // slots
    remainder = total % slots
    return [base + (1 if index < remainder else 0) for index in range(slots)]


def _pod_offset(index: int, total_count: int, block_count: int) -> dict[str, float]:
    per_cell = math.ceil(total_count / max(1, block_count))
    slots = max(6, min(10, per_cell))
    ring = index // slots
    angle = ((index % slots) / slots) * math.pi * 2 + ((math.pi / slots) if ring % 2 else 0)
    radius = 56 + ring * 16
    return _v(math.cos(angle) * radius, 0, math.sin(angle) * radius)


def _size_factor_for(
    policy_id: str,
    residents_served: int,
    base: float = 1.0,
    maximum: float = 1.35,
    policy: dict[str, Any] | None = None,
) -> float:
    effective_policy = policy or SCALING_POLICIES.get(policy_id, {})
    preferred = max(1, int(effective_policy.get("preferred") or 1))
    return base * min(maximum, max(0.78, math.sqrt(max(1, int(residents_served)) / preferred)))


def _scaled_size(size: dict[str, float], factor: float) -> dict[str, float]:
    return _v(
        _round(float(size.get("x", 6)) * factor),
        _round(float(size.get("y", 3)) * min(1.12, max(0.92, factor))),
        _round(float(size.get("z", 5)) * factor),
    )


def _translate(vector: dict[str, float], offset: dict[str, float]) -> dict[str, float]:
    return _v(
        float(vector.get("x", 0.0)) + float(offset.get("x", 0.0)),
        float(vector.get("y", 0.0)) + float(offset.get("y", 0.0)),
        float(vector.get("z", 0.0)) + float(offset.get("z", 0.0)),
    )


def _compact_points(points: list[dict[str, float] | None]) -> list[dict[str, float]]:
    return [point for point in points if isinstance(point, dict)]


def _distance(a: dict[str, float], b: dict[str, float]) -> float:
    dx = float(a.get("x", 0.0)) - float(b.get("x", 0.0))
    dz = float(a.get("z", 0.0)) - float(b.get("z", 0.0))
    return math.sqrt(dx * dx + dz * dz)


def _nearest_point(points: list[dict[str, float]], origin: dict[str, float]) -> dict[str, float] | None:
    nearest = _nearest_points(points, origin, 1)
    return nearest[0] if nearest else None


def _nearest_points(points: list[dict[str, float]], origin: dict[str, float], limit: int) -> list[dict[str, float]]:
    return sorted(_compact_points(points), key=lambda point: _distance(point, origin))[:limit]


def _loop_points(points: list[dict[str, float]]) -> list[dict[str, float]]:
    ordered = _radial_order(points)
    return [*ordered, ordered[0]] if len(ordered) > 2 else ordered


def _radial_order(points: list[dict[str, float]]) -> list[dict[str, float]]:
    if not points:
        return []
    center_x = sum(float(point.get("x", 0.0)) for point in points) / len(points)
    center_z = sum(float(point.get("z", 0.0)) for point in points) / len(points)
    return sorted(points, key=lambda point: math.atan2(float(point.get("z", 0.0)) - center_z, float(point.get("x", 0.0)) - center_x))


def _ordered_points(points: list[dict[str, float]]) -> list[dict[str, float]]:
    return sorted(_compact_points(points), key=lambda point: (float(point.get("z", 0.0)), float(point.get("x", 0.0))))


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


def _module_lookup(runtime_bundle: dict[str, Any]) -> dict[str, dict[str, Any]]:
    lookup: dict[str, dict[str, Any]] = {}
    for module in build_modules(runtime_bundle):
        if module.get("module_id"):
            lookup[str(module["module_id"])] = module
        if module.get("pattern_id"):
            lookup[str(module["pattern_id"])] = module
    return lookup


def _policy_sources_by_domain(runtime_bundle: dict[str, Any], research_registry: dict[str, Any] | None = None) -> dict[str, list[str]]:
    domains = runtime_bundle.get("capabilities", {}).get("policy_gate", {}).get("domain_statuses", {})
    source_ids_by_domain: dict[str, list[str]] = {}
    for domain, status in domains.items():
        source_ids = set(status.get("source_ids", []))
        for gate in status.get("gates", []):
            source_ids.update(gate.get("source_ids", []))
        normalized_domain = _normalize_source_domain(domain)
        source_ids_by_domain[normalized_domain] = sorted(source_ids)
    for entry in (research_registry or {}).get("entries", []):
        for domain in entry.get("domains", []):
            domain = _normalize_source_domain(domain)
            if domain == "unmapped":
                continue
            source_ids_by_domain.setdefault(str(domain), [])
            source_ids_by_domain[str(domain)] = sorted(set([*source_ids_by_domain[str(domain)], str(entry.get("id"))]))
    return source_ids_by_domain


def _policy_source_registry(runtime_bundle: dict[str, Any], research_registry: dict[str, Any] | None = None) -> dict[str, dict[str, Any]]:
    registry: dict[str, dict[str, Any]] = {}
    for source in runtime_bundle.get("capabilities", {}).get("policy_gate", {}).get("source_registry", []):
        source_id = source.get("id")
        if source_id:
            registry[str(source_id)] = source
    for entry in (research_registry or {}).get("entries", []):
        source_id = entry.get("id")
        if source_id:
            registry[str(source_id)] = entry
    return registry


def _with_sources(
    card: dict[str, Any],
    module_by_ref: dict[str, dict[str, Any]],
    sources_by_domain: dict[str, list[str]],
    source_registry: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    domains = set()
    for module_ref in card.get("module_refs", []):
        module = module_by_ref.get(str(module_ref), {})
        domain = _normalize_source_domain(module.get("domain") or _domain_from_module_ref(str(module_ref)))
        if domain:
            domains.add(str(domain))
    source_ids = sorted({source_id for domain in domains for source_id in sources_by_domain.get(domain, [])})
    sources = []
    for source_id in source_ids:
        source = source_registry.get(source_id)
        if not source:
            sources.append({"id": source_id, "title": source_id, "organization": "unknown", "evidence_quality": "mixed"})
            continue
        sources.append(
            {
                "id": source_id,
                "title": source.get("title", source_id),
                "organization": source.get("organization", "unknown"),
                "url": source.get("url"),
                "evidence_quality": source.get("evidence_quality", "mixed"),
                "supports": source.get("supports", []),
            }
        )
    return {
        **card,
        "source_ids": source_ids,
        "sources": sources,
        "source_note": "Sources support modeled capability gates and review assumptions; they are not approvals to build or operate.",
    }


def _domain_from_module_ref(module_ref: str) -> str:
    if "." in module_ref:
        return module_ref.split(".", 1)[0]
    return _domain_for_pattern(module_ref, {})


def _normalize_source_domain(domain: Any) -> str:
    aliases = {
        "mobility": "mobility_access",
        "maintenance": "maintenance_repair",
        "social": "social_cultural",
        "legal": "legal_land_finance",
    }
    value = str(domain or "")
    return aliases.get(value, value)


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


def _sanitation_status(runtime_bundle: dict[str, Any]) -> str:
    capabilities = runtime_bundle.get("capabilities", {})
    return (
        capabilities.get("policy_gate", {}).get("domain_statuses", {}).get("sanitation", {}).get("status")
        or capabilities.get("domain_statuses", {}).get("sanitation", {}).get("status")
        or "provisional"
    )


def _sanitation_fields(runtime_bundle: dict[str, Any]) -> dict[str, Any]:
    return runtime_bundle.get("capabilities", {}).get("state", {}).get("domains", {}).get("sanitation", {})


def _module_id(domain: str, pattern_id: str) -> str:
    return f"{domain}.{pattern_id}.active"


def _domain_for_pattern(pattern_id: str, system: dict[str, Any]) -> str:
    if pattern_id.startswith("care_health_") or "medication" in pattern_id or "care_" in pattern_id:
        return "care_health"
    if pattern_id in {"hygienic_circular_commons", "composting_system", "shared_bathhouse"}:
        return "sanitation"
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
    if domain == "sanitation":
        return "Sanitation, waste-stream, hygiene, and worker-safety operating module."
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


def _overlay(name: str, status: str, summary: str, messages: list[str] | None = None, fields: dict[str, Any] | None = None, policy: dict[str, Any] | None = None) -> dict[str, Any]:
    return {
        "enabled": True,
        "status": status,
        "summary": summary,
        "messages": messages or [],
        "fields": fields or {},
        "policy": policy or {},
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
