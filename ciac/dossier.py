from __future__ import annotations

from typing import Any


REVIEW_CATALOG = [
    ("water_public_health", "Water / public health review", "water", "licensed water/public-health professional"),
    ("electrical", "Electrical review", "energy", "licensed electrician or electrical engineer"),
    ("structural_building", "Structural/building review", "shelter", "licensed design/building professional"),
    ("sanitation", "Sanitation review", "sanitation", "qualified sanitation/public-health authority"),
    ("food_safety", "Food safety review", "food", "qualified food-safety reviewer"),
    ("accessibility_care", "Accessibility and care review", "care", "accessibility/care specialist and affected residents"),
    ("governance_legal", "Governance/legal review", "governance", "qualified legal/governance counsel"),
    ("insurance_liability", "Insurance/liability review", "risk", "insurance and liability professional"),
]


def generate_dossier(audit_report: dict[str, Any], compiled_plan: dict[str, Any]) -> dict[str, Any]:
    warnings = _warnings_by_subsystem(audit_report)
    decision = audit_report.get("promotion_decision", "do_not_promote")
    readiness = _readiness_status(audit_report, warnings)

    return {
        "kind": "PilotDossier",
        "id": f"{compiled_plan['id']}_{audit_report['id']}_dossier",
        "compiled_plan": compiled_plan["id"],
        "audit_report": audit_report["id"],
        "generated_by": "ciac.dossier.v0",
        "provisional": True,
        "current_promotion_decision": decision,
        "readiness_status": readiness,
        "unresolved_warnings_by_subsystem": warnings,
        "required_professional_reviews": _required_reviews(warnings),
        "legal_jurisdictional_unknowns": _legal_unknowns(compiled_plan),
        "evidence_gaps": _evidence_gaps(audit_report, warnings),
        "resident_governance_questions": _governance_questions(audit_report),
        "documents_needed_before_pilot": _documents_needed(),
        "go_no_go_checklist": _go_no_go_checklist(audit_report, warnings),
        "must_never_be_inferred": _must_never_be_inferred(),
        "unknowns": [
            "This dossier is a software-generated review package, not a permit, certification, professional opinion, or consent process.",
            "Every review item requires jurisdiction-specific and site-specific evidence before real-world use.",
            "No generated status should override resident consent, professional judgment, or law.",
        ],
    }


def _warnings_by_subsystem(audit_report: dict[str, Any]) -> dict[str, list[str]]:
    grouped: dict[str, list[str]] = {}
    for warning in audit_report.get("noncritical_warnings", []):
        subsystem = warning.split(":", 1)[0] if ":" in warning else "general"
        grouped.setdefault(subsystem, []).append(warning)
    return {key: sorted(set(values)) for key, values in sorted(grouped.items())}


def _readiness_status(audit_report: dict[str, Any], warnings: dict[str, list[str]]) -> str:
    if audit_report.get("promotion_decision") == "do_not_promote":
        return "not_ready"
    if warnings or audit_report.get("promotion_decision") == "revise_before_pilot":
        return "review_package_needed"
    return "candidate_for_external_review"


def _required_reviews(warnings: dict[str, list[str]]) -> list[dict[str, Any]]:
    reviews: list[dict[str, Any]] = []
    warning_text = " ".join(item for values in warnings.values() for item in values).lower()
    for review_id, title, subsystem, reviewer in REVIEW_CATALOG:
        required = True
        reason = "Required for any real-world pilot review."
        if subsystem in warning_text:
            reason = f"Required and directly implicated by unresolved {subsystem} warnings."
        reviews.append(
            {
                "id": review_id,
                "title": title,
                "subsystem": subsystem,
                "required": required,
                "reviewer": reviewer,
                "reason": reason,
            }
        )
    return reviews


def _legal_unknowns(compiled_plan: dict[str, Any]) -> list[str]:
    site = compiled_plan.get("site_summary", {})
    return [
        f"No jurisdiction-specific zoning, building, water, sanitation, health, labor, or occupancy review is attached for site type {site.get('site_type', 'unknown')}.",
        "No land tenure, commons asset lock, easement, water rights, or cooperative governance instrument is verified.",
        "No permitting pathway is validated for dwellings, shared bathhouse, composting, well, rainwater, food preparation, workshop, or energy systems.",
        "No insurance, liability, emergency service access, or resident protection review is attached.",
    ]


def _evidence_gaps(audit_report: dict[str, Any], warnings: dict[str, list[str]]) -> list[str]:
    gaps = [
        "Professional review evidence is absent for all safety-critical systems.",
        "All current subsystem values remain provisional seed assumptions.",
        "No physical site survey, soil test, water quality lab report, load calculation, engineering drawing, or code analysis is attached.",
        "No resident consent record, role agreement, conflict process, or exit-rights procedure is attached.",
    ]
    for subsystem in sorted(warnings):
        gaps.append(f"Unresolved {subsystem} warnings require evidence before pilot review.")
    if audit_report.get("confidence") == "low":
        gaps.append("Audit confidence is low.")
    return gaps


def _governance_questions(audit_report: dict[str, Any]) -> list[str]:
    questions = [
        "Who can pause, refuse, or leave commons labor without losing access to MDL?",
        "Who holds emergency authority, for how long, and how is it audited afterward?",
        "How are children, elders, disabled residents, medically vulnerable residents, and high-care households protected?",
        "How are care work, conflict mediation, and invisible labor counted without becoming surveillance?",
        "What assets are permanently non-market, and what legal mechanism protects them?",
        "What failure would trigger shutdown, external intervention, or redesign?",
    ]
    if audit_report.get("promotion_decision") != "candidate_for_review":
        questions.append("Which warnings must be resolved before residents are asked to consider participation?")
    return questions


def _documents_needed() -> list[str]:
    return [
        "Site survey and access plan",
        "Jurisdiction-specific permitting matrix",
        "Water source test results and water safety plan",
        "Sanitation design and public-health review",
        "Electrical load calculation and qualified review",
        "Structural/building drawings and inspection plan",
        "Food safety and storage plan",
        "Accessibility and care plan",
        "Role rotation, backup, burnout, and consent policy",
        "Commons governance and asset-lock documents",
        "Emergency response procedures",
        "Insurance and liability review",
        "Resident exit-rights and conflict-resolution process",
    ]


def _go_no_go_checklist(audit_report: dict[str, Any], warnings: dict[str, list[str]]) -> list[dict[str, Any]]:
    blockers = audit_report.get("survival_critical_blockers", [])
    return [
        {
            "item": "No survival-critical blockers remain in audit.",
            "status": "pass" if not blockers else "fail",
            "evidence": f"{len(blockers)} survival-critical blocker(s).",
        },
        {
            "item": "All unresolved warnings are assigned to review owners.",
            "status": "fail" if warnings else "pass",
            "evidence": f"{sum(len(values) for values in warnings.values())} unresolved warning(s).",
        },
        {
            "item": "Professional reviews are complete.",
            "status": "fail",
            "evidence": "No professional review artifacts are attached in CIaC Sprint 14.",
        },
        {
            "item": "Jurisdiction-specific legal path is documented.",
            "status": "fail",
            "evidence": "No jurisdiction-specific legal path is attached.",
        },
        {
            "item": "Resident governance and exit-rights package is documented.",
            "status": "fail",
            "evidence": "No signed or reviewed governance package is attached.",
        },
    ]


def _must_never_be_inferred() -> list[str]:
    return [
        "Do not infer that a generated plan is legally permitted.",
        "Do not infer that a structure, water system, sanitation system, energy system, or food process is safe.",
        "Do not infer that residents consent to role obligations.",
        "Do not infer that vulnerable residents are protected without direct review.",
        "Do not infer that commons governance prevents abuse without enforceable procedures.",
        "Do not infer that candidate_for_review means approved for construction, occupancy, fundraising, or recruitment.",
    ]

