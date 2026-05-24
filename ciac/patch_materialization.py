from __future__ import annotations

import re
from pathlib import Path
from typing import Any

import yaml

from .io import load_data, write_json
from .validation import validate_data


def materialize_patch_proposal(
    patch_proposal: dict[str, Any],
    candidate: dict[str, Any] | None = None,
    *,
    repo_root: str | Path = ".",
    overwrite: bool = False,
    report_output: str | Path | None = None,
) -> dict[str, Any]:
    patch_validation = validate_data(patch_proposal, patch_proposal.get("id", "<patch-proposal>"))
    if candidate is None:
        candidate = infer_candidate_for_patch(patch_proposal, repo_root)
    candidate = _normalized_candidate(candidate)
    candidate_validation = validate_data(candidate, candidate.get("id", "<candidate>"))
    if not patch_validation.ok or not candidate_validation.ok:
        report = _blocked_report(
            patch_proposal,
            candidate,
            _validation_messages(patch_validation) + _validation_messages(candidate_validation),
        )
        if report_output:
            write_json(report_output, report)
        return report

    target_path = _resolve_target_path(repo_root, patch_proposal.get("target", {}).get("artifact", ""))
    pattern = build_civic_pattern_from_patch(patch_proposal, candidate)
    pattern_validation = validate_data(pattern, str(target_path))
    warnings = [f"{issue.path}: {issue.message}" for issue in pattern_validation.issues if issue.severity == "warning"]
    errors = [f"{issue.path}: {issue.message}" for issue in pattern_validation.issues if issue.severity == "error"]
    if target_path.exists() and not overwrite:
        errors.append(f"Target artifact already exists: {_display_path(target_path, repo_root)}")

    if errors:
        report = _blocked_report(patch_proposal, candidate, errors, warnings, target_path)
        if report_output:
            write_json(report_output, report)
        return report

    target_path.parent.mkdir(parents=True, exist_ok=True)
    target_path.write_text(yaml.safe_dump(pattern, sort_keys=False, allow_unicode=False), encoding="utf-8")

    report = _materialized_report(patch_proposal, candidate, pattern, target_path, repo_root, warnings)
    report_validation = validate_data(report, report.get("id", "<materialization>"))
    if not report_validation.ok:
        raise ValueError("; ".join(f"{issue.path}: {issue.message}" for issue in report_validation.issues))
    if report_output:
        write_json(report_output, report)
    return report


def infer_candidate_for_patch(patch_proposal: dict[str, Any], repo_root: str | Path = ".") -> dict[str, Any]:
    candidate_id = _safe_id(patch_proposal.get("source_candidate_id", "candidate"))
    path = Path(repo_root) / "candidate_interventions" / f"{candidate_id}.json"
    return load_data(path)


def build_civic_pattern_from_patch(patch_proposal: dict[str, Any], candidate: dict[str, Any]) -> dict[str, Any]:
    candidate_id = _safe_id(candidate.get("id") or patch_proposal.get("source_candidate_id") or "candidate")
    title = str(candidate.get("title") or patch_proposal.get("title") or candidate_id).strip()
    focus_domain = str(candidate.get("focus_domain") or patch_proposal.get("focus_domain") or "care_health")
    change_type = str(patch_proposal.get("target", {}).get("change_type") or "add_operating_protocol")
    pattern_type = "Commons" if change_type in {"add_operating_protocol", "add_governance_rule", "add_pattern"} else "Storage"
    metrics = _metrics_for_candidate(candidate)
    dependencies = _dependencies_for_candidate(candidate, change_type)
    capability_effects = _capability_effects_for_candidate(candidate, focus_domain)

    return {
        "kind": "CivicPattern",
        "id": candidate_id,
        "type": pattern_type,
        "status": "draft",
        "provisional": True,
        "provisional_for": _provisional_tags(focus_domain),
        "purpose": _purpose(candidate, title),
        "scale": _scale_for_candidate(candidate),
        "mdl_categories": _mdl_categories(focus_domain),
        "inputs": _inputs_for_candidate(candidate),
        "outputs": _outputs_for_candidate(candidate, title),
        "dependencies": dependencies,
        "constraints": _constraints_for_domain(focus_domain),
        "build_phase": 0,
        "lifecycle": _lifecycle_for_domain(candidate_id, focus_domain, metrics),
        "failure_modes": _failure_modes_for_candidate(candidate),
        "governance": _governance_for_domain(focus_domain),
        "metrics": metrics,
        "capability_effects": capability_effects,
        "simulation": {
            "resource_effects": {
                "water_liters_per_day": 0,
                "energy_kwh_per_day": -metrics["energy_use"],
                "food_servings_per_day": 0,
            },
            "critical_resources": _critical_resources_for_domain(focus_domain, metrics),
            "notes": "Materialized from a research-loop patch proposal. Effects are provisional and should be validated through illness, contamination, power-loss, and hidden-labor scenarios before promotion.",
            "provisional": True,
        },
    }


def _materialized_report(
    patch_proposal: dict[str, Any],
    candidate: dict[str, Any],
    pattern: dict[str, Any],
    target_path: Path,
    repo_root: str | Path,
    warnings: list[str],
) -> dict[str, Any]:
    external_dependencies = [
        dependency["id"]
        for dependency in pattern.get("dependencies", [])
        if dependency.get("kind") == "external" and dependency.get("critical")
    ]
    return {
        "kind": "PatchMaterializationReport",
        "version": "v0",
        "id": f"materialize_{_safe_id(patch_proposal.get('id', pattern['id']))}",
        "status": "materialized_draft",
        "source_patch_proposal_id": str(patch_proposal.get("id")),
        "source_candidate_id": str(candidate.get("id")),
        "source_candidate_title": str(candidate.get("title") or patch_proposal.get("title")),
        "focus_domain": str(candidate.get("focus_domain") or patch_proposal.get("focus_domain")),
        "materialized_kind": "CivicPattern",
        "materialized_artifact_path": _display_path(target_path, repo_root),
        "placement_target": _placement_target(candidate.get("focus_domain") or patch_proposal.get("focus_domain")),
        "validation": {
            "artifact_valid": True,
            "blocking_reasons": [],
            "warnings": warnings,
        },
        "suggested_plan_change": {
            "selected_pattern_id": pattern["id"],
            "resolved_external_dependencies": external_dependencies,
            "notes": [
                "Add selected_pattern_id to a site profile only after listed external dependencies are reviewed or represented in review status.",
                "Compile and replay illness, contamination, power-loss, and labor-burden scenarios before promotion.",
            ],
        },
        "next_actions": [
            *_next_actions_for_domain(str(candidate.get("focus_domain") or patch_proposal.get("focus_domain"))),
        ],
        "provisional": True,
    }


def _blocked_report(
    patch_proposal: dict[str, Any],
    candidate: dict[str, Any] | None,
    errors: list[str],
    warnings: list[str] | None = None,
    target_path: Path | None = None,
) -> dict[str, Any]:
    candidate = candidate or {}
    return {
        "kind": "PatchMaterializationReport",
        "version": "v0",
        "id": f"materialize_{_safe_id(patch_proposal.get('id', 'patch'))}",
        "status": "blocked",
        "source_patch_proposal_id": str(patch_proposal.get("id", "unknown_patch")),
        "source_candidate_id": str(candidate.get("id") or patch_proposal.get("source_candidate_id", "unknown_candidate")),
        "source_candidate_title": str(candidate.get("title") or patch_proposal.get("title", "Unknown candidate")),
        "focus_domain": str(candidate.get("focus_domain") or patch_proposal.get("focus_domain", "unknown")),
        "materialized_kind": "CivicPattern",
        "materialized_artifact_path": str(target_path or patch_proposal.get("target", {}).get("artifact", "")),
        "placement_target": _placement_target(candidate.get("focus_domain") or patch_proposal.get("focus_domain")),
        "validation": {
            "artifact_valid": False,
            "blocking_reasons": errors,
            "warnings": warnings or [],
        },
        "suggested_plan_change": {
            "selected_pattern_id": str(patch_proposal.get("source_candidate_id", "unknown_candidate")),
            "resolved_external_dependencies": [],
            "notes": ["Fix blocking materialization issues before changing any active site profile."],
        },
        "next_actions": ["Fix blocking materialization issues and rerun the patch materialization step."],
        "provisional": True,
    }


def _resolve_target_path(repo_root: str | Path, artifact: str) -> Path:
    root = Path(repo_root).resolve()
    target = Path(artifact)
    if not target.is_absolute():
        target = root / target
    target = target.resolve()
    if not target.is_relative_to(root):
        raise ValueError(f"Patch target escapes repo root: {artifact}")
    return target


def _display_path(path: Path, repo_root: str | Path) -> str:
    root = Path(repo_root).resolve()
    try:
        return str(path.resolve().relative_to(root))
    except ValueError:
        return str(path)


def _validation_messages(report: Any) -> list[str]:
    return [f"{issue.path}: {issue.message}" for issue in getattr(report, "issues", [])]


def _purpose(candidate: dict[str, Any], title: str) -> str:
    hypothesis = str(candidate.get("hypothesis") or "").strip()
    if len(hypothesis) >= 10:
        return hypothesis
    return f"Provide a provisional operating protocol for {title.lower()} while making evidence gaps, safety boundaries, and simulation effects explicit."


def _provisional_tags(focus_domain: str) -> list[str]:
    tags = ["legal", "health", "labor", "governance"]
    if "water" in focus_domain:
        tags.append("water")
    if focus_domain == "mobility_access":
        tags = ["engineering", "legal", "labor", "governance"]
    return tags


def _mdl_categories(focus_domain: str) -> list[str]:
    if focus_domain == "mobility_access":
        return ["commons", "contribution", "health"]
    categories = ["health", "privacy", "commons", "contribution"]
    if "water" in focus_domain:
        categories.insert(0, "water")
    return list(dict.fromkeys(categories))


def _inputs_for_candidate(candidate: dict[str, Any]) -> list[str]:
    focus_domain = str(candidate.get("focus_domain", ""))
    if focus_domain == "water_public_health":
        base = ["water_reserve_register", "sanitation_schedule", "test_and_release_log", "role_registry", "review_register"]
    elif focus_domain == "mobility_access":
        base = ["route_inventory", "daily_need_map", "accessible_route_survey", "maintenance_backlog", "review_register"]
    else:
        base = ["resident_consent", "privacy_boundary", "care_need_inventory", "role_registry", "review_register"]
    for module_ref in candidate.get("module_refs", []):
        base.append(_safe_id(module_ref))
    return list(dict.fromkeys(base))


def _outputs_for_candidate(candidate: dict[str, Any], title: str) -> list[str]:
    outputs = [_safe_id(title), "reviewable_assumption_register", "hidden_labor_visibility"]
    focus_domain = str(candidate.get("focus_domain", ""))
    if focus_domain == "water_public_health":
        outputs.extend(["explicit_water_reserve_sanitation_protocol", "public_health_review_visibility"])
    elif focus_domain == "mobility_access":
        outputs.extend(["accessible_route_gap_register", "route_status_map", "mobility_burden_visibility"])
    else:
        outputs.append("explicit_care_continuity_protocol")
    for effect in candidate.get("expected_effects", []):
        metric = _safe_id(effect.get("metric", "expected_effect"))
        outputs.append(metric)
    return list(dict.fromkeys(outputs))


def _dependencies_for_candidate(candidate: dict[str, Any], change_type: str) -> list[dict[str, Any]]:
    focus_domain = str(candidate.get("focus_domain", ""))
    if focus_domain == "water_public_health":
        return _water_dependencies_for_candidate(candidate, change_type)
    if focus_domain == "mobility_access":
        return _mobility_dependencies_for_candidate(candidate, change_type)
    dependencies = [
        {
            "id": "commons_stewardship_protocol",
            "kind": "pattern",
            "critical": False,
            "rationale": "Care continuity should align with explicit stewardship, backup authority, privacy, and anti-capture boundaries, but a draft local protocol can be reviewed before the full commons layer is selected.",
        },
        {
            "id": "local_health_privacy_review",
            "kind": "external",
            "critical": True,
            "rationale": "Medication, health data, consent, safety, and local public-health assumptions require qualified local review.",
        },
        {
            "id": "professional_care_boundary_review",
            "kind": "external",
            "critical": True,
            "rationale": "The protocol must not substitute resident labor for licensed clinical, pharmacy, emergency, or safeguarding responsibilities.",
        },
    ]
    if change_type == "add_governance_rule":
        dependencies.append(
            {
                "id": "resident_governance_consent_review",
                "kind": "external",
                "critical": True,
                "rationale": "Governance rules affecting care access need resident consent, due process, and privacy review.",
            }
        )
    if "cold" in _candidate_text(candidate) or "energy" in _candidate_text(candidate):
        dependencies.append(
            {
                "id": "critical_load_energy_commons",
                "kind": "pattern",
                "critical": True,
                "rationale": "Cold-chain medication continuity depends on reviewed critical-load energy support.",
            }
        )
    return dependencies


def _mobility_dependencies_for_candidate(candidate: dict[str, Any], change_type: str) -> list[dict[str, Any]]:
    dependencies = [
        {
            "id": "pedestrian_first_access_commons",
            "kind": "pattern",
            "critical": False,
            "rationale": "Route surveys should attach to the modeled daily-access network instead of floating as an unplaced model note.",
        },
        {
            "id": "accessibility_and_emergency_access_review",
            "kind": "external",
            "critical": True,
            "rationale": "Grade, surface, rest-point, lighting, weather, emergency-access, and code assumptions require qualified local review.",
        },
        {
            "id": "labor_burden_review",
            "kind": "external",
            "critical": True,
            "rationale": "Route mapping and gap response work must remain visible and must not become untracked resident burden.",
        },
    ]
    if change_type == "add_governance_rule":
        dependencies.append(
            {
                "id": "accessible_route_priority_review",
                "kind": "external",
                "critical": True,
                "rationale": "Route-priority rules must preserve non-driver access, disability access, and appeal paths.",
            }
        )
    return dependencies


def _water_dependencies_for_candidate(candidate: dict[str, Any], change_type: str) -> list[dict[str, Any]]:
    dependencies = [
        {
            "id": "resilient_water_commons",
            "kind": "pattern",
            "critical": False,
            "rationale": "Reserve sanitation protocol should attach to the modeled water source, reserve, testing, and recovery layer.",
        },
        {
            "id": "water_public_health_review",
            "kind": "external",
            "critical": True,
            "rationale": "Stored-water sanitation, contamination response, testing, release authority, and recovery assumptions require local public-health review.",
        },
        {
            "id": "labor_burden_review",
            "kind": "external",
            "critical": True,
            "rationale": "Reserve sanitation work must remain visible and must not become untracked resident burden.",
        },
    ]
    if change_type == "add_governance_rule":
        dependencies.append(
            {
                "id": "water_release_authority_review",
                "kind": "external",
                "critical": True,
                "rationale": "Rules for releasing stored or recovered water require explicit authority and appeal boundaries.",
            }
        )
    return dependencies


def _metrics_for_candidate(candidate: dict[str, Any]) -> dict[str, Any]:
    text = _candidate_text(candidate)
    is_water_protocol = str(candidate.get("focus_domain", "")) == "water_public_health"
    is_mobility_protocol = str(candidate.get("focus_domain", "")) == "mobility_access"
    has_cold_chain = "cold" in text or "refriger" in text
    has_rota = "rota" in text or "steward" in text
    return {
        "cost": 1800 if is_mobility_protocol else 12000 if has_cold_chain else 3500 if has_rota else 5000,
        "build_labor_hours": 16 if is_mobility_protocol else 48 if has_cold_chain else 30 if has_rota else 24,
        "recurring_labor_hours_per_week": 1 if is_mobility_protocol else 3 if has_rota else 1.5,
        "energy_use": 0 if is_water_protocol or is_mobility_protocol else 1.2 if has_cold_chain else 0.1,
        "water_use": 0,
        "embodied_carbon": 0.4 if has_cold_chain else 0.1,
        "maintenance_burden": 2 if has_cold_chain else 1,
        "dignity_score": 9,
        "autonomy_score": 8,
        "resilience_score": 9,
        "provisional": True,
    }


def _capability_effects_for_candidate(candidate: dict[str, Any], focus_domain: str) -> dict[str, Any]:
    if focus_domain == "water_public_health":
        return {
            "water_public_health": {
                "reserve_sanitation_protocol_supported": True,
                "public_health_review_required": True,
                "recovery_labor_visibility_supported": True,
            },
            "labor_time": {
                "hidden_labor_tracking_supported": True,
                "water_recovery_labor_visibility_supported": True,
            },
        }
    if focus_domain == "mobility_access":
        coverage_delta = 0.25 if any(_safe_id(effect.get("metric", "")) == "accessible_route_coverage" for effect in candidate.get("expected_effects", [])) else 0.1
        return {
            "mobility_access": {
                "route_gap_survey_supported": True,
                "accessible_route_status_visibility_supported": True,
                "emergency_access_status_declared": True,
                "accessible_route_coverage_delta": coverage_delta,
            },
            "labor_time": {
                "hidden_labor_tracking_supported": True,
                "mobility_labor_visibility_supported": True,
            },
        }
    text = _candidate_text(candidate)
    care_effects: dict[str, Any] = {
        "care_continuity_protocol_supported": True,
        "reviewable_assumption_register_supported": True,
        "privacy_boundary_required": True,
    }
    if "medication" in text or "medicine" in text or "cold" in text:
        care_effects["medication_continuity_supported"] = True
    if "steward" in text or "rota" in text or "high_need" in text:
        care_effects["high_need_support_coverage_delta"] = 0.10
        care_effects["role_backup_coverage_delta"] = 0.10
    effects = {focus_domain: care_effects}
    effects["labor_time"] = {
        "hidden_labor_tracking_supported": True,
        "care_labor_visibility_supported": True,
    }
    return effects


def _failure_modes_for_candidate(candidate: dict[str, Any]) -> list[dict[str, Any]]:
    modes = []
    for risk in candidate.get("risk_tradeoffs", [])[:3]:
        modes.append(
            {
                "mode": _safe_id(risk.get("risk", "care_continuity_failure")),
                "likelihood": "medium",
                "severity": "high" if risk.get("severity") in {"high", "unknown"} else str(risk.get("severity", "medium")),
                "detection_method": "resident report, steward review, audit log, scenario replay, or external professional handoff trigger",
                "mitigation": str(risk.get("mitigation") or "Pause unsafe practice, assign backup role, and escalate to qualified review."),
            }
        )
    if modes:
        return modes
    return [
        {
            "mode": "care_continuity_gap",
            "likelihood": "medium",
            "severity": "high",
            "detection_method": "missed continuity check, resident report, steward backup failure, or scenario replay warning",
            "mitigation": "Activate backup steward, restore minimum continuity, record hidden labor, and escalate to qualified local review.",
        }
    ]


def _scale_for_candidate(candidate: dict[str, Any]) -> str:
    text = _candidate_text(candidate)
    if "cabinet" in text or "kit" in text:
        return "room"
    return "village"


def _candidate_text(candidate: dict[str, Any]) -> str:
    fields = [
        candidate.get("id", ""),
        candidate.get("title", ""),
        candidate.get("hypothesis", ""),
        " ".join(str(item) for item in candidate.get("module_refs", [])),
    ]
    return " ".join(fields).lower()


def _safe_id(value: Any) -> str:
    return re.sub(r"[^a-z0-9_]+", "_", str(value).lower()).strip("_") or "artifact"


def _normalized_candidate(candidate: dict[str, Any]) -> dict[str, Any]:
    normalized = dict(candidate)
    effects = []
    for effect in candidate.get("expected_effects", []):
        item = dict(effect)
        item["direction"] = _normalized_effect_direction(item.get("direction"))
        effects.append(item)
    if effects:
        normalized["expected_effects"] = effects
    return normalized


def _normalized_effect_direction(value: Any) -> str:
    direction = str(value or "unknown").strip().lower()
    if direction in {"increase", "decrease", "neutral", "unknown"}:
        return direction
    if direction in {"pass", "passed", "improve", "improved", "improvement", "resolve", "resolved"}:
        return "increase"
    if direction in {"fail", "failed", "worsen", "worse", "regress", "regressed"}:
        return "decrease"
    if direction in {"stable", "same", "unchanged", "maintain", "maintained"}:
        return "neutral"
    return "unknown"


def _constraints_for_domain(focus_domain: str) -> dict[str, list[str]]:
    if focus_domain == "water_public_health":
        return {
            "physical": [
                "Keep water reserve inspection, sanitation, isolation, test, release, and fallback paths explicit at the water node.",
                "Separate potable reserve status from general commons notes so unsafe or unreviewed water cannot appear available.",
            ],
            "ecological": [
                "Prefer low-waste testing, rotation, and reserve-maintenance practices that do not create avoidable discard cycles.",
            ],
            "legal": [
                "Potable-water testing, contamination response, release authority, and public-health assumptions require local qualified review.",
                "This draft does not certify potable water safety or authorize unlicensed public-health decisions.",
            ],
            "social": [
                "Sanitation and recovery labor must be scheduled, visible, and bounded so residents are not silently assigned emergency burden.",
                "Reserve access rules must not privilege residents by status, role, popularity, or ability to perform maintenance work.",
            ],
            "safety": [
                "Contaminated, uncertain, or untested reserve water must remain isolated until reviewed release criteria are met.",
                "Fallback supply, conservative no-release defaults, and escalation thresholds must be explicit during contamination events.",
            ],
        }
    if focus_domain == "mobility_access":
        return {
            "physical": [
                "Every daily-need route claim must identify grade, surface, clear width, rest points, lighting status, weather exposure, and emergency-access status.",
                "The survey may improve modeled route visibility, but it must not claim full accessible-route coverage until gaps are resolved or explicitly accepted as blockers.",
            ],
            "ecological": [
                "Prefer repair, surface improvement, shade, lighting efficiency, and route consolidation before adding avoidable paved area.",
            ],
            "legal": [
                "Accessibility, emergency access, public-way, lighting, drainage, and code assumptions require qualified local review.",
                "This draft does not certify ADA, fire, building-code, transportation, or public-realm compliance.",
            ],
            "social": [
                "Non-driver access, disability access, weather exposure, trip burden, and high-need resident routes must be visible in the review register.",
                "Route priority must not make daily needs depend on car access, popularity, informal labor availability, or unreviewable role authority.",
            ],
            "safety": [
                "Blocked emergency routes, unsafe grades, poor lighting, heat exposure, ice risk, and missing rest points must remain explicit blockers until resolved.",
                "Survey labor and remediation labor must be tracked so access gaps are not converted into hidden resident burden.",
            ],
        }
    return {
        "physical": [
            "Maintain a visible inventory, storage location, access boundary, and backup handoff for every resident-facing care continuity item.",
            "Keep protected health, medication, identity, and caregiver information separate from general commons records.",
        ],
        "ecological": [
            "Prefer low-energy, low-waste storage and procurement paths, and avoid creating discard cycles for still-usable supplies.",
        ],
        "legal": [
            "Medication, clinical, privacy, consent, controlled-substance, prescription, and professional-scope assumptions require local legal and health review.",
            "This draft does not authorize diagnosis, prescribing, dispensing, or unlicensed clinical care.",
        ],
        "social": [
            "Resident participation must remain consent-based, privacy-preserving, and accessible to residents with limited time, disability, or high support needs.",
            "The protocol must not make medication access depend on popularity, ideology, informal social standing, or unreviewable role authority.",
        ],
        "safety": [
            "Emergency access, cold-chain continuity, medication error prevention, contamination, spoilage, diversion, and safeguarding must have explicit escalation paths.",
            "Care stewards must have stop-work authority and external professional handoff thresholds when resident safety is uncertain.",
        ],
    }


def _lifecycle_for_domain(candidate_id: str, focus_domain: str, metrics: dict[str, Any]) -> dict[str, Any]:
    if focus_domain == "water_public_health":
        return {
            "build_sequence": [
                "define reserve inspection, sanitation, isolation, testing, fallback supply, and release-authority boundaries",
                "map reserve sanitation labor without assigning invisible emergency burden to residents",
                "assign primary and backup water stewardship roles with public-health escalation thresholds",
                "record evidence gaps, local review dependencies, and water-contamination scenario tests before promotion",
            ],
            "inspection_points": [
                "reserve level and isolation state",
                "sanitation schedule and visible labor hours",
                "public-health review status",
                "test-and-release criteria",
                "fallback supply and emergency access path",
            ],
            "maintenance": [
                {
                    "id": f"{_safe_id(candidate_id)}_reserve_sanitation_round",
                    "description": "Review water reserve sanitation records, labor visibility, isolation status, testing assumptions, and release thresholds.",
                    "interval": "weekly",
                    "role": "water_steward",
                    "estimated_hours": metrics["recurring_labor_hours_per_week"],
                    "provisional": True,
                }
            ],
            "expected_lifespan": "ongoing protocol with monthly water public-health, labor-burden, and recovery review",
            "repair_procedure": [
                "classify the issue as contamination, unclear reserve status, missed sanitation, labor overload, testing gap, release-authority gap, or fallback supply risk",
                "isolate uncertain reserve water, activate fallback supply, preserve minimum continuity, and escalate to public-health review when needed",
                "record correction, affected assumptions, visible labor burden, scenario impact, and follow-up review date",
            ],
            "end_of_life_path": [
                "retire outdated sanitation records under public-health and governance rules",
                "dispose, flush, retest, or recommission reserve components under reviewed safety requirements",
                "preserve non-sensitive lessons needed for future water resilience modeling",
            ],
        }
    if focus_domain == "mobility_access":
        return {
            "build_sequence": [
                "inventory daily-need destinations and routes from housing to food, water, care, commons, sanitation, maintenance, and emergency access points",
                "record grade, surface, clear width, rest points, lighting, weather exposure, non-driver burden, and emergency-access status for each route",
                "map route gaps into the maintenance backlog with resident-visible priority and labor burden",
                "record evidence gaps, local review dependencies, and route-failure scenario tests before treating coverage as complete",
            ],
            "inspection_points": [
                "accessible-route coverage and remaining gaps",
                "non-driver access to daily needs",
                "emergency access status",
                "surface, grade, rest-point, lighting, and weather-exposure status",
                "hidden labor and high-need resident trip burden",
            ],
            "maintenance": [
                {
                    "id": f"{_safe_id(candidate_id)}_route_gap_survey_round",
                    "description": "Review accessible route survey records, unresolved gaps, non-driver access burden, emergency access status, and maintenance follow-up.",
                    "interval": "weekly",
                    "role": "mobility_steward",
                    "estimated_hours": metrics["recurring_labor_hours_per_week"],
                    "provisional": True,
                }
            ],
            "expected_lifespan": "ongoing route survey and maintenance-priority protocol with monthly accessibility and emergency-access review",
            "repair_procedure": [
                "classify the issue as grade, surface, clear width, rest point, lighting, weather exposure, emergency access, non-driver access, or hidden labor burden",
                "mark the affected route as incomplete, assign a visible maintenance response or workaround, and escalate to qualified review when safety is uncertain",
                "record correction, affected residents, labor burden, scenario impact, and follow-up review date",
            ],
            "end_of_life_path": [
                "retire outdated route maps only after replacement maps are active",
                "archive non-sensitive access lessons needed for future layout and scaling decisions",
                "preserve unresolved blocker history until the route is repaired, redesigned, or formally removed from daily-need service",
            ],
        }
    return {
        "build_sequence": [
            "define resident consent, privacy, access, professional handoff, emergency, and audit boundaries",
            "map resident-controlled continuity needs without exposing protected personal details to general governance",
            "assign primary and backup stewardship roles with escalation and review thresholds",
            "record evidence gaps, local review dependencies, and scenario tests before promotion",
        ],
        "inspection_points": [
            "consent and privacy boundaries",
            "local health and legal review status",
            "resident access and backup access paths",
            "cold-chain, storage, spoilage, and emergency continuity checks",
            "hidden labor and high-need resident burden",
        ],
        "maintenance": [
            {
                "id": f"{_safe_id(candidate_id)}_continuity_round",
                "description": "Review continuity records, access boundaries, stock or rota status, evidence gaps, and professional handoff thresholds.",
                "interval": "weekly",
                "role": "care_steward",
                "estimated_hours": metrics["recurring_labor_hours_per_week"],
                "provisional": True,
            }
        ],
        "expected_lifespan": "ongoing protocol with monthly resident, privacy, safety, and local compliance review",
        "repair_procedure": [
            "classify the issue as consent, privacy, access, cold-chain, medication error, role coverage, hidden labor, emergency handoff, or local compliance risk",
            "pause unsafe practice, assign backup steward, preserve minimum continuity, and escalate to external professional review when needed",
            "record correction, affected assumptions, resident burden, scenario impact, and follow-up review date",
        ],
        "end_of_life_path": [
            "retire protected records under privacy and retention rules",
            "return, dispose, or transfer supplies under reviewed local health and safety requirements",
            "preserve only non-sensitive learning needed for future model improvement",
        ],
    }


def _governance_for_domain(focus_domain: str) -> dict[str, str]:
    if focus_domain == "water_public_health":
        return {
            "owner": "commons",
            "access_rule": "Reserve sanitation and release decisions are visible, review-bound, and conservative by default; unsafe or untested water remains isolated.",
            "stewardship_role": "water_steward",
            "backup_role": "backup_water_steward",
            "audit_frequency": "monthly",
            "capture_risk": "Water reserve access and release authority can become coercive if public-health review, labor burden, or fallback supply paths are not visible.",
        }
    if focus_domain == "mobility_access":
        return {
            "owner": "commons",
            "access_rule": "Route status, gaps, priorities, and temporary workarounds are visible and review-bound; unresolved access blockers cannot be hidden by population scaling.",
            "stewardship_role": "mobility_steward",
            "backup_role": "backup_mobility_steward",
            "audit_frequency": "monthly",
            "capture_risk": "Mobility access can become coercive if daily needs, emergency access, or route priorities depend on car access, informal status, or invisible resident labor.",
        }
    return {
        "owner": "commons",
        "access_rule": "Access is resident-controlled and privacy-limited, with care steward support only under explicit consent, emergency threshold, or reviewed professional handoff rule.",
        "stewardship_role": "care_steward",
        "backup_role": "backup_care_steward",
        "audit_frequency": "monthly",
        "capture_risk": "Care continuity can become coercive if medication access, health data, or emergency discretion is controlled by unreviewable residents or roles.",
    }


def _critical_resources_for_domain(focus_domain: str, metrics: dict[str, Any]) -> list[str]:
    if focus_domain == "water_public_health":
        return ["maintenance", "water"]
    if focus_domain == "mobility_access":
        return ["maintenance"]
    return ["maintenance", "energy"] if metrics["energy_use"] > 0 else ["maintenance"]


def _next_actions_for_domain(focus_domain: str) -> list[str]:
    if focus_domain == "water_public_health":
        return [
            "Validate the materialized CivicPattern artifact.",
            "Resolve local public-health, potable-water safety, release-authority, consent, and labor-burden assumptions.",
            "Run simulation comparisons before selecting this pattern in an active site profile.",
        ]
    if focus_domain == "mobility_access":
        return [
            "Validate the materialized CivicPattern artifact.",
            "Resolve local accessibility, emergency-access, engineering, safety, consent, and labor-burden assumptions.",
            "Run simulation comparisons before selecting this pattern in an active site profile.",
        ]
    return [
        "Validate the materialized CivicPattern artifact.",
        "Resolve local health, privacy, consent, safety, and professional-boundary assumptions.",
        "Run simulation comparisons before selecting this pattern in an active site profile.",
    ]


def _placement_target(focus_domain: Any) -> dict[str, str]:
    domain = str(focus_domain or "")
    if domain == "care_health":
        return {
            "object_id": "structure_care_room",
            "label": "Care Room",
            "relationship": "contained_module",
        }
    if domain == "labor_time":
        return {
            "object_id": "structure_quiet_studio",
            "label": "Quiet Studio",
            "relationship": "contained_module",
        }
    if domain == "governance_anticapture":
        return {
            "object_id": "structure_common_house",
            "label": "Common House",
            "relationship": "contained_module",
        }
    if domain == "water_public_health":
        return {
            "object_id": "node_water_reserve",
            "label": "Water Source + Reserve",
            "relationship": "attached_operating_protocol",
        }
    if domain == "mobility_access":
        return {
            "object_id": "zone_mobility_loop",
            "label": "Mobility Loop / Daily Route Network",
            "relationship": "attached_operating_protocol",
        }
    return {
        "object_id": "",
        "label": "Unplaced Model Layer",
        "relationship": "model_layer",
    }
