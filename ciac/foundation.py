from __future__ import annotations

from typing import Any


REQUIRED_DEMO_SCENARIOS = {
    "water": {"water_contamination_response_v2"},
    "food": {"crop_failure"},
    "energy": {"energy_outage_reserve_v2"},
}


def evaluate_foundation_gate(
    compiled_plan: dict[str, Any],
    baseline_simulation: dict[str, Any],
    runtime_bundle: dict[str, Any],
    replay_matrix: dict[str, Any],
    review_status: dict[str, Any] | None = None,
    comparisons: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    checks = [
        _baseline_check(baseline_simulation),
        _state_model_check(compiled_plan, baseline_simulation),
        _scenario_coverage_check(replay_matrix),
        _unmet_survival_demand_check(replay_matrix, comparisons or []),
        _runtime_bundle_check(runtime_bundle),
        _review_visibility_check(baseline_simulation, runtime_bundle, review_status),
        _warning_legibility_check(replay_matrix, runtime_bundle),
    ]
    status = _overall_status(checks)
    return {
        "kind": "FoundationGateReport",
        "id": f"{compiled_plan['id']}_foundation_gate",
        "compiled_plan": compiled_plan["id"],
        "generated_by": "ciac.foundation.v0",
        "provisional": True,
        "status": status,
        "ready_for_visual_buildout": status in {"ready", "ready_with_warnings"},
        "checks": checks,
        "artifact_summary": _artifact_summary(baseline_simulation, runtime_bundle, replay_matrix, review_status, comparisons or []),
        "stop_conditions": _stop_conditions(checks),
        "next_actions": _next_actions(status, checks),
        "unknowns": [
            "Foundation readiness means the simulation artifacts are inspectable; it is not safety, legal, engineering, health, or consent approval.",
            "Warnings can be acceptable when they are explicit, visible, and do not hide unmet survival demand.",
            "This report evaluates generated artifacts and inherits all provisional assumptions in those artifacts.",
        ],
    }


def _baseline_check(baseline_simulation: dict[str, Any]) -> dict[str, Any]:
    days = int(baseline_simulation.get("days", 0))
    status = baseline_simulation.get("status", "missing")
    failures = [
        resource
        for resource, summary in baseline_simulation.get("resource_ledger", {}).items()
        if float(summary.get("total_unmet_demand", 0.0)) > 0
    ]
    if status == "fail" or failures:
        return _check(
            "baseline_normal_year",
            "fail",
            f"Baseline status is {status}; unmet resources: {', '.join(failures) if failures else 'none'}.",
            "Fix the normal-year baseline before using CIaC for visual buildout.",
        )
    if days < 365:
        return _check(
            "baseline_normal_year",
            "warn",
            f"Baseline covers {days} day(s), below the 365-day foundation target.",
            "Regenerate the baseline simulation for 365 days.",
        )
    return _check(
        "baseline_normal_year",
        "pass",
        f"Baseline covers {days} day(s) with status {status} and no unmet tracked demand.",
        "No action needed for the foundation demo.",
    )


def _state_model_check(compiled_plan: dict[str, Any], baseline_simulation: dict[str, Any]) -> dict[str, Any]:
    ledger_resources = set(baseline_simulation.get("resource_ledger", {}))
    required_resources = {"water_liters", "food_servings", "energy_kwh", "sanitation_capacity", "labor_hours"}
    missing = sorted(required_resources - ledger_resources)
    storage_resources = set(baseline_simulation.get("storage", {}).get("resources", {}))
    has_households = bool(compiled_plan.get("simulation_inputs", {}).get("household_profile"))
    has_layout = bool(compiled_plan.get("layout_graph", {}).get("nodes"))
    if missing or not has_households or not has_layout:
        evidence = [
            f"missing ledger resources: {', '.join(missing) if missing else 'none'}",
            f"household profile embedded: {has_households}",
            f"layout graph embedded: {has_layout}",
        ]
        return _check(
            "minimum_state_model",
            "fail",
            "; ".join(evidence),
            "Compile with household and spatial profiles and ensure all minimum dignity resources are in the ledger.",
        )
    if not {"water_liters", "food_servings", "energy_kwh"}.issubset(storage_resources):
        return _check(
            "minimum_state_model",
            "warn",
            f"Ledger is complete, but storage resources are only: {', '.join(sorted(storage_resources))}.",
            "Keep reserve state explicit for water, food, and energy before richer visual buildout.",
        )
    return _check(
        "minimum_state_model",
        "pass",
        "Water, food, energy, sanitation, and labor have ledger state; household and spatial profiles are embedded.",
        "No action needed for the foundation demo.",
    )


def _scenario_coverage_check(replay_matrix: dict[str, Any]) -> dict[str, Any]:
    scenarios = {entry.get("scenario", "") for entry in replay_matrix.get("entries", replay_matrix.get("rankings", []))}
    missing_domains = [
        domain
        for domain, acceptable_ids in REQUIRED_DEMO_SCENARIOS.items()
        if not scenarios.intersection(acceptable_ids)
    ]
    if missing_domains:
        return _check(
            "stress_replay_coverage",
            "fail",
            f"Missing required demo replay domain(s): {', '.join(missing_domains)}.",
            "Regenerate replay comparisons and matrix with water, food/procurement, and energy stress replays.",
        )
    return _check(
        "stress_replay_coverage",
        "pass",
        f"Replay matrix covers required demo domains with scenarios: {', '.join(sorted(scenarios))}.",
        "No action needed for the foundation demo.",
    )


def _unmet_survival_demand_check(replay_matrix: dict[str, Any], comparisons: list[dict[str, Any]]) -> dict[str, Any]:
    failed = [entry["scenario"] for entry in replay_matrix.get("rankings", []) if entry.get("status") == "stress_failed"]
    unmet_entries = [
        entry["scenario"]
        for entry in replay_matrix.get("rankings", [])
        if float(entry.get("total_unmet_delta", 0.0)) > 0
    ]
    unmet_from_comparisons = [
        comparison.get("scenario_context", {}).get("id", "unknown")
        for comparison in comparisons
        if any(float(item.get("delta", 0.0)) > 0 for item in comparison.get("unmet_need_deltas", []))
    ]
    names = sorted(set(failed + unmet_entries + unmet_from_comparisons))
    if names:
        return _check(
            "stress_unmet_survival_demand",
            "fail",
            f"Stress replays still expose unmet tracked demand or stress failure in: {', '.join(names)}.",
            "Do not move to visual buildout until stress failures and hidden unmet demand are resolved or intentionally scoped out.",
        )
    if replay_matrix.get("status") == "stress_warn":
        return _check(
            "stress_unmet_survival_demand",
            "warn",
            "Replay matrix is stress_warn with zero unmet-demand delta.",
            "Warnings may be acceptable if they remain visible in the viewer and review packet.",
        )
    return _check(
        "stress_unmet_survival_demand",
        "pass",
        "Replay matrix has no stress failures and no unmet-demand delta.",
        "No action needed for the foundation demo.",
    )


def _runtime_bundle_check(runtime_bundle: dict[str, Any]) -> dict[str, Any]:
    daily_states = runtime_bundle.get("timeline", {}).get("daily_states", [])
    systems = runtime_bundle.get("systems", [])
    scenarios = runtime_bundle.get("scenarios", [])
    hints = runtime_bundle.get("viewer_hints", {})
    missing = []
    if not daily_states:
        missing.append("daily timeline")
    if not systems:
        missing.append("systems")
    if len(scenarios) < 3:
        missing.append("three scenario summaries")
    if not hints.get("do_not_visualize_as_proof"):
        missing.append("non-proof viewer hints")
    if missing:
        return _check(
            "runtime_viewer_contract",
            "fail",
            f"Runtime bundle is missing: {', '.join(missing)}.",
            "Regenerate the runtime bundle with baseline timeline, scenario summaries, systems, and viewer warnings.",
        )
    return _check(
        "runtime_viewer_contract",
        "pass",
        f"Runtime bundle has {len(daily_states)} daily state(s), {len(systems)} system(s), and {len(scenarios)} scenario summary item(s).",
        "No action needed for the foundation demo.",
    )


def _review_visibility_check(
    baseline_simulation: dict[str, Any],
    runtime_bundle: dict[str, Any],
    review_status: dict[str, Any] | None,
) -> dict[str, Any]:
    simulation_review = baseline_simulation.get("review_context", {})
    bundle_review = runtime_bundle.get("timeline", {}).get("review_context", {})
    blocked = set(simulation_review.get("blocked_domains", [])) | set(bundle_review.get("blocked_domains", []))
    register_status = review_status.get("status") if review_status else "missing"
    if not simulation_review and not review_status:
        return _check(
            "review_blocker_visibility",
            "fail",
            "No review status artifact or runtime review context was provided.",
            "Run ciac review and simulate with --review-status before visual buildout.",
        )
    if blocked or register_status == "missing_evidence":
        return _check(
            "review_blocker_visibility",
            "warn",
            f"Review status is {register_status}; blocked domains visible: {', '.join(sorted(blocked)) if blocked else 'none'}.",
            "Keep review blockers visible; do not present the visual layer as approval or safety evidence.",
        )
    return _check(
        "review_blocker_visibility",
        "pass",
        f"Review status is {register_status}; no blocked domains are visible in runtime context.",
        "No action needed for the foundation demo.",
    )


def _warning_legibility_check(replay_matrix: dict[str, Any], runtime_bundle: dict[str, Any]) -> dict[str, Any]:
    warning_text = " ".join(replay_matrix.get("summary", []) + runtime_bundle.get("manifest", {}).get("warnings", [])).lower()
    visible_warnings = []
    for phrase in ("food model is partial", "active failure days", "blocked review", "provisional"):
        if phrase in warning_text:
            visible_warnings.append(phrase)
    if not visible_warnings:
        return _check(
            "warning_legibility",
            "warn",
            "Foundation artifacts do not expose the expected limitation vocabulary.",
            "Make partial models, active failure windows, review blockers, and provisional status visible in reports or viewer output.",
        )
    return _check(
        "warning_legibility",
        "pass",
        f"Visible limitation signals include: {', '.join(sorted(set(visible_warnings)))}.",
        "No action needed for the foundation demo.",
    )


def _artifact_summary(
    baseline_simulation: dict[str, Any],
    runtime_bundle: dict[str, Any],
    replay_matrix: dict[str, Any],
    review_status: dict[str, Any] | None,
    comparisons: list[dict[str, Any]],
) -> dict[str, Any]:
    return {
        "baseline_simulation": baseline_simulation.get("id", ""),
        "baseline_days": int(baseline_simulation.get("days", 0)),
        "baseline_status": baseline_simulation.get("status", "missing"),
        "runtime_bundle": runtime_bundle.get("id", ""),
        "runtime_daily_state_count": len(runtime_bundle.get("timeline", {}).get("daily_states", [])),
        "runtime_scenario_count": len(runtime_bundle.get("scenarios", [])),
        "replay_matrix": replay_matrix.get("id", ""),
        "replay_matrix_status": replay_matrix.get("status", "missing"),
        "replay_comparison_count": len(comparisons) if comparisons else int(replay_matrix.get("comparison_count", 0)),
        "review_status": review_status.get("status", "not_provided") if review_status else "not_provided",
        "top_stressor": replay_matrix.get("top_stressor", {}).get("scenario", ""),
        "provisional": True,
    }


def _stop_conditions(checks: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "id": check["id"],
            "met": check["status"] in {"pass", "warn"},
            "status": check["status"],
            "evidence": check["evidence"],
        }
        for check in checks
    ]


def _next_actions(status: str, checks: list[dict[str, Any]]) -> list[str]:
    failed = [check for check in checks if check["status"] == "fail"]
    warned = [check for check in checks if check["status"] == "warn"]
    if failed:
        return [f"Fix {check['id']}: {check['remediation']}" for check in failed[:3]]
    if warned:
        return [
            "Treat this as ready with warnings, not as real-world approval.",
            "Before visual buildout, make warning states visible in the viewer and review packet.",
            f"First warning to inspect: {warned[0]['id']}.",
        ]
    return [
        "Freeze the current runtime JSON shape as the visual-buildout contract.",
        "Move to a minimal viewer demo that inspects baseline, water, food, and energy replay artifacts.",
    ]


def _overall_status(checks: list[dict[str, Any]]) -> str:
    if any(check["status"] == "fail" for check in checks):
        return "not_ready"
    if any(check["status"] == "warn" for check in checks):
        return "ready_with_warnings"
    return "ready"


def _check(check_id: str, status: str, evidence: str, remediation: str) -> dict[str, Any]:
    return {
        "id": check_id,
        "status": status,
        "evidence": evidence,
        "remediation": remediation,
        "provisional": True,
    }

