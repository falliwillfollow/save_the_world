from __future__ import annotations

from pathlib import Path
from typing import Any

from .io import write_json
from .validation import validate_data


ALLOWED_AUTOMATION_DOMAINS = [
    "scheduling",
    "monitoring",
    "inventory",
    "route_planning",
    "routine_inspection",
    "task_reminders",
    "scenario_testing",
    "hidden_burden_detection",
    "logistics_support",
    "maintenance_queueing",
]

BLOCKED_AUTOMATION_DOMAINS = [
    "resident_consent",
    "expulsion_or_loss_of_access",
    "clinical_diagnosis",
    "legal_judgment",
    "punishment",
    "emotional_coercion",
    "private_life_inference",
    "governance_legitimacy",
    "determining_human_worth",
]

BLOCKED_AUTOMATION_TASKS = [
    "decide_expulsion_or_loss_of_access",
    "diagnose_resident_health",
    "determine_legal_validity",
    "determine_human_worth_or_contribution_value",
    "override_resident_consent",
    "infer_private_life_or_social_status_without_consent",
    "punish_or_rank_residents",
    "make_final_governance_decision",
]


def build_automation_manifest(
    runtime_bundle: dict[str, Any],
    world_manifest: dict[str, Any] | None = None,
    *,
    runtime_bundle_path: str | None = None,
    world_manifest_path: str | None = None,
) -> dict[str, Any]:
    residents = _world_residents(world_manifest) or _runtime_population(runtime_bundle) or 80
    tasks = default_automation_tasks(runtime_bundle, world_manifest)
    warnings = validate_no_blocked_automation_tasks(tasks)
    return {
        "kind": "AutomationManifest",
        "version": "v0",
        "manifest_id": f"automation_manifest_{residents}_v0",
        "source": {
            "runtime_bundle_path": runtime_bundle_path,
            "world_manifest_path": world_manifest_path,
            "generated_at": None,
            "provisional": True,
        },
        "automation_thesis": {
            "tagline": "Machines handle the repeating burden. Humans keep the non-repeatable life.",
            "description": (
                "Automation in CIaC is treated as a review-gated coordination substrate. It may schedule, monitor, "
                "summarize, queue, remind, and test scenarios, but it may not decide resident worth, rights, consent, "
                "legal validity, diagnosis, punishment, or governance legitimacy."
            ),
        },
        "allowed_automation_domains": ALLOWED_AUTOMATION_DOMAINS,
        "blocked_automation_domains": BLOCKED_AUTOMATION_DOMAINS,
        "blocked_automation_tasks": BLOCKED_AUTOMATION_TASKS,
        "tasks": tasks,
        "human_sovereignty_boundaries": [
            {
                "id": "no_automated_expulsion",
                "rule": "Automation may flag a governance issue, but may not remove housing or access rights.",
            },
            {
                "id": "no_automated_consent",
                "rule": "Automation may request review, but may not infer or override resident consent.",
            },
            {
                "id": "no_clinical_or_legal_finality",
                "rule": "Automation may prepare evidence summaries, but may not diagnose or determine legal validity.",
            },
            {
                "id": "no_private_life_inference",
                "rule": "Automation may use archetypal public stories, but may not infer private life or social status without consent.",
            },
        ],
        "review_gates": _review_gates(runtime_bundle),
        "warnings": [
            {
                "id": "provisional_automation",
                "message": "Automation tasks are design contracts and require privacy, safety, labor, and governance review before real deployment.",
                "severity": "info",
            },
            *warnings,
        ],
    }


def default_automation_tasks(runtime_bundle: dict[str, Any], world_manifest: dict[str, Any] | None = None) -> list[dict[str, Any]]:
    return [
        _task(
            "water_quality_check_schedule",
            "water",
            "AI_scheduler",
            "weekly",
            ["water_public_health_protocol", "water_reserve_status", "testing_calendar"],
            "water_testing_task",
            "public_health",
            "member_visible",
            "missed testing interval or stale reserve status",
        ),
        _task(
            "food_inventory_balance",
            "food",
            "AI_scheduler",
            "daily",
            ["food_inventory", "meal_demand_forecast", "dietary_constraints_summary"],
            "food_inventory_warning",
            "food_safety",
            "role_limited",
            "inventory recommendation hides shortage or dietary risk",
        ),
        _task(
            "care_meal_route",
            "care_health",
            "human_reviewed_AI",
            "care_meal_request",
            ["care_meal_requests", "accessible_route_status", "privacy_limited_delivery_window"],
            "delivery_schedule",
            "privacy",
            "role_limited",
            "route exposes private health or care information",
        ),
        _task(
            "maintenance_queue_prioritization",
            "maintenance_repair",
            "AI_scheduler",
            "work_order_created",
            ["work_orders", "asset_criticality", "safety_flags"],
            "prioritized_work_queue",
            "safety",
            "member_visible",
            "priority queue defers safety-critical repair",
        ),
        _task(
            "hidden_labor_detection",
            "labor_time",
            "human_reviewed_AI",
            "weekly",
            ["labor_ledger", "anonymous_time_burden_reports", "role_rotation_schedule"],
            "labor_burden_warning",
            "labor_fairness",
            "anonymized_or_role_limited",
            "hidden labor pattern is missed or privacy is overexposed",
        ),
        _task(
            "scenario_stress_test",
            "risk_resilience",
            "AI_simulation_runner",
            "manual_or_scheduled",
            ["runtime_bundle", "scenario_library", "resource_telemetry"],
            "scenario_report",
            "resilience_review",
            "member_visible",
            "scenario confidence is overstated",
        ),
        _task(
            "resident_story_projection",
            "social_cultural",
            "AI_narrative_compiler",
            "manifest_generation",
            ["life_manifest", "public_archetype_library", "provisionality_statement"],
            "archetype_story",
            "public_demo_review",
            "public_archetype_only",
            "story is mistaken for a real resident profile",
        ),
        _task(
            "sanitation_hygiene_round_schedule",
            "sanitation",
            "AI_scheduler",
            "daily",
            ["sanitation_protocol", "ppe_station_status", "cleaning_schedule"],
            "sanitation_round_task",
            "worker_safety",
            "member_visible",
            "dirty labor is hidden or worker safety review is skipped",
        ),
    ]


def validate_no_blocked_automation_tasks(tasks: list[dict[str, Any]]) -> list[dict[str, str]]:
    warnings: list[dict[str, str]] = []
    blocked_tokens = [item.replace("_", " ") for item in [*BLOCKED_AUTOMATION_DOMAINS, *BLOCKED_AUTOMATION_TASKS]]
    for task in tasks:
        searchable = " ".join(
            str(task.get(field, "")).replace("_", " ")
            for field in ("id", "domain", "output")
        ).lower()
        for token in blocked_tokens:
            if token.lower() in searchable:
                warnings.append(
                    {
                        "id": f"blocked_automation_overlap_{task.get('id', 'unknown')}",
                        "message": f"Automation task appears to overlap a blocked domain: {token}",
                        "severity": "block",
                    }
                )
    return warnings


def write_automation_manifest(manifest: dict[str, Any], path: str | Path) -> None:
    report = validate_data(manifest, str(path))
    if not report.ok:
        details = "; ".join(f"{issue.path}: {issue.message}" for issue in report.issues)
        raise ValueError(f"Invalid automation manifest: {details}")
    write_json(path, manifest)


def _task(
    task_id: str,
    domain: str,
    actor: str,
    trigger: str,
    input_data: list[str],
    output: str,
    review_gate: str,
    privacy_level: str,
    failure_mode: str,
) -> dict[str, Any]:
    return {
        "id": task_id,
        "domain": domain,
        "actor": actor,
        "trigger": trigger,
        "input_data": input_data,
        "output": output,
        "human_review_required": True,
        "review_gate": review_gate,
        "privacy_level": privacy_level,
        "failure_mode": failure_mode,
        "visible_in_world": True,
    }


def _review_gates(runtime_bundle: dict[str, Any]) -> list[dict[str, Any]]:
    policy_gate = runtime_bundle.get("capabilities", {}).get("policy_gate", {})
    gates = [
        {"id": "clinical_boundary_review", "domain": "care_health", "required_for": ["medication_continuity", "care_plan_suggestions"]},
        {"id": "privacy_review", "domain": "labor_time", "required_for": ["hidden_labor_detection", "care_meal_route"]},
        {"id": "public_health_review", "domain": "water", "required_for": ["water_quality_check_schedule", "sanitation_hygiene_round_schedule"]},
        {"id": "governance_review", "domain": "governance_anticapture", "required_for": ["automation_policy_changes"]},
    ]
    for domain, status in policy_gate.get("domain_statuses", {}).items():
        blockers = status.get("external_review_blockers", [])
        if blockers:
            gates.append({"id": f"{domain}_external_review", "domain": domain, "required_for": blockers})
    return gates


def _world_residents(world_manifest: dict[str, Any] | None) -> int | None:
    if not world_manifest:
        return None
    return world_manifest.get("population", {}).get("residents")


def _runtime_population(runtime_bundle: dict[str, Any]) -> int | None:
    for path in (("site", "population"), ("summary", "population"), ("manifest", "population"), ("capabilities", "state", "population")):
        cursor: Any = runtime_bundle
        for key in path:
            cursor = cursor.get(key, {}) if isinstance(cursor, dict) else {}
        if isinstance(cursor, int):
            return cursor
    return None
