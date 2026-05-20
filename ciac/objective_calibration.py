from __future__ import annotations

from typing import Any


def evaluate_objective_calibration(
    search_optimizer_report: dict[str, Any],
    calibration_profile: dict[str, Any],
) -> dict[str, Any]:
    calibrations = {
        calibration["metric"]: calibration
        for calibration in calibration_profile.get("metric_calibrations", [])
    }
    selected = search_optimizer_report.get("selected_candidate", "")
    top_candidates = search_optimizer_report.get("top_candidates", [])
    selected_candidate = next((candidate for candidate in top_candidates if candidate.get("id") == selected), top_candidates[0] if top_candidates else {})
    calibrated = _calibrated_objectives(selected_candidate, calibrations)
    missing = sorted(
        {
            score.get("metric", "")
            for score in selected_candidate.get("objective_scores", [])
            if score.get("metric") not in calibrations
        }
    )
    uncalibrated_count = sum(1 for item in calibrated if item["calibration_status"] == "missing")
    status = _status(missing, calibration_profile)
    return {
        "kind": "ObjectiveCalibrationReport",
        "id": f"{search_optimizer_report['id']}_{calibration_profile['id']}_objective_calibration",
        "search_optimizer_report": search_optimizer_report["id"],
        "calibration_profile": calibration_profile["id"],
        "generated_by": "ciac.objective_calibration.v0",
        "provisional": True,
        "status": status,
        "selected_candidate": selected,
        "calibrated_objectives": calibrated,
        "missing_metrics": missing,
        "uncalibrated_score_count": uncalibrated_count,
        "governance_status": calibration_profile.get("governance", {}),
        "metric_updates": _metric_updates(status),
        "next_actions": _next_actions(status),
        "unknowns": _unknowns(search_optimizer_report, calibration_profile),
    }


def _calibrated_objectives(selected_candidate: dict[str, Any], calibrations: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    results = []
    for score in selected_candidate.get("objective_scores", []):
        metric = score.get("metric", "")
        calibration = calibrations.get(metric)
        if not calibration:
            results.append(
                {
                    "objective": score.get("id", ""),
                    "metric": metric,
                    "score": score.get("score", 0),
                    "weight": score.get("weight", 0),
                    "calibration_status": "missing",
                    "formula_id": "",
                    "evidence_status": "missing",
                    "review_required": True,
                    "interpretation": "No calibration rule exists for this metric.",
                    "risk_of_false_precision": "Uncalibrated objective score should not drive selection.",
                    "provisional": True,
                }
            )
            continue
        results.append(
            {
                "objective": score.get("id", ""),
                "metric": metric,
                "score": score.get("score", 0),
                "weighted_score": score.get("weighted_score", 0),
                "weight": score.get("weight", 0),
                "calibration_status": _calibration_status(calibration),
                "formula_id": calibration["formula_id"],
                "direction": calibration["direction"],
                "inputs": calibration["inputs"],
                "evidence_status": calibration["evidence_status"],
                "review_required": calibration["review_required"],
                "interpretation": calibration["score_interpretation"],
                "risk_of_false_precision": calibration["risk_of_false_precision"],
                "provisional": True,
            }
        )
    return results


def _calibration_status(calibration: dict[str, Any]) -> str:
    if calibration.get("evidence_status") == "sourced" and calibration.get("review_required") is False:
        return "calibrated"
    return "provisional"


def _status(missing: list[str], calibration_profile: dict[str, Any]) -> str:
    if missing:
        return "missing_calibration"
    governance = calibration_profile.get("governance", {})
    if (
        calibration_profile.get("provisional")
        or governance.get("resident_consent_status") != "ratified"
        or governance.get("review_status") != "accepted"
    ):
        return "provisional_calibrated"
    return "calibrated"


def _metric_updates(status: str) -> dict[str, Any]:
    if status == "missing_calibration":
        return {
            "inspectable_simulation_proof_of_concept": "100%",
            "mature_commune_virtualization_data_contract": "100%",
            "faithful_pattern_optimization_engine": "98%",
            "rationale": "Objective calibration is incomplete for one or more metrics.",
        }
    return {
        "inspectable_simulation_proof_of_concept": "100%",
        "mature_commune_virtualization_data_contract": "100%",
        "faithful_pattern_optimization_engine": "99%",
        "rationale": "Sprint 48 makes every selected-candidate objective score traceable to an explicit calibration rule and evidence status.",
    }


def _next_actions(status: str) -> list[str]:
    if status == "missing_calibration":
        return [
            "Add calibration rules for every metric used by the selected candidate before treating optimizer scores as comparable.",
            "Do not hide uncalibrated metrics behind aggregate scores.",
        ]
    return [
        "Replace proxy formulas with sourced cost, labor, resilience, review, and dignity evidence as it becomes available.",
        "Add governance-approved weight profiles before claiming full optimization completion.",
        "Keep every high-stakes score provisional until review and resident consent are represented.",
    ]


def _unknowns(search_optimizer_report: dict[str, Any], calibration_profile: dict[str, Any]) -> list[str]:
    unknowns = set(search_optimizer_report.get("unknowns", []))
    unknowns.update(calibration_profile.get("unknowns", []))
    unknowns.add("Objective calibration makes scoring inspectable; it does not make the formulas true.")
    return sorted(unknowns)
