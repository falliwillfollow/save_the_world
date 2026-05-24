from __future__ import annotations

from copy import deepcopy
from typing import Any


SAFETY_LANGUAGE = (
    "Capability scores are provisional modeling aids. They do not prove real-world dignity, safety, legal validity, "
    "health outcomes, consent, accessibility compliance, resident trust, or anti-capture success. They expose "
    "assumptions and blockers for review."
)

CAPABILITY_DOMAINS = {
    "dignity_privacy": {
        "privacy_floor": "unknown",
        "private_retreat_supported": False,
        "opt_out_protected": False,
        "dignity_risk_score": 5,
    },
    "labor_time": {
        "required_wage_hours_reduction_percent": 0.0,
        "commons_labor_hours_per_resident_per_week": 0.0,
        "hidden_labor_risk_score": 5,
        "burnout_risk_score": 5,
        "free_time_increase_supported": False,
    },
    "governance_anticapture": {
        "due_process_defined": False,
        "emergency_power_sunset_defined": False,
        "role_backup_coverage": 0.0,
        "capture_risk_score": 5,
    },
    "care_health": {
        "care_continuity_protocol_supported": False,
        "high_need_support_coverage": 0.0,
        "medication_continuity_supported": False,
        "care_meal_protocol_supported": False,
        "illness_wave_protocol_supported": False,
    },
    "sanitation": {
        "toilet_hygiene_access_supported": False,
        "blackwater_path_defined": False,
        "greywater_boundary_defined": False,
        "waste_stream_separation_supported": False,
        "hazardous_waste_plan_supported": False,
        "worker_safety_training_supported": False,
        "sanitation_labor_visibility_supported": False,
        "emergency_sanitation_fallback_supported": False,
        "pathogen_control_protocol_supported": False,
    },
    "mobility_access": {
        "accessible_route_coverage": 0.0,
        "route_gap_survey_supported": False,
        "accessible_route_status_visibility_supported": False,
        "emergency_access_status_declared": False,
        "non_driver_access_supported": False,
        "emergency_access_supported": False,
        "transport_burden_risk_score": 5,
    },
    "legal_land_finance": {
        "land_security_status": "unknown",
        "reserve_modeling_supported": False,
        "resident_rights_defined": False,
        "debt_risk_score": 5,
    },
    "maintenance_repair": {
        "asset_registry_supported": False,
        "class_a_coverage": 0.0,
        "spares_tracking_supported": False,
        "backlog_visibility_supported": False,
    },
    "education_skill": {
        "skill_redundancy_coverage": 0.0,
        "onboarding_supported": False,
        "safety_gate_supported": False,
        "knowledge_base_supported": False,
    },
    "social_cultural": {
        "belonging_supported": False,
        "opt_out_protected": False,
        "anti_clique_monitoring_supported": False,
        "coercion_risk_score": 5,
    },
    "risk_resilience": {
        "hazard_register_supported": False,
        "dependency_graph_supported": False,
        "dependency_graph_coverage": 0.0,
        "scenario_coverage_count": 0,
        "recovery_playbook_count": 0,
        "graceful_degradation_supported": False,
    },
    "materials_fabrication": {
        "maintainability_supported": False,
        "code_path_supported": False,
        "panelization_supported": False,
        "embodied_impact_tracking_supported": False,
    },
}

DELTA_TARGETS = {
    "burnout_risk_delta": "burnout_risk_score",
    "care_burnout_risk_delta": "burnout_risk_score",
    "capture_risk_delta": "capture_risk_score",
    "coercion_risk_delta": "coercion_risk_score",
    "debt_risk_delta": "debt_risk_score",
    "dignity_risk_delta": "dignity_risk_score",
    "hidden_labor_risk_delta": "hidden_labor_risk_score",
    "transport_burden_risk_delta": "transport_burden_risk_score",
    "required_wage_hours_delta_percent": "required_wage_hours_reduction_percent",
    "commons_labor_hours_per_resident_per_week_delta": "commons_labor_hours_per_resident_per_week",
    "commons_labor_hours_per_week_delta": "commons_labor_hours_per_resident_per_week",
    "role_backup_coverage_delta": "role_backup_coverage",
    "high_need_support_coverage_delta": "high_need_support_coverage",
    "accessible_route_coverage_delta": "accessible_route_coverage",
    "dependency_graph_coverage_delta": "dependency_graph_coverage",
    "class_a_coverage_delta": "class_a_coverage",
    "skill_redundancy_coverage_delta": "skill_redundancy_coverage",
    "scenario_coverage_delta": "scenario_coverage_count",
    "recovery_playbook_count_delta": "recovery_playbook_count",
}

NEGATIVE_BOOLEAN_FLAGS = {
    "private_retreat_supported",
    "opt_out_protected",
    "due_process_defined",
    "emergency_power_sunset_defined",
    "medication_continuity_supported",
    "care_meal_protocol_supported",
    "toilet_hygiene_access_supported",
    "blackwater_path_defined",
    "greywater_boundary_defined",
    "waste_stream_separation_supported",
    "hazardous_waste_plan_supported",
    "worker_safety_training_supported",
    "sanitation_labor_visibility_supported",
    "emergency_sanitation_fallback_supported",
    "pathogen_control_protocol_supported",
    "emergency_access_supported",
    "reserve_modeling_supported",
    "resident_rights_defined",
    "dependency_graph_supported",
    "graceful_degradation_supported",
}


def default_capability_state(population: int | None = None) -> dict[str, Any]:
    return {
        "kind": "CapabilityState",
        "version": "v0",
        "provisional": True,
        "population": int(population or 0),
        "domains": deepcopy(CAPABILITY_DOMAINS),
        "ledger": [],
        "warnings": [
            SAFETY_LANGUAGE,
            "Capability defaults are conservative placeholders until patterns declare explicit capability effects.",
        ],
        "failures": [],
    }


def apply_capability_effects(
    capability_state: dict[str, Any],
    pattern_id: str,
    effects: dict[str, Any] | None,
    source: str = "selected_pattern",
) -> dict[str, Any]:
    state = deepcopy(capability_state)
    if not effects:
        return state

    domains = state.setdefault("domains", {})
    ledger = state.setdefault("ledger", [])
    warnings = state.setdefault("warnings", [])

    for domain, domain_effects in sorted(effects.items()):
        if not isinstance(domain_effects, dict):
            warnings.append(f"{pattern_id}:{domain} capability effects were ignored because the domain value is not an object.")
            continue
        if domain not in domains:
            domains[domain] = {}
            warnings.append(f"{pattern_id} declared provisional unknown capability domain: {domain}.")
        domain_state = domains[domain]
        for field, value in sorted(domain_effects.items()):
            if isinstance(value, bool):
                target_field = field
                before = domain_state.get(target_field)
                after = True if value else (False if field in NEGATIVE_BOOLEAN_FLAGS else before)
                domain_state[target_field] = after
                operation = "boolean_set" if value or field in NEGATIVE_BOOLEAN_FLAGS else "boolean_declaration"
            elif isinstance(value, (int, float)) and field.endswith("_delta"):
                target_field = _delta_target(field, domain_state)
                before = domain_state.get(target_field, 0)
                after = _clamp_field(target_field, float(before or 0) + float(value))
                domain_state[target_field] = after
                operation = "delta"
            else:
                target_field = field
                before = domain_state.get(target_field)
                after = _clamp_field(target_field, value)
                domain_state[target_field] = after
                operation = "absolute"
            ledger.append(
                {
                    "pattern_id": pattern_id,
                    "domain": domain,
                    "field": target_field,
                    "input_field": field,
                    "operation": operation,
                    "value": value,
                    "before": before,
                    "after": after,
                    "source": source,
                    "provisional": True,
                }
            )
    return state


def capability_effects_for_plan(compiled_plan: dict[str, Any]) -> dict[str, Any]:
    return compiled_plan.get("simulation_inputs", {}).get("capability_effects_by_pattern", {}) or {}


def build_capability_state(
    compiled_plan: dict[str, Any],
    population: int | None = None,
    scenario: dict[str, Any] | None = None,
) -> dict[str, Any]:
    state = default_capability_state(population=population)
    _apply_compiled_plan_context(state, compiled_plan)
    for pattern_id, effects in sorted(capability_effects_for_plan(compiled_plan).items()):
        state = apply_capability_effects(state, pattern_id=pattern_id, effects=effects, source="selected_pattern")
    if scenario and scenario.get("capability_shocks"):
        state = apply_capability_effects(
            state,
            pattern_id=scenario.get("id", "scenario"),
            effects=scenario.get("capability_shocks", {}),
            source="scenario",
        )
    return state


def _apply_compiled_plan_context(state: dict[str, Any], compiled_plan: dict[str, Any]) -> None:
    labor = state.setdefault("domains", {}).setdefault("labor_time", {})
    burden = compiled_plan.get("role_burden", {})
    if isinstance(burden.get("recurring_hours_per_resident_per_week"), (int, float)):
        labor["commons_labor_hours_per_resident_per_week"] = round(float(burden["recurring_hours_per_resident_per_week"]), 3)


def evaluate_capability_gate(
    capability_state: dict[str, Any],
    active_patterns: list[str] | None = None,
) -> dict[str, Any]:
    patterns = set(active_patterns or [])
    domains = capability_state.get("domains", {})
    domain_statuses = {
        "labor_time": _labor_time_gate(domains.get("labor_time", {})),
        "governance_anticapture": _governance_gate(domains.get("governance_anticapture", {}), patterns),
        "care_health": _care_gate(domains.get("care_health", {}), patterns),
        "mobility_access": _mobility_gate(domains.get("mobility_access", {}), patterns),
        "legal_land_finance": _legal_finance_gate(domains.get("legal_land_finance", {}), patterns),
        "risk_resilience": _risk_resilience_gate(domains.get("risk_resilience", {}), patterns),
    }
    failures = [
        message
        for result in domain_statuses.values()
        for message in result["messages"]
        if result["status"] == "fail"
    ]
    warnings = [
        message
        for result in domain_statuses.values()
        for message in result["messages"]
        if result["status"] == "warn"
    ]
    status = _overall_status(domain_statuses.values())
    return {
        "kind": "CapabilityGateReport",
        "id": "capability_gate_v0",
        "generated_by": "ciac.capabilities.v0",
        "provisional": True,
        "status": status,
        "domain_statuses": domain_statuses,
        "failures": failures,
        "warnings": warnings,
        "unknowns": [
            SAFETY_LANGUAGE,
            "Unknown capability fields warn by default unless a safety-critical active module depends on them.",
        ],
    }


def runtime_capability_summary(capability_state: dict[str, Any], capability_gate: dict[str, Any] | None = None) -> dict[str, Any]:
    gate = capability_gate or evaluate_capability_gate(capability_state)
    return {
        "state": capability_state,
        "domain_statuses": gate.get("domain_statuses", {}),
        "ledger": capability_state.get("ledger", []),
        "warnings": sorted(set(capability_state.get("warnings", []) + gate.get("warnings", []))),
        "failures": sorted(set(capability_state.get("failures", []) + gate.get("failures", []))),
        "provisional": True,
    }


def _delta_target(field: str, domain_state: dict[str, Any]) -> str:
    if field in DELTA_TARGETS:
        return DELTA_TARGETS[field]
    base = field[:-6]
    if f"{base}_score" in domain_state:
        return f"{base}_score"
    if base in domain_state:
        return base
    return base


def _clamp_field(field: str, value: Any) -> Any:
    if not isinstance(value, (int, float)):
        return value
    numeric = float(value)
    if field.endswith("_coverage") or field.endswith("_ratio"):
        return round(max(0.0, min(1.0, numeric)), 3)
    if field.endswith("_risk_score") or field in {"dignity_risk_score", "burnout_risk_score"}:
        return round(max(0.0, min(10.0, numeric)), 3)
    if field.endswith("_count"):
        return max(0, int(round(numeric)))
    return round(numeric, 3)


def _labor_time_gate(domain: dict[str, Any]) -> dict[str, Any]:
    failures = []
    warnings = []
    if float(domain.get("hidden_labor_risk_score", 5)) >= 8:
        failures.append("Hidden labor risk is at or above the blocking threshold.")
    if float(domain.get("burnout_risk_score", 5)) >= 8:
        failures.append("Burnout risk is at or above the blocking threshold.")
    if float(domain.get("commons_labor_hours_per_resident_per_week", 0)) > 12:
        failures.append("Commons labor exceeds 12 hours per resident per week.")
    if not domain.get("hidden_labor_tracking_supported"):
        warnings.append("Hidden labor tracking is not yet explicitly supported.")
    return _domain_result(failures, warnings)


def _governance_gate(domain: dict[str, Any], patterns: set[str]) -> dict[str, Any]:
    failures = []
    warnings = []
    governance_active = bool(patterns.intersection({"commons_stewardship_protocol", "graceful_degradation_engine"}))
    if not domain.get("due_process_defined"):
        (failures if "commons_stewardship_protocol" in patterns else warnings).append("Due process is not explicitly defined.")
    if not domain.get("emergency_power_sunset_defined"):
        (failures if governance_active else warnings).append("Emergency power sunset is not explicitly defined.")
    if float(domain.get("capture_risk_score", 5)) >= 8:
        failures.append("Capture risk is at or above the blocking threshold.")
    if float(domain.get("role_backup_coverage", 0)) < 0.1 and governance_active:
        warnings.append("Governance role-backup coverage is low.")
    return _domain_result(failures, warnings)


def _care_gate(domain: dict[str, Any], patterns: set[str]) -> dict[str, Any]:
    failures = []
    warnings = []
    care_active = "community_care_commons" in patterns
    if not domain.get("care_continuity_protocol_supported"):
        warnings.append("Care continuity protocol is not explicitly supported.")
    if care_active and float(domain.get("high_need_support_coverage", 0)) < 0.2:
        failures.append("High-need support coverage is below the active care-module threshold.")
    elif float(domain.get("high_need_support_coverage", 0)) < 0.2:
        warnings.append("High-need support coverage is below the review threshold.")
    if care_active and not domain.get("medication_continuity_supported"):
        failures.append("Medication continuity is not explicitly supported for the active care module.")
    elif not domain.get("medication_continuity_supported"):
        warnings.append("Medication continuity is not yet explicitly supported.")
    if not domain.get("care_meal_protocol_supported"):
        warnings.append("Care meal protocol is not explicitly supported.")
    if not domain.get("illness_wave_protocol_supported"):
        warnings.append("Illness-wave protocol is not explicitly supported.")
    return _domain_result(failures, warnings)


def _mobility_gate(domain: dict[str, Any], patterns: set[str]) -> dict[str, Any]:
    failures = []
    warnings = []
    if "pedestrian_first_access_commons" in patterns and not domain.get("emergency_access_supported"):
        failures.append("Emergency access is not explicitly supported for the active mobility module.")
    if float(domain.get("accessible_route_coverage", 0)) < 1.0:
        warnings.append("Accessible-route coverage is not complete.")
    if not domain.get("non_driver_access_supported"):
        warnings.append("Non-driver access is not explicitly supported.")
    if not domain.get("emergency_access_supported"):
        warnings.append("Emergency access is not explicitly supported.")
    return _domain_result(failures, warnings)


def _legal_finance_gate(domain: dict[str, Any], patterns: set[str]) -> dict[str, Any]:
    failures = []
    warnings = []
    active = "anti_speculative_civic_floor" in patterns
    if domain.get("land_security_status") == "fail":
        failures.append("Land security status is fail.")
    if float(domain.get("debt_risk_score", 5)) >= 8:
        failures.append("Debt risk is at or above the blocking threshold.")
    if active and not domain.get("reserve_modeling_supported"):
        warnings.append("Reserve modeling is not explicitly supported for the active legal-finance module.")
    if active and not domain.get("resident_rights_defined"):
        warnings.append("Resident rights are not explicitly defined for the active legal-finance module.")
    return _domain_result(failures, warnings)


def _risk_resilience_gate(domain: dict[str, Any], patterns: set[str]) -> dict[str, Any]:
    failures = []
    warnings = []
    active = "graceful_degradation_engine" in patterns
    if active and not domain.get("dependency_graph_supported"):
        failures.append("Dependency graph is not explicitly supported for the active resilience module.")
    if active and int(domain.get("recovery_playbook_count", 0)) == 0:
        warnings.append("No recovery playbooks are declared for the active resilience module.")
    if active and int(domain.get("scenario_coverage_count", 0)) < 1:
        warnings.append("No scenario coverage is declared for the active resilience module.")
    return _domain_result(failures, warnings)


def _domain_result(failures: list[str], warnings: list[str]) -> dict[str, Any]:
    status = "fail" if failures else "warn" if warnings else "pass"
    return {
        "status": status,
        "messages": failures + warnings,
        "provisional": True,
    }


def _overall_status(results: Any) -> str:
    statuses = [result["status"] for result in results]
    if "fail" in statuses:
        return "fail"
    if "warn" in statuses:
        return "warn"
    return "pass"
