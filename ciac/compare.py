from __future__ import annotations

from typing import Any


DECISION_RANK = {
    "do_not_promote": 0,
    "revise_before_pilot": 1,
    "candidate_for_review": 2,
}


def compare_audits(before: dict[str, Any], after: dict[str, Any]) -> dict[str, Any]:
    before_blockers = set(before.get("survival_critical_blockers", []))
    after_blockers = set(after.get("survival_critical_blockers", []))
    before_warnings = set(before.get("noncritical_warnings", []))
    after_warnings = set(after.get("noncritical_warnings", []))
    resolved = sorted(before_blockers - after_blockers)
    new_blockers = sorted(after_blockers - before_blockers)
    remaining = sorted(before_blockers & after_blockers)
    new_warnings = sorted(after_warnings - before_warnings)
    blocker_delta = len(before_blockers) - len(after_blockers)
    status_changes = _status_changes(before, after)
    decision_delta = _promotion_decision_delta(before, after)
    metric_deltas = {
        "blocker_count": blocker_delta,
        "warning_count": len(before_warnings) - len(after_warnings),
        "resolved_blocker_count": len(resolved),
        "new_blocker_count": len(new_blockers),
    }
    acceptance = _acceptance_criteria(after)
    status = _comparison_status(blocker_delta, decision_delta, new_blockers)

    return {
        "kind": "ComparisonReport",
        "id": f"{before['id']}_to_{after['id']}_comparison",
        "before_audit": before["id"],
        "after_audit": after["id"],
        "generated_by": "ciac.compare.v0",
        "provisional": True,
        "status": status,
        "blocker_count_before": len(before_blockers),
        "blocker_count_after": len(after_blockers),
        "blocker_delta": blocker_delta,
        "promotion_decision_delta": decision_delta,
        "status_changes_by_subsystem": status_changes,
        "resolved_blockers": resolved,
        "remaining_blockers": remaining,
        "new_blockers": new_blockers,
        "new_warnings": new_warnings,
        "metric_deltas": metric_deltas,
        "acceptance_criteria": acceptance,
        "summary": _summary(status, blocker_delta, resolved, remaining, new_blockers, acceptance),
        "unknowns": [
            "Comparison only sees audit-report evidence; it does not independently verify source-plan changes.",
            "Resolved blockers can reappear if later reports or scenarios are regenerated with stricter assumptions.",
            "Improvement is not promotion; real-world review remains out of scope.",
        ],
    }


def _status_changes(before: dict[str, Any], after: dict[str, Any]) -> list[dict[str, Any]]:
    before_statuses = before.get("subsystem_statuses", {})
    after_statuses = after.get("subsystem_statuses", {})
    changes: list[dict[str, Any]] = []
    for subsystem in sorted(set(before_statuses) | set(after_statuses)):
        before_status = before_statuses.get(subsystem, {}).get("status", "missing")
        after_status = after_statuses.get(subsystem, {}).get("status", "missing")
        if before_status != after_status:
            changes.append(
                {
                    "subsystem": subsystem,
                    "before": before_status,
                    "after": after_status,
                }
            )
    return changes


def _promotion_decision_delta(before: dict[str, Any], after: dict[str, Any]) -> dict[str, Any]:
    before_decision = before.get("promotion_decision", "do_not_promote")
    after_decision = after.get("promotion_decision", "do_not_promote")
    before_rank = DECISION_RANK.get(before_decision, 0)
    after_rank = DECISION_RANK.get(after_decision, 0)
    if after_rank > before_rank:
        direction = "improved"
    elif after_rank < before_rank:
        direction = "regressed"
    else:
        direction = "unchanged"
    return {
        "before": before_decision,
        "after": after_decision,
        "direction": direction,
    }


def _acceptance_criteria(after: dict[str, Any]) -> list[dict[str, Any]]:
    blockers = " ".join(after.get("survival_critical_blockers", [])).lower()
    subsystem_statuses = after.get("subsystem_statuses", {})
    water_status = subsystem_statuses.get("water", {}).get("status")
    energy_status = subsystem_statuses.get("energy", {}).get("status")
    roles_status = subsystem_statuses.get("roles", {}).get("status")
    drought_status = subsystem_statuses.get("scenario:drought_reserve_v2", subsystem_statuses.get("scenario:drought", {})).get("status")
    energy_outage_status = subsystem_statuses.get(
        "scenario:energy_outage_reserve_v2",
        subsystem_statuses.get("scenario:energy_outage", {}),
    ).get("status")
    contamination_status = subsystem_statuses.get(
        "scenario:water_contamination_response_v2",
        subsystem_statuses.get("scenario:water_contamination", {}),
    ).get("status")
    return [
        {
            "candidate": "water_storage_and_drought_reserve",
            "criterion": "ciac water returns non-fail status for the updated water plan.",
            "passed": water_status != "fail",
            "evidence": f"water status is {water_status}",
        },
        {
            "candidate": "water_storage_and_drought_reserve",
            "criterion": "drought scenario no longer fails water_gate.",
            "passed": "drought_reserve_v2 failed water_gate" not in blockers and "drought failed water_gate" not in blockers,
            "evidence": "after audit blocker list checked for drought water_gate failure",
        },
        {
            "candidate": "water_storage_and_drought_reserve",
            "criterion": "scenario drought status is not fail.",
            "passed": drought_status != "fail",
            "evidence": f"drought scenario status is {drought_status}",
        },
        {
            "candidate": "energy_battery_and_backup",
            "criterion": "ciac energy returns non-fail status for the updated energy plan.",
            "passed": energy_status != "fail",
            "evidence": f"energy status is {energy_status}",
        },
        {
            "candidate": "energy_battery_and_backup",
            "criterion": "energy blockers are absent from the after audit.",
            "passed": "energy:" not in blockers,
            "evidence": "after audit blocker list checked for energy failures",
        },
        {
            "candidate": "energy_battery_and_backup",
            "criterion": "energy outage scenario is not fail when included.",
            "passed": energy_outage_status != "fail",
            "evidence": f"energy outage scenario status is {energy_outage_status}",
        },
        {
            "candidate": "roles_train_second_energy_steward",
            "criterion": "ciac roles returns non-fail status for the updated role plan.",
            "passed": roles_status != "fail",
            "evidence": f"roles status is {roles_status}",
        },
        {
            "candidate": "roles_train_second_energy_steward",
            "criterion": "role blockers are absent from the after audit.",
            "passed": "roles:" not in blockers,
            "evidence": "after audit blocker list checked for role failures",
        },
        {
            "candidate": "roles_rebalance_care_and_fairness",
            "criterion": "care and fairness redesign does not introduce new role blockers.",
            "passed": "roles:" not in blockers,
            "evidence": "after audit blocker list checked for role failures",
        },
        {
            "candidate": "water_verified_backup_source",
            "criterion": "water contamination scenario no longer fails water_gate.",
            "passed": "water_contamination_response_v2 failed water_gate" not in blockers
            and "water_contamination failed water_gate" not in blockers,
            "evidence": "after audit blocker list checked for contamination water_gate failure",
        },
        {
            "candidate": "water_verified_backup_source",
            "criterion": "water contamination scenario status is not fail.",
            "passed": contamination_status != "fail",
            "evidence": f"water contamination scenario status is {contamination_status}",
        },
    ]


def _comparison_status(
    blocker_delta: int,
    decision_delta: dict[str, Any],
    new_blockers: list[str],
) -> str:
    if new_blockers or blocker_delta < 0 or decision_delta["direction"] == "regressed":
        return "regressed"
    if blocker_delta > 0 or decision_delta["direction"] == "improved":
        return "improved"
    return "unchanged"


def _summary(
    status: str,
    blocker_delta: int,
    resolved: list[str],
    remaining: list[str],
    new_blockers: list[str],
    acceptance: list[dict[str, Any]],
) -> list[str]:
    passed_acceptance = sum(1 for item in acceptance if item["passed"])
    return [
        f"Comparison status is {status}.",
        f"Survival-critical blocker count changed by {blocker_delta}.",
        f"Resolved blockers: {len(resolved)}.",
        f"Remaining blockers: {len(remaining)}.",
        f"New blockers: {len(new_blockers)}.",
        f"Acceptance criteria passed: {passed_acceptance}/{len(acceptance)}.",
    ]
