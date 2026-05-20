from __future__ import annotations

from typing import Any


STATUS_RANK = {
    "stable": 0,
    "stress_warn": 1,
    "stress_failed": 2,
}


def build_replay_matrix(comparisons: list[dict[str, Any]]) -> dict[str, Any]:
    if not comparisons:
        raise ValueError("At least one simulation comparison is required")
    entries = [_matrix_entry(comparison) for comparison in comparisons]
    rankings = sorted(entries, key=lambda item: (-float(item["stress_score"]), item["scenario"], item["comparison"]))
    status = _matrix_status(entries)
    return {
        "kind": "ReplayMatrixReport",
        "id": f"replay_matrix_{len(entries)}_comparisons",
        "generated_by": "ciac.replay_matrix.v0",
        "provisional": True,
        "status": status,
        "comparison_count": len(entries),
        "entries": entries,
        "rankings": rankings,
        "top_stressor": rankings[0],
        "summary": _summary(status, rankings),
        "unknowns": [
            "Replay matrix rankings compare generated comparison artifacts only; they do not verify scenario assumptions.",
            "Stress scores are coarse planning signals for prioritization, not probabilities or real-world risk ratings.",
            "A lower-ranked replay may still be unacceptable if it exposes legal, public-health, engineering, consent, or governance blockers.",
        ],
    }


def _matrix_entry(comparison: dict[str, Any]) -> dict[str, Any]:
    scenario = comparison.get("scenario_context", {}).get("id") or "normal_replay"
    total_unmet_delta = sum(max(0.0, float(item.get("delta", 0.0))) for item in comparison.get("unmet_need_deltas", []))
    blocked_review_count = (
        len(comparison.get("review_delta", {}).get("new_blocked_domains", []))
        + len(comparison.get("review_delta", {}).get("remaining_blocked_domains", []))
    )
    active_failure_day_delta = int(comparison.get("failure_day_delta", {}).get("delta", 0))
    emergency_hours = float(comparison.get("labor_delta", {}).get("scenario_emergency_hours", 0.0))
    recovery_blocked_delta = int(comparison.get("recovery_delta", {}).get("blocked_review_count_delta", 0))
    replay_days = int(comparison.get("duration", {}).get("replay_days", 0))
    score = _stress_score(
        comparison.get("status", "stable"),
        total_unmet_delta,
        emergency_hours,
        active_failure_day_delta,
        blocked_review_count,
        recovery_blocked_delta,
    )
    return {
        "comparison": comparison["id"],
        "scenario": scenario,
        "status": comparison.get("status", "stable"),
        "baseline_simulation": comparison.get("baseline_simulation", ""),
        "replay_simulation": comparison.get("replay_simulation", ""),
        "replay_days": replay_days,
        "stress_score": round(score, 3),
        "stress_score_per_day": round(score / max(1, replay_days), 3),
        "total_unmet_delta": round(total_unmet_delta, 3),
        "scenario_emergency_hours": round(emergency_hours, 3),
        "active_failure_day_delta": active_failure_day_delta,
        "blocked_review_domain_count": blocked_review_count,
        "blocked_recovery_delta": recovery_blocked_delta,
        "top_bottlenecks": comparison.get("bottlenecks", [])[:5],
        "provisional": True,
    }


def _stress_score(
    status: str,
    total_unmet_delta: float,
    emergency_hours: float,
    active_failure_day_delta: int,
    blocked_review_count: int,
    recovery_blocked_delta: int,
) -> float:
    status_weight = {
        "stable": 0.0,
        "stress_warn": 1000.0,
        "stress_failed": 10000.0,
    }.get(status, 0.0)
    return (
        status_weight
        + total_unmet_delta
        + (emergency_hours * 10)
        + (active_failure_day_delta * 100)
        + (blocked_review_count * 500)
        + (max(0, recovery_blocked_delta) * 750)
    )


def _matrix_status(entries: list[dict[str, Any]]) -> str:
    worst = max(STATUS_RANK.get(entry["status"], 0) for entry in entries)
    for status, rank in STATUS_RANK.items():
        if rank == worst:
            return status
    return "stable"


def _summary(status: str, rankings: list[dict[str, Any]]) -> list[str]:
    top = rankings[0]
    top_per_day = max(rankings, key=lambda item: float(item["stress_score_per_day"]))
    failed = [entry["scenario"] for entry in rankings if entry["status"] == "stress_failed"]
    warned = [entry["scenario"] for entry in rankings if entry["status"] == "stress_warn"]
    return [
        f"Replay matrix status is {status}.",
        f"Top stressor is {top['scenario']} with score {top['stress_score']}.",
        f"Highest per-day stressor is {top_per_day['scenario']} with score/day {top_per_day['stress_score_per_day']}.",
        f"Stress-failed replays: {', '.join(failed) if failed else 'none'}.",
        f"Stress-warning replays: {', '.join(warned) if warned else 'none'}.",
        f"Highest unmet-demand delta: {top['total_unmet_delta']}.",
        f"Highest active failure-day delta in top stressor: {top['active_failure_day_delta']}.",
    ]
