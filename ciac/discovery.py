from __future__ import annotations

import re
from typing import Any


DOMAIN_HINTS = {
    "care_health": {
        "keywords": ("medication", "care", "illness"),
        "objects": ("structure_care_room", "structure_common_house"),
        "modules": ("risk_resilience.graceful_degradation_engine.v0_1",),
        "scenario_ids": ("scenario_illness_wave", "water_contamination_response_v2"),
    },
    "governance_anticapture": {
        "keywords": ("due process", "emergency power", "governance", "capture"),
        "objects": ("node_risk_governance", "structure_common_house"),
        "modules": ("governance.commons_stewardship_protocol.v0_1",),
        "scenario_ids": ("scenario_financial_shock",),
    },
    "labor_time": {
        "keywords": ("hidden labor", "labor", "burden", "maintenance"),
        "objects": ("structure_maintenance_shop", "structure_quiet_studio"),
        "modules": ("labor_time.life_burden_ledger.v0_1", "maintenance.maintainable_commons_spine.v0_1"),
        "scenario_ids": ("crop_failure", "energy_outage_reserve_v2"),
    },
    "mobility_access": {
        "keywords": ("accessible-route", "mobility", "access", "route"),
        "objects": ("path_primary_ring", "path_daily_spine"),
        "modules": ("mobility_access.pedestrian_first_access_commons.v0_1",),
        "scenario_ids": ("scenario_illness_wave", "water_contamination_response_v2"),
    },
    "water_public_health": {
        "keywords": ("water", "public health", "contamination", "recovery review"),
        "objects": ("node_water_reserve", "structure_common_house"),
        "modules": ("water.resilient_water_commons.v0_1",),
        "scenario_ids": ("water_contamination_response_v2",),
    },
    "risk_resilience": {
        "keywords": ("risk mode", "response planning", "outage", "failure"),
        "objects": ("node_risk_governance", "structure_common_house"),
        "modules": ("risk_resilience.graceful_degradation_engine.v0_1",),
        "scenario_ids": ("crop_failure", "energy_outage_reserve_v2", "water_contamination_response_v2"),
    },
}


def build_discovery_loop(
    world_manifest: dict[str, Any],
    runtime_bundle: dict[str, Any] | None = None,
    focus: str | None = None,
    source_paths: dict[str, str | None] | None = None,
) -> dict[str, Any]:
    source_paths = source_paths or {}
    focus_domain = focus or _first_warning_domain(world_manifest, runtime_bundle) or "care_health"
    findings = _findings(world_manifest, runtime_bundle, focus_domain)
    retrieval_plan = [_retrieval_query(finding) for finding in findings]
    candidate_requests = [_candidate_request(finding) for finding in findings]
    seed_candidates = [candidate for finding in findings for candidate in _seed_candidates(world_manifest, finding)]
    status = "ready_for_generation" if findings else "no_findings"
    loop_id = f"discovery_{world_manifest.get('world_id', 'world')}_{focus_domain}_v0"
    return {
        "kind": "DiscoveryLoopReport",
        "version": "v0",
        "id": loop_id,
        "source": {
            "world_manifest_path": source_paths.get("world_manifest"),
            "runtime_bundle_path": source_paths.get("runtime_bundle"),
            "world_id": world_manifest.get("world_id"),
            "population": world_manifest.get("population", {}).get("residents"),
            "scale_class": world_manifest.get("scale", {}).get("scale_class"),
        },
        "focus": focus_domain,
        "status": status,
        "findings": findings,
        "retrieval_plan": retrieval_plan,
        "candidate_requests": candidate_requests,
        "seed_candidates": seed_candidates,
        "evaluation_contract": {
            "metrics_to_compare": [
                "resource_telemetry.resources.current_ratio",
                "resource_telemetry.resources.net_per_day",
                "resource_telemetry.labor.required_minutes_per_resident_per_day",
                "capabilities.domain_statuses",
                "scenario.total_unmet_delta",
                "scenario.blocked_review_domain_count",
            ],
            "scenarios_to_run": sorted({scenario for finding in findings for scenario in finding.get("scenario_ids", [])}),
            "hard_rejection_rules": [
                "Reject candidates that create new survival-critical unmet demand.",
                "Reject candidates that hide labor by moving it into untracked resident work.",
                "Reject candidates that lower privacy, consent, accessibility, or public-health visibility without an explicit mitigation.",
                "Reject candidates that require a professional license or legal authority but omit that dependency.",
            ],
            "output_schema": "schemas/discovery_candidate_intervention.schema.json",
        },
        "n8n_contract": _n8n_contract(),
        "next_actions": [
            "Run retrieval_plan queries against the local vector store.",
            "Ask Ollama to generate DiscoveryCandidateIntervention JSON only; reject prose-only answers.",
            "Validate each candidate with `py -3.10 -m ciac validate <candidate_dir>`.",
            "Run candidate simulation or pressure-test commands before promotion.",
            "Write accepted candidates to candidate_interventions/ with source_loop_id preserved.",
        ],
        "provisional": True,
    }


def _findings(world_manifest: dict[str, Any], runtime_bundle: dict[str, Any] | None, focus: str) -> list[dict[str, Any]]:
    warnings = list(world_manifest.get("warnings", []))
    if runtime_bundle:
        warnings.extend(runtime_bundle.get("capabilities", {}).get("warnings", []))
        for domain, status in runtime_bundle.get("capabilities", {}).get("domain_statuses", {}).items():
            for message in status.get("messages", []):
                warnings.append(f"{domain}: {message}")
    domains = [focus] if focus != "all" else list(DOMAIN_HINTS)
    findings = []
    for domain in domains:
        messages = _domain_messages(domain, warnings)
        overlay = world_manifest.get("overlays", {}).get(domain)
        if overlay and overlay.get("status") in {"warn", "warning", "fail", "failed"}:
            messages.append(overlay.get("summary", f"{domain} overlay is warning."))
        if not messages and focus != domain:
            continue
        if not messages:
            messages.append(f"{domain} selected for discovery; no explicit warning message was present.")
        findings.append(
            {
                "id": f"finding_{domain}",
                "domain": domain,
                "severity": _severity(messages),
                "summary": _summary(domain, messages),
                "evidence": sorted(set(messages)),
                "target_objects": _objects_for_domain(world_manifest, domain),
                "module_refs": list(DOMAIN_HINTS.get(domain, {}).get("modules", ())),
                "scenario_ids": list(DOMAIN_HINTS.get(domain, {}).get("scenario_ids", ())),
            }
        )
    return findings


def _seed_candidates(world_manifest: dict[str, Any], finding: dict[str, Any]) -> list[dict[str, Any]]:
    domain = finding["domain"]
    templates = _templates(domain)
    return [
        _candidate(world_manifest, finding, index, template)
        for index, template in enumerate(templates, start=1)
    ]


def _templates(domain: str) -> list[dict[str, Any]]:
    if domain == "care_health":
        return [
            {
                "title": "Resident-controlled medication continuity kit",
                "type": "operating_protocol",
                "hypothesis": "A resident-controlled medication continuity kit plus opt-in care-room backup tracking can close continuity gaps without centralizing private health data.",
                "effects": [("care_continuity_coverage", "increase"), ("hidden_labor_risk", "decrease"), ("privacy_exposure", "neutral")],
                "risks": [("Inventory drift or missed refills", "medium", "Use opt-in refill reminders and non-diagnostic inventory checks.")],
            },
            {
                "title": "Critical-load medication cold-chain cabinet",
                "type": "module_candidate",
                "hypothesis": "A small critical-load cold-chain cabinet can protect temperature-sensitive medication during outage and illness-wave scenarios.",
                "effects": [("critical_load_energy_draw", "increase"), ("medication_spoilage_risk", "decrease"), ("maintenance_burden", "increase")],
                "risks": [("Battery dependency concentrates continuity risk", "medium", "Add manual outage checklist and backup storage transfer protocol.")],
            },
            {
                "title": "Care steward continuity rota",
                "type": "operating_protocol",
                "hypothesis": "A backup care steward rota can make medication and high-need continuity visible while preventing a single role from becoming a hidden labor sink.",
                "effects": [("role_backup_coverage", "increase"), ("hidden_labor_tracking", "increase"), ("commons_labor_minutes", "increase")],
                "risks": [("Role may become coercive or privacy-invasive", "medium", "Use opt-in support boundaries and resident-controlled disclosure.")],
            },
        ]
    if domain == "governance_anticapture":
        return [
            {
                "title": "Emergency authority sunset rule",
                "type": "governance_rule",
                "hypothesis": "Every emergency authority should expire automatically unless renewed through a visible resident process.",
                "effects": [("capture_risk_score", "decrease"), ("decision_latency", "increase"), ("due_process_coverage", "increase")],
                "risks": [("Slow renewal could delay response", "medium", "Allow short renewal windows with published scope and appeal path.")],
            },
            {
                "title": "Due process appeal lane",
                "type": "governance_rule",
                "hypothesis": "A minimal appeal lane can reduce capture risk by giving residents notice, reply, and documented review for contested decisions.",
                "effects": [("due_process_coverage", "increase"), ("admin_labor", "increase"), ("resident_trust", "increase")],
                "risks": [("Administrative burden expands", "medium", "Use lightweight templates and time-boxed review.")],
            },
        ]
    if domain == "labor_time":
        return [
            {
                "title": "Hidden labor ledger extension",
                "type": "pattern_patch",
                "hypothesis": "Adding hidden labor categories to the life burden ledger can expose informal care, cleaning, coordination, and emotional labor before optimization hides it.",
                "effects": [("hidden_labor_visibility", "increase"), ("reported_labor_minutes", "increase"), ("burnout_risk_score", "decrease")],
                "risks": [("Tracking can feel surveillant", "medium", "Aggregate categories and avoid individual productivity scoring.")],
            },
            {
                "title": "Rotating task friction audit",
                "type": "operating_protocol",
                "hypothesis": "A periodic task-friction audit can identify invisible work before it becomes normalized obligation.",
                "effects": [("maintenance_feedback_quality", "increase"), ("admin_labor", "increase"), ("burnout_risk_score", "decrease")],
                "risks": [("Meetings become extra burden", "low", "Keep audits brief and attach them to existing commons check-ins.")],
            },
        ]
    if domain == "mobility_access":
        return [
            {
                "title": "Accessible route coverage map",
                "type": "pattern_patch",
                "hypothesis": "Every daily task route should declare grade, surface, rest points, lighting, and emergency access status so population scaling cannot hide access gaps.",
                "effects": [("accessible_route_coverage", "increase"), ("spatial_review_burden", "increase"), ("non_driver_access", "increase")],
                "risks": [("Proxy geometry may imply false compliance", "high", "Mark all route claims provisional until surveyed.")],
            }
        ]
    if domain == "water_public_health":
        return [
            {
                "title": "Water recovery test-and-release playbook",
                "type": "scenario_playbook",
                "hypothesis": "Water recovery can move from blocked to testable if source isolation, alternate supply, lab testing, and release authority are modeled explicitly.",
                "effects": [("blocked_review_domain_count", "decrease"), ("recovery_time", "increase"), ("public_health_visibility", "increase")],
                "risks": [("Testing authority may be unavailable during disruption", "high", "Model delivered water fallback and conservative no-release default.")],
            }
        ]
    if domain == "risk_resilience":
        return [
            {
                "title": "Cross-scenario failure response ledger",
                "type": "pattern_patch",
                "hypothesis": "A shared failure response ledger can keep outage, crop-failure, and contamination actions visible across scenarios instead of burying them in one-off playbooks.",
                "effects": [("scenario_coverage_count", "increase"), ("response_labor_visibility", "increase"), ("unknown_failure_modes", "decrease")],
                "risks": [("Response records may become administrative drag", "medium", "Keep entries scenario-scoped, time-boxed, and linked to concrete recovery decisions.")],
            },
            {
                "title": "Recovery threshold decision table",
                "type": "scenario_playbook",
                "hypothesis": "Explicit thresholds for conserve, isolate, substitute, repair, and external-handoff decisions can make stress recovery more repeatable without pretending the model certifies safety.",
                "effects": [("recovery_decision_latency", "decrease"), ("external_dependency_visibility", "increase"), ("scenario_coverage_count", "increase")],
                "risks": [("Thresholds may imply false precision", "medium", "Mark thresholds as provisional and require scenario replay plus local review before promotion.")],
            },
        ]
    return [
        {
            "title": f"{domain.replace('_', ' ').title()} response playbook",
            "type": "scenario_playbook",
            "hypothesis": f"An explicit {domain.replace('_', ' ')} response playbook can convert vague risk modes into testable scenario actions.",
            "effects": [("scenario_coverage_count", "increase"), ("recovery_labor", "increase"), ("unknown_failure_modes", "decrease")],
            "risks": [("Playbook may overfit current assumptions", "medium", "Run against multiple stress scenarios and preserve unknowns.")],
        }
    ]


def _candidate(world_manifest: dict[str, Any], finding: dict[str, Any], index: int, template: dict[str, Any]) -> dict[str, Any]:
    slug = _slug(template["title"])
    loop_id = f"discovery_{world_manifest.get('world_id', 'world')}_{finding['domain']}_v0"
    return {
        "kind": "DiscoveryCandidateIntervention",
        "version": "v0",
        "id": f"{finding['domain']}_{slug}_v0",
        "source_loop_id": loop_id,
        "focus_domain": finding["domain"],
        "title": template["title"],
        "hypothesis": template["hypothesis"],
        "intervention_type": template["type"],
        "target_objects": finding.get("target_objects", []),
        "module_refs": finding.get("module_refs", []),
        "assumptions": [
            {
                "id": f"assumption_{index}_local_fit",
                "statement": "Candidate is generated from CIaC warning context and must be checked against local law, safety, consent, and engineering constraints before promotion.",
                "confidence": "low",
                "needs_evidence": True,
            }
        ],
        "expected_effects": [
            {"metric": metric, "direction": direction, "rationale": f"Generated hypothesis expects {metric} to {direction}."}
            for metric, direction in template["effects"]
        ],
        "risk_tradeoffs": [
            {"risk": risk, "severity": severity, "mitigation": mitigation}
            for risk, severity, mitigation in template["risks"]
        ],
        "simulation_hooks": {
            "metrics_to_compare": [
                "resource_telemetry.labor.required_minutes_per_resident_per_day",
                "capabilities.domain_statuses",
                "scenario.blocked_review_domain_count",
            ],
            "scenarios_to_run": finding.get("scenario_ids", []),
            "acceptance_tests": [
                "No new survival-critical unmet demand is introduced.",
                "No labor is shifted into untracked resident burden.",
                "Privacy, consent, public-health, accessibility, and governance assumptions remain explicit.",
            ],
        },
        "rag_context": {
            "queries": [_query_for_domain(finding["domain"])],
            "required_sources": [
                "patterns/",
                "docs/module_reports/",
                "examples/generated/micro_commons_runtime_bundle.json",
                "examples/world_manifests/civic_floor_80_v0.world.json",
            ],
            "source_ids": [],
        },
        "status": "draft",
        "provisional": True,
    }


def _retrieval_query(finding: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": f"retrieve_{finding['domain']}",
        "domain": finding["domain"],
        "query": _query_for_domain(finding["domain"]),
        "required_context": [
            "relevant civic patterns and capability effects",
            "module reports and sprint plans",
            "runtime warnings and current telemetry",
            "scenario failure modes and recovery requirements",
        ],
    }


def _candidate_request(finding: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": f"generate_{finding['domain']}_candidates",
        "finding_id": finding["id"],
        "prompt": (
            "Generate 2-4 DiscoveryCandidateIntervention JSON objects for this finding. "
            "Do not certify safety. Compare labor, energy, privacy, public-health, accessibility, governance, "
            "scenario resilience, and new risks. Use only retrieved context plus explicit assumptions."
        ),
        "required_candidate_count": 3,
        "output_kind": "DiscoveryCandidateIntervention",
    }


def _n8n_contract() -> dict[str, Any]:
    return {
        "workflow": "n8n/workflow_specs/discovery_lab_pipeline.md",
        "local_model_provider": "Ollama",
        "rag_role": "Retrieve local CIaC context before candidate generation.",
        "required_nodes": [
            "Manual Trigger or Webhook",
            "Execute Command: ciac discovery-loop",
            "Vector Store Retriever",
            "Ollama Chat Model",
            "Code: JSON repair and split",
            "Execute Command: ciac validate candidate_interventions",
            "Execute Command: ciac discovery-compare or simulation commands",
        ],
        "artifact_outputs": [
            "examples/discovery/*.discovery.json",
            "candidate_interventions/*.json",
            "examples/discovery/*_comparison.json",
        ],
    }


def _first_warning_domain(world_manifest: dict[str, Any], runtime_bundle: dict[str, Any] | None) -> str | None:
    warning_text = " ".join(world_manifest.get("warnings", []))
    if runtime_bundle:
        for domain, status in runtime_bundle.get("capabilities", {}).get("domain_statuses", {}).items():
            if status.get("status") in {"warn", "warning", "fail", "failed"}:
                return domain
            warning_text += " " + " ".join(status.get("messages", []))
    lowered = warning_text.lower()
    for domain, hints in DOMAIN_HINTS.items():
        if any(keyword in lowered for keyword in hints["keywords"]):
            return domain
    return None


def _domain_messages(domain: str, warnings: list[str]) -> list[str]:
    hints = DOMAIN_HINTS.get(domain, {})
    keywords = hints.get("keywords", ())
    matches = []
    for warning in warnings:
        if _generic_warning(warning):
            continue
        lowered = warning.lower()
        if domain in lowered or any(keyword in lowered for keyword in keywords):
            matches.append(warning)
    return matches


def _objects_for_domain(world_manifest: dict[str, Any], domain: str) -> list[str]:
    suffixes = DOMAIN_HINTS.get(domain, {}).get("objects", ())
    objects = [
        *world_manifest.get("structures", []),
        *world_manifest.get("infrastructure_nodes", []),
        *world_manifest.get("paths", []),
    ]
    return [
        item["id"]
        for item in objects
        if any(item.get("id") == suffix or item.get("id", "").endswith(f"__{suffix}") for suffix in suffixes)
    ]


def _summary(domain: str, messages: list[str]) -> str:
    first = messages[0] if messages else "No warning message."
    return f"{domain.replace('_', ' ').title()} discovery loop is needed because: {first}"


def _severity(messages: list[str]) -> str:
    text = " ".join(messages).lower()
    if "block" in text or "fail" in text or "critical" in text:
        return "critical"
    if "not " in text or "incomplete" in text or "warn" in text:
        return "warning"
    return "watch"


def _query_for_domain(domain: str) -> str:
    return (
        f"CIaC {domain.replace('_', ' ')} warning interventions expected effects labor energy privacy "
        "public health governance accessibility scenario resilience"
    )


def _slug(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", value.lower()).strip("_")


def _generic_warning(warning: str) -> bool:
    lowered = warning.lower()
    return (
        "provisional civic simulation" in lowered
        or "capability scores are provisional" in lowered
        or "capability defaults are conservative" in lowered
    )
