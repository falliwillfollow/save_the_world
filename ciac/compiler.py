from __future__ import annotations

from collections import defaultdict
from pathlib import Path
from typing import Any

from .graph import dependency_order
from .io import iter_data_files, load_data
from .models import MissingDependency
from .validation import validate_data, validate_pattern_library


class CompileError(ValueError):
    def __init__(self, message: str, plan: dict[str, Any] | None = None):
        super().__init__(message)
        self.plan = plan


def load_patterns(pattern_dir: str | Path) -> dict[str, dict[str, Any]]:
    patterns: list[dict[str, Any]] = []
    for data_file in iter_data_files(pattern_dir):
        data = load_data(data_file)
        if data.get("kind") == "CivicPattern":
            report = validate_data(data, str(data_file))
            if not report.ok:
                details = "; ".join(f"{issue.path}: {issue.message}" for issue in report.issues)
                raise CompileError(f"Invalid pattern {data_file}: {details}")
            patterns.append(data)

    library_issues = validate_pattern_library(patterns)
    errors = [issue for issue in library_issues if issue.severity == "error"]
    if errors:
        details = "; ".join(f"{issue.path}: {issue.message}" for issue in errors)
        raise CompileError(f"Invalid pattern library: {details}")
    return {pattern["id"]: pattern for pattern in patterns}


def compile_plan(
    site_profile: dict[str, Any],
    patterns_by_id: dict[str, dict[str, Any]],
    seasonal_profile: dict[str, Any] | None = None,
    household_profile: dict[str, Any] | None = None,
    spatial_profile: dict[str, Any] | None = None,
) -> dict[str, Any]:
    site_report = validate_data(site_profile, site_profile.get("id", "<site-profile>"))
    if not site_report.ok:
        details = "; ".join(f"{issue.path}: {issue.message}" for issue in site_report.issues)
        raise CompileError(f"Invalid site profile: {details}")
    if seasonal_profile is not None:
        seasonal_report = validate_data(seasonal_profile, seasonal_profile.get("id", "<seasonal-profile>"))
        if not seasonal_report.ok:
            details = "; ".join(f"{issue.path}: {issue.message}" for issue in seasonal_report.issues)
            raise CompileError(f"Invalid seasonal profile: {details}")
        expected_profile = site_profile.get("seasonal_profile_id")
        if expected_profile and seasonal_profile["id"] != expected_profile:
            raise CompileError(f"Seasonal profile {seasonal_profile['id']} does not match site reference {expected_profile}")
        if seasonal_profile["climate_zone"] != site_profile["climate_zone"]:
            raise CompileError(
                f"Seasonal profile climate zone {seasonal_profile['climate_zone']} does not match site climate zone {site_profile['climate_zone']}"
            )
    if household_profile is not None:
        _validate_household_profile_for_site(site_profile, household_profile)
    if spatial_profile is not None:
        _validate_spatial_profile_for_site(site_profile, spatial_profile)

    selected_ids = site_profile.get("selected_patterns") or sorted(patterns_by_id)
    unknown_selected = sorted(pattern_id for pattern_id in selected_ids if pattern_id not in patterns_by_id)
    if unknown_selected:
        raise CompileError(f"Selected patterns not found: {', '.join(unknown_selected)}")

    missing = _missing_dependencies(site_profile, patterns_by_id, selected_ids)
    order = dependency_order(patterns_by_id, selected_ids)
    if spatial_profile is not None:
        _validate_spatial_profile_for_selection(spatial_profile, selected_ids)
    plan = _build_plan(site_profile, patterns_by_id, selected_ids, order, missing, seasonal_profile, household_profile, spatial_profile)

    critical_missing = [dep for dep in missing if dep.critical]
    if critical_missing:
        raise CompileError("Plan has unresolved survival-critical dependencies", plan)
    return plan


def _missing_dependencies(
    site_profile: dict[str, Any],
    patterns_by_id: dict[str, dict[str, Any]],
    selected_ids: list[str],
) -> list[MissingDependency]:
    selected_set = set(selected_ids)
    resolved_external = set(site_profile.get("resolved_external_dependencies", []))
    missing: list[MissingDependency] = []
    for pattern_id in selected_ids:
        pattern = patterns_by_id[pattern_id]
        for dep in pattern.get("dependencies", []):
            dep_id = dep["id"]
            dep_kind = dep["kind"]
            critical = bool(dep.get("critical"))
            if dep_kind == "pattern" and dep_id not in selected_set:
                missing.append(MissingDependency(pattern_id, dep_id, dep_kind, critical, dep.get("rationale", "")))
            elif dep_kind == "external" and dep_id not in resolved_external:
                missing.append(MissingDependency(pattern_id, dep_id, dep_kind, critical, dep.get("rationale", "")))
    return missing


def _build_plan(
    site_profile: dict[str, Any],
    patterns_by_id: dict[str, dict[str, Any]],
    selected_ids: list[str],
    order: list[str],
    missing: list[MissingDependency],
    seasonal_profile: dict[str, Any] | None,
    household_profile: dict[str, Any] | None,
    spatial_profile: dict[str, Any] | None,
) -> dict[str, Any]:
    phase_map: dict[str, list[dict[str, Any]]] = defaultdict(list)
    maintenance_calendar: list[dict[str, Any]] = []
    risk_register: list[dict[str, Any]] = []
    role_burden: dict[str, float] = defaultdict(float)
    resource_effects_by_pattern: dict[str, dict[str, float]] = {}
    critical_resources_by_pattern: dict[str, list[str]] = {}
    storage_by_pattern: dict[str, list[dict[str, Any]]] = {}
    capability_effects_by_pattern: dict[str, dict[str, Any]] = {}
    capability_metadata_by_pattern: dict[str, dict[str, Any]] = {}

    for pattern_id in order:
        pattern = patterns_by_id[pattern_id]
        phase_key = f"phase_{pattern['build_phase']}"
        phase_map[phase_key].append(
            {
                "pattern_id": pattern_id,
                "purpose": pattern["purpose"],
                "build_labor_hours": pattern["metrics"]["build_labor_hours"],
                "provisional": pattern["provisional"],
            }
        )

        for task in pattern["lifecycle"]["maintenance"]:
            maintenance_calendar.append(
                {
                    "pattern_id": pattern_id,
                    "task_id": task["id"],
                    "description": task["description"],
                    "interval": task["interval"],
                    "role": task["role"],
                    "estimated_hours": task["estimated_hours"],
                    "provisional": task.get("provisional", True),
                }
            )
            role_burden[task["role"]] += float(task["estimated_hours"])

        for mode in pattern["failure_modes"]:
            risk_register.append(
                {
                    "pattern_id": pattern_id,
                    "mode": mode["mode"],
                    "likelihood": mode["likelihood"],
                    "severity": mode["severity"],
                    "detection_method": mode["detection_method"],
                    "mitigation": mode["mitigation"],
                }
            )
        resource_effects_by_pattern[pattern_id] = pattern["simulation"]["resource_effects"]
        critical_resources_by_pattern[pattern_id] = pattern["simulation"]["critical_resources"]
        storage_by_pattern[pattern_id] = pattern["simulation"].get("storage", [])
        if pattern.get("capability_effects"):
            capability_effects_by_pattern[pattern_id] = pattern.get("capability_effects", {})
        capability_metadata_by_pattern[pattern_id] = {
            "name": pattern.get("name", pattern_id),
            "scale": pattern.get("scale", ""),
            "provisional": pattern.get("provisional", True),
        }

    phases = [
        {
            "phase": phase_key,
            "patterns": phase_map[phase_key],
        }
        for phase_key in sorted(phase_map)
    ]

    population = max(1, int(site_profile["population_target"]))
    recurring_labor = sum(patterns_by_id[pattern_id]["metrics"]["recurring_labor_hours_per_week"] for pattern_id in selected_ids)

    simulation_inputs: dict[str, Any] = {
        "resource_effects_by_pattern": resource_effects_by_pattern,
        "critical_resources_by_pattern": critical_resources_by_pattern,
        "storage_by_pattern": storage_by_pattern,
        "capability_effects_by_pattern": capability_effects_by_pattern,
        "capability_metadata_by_pattern": capability_metadata_by_pattern,
        "provisional": True,
    }
    if seasonal_profile is not None:
        simulation_inputs["seasonal_profile"] = seasonal_profile
    if household_profile is not None:
        simulation_inputs["household_profile"] = household_profile
    layout_graph = _layout_graph(site_profile, selected_ids, spatial_profile)

    return {
        "kind": "CompiledPlan",
        "id": f"{site_profile['id']}_compiled_v0",
        "source_site_profile": site_profile["id"],
        "generated_by": "ciac.compiler.v0",
        "provisional": True,
        "site_summary": {
            "acres": site_profile["acres"],
            "site_type": site_profile["site_type"],
            "climate_zone": site_profile["climate_zone"],
            "seasonal_profile_id": site_profile.get("seasonal_profile_id", ""),
            "household_profile_id": site_profile.get("household_profile_id", ""),
            "spatial_profile_id": site_profile.get("spatial_profile_id", ""),
            "households": site_profile["households"],
            "population_target": site_profile["population_target"],
        },
        "selected_patterns": selected_ids,
        "dependency_order": order,
        "missing_dependencies": [dep.to_dict() for dep in missing],
        "phases": phases,
        "maintenance_calendar": sorted(maintenance_calendar, key=lambda item: (item["role"], item["pattern_id"], item["task_id"])),
        "role_burden": {
            "weekly_hours_by_role": dict(sorted(role_burden.items())),
            "total_recurring_hours_per_week": recurring_labor,
            "recurring_hours_per_resident_per_week": recurring_labor / population,
        },
        "layout_graph": layout_graph,
        "risk_register": risk_register,
        "simulation_inputs": simulation_inputs,
        "promotion_status": "draft_not_validated_for_real_world_use",
    }


def _validate_household_profile_for_site(site_profile: dict[str, Any], household_profile: dict[str, Any]) -> None:
    household_report = validate_data(household_profile, household_profile.get("id", "<household-profile>"))
    if not household_report.ok:
        details = "; ".join(f"{issue.path}: {issue.message}" for issue in household_report.issues)
        raise CompileError(f"Invalid household profile: {details}")
    expected_profile = site_profile.get("household_profile_id")
    if expected_profile and household_profile["id"] != expected_profile:
        raise CompileError(f"Household profile {household_profile['id']} does not match site reference {expected_profile}")
    if household_profile["site_profile_id"] != site_profile["id"]:
        raise CompileError(f"Household profile is for {household_profile['site_profile_id']}, not {site_profile['id']}")
    if len(household_profile["households"]) != int(site_profile["households"]):
        raise CompileError("Household profile household count does not match site profile")
    if _household_profile_population(household_profile) != int(site_profile["population_target"]):
        raise CompileError("Household profile population does not match site profile population target")


def _household_profile_population(household_profile: dict[str, Any]) -> int:
    return sum(
        int(household["adults"]) + int(household["children"]) + int(household["elders"])
        for household in household_profile.get("households", [])
    )


def _validate_spatial_profile_for_site(site_profile: dict[str, Any], spatial_profile: dict[str, Any]) -> None:
    spatial_report = validate_data(spatial_profile, spatial_profile.get("id", "<spatial-profile>"))
    if not spatial_report.ok:
        details = "; ".join(f"{issue.path}: {issue.message}" for issue in spatial_report.issues)
        raise CompileError(f"Invalid spatial profile: {details}")
    expected_profile = site_profile.get("spatial_profile_id")
    if expected_profile and spatial_profile["id"] != expected_profile:
        raise CompileError(f"Spatial profile {spatial_profile['id']} does not match site reference {expected_profile}")
    if spatial_profile["site_profile_id"] != site_profile["id"]:
        raise CompileError(f"Spatial profile is for {spatial_profile['site_profile_id']}, not {site_profile['id']}")


def _validate_spatial_profile_for_selection(spatial_profile: dict[str, Any], selected_ids: list[str]) -> None:
    selected = set(selected_ids)
    zones = {zone["id"] for zone in spatial_profile["zones"]}
    placements = {placement["pattern_id"]: placement for placement in spatial_profile["placements"]}
    missing_placements = sorted(selected - set(placements))
    if missing_placements:
        raise CompileError(f"Spatial profile missing placements for selected patterns: {', '.join(missing_placements)}")
    extra_placements = sorted(set(placements) - selected)
    if extra_placements:
        raise CompileError(f"Spatial profile includes unselected pattern placements: {', '.join(extra_placements)}")
    for placement in spatial_profile["placements"]:
        if placement["zone_id"] not in zones:
            raise CompileError(f"Spatial placement {placement['pattern_id']} references unknown zone {placement['zone_id']}")
        for target in placement["adjacent_to"] + placement["separate_from"]:
            if target not in selected:
                raise CompileError(f"Spatial placement {placement['pattern_id']} references unknown selected pattern {target}")
    for route in spatial_profile["routes"]:
        if route["from_zone"] not in zones or route["to_zone"] not in zones:
            raise CompileError(f"Spatial route {route['id']} references unknown zone")


def _layout_graph(site_profile: dict[str, Any], selected_ids: list[str], spatial_profile: dict[str, Any] | None) -> dict[str, Any]:
    if spatial_profile is None:
        return {
            "kind": "LayoutGraph",
            "source_spatial_profile": "",
            "provisional": True,
            "zones": [],
            "nodes": [],
            "edges": [],
            "routes": [],
            "unresolved_spatial_issues": [
                "No spatial profile was provided; visual buildout has no placement, access, hazard, or adjacency data.",
            ],
        }

    placements = {placement["pattern_id"]: placement for placement in spatial_profile["placements"]}
    routes = spatial_profile["routes"]
    nodes = [
        _layout_node(placements[pattern_id])
        for pattern_id in selected_ids
    ]
    edges = _layout_edges(placements)
    issues = _spatial_issues(spatial_profile, placements, routes)
    return {
        "kind": "LayoutGraph",
        "source_spatial_profile": spatial_profile["id"],
        "site_profile": site_profile["id"],
        "provisional": spatial_profile.get("provisional", True),
        "zones": spatial_profile["zones"],
        "nodes": nodes,
        "edges": edges,
        "routes": routes,
        "unresolved_spatial_issues": issues,
        "unknowns": spatial_profile["unknowns"],
    }


def _layout_node(placement: dict[str, Any]) -> dict[str, Any]:
    return {
        "pattern_id": placement["pattern_id"],
        "zone_id": placement["zone_id"],
        "footprint_m2": placement["footprint_m2"],
        "access_needs": placement["access_needs"],
        "hazard_flags": placement["hazard_flags"],
        "notes": placement["notes"],
        "provisional": True,
    }


def _layout_edges(placements: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    edges: list[dict[str, Any]] = []
    seen: set[tuple[str, str, str]] = set()
    for source, placement in sorted(placements.items()):
        for target in placement["adjacent_to"]:
            key = tuple(sorted([source, target]) + ["adjacency"])
            if key not in seen:
                edges.append({"from": source, "to": target, "relationship": "adjacency", "provisional": True})
                seen.add(key)
        for target in placement["separate_from"]:
            key = tuple(sorted([source, target]) + ["separation"])
            if key not in seen:
                edges.append({"from": source, "to": target, "relationship": "separation", "provisional": True})
                seen.add(key)
    return sorted(edges, key=lambda item: (item["relationship"], item["from"], item["to"]))


def _spatial_issues(
    spatial_profile: dict[str, Any],
    placements: dict[str, dict[str, Any]],
    routes: list[dict[str, Any]],
) -> list[str]:
    issues: list[str] = []
    route_zones = {route["from_zone"] for route in routes} | {route["to_zone"] for route in routes}
    emergency_zones = {route["from_zone"] for route in routes if route["emergency_access"]} | {
        route["to_zone"] for route in routes if route["emergency_access"]
    }
    for pattern_id, placement in sorted(placements.items()):
        if "emergency_access" in placement["access_needs"] and placement["zone_id"] not in emergency_zones:
            issues.append(f"{pattern_id} needs emergency access but its zone has no emergency route.")
        if placement["access_needs"] and placement["zone_id"] not in route_zones:
            issues.append(f"{pattern_id} has access needs but its zone is not connected by any route.")
        for target in placement["separate_from"]:
            if placements[target]["zone_id"] == placement["zone_id"]:
                issues.append(f"{pattern_id} must be separated from {target}, but both are placed in {placement['zone_id']}.")
    issues.append("Spatial profile is provisional; survey, accessibility, emergency, utility, drainage, and code review remain unresolved.")
    return sorted(set(issues))
