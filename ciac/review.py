from __future__ import annotations

from datetime import date
from typing import Any


COVERING_STATUSES = {"submitted", "reviewed", "accepted"}
IN_PROGRESS_STATUSES = {"planned", "submitted", "reviewed"}


def evaluate_review_status(dossier: dict[str, Any], register: dict[str, Any]) -> dict[str, Any]:
    required_ids = [review["id"] for review in dossier.get("required_professional_reviews", []) if review.get("required")]
    reviews_by_domain = {review["domain"]: review for review in register.get("reviews", [])}
    covered = sorted(domain for domain in required_ids if _is_covered(reviews_by_domain.get(domain)))
    missing = sorted(domain for domain in required_ids if domain not in covered)
    expired_or_rejected = _expired_or_rejected(reviews_by_domain)
    unresolved = _unresolved_issues(reviews_by_domain)
    go_no_go = _go_no_go_updates(dossier, covered, missing, expired_or_rejected)
    status = _status(required_ids, covered, expired_or_rejected)

    return {
        "kind": "ReviewStatusReport",
        "id": f"{dossier['id']}_{register['id']}_review_status",
        "dossier": dossier["id"],
        "review_register": register["id"],
        "generated_by": "ciac.review.v0",
        "provisional": True,
        "status": status,
        "required_reviews_covered": covered,
        "required_reviews_missing": missing,
        "review_status_by_domain": {
            domain: _review_summary(review)
            for domain, review in sorted(reviews_by_domain.items())
        },
        "expired_or_rejected_evidence": expired_or_rejected,
        "unresolved_issues_by_domain": unresolved,
        "go_no_go_updates": go_no_go,
        "readiness_delta": _readiness_delta(dossier, status, missing, expired_or_rejected),
        "unknowns": [
            "Review status tracks artifacts; it does not validate professional credentials or conclusions.",
            "Accepted evidence means the register marks it accepted, not that CIaC has verified it.",
            "Missing, expired, rejected, or unresolved review issues should block pilot readiness discussions.",
        ],
    }


def _is_covered(review: dict[str, Any] | None) -> bool:
    return bool(review and review.get("status") in COVERING_STATUSES and review.get("status") != "rejected")


def _review_summary(review: dict[str, Any]) -> dict[str, Any]:
    return {
        "status": review["status"],
        "reviewer_name": review["reviewer_name"],
        "reviewer_org": review["reviewer_org"],
        "credential_type": review["credential_type"],
        "artifact_reference": review["artifact_reference"],
        "expiration_date": review["expiration_date"],
        "unresolved_issue_count": len(review["unresolved_issues"]),
    }


def _expired_or_rejected(reviews_by_domain: dict[str, dict[str, Any]]) -> list[str]:
    today = date.today().isoformat()
    issues: list[str] = []
    for domain, review in sorted(reviews_by_domain.items()):
        if review["status"] == "rejected":
            issues.append(f"{domain}:rejected")
        expiration = review.get("expiration_date", "")
        if expiration and expiration < today:
            issues.append(f"{domain}:expired:{expiration}")
    return issues


def _unresolved_issues(reviews_by_domain: dict[str, dict[str, Any]]) -> dict[str, list[str]]:
    return {
        domain: review["unresolved_issues"]
        for domain, review in sorted(reviews_by_domain.items())
        if review.get("unresolved_issues")
    }


def _go_no_go_updates(
    dossier: dict[str, Any],
    covered: list[str],
    missing: list[str],
    expired_or_rejected: list[str],
) -> list[dict[str, Any]]:
    updates = []
    for item in dossier.get("go_no_go_checklist", []):
        updated_status = item["status"]
        evidence = item["evidence"]
        if item["item"] == "Professional reviews are complete.":
            updated_status = "pass" if not missing and not expired_or_rejected else "fail"
            evidence = f"{len(covered)} review(s) covered; {len(missing)} missing; {len(expired_or_rejected)} expired/rejected."
        updates.append(
            {
                "item": item["item"],
                "original_status": item["status"],
                "updated_status": updated_status,
                "evidence": evidence,
            }
        )
    return updates


def _readiness_delta(
    dossier: dict[str, Any],
    status: str,
    missing: list[str],
    expired_or_rejected: list[str],
) -> dict[str, Any]:
    before = dossier.get("readiness_status", "not_ready")
    after = before
    if status == "ready_for_review_update" and before == "review_package_needed":
        after = "candidate_for_external_review"
    return {
        "before": before,
        "after": after,
        "covered_missing_count": len(missing),
        "expired_or_rejected_count": len(expired_or_rejected),
    }


def _status(required_ids: list[str], covered: list[str], expired_or_rejected: list[str]) -> str:
    if expired_or_rejected or not covered:
        return "missing_evidence"
    if len(covered) < len(required_ids):
        return "in_progress"
    return "ready_for_review_update"

