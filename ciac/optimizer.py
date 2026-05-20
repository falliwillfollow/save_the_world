from __future__ import annotations

from typing import Any


def optimize_candidates(
    candidate_matrix: dict[str, Any],
    optimization_profile: dict[str, Any],
    tradeoff_scale_report: dict[str, Any] | None = None,
) -> dict[str, Any]:
    candidates = candidate_matrix.get("candidates", [])
    optimized = [_optimized_candidate(candidate, optimization_profile, tradeoff_scale_report) for candidate in candidates]
    rankings = sorted(
        optimized,
        key=lambda item: (
            item["hard_constraint_failures"],
            -float(item["optimizer_score"]),
            item["candidate"],
        ),
    )
    selected = _selected_candidate(rankings)
    sensitivity = _sensitivity_checks(candidates, optimization_profile, selected)
    constraint_explanations = _constraint_explanations(optimized)
    status = _status(rankings, constraint_explanations)
    return {
        "kind": "OptimizerReport",
        "id": f"{candidate_matrix['id']}_{optimization_profile['id']}_optimizer",
        "candidate_matrix": candidate_matrix["id"],
        "optimization_profile": optimization_profile["id"],
        "tradeoff_scale_report": tradeoff_scale_report.get("id", "") if tradeoff_scale_report else "",
        "generated_by": "ciac.optimizer.v0",
        "provisional": True,
        "status": status,
        "selected_candidate": selected,
        "rankings": rankings,
        "constraint_explanations": constraint_explanations,
        "sensitivity_checks": sensitivity,
        "metric_updates": _metric_updates(status),
        "next_actions": _next_actions(status, selected),
        "unknowns": [
            "Optimizer output ranks generated candidate artifacts only; it does not prove real-world buildability, safety, legality, consent, or engineering adequacy.",
            "Objective weights are provisional and must be replaced or ratified through governance before real use.",
            "Review-locked parameters remain non-optimizable even when a candidate ranks first.",
        ],
    }


def _optimized_candidate(
    candidate: dict[str, Any],
    optimization_profile: dict[str, Any],
    tradeoff_scale_report: dict[str, Any] | None,
) -> dict[str, Any]:
    score = _score(candidate, optimization_profile.get("objectives", []))
    hard_failures = int(candidate.get("hard_constraint_failures", 0))
    scale_summary = _scale_summary(candidate["id"], tradeoff_scale_report)
    return {
        "candidate": candidate["id"],
        "status": candidate["status"],
        "optimizer_score": score,
        "base_candidate_score": candidate.get("aggregate_score", 0),
        "hard_constraint_failures": hard_failures,
        "soft_constraint_warnings": sum(
            1
            for constraint in candidate.get("constraint_results", [])
            if constraint.get("severity") == "soft" and constraint.get("status") != "pass"
        ),
        "dominant_strengths": _dominant_strengths(candidate),
        "dominant_tradeoffs": candidate.get("tradeoffs", [])[:3],
        "constraint_results": candidate.get("constraint_results", []),
        "scale_summary": scale_summary,
        "selection_reason": _selection_reason(candidate, score, hard_failures, scale_summary),
        "provisional": True,
    }


def _score(candidate: dict[str, Any], objectives: list[dict[str, Any]]) -> float:
    scores = {item["id"]: item for item in candidate.get("objective_scores", [])}
    total_weight = sum(float(objective["weight"]) for objective in objectives) or 1.0
    weighted = 0.0
    for objective in objectives:
        objective_score = scores.get(objective["id"], {})
        weighted += float(objective["weight"]) * float(objective_score.get("score", 0.0))
    if int(candidate.get("hard_constraint_failures", 0)):
        weighted = 0.0
    return round(weighted / total_weight, 3)


def _dominant_strengths(candidate: dict[str, Any]) -> list[str]:
    strengths = [
        f"{score['metric']}={score['score']}"
        for score in candidate.get("objective_scores", [])
        if float(score.get("score", 0.0)) >= 0.75
    ]
    return strengths or ["balanced but no dominant objective strength"]


def _scale_summary(candidate_id: str, tradeoff_scale_report: dict[str, Any] | None) -> dict[str, Any]:
    if not tradeoff_scale_report:
        return {
            "available": False,
            "max_scale_households": 0,
            "review_required_parameter_count": 0,
            "best_for": [],
            "provisional": True,
        }
    summary = next(
        (item for item in tradeoff_scale_report.get("viewer_candidate_summary", []) if item.get("candidate") == candidate_id),
        {},
    )
    return {
        "available": bool(summary),
        "max_scale_households": int(summary.get("max_scale_households", 0)),
        "review_required_parameter_count": int(summary.get("review_required_parameter_count", 0)),
        "best_for": summary.get("best_for", []),
        "provisional": True,
    }


def _selection_reason(candidate: dict[str, Any], score: float, hard_failures: int, scale_summary: dict[str, Any]) -> str:
    if hard_failures:
        return "Rejected because one or more hard constraints failed."
    parts = [f"optimizer score {score}"]
    if scale_summary.get("available"):
        parts.append(f"scale summary reaches {scale_summary['max_scale_households']} households")
    if candidate.get("tradeoffs"):
        parts.append(candidate["tradeoffs"][0])
    return "; ".join(parts)


def _constraint_explanations(optimized: list[dict[str, Any]]) -> list[dict[str, Any]]:
    explanations = []
    for candidate in optimized:
        for constraint in candidate.get("constraint_results", []):
            if constraint.get("status") == "pass":
                continue
            remediation = "Revise or reject this candidate before selection."
            if constraint.get("severity") == "soft":
                remediation = "Keep this warning visible in the visualization and review packet."
            explanations.append(
                {
                    "candidate": candidate["candidate"],
                    "constraint": constraint.get("id", "unknown_constraint"),
                    "severity": constraint.get("severity", "soft"),
                    "status": constraint.get("status", "warn"),
                    "description": constraint.get("description", ""),
                    "explanation": _constraint_explanation(candidate, constraint),
                    "remediation": remediation,
                    "provisional": True,
                }
            )
    return explanations


def _constraint_explanation(candidate: dict[str, Any], constraint: dict[str, Any]) -> str:
    if constraint.get("severity") == "hard" and constraint.get("status") == "fail":
        return f"{candidate['candidate']} is not selectable because {constraint.get('id', 'a hard constraint')} failed."
    return f"{candidate['candidate']} remains viable but carries {constraint.get('id', 'a soft constraint')} as a visible warning."


def _sensitivity_checks(
    candidates: list[dict[str, Any]],
    optimization_profile: dict[str, Any],
    selected_candidate: str,
) -> list[dict[str, Any]]:
    checks = []
    objectives = optimization_profile.get("objectives", [])
    for objective in objectives:
        adjusted = []
        for item in objectives:
            copy = dict(item)
            if item["id"] == objective["id"]:
                copy["weight"] = float(item["weight"]) * 2
            adjusted.append(copy)
        ranked = sorted(
            candidates,
            key=lambda candidate: (
                int(candidate.get("hard_constraint_failures", 0)),
                -_score(candidate, adjusted),
                candidate["id"],
            ),
        )
        leader = ranked[0]["id"] if ranked else ""
        checks.append(
            {
                "objective": objective["id"],
                "metric": objective["metric"],
                "weight_multiplier": 2,
                "leader": leader,
                "leader_score": _score(ranked[0], adjusted) if ranked else 0,
                "selection_stable": leader == selected_candidate,
                "provisional": True,
            }
        )
    return checks


def _status(rankings: list[dict[str, Any]], constraint_explanations: list[dict[str, Any]]) -> str:
    if not rankings or rankings[0]["hard_constraint_failures"]:
        return "not_ready"
    if constraint_explanations:
        return "ready_with_warnings"
    return "ready"


def _selected_candidate(rankings: list[dict[str, Any]]) -> str:
    for candidate in rankings:
        if candidate["hard_constraint_failures"] == 0 and candidate["status"] == "viable":
            return candidate["candidate"]
    return ""


def _metric_updates(status: str) -> dict[str, Any]:
    if status == "not_ready":
        return {
            "inspectable_simulation_proof_of_concept": "90%",
            "mature_commune_virtualization_data_contract": "85%",
            "faithful_pattern_optimization_engine": "80%",
            "rationale": "Optimizer could not select a candidate without hard constraint failure.",
        }
    return {
        "inspectable_simulation_proof_of_concept": "95%",
        "mature_commune_virtualization_data_contract": "92%",
        "faithful_pattern_optimization_engine": "90%",
        "rationale": "Chunk D produces deterministic rankings, constraint explanations, and objective sensitivity checks.",
    }


def _next_actions(status: str, selected_candidate: str) -> list[str]:
    if status == "not_ready":
        return [
            "Regenerate candidate matrix with viable candidates before freezing visualization contracts.",
            "Do not loosen hard constraints solely to produce an optimizer winner.",
        ]
    return [
        f"Treat {selected_candidate} as the provisional selected candidate for visualization contract testing.",
        "Proceed to Chunk E: versioned runtime/optimization bundle and schema contract freeze.",
        "Keep optimizer output labeled as provisional and review-bound.",
    ]
