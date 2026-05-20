from __future__ import annotations

from statistics import pstdev
from typing import Any


def evaluate_roles(compiled_plan: dict[str, Any], role_plan: dict[str, Any]) -> dict[str, Any]:
    role_hours = _role_hours(compiled_plan)
    participants = role_plan["participants"]
    role_requirements = {item["role"]: item for item in role_plan["role_requirements"]}
    assignment_state = {
        participant["id"]: {
            "participant": participant,
            "assigned_hours": 0.0,
            "roles": [],
            "backup_roles": [],
        }
        for participant in participants
    }
    schedule, unfilled_roles, single_points = _assign_roles(role_hours, participants, role_requirements, role_plan, assignment_state)
    overloaded = _overloaded_residents(role_plan, assignment_state)
    backup_coverage = _backup_coverage(role_hours, schedule, role_plan)
    care_work = _care_work_accounting(role_plan, assignment_state)
    fairness = _fairness(role_plan, assignment_state)
    burnout_warnings = _burnout_warnings(unfilled_roles, overloaded, single_points, backup_coverage, care_work, fairness)
    recommendations = _recommendations(unfilled_roles, overloaded, single_points, backup_coverage, care_work, fairness)
    status = _status(unfilled_roles, overloaded, single_points, backup_coverage)

    return {
        "kind": "RoleReport",
        "id": f"{compiled_plan['id']}_{role_plan['id']}_roles",
        "compiled_plan": compiled_plan["id"],
        "role_plan": role_plan["id"],
        "generated_by": "ciac.roles.v0",
        "weeks": role_plan["weeks"],
        "provisional": True,
        "status": status,
        "assigned_role_schedule": schedule,
        "unfilled_roles": unfilled_roles,
        "overloaded_residents": overloaded,
        "single_point_of_failure_roles": single_points,
        "backup_coverage": backup_coverage,
        "care_work_accounting": care_work,
        "fairness": fairness,
        "burnout_warnings": burnout_warnings,
        "redesign_recommendations": recommendations,
        "unknowns": [
            "Role assignments are deterministic planning aids, not consent, labor contracts, or governance decisions.",
            "The model does not yet simulate illness, conflict, learning curves, task quality, emotional labor, or resident preference.",
            "Care work is counted as load pressure but not scheduled at task-level detail.",
            role_plan["notes"],
        ],
    }


def _role_hours(compiled_plan: dict[str, Any]) -> dict[str, float]:
    hours: dict[str, float] = {}
    for role, value in compiled_plan.get("role_burden", {}).get("weekly_hours_by_role", {}).items():
        hours[role] = float(value)
    return dict(sorted(hours.items()))


def _assign_roles(
    role_hours: dict[str, float],
    participants: list[dict[str, Any]],
    role_requirements: dict[str, dict[str, Any]],
    role_plan: dict[str, Any],
    assignment_state: dict[str, dict[str, Any]],
) -> tuple[list[dict[str, Any]], list[str], list[str]]:
    schedule: list[dict[str, Any]] = []
    unfilled_roles: list[str] = []
    single_points: list[str] = []

    for role, hours in role_hours.items():
        eligible = _eligible_participants(role, participants, role_requirements.get(role))
        if not eligible:
            unfilled_roles.append(role)
            continue
        primary = _least_loaded(eligible, assignment_state, role_plan)
        assignment_state[primary["id"]]["assigned_hours"] += hours
        assignment_state[primary["id"]]["roles"].append(role)

        backup = None
        backup_candidates = [candidate for candidate in eligible if candidate["id"] != primary["id"]]
        if backup_candidates:
            backup = _least_loaded(backup_candidates, assignment_state, role_plan)
            assignment_state[backup["id"]]["backup_roles"].append(role)
        elif role_plan["backup_required"]:
            single_points.append(role)

        min_people = role_requirements.get(role, {}).get("min_people", 1)
        if len(eligible) < min_people and role not in single_points:
            single_points.append(role)

        schedule.append(
            {
                "role": role,
                "weekly_hours": round(hours, 3),
                "primary": primary["id"],
                "backup": backup["id"] if backup else None,
                "eligible_count": len(eligible),
                "rotation_cadence_weeks": role_plan["rotation_cadence_weeks"],
                "safety_critical": bool(role_requirements.get(role, {}).get("safety_critical", False)),
            }
        )

    return schedule, sorted(unfilled_roles), sorted(set(single_points))


def _eligible_participants(
    role: str,
    participants: list[dict[str, Any]],
    requirement: dict[str, Any] | None,
) -> list[dict[str, Any]]:
    required_skills = set(requirement.get("required_skills", [])) if requirement else set()
    eligible: list[dict[str, Any]] = []
    for participant in participants:
        if role not in participant["eligible_roles"]:
            continue
        if required_skills and not required_skills.issubset(set(participant["skills"])):
            continue
        eligible.append(participant)
    return eligible


def _least_loaded(
    candidates: list[dict[str, Any]],
    assignment_state: dict[str, dict[str, Any]],
    role_plan: dict[str, Any],
) -> dict[str, Any]:
    return sorted(
        candidates,
        key=lambda candidate: (
            _load_ratio(candidate, assignment_state[candidate["id"]]["assigned_hours"], role_plan),
            candidate["reduced_load"],
            candidate["id"],
        ),
    )[0]


def _load_ratio(participant: dict[str, Any], assigned_hours: float, role_plan: dict[str, Any]) -> float:
    capacity = _effective_capacity(participant, role_plan)
    if capacity <= 0:
        return float("inf")
    return assigned_hours / capacity


def _effective_capacity(participant: dict[str, Any], role_plan: dict[str, Any]) -> float:
    care_allowance = min(float(participant["care_hours_per_week"]), float(role_plan["care_work_allowance_hours_per_week"]))
    capacity = float(participant["availability_hours_per_week"]) - care_allowance
    if participant["reduced_load"]:
        capacity *= 0.75
    return max(0.0, capacity)


def _overloaded_residents(role_plan: dict[str, Any], assignment_state: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    overloaded: list[dict[str, Any]] = []
    max_hours = float(role_plan["max_compulsory_hours_per_person_per_week"])
    for participant_id, state in assignment_state.items():
        participant = state["participant"]
        assigned = float(state["assigned_hours"])
        capacity = min(max_hours, _effective_capacity(participant, role_plan))
        if assigned > capacity:
            overloaded.append(
                {
                    "participant_id": participant_id,
                    "assigned_hours": round(assigned, 3),
                    "effective_capacity_hours": round(capacity, 3),
                    "overage_hours": round(assigned - capacity, 3),
                    "reduced_load": participant["reduced_load"],
                    "protected_notes": participant["protected_notes"],
                }
            )
    return overloaded


def _backup_coverage(role_hours: dict[str, float], schedule: list[dict[str, Any]], role_plan: dict[str, Any]) -> dict[str, Any]:
    roles_with_backup = [item["role"] for item in schedule if item["backup"]]
    total_roles = len(role_hours)
    coverage_percent = (len(roles_with_backup) / total_roles * 100.0) if total_roles else 100.0
    missing = sorted(role for role in role_hours if role not in roles_with_backup)
    status = "pass"
    if role_plan["backup_required"] and missing:
        status = "fail"
    elif coverage_percent < 100:
        status = "warn"
    return {
        "roles_with_backup": sorted(roles_with_backup),
        "roles_missing_backup": missing,
        "coverage_percent": round(coverage_percent, 3),
        "status": status,
    }


def _care_work_accounting(role_plan: dict[str, Any], assignment_state: dict[str, dict[str, Any]]) -> dict[str, Any]:
    total_care = sum(float(participant["care_hours_per_week"]) for participant in role_plan["participants"])
    participants_with_high_care = [
        participant["id"]
        for participant in role_plan["participants"]
        if float(participant["care_hours_per_week"]) > float(role_plan["care_work_allowance_hours_per_week"])
    ]
    assigned_plus_care = {
        participant_id: round(state["assigned_hours"] + float(state["participant"]["care_hours_per_week"]), 3)
        for participant_id, state in sorted(assignment_state.items())
    }
    status = "warn" if participants_with_high_care else "pass"
    return {
        "total_declared_care_hours_per_week": round(total_care, 3),
        "care_work_allowance_hours_per_week": role_plan["care_work_allowance_hours_per_week"],
        "participants_above_allowance": participants_with_high_care,
        "assigned_plus_care_hours_by_participant": assigned_plus_care,
        "status": status,
    }


def _fairness(role_plan: dict[str, Any], assignment_state: dict[str, dict[str, Any]]) -> dict[str, Any]:
    ratios = []
    assigned_by_participant = {}
    for participant_id, state in sorted(assignment_state.items()):
        assigned = float(state["assigned_hours"])
        capacity = _effective_capacity(state["participant"], role_plan)
        ratio = _safe_div(assigned, capacity)
        ratios.append(ratio)
        assigned_by_participant[participant_id] = round(assigned, 3)
    spread = max(ratios) - min(ratios) if ratios else 0.0
    deviation = pstdev(ratios) if len(ratios) > 1 else 0.0
    score = max(0.0, 100.0 - (spread * 40.0) - (deviation * 20.0))
    status = "pass"
    if score < 60:
        status = "fail"
    elif score < 75:
        status = "warn"
    return {
        "score": round(score, 3),
        "load_ratio_spread": round(spread, 3),
        "load_ratio_stddev": round(deviation, 3),
        "assigned_hours_by_participant": assigned_by_participant,
        "status": status,
    }


def _burnout_warnings(
    unfilled_roles: list[str],
    overloaded: list[dict[str, Any]],
    single_points: list[str],
    backup_coverage: dict[str, Any],
    care_work: dict[str, Any],
    fairness: dict[str, Any],
) -> list[str]:
    warnings: list[str] = []
    if unfilled_roles:
        warnings.append("One or more maintenance roles cannot be assigned.")
    if overloaded:
        warnings.append("One or more residents exceed effective compulsory work capacity.")
    if single_points:
        warnings.append("One or more roles depend on too few eligible people.")
    if backup_coverage["status"] != "pass":
        warnings.append("Backup coverage is incomplete.")
    if care_work["status"] != "pass":
        warnings.append("Some declared care work exceeds the current allowance and may hide overload.")
    if fairness["status"] != "pass":
        warnings.append("Role load distribution is uneven enough to create fairness or burnout risk.")
    return warnings


def _recommendations(
    unfilled_roles: list[str],
    overloaded: list[dict[str, Any]],
    single_points: list[str],
    backup_coverage: dict[str, Any],
    care_work: dict[str, Any],
    fairness: dict[str, Any],
) -> list[str]:
    recommendations: list[str] = []
    if unfilled_roles:
        recommendations.append("Train or recruit participants for unfilled roles before promotion.")
    if overloaded:
        recommendations.append("Reduce recurring maintenance burden, increase participation, or lower role assignments for overloaded residents.")
    if single_points:
        recommendations.append("Create backup training paths for single-point-of-failure roles.")
    if backup_coverage["status"] != "pass":
        recommendations.append("Require a named backup for each survival-critical role.")
    if care_work["status"] != "pass":
        recommendations.append("Account for care work explicitly when assigning commons labor.")
    if fairness["status"] != "pass":
        recommendations.append("Rebalance rotation assignments to reduce load-ratio spread.")
    if not recommendations:
        recommendations.append("Keep role plan as a regression case while adding preferences, absences, illness, and learning curves.")
    return recommendations


def _status(
    unfilled_roles: list[str],
    overloaded: list[dict[str, Any]],
    single_points: list[str],
    backup_coverage: dict[str, Any],
) -> str:
    if unfilled_roles or overloaded or backup_coverage["status"] == "fail":
        return "fail"
    if single_points:
        return "warn"
    return "pass"


def _safe_div(numerator: float, denominator: float) -> float:
    if denominator <= 0:
        return 0.0
    return numerator / denominator

