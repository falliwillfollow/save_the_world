from __future__ import annotations

from typing import Any


def build_runtime_bundle(
    compiled_plan: dict[str, Any],
    simulation_run: dict[str, Any],
    scenario_runs: list[dict[str, Any]] | None = None,
    artifact_paths: dict[str, Any] | None = None,
) -> dict[str, Any]:
    scenarios = scenario_runs or []
    paths = artifact_paths or {}
    return {
        "kind": "RuntimeBundle",
        "id": f"{compiled_plan['id']}_runtime_bundle_v0",
        "generated_by": "ciac.runtime_export.v0",
        "provisional": True,
        "manifest": _manifest(compiled_plan, simulation_run, scenarios, paths),
        "site": _site(compiled_plan),
        "systems": _systems(compiled_plan, simulation_run),
        "timeline": _timeline(simulation_run),
        "scenarios": [_scenario_summary(scenario) for scenario in scenarios],
        "viewer_hints": _viewer_hints(),
        "unknowns": _unknowns(compiled_plan, simulation_run, scenarios),
    }


def _manifest(
    compiled_plan: dict[str, Any],
    simulation_run: dict[str, Any],
    scenarios: list[dict[str, Any]],
    paths: dict[str, Any],
) -> dict[str, Any]:
    return {
        "schema_version": "runtime_bundle.v0",
        "compiled_plan": compiled_plan["id"],
        "simulation_run": simulation_run["id"],
        "scenario_runs": [scenario["id"] for scenario in scenarios],
        "source_artifacts": {
            "compiled_plan": paths.get("compiled_plan", ""),
            "simulation": paths.get("simulation", ""),
            "scenarios": paths.get("scenarios", []),
        },
        "status": {
            "simulation": simulation_run["status"],
            "scenario_statuses": {scenario["scenario"]: scenario["status"] for scenario in scenarios},
        },
        "warnings": _manifest_warnings(compiled_plan, simulation_run, scenarios),
        "provisional": True,
    }


def _manifest_warnings(compiled_plan: dict[str, Any], simulation_run: dict[str, Any], scenarios: list[dict[str, Any]]) -> list[str]:
    warnings: list[str] = []
    warnings.extend(compiled_plan.get("layout_graph", {}).get("unresolved_spatial_issues", []))
    warnings.extend(simulation_run.get("bottlenecks", []))
    for scenario in scenarios:
        warnings.extend(f"{scenario['scenario']}:{item}" for item in scenario.get("bottlenecks", []))
    return sorted(set(warnings))


def _site(compiled_plan: dict[str, Any]) -> dict[str, Any]:
    layout = compiled_plan.get("layout_graph", {})
    return {
        "summary": compiled_plan["site_summary"],
        "layout_graph": layout,
        "zones": layout.get("zones", []),
        "routes": layout.get("routes", []),
        "unresolved_spatial_issues": layout.get("unresolved_spatial_issues", []),
        "provisional": True,
    }


def _systems(compiled_plan: dict[str, Any], simulation_run: dict[str, Any]) -> list[dict[str, Any]]:
    layout_nodes = {
        node["pattern_id"]: node
        for node in compiled_plan.get("layout_graph", {}).get("nodes", [])
    }
    failures_by_pattern: dict[str, list[dict[str, Any]]] = {}
    for failure in simulation_run.get("runtime_failures", []):
        failures_by_pattern.setdefault(failure["pattern_id"], []).append(failure)
    risk_register = compiled_plan.get("risk_register", [])
    critical_resources = compiled_plan.get("simulation_inputs", {}).get("critical_resources_by_pattern", {})
    systems = []
    for pattern_id in compiled_plan["selected_patterns"]:
        node = layout_nodes.get(pattern_id, {})
        systems.append(
            {
                "pattern_id": pattern_id,
                "zone_id": node.get("zone_id", ""),
                "footprint_m2": node.get("footprint_m2", 0),
                "access_needs": node.get("access_needs", []),
                "hazard_flags": node.get("hazard_flags", []),
                "critical_resources": critical_resources.get(pattern_id, []),
                "failure_modes": [
                    risk
                    for risk in risk_register
                    if risk["pattern_id"] == pattern_id
                ],
                "active_failure_count": len(failures_by_pattern.get(pattern_id, [])),
                "viewer_status": _system_status(pattern_id, simulation_run),
                "provisional": True,
            }
        )
    return systems


def _system_status(pattern_id: str, simulation_run: dict[str, Any]) -> str:
    if any(failure["pattern_id"] == pattern_id for failure in simulation_run.get("runtime_failures", [])):
        return "failure"
    if any(pattern_id in risk.get("pattern_id", "") for state in simulation_run.get("daily_states", []) for risk in state.get("active_risks", [])):
        return "risk"
    return "provisional"


def _timeline(simulation_run: dict[str, Any]) -> dict[str, Any]:
    return {
        "days": simulation_run["days"],
        "simulation_status": simulation_run["status"],
        "review_context": simulation_run.get("review_context", {}),
        "scenario_context": simulation_run.get("scenario_context", {}),
        "resource_balance": simulation_run["resource_balance"],
        "storage": simulation_run.get("storage", {}),
        "labor": simulation_run.get("labor", {}),
        "event_timeline": simulation_run.get("timeline", []),
        "daily_states": [_daily_state_for_viewer(state) for state in simulation_run.get("daily_states", [])],
        "provisional": True,
    }


def _daily_state_for_viewer(state: dict[str, Any]) -> dict[str, Any]:
    return {
        "day": state["day"],
        "season": state["season"],
        "resources": {
            resource: {
                "opening_balance": summary.get("opening_balance", summary["ending_balance"]),
                "production": summary.get("production", 0),
                "consumption": summary.get("consumption", 0),
                "raw_net": summary.get("raw_net", summary["net"]),
                "storage_release": summary.get("storage_release", 0),
                "storage_refill": summary.get("storage_refill", 0),
                "curtailment": summary.get("curtailment", 0),
                "ending_balance": summary["ending_balance"],
                "net": summary["net"],
                "status": summary["status"],
                "unmet_demand": summary["unmet_demand"],
            }
            for resource, summary in state["resources"].items()
        },
        "maintenance": {
            "required_hours": state["maintenance_state"]["required_hours"],
            "deferred_count": state["maintenance_state"]["deferred_count"],
            "backlog_count": state["maintenance_state"]["backlog_count"],
            "status": state["maintenance_state"]["status"],
        },
        "labor": state.get("labor", {}),
        "scenario_events": state.get("scenario_events", []),
        "storage": {
            resource: {
                "opening_total": summary.get("opening_total", summary["ending_total"]),
                "released": summary.get("released", 0),
                "refilled": summary.get("refilled", 0),
                "curtailed": summary.get("curtailed", 0),
                "quality_loss": summary.get("quality_loss", 0),
                "ending_total": summary["ending_total"],
                "capacity": summary["capacity"],
                "reserve_floor": summary["reserve_floor"],
                "percent_full": summary.get("percent_full", 0),
                "quantity_status": summary.get("quantity_status", summary["status"]),
                "quality_status": summary.get("quality_status", "pass"),
                "status": summary["status"],
            }
            for resource, summary in state.get("storage_state", {}).get("resources", {}).items()
        },
        "storage_recovery_tasks": state.get("storage_state", {}).get("recovery_tasks", []),
        "active_failures": [
            {
                "pattern_id": failure["pattern_id"],
                "mode": failure["mode"],
                "severity": failure["severity"],
            }
            for failure in state.get("active_failures", [])
        ],
        "unmet_needs": state.get("unmet_needs", []),
    }


def _scenario_summary(scenario: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": scenario["id"],
        "scenario": scenario["scenario"],
        "status": scenario["status"],
        "days": scenario["days"],
        "affected_resources": scenario.get("affected_resources", []),
        "runtime_failures": scenario.get("runtime_failures", []),
        "failure_timeline": scenario.get("failure_timeline", []),
        "resource_balance": scenario.get("resource_balance", {}),
        "review_context": scenario.get("review_context", {}),
        "survival_critical_gate_failures": scenario.get("survival_critical_gate_failures", []),
        "provisional": True,
    }


def _viewer_hints() -> dict[str, Any]:
    return {
        "status_colors": {
            "pass": "#2e7d32",
            "warn": "#ed9c22",
            "fail": "#c62828",
            "provisional": "#607d8b",
            "failure": "#8e24aa",
            "risk": "#d84315",
        },
        "safe_to_visualize": [
            "zones",
            "routes",
            "pattern placements",
            "daily resource trends",
            "maintenance backlog",
            "runtime failures",
            "unmet needs",
        ],
        "must_label_as_provisional": [
            "resource quantities",
            "labor capacity",
            "household demand",
            "spatial layout",
            "failure effects",
            "scenario outcomes",
        ],
        "do_not_visualize_as_proof": [
            "legal permission",
            "engineering safety",
            "water or sanitation safety",
            "resident consent",
            "accessibility compliance",
            "construction readiness",
        ],
    }


def _unknowns(compiled_plan: dict[str, Any], simulation_run: dict[str, Any], scenarios: list[dict[str, Any]]) -> list[str]:
    unknowns = set(compiled_plan.get("layout_graph", {}).get("unknowns", []))
    unknowns.update(simulation_run.get("unknowns", []))
    for scenario in scenarios:
        unknowns.update(scenario.get("unknowns", []))
    unknowns.add("Runtime bundle is a visualization contract, not a safety, legal, engineering, or consent artifact.")
    return sorted(unknowns)
