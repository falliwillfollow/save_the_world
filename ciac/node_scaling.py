from __future__ import annotations

import math
from collections import Counter
from typing import Any


def generate_node_scaling_report(
    module_registry: dict[str, Any],
    scale_profile: dict[str, Any] | None = None,
    extra_people: list[int] | None = None,
) -> dict[str, Any]:
    targets = _targets(module_registry, scale_profile, extra_people)
    tier_by_slot = _tier_by_slot(module_registry)
    target_results = [_target_result(module_registry, tier_by_slot, target) for target in targets]
    hotspots = _hotspots(target_results)
    return {
        "kind": "InfrastructureNodeReport",
        "id": f"{module_registry.get('id', 'module_registry')}_infrastructure_nodes",
        "generated_by": "ciac.node_scaling.v0",
        "provisional": True,
        "status": _status(hotspots),
        "module_registry": module_registry.get("id", ""),
        "scale_profile": scale_profile.get("id", "") if scale_profile else "",
        "orchestration_model": {
            "unit": "civic infrastructure node pool",
            "scale_up_rule": "replicate village-scale nodes when population exceeds a slot maximum",
            "scale_down_rule": "fall back to seed/default patterns when population is below a slot minimum",
            "federation_rule": "coordinate across replicated nodes through shared capability layers without replacing local dignity floors",
            "flourishing_frame": module_registry.get("flourishing_posture", {}).get("frame", ""),
            "scope_rule": module_registry.get("flourishing_posture", {}).get("scope_rule", ""),
            "provisional": True,
        },
        "node_policy_catalog": _node_policy_catalog(module_registry, tier_by_slot),
        "target_results": target_results,
        "hotspots": hotspots,
        "recommendations": _recommendations(hotspots),
        "unknowns": [
            "Infrastructure nodes are planning topology units, not construction packages, permits, or operating licenses.",
            "Stateful nodes need migration plans before scale-down; people, rights, land, reserves, and records cannot be deleted like compute containers.",
            "Federation above village scale must preserve resident rights, review boundaries, privacy, and local autonomy.",
        ],
    }


def _node_policy_catalog(module_registry: dict[str, Any], tier_by_slot: dict[str, str]) -> list[dict[str, Any]]:
    rows = []
    for slot in module_registry.get("slots", []):
        policy = slot.get("node_policy", {})
        if not policy:
            continue
        rows.append(
            {
                "slot": slot.get("id", ""),
                "domain": slot.get("domain", ""),
                "tier": tier_by_slot.get(slot.get("id", ""), "unclassified"),
                "default_patterns": slot.get("default_patterns", []),
                "accepted_patterns": slot.get("accepted_patterns", []),
                "scale_unit": policy.get("scale_unit", "residents"),
                "minimum_population_per_node": int(policy["minimum_population_per_node"]),
                "preferred_population_per_node": int(policy["preferred_population_per_node"]),
                "maximum_population_per_node": int(policy["maximum_population_per_node"]),
                "scale_down_strategy": policy["scale_down_strategy"],
                "scale_up_strategy": policy["scale_up_strategy"],
                "stateful": bool(policy.get("stateful", True)),
                "provisional": True,
            }
        )
    return rows


def _targets(module_registry: dict[str, Any], scale_profile: dict[str, Any] | None, extra_people: list[int] | None) -> list[dict[str, Any]]:
    if scale_profile:
        targets = [
            {
                "people": int(target["people"]),
                "label": target.get("label", f"{target['people']} people"),
                "notes": target.get("notes", ""),
                "provisional": True,
            }
            for target in scale_profile.get("targets", [])
            if "people" in target
        ]
    else:
        targets = [
            {
                "people": int(people),
                "label": f"{people} people",
                "notes": "From module registry scaling policy.",
                "provisional": True,
            }
            for people in module_registry.get("scaling_policy", {}).get("required_targets", [])
        ]
    for people in extra_people or []:
        targets.append(
            {
                "people": int(people),
                "label": f"{people} people",
                "notes": "Ad hoc operator-selected population target.",
                "provisional": True,
            }
        )
    return [
        target
        for _, target in sorted({target["people"]: target for target in targets}.items())
    ]


def _tier_by_slot(module_registry: dict[str, Any]) -> dict[str, str]:
    tiers = {}
    for tier, slot_ids in module_registry.get("module_tiers", {}).items():
        for slot_id in slot_ids:
            tiers[slot_id] = tier
    return tiers


def _target_result(module_registry: dict[str, Any], tier_by_slot: dict[str, str], target: dict[str, Any]) -> dict[str, Any]:
    people = int(target["people"])
    slot_results = [_slot_node_result(slot, tier_by_slot.get(slot.get("id", ""), "unclassified"), people) for slot in module_registry.get("slots", [])]
    tier_counts = Counter()
    for result in slot_results:
        tier_counts[result["tier"]] += result["desired_nodes"]
    replicated = [result for result in slot_results if result["mode"] == "replicated_nodes"]
    scaled_down = [result for result in slot_results if result["mode"] == "seed_or_minimal"]
    return {
        "people": people,
        "label": target["label"],
        "notes": target.get("notes", ""),
        "total_desired_nodes": sum(result["desired_nodes"] for result in slot_results),
        "tier_node_counts": dict(sorted(tier_counts.items())),
        "replicated_slot_count": len(replicated),
        "scaled_down_slot_count": len(scaled_down),
        "slot_results": slot_results,
        "provisional": True,
    }


def _slot_node_result(slot: dict[str, Any], tier: str, people: int) -> dict[str, Any]:
    policy = slot.get("node_policy", {})
    if not policy:
        return {
            "slot": slot.get("id", ""),
            "tier": tier,
            "mode": "missing_policy",
            "desired_nodes": 0,
            "population_per_node": 0,
            "headroom_per_node": 0,
            "active_patterns": slot.get("default_patterns", []),
            "node_policy": {},
            "action": "define_node_policy",
            "notes": "No node policy is declared for this slot.",
            "provisional": True,
        }
    minimum = int(policy["minimum_population_per_node"])
    preferred = int(policy["preferred_population_per_node"])
    maximum = int(policy["maximum_population_per_node"])
    if people < minimum:
        desired_nodes = 1
        mode = "seed_or_minimal"
        action = "scale_down"
        active_patterns = slot.get("default_patterns", [])
        notes = policy["scale_down_strategy"]
    elif people <= maximum:
        desired_nodes = 1
        mode = "village_node"
        action = "steady" if people <= preferred else "near_capacity"
        active_patterns = slot.get("accepted_patterns") or slot.get("default_patterns", [])
        notes = "Within one node; monitor headroom." if action == "near_capacity" else "Within preferred node range."
    else:
        desired_nodes = math.ceil(people / maximum)
        mode = "replicated_nodes"
        action = "scale_up"
        active_patterns = slot.get("accepted_patterns") or slot.get("default_patterns", [])
        notes = policy["scale_up_strategy"]
    population_per_node = people / desired_nodes if desired_nodes else 0
    return {
        "slot": slot.get("id", ""),
        "domain": slot.get("domain", ""),
        "tier": tier,
        "mode": mode,
        "action": action,
        "desired_nodes": desired_nodes,
        "population_per_node": round(population_per_node, 3),
        "headroom_per_node": round(maximum - population_per_node, 3),
        "active_patterns": active_patterns,
        "node_policy": {
            "minimum_population_per_node": minimum,
            "preferred_population_per_node": preferred,
            "maximum_population_per_node": maximum,
            "stateful": bool(policy.get("stateful", True)),
            "provisional": True,
        },
        "notes": notes,
        "provisional": True,
    }


def _hotspots(target_results: list[dict[str, Any]]) -> list[dict[str, Any]]:
    hotspots = []
    for target in target_results:
        people = target["people"]
        for slot in target["slot_results"]:
            if slot["mode"] == "missing_policy":
                hotspots.append(_hotspot("missing_node_policy", "fail", slot["slot"], f"No node policy exists at {people} people."))
            if slot["mode"] == "seed_or_minimal":
                hotspots.append(
                    _hotspot(
                        "below_node_minimum",
                        "warn",
                        f"{people}:{slot['slot']}",
                        f"{slot['slot']} is below its minimum node size and should use scale-down seed/default patterns.",
                    )
                )
            if slot["action"] == "near_capacity":
                hotspots.append(
                    _hotspot(
                        "near_node_capacity",
                        "warn",
                        f"{people}:{slot['slot']}",
                        f"{slot['slot']} is above preferred population but still inside one maximum-size node.",
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
        "Treat each module slot as a node pool with explicit scale-up and scale-down behavior.",
        "Prefer replicated village nodes over centralized megastructures once a slot exceeds maximum node population.",
        "Keep dignity floors local while federating capabilities that genuinely benefit from district, town, city, or regional scale.",
        "Use legal, governance, and review systems as thin boundary services; the primary design move is abundance that prevents avoidable scarcity conflict.",
    ]
    if any(hotspot["kind"] == "below_node_minimum" for hotspot in hotspots):
        recommendations.append("At micro-commons scale, run seed/default patterns instead of activating every village-scale module.")
    if any(hotspot["kind"] == "near_node_capacity" for hotspot in hotspots):
        recommendations.append("At 150-person scale, watch near-capacity slots and pre-plan the second node before adding residents.")
    return recommendations


def _status(hotspots: list[dict[str, Any]]) -> str:
    if any(hotspot["severity"] == "fail" for hotspot in hotspots):
        return "not_ready"
    if hotspots:
        return "ready_with_warnings"
    return "ready"
