from __future__ import annotations

import math
from typing import Any


def generate_topology_recommendation(
    node_scaling_report: dict[str, Any],
    population: int,
    food_labor_report: dict[str, Any] | None = None,
    complexity_report: dict[str, Any] | None = None,
) -> dict[str, Any]:
    policies = node_scaling_report.get("node_policy_catalog", [])
    node_rows = [_node_row(policy, population) for policy in policies]
    candidates = [
        *_node_actions(node_rows, population),
        *_capability_actions(population, node_rows),
        *_food_labor_actions(food_labor_report, population),
        *_complexity_actions(complexity_report, population),
    ]
    ranked = sorted(candidates, key=lambda item: (-int(item["priority"]), item["id"]))
    selected = ranked[0] if ranked else _monitor_action(population)
    status = "action_recommended" if selected["type"] != "monitor" else "monitor"
    if not policies:
        status = "not_ready"
    return {
        "kind": "TopologyRecommendationReport",
        "id": f"{node_scaling_report.get('module_registry', 'module_registry')}_{population}_topology_recommendation",
        "generated_by": "ciac.topology_optimizer.v0",
        "provisional": True,
        "status": status,
        "population": population,
        "module_registry": node_scaling_report.get("module_registry", ""),
        "source_reports": {
            "node_scaling": node_scaling_report.get("id", ""),
            "food_labor": food_labor_report.get("id", "") if food_labor_report else "",
            "complexity": complexity_report.get("id", "") if complexity_report else "",
            "provisional": True,
        },
        "orchestration_model": node_scaling_report.get("orchestration_model", {}),
        "node_summary": _node_summary(node_rows),
        "selected_action": selected,
        "candidate_actions": ranked[:12],
        "decision_basis": _decision_basis(selected, node_rows, food_labor_report, complexity_report),
        "next_actions": _next_actions(selected),
        "unknowns": [
            "Topology recommendations choose simulation/planning actions, not real-world construction or governance actions.",
            "Population-aware recommendations need household composition, site geometry, mobility, care, climate, and culture models before promotion.",
            "The goal is flexible abundance-first topology, not automatic centralization or adversarial scarcity management.",
        ],
    }


def _node_row(policy: dict[str, Any], population: int) -> dict[str, Any]:
    minimum = int(policy.get("minimum_population_per_node", 1))
    preferred = int(policy.get("preferred_population_per_node", minimum))
    maximum = int(policy.get("maximum_population_per_node", preferred))
    if population < minimum:
        desired_nodes = 1
        mode = "seed_or_minimal"
        action = "scale_down"
        notes = policy.get("scale_down_strategy", "Use seed/default patterns.")
    elif population <= maximum:
        desired_nodes = 1
        mode = "village_node"
        action = "steady" if population <= preferred else "near_capacity"
        notes = "Within preferred range." if action == "steady" else "Above preferred population; pre-plan split or second node."
    else:
        desired_nodes = math.ceil(population / maximum)
        mode = "replicated_nodes"
        action = "scale_up"
        notes = policy.get("scale_up_strategy", "Replicate node pool.")
    population_per_node = population / desired_nodes
    return {
        **policy,
        "mode": mode,
        "action": action,
        "desired_nodes": desired_nodes,
        "population_per_node": round(population_per_node, 3),
        "headroom_per_node": round(maximum - population_per_node, 3),
        "notes": notes,
        "provisional": True,
    }


def _node_actions(node_rows: list[dict[str, Any]], population: int) -> list[dict[str, Any]]:
    actions = []
    scaled_down = [row for row in node_rows if row["mode"] == "seed_or_minimal"]
    replicated = [row for row in node_rows if row["mode"] == "replicated_nodes"]
    near_capacity = [row for row in node_rows if row["action"] == "near_capacity"]
    if scaled_down:
        actions.append(
            _action(
                "scale_down_to_seed_patterns",
                "scale_down",
                82 if population < 50 else 45,
                "Use seed/default patterns instead of carrying every village-scale module.",
                [row["slot"] for row in scaled_down],
            )
        )
    if replicated:
        actions.append(
            _action(
                "replicate_village_node_pools",
                "scale_up",
                88,
                "Replicate local dignity-floor and capacity nodes rather than centralizing one oversized system.",
                [row["slot"] for row in replicated],
            )
        )
    if near_capacity:
        floor_near = [row["slot"] for row in near_capacity if row.get("tier") == "floor_systems"]
        actions.append(
            _action(
                "preplan_second_village_cell",
                "prepare_scale_up",
                76 if floor_near else 62,
                "Population is above preferred node size; prepare split-node topology before adding more residents.",
                floor_near or [row["slot"] for row in near_capacity],
            )
        )
    if not actions:
        actions.append(_monitor_action(population))
    return actions


def _capability_actions(population: int, node_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    local_cells = max((int(row.get("desired_nodes", 1)) for row in node_rows), default=1)
    actions = []
    if population >= 300:
        actions.append(
            _action(
                "add_district_capability_layer",
                "add_capability_layer",
                64,
                "Add district-scale shared services while preserving local dignity-floor nodes.",
                ["clinic_access", "logistics", "advanced_workshop", "learning_partnerships"],
                desired_nodes=max(1, math.ceil(population / 500)),
            )
        )
    if population >= 900:
        actions.append(
            _action(
                "add_town_city_capability_layer",
                "add_capability_layer",
                66,
                "Add town/city capability for transit, culture, markets, and utilities coordination.",
                ["transit_spine", "cultural_venues", "markets", "utility_coordination"],
                desired_nodes=max(1, math.ceil(population / 1500)),
            )
        )
    if local_cells >= 6:
        actions.append(
            _action(
                "federate_cross_node_control_plane",
                "federate",
                70,
                "Add a thin federation layer for aggregate dashboards, mutual aid, standards, and portability.",
                ["aggregate_dashboards", "mutual_aid", "standards", "portability"],
                desired_nodes=1,
            )
        )
    return actions


def _food_labor_actions(food_labor_report: dict[str, Any] | None, population: int) -> list[dict[str, Any]]:
    if not food_labor_report:
        return []
    scale_row = _nearest_scale_row(food_labor_report.get("scaling_results", []), population)
    if not scale_row:
        return []
    if scale_row.get("status") == "warn" and population >= 50:
        return [
            _action(
                "split_food_labor_roles",
                "reduce_labor_concentration",
                72,
                "Food labor is scale-plausible per resident, but one category is too concentrated per node.",
                ["food_production", "common_meal_prep", "garden_greenhouse_coordination"],
            )
        ]
    return []


def _complexity_actions(complexity_report: dict[str, Any] | None, population: int) -> list[dict[str, Any]]:
    if not complexity_report or population < 150:
        return []
    hotspots = complexity_report.get("hotspots", [])
    subjects = [
        hotspot.get("subject", "")
        for hotspot in hotspots
        if hotspot.get("kind") == "slot_interface_surface"
    ]
    if not subjects:
        return []
    return [
        _action(
            "bundle_repeated_interfaces",
            "simplify_contracts",
            52,
            "Large slot interfaces should migrate repeated fields into reusable bundles before adding more modules.",
            subjects[:6],
        )
    ]


def _nearest_scale_row(rows: list[dict[str, Any]], population: int) -> dict[str, Any] | None:
    if not rows:
        return None
    return min(rows, key=lambda row: abs(int(row.get("target_population", population)) - population))


def _action(
    identifier: str,
    action_type: str,
    priority: int,
    rationale: str,
    affected_slots: list[str],
    desired_nodes: int | None = None,
) -> dict[str, Any]:
    row = {
        "id": identifier,
        "type": action_type,
        "priority": priority,
        "rationale": rationale,
        "affected_slots": affected_slots,
        "provisional": True,
    }
    if desired_nodes is not None:
        row["desired_nodes"] = desired_nodes
    return row


def _monitor_action(population: int) -> dict[str, Any]:
    return _action(
        "monitor_current_topology",
        "monitor",
        20,
        f"Current node topology is inside preferred range for {population} people.",
        [],
    )


def _node_summary(node_rows: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "total_desired_nodes": sum(int(row.get("desired_nodes", 0)) for row in node_rows),
        "replicated_slot_count": sum(1 for row in node_rows if row.get("mode") == "replicated_nodes"),
        "scaled_down_slot_count": sum(1 for row in node_rows if row.get("mode") == "seed_or_minimal"),
        "near_capacity_slot_count": sum(1 for row in node_rows if row.get("action") == "near_capacity"),
        "provisional": True,
    }


def _decision_basis(
    selected: dict[str, Any],
    node_rows: list[dict[str, Any]],
    food_labor_report: dict[str, Any] | None,
    complexity_report: dict[str, Any] | None,
) -> list[str]:
    basis = [selected["rationale"]]
    summary = _node_summary(node_rows)
    basis.append(
        f"Node summary: {summary['total_desired_nodes']} desired nodes, {summary['replicated_slot_count']} replicated slots, {summary['near_capacity_slot_count']} near-capacity slots."
    )
    if food_labor_report:
        basis.append(f"Food labor status: {food_labor_report.get('status', 'unknown')}.")
    if complexity_report:
        basis.append(f"Complexity status: {complexity_report.get('status', 'unknown')}.")
    return basis


def _next_actions(selected: dict[str, Any]) -> list[str]:
    action_type = selected.get("type")
    if action_type == "scale_down":
        return ["Keep micro-scale demos on seed/default patterns and avoid activating full village overhead."]
    if action_type == "prepare_scale_up":
        return ["Create a second-cell topology candidate before allowing the current node to exceed its maximum population."]
    if action_type == "scale_up":
        return ["Materialize replicated node pools in the topology viewer and evaluate federated capability layers."]
    if action_type == "add_capability_layer":
        return ["Define district/town service boundaries without replacing local dignity-floor nodes."]
    if action_type == "reduce_labor_concentration":
        return ["Split roles, simplify menus, or add food nodes until per-node category labor is below threshold."]
    return ["Continue monitoring topology pressure as population changes."]
