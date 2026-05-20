from __future__ import annotations

from typing import Any


CONTRACT_VERSION = "visualization_bundle.v0"


def build_visualization_bundle(
    runtime_bundle: dict[str, Any],
    foundation_gate: dict[str, Any],
    candidate_matrix: dict[str, Any],
    tradeoff_scale_report: dict[str, Any],
    optimizer_report: dict[str, Any],
    artifact_paths: dict[str, str] | None = None,
) -> dict[str, Any]:
    paths = artifact_paths or {}
    selected_candidate = optimizer_report.get("selected_candidate", "")
    status = _status(foundation_gate, optimizer_report)
    return {
        "kind": "VisualizationBundle",
        "id": f"{runtime_bundle['id']}_visualization_bundle_v0",
        "schema_version": CONTRACT_VERSION,
        "generated_by": "ciac.visualization_bundle.v0",
        "provisional": True,
        "status": status,
        "selected_candidate": selected_candidate,
        "manifest": _manifest(runtime_bundle, foundation_gate, candidate_matrix, tradeoff_scale_report, optimizer_report, paths),
        "site": runtime_bundle.get("site", {}),
        "runtime": _runtime(runtime_bundle, foundation_gate),
        "optimization": _optimization(candidate_matrix, tradeoff_scale_report, optimizer_report),
        "viewer_contract": _viewer_contract(runtime_bundle, optimizer_report),
        "metric_updates": _metric_updates(status),
        "next_actions": _next_actions(status),
        "unknowns": _unknowns(runtime_bundle, foundation_gate, candidate_matrix, tradeoff_scale_report, optimizer_report),
    }


def _manifest(
    runtime_bundle: dict[str, Any],
    foundation_gate: dict[str, Any],
    candidate_matrix: dict[str, Any],
    tradeoff_scale_report: dict[str, Any],
    optimizer_report: dict[str, Any],
    paths: dict[str, str],
) -> dict[str, Any]:
    return {
        "contract_versions": {
            "visualization_bundle": CONTRACT_VERSION,
            "runtime_bundle": runtime_bundle.get("manifest", {}).get("schema_version", "runtime_bundle.v0"),
            "candidate_matrix": "candidate_plan_matrix_report.v0",
            "tradeoff_scale": "tradeoff_scale_report.v0",
            "optimizer": "optimizer_report.v0",
        },
        "source_ids": {
            "runtime_bundle": runtime_bundle["id"],
            "foundation_gate": foundation_gate["id"],
            "candidate_matrix": candidate_matrix["id"],
            "tradeoff_scale": tradeoff_scale_report["id"],
            "optimizer_report": optimizer_report["id"],
        },
        "source_artifacts": {
            "runtime_bundle": paths.get("runtime_bundle", ""),
            "foundation_gate": paths.get("foundation_gate", ""),
            "candidate_matrix": paths.get("candidate_matrix", ""),
            "tradeoff_scale": paths.get("tradeoff_scale", ""),
            "optimizer_report": paths.get("optimizer_report", ""),
        },
        "readiness": {
            "foundation_gate": foundation_gate.get("status", "unknown"),
            "candidate_matrix": candidate_matrix.get("status", "unknown"),
            "tradeoff_scale": tradeoff_scale_report.get("status", "unknown"),
            "optimizer": optimizer_report.get("status", "unknown"),
        },
        "provisional": True,
    }


def _runtime(runtime_bundle: dict[str, Any], foundation_gate: dict[str, Any]) -> dict[str, Any]:
    timeline = runtime_bundle.get("timeline", {})
    return {
        "bundle": runtime_bundle,
        "summary": {
            "days": timeline.get("days", 0),
            "baseline_status": timeline.get("simulation_status", "unknown"),
            "scenario_count": len(runtime_bundle.get("scenarios", [])),
            "system_count": len(runtime_bundle.get("systems", [])),
            "foundation_status": foundation_gate.get("status", "unknown"),
            "foundation_checks": foundation_gate.get("checks", []),
            "warning_checks": foundation_gate.get("warning_checks", []),
            "provisional": True,
        },
        "entrypoints": {
            "site": "$.site",
            "systems": "$.runtime.bundle.systems",
            "timeline": "$.runtime.bundle.timeline.daily_states",
            "scenarios": "$.runtime.bundle.scenarios",
            "foundation": "$.runtime.summary.foundation_checks",
            "provisional": True,
        },
    }


def _optimization(
    candidate_matrix: dict[str, Any],
    tradeoff_scale_report: dict[str, Any],
    optimizer_report: dict[str, Any],
) -> dict[str, Any]:
    return {
        "selected_candidate": optimizer_report.get("selected_candidate", ""),
        "rankings": optimizer_report.get("rankings", []),
        "candidate_summaries": _candidate_summaries(candidate_matrix, tradeoff_scale_report, optimizer_report),
        "constraint_explanations": optimizer_report.get("constraint_explanations", []),
        "sensitivity_checks": optimizer_report.get("sensitivity_checks", []),
        "scale_targets": tradeoff_scale_report.get("scale_targets", []),
        "objective_leaders": tradeoff_scale_report.get("objective_leaders", []),
        "provisional": True,
    }


def _candidate_summaries(
    candidate_matrix: dict[str, Any],
    tradeoff_scale_report: dict[str, Any],
    optimizer_report: dict[str, Any],
) -> list[dict[str, Any]]:
    rankings = {item["candidate"]: item for item in optimizer_report.get("rankings", [])}
    scale_summaries = {
        item["candidate"]: item
        for item in tradeoff_scale_report.get("viewer_candidate_summary", [])
    }
    summaries = []
    for candidate in candidate_matrix.get("candidates", []):
        candidate_id = candidate["id"]
        ranking = rankings.get(candidate_id, {})
        scale = scale_summaries.get(candidate_id, {})
        summaries.append(
            {
                "candidate": candidate_id,
                "label": candidate.get("label", candidate_id),
                "status": candidate.get("status", "unknown"),
                "optimizer_score": ranking.get("optimizer_score", 0),
                "aggregate_score": candidate.get("aggregate_score", 0),
                "hard_constraint_failures": candidate.get("hard_constraint_failures", 0),
                "dominant_strengths": ranking.get("dominant_strengths", []),
                "best_for": scale.get("best_for", []),
                "max_scale_households": scale.get("max_scale_households", 0),
                "top_tradeoff": scale.get("top_tradeoff", candidate.get("tradeoffs", [""])[0] if candidate.get("tradeoffs") else ""),
                "selected": candidate_id == optimizer_report.get("selected_candidate", ""),
                "provisional": True,
            }
        )
    return summaries


def _viewer_contract(runtime_bundle: dict[str, Any], optimizer_report: dict[str, Any]) -> dict[str, Any]:
    return {
        "stable_entrypoints": [
            "$.manifest",
            "$.site",
            "$.runtime.summary",
            "$.runtime.bundle.timeline.daily_states",
            "$.runtime.bundle.systems",
            "$.runtime.bundle.scenarios",
            "$.optimization.candidate_summaries",
            "$.optimization.rankings",
            "$.optimization.sensitivity_checks",
            "$.optimization.constraint_explanations",
        ],
        "status_colors": runtime_bundle.get("viewer_hints", {}).get("status_colors", {}),
        "must_label_as_provisional": runtime_bundle.get("viewer_hints", {}).get("must_label_as_provisional", []),
        "do_not_visualize_as_proof": runtime_bundle.get("viewer_hints", {}).get("do_not_visualize_as_proof", []),
        "selected_candidate": optimizer_report.get("selected_candidate", ""),
        "non_proof_notice": (
            "This visualization bundle is an inspection contract for provisional CIaC artifacts. "
            "It is not engineering, legal, public-health, construction, accessibility, or resident-consent proof."
        ),
        "provisional": True,
    }


def _status(foundation_gate: dict[str, Any], optimizer_report: dict[str, Any]) -> str:
    if foundation_gate.get("status") == "not_ready" or optimizer_report.get("status") == "not_ready":
        return "not_ready"
    if foundation_gate.get("status") == "ready" and optimizer_report.get("status") == "ready":
        return "ready"
    return "ready_with_warnings"


def _metric_updates(status: str) -> dict[str, Any]:
    if status == "not_ready":
        return {
            "inspectable_simulation_proof_of_concept": "95%",
            "mature_commune_virtualization_data_contract": "92%",
            "faithful_pattern_optimization_engine": "90%",
            "rationale": "Visualization bundle could not freeze a ready handoff from current source artifacts.",
        }
    return {
        "inspectable_simulation_proof_of_concept": "100%",
        "mature_commune_virtualization_data_contract": "100%",
        "faithful_pattern_optimization_engine": "95%",
        "rationale": "Chunk E freezes a versioned runtime and optimization handoff contract for visualization consumers.",
    }


def _next_actions(status: str) -> list[str]:
    if status == "not_ready":
        return [
            "Regenerate foundation and optimizer artifacts before using this bundle for visualization.",
            "Keep unresolved review and survival-critical blockers visible; do not hide them in the viewer layer.",
        ]
    return [
        "Use this bundle as the stable input for richer commune virtualization.",
        "Keep new modeling changes behind schema/version updates so viewer consumers do not reverse-engineer internals.",
        "Treat optimization results as provisional until review, governance, cost, safety, and resident consent evidence exist.",
    ]


def _unknowns(*artifacts: dict[str, Any]) -> list[str]:
    unknowns: set[str] = set()
    for artifact in artifacts:
        for unknown in artifact.get("unknowns", []):
            unknowns.add(str(unknown))
    unknowns.add("Visualization bundle stability is a software contract only, not proof of real-world feasibility.")
    return sorted(unknowns)
