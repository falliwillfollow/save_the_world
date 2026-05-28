from __future__ import annotations

from pathlib import Path
from typing import Any

from .io import write_json
from .validation import validate_data
from .world_manifest import infer_scale


PROVISIONALITY_STATEMENT = (
    "This is a provisional civic simulation. It visualizes model assumptions and stress tests. It does not certify "
    "real-world safety, legality, affordability, engineering, public health, accessibility, resident consent, or buildability."
)

BASELINE_PROFILE = {
    "id": "default_renter_creator",
    "label": "Default renter creator baseline",
    "weekly_hours": {
        "wage_hours": 42.0,
        "commute_hours": 6.0,
        "errands_admin": 5.0,
        "domestic_survival": 12.0,
        "required_care": 2.0,
        "recovery": 7.0,
        "passion_time": 4.0,
    },
    "anxiety_sources": [
        "rent insecurity",
        "unplanned maintenance costs",
        "food price volatility",
        "health interruption risk",
        "transport dependency",
        "errand and supply-chain burden",
    ],
}

ARCHETYPES = [
    ("resident_artist_01", "Artist", "creator"),
    ("resident_elder_02", "Elder", "elder"),
    ("resident_caregiver_03", "Caregiver", "caregiver"),
    ("resident_student_04", "Student", "student"),
    ("resident_maintenance_steward_05", "Maintenance steward", "steward"),
]


def build_life_manifest(
    runtime_bundle: dict[str, Any],
    world_manifest: dict[str, Any] | None = None,
    *,
    population: int | None = None,
    baseline_profile: str = "default_renter_creator",
    runtime_bundle_path: str | None = None,
    world_manifest_path: str | None = None,
) -> dict[str, Any]:
    residents = int(population or _world_residents(world_manifest) or _runtime_population(runtime_bundle) or 80)
    scale = world_manifest.get("scale") if world_manifest else infer_scale(residents)
    policy_gate = runtime_bundle.get("capabilities", {}).get("policy_gate", {})
    capability_state = runtime_bundle.get("capabilities", {}).get("state", {})
    labor_state = capability_state.get("domains", {}).get("labor_time", capability_state.get("labor_time", {}))
    commons_labor = float(labor_state.get("commons_labor_hours_per_resident_per_week", 6.0))
    hidden_labor_status = "pass" if labor_state.get("hidden_labor_tracking_supported") else "warn"
    capability_gate_status = str(policy_gate.get("status") or _capability_status(runtime_bundle))
    archetypes = default_resident_archetypes(residents)
    for archetype in archetypes:
        baseline_life = build_baseline_life(archetype["archetype"], baseline_profile)
        civic_floor_life = build_civic_floor_life(archetype["archetype"], runtime_bundle, world_manifest)
        life_returned = compute_life_returned(baseline_life, civic_floor_life)
        archetype.update(
            {
                "baseline_life": baseline_life,
                "civic_floor_life": civic_floor_life,
                "life_returned": life_returned,
                "narrative_beats": _narrative_beats(archetype, life_returned),
                "warnings": ["Archetype is public and synthetic; it is not a resident profile."],
            }
        )

    average_life_returned = round(sum(item["life_returned"]["hours_per_week"] for item in archetypes) / len(archetypes), 3)
    average_free_time = round(sum(item["life_returned"]["free_time_increase_hours_per_week"] for item in archetypes) / len(archetypes), 3)
    average_passion = round(sum(item["life_returned"]["passion_time_increase_hours_per_week"] for item in archetypes) / len(archetypes), 3)
    average_scarcity_wage = round(sum(item["baseline_life"]["weekly_hours"]["wage_hours"] for item in archetypes) / len(archetypes), 3)

    return {
        "kind": "LifeManifest",
        "version": "v0",
        "manifest_id": f"life_manifest_{residents}_v0",
        "source": {
            "runtime_bundle_path": runtime_bundle_path,
            "world_manifest_path": world_manifest_path,
            "capability_policy_id": policy_gate.get("policy_id"),
            "generated_at": None,
            "provisional": True,
        },
        "population": {
            "residents": residents,
            "households": world_manifest.get("population", {}).get("households") if world_manifest else None,
        },
        "scale": {
            "scale_class": scale.get("scale_class", "village_block"),
            "active_layers": scale.get("active_layers", []),
            "implied_village_blocks": scale.get("implied_village_blocks", 1),
        },
        "public_thesis": {
            "tagline": "Infrastructure should return life, not merely optimize scarcity.",
            "short": "The civic floor translates shared systems into visible reductions in compulsory burden without treating commute and errands as civic-floor defaults.",
            "long": (
                "CIaC models housing, food, water, energy, sanitation, care, mobility, governance, and labor visibility as "
                "a coordinated substrate for post-labor abundance. This manifest shows the human-facing promise in cautious, "
                "reviewable terms: no required external wage burden inside the model, no rent pressure, fewer hidden chores, structurally absent commute and errand burden, "
                "more protected recovery, and more meaningful time."
            ),
        },
        "metrics": {
            "life_returned_hours_per_week": average_life_returned,
            "required_wage_hours_reduction_percent": 100.0,
            "scarcity_reference_wage_hours_per_week": average_scarcity_wage,
            "civic_floor_external_wage_hours_per_week": 0.0,
            "capability_policy_wage_reduction_signal_percent": float(labor_state.get("required_wage_hours_reduction_percent", 0.0)),
            "free_time_increase_hours_per_week": average_free_time,
            "passion_time_increase_hours_per_week": average_passion,
            "commons_labor_hours_per_resident_per_week": commons_labor,
            "hidden_labor_status": hidden_labor_status,
            "capability_gate_status": capability_gate_status if capability_gate_status in {"pass", "warn", "fail", "promotion_blocked"} else "unknown",
        },
        "resident_archetypes": archetypes,
        "baseline_model": {
            "description": "A conventional scarcity baseline with wage dependence, transport dependency, fragmented errands, and private household survival work.",
            "profile_id": baseline_profile,
            "assumptions": [
                "The baseline is illustrative and should be replaced with local survey data before planning decisions.",
                "Weekly hours are rounded and intentionally low precision.",
                "The model treats time returned as a signal for review, not as proof of real-world wellbeing.",
            ],
            "conventional_life_burdens": [
                "rent pressure",
                "commute dependency",
                "duplicated private domestic work",
                "food procurement and preparation volatility",
                "transport dependency",
                "manual errand burden",
                "maintenance uncertainty",
            ],
        },
        "civic_floor_model": {
            "description": "A civic floor with shared capability layers, visible commons labor, local walkable life, delivered goods, and review-gated automation support.",
            "support_systems": _support_systems(runtime_bundle, world_manifest),
            "automation_assists": [
                "water quality check scheduling",
                "food inventory balancing",
                "goods delivery coordination",
                "maintenance queueing",
                "hidden labor detection",
                "scenario stress testing",
            ],
            "human_sovereignty_boundaries": [
                "resident consent",
                "housing and access rights",
                "clinical diagnosis",
                "legal judgment",
                "governance legitimacy",
                "private life inference",
                "creative purpose",
            ],
        },
        "life_returned": {
            "summary": "Average weekly hours shifted from wage/rent scarcity burden into recovery, learning, care, art, friendship, and invention.",
            "hours_per_week": average_life_returned,
            "meaningful_uses": ["art", "study", "care", "rest", "nature", "invention", "friendship"],
            "confidence": "provisional",
            "assumptions": [
                "The estimate compares a conventional scarcity reference life with a civic-floor abundance hypothesis.",
                "Required external wage work is zero inside the civic-floor hypothesis.",
                "Rent pressure is not modeled as a resident burden inside the civic-floor hypothesis.",
                "Commons labor is visible and counted as compulsory civic burden.",
                "Commute and errands are modeled as structurally absent civic-floor burdens, not as optimized modern obligations.",
                "Automation assists reduce coordination burden only after human review gates are satisfied.",
            ],
        },
        "scenes": [
            {
                "id": "normal_day",
                "title": "Normal Day",
                "mode": "life",
                "beats": build_story_beats(archetypes, runtime_bundle),
            }
        ],
        "scenario_story_beats": _scenario_story_beats(runtime_bundle),
        "warnings": _warnings(runtime_bundle),
        "promotion_blockers": _promotion_blockers(policy_gate),
        "provisionality": {
            "statement": PROVISIONALITY_STATEMENT,
            "external_reviews_required": [
                "public health",
                "building and fire code",
                "accessibility",
                "labor and employment",
                "privacy and consent",
                "local governance",
            ],
        },
    }


def default_resident_archetypes(population: int) -> list[dict[str, Any]]:
    return [
        {
            "id": resident_id,
            "label": label,
            "archetype": archetype,
            "population_share": round(1 / max(1, min(population, len(ARCHETYPES))), 3),
        }
        for resident_id, label, archetype in ARCHETYPES
    ]


def build_baseline_life(archetype: str, baseline_profile: str) -> dict[str, Any]:
    hours = dict(BASELINE_PROFILE["weekly_hours"])
    if archetype == "caregiver":
        hours["required_care"] += 5.0
        hours["passion_time"] -= 1.0
    if archetype == "elder":
        hours["wage_hours"] = 18.0
        hours["required_care"] += 4.0
        hours["recovery"] += 3.0
    if archetype == "student":
        hours["wage_hours"] = 28.0
        hours["errands_admin"] += 2.0
        hours["passion_time"] += 3.0
    if archetype == "steward":
        hours["wage_hours"] = 36.0
        hours["domestic_survival"] += 2.0
    return {
        "profile_id": baseline_profile,
        "weekly_hours": _round_hours(hours),
        "anxiety_sources": BASELINE_PROFILE["anxiety_sources"],
        "description": "Conventional scarcity-reference life budget before civic-floor support.",
    }


def build_civic_floor_life(
    archetype: str,
    runtime_bundle: dict[str, Any],
    world_manifest: dict[str, Any] | None,
) -> dict[str, Any]:
    capability_state = runtime_bundle.get("capabilities", {}).get("state", {})
    labor_state = capability_state.get("domains", {}).get("labor_time", capability_state.get("labor_time", {}))
    commons_labor = float(labor_state.get("commons_labor_hours_per_resident_per_week", 6.0))
    baseline = build_baseline_life(archetype, "default_renter_creator")["weekly_hours"]
    hours = {
        "wage_hours": 0.0,
        "commons_labor": commons_labor,
        "commute_hours": 0.0,
        "errands_admin": 0.0,
        "domestic_survival": max(2.0, baseline["domestic_survival"] - 9.0),
        "required_care": max(0.5, baseline["required_care"] - 1.0),
        "recovery": baseline["recovery"],
        "passion_time": baseline["passion_time"],
    }
    if archetype == "elder":
        hours["required_care"] = max(1.0, baseline["required_care"] - 3.0)
    if archetype == "steward":
        hours["commons_labor"] += 1.0
    baseline_compulsory = _compulsory_burden(baseline)
    civic_compulsory = (
        hours["wage_hours"]
        + hours["commons_labor"]
        + hours["commute_hours"]
        + hours["errands_admin"]
        + hours["domestic_survival"]
        + hours["required_care"]
    )
    reclaimed = max(0.0, baseline_compulsory - civic_compulsory)
    recovery_share = 0.4
    if archetype == "elder":
        recovery_share = 0.55
    if archetype == "student":
        recovery_share = 0.3
    passion_share = 1.0 - recovery_share
    hours["recovery"] += reclaimed * recovery_share
    hours["passion_time"] += reclaimed * passion_share
    return {
        "weekly_hours": _round_hours(hours),
        "support_locations": _support_locations(world_manifest),
        "description": "Civic-floor abundance budget with visible commons labor, no required external wage work, no rent pressure, no required commute, no manual errand burden, and shared support systems.",
        "reclaimed_time_allocation": {
            "source": "scarcity_burden_removed",
            "hours_per_week": round(reclaimed, 3),
            "recovery_share": round(recovery_share, 3),
            "passion_share": round(passion_share, 3),
        },
        "automation_handled_burdens": [
            "goods delivery coordination",
            "inventory balancing",
            "routine supply checks",
            "maintenance queueing",
        ],
        "structurally_absent_burdens": [
            "required commute",
            "routine consumer errands",
            "rent payment pressure",
            "required external wage job",
        ],
    }


def compute_life_returned(
    baseline_life: dict[str, Any],
    civic_floor_life: dict[str, Any],
) -> dict[str, Any]:
    baseline = baseline_life["weekly_hours"]
    civic = civic_floor_life["weekly_hours"]
    baseline_compulsory = _compulsory_burden(baseline)
    civic_compulsory = (
        civic["wage_hours"]
        + civic["commons_labor"]
        + civic["commute_hours"]
        + civic["errands_admin"]
        + civic["domestic_survival"]
        + civic["required_care"]
    )
    wage_reduction = 0.0
    if baseline["wage_hours"]:
        wage_reduction = ((baseline["wage_hours"] - civic["wage_hours"]) / baseline["wage_hours"]) * 100.0
    return {
        "hours_per_week": round(baseline_compulsory - civic_compulsory, 3),
        "compulsory_burden_baseline_hours": round(baseline_compulsory, 3),
        "compulsory_burden_civic_hours": round(civic_compulsory, 3),
        "required_wage_hours_reduction_percent": round(wage_reduction, 3),
        "free_time_increase_hours_per_week": round((civic["recovery"] + civic["passion_time"]) - (baseline["recovery"] + baseline["passion_time"]), 3),
        "passion_time_increase_hours_per_week": round(civic["passion_time"] - baseline["passion_time"], 3),
        "confidence": "hypothesis",
        "assumptions": [
                "The baseline is an outside scarcity reference, not an assumption about residents in the civic-floor world.",
                "Civic-floor residents do not have required jobs, rent payments, commutes, or routine errands in this hypothesis.",
                "Commons labor is included in civic compulsory burden.",
                "Commute and errands are modeled as absent from civic-floor burden because the design intent is local walkable life plus automation-supported logistics.",
            ],
    }


def build_story_beats(
    resident_archetypes: list[dict[str, Any]],
    runtime_bundle: dict[str, Any],
) -> list[dict[str, Any]]:
    return [
        beat
        for archetype in resident_archetypes
        for beat in archetype.get("narrative_beats", [])
    ][:8]


def write_life_manifest(manifest: dict[str, Any], path: str | Path) -> None:
    report = validate_data(manifest, str(path))
    if not report.ok:
        details = "; ".join(f"{issue.path}: {issue.message}" for issue in report.issues)
        raise ValueError(f"Invalid life manifest: {details}")
    write_json(path, manifest)


def _world_residents(world_manifest: dict[str, Any] | None) -> int | None:
    if not world_manifest:
        return None
    return world_manifest.get("population", {}).get("residents")


def _runtime_population(runtime_bundle: dict[str, Any]) -> int | None:
    for path in (
        ("site", "population"),
        ("summary", "population"),
        ("manifest", "population"),
        ("capabilities", "state", "population"),
    ):
        cursor: Any = runtime_bundle
        for key in path:
            cursor = cursor.get(key, {}) if isinstance(cursor, dict) else {}
        if isinstance(cursor, int):
            return cursor
    return None


def _capability_status(runtime_bundle: dict[str, Any]) -> str:
    statuses = [domain.get("status") for domain in runtime_bundle.get("capabilities", {}).get("domain_statuses", {}).values()]
    if any(status == "fail" for status in statuses):
        return "fail"
    if any(status == "warn" for status in statuses):
        return "warn"
    if statuses and all(status == "pass" for status in statuses):
        return "pass"
    return "unknown"


def _round_hours(hours: dict[str, float]) -> dict[str, float]:
    return {key: round(float(value), 3) for key, value in hours.items()}


def _compulsory_burden(hours: dict[str, float]) -> float:
    return (
        float(hours.get("wage_hours", 0.0))
        + float(hours.get("commute_hours", 0.0))
        + float(hours.get("errands_admin", 0.0))
        + float(hours.get("domestic_survival", 0.0))
        + float(hours.get("required_care", 0.0))
    )


def _support_locations(world_manifest: dict[str, Any] | None) -> list[str]:
    if not world_manifest:
        return []
    return [
        item["id"]
        for item in [*world_manifest.get("structures", []), *world_manifest.get("infrastructure_nodes", [])]
        if item.get("id")
    ][:8]


def _support_systems(runtime_bundle: dict[str, Any], world_manifest: dict[str, Any] | None) -> list[str]:
    systems = [_title(system.get("pattern_id", "")) for system in runtime_bundle.get("systems", []) if system.get("pattern_id")]
    if systems:
        return systems[:12]
    if world_manifest:
        return [_title(module.get("pattern_id", "")) for module in world_manifest.get("modules", [])][:12]
    return []


def _scenario_story_beats(runtime_bundle: dict[str, Any]) -> list[dict[str, Any]]:
    beats = []
    for index, scenario in enumerate(runtime_bundle.get("scenarios", [])[:5], start=1):
        beats.append(
            {
                "id": f"scenario_{index}",
                "scenario_id": scenario.get("scenario_id") or scenario.get("id") or f"scenario_{index}",
                "title": scenario.get("label") or scenario.get("scenario_id") or "Stress scenario",
                "beats": [
                    {
                        "time": "during",
                        "subject": "community",
                        "text": "Scenario stress is translated into a visible support and recovery beat.",
                        "location_id": "structure_common_house",
                    }
                ],
            }
        )
    return beats


def _warnings(runtime_bundle: dict[str, Any]) -> list[dict[str, str]]:
    warnings = [
        {"id": "provisionality", "message": PROVISIONALITY_STATEMENT, "severity": "info"},
    ]
    for index, message in enumerate(runtime_bundle.get("manifest", {}).get("warnings", [])[:8], start=1):
        warnings.append({"id": f"runtime_warning_{index}", "message": str(message), "severity": "warn"})
    return warnings


def _promotion_blockers(policy_gate: dict[str, Any]) -> list[dict[str, str]]:
    blockers = []
    for index, blocker in enumerate(policy_gate.get("promotion_blockers", []), start=1):
        if isinstance(blocker, dict):
            blockers.append(
                {
                    "id": str(blocker.get("id") or f"promotion_blocker_{index}"),
                    "domain": str(blocker.get("domain") or "unknown"),
                    "message": str(blocker.get("message") or blocker),
                }
            )
        else:
            blockers.append({"id": f"promotion_blocker_{index}", "domain": "unknown", "message": str(blocker)})
    return blockers


def _narrative_beats(archetype: dict[str, Any], life_returned: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "time": "morning",
            "subject": archetype["label"],
            "text": f"{archetype['label']} begins the day with fewer compulsory tasks in queue.",
            "location_id": "structure_common_house",
        },
        {
            "time": "afternoon",
            "subject": archetype["label"],
            "text": f"{life_returned['hours_per_week']} weekly hours are modeled as shifted toward recovery, study, care, or creation.",
            "location_id": "structure_quiet_studio",
        },
    ]


def _title(value: str) -> str:
    return str(value).replace("_", " ").replace(".", " ").title()
