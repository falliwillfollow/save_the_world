# CIaC Capability Thresholds Research Pack, Part 2: Policy Translation and Scenario Logic

**Research ID:** `ciac_capability_thresholds_research_pack_part_2_v0_1`  
**Parent:** `ciac_capability_thresholds_research_pack_part_1_v0_1`  
**Purpose:** Translate the Part 1 capability research into a machine-readable policy structure, capability gates, scenario tests, viewer warnings, and repo implementation steps.  
**Status:** Implementation-oriented research synthesis. This is not legal, medical, clinical, accessibility, engineering, employment, finance, or emergency-management certification.  
**Primary CIaC use:** create `capability_policy.schema.json`, `capability_policies/ciac_capability_policy_v0.yaml`, capability-gate tests, scenario packs, and viewer warning logic.

---

## 0. Why This Part Exists

Part 1 answered the capability research questions across six domains:

```text
Care Health
Governance
Mobility
Legal / Land / Finance
Risk Resilience
Labor / Time
```

Part 2 converts those answers into policy logic:

```text
source registry
capability field registry
domain gates
pass / warn / fail / promotion-block states
mandatory scenario coverage
viewer warning messages
test cases
implementation order
```

The key implementation idea is that a model can be **simulation-useful** while still **promotion-blocked**.

```yaml
simulation_only:
  meaning: The model may visualize or reason about a capability, but it cannot claim real-world validity.

review_blocked:
  meaning: The model may simulate this capability, but real-world promotion is blocked until external review is complete.

promotion_ready:
  meaning: Internal gates are green and no unresolved external-review blockers remain for the claim being made.
```

---

## 1. Proposed Repo Additions

```text
schemas/capability_policy.schema.json
capability_policies/ciac_capability_policy_v0.yaml
ciac/capability_policy.py
ciac/capability_gate.py
scenarios/capability/
  care_health_illness_wave.yaml
  governance_emergency_power_drift.yaml
  mobility_access_route_blockage.yaml
  legal_finance_reserve_shock.yaml
  risk_resilience_compound_failure.yaml
  labor_time_hidden_burden.yaml
tests/test_capability_policy.py
tests/test_capability_gate_policy.py
tests/test_capability_scenarios.py
docs/capability_policy_v0.md
```

---

## 2. Proposed Capability Policy Schema

```yaml
CapabilityPolicy:
  policy_id: string
  version: string
  status: provisional | reviewed | deprecated
  source_registry: list[Source]
  domains: map[DomainPolicy]
  promotion_blockers: list[PromotionBlocker]
  scenario_requirements: list[ScenarioRequirement]
  ui_warnings: map[UIWarning]

Source:
  id: string
  title: string
  organization: string
  url: string
  evidence_quality: high | moderate | low | mixed
  supports: list[string]

DomainPolicy:
  domain: string
  capability_fields: list[string]
  gates: list[CapabilityGate]
  required_structures: list[string]
  required_protocols: list[string]
  external_review_blockers: list[string]
  scenarios: list[string]
  ui_warnings: list[string]

CapabilityGate:
  gate_id: string
  capability_field: string
  pass_condition: any
  warn_condition: any
  fail_condition: any
  promotion_block_condition: any
  evidence_quality: high | moderate | low | mixed
  translation_confidence: high | moderate | low
  regulatory_strength: binding | guideline | professional_practice | research_inferred | heuristic
  source_ids: list[string]
```

---

## 3. Source Registry, Policy IDs

Use the source registry from Part 1. Minimum source IDs required for this policy:

```yaml
required_source_ids:
  care_health:
    - CDC_DISABILITY_EMERGENCY_KIT
    - CDC_RESPIRATORY_PREVENTION
    - HRSA_HEALTH_CENTER_PROGRAM
    - CDC_CHW_CHRONIC_CARE
    - IMPACT_CHW_RCT

  governance:
    - CORNELL_PROCEDURAL_DUE_PROCESS
    - NIST_PRIVACY_FRAMEWORK
    - FEMA_ICS_SPAN_CONTROL
    - FEMA_NATIONAL_RESILIENCE_GUIDANCE

  mobility:
    - ACCESS_BOARD_ACCESSIBLE_ROUTES
    - ITDP_TOD_STANDARD
    - CDC_DISABILITY_EMERGENCY_KIT

  legal_land_finance:
    - GSN_CLT
    - GSN_RESALE_FORMULAS
    - LOCAL_HOUSING_SOLUTIONS_LEC
    - HUD_CHAS_COST_BURDEN
    - IRS_501C3_ORGANIZATIONAL_TEST

  risk_resilience:
    - NIST_COMMUNITY_RESILIENCE_GUIDE
    - FEMA_NATIONAL_RESILIENCE_GUIDANCE
    - SENDAI_FRAMEWORK

  labor_time:
    - BLS_ATUS_2024
    - WHO_ILO_LONG_WORKING_HOURS
    - OECD_WORK_LIFE_BALANCE
    - UKRI_FOUR_DAY_WEEK
```

---

## 4. Capability Field Registry

```yaml
capability_fields:
  care_health:
    - care_health.nonclinical_care_floor
    - care_health.external_care_path
    - care_health.clinical_boundary_status
    - care_health.high_need_support_coverage
    - care_health.medication_continuity_status
    - care_health.care_meal_protocol_status
    - care_health.illness_wave_readiness
    - care_health.care_labor_burden_status

  governance_anticapture:
    - governance_anticapture.due_process_status
    - governance_anticapture.emergency_power_sunset
    - governance_anticapture.role_backup_coverage
    - governance_anticapture.role_concentration_score
    - governance_anticapture.decision_domain_clarity
    - governance_anticapture.records_privacy_status
    - governance_anticapture.external_review_trigger_status

  mobility_access:
    - mobility_access.accessible_route_coverage
    - mobility_access.essential_access_minutes_max
    - mobility_access.accessible_route_penalty
    - mobility_access.non_driver_access_status
    - mobility_access.emergency_access_status
    - mobility_access.mobility_support_module_status
    - mobility_access.route_quality_score

  legal_land_finance:
    - legal_land_finance.tenure_security_status
    - legal_land_finance.resident_rights_status
    - legal_land_finance.reserve_status
    - legal_land_finance.affordability_burden_status
    - legal_land_finance.anti_displacement_status
    - legal_land_finance.external_review_blockers
    - legal_land_finance.asset_lock_status

  risk_resilience:
    - risk_resilience.hazard_register_coverage
    - risk_resilience.dependency_graph_completeness
    - risk_resilience.recovery_playbook_count
    - risk_resilience.graceful_degradation_status
    - risk_resilience.recovery_time_objective_status
    - risk_resilience.promotion_blocker_count
    - risk_resilience.single_point_failure_count

  labor_time:
    - labor_time.commons_labor_hours_per_resident_per_week
    - labor_time.required_wage_hours_reduction_percent
    - labor_time.free_time_increase_hours_per_week
    - labor_time.passion_time_increase_hours_per_week
    - labor_time.hidden_labor_status
    - labor_time.labor_concentration_score
    - labor_time.burnout_risk_score
    - labor_time.trained_role_requirement_status
```

---

# 5. Domain Policy, Care Health

```yaml
domain: care_health

required_structures:
  - care_room
  - first_aid_station
  - medication_refrigeration_point
  - emergency_charging_point
  - care_meal_delivery_path
  - privacy_limited_high_need_registry
  - external_healthcare_registry

required_protocols:
  - nonclinical_support_scope
  - emergency_escalation
  - privacy_and_consent
  - medication_cold_chain
  - care_meal_activation
  - illness_wave_protocol
  - high_need_support_plan
  - care_labor_review

external_review_blockers:
  - clinical_boundary_review
  - privacy_review
  - liability_review
  - EMS_fire_access_review
  - public_health_review_for_illness_wave
```

### 5.1 Care Health Gates

```yaml
gates:
  - gate_id: care_nonclinical_floor
    capability_field: care_health.nonclinical_care_floor
    pass_condition:
      care_room: true
      first_aid_station: true
      external_care_path: true
      no_clinical_claims: true
    warn_condition:
      care_room_exists_but_trained_backup_missing: true
      external_care_path_unclear: true
    fail_condition:
      no_private_care_space: true
      claims_to_replace_professional_care: true
    promotion_block_condition:
      clinical_boundary_unreviewed_and_public_claim_made: true
    source_ids:
      - CDC_DISABILITY_EMERGENCY_KIT
      - HRSA_HEALTH_CENTER_PROGRAM
      - CDC_CHW_CHRONIC_CARE

  - gate_id: high_need_support_coverage
    capability_field: care_health.high_need_support_coverage
    pass_condition:
      known_or_opt_in_high_need_support_plans: 100_percent
      backup_role: true
      privacy: function_based_not_diagnosis_based
    warn_condition:
      coverage_below_100_percent: true
      backup_missing: true
    fail_condition:
      high_need_residents_not_modeled: true
      public_diagnosis_disclosure_required: true
    promotion_block_condition:
      high_need_support_unmodeled_in_public_demo: true
    source_ids:
      - CDC_DISABILITY_EMERGENCY_KIT
      - FEMA_NATIONAL_RESILIENCE_GUIDANCE

  - gate_id: medication_continuity
    capability_field: care_health.medication_continuity_status
    pass_condition:
      one_week_medication_planning: true
      refrigerated_medication_cooler_or_backup: true
      critical_energy_mapping: true
      pharmacy_access_plan: true
    warn_condition:
      refrigerated_medications_present_without_backup_power: true
    fail_condition:
      no_medication_continuity_plan: true
      no_privacy_for_medication_needs: true
    promotion_block_condition:
      medically_vulnerable_population_modeled_without_medication_continuity: true
    source_ids:
      - CDC_DISABILITY_EMERGENCY_KIT

  - gate_id: illness_wave_readiness
    capability_field: care_health.illness_wave_readiness
    pass_condition:
      stay_home_support: true
      meal_delivery: true
      sanitation_escalation: true
      medication_check: true
      privacy_preserved: true
    warn_condition:
      no_cleaner_air_strategy: true
      backup_labor_missing: true
    fail_condition:
      sick_residents_must_use_common_meals: true
      public_diagnosis_disclosure_required: true
      no_sanitation_escalation: true
    promotion_block_condition:
      public_health_claims_made_without_review: true
    source_ids:
      - CDC_RESPIRATORY_PREVENTION
      - CDC_DISABILITY_EMERGENCY_KIT
```

---

# 6. Domain Policy, Governance and Anti-Capture

```yaml
domain: governance_anticapture

required_structures:
  - decision_log
  - policy_registry
  - role_registry
  - backup_role_registry
  - conflict_process
  - recusal_policy
  - emergency_authority_log
  - records_classification_policy

required_protocols:
  - notice_and_response
  - impartial_review
  - appeal_or_reconsideration
  - emergency_power_sunset
  - role_concentration_audit
  - public_private_anonymized_records_policy

external_review_blockers:
  - loss_of_access_or_expulsion_legal_review
  - serious_harm_safeguarding_review
  - privacy_review
  - asset_or_land_decision_legal_review
```

### 6.1 Governance Gates

```yaml
gates:
  - gate_id: due_process_minimum
    capability_field: governance_anticapture.due_process_status
    pass_condition:
      notice: true
      stated_reasons: true
      opportunity_to_respond: true
      impartial_review: true
      recordkeeping: true
      appeal_path: true
    warn_condition:
      appeal_path_missing: true
      recusal_rule_missing: true
    fail_condition:
      loss_of_access_without_notice_review_or_appeal: true
    promotion_block_condition:
      membership_or_occupancy_decision_without_legal_review: true
    source_ids:
      - CORNELL_PROCEDURAL_DUE_PROCESS

  - gate_id: emergency_power_sunset
    capability_field: governance_anticapture.emergency_power_sunset
    pass_condition:
      default_sunset_hours: 72
      extension_requires_review: true
      incident_log: true
      after_action_review: true
    warn_condition:
      extension_beyond_72_without_member_notice: true
    fail_condition:
      no_sunset: true
      emergency_power_can_change_constitutional_rules: true
    promotion_block_condition:
      emergency_power_can_transfer_assets_or_remove_opponents: true
    source_ids:
      - FEMA_ICS_SPAN_CONTROL
      - FEMA_NATIONAL_RESILIENCE_GUIDANCE

  - gate_id: role_backup_and_concentration
    capability_field: governance_anticapture.role_backup_coverage
    pass_condition:
      critical_roles_with_backup: 100_percent
      high_power_functions_separated: true
    warn_condition:
      critical_roles_with_backup_below_100_percent: true
      one_person_holds_two_high_power_roles: true
    fail_condition:
      one_person_controls_money_records_conflict_or_survival_access: true
      emergency_role_no_backup: true
    promotion_block_condition:
      founder_or_admin_single_point_authority: true
    source_ids:
      - FEMA_ICS_SPAN_CONTROL
      - NIST_PRIVACY_FRAMEWORK

  - gate_id: records_classification
    capability_field: governance_anticapture.records_privacy_status
    pass_condition:
      member_public_budget_records: true
      private_health_conflict_financial_records: true
      anonymized_aggregate_sensitive_dashboards: true
      role_based_access: true
    warn_condition:
      no_retention_policy: true
      role_access_unclear: true
    fail_condition:
      health_conflict_or_financial_hardship_public_by_default: true
      common_power_records_hidden: true
    promotion_block_condition:
      sensitive_data_exposed_in_public_world_or_report: true
    source_ids:
      - NIST_PRIVACY_FRAMEWORK
```

---

# 7. Domain Policy, Mobility and Access

```yaml
domain: mobility_access

required_structures:
  - accessible_route_map
  - distance_friction_calculator
  - emergency_route_map
  - rest_node_map
  - route_quality_metadata
  - shared_cart_or_vehicle_node
  - care_transport_plan

required_protocols:
  - accessibility_audit
  - route_inspection
  - route_clearance
  - care_transport
  - shared_mobility_booking
  - repair_protocol
  - non_driver_access_review

external_review_blockers:
  - accessibility_code_review
  - fire_EMS_access_review
  - shared_vehicle_insurance_review
  - civil_drainage_route_review
```

### 7.1 Mobility Gates

```yaml
gates:
  - gate_id: accessible_route_coverage
    capability_field: mobility_access.accessible_route_coverage
    pass_condition:
      essential_accessible_route_coverage: 100_percent
    warn_condition:
      essential_accessible_route_coverage_between_95_and_99: true
      accessible_route_longer_than_primary_route: true
    fail_condition:
      any_essential_space_lacks_accessible_route: true
      emergency_route_inaccessible: true
    promotion_block_condition:
      public_demo_claims_accessibility_with_unresolved_route_failure: true
    source_ids:
      - ACCESS_BOARD_ACCESSIBLE_ROUTES

  - gate_id: daily_need_distance
    capability_field: mobility_access.essential_access_minutes_max
    pass_condition:
      essential_daily_needs_within_5_minutes: true
      high_need_care_food_water_access_within_3_to_5_minutes: true
      transit_or_shuttle_within_10_minutes_where_needed: true
    warn_condition:
      essentials_above_5_minutes_for_high_need_residents: true
      transit_above_10_minutes: true
    fail_condition:
      daily_needs_require_private_car: true
      non_drivers_cannot_access_food_care_pharmacy_or_clinic: true
    promotion_block_condition:
      transport_cost_erases_affordability_but_unmodeled: true
    source_ids:
      - ITDP_TOD_STANDARD
      - ACCESS_BOARD_ACCESSIBLE_ROUTES

  - gate_id: emergency_access
    capability_field: mobility_access.emergency_access_status
    pass_condition:
      fire_EMS_access_reviewed: true
      emergency_pickup_points_mapped: true
      high_need_evacuation_plan: true
    warn_condition:
      no_backup_route: true
      emergency_route_crosses_social_core: true
    fail_condition:
      no_fire_EMS_review: true
      pedestrian_only_design_blocks_emergency_response: true
    promotion_block_condition:
      build_claim_made_without_fire_EMS_access_review: true
    source_ids:
      - FEMA_NATIONAL_RESILIENCE_GUIDANCE
```

---

# 8. Domain Policy, Legal Land and Finance

```yaml
domain: legal_land_finance

required_structures:
  - land_stewardship_model
  - written_resident_rights
  - occupancy_or_use_agreement
  - asset_lock
  - resale_or_exit_formula
  - operating_reserve
  - replacement_reserve
  - emergency_repair_reserve
  - affordability_calculator
  - hardship_policy

required_protocols:
  - resident_rights_onboarding
  - due_process_before_loss_of_access
  - payment_hardship_review
  - reserve_drawdown_and_replenishment
  - resale_or_exit_process
  - external_review_blocker_tracking

external_review_blockers:
  - entity_structure
  - land_control
  - occupancy_agreements
  - debt_collateral
  - securities_or_fundraising
  - tax_status
  - insurance
  - zoning_permitting
```

### 8.1 Legal / Finance Gates

```yaml
gates:
  - gate_id: tenure_security
    capability_field: legal_land_finance.tenure_security_status
    pass_condition:
      secure_land_control: true
      written_use_rights: true
      due_process: true
      asset_lock_or_transfer_restriction: true
      external_legal_review: true
    warn_condition:
      founder_or_investor_owned_land: true
      exit_formula_unclear: true
    fail_condition:
      no_secure_land_control: true
      residents_have_no_written_use_rights: true
      core_assets_can_be_sold_for_private_gain_without_review: true
    promotion_block_condition:
      real_world_pilot_claim_without_legal_review: true
    source_ids:
      - GSN_CLT
      - LOCAL_HOUSING_SOLUTIONS_LEC

  - gate_id: reserve_status
    capability_field: legal_land_finance.reserve_status
    pass_condition:
      operating_reserve_months: 3_to_6
      replacement_reserve_funded: true
      emergency_repair_reserve: true
      deductible_reserve: true
      replenishment_plan: true
    warn_condition:
      operating_reserve_below_3_months: true
      hardship_reserve_absent: true
    fail_condition:
      no_operating_reserve: true
      no_replacement_reserve_for_class_A_assets: true
      reserves_excluded_from_affordability: true
    promotion_block_condition:
      affordability_claim_excludes_reserves: true
    source_ids:
      - HUD_CHAS_COST_BURDEN

  - gate_id: affordability_burden
    capability_field: legal_land_finance.affordability_burden_status
    pass_condition:
      housing_plus_utilities_below_30_percent_income: true
      transport_included: true
      reserves_included: true
      required_wage_hours_modeled: true
    warn_condition:
      housing_plus_utilities_30_to_50_percent_income: true
      transport_erases_savings: true
    fail_condition:
      housing_plus_utilities_above_50_percent_without_subsidy_or_hardship_plan: true
      affordability_depends_on_unpaid_hidden_labor: true
    promotion_block_condition:
      public_affordability_claim_without_cost_burden_and_reserve_model: true
    source_ids:
      - HUD_CHAS_COST_BURDEN
      - BLS_ATUS_2024

  - gate_id: external_review_blockers
    capability_field: legal_land_finance.external_review_blockers
    pass_condition:
      all_required_reviews_complete_or_not_applicable: true
    warn_condition:
      review_required_but_simulation_only: true
    fail_condition:
      real_world_promotion_attempt_with_unresolved_blocker: true
    promotion_block_condition:
      unresolved_legal_finance_blocker: true
    source_ids:
      - IRS_501C3_ORGANIZATIONAL_TEST
      - GSN_CLT
```

---

# 9. Domain Policy, Risk and Resilience

```yaml
domain: risk_resilience

required_structures:
  - hazard_register
  - dependency_graph
  - critical_function_map
  - recovery_playbook_library
  - service_level_matrix
  - emergency_mode_manager
  - reserve_and_buffer_dashboard
  - after_action_review_log

required_protocols:
  - annual_risk_review
  - scenario_run_schedule
  - hazard_owner_assignment
  - after_action_review
  - reserve_replenishment
  - emergency_mode_sunset
  - promotion_blocker_check

external_review_blockers:
  - emergency_management_review
  - fire_EMS_review
  - public_health_review
  - insurance_review
  - climate_hazard_review
```

### 9.1 Risk / Resilience Gates

```yaml
gates:
  - gate_id: mandatory_hazard_register
    capability_field: risk_resilience.hazard_register_coverage
    pass_condition:
      mandatory_hazards_modeled:
        - water_contamination
        - energy_outage_72h
        - illness_wave
        - food_disruption
        - fire
        - extreme_heat
        - extreme_cold
        - financial_shock
        - care_steward_unavailable
        - governance_conflict_or_capture
        - mobility_route_blockage
    warn_condition:
      not_all_mandatory_hazards_modelled: true
      no_compound_scenarios: true
    fail_condition:
      no_hazard_register: true
      no_floor_continuity_scenario: true
      no_high_need_scenario: true
    promotion_block_condition:
      public_resilience_claim_without_hazard_register: true
    source_ids:
      - NIST_COMMUNITY_RESILIENCE_GUIDE
      - FEMA_NATIONAL_RESILIENCE_GUIDANCE
      - SENDAI_FRAMEWORK

  - gate_id: dependency_graph
    capability_field: risk_resilience.dependency_graph_completeness
    pass_condition:
      includes:
        - resource_flows
        - labor_roles
        - external_suppliers
        - critical_infrastructure
        - governance_authority
        - high_need_support
        - professional_review_dependencies
        - reserves
        - transport_access_routes
        - data_admin_access
    warn_condition:
      external_dependencies_unmapped: true
      labor_roles_omitted: true
    fail_condition:
      no_dependency_graph: true
      critical_functions_untraceable: true
    promotion_block_condition:
      public_system_claim_without_dependency_graph: true
    source_ids:
      - NIST_COMMUNITY_RESILIENCE_GUIDE

  - gate_id: recovery_playbooks
    capability_field: risk_resilience.recovery_playbook_count
    pass_condition:
      count: 8
      includes:
        - water_contamination_recovery
        - energy_outage_recovery
        - illness_wave_recovery
        - food_disruption_recovery
        - fire_or_shelter_loss_recovery
        - financial_shock_recovery
        - care_support_failure_recovery
        - governance_conflict_or_capture_recovery
    warn_condition:
      count_between_4_and_7: true
    fail_condition:
      count_below_4: true
      missing_water_energy_illness_or_finance_playbook: true
    promotion_block_condition:
      public_resilience_claim_without_recovery_playbooks: true
    source_ids:
      - NIST_COMMUNITY_RESILIENCE_GUIDE
      - FEMA_NATIONAL_RESILIENCE_GUIDANCE

  - gate_id: graceful_degradation
    capability_field: risk_resilience.graceful_degradation_status
    pass_condition:
      service_levels_defined: true
      rationing_rules_defined: true
      priority_loads_defined: true
      fallback_services_defined: true
      high_need_protections_defined: true
      rights_preserved: true
      recovery_path_defined: true
    warn_condition:
      labor_surge_unmodeled: true
      high_need_impact_incomplete: true
    fail_condition:
      optional_systems_protected_before_vulnerable_residents: true
      no_rationing_or_fallback_logic: true
      emergency_mode_suspends_rights_without_limit: true
    promotion_block_condition:
      resilience_claim_without_degradation_logic: true
    source_ids:
      - NIST_COMMUNITY_RESILIENCE_GUIDE
      - SENDAI_FRAMEWORK
```

---

# 10. Domain Policy, Labor and Time

```yaml
domain: labor_time

required_structures:
  - labor_ledger
  - role_scheduler
  - hidden_labor_tracker
  - care_labor_tracker
  - emergency_labor_tracker
  - protected_time_dashboard
  - baseline_comparison
  - training_gate_matrix

required_protocols:
  - weekly_labor_accounting
  - monthly_fairness_audit
  - labor_concentration_review
  - burnout_trigger
  - paid_external_support_threshold
  - accommodation_process
  - optional_vs_required_labor_classifier

external_review_blockers:
  - employment_labor_review_if_work_is_required_or_paid
  - disability_accommodation_review
  - privacy_review_for_labor_data
```

### 10.1 Labor / Time Gates

```yaml
gates:
  - gate_id: commons_labor_upper_bound
    capability_field: labor_time.commons_labor_hours_per_resident_per_week
    pass_condition:
      value_range: 4_to_8
    warn_condition:
      value_range: 8_to_10
    fail_condition:
      value_above: 12
      condition: by_default_or_unpaid_hidden_labor
    promotion_block_condition:
      public_life_burden_reduction_claim_while_labor_above_fail: true
    source_ids:
      - BLS_ATUS_2024
      - WHO_ILO_LONG_WORKING_HOURS
      - OECD_WORK_LIFE_BALANCE

  - gate_id: labor_type_separation
    capability_field: labor_time.hidden_labor_status
    pass_condition:
      categories_tracked:
        - required_wage_labor
        - commons_labor
        - private_household_labor
        - care_labor
        - governance_labor
        - maintenance_labor
        - training_labor
        - emergency_labor
        - emotional_support_labor
        - optional_passion_labor
    warn_condition:
      emotional_or_scheduling_labor_untracked: true
      emergency_labor_untracked: true
    fail_condition:
      care_cleaning_food_governance_or_maintenance_labor_untracked: true
      savings_depend_on_unpaid_hidden_labor: true
    promotion_block_condition:
      life_burden_claim_without_hidden_labor_model: true
    source_ids:
      - BLS_ATUS_2024
      - OECD_WORK_LIFE_BALANCE

  - gate_id: meaningful_free_time
    capability_field: labor_time.free_time_increase_hours_per_week
    pass_condition:
      free_time_increase_hours_per_week_at_least: 5
      passion_time_increase_hours_per_week_at_least: 3
      required_wage_hours_reduction_percent_at_least: 25
      total_compulsory_labor_reduction_positive: true
    warn_condition:
      free_time_increase_hours_per_week_between: 1_to_5
      gains_erased_in_bad_week: true
    fail_condition:
      free_time_not_increased: true
      required_wage_hours_not_reduced: true
      total_compulsory_labor_increases: true
    promotion_block_condition:
      public_liberated_time_claim_without_baseline_comparison: true
    source_ids:
      - BLS_ATUS_2024
      - WHO_ILO_LONG_WORKING_HOURS
      - UKRI_FOUR_DAY_WEEK

  - gate_id: trained_role_requirement
    capability_field: labor_time.trained_role_requirement_status
    pass_condition:
      safety_critical_tasks_have_training_gates: true
      licensed_or_professional_work_not_assigned_to_residents: true
    warn_condition:
      training_gate_unclear_for_sensitive_task: true
    fail_condition:
      safety_critical_task_assigned_to_generic_resident_contribution: true
      licensed_work_assigned_to_residents: true
    promotion_block_condition:
      public_operation_claim_with_untrained_safety_task: true
    source_ids:
      - OSHA_TRAINING_UNDERSTANDABLE
      - OSHA_LOCKOUT_TAGOUT
```

---

## 11. Scenario Requirements

```yaml
scenario_requirements:
  care_health:
    required:
      - injury_event
      - medication_refrigeration_outage
      - illness_wave
      - high_need_evacuation
      - care_steward_exit
      - care_labor_burnout

  governance_anticapture:
    required:
      - member_expulsion_case
      - emergency_power_extension
      - founder_exit
      - admin_capture
      - major_debt_or_land_sale
      - privacy_breach

  mobility_access:
    required:
      - wheelchair_resident_day
      - elder_pharmacy_trip
      - fire_EMS_access
      - route_blockage
      - no_private_car_resident
      - shared_vehicle_failure

  legal_land_finance:
    required:
      - income_loss
      - reserve_drawdown
      - insurance_shock
      - debt_pressure
      - resident_exit
      - land_sale_pressure

  risk_resilience:
    required:
      - water_contamination
      - 72_hour_energy_outage
      - food_disruption
      - illness_wave
      - fire_or_shelter_loss
      - financial_shock
      - compound_heat_grid_outage

  labor_time:
    required:
      - normal_week
      - bad_week
      - hidden_labor_detection
      - care_labor_concentration
      - governance_conflict_month
      - maintenance_emergency
      - scale_80_300_730_1500
```

---

## 12. Automatic Promotion Blockers

```yaml
promotion_blockers:
  - id: no_tested_potable_water_path
    domain: risk_resilience
    severity: block

  - id: no_sanitation_blackwater_plan
    domain: risk_resilience
    severity: block

  - id: no_high_need_support_model
    domain: care_health
    severity: block

  - id: no_accessible_route_to_essentials
    domain: mobility_access
    severity: block

  - id: no_due_process
    domain: governance_anticapture
    severity: block

  - id: no_emergency_power_sunset
    domain: governance_anticapture
    severity: block

  - id: no_written_resident_rights_or_tenure
    domain: legal_land_finance
    severity: block

  - id: reserves_excluded_from_affordability
    domain: legal_land_finance
    severity: block

  - id: no_hazard_register_or_dependency_graph
    domain: risk_resilience
    severity: block

  - id: safety_critical_task_without_training_gate
    domain: labor_time
    severity: block

  - id: clinical_legal_engineering_or_accessibility_claim_without_review
    domain: multiple
    severity: block
```

---

## 13. Viewer Warning Messages

```yaml
viewer_warnings:
  care_no_external_path:
    message: Care room lacks a clear external professional care path. This remains simulation-only.

  medication_unprotected:
    message: Medication continuity is not protected by critical energy, privacy, or pharmacy access.

  illness_wave_unready:
    message: Illness-wave protocol lacks meal delivery, sanitation escalation, or privacy protection.

  governance_due_process_missing:
    message: Commons decision lacks notice, review, appeal, or recordkeeping.

  emergency_power_no_sunset:
    message: Emergency authority has no sunset. Promotion blocked.

  role_concentration:
    message: One person or group controls too many high-power roles.

  accessible_route_gap:
    message: Essential route coverage is below the 100% accessibility target.

  non_driver_exclusion:
    message: Non-drivers cannot access daily needs without informal help.

  tenure_insecure:
    message: Resident rights or land tenure are not explicit enough to pass.

  reserve_shortfall:
    message: Reserves are missing or excluded from affordability. Cost model is not credible.

  hazard_register_missing:
    message: Hazard register or dependency graph is missing. Resilience claim blocked.

  hidden_labor:
    message: Savings appear to depend on hidden or untracked labor.

  free_time_not_proven:
    message: Life burden reduction is not proven because free time or wage-hour reduction is not demonstrated.
```

---

## 14. Suggested Tests

```yaml
tests:
  care_health:
    - test_care_floor_fails_without_external_care_path
    - test_medication_continuity_fails_without_critical_energy
    - test_illness_wave_warns_without_meal_delivery
    - test_high_need_support_requires_coverage_100

  governance:
    - test_due_process_fails_without_notice_review_appeal
    - test_emergency_power_blocks_without_sunset
    - test_role_concentration_fails_when_money_records_conflict_same_person
    - test_sensitive_records_not_public

  mobility:
    - test_accessible_route_coverage_100_green
    - test_coverage_95_warns
    - test_any_essential_route_missing_fails
    - test_non_driver_exclusion_fails

  legal_finance:
    - test_no_written_rights_fails
    - test_reserves_excluded_from_affordability_blocks
    - test_cost_burden_above_50_fails_without_subsidy
    - test_unresolved_review_blocker_blocks_promotion

  risk_resilience:
    - test_no_hazard_register_fails
    - test_dependency_graph_missing_fails
    - test_recovery_playbooks_below_4_fails
    - test_mandatory_hazards_missing_warns
    - test_compound_scenario_required

  labor_time:
    - test_commons_labor_4_to_8_green
    - test_commons_labor_8_to_10_warn
    - test_commons_labor_above_12_fail
    - test_hidden_labor_untracked_fails
    - test_free_time_gain_required_for_life_burden_claim
```

---

## 15. Implementation Order

```yaml
phase_1_schema:
  - add capability_policy.schema.json
  - add capability_policies/ciac_capability_policy_v0.yaml
  - validate static policy file

phase_2_loader:
  - add ciac/capability_policy.py
  - load policy
  - expose domain gates
  - connect source IDs

phase_3_gate_engine:
  - update capability_gate to use policy gates
  - preserve existing v0 hardcoded gates as fallback
  - add pass/warn/fail/promotion_block states

phase_4_scenarios:
  - add capability scenario files
  - add scenario coverage report
  - connect mandatory scenarios to promotion gate

phase_5_viewer:
  - add warning mappings
  - display promotion_blocked vs simulation_only
  - show source IDs on evidence cards

phase_6_tests:
  - add tests listed above
  - ensure no existing tests regress
```

---

## 16. Status

```yaml
status: ready_for_policy_translation
not_yet:
  - final verified capability policy
  - legal review
  - medical review
  - accessibility review
  - labor/employment review
  - emergency management review

next_recommended_artifact:
  - capability_policy_v0_execution_plan.md
```
