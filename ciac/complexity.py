from __future__ import annotations

from collections import Counter, defaultdict
from typing import Any


DEFAULT_INTERFACE_WARNING_THRESHOLD = 50
DEFAULT_PATTERN_DEPENDENCY_WARNING_THRESHOLD = 6
DEFAULT_REVIEW_WARNING_THRESHOLD = 4
DEFAULT_RECURRING_LABOR_WARNING_THRESHOLD = 40.0


def generate_complexity_report(
    module_registry: dict[str, Any],
    patterns: list[dict[str, Any]] | dict[str, dict[str, Any]],
) -> dict[str, Any]:
    bundles = module_registry.get("interface_bundles", {})
    pattern_list = list(patterns.values()) if isinstance(patterns, dict) else patterns
    slots = module_registry.get("slots", [])
    slot_tiers = _slot_tiers(module_registry)
    pattern_by_id = {pattern.get("id", ""): pattern for pattern in pattern_list}

    slot_results = [
        _slot_result(slot, bundles, slot_tiers.get(slot.get("id", ""), "unclassified"), pattern_by_id)
        for slot in slots
    ]
    pattern_results = [_pattern_result(pattern) for pattern in pattern_list]
    bundle_results = _bundle_results(bundles, slots)
    registry_summary = _registry_summary(slot_results, bundle_results)
    pattern_summary = _pattern_summary(pattern_results)
    hotspots = _hotspots(slot_results, pattern_results)
    status = _status(hotspots)

    return {
        "kind": "ComplexityReport",
        "id": f"{module_registry.get('id', 'module_registry')}_complexity_report",
        "generated_by": "ciac.complexity.v0",
        "provisional": True,
        "status": status,
        "module_registry": module_registry.get("id", ""),
        "registry_summary": registry_summary,
        "pattern_summary": pattern_summary,
        "bundle_results": bundle_results,
        "slot_results": slot_results,
        "pattern_results": pattern_results,
        "hotspots": hotspots,
        "recommendations": _recommendations(hotspots, registry_summary),
        "unknowns": [
            "Complexity scores are structural indicators, not proof that a module is too complicated in real life.",
            "Interface bundles are canonical contract surfaces; existing direct interfaces remain authoritative until migrated.",
            "Labor and dependency totals are only as accurate as the authored pattern metadata.",
        ],
    }


def _slot_tiers(module_registry: dict[str, Any]) -> dict[str, str]:
    tiers: dict[str, str] = {}
    for tier_id, slot_ids in module_registry.get("module_tiers", {}).items():
        for slot_id in slot_ids:
            tiers[slot_id] = tier_id
    return tiers


def _slot_result(
    slot: dict[str, Any],
    bundles: dict[str, Any],
    tier: str,
    pattern_by_id: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    direct_interfaces = list(slot.get("required_interfaces", []))
    bundle_ids = list(slot.get("required_interface_bundles", []))
    bundled_interfaces = _interfaces_from_bundles(bundle_ids, bundles)
    effective_interfaces = sorted(set(direct_interfaces).union(bundled_interfaces))
    default_pattern_ids = list(slot.get("default_patterns", []))
    accepted_pattern_ids = list(slot.get("accepted_patterns", []))
    default_patterns = [pattern_by_id[pattern_id] for pattern_id in default_pattern_ids if pattern_id in pattern_by_id]
    accepted_patterns = [pattern_by_id[pattern_id] for pattern_id in accepted_pattern_ids if pattern_id in pattern_by_id]
    related_patterns = _unique_patterns([*default_patterns, *accepted_patterns])
    recurring_labor = sum(_metric(pattern, "recurring_labor_hours_per_week") for pattern in related_patterns)
    build_labor = sum(_metric(pattern, "build_labor_hours") for pattern in related_patterns)
    external_dependencies = sum(_dependency_count(pattern, "external") for pattern in related_patterns)
    pattern_dependencies = sum(_dependency_count(pattern, "pattern") for pattern in related_patterns)
    review_dependencies = sum(_review_dependency_count(pattern) for pattern in related_patterns)

    return {
        "slot": slot.get("id", ""),
        "domain": slot.get("domain", ""),
        "tier": tier,
        "direct_required_interfaces": len(direct_interfaces),
        "required_interface_bundles": bundle_ids,
        "bundle_interface_count": len(bundled_interfaces),
        "effective_required_interfaces": len(effective_interfaces),
        "bundle_coverage_ratio": _ratio(len(set(direct_interfaces).intersection(bundled_interfaces)), len(direct_interfaces)),
        "default_patterns": default_pattern_ids,
        "accepted_patterns": accepted_pattern_ids,
        "related_pattern_count": len(related_patterns),
        "pattern_dependencies": pattern_dependencies,
        "external_dependencies": external_dependencies,
        "review_dependencies": review_dependencies,
        "build_labor_hours": round(build_labor, 3),
        "recurring_labor_hours_per_week": round(recurring_labor, 3),
        "scaling_basis": slot.get("scaling_basis", ""),
        "provisional": True,
    }


def _interfaces_from_bundles(bundle_ids: list[str], bundles: dict[str, Any]) -> list[str]:
    interfaces: list[str] = []
    for bundle_id in bundle_ids:
        bundle = bundles.get(bundle_id, {})
        interfaces.extend(bundle.get("interfaces", []))
    return interfaces


def _unique_patterns(patterns: list[dict[str, Any]]) -> list[dict[str, Any]]:
    seen = set()
    unique = []
    for pattern in patterns:
        pattern_id = pattern.get("id")
        if pattern_id and pattern_id not in seen:
            seen.add(pattern_id)
            unique.append(pattern)
    return unique


def _pattern_result(pattern: dict[str, Any]) -> dict[str, Any]:
    return {
        "pattern": pattern.get("id", ""),
        "scale": pattern.get("scale", ""),
        "categories": pattern.get("mdl_categories", []),
        "dependency_count": len(pattern.get("dependencies", [])),
        "pattern_dependencies": _dependency_count(pattern, "pattern"),
        "external_dependencies": _dependency_count(pattern, "external"),
        "review_dependencies": _review_dependency_count(pattern),
        "build_labor_hours": _metric(pattern, "build_labor_hours"),
        "recurring_labor_hours_per_week": _metric(pattern, "recurring_labor_hours_per_week"),
        "maintenance_burden": _metric(pattern, "maintenance_burden"),
        "commons_owned": pattern.get("governance", {}).get("owner") == "commons",
        "has_scaling_policy": bool(pattern.get("optimization", {}).get("scaling")),
        "provisional": True,
    }


def _bundle_results(bundles: dict[str, Any], slots: list[dict[str, Any]]) -> list[dict[str, Any]]:
    references: dict[str, list[str]] = defaultdict(list)
    for slot in slots:
        for bundle_id in slot.get("required_interface_bundles", []):
            references[bundle_id].append(slot.get("id", ""))
    return [
        {
            "bundle": bundle_id,
            "interface_count": len(bundle.get("interfaces", [])),
            "referenced_by_slots": sorted(references.get(bundle_id, [])),
            "reference_count": len(references.get(bundle_id, [])),
            "description": bundle.get("description", ""),
            "provisional": True,
        }
        for bundle_id, bundle in sorted(bundles.items())
    ]


def _registry_summary(slot_results: list[dict[str, Any]], bundle_results: list[dict[str, Any]]) -> dict[str, Any]:
    direct_interface_count = sum(slot["direct_required_interfaces"] for slot in slot_results)
    bundle_reference_count = sum(len(slot["required_interface_bundles"]) for slot in slot_results)
    bundle_interface_count = sum(slot["bundle_interface_count"] for slot in slot_results)
    effective_interface_count = sum(slot["effective_required_interfaces"] for slot in slot_results)
    tier_counts = Counter(slot["tier"] for slot in slot_results)
    return {
        "slot_count": len(slot_results),
        "bundle_count": len(bundle_results),
        "bundle_reference_count": bundle_reference_count,
        "direct_required_interface_entries": direct_interface_count,
        "bundled_interface_entries": bundle_interface_count,
        "effective_required_interface_entries": effective_interface_count,
        "average_direct_interfaces_per_slot": round(_ratio(direct_interface_count, len(slot_results)), 3),
        "average_effective_interfaces_per_slot": round(_ratio(effective_interface_count, len(slot_results)), 3),
        "tiers": dict(sorted(tier_counts.items())),
        "provisional": True,
    }


def _pattern_summary(pattern_results: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "pattern_count": len(pattern_results),
        "pattern_dependency_entries": sum(pattern["pattern_dependencies"] for pattern in pattern_results),
        "external_dependency_entries": sum(pattern["external_dependencies"] for pattern in pattern_results),
        "review_dependency_entries": sum(pattern["review_dependencies"] for pattern in pattern_results),
        "build_labor_hours": round(sum(pattern["build_labor_hours"] for pattern in pattern_results), 3),
        "recurring_labor_hours_per_week": round(sum(pattern["recurring_labor_hours_per_week"] for pattern in pattern_results), 3),
        "commons_owned_patterns": sum(1 for pattern in pattern_results if pattern["commons_owned"]),
        "patterns_with_scaling_policy": sum(1 for pattern in pattern_results if pattern["has_scaling_policy"]),
        "provisional": True,
    }


def _hotspots(slot_results: list[dict[str, Any]], pattern_results: list[dict[str, Any]]) -> list[dict[str, Any]]:
    hotspots: list[dict[str, Any]] = []
    for slot in slot_results:
        if slot["direct_required_interfaces"] > DEFAULT_INTERFACE_WARNING_THRESHOLD:
            hotspots.append(
                _hotspot(
                    "slot_interface_surface",
                    "warn",
                    slot["slot"],
                    f"{slot['direct_required_interfaces']} direct interfaces exceed the {DEFAULT_INTERFACE_WARNING_THRESHOLD} interface review threshold.",
                )
            )
        if slot["recurring_labor_hours_per_week"] > DEFAULT_RECURRING_LABOR_WARNING_THRESHOLD:
            hotspots.append(
                _hotspot(
                    "slot_labor_burden",
                    "warn",
                    slot["slot"],
                    f"{slot['recurring_labor_hours_per_week']} recurring hours/week exceed the {DEFAULT_RECURRING_LABOR_WARNING_THRESHOLD} hour review threshold.",
                )
            )
    for pattern in pattern_results:
        if pattern["dependency_count"] > DEFAULT_PATTERN_DEPENDENCY_WARNING_THRESHOLD:
            hotspots.append(
                _hotspot(
                    "pattern_dependency_fanout",
                    "warn",
                    pattern["pattern"],
                    f"{pattern['dependency_count']} dependencies exceed the {DEFAULT_PATTERN_DEPENDENCY_WARNING_THRESHOLD} dependency review threshold.",
                )
            )
        if pattern["review_dependencies"] > DEFAULT_REVIEW_WARNING_THRESHOLD:
            hotspots.append(
                _hotspot(
                    "pattern_review_surface",
                    "warn",
                    pattern["pattern"],
                    f"{pattern['review_dependencies']} review dependencies exceed the {DEFAULT_REVIEW_WARNING_THRESHOLD} review threshold.",
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


def _recommendations(hotspots: list[dict[str, Any]], registry_summary: dict[str, Any]) -> list[str]:
    recommendations = [
        "Keep domain modules separate, but migrate repeated privacy, review, labor, role, dashboard, and scenario fields into reusable interface bundles.",
        "Model meta-modules as observers or coordinators where possible instead of adding hard compile-time dependencies.",
        "Use module tiers when comparing scale pressure so floor, operating, capacity, and meta systems are not averaged together.",
    ]
    if registry_summary["direct_required_interface_entries"] > 250:
        recommendations.insert(0, "Prioritize registry simplification: the direct interface surface is large enough to drift without bundle discipline.")
    if any(hotspot["kind"] == "slot_labor_burden" for hotspot in hotspots):
        recommendations.append("Run labor reduction work against the highest recurring-hour slots before adding new amenities.")
    return recommendations


def _status(hotspots: list[dict[str, Any]]) -> str:
    if any(hotspot["severity"] == "fail" for hotspot in hotspots):
        return "blocked"
    if hotspots:
        return "needs_simplification"
    return "manageable"


def _dependency_count(pattern: dict[str, Any], kind: str) -> int:
    return sum(1 for dependency in pattern.get("dependencies", []) if dependency.get("kind") == kind)


def _review_dependency_count(pattern: dict[str, Any]) -> int:
    count = 0
    for storage in pattern.get("simulation", {}).get("storage", []):
        quality = storage.get("quality", {})
        if isinstance(quality, dict) and quality.get("review_dependency"):
            count += 1
    for gate in pattern.get("optimization", {}).get("gates", []):
        if gate.get("review_dependency"):
            count += 1
    return count


def _metric(pattern: dict[str, Any], key: str) -> float:
    value = pattern.get("metrics", {}).get(key, 0)
    if isinstance(value, (int, float)):
        return float(value)
    return 0.0


def _ratio(numerator: int | float, denominator: int | float) -> float:
    if not denominator:
        return 0.0
    return float(numerator) / float(denominator)
