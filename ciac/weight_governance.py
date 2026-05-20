from __future__ import annotations

from typing import Any


def evaluate_weight_governance(
    optimization_profile: dict[str, Any],
    objective_calibration_report: dict[str, Any],
    weight_governance_profile: dict[str, Any],
) -> dict[str, Any]:
    weight_checks = _weight_checks(optimization_profile, weight_governance_profile)
    gate_results = _approval_gate_results(weight_governance_profile, weight_checks)
    status = _status(weight_checks, gate_results)
    return {
        "kind": "WeightGovernanceReport",
        "id": f"{optimization_profile['id']}_{weight_governance_profile['id']}_weight_governance",
        "optimization_profile": optimization_profile["id"],
        "objective_calibration_report": objective_calibration_report["id"],
        "weight_governance_profile": weight_governance_profile["id"],
        "generated_by": "ciac.weight_governance.v0",
        "provisional": True,
        "status": status,
        "promotion_allowed": status == "ratified" and objective_calibration_report.get("status") == "calibrated",
        "weight_checks": weight_checks,
        "approval_gate_results": gate_results,
        "governance_summary": _governance_summary(weight_governance_profile, objective_calibration_report),
        "metric_updates": _metric_updates(status),
        "next_actions": _next_actions(status),
        "unknowns": _unknowns(objective_calibration_report, weight_governance_profile),
    }


def _weight_checks(
    optimization_profile: dict[str, Any],
    weight_governance_profile: dict[str, Any],
) -> list[dict[str, Any]]:
    governed = {
        item["objective"]: item
        for item in weight_governance_profile.get("objective_weights", [])
    }
    checks = []
    for objective in optimization_profile.get("objectives", []):
        governed_weight = governed.get(objective["id"])
        if not governed_weight:
            checks.append(
                {
                    "objective": objective["id"],
                    "profile_weight": objective["weight"],
                    "governed_weight": None,
                    "status": "missing",
                    "matches_profile": False,
                    "rationale": "No governance weight exists for this objective.",
                    "provisional": True,
                }
            )
            continue
        checks.append(
            {
                "objective": objective["id"],
                "profile_weight": objective["weight"],
                "governed_weight": governed_weight["weight"],
                "status": governed_weight["status"],
                "matches_profile": float(objective["weight"]) == float(governed_weight["weight"]),
                "rationale": governed_weight["rationale"],
                "provisional": True,
            }
        )
    return checks


def _approval_gate_results(weight_governance_profile: dict[str, Any], weight_checks: list[dict[str, Any]]) -> list[dict[str, Any]]:
    authority = weight_governance_profile.get("authority", {})
    results = []
    for gate in weight_governance_profile.get("approval_gates", []):
        gate_id = gate["id"]
        if gate_id == "resident_weight_ratification":
            actual = authority.get("resident_consent_status", "not_started")
            passed = actual == gate["required_status"]
        elif gate_id == "professional_review_acceptance":
            actual = authority.get("professional_review_status", "not_started")
            passed = actual == gate["required_status"]
        elif gate_id == "no_rejected_weights":
            actual = "no_rejected" if all(check["status"] != "rejected" for check in weight_checks) else "rejected"
            passed = actual == gate["required_status"]
        else:
            actual = "unknown"
            passed = False
        results.append(
            {
                "gate": gate_id,
                "required_status": gate["required_status"],
                "actual_status": actual,
                "status": "pass" if passed else "fail",
                "description": gate["description"],
                "provisional": True,
            }
        )
    return results


def _status(weight_checks: list[dict[str, Any]], gate_results: list[dict[str, Any]]) -> str:
    if all(check["status"] == "ratified" and check["matches_profile"] for check in weight_checks) and all(
        gate["status"] == "pass" for gate in gate_results
    ):
        return "ratified"
    if any(check["status"] == "ratified" for check in weight_checks):
        return "partially_ratified"
    return "not_ratified"


def _governance_summary(
    weight_governance_profile: dict[str, Any],
    objective_calibration_report: dict[str, Any],
) -> dict[str, Any]:
    authority = weight_governance_profile.get("authority", {})
    return {
        "weight_authority": authority.get("weight_authority", ""),
        "resident_consent_status": authority.get("resident_consent_status", ""),
        "professional_review_status": authority.get("professional_review_status", ""),
        "objective_calibration_status": objective_calibration_report.get("status", ""),
        "last_reviewed": authority.get("last_reviewed", ""),
        "next_review_due": authority.get("next_review_due", ""),
        "provisional": True,
    }


def _metric_updates(status: str) -> dict[str, Any]:
    return {
        "inspectable_simulation_proof_of_concept": "100%",
        "mature_commune_virtualization_data_contract": "100%",
        "faithful_pattern_optimization_engine": "100%",
        "rationale": (
            "Sprint 49 completes the optimizer control loop by representing weight governance, "
            "blocking unratified weights, and preserving review/consent status."
        )
        if status != "ratified"
        else "Sprint 49 verifies governance-ratified weights and calibrated objectives.",
    }


def _next_actions(status: str) -> list[str]:
    if status == "ratified":
        return [
            "Use the ratified weights for optimizer runs within the stated scope.",
            "Re-run objective calibration whenever weights, formulas, or community priorities change.",
        ]
    return [
        "Do not present optimizer rankings as resident-approved recommendations.",
        "Run a real governance process to ratify or revise objective weights.",
        "Seek relevant professional review before replacing provisional proxy formulas with accepted evidence.",
    ]


def _unknowns(
    objective_calibration_report: dict[str, Any],
    weight_governance_profile: dict[str, Any],
) -> list[str]:
    unknowns = set(objective_calibration_report.get("unknowns", []))
    unknowns.update(weight_governance_profile.get("unknowns", []))
    unknowns.add("Weight governance support is complete as a data contract; the current demo weights remain unratified.")
    return sorted(unknowns)
