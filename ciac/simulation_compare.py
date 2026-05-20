from __future__ import annotations

from typing import Any


def compare_simulations(baseline: dict[str, Any], replay: dict[str, Any]) -> dict[str, Any]:
    resource_deltas = _resource_deltas(baseline, replay)
    storage_deltas = _storage_deltas(baseline, replay)
    labor_delta = _labor_delta(baseline, replay)
    unmet_need_deltas = _unmet_need_deltas(baseline, replay)
    failure_day_delta = _failure_day_delta(baseline, replay)
    recovery_delta = _recovery_delta(baseline, replay)
    review_delta = _review_delta(baseline, replay)
    bottlenecks = _bottlenecks(
        replay,
        resource_deltas,
        unmet_need_deltas,
        labor_delta,
        failure_day_delta,
        recovery_delta,
        review_delta,
    )
    status = _status(baseline, replay, unmet_need_deltas, labor_delta, recovery_delta, review_delta)
    scenario_context = replay.get("scenario_context", {})

    return {
        "kind": "SimulationComparisonReport",
        "id": f"{baseline['id']}_to_{replay['id']}_simulation_comparison",
        "baseline_simulation": baseline["id"],
        "replay_simulation": replay["id"],
        "generated_by": "ciac.simulation_compare.v0",
        "provisional": True,
        "status": status,
        "scenario_context": scenario_context,
        "status_delta": {
            "baseline": baseline["status"],
            "replay": replay["status"],
            "changed": baseline["status"] != replay["status"],
        },
        "duration": {
            "baseline_days": int(baseline["days"]),
            "replay_days": int(replay["days"]),
            "same_duration": int(baseline["days"]) == int(replay["days"]),
        },
        "resource_deltas": resource_deltas,
        "storage_deltas": storage_deltas,
        "labor_delta": labor_delta,
        "unmet_need_deltas": unmet_need_deltas,
        "failure_day_delta": failure_day_delta,
        "recovery_delta": recovery_delta,
        "review_delta": review_delta,
        "bottlenecks": bottlenecks,
        "summary": _summary(status, scenario_context, resource_deltas, unmet_need_deltas, labor_delta, recovery_delta, review_delta),
        "unknowns": [
            "Simulation comparisons compare generated JSON artifacts only; they do not verify source assumptions.",
            "Scenario replay deltas are deterministic provisional stress signals, not forecasts.",
            "A stable comparison does not imply real-world safety, legal compliance, public-health clearance, or adequate resident consent.",
        ],
    }


def _resource_deltas(baseline: dict[str, Any], replay: dict[str, Any]) -> list[dict[str, Any]]:
    baseline_balance = baseline.get("resource_balance", {})
    replay_balance = replay.get("resource_balance", {})
    deltas: list[dict[str, Any]] = []
    for resource in sorted(set(baseline_balance) | set(replay_balance)):
        before = baseline_balance.get(resource, {})
        after = replay_balance.get(resource, {})
        deltas.append(
            {
                "resource": resource,
                "baseline_status": before.get("status", "missing"),
                "replay_status": after.get("status", "missing"),
                "net_per_day_delta": _round(float(after.get("net_per_day", 0.0)) - float(before.get("net_per_day", 0.0))),
                "ending_balance_delta": _round(float(after.get("ending_balance", 0.0)) - float(before.get("ending_balance", 0.0))),
                "minimum_balance_delta": _round(float(after.get("minimum_balance", 0.0)) - float(before.get("minimum_balance", 0.0))),
            }
        )
    return deltas


def _storage_deltas(baseline: dict[str, Any], replay: dict[str, Any]) -> list[dict[str, Any]]:
    baseline_storage = baseline.get("storage", {}).get("resources", {})
    replay_storage = replay.get("storage", {}).get("resources", {})
    deltas: list[dict[str, Any]] = []
    for resource in sorted(set(baseline_storage) | set(replay_storage)):
        before = baseline_storage.get(resource, {})
        after = replay_storage.get(resource, {})
        deltas.append(
            {
                "resource": resource,
                "baseline_status": before.get("status", "missing"),
                "replay_status": after.get("status", "missing"),
                "ending_total_delta": _round(float(after.get("ending_total", 0.0)) - float(before.get("ending_total", 0.0))),
                "minimum_total_delta": _round(float(after.get("minimum_total", 0.0)) - float(before.get("minimum_total", 0.0))),
                "total_released_delta": _round(float(after.get("total_released", 0.0)) - float(before.get("total_released", 0.0))),
                "total_quality_loss_delta": _round(float(after.get("total_quality_loss", 0.0)) - float(before.get("total_quality_loss", 0.0))),
            }
        )
    return deltas


def _labor_delta(baseline: dict[str, Any], replay: dict[str, Any]) -> dict[str, Any]:
    before = baseline.get("labor", {})
    after = replay.get("labor", {})
    return {
        "baseline_status": before.get("status", "missing"),
        "replay_status": after.get("status", "missing"),
        "estimated_hours_per_resident_per_week_delta": _round(
            float(after.get("estimated_hours_per_resident_per_week", 0.0))
            - float(before.get("estimated_hours_per_resident_per_week", 0.0))
        ),
        "labor_utilization_delta": _round(float(after.get("labor_utilization", 0.0)) - float(before.get("labor_utilization", 0.0))),
        "scenario_emergency_hours": _round(float(after.get("scenario_emergency_hours", 0.0))),
        "runtime_failure_response_hours_delta": _round(
            float(after.get("runtime_failure_response_hours", 0.0))
            - float(before.get("runtime_failure_response_hours", 0.0))
        ),
        "storage_recovery_hours_delta": _round(
            float(after.get("storage_recovery_hours", 0.0))
            - float(before.get("storage_recovery_hours", 0.0))
        ),
    }


def _unmet_need_deltas(baseline: dict[str, Any], replay: dict[str, Any]) -> list[dict[str, Any]]:
    baseline_ledger = baseline.get("resource_ledger", {})
    replay_ledger = replay.get("resource_ledger", {})
    deltas: list[dict[str, Any]] = []
    for resource in sorted(set(baseline_ledger) | set(replay_ledger)):
        before = baseline_ledger.get(resource, {})
        after = replay_ledger.get(resource, {})
        before_unmet = float(before.get("total_unmet_demand", 0.0))
        after_unmet = float(after.get("total_unmet_demand", 0.0))
        deltas.append(
            {
                "resource": resource,
                "baseline_total_unmet": _round(before_unmet),
                "replay_total_unmet": _round(after_unmet),
                "delta": _round(after_unmet - before_unmet),
                "first_unmet_day": _first_unmet_day(replay, resource),
            }
        )
    return deltas


def _failure_day_delta(baseline: dict[str, Any], replay: dict[str, Any]) -> dict[str, Any]:
    before_days = _active_failure_days(baseline)
    after_days = _active_failure_days(replay)
    return {
        "baseline_active_failure_days": before_days,
        "replay_active_failure_days": after_days,
        "delta": after_days - before_days,
        "replay_failure_modes": sorted({failure["mode"] for failure in replay.get("runtime_failures", [])}),
    }


def _recovery_delta(baseline: dict[str, Any], replay: dict[str, Any]) -> dict[str, Any]:
    before = baseline.get("storage", {}).get("recovery", {})
    after = replay.get("storage", {}).get("recovery", {})
    return {
        "baseline_status": before.get("status", "missing"),
        "replay_status": after.get("status", "missing"),
        "active_task_count_delta": int(after.get("active_task_count", 0)) - int(before.get("active_task_count", 0)),
        "blocked_review_count_delta": int(after.get("blocked_review_count", 0)) - int(before.get("blocked_review_count", 0)),
        "resolved_count_delta": int(after.get("resolved_count", 0)) - int(before.get("resolved_count", 0)),
        "total_remaining_hours_delta": _round(float(after.get("total_remaining_hours", 0.0)) - float(before.get("total_remaining_hours", 0.0))),
    }


def _review_delta(baseline: dict[str, Any], replay: dict[str, Any]) -> dict[str, Any]:
    before = baseline.get("review_context", {})
    after = replay.get("review_context", {})
    before_blocked = set(before.get("blocked_domains", []))
    after_blocked = set(after.get("blocked_domains", []))
    return {
        "baseline_status": before.get("status", "missing"),
        "replay_status": after.get("status", "missing"),
        "new_blocked_domains": sorted(after_blocked - before_blocked),
        "remaining_blocked_domains": sorted(before_blocked & after_blocked),
        "scenario_review_event_count": len(after.get("scenario_events", [])),
    }


def _bottlenecks(
    replay: dict[str, Any],
    resource_deltas: list[dict[str, Any]],
    unmet_need_deltas: list[dict[str, Any]],
    labor_delta: dict[str, Any],
    failure_day_delta: dict[str, Any],
    recovery_delta: dict[str, Any],
    review_delta: dict[str, Any],
) -> list[str]:
    bottlenecks = list(replay.get("bottlenecks", []))
    for item in unmet_need_deltas:
        if float(item["delta"]) > 0:
            bottlenecks.append(f"{item['resource']} unmet demand increases by {item['delta']}")
    for item in resource_deltas:
        if item["replay_status"] == "fail" and item["baseline_status"] != "fail":
            bottlenecks.append(f"{item['resource']} regresses to fail under replay")
    if float(labor_delta["scenario_emergency_hours"]) > 0:
        bottlenecks.append(f"scenario emergency work adds {labor_delta['scenario_emergency_hours']} labor hours")
    if failure_day_delta["delta"] > 0:
        bottlenecks.append(f"active failure days increase by {failure_day_delta['delta']}")
    if recovery_delta["blocked_review_count_delta"] > 0:
        bottlenecks.append("blocked recovery review count increases")
    for domain in review_delta["new_blocked_domains"]:
        bottlenecks.append(f"new blocked review domain: {domain}")
    return sorted(set(bottlenecks))


def _status(
    baseline: dict[str, Any],
    replay: dict[str, Any],
    unmet_need_deltas: list[dict[str, Any]],
    labor_delta: dict[str, Any],
    recovery_delta: dict[str, Any],
    review_delta: dict[str, Any],
) -> str:
    if (replay.get("status") == "fail" and baseline.get("status") != "fail") or any(float(item["delta"]) > 0 for item in unmet_need_deltas):
        return "stress_failed"
    if recovery_delta["blocked_review_count_delta"] > 0 or review_delta["new_blocked_domains"]:
        return "stress_warn"
    if replay.get("status") == "warn" and baseline.get("status") != "warn":
        return "stress_warn"
    if float(labor_delta["scenario_emergency_hours"]) > 0:
        return "stress_warn"
    return "stable"


def _summary(
    status: str,
    scenario_context: dict[str, Any],
    resource_deltas: list[dict[str, Any]],
    unmet_need_deltas: list[dict[str, Any]],
    labor_delta: dict[str, Any],
    recovery_delta: dict[str, Any],
    review_delta: dict[str, Any],
) -> list[str]:
    largest_unmet = max(unmet_need_deltas, key=lambda item: float(item["delta"]), default={"resource": "none", "delta": 0})
    largest_depletion = min(resource_deltas, key=lambda item: float(item["minimum_balance_delta"]), default={"resource": "none", "minimum_balance_delta": 0})
    depletion_line = (
        f"Largest minimum-balance drop: {largest_depletion['resource']} ({largest_depletion['minimum_balance_delta']})."
        if float(largest_depletion["minimum_balance_delta"]) < 0
        else "No resource minimum-balance drop was detected; stress appears as unmet demand, failure state, or labor/review burden."
    )
    unmet_resources = [item["resource"] for item in unmet_need_deltas if float(item["delta"]) > 0]
    scenario_id = scenario_context.get("id") or "normal_replay"
    return [
        f"Comparison status is {status}.",
        f"Replay scenario is {scenario_id}.",
        f"Largest unmet-demand increase: {largest_unmet['resource']} ({largest_unmet['delta']}).",
        depletion_line,
        f"Unmet demand increased for {len(unmet_resources)} resource(s): {', '.join(unmet_resources) if unmet_resources else 'none'}.",
        f"Scenario emergency labor hours: {labor_delta['scenario_emergency_hours']}.",
        f"Blocked recovery review delta: {recovery_delta['blocked_review_count_delta']}.",
        f"New blocked review domains: {', '.join(review_delta['new_blocked_domains']) if review_delta['new_blocked_domains'] else 'none'}.",
    ]


def _first_unmet_day(simulation: dict[str, Any], resource: str) -> int | None:
    for state in simulation.get("daily_states", []):
        if float(state.get("resources", {}).get(resource, {}).get("unmet_demand", 0.0)) > 0:
            return int(state["day"])
    return None


def _active_failure_days(simulation: dict[str, Any]) -> int:
    return sum(1 for state in simulation.get("daily_states", []) if state.get("active_failures"))


def _round(value: float) -> float:
    return round(value, 3)
