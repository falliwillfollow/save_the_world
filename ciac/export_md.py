from __future__ import annotations

from pathlib import Path
from typing import Any


def render_review_packet(
    compiled_plan: dict[str, Any],
    audit_report: dict[str, Any],
    dossier: dict[str, Any],
    review_status: dict[str, Any],
    artifact_paths: dict[str, str] | None = None,
) -> str:
    paths = artifact_paths or {}
    lines: list[str] = [
        "# CIaC Review Packet",
        "",
        "## Executive Summary",
        "",
        f"- Compiled plan: `{compiled_plan.get('id', 'unknown')}`",
        f"- Audit decision: `{audit_report.get('promotion_decision', 'unknown')}`",
        f"- Audit status: `{audit_report.get('overall_status', 'unknown')}`",
        f"- Dossier readiness: `{dossier.get('readiness_status', 'unknown')}`",
        f"- Review evidence status: `{review_status.get('status', 'unknown')}`",
        "",
        "This packet is a human-readable summary of generated CIaC evidence. It is not a permit, certification, professional opinion, construction approval, or resident consent process.",
        "",
    ]

    lines.extend(_artifact_links(paths))
    lines.extend(_current_status(audit_report, dossier, review_status))
    lines.extend(_improvements(audit_report))
    lines.extend(_remaining_warnings(dossier))
    lines.extend(_required_reviews(dossier))
    lines.extend(_review_evidence(review_status))
    lines.extend(_go_no_go(dossier, review_status))
    lines.extend(_must_never_infer(dossier))
    lines.extend(_next_actions(audit_report, dossier, review_status))
    return "\n".join(lines).rstrip() + "\n"


def write_review_packet(path: str | Path, content: str) -> None:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding="utf-8")


def _artifact_links(paths: dict[str, str]) -> list[str]:
    if not paths:
        return []
    lines = ["## Evidence Artifacts", ""]
    for label in ("compiled_plan", "audit", "dossier", "review"):
        if label in paths:
            lines.append(f"- {label.replace('_', ' ').title()}: `{paths[label]}`")
    lines.append("")
    return lines


def _current_status(audit_report: dict[str, Any], dossier: dict[str, Any], review_status: dict[str, Any]) -> list[str]:
    blockers = audit_report.get("survival_critical_blockers", [])
    warnings = audit_report.get("noncritical_warnings", [])
    return [
        "## Current Status",
        "",
        f"- Survival-critical blockers: `{len(blockers)}`",
        f"- Noncritical warnings: `{len(warnings)}`",
        f"- Required reviews covered: `{len(review_status.get('required_reviews_covered', []))}`",
        f"- Required reviews missing: `{len(review_status.get('required_reviews_missing', []))}`",
        f"- Expired or rejected evidence items: `{len(review_status.get('expired_or_rejected_evidence', []))}`",
        f"- Current promotion decision: `{dossier.get('current_promotion_decision', 'unknown')}`",
        "",
    ]


def _improvements(audit_report: dict[str, Any]) -> list[str]:
    statuses = audit_report.get("subsystem_statuses", {})
    pass_count = sum(1 for item in statuses.values() if item.get("status") == "pass")
    warn_count = sum(1 for item in statuses.values() if item.get("status") == "warn")
    fail_count = sum(1 for item in statuses.values() if item.get("status") == "fail")
    lines = [
        "## What Improved Across Iterations",
        "",
        "- This packet summarizes the current evidence snapshot. Compare reports remain the source of truth for before/after claims.",
        f"- Current subsystem counts: `{pass_count}` pass, `{warn_count}` warn, `{fail_count}` fail.",
    ]
    scenarios = audit_report.get("inputs", {}).get("scenarios", [])
    if scenarios:
        lines.append(f"- Scenario evidence included: `{len(scenarios)}` scenario report(s).")
    lines.append("")
    return lines


def _remaining_warnings(dossier: dict[str, Any]) -> list[str]:
    warnings = dossier.get("unresolved_warnings_by_subsystem", {})
    lines = ["## Remaining Warnings", ""]
    if not warnings:
        lines.extend(["No unresolved warnings are listed in the dossier.", ""])
        return lines
    for subsystem, items in warnings.items():
        lines.append(f"### {subsystem}")
        for item in items[:8]:
            lines.append(f"- {item}")
        if len(items) > 8:
            lines.append(f"- ...and {len(items) - 8} more")
        lines.append("")
    return lines


def _required_reviews(dossier: dict[str, Any]) -> list[str]:
    lines = ["## Required Professional Reviews", ""]
    reviews = dossier.get("required_professional_reviews", [])
    if not reviews:
        lines.extend(["No required professional reviews are listed in the dossier.", ""])
        return lines
    for review in reviews:
        lines.append(f"- **{review.get('title', review.get('id'))}**: {review.get('reviewer', 'reviewer TBD')} ({review.get('reason', 'required')})")
    lines.append("")
    return lines


def _review_evidence(review_status: dict[str, Any]) -> list[str]:
    lines = ["## Missing Or Rejected Review Evidence", ""]
    missing = review_status.get("required_reviews_missing", [])
    rejected = review_status.get("expired_or_rejected_evidence", [])
    covered = review_status.get("required_reviews_covered", [])
    if covered:
        lines.append("Covered required reviews:")
        for item in covered:
            lines.append(f"- {item}")
        lines.append("")
    if missing:
        lines.append("Missing required reviews:")
        for item in missing:
            lines.append(f"- {item}")
        lines.append("")
    if rejected:
        lines.append("Expired or rejected evidence:")
        for item in rejected:
            lines.append(f"- {item}")
        lines.append("")
    unresolved = review_status.get("unresolved_issues_by_domain", {})
    if unresolved:
        lines.append("Unresolved issues:")
        for domain, issues in unresolved.items():
            lines.append(f"- {domain}: {len(issues)} issue(s)")
        lines.append("")
    return lines


def _go_no_go(dossier: dict[str, Any], review_status: dict[str, Any]) -> list[str]:
    updates = review_status.get("go_no_go_updates") or []
    checklist = updates if updates else dossier.get("go_no_go_checklist", [])
    lines = ["## Go/No-Go Checklist", ""]
    for item in checklist:
        status = item.get("updated_status", item.get("status", "unknown"))
        lines.append(f"- `{status}`: {item.get('item')} ({item.get('evidence', 'no evidence')})")
    lines.append("")
    return lines


def _must_never_infer(dossier: dict[str, Any]) -> list[str]:
    lines = ["## Must Never Be Inferred", ""]
    for item in dossier.get("must_never_be_inferred", []):
        lines.append(f"- {item}")
    lines.append("")
    return lines


def _next_actions(audit_report: dict[str, Any], dossier: dict[str, Any], review_status: dict[str, Any]) -> list[str]:
    actions = [
        "Assign owners for each unresolved warning and review domain.",
        "Replace placeholder review-register entries with real artifacts or explicit rejections.",
        "Resolve missing, rejected, and unresolved review evidence before any pilot-facing claim.",
        "Rerun `ciac review` and regenerate this packet after each evidence update.",
    ]
    if audit_report.get("promotion_decision") == "revise_before_pilot":
        actions.insert(0, "Do not treat `revise_before_pilot` as approval; complete the dossier workflow first.")
    if dossier.get("readiness_status") != "candidate_for_external_review":
        actions.append("Do not proceed to external pilot recruitment or site work from this packet.")
    if review_status.get("status") != "ready_for_review_update":
        actions.append("Focus next work on review evidence rather than visual/Unreal demonstration.")
    lines = ["## Next Actions", ""]
    lines.extend(f"- {item}" for item in actions)
    lines.append("")
    return lines
