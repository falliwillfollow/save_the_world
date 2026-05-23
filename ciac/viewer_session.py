from __future__ import annotations

from pathlib import Path
from typing import Any

from .io import load_data, write_json


def empty_viewer_run_report() -> dict[str, Any]:
    return {
        "kind": "ViewerRunReport",
        "id": "micro_commons_viewer_session_report",
        "generated_by": "ciac.viewer_session.v0",
        "provisional": True,
        "status": "no_runs",
        "active_population": 0,
        "run_count": 0,
        "runs": [],
        "unknowns": [
            "Viewer run reports record browser-triggered inspection cycles and the UI run context used for backend regeneration.",
            "A completed viewer year records the population and topology visible in the web app at completion time.",
            "When served through ciac viewer-server, a completed webapp year regenerates the population-specific simulator, topology, and reporting artifacts before returning the response.",
        ],
    }


def append_viewer_run_event(report: dict[str, Any] | None, event: dict[str, Any]) -> dict[str, Any]:
    current = report if isinstance(report, dict) and report.get("kind") == "ViewerRunReport" else empty_viewer_run_report()
    runs = list(current.get("runs", []))
    normalized = _normalize_event(event, len(runs) + 1)
    runs.append(normalized)
    active_population = int(normalized.get("population", 0))
    return {
        **current,
        "status": "runs_recorded",
        "active_population": active_population,
        "run_count": len(runs),
        "runs": runs,
    }


def append_viewer_run_event_to_path(path: str | Path, event: dict[str, Any]) -> dict[str, Any]:
    target = Path(path)
    report = load_data(target) if target.exists() else empty_viewer_run_report()
    updated = append_viewer_run_event(report, event)
    write_json(target, updated)
    return updated


def _normalize_event(event: dict[str, Any], fallback_index: int) -> dict[str, Any]:
    population = int(event.get("population", 0))
    total_nodes = int(event.get("total_nodes", 0))
    replicated_slots = int(event.get("replicated_slots", 0))
    scaled_down_slots = int(event.get("scaled_down_slots", 0))
    near_capacity_slots = int(event.get("near_capacity_slots", 0))
    return {
        "run_index": int(event.get("run_index") or fallback_index),
        "event_type": str(event.get("event_type") or "year_cycle_completed"),
        "completed_at": str(event.get("completed_at") or ""),
        "cycle_number": int(event.get("cycle_number", 1)),
        "population": population,
        "days": int(event.get("days", 0)),
        "bundle_id": str(event.get("bundle_id") or ""),
        "selected_candidate": str(event.get("selected_candidate") or ""),
        "topology_action": str(event.get("topology_action") or ""),
        "topology_status": str(event.get("topology_status") or ""),
        "total_nodes": total_nodes,
        "replicated_slots": replicated_slots,
        "scaled_down_slots": scaled_down_slots,
        "near_capacity_slots": near_capacity_slots,
        "tier_node_counts": dict(event.get("tier_node_counts") or {}),
        "provisional": True,
    }
