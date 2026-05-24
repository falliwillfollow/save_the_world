# CIaC Capability Thresholds Research Pack, Part 1

**Research ID:** `ciac_capability_thresholds_research_pack_part_1_v0_1`  
**Purpose:** Convert the second research pack questions into provisional model logic for `CapabilityState`, capability gates, scenario tests, world viewer warnings, and future `capability_policy_v0.yaml`.  
**Status:** Research synthesis only. This is not legal, medical, clinical, accessibility, engineering, employment, finance, or emergency-management certification.

---

## 0. Report Format

Each answer uses:

```yaml
capability_field_addressed:
recommended_threshold:
required_structure_module:
required_operating_protocol:
labor_impact:
resource_impact:
failure_modes:
external_review_needed:
simulation_scenarios_to_test:
source_quality_confidence:
source_ids:
```

---

## 1. Source Registry

```yaml
source_registry:
  - id: CDC_DISABILITY_EMERGENCY_KIT
    title: Building an Emergency Kit for People with Disabilities
    url: https://www.cdc.gov/disability-emergency-preparedness/people-with-disabilities/build-a-kit.html
    supports:
      - one_week_prescription_medication_supply
      - cooler_for_refrigerated_medications
      - batteries_chargers_assistive_devices
      - mobility_devices_and_health_documents

  - id: CDC_RESPIRATORY_PREVENTION
    title: Preventing Respiratory Illnesses
    url: https://www.cdc.gov/respiratory-viruses/prevention/index.html
    supports:
      - stay_home_when_sick
      - hygiene
      - cleaner_air
      - masks_as_layered_protection

  - id: HRSA_HEALTH_CENTER_PROGRAM
    title: About the Health Center Program
    url: https://bphc.hrsa.gov/about-health-center-program
    supports:
      - external_professional_care_interface
      - community_based_medical_dental_behavioral_vision_services

  - id: CDC_CHW_CHRONIC_CARE
    title: Emerging Model for Community Health Worker-Based Chronic Care Management
    url: https://www.cdc.gov/pcd/issues/2020/19_0316.htm
    supports:
      - nonclinical_care_navigation
      - community_health_worker_support

  - id: IMPACT_CHW_RCT
    title: Evidence-Based Community Health Worker Program Addresses Unmet Social Needs
    url: https://pmc.ncbi.nlm.nih.gov/articles/PMC8564553/
    supports:
      - structured_CHW_support
      - unmet_social_needs_support

  - id: FEMA_ICS_SPAN_CONTROL
    title: ICS Principle, Manageable Span of Control
    url: https://emilms.fema.gov/is_0362a/groups/103.html
    supports:
      - incident_supervisor_span_3_to_7
      - five_as_operational_rule_of_thumb

  - id: CORNELL_PROCEDURAL_DUE_PROCESS
    title: Procedural Due Process
    url: https://www.law.cornell.edu/wex/procedural_due_process
    supports:
      - notice
      - neutral_tribunal
      - opportunity_to_respond
      - evidence_access
      - right_to_present_evidence

  - id: NIST_PRIVACY_FRAMEWORK
    title: NIST Privacy Framework
    url: https://www.nist.gov/privacy-framework
    supports:
      - privacy_risk_management
      - role_based_data_governance

  - id: GSN_CLT
    title: Community Land Trusts
    url: https://groundedsolutions.org/strengthening-neighborhoods/community-land-trusts/
    supports:
      - community_land_stewardship
      - permanent_affordability
      - resale_restriction

  - id: GSN_RESALE_FORMULAS
    title: Affordable Pricing and Resale Formulas
    url: https://groundedsolutions.org/resources/affordable-pricing-and-resale-formulas/
    supports:
      - resale_formula_preserves_affordability

  - id: LOCAL_HOUSING_SOLUTIONS_LEC
    title: Limited Equity Cooperatives
    url: https://www.localhousingsolutions.org/housing-policy-library/limited-equity-cooperatives/
    supports:
      - limited_equity_coop_resale_formula
      - affordability_preservation

  - id: HUD_CHAS_COST_BURDEN
    title: CHAS Background
    url: https://www.huduser.gov/portal/datasets/cp/CHAS/bg_chas.html
    supports:
      - housing_cost_burden_above_30_percent_income
      - severe_cost_burden_above_50_percent_income

  - id: IRS_501C3_ORGANIZATIONAL_TEST
    title: Organizational Test, IRC Section 501(c)(3)
    url: https://www.irs.gov/charities-non-profits/charitable-organizations/organizational-test-internal-revenue-code-section-501c3
    supports:
      - assets_permanently_dedicated_to_exempt_purpose
      - dissolution_assets_not_private_distribution

  - id: NIST_COMMUNITY_RESILIENCE_GUIDE
    title: Community Resilience Planning Guide
    url: https://www.nist.gov/community-resilience/planning-guide
    supports:
      - critical_social_functions
      - infrastructure_dependencies
      - recovery_goals

  - id: FEMA_NATIONAL_RESILIENCE_GUIDANCE
    title: National Resilience Guidance
    url: https://www.fema.gov/emergency-managers/national-preparedness/plan/resilience-guidance
    supports:
      - whole_community_resilience
      - resilience_planning

  - id: SENDAI_FRAMEWORK
    title: Sendai Framework for Disaster Risk Reduction 2015-2030
    url: https://www.undrr.org/publication/sendai-framework-disaster-risk-reduction-2015-2030
    supports:
      - understand_disaster_risk
      - risk_governance
      - recovery_preparedness

  - id: ITDP_TOD_STANDARD
    title: TOD Standard
    url: https://tod.itdp.org/tod-standard/tod-standard-framework.html
    supports:
      - 500_meter_frequent_transit_reference
      - walk_cycle_connect_transit_logic

  - id: ACCESS_BOARD_ACCESSIBLE_ROUTES
    title: ADA Guide, Accessible Routes
    url: https://www.access-board.gov/ada/guides/chapter-4-accessible-routes/
    supports:
      - accessible_route_requirements
      - route_width_and_clearance_logic

  - id: BLS_ATUS_2024
    title: American Time Use Survey, 2024 Results
    url: https://www.bls.gov/news.release/atus.nr0.htm
    supports:
      - paid_work
      - household_activities
      - care_activities
      - leisure_time
      - gender_distribution_of_household_labor

  - id: WHO_ILO_LONG_WORKING_HOURS
    title: Long working hours increasing deaths from heart disease and stroke
    url: https://www.who.int/news/item/17-05-2021-long-working-hours-increasing-deaths-from-heart-disease-and-stroke-who-ilo
    supports:
      - 55_plus_hours_per_week_health_risk
      - long_working_hours_stroke_heart_disease_burden

  - id: OECD_WORK_LIFE_BALANCE
    title: OECD Better Life Index, Work-Life Balance
    url: https://oecd-better-life-index.truth-and-beauty.net/topics/work-life-balance/
    supports:
      - leisure_and_personal_care_as_wellbeing_metrics

  - id: UKRI_FOUR_DAY_WEEK
    title: Four-day working week improves mental and physical health
    url: https://www.ukri.org/who-we-are/how-we-are-doing/research-outcomes-and-impact/esrc/a-four-day-working-week-improves-mental-and-physical-health/
    supports:
      - reduced_hours_lower_stress_burnout
      - reduced_work_time_can_preserve_productivity
```

---

# CARE HEALTH

## 2. Minimum Non-Clinical Care Support Floor

```yaml
domain: care_health
question: What minimum care-support functions should a dignified small community provide without becoming an unlicensed clinic?

capability_field_addressed:
  - care_health.nonclinical_care_floor
  - care_health.external_care_path
  - care_health.clinical_boundary_status

recommended_threshold:
  green:
    - private care room
    - first aid station
    - medication continuity plan
    - refrigerated medication backup if needed
    - care meal protocol
    - transport-to-care plan
    - external clinic/pharmacy/EMS relationships
    - no diagnosis or treatment claims by non-clinical residents
  warn:
    - care room exists but no backup steward
    - external care path unclear
    - care support depends on informal relationships
  fail:
    - settlement claims to replace professional care
    - no private care space
    - no medication continuity
    - no transport-to-care plan

required_structure_module:
  - care_room
  - first_aid_station
  - telehealth_private_space
  - medication_refrigeration_point
  - emergency_charging_point
  - care_meal_pickup_or_delivery_path
  - external_healthcare_registry

required_operating_protocol:
  - nonclinical_support_scope
  - emergency_escalation
  - privacy_and_consent
  - care_request_intake
  - pharmacy_pickup_or_delivery
  - medication_cold_chain
  - care_meal_activation
  - incident_log

labor_impact:
  - requires care steward and backup
  - routine care burden should target 0.5 to 2 hours per resident per week
  - sustained high-need support should trigger paid or external support

resource_impact:
  - small room
  - critical energy for refrigeration/devices
  - first aid/PPE/cleaning supplies
  - transport capacity
  - privacy-preserving records

failure_modes:
  - unlicensed clinic drift
  - hidden care labor
  - public disclosure of health needs
  - medication failure during outage
  - no transportation to professional care

external_review_needed:
  - medical/legal boundary review
  - privacy review
  - liability/insurance review
  - EMS/fire access review

simulation_scenarios_to_test:
  - injury_event
  - elder_high_need_week
  - medication_refrigeration_outage
  - transport_to_care_failure
  - care_steward_exit
  - illness_wave

source_quality_confidence:
  evidence_quality: moderate
  translation_confidence: moderate
  regulatory_strength: professional_practice

source_ids:
  - CDC_DISABILITY_EMERGENCY_KIT
  - HRSA_HEALTH_CENTER_PROGRAM
  - CDC_CHW_CHRONIC_CARE
  - IMPACT_CHW_RCT
```

---

## 3. High-Need Support Coverage

```yaml
domain: care_health
question: What ratio or coverage threshold is reasonable for high-need support planning?

capability_field_addressed:
  - care_health.high_need_support_coverage
  - care_health.function_based_registry
  - labor_time.care_labor_concentration

recommended_threshold:
  green:
    coverage: 100_percent_of_opt_in_or_known_high_need_residents_have_function_based_support_plan
    backup: each_support_plan_has_primary_and_backup_role
    privacy: support_need_recorded_by_function_not_public_diagnosis
  warn:
    - coverage_below_100_percent
    - no backup
    - same small group supports majority of needs
  fail:
    - high-need residents not modeled
    - no accessible evacuation plan
    - medication/device power needs unmodeled
    - support requires public diagnosis disclosure

required_structure_module:
  - privacy_limited_high_need_registry
  - care_room
  - medication_backup
  - mobility_access_support
  - emergency_charging_station
  - care_meal_delivery_path

required_operating_protocol:
  - voluntary/function-based disclosure
  - role-based access controls
  - backup support assignment
  - periodic review
  - no public dashboard of diagnoses

labor_impact:
  - high-need support labor must be tracked separately
  - repeated support over target triggers external support
  - backup roles required

resource_impact:
  - energy for devices/refrigeration
  - accessible transport
  - food/water delivery
  - privacy-protected records

failure_modes:
  - high-need residents invisible
  - privacy breach
  - one informal helper becomes care system
  - evacuation failure
  - medication failure

external_review_needed:
  - disability/accessibility review
  - privacy review
  - emergency management review
  - clinical review for medically complex needs

simulation_scenarios_to_test:
  - power_outage_with_medical_devices
  - evacuation_event
  - medication_disruption
  - caregiver_burnout
  - illness_wave

source_quality_confidence:
  evidence_quality: high
  translation_confidence: moderate
  regulatory_strength: guideline

source_ids:
  - CDC_DISABILITY_EMERGENCY_KIT
  - FEMA_NATIONAL_RESILIENCE_GUIDANCE
  - NIST_COMMUNITY_RESILIENCE_GUIDE
```

---

## 4. Care Meal Protocol

```yaml
domain: care_health
question: What should a care meal protocol include for illness, injury, disability, postpartum, elder support, and recovery periods?

capability_field_addressed:
  - care_health.care_meal_protocol
  - labor_time.care_meal_labor
  - food.care_meal_delivery

recommended_threshold:
  green:
    - activation triggers defined
    - dietary/allergen constraints captured privately
    - delivery route defined
    - food safety rules defined
    - labor assigned and tracked
    - backup cook/delivery role exists
    - opt-out and private food autonomy preserved
  warn:
    - relies on informal goodwill
    - no allergen protocol
    - no delivery backup
  fail:
    - sick/injured/high-need residents must attend common meals to be fed
    - care meal labor untracked
    - allergen risk unmanaged

required_structure_module:
  - meal_support_kitchen_or_food_commons_interface
  - care_meal_delivery_bins
  - allergen/dietary registry with privacy
  - delivery route to unit/pod
  - cleaning and container return station

required_operating_protocol:
  - triggers: illness, injury, surgery recovery, disability flare, elder need, postpartum, grief, caregiver overload
  - intake: dietary restrictions, delivery needs, duration
  - food safety: time/temperature, labeling, cleaning, allergen separation
  - schedule: who cooks, delivers, cleans
  - defined renewal/closure

labor_impact:
  - moderate surge labor during care events
  - counted as care labor, not social generosity
  - repeated use triggers care steward review

resource_impact:
  - prepared meals
  - delivery containers
  - kitchen time
  - cleaning/sanitizing
  - food inventory buffer

failure_modes:
  - hidden gendered care labor
  - dietary/allergen failure
  - foodborne illness risk
  - shame around requesting meals
  - no backup during illness wave

external_review_needed:
  - food safety review if scale/vulnerability warrants
  - dietitian/clinician review for prescribed diets

simulation_scenarios_to_test:
  - illness_week
  - postpartum_recovery
  - elder_support_week
  - caregiver_overload
  - food_commons_labor_shortage
  - allergen_event

source_quality_confidence:
  evidence_quality: moderate
  translation_confidence: moderate
  regulatory_strength: professional_practice

source_ids:
  - CDC_DISABILITY_EMERGENCY_KIT
  - CDC_CHW_CHRONIC_CARE
```

---

## 5. Illness-Wave Protocol

```yaml
domain: care_health
question: What should an illness-wave protocol require?

capability_field_addressed:
  - care_health.illness_wave_protocol
  - sanitation_waste.cleaning_escalation
  - labor_time.illness_wave_labor
  - food.care_meal_delivery

recommended_threshold:
  green:
    - stay-home/support protocol
    - meal delivery
    - cleaning/sanitation escalation
    - medication continuity check
    - cleaner-air or ventilation strategy
    - high-need residents protected
    - staffing backup active
    - privacy preserved
  warn:
    - no cleaner-air layer
    - no backup labor
    - no care-meal scaling plan
  fail:
    - public diagnosis disclosure required
    - symptomatic residents must attend common meals
    - no cleaning escalation
    - no high-need protection
    - no medication continuity

required_structure_module:
  - care room or recovery support space
  - meal delivery system
  - cleaning supply/PPE station
  - hand hygiene points
  - medication backup
  - communication tree

required_operating_protocol:
  - illness trigger thresholds
  - stay-home support
  - delivery to units/pods
  - common meal modification
  - cleaning escalation
  - masking/ventilation guidance where appropriate
  - care steward backup
  - after-action review

labor_impact:
  - care, food, sanitation, and communication labor surge
  - same-group overload should trigger warn/fail
  - prolonged surge triggers external support

resource_impact:
  - food delivery inventory
  - PPE/cleaning supplies
  - critical energy for care/meds
  - communications
  - possible portable filtration/ventilation

failure_modes:
  - illness spreads through common meals
  - sick residents punished socially
  - cleaning labor hidden
  - high-need residents exposed
  - privacy breach
  - care steward burnout

external_review_needed:
  - public health guidance check
  - clinician review for high-risk populations
  - workplace/food safety review if staff/paid roles exist

simulation_scenarios_to_test:
  - respiratory_illness_wave
  - gastrointestinal_illness_wave
  - care_steward_sick
  - common_kitchen_reduced_labor
  - high_need_resident_exposure

source_quality_confidence:
  evidence_quality: high
  translation_confidence: moderate
  regulatory_strength: guideline

source_ids:
  - CDC_RESPIRATORY_PREVENTION
  - CDC_DISABILITY_EMERGENCY_KIT
```

---

## 6. Care Steward Labor Burden

```yaml
domain: care_health
question: What labor burden is acceptable for care stewards before professional or external support is required?

capability_field_addressed:
  - labor_time.care_labor_hours
  - care_health.care_steward_capacity
  - care_health.external_support_trigger

recommended_threshold:
  green:
    routine_care_labor_per_resident_per_week: 0.5_to_2_hours
    volunteer_care_steward_hours_per_week: under_5_to_8_hours
    backup_coverage: 100_percent_for_core_roles
  warn:
    routine_care_labor_per_resident_per_week: above_3_hours
    volunteer_care_steward_hours_per_week: above_8_hours
    same_people_do_majority_of_care: true
  fail:
    routine_care_labor_per_resident_per_week: above_5_hours_without_paid_or_external_support
    care_steward_no_backup: true
    high_need_support_unfilled: true
    care_labor_untracked: true

required_structure_module:
  - labor ledger
  - care steward rota
  - backup steward role
  - external care partner list
  - privacy-limited care task queue

required_operating_protocol:
  - weekly labor review
  - burnout trigger
  - paid/external support escalation
  - respite and role rotation
  - confidential accommodation process

labor_impact:
  - care labor is high-risk hidden labor
  - should be tracked separately from generic commons contribution
  - repeated overload should pause optional projects

resource_impact:
  - possible paid support budget
  - transport budget
  - care supplies
  - food and cleaning buffers

failure_modes:
  - empathetic residents become invisible care system
  - gendered care burden
  - burnout
  - high-need residents neglected
  - privacy compromised by informal coordination

external_review_needed:
  - clinical/home-care review for sustained high-need support
  - employment/labor review if care roles become paid
  - liability review

simulation_scenarios_to_test:
  - caregiver_burnout
  - elder_support_gap
  - illness_wave
  - injury_recovery
  - paid_support_activation

source_quality_confidence:
  evidence_quality: moderate
  translation_confidence: low_to_moderate
  regulatory_strength: heuristic

source_ids:
  - BLS_ATUS_2024
  - CDC_CHW_CHRONIC_CARE
  - IMPACT_CHW_RCT
  - WHO_ILO_LONG_WORKING_HOURS
```

---


# GOVERNANCE

## 7. Minimum Due-Process Structure

```yaml
domain: governance
question: What minimum due-process structure is needed for commons decisions?

capability_field_addressed:
  - governance_anticapture.due_process_status
  - governance_anticapture.decision_legitimacy
  - governance_anticapture.appeal_path

recommended_threshold:
  green:
    - written notice
    - stated reasons
    - evidence access where safe
    - opportunity to respond
    - impartial review
    - recusal/conflict-of-interest rule
    - decision record
    - appeal or reconsideration path
    - external review trigger for serious cases
  warn:
    - no appeal path
    - recusal rule missing
    - records incomplete
  fail:
    - expulsion or loss of access without notice/review
    - one clique controls review
    - no written decision
    - retaliation against complainants

required_structure_module:
  - decision log
  - policy registry
  - conflict/safeguarding process
  - recusal and conflict-of-interest rule
  - appeal panel or external mediation path

required_operating_protocol:
  - ordinary issue path
  - serious harm path
  - emergency temporary action path
  - recusal policy
  - records and privacy classification
  - appeal or review timeline

labor_impact:
  - moderate governance labor
  - reduces conflict/capture risk
  - should not require full assembly for every case

resource_impact:
  - records system
  - private meeting space
  - possible external mediation/legal budget

failure_modes:
  - mob decision
  - founder/clique capture
  - procedural opacity
  - records used for social punishment
  - conflict process replaces safety process

external_review_needed:
  - legal review for occupancy/membership/expulsion
  - safeguarding review for abuse/harassment
  - mediation/legal review for serious disputes

simulation_scenarios_to_test:
  - member_expulsion_case
  - conflict_month
  - harassment_case
  - role_abuse
  - emergency_temporary_restriction
  - appeal_case

source_quality_confidence:
  evidence_quality: moderate
  translation_confidence: moderate
  regulatory_strength: research_inferred_to_legal_principle

source_ids:
  - CORNELL_PROCEDURAL_DUE_PROCESS
  - NIST_PRIVACY_FRAMEWORK
```

---

## 8. Emergency Powers and Sunset Periods

```yaml
domain: governance
question: What emergency powers are legitimate in a small community, and what sunset periods are defensible?

capability_field_addressed:
  - governance_anticapture.emergency_power_sunset
  - risk_resilience.emergency_mode_status
  - governance_anticapture.audit_log_status

recommended_threshold:
  green:
    emergency_power_scope: narrow_and_predefined
    default_sunset: 72_hours
    extension: requires documented reason, resident notification, and review
    incident_log: required
    after_action_review: required
  warn:
    - extension beyond 72 hours without member notice
    - emergency role no backup
  fail:
    - emergency power has no sunset
    - emergency power can change constitutional rules
    - emergency power can remove opponents or transfer assets
    - no incident log

required_structure_module:
  - emergency roles
  - authority limits
  - incident log
  - communication tree
  - sunset clock
  - after-action review

required_operating_protocol:
  - mode activation triggers
  - 72-hour default review
  - extension approval path
  - external authority contact
  - deactivation and recovery process

labor_impact:
  - emergency role surge
  - crisis communication burden
  - after-action review time
  - must be followed by recovery/rest period

resource_impact:
  - communications
  - emergency supplies
  - records
  - possible legal/insurance support

failure_modes:
  - emergency authoritarianism
  - permanent rule drift
  - asset capture during crisis
  - no record of actions
  - exhausted emergency team

external_review_needed:
  - emergency management review
  - legal review for authority over occupancy/access
  - insurance/liability review

simulation_scenarios_to_test:
  - 72_hour_grid_outage
  - water_contamination
  - illness_wave
  - emergency_power_extension
  - emergency_power_abuse_attempt

source_quality_confidence:
  evidence_quality: moderate
  translation_confidence: moderate
  regulatory_strength: heuristic_with_emergency_management_support

source_ids:
  - FEMA_ICS_SPAN_CONTROL
  - FEMA_NATIONAL_RESILIENCE_GUIDANCE
  - SENDAI_FRAMEWORK
```

---

## 9. Role Backup Ratio and Anti-Capture

```yaml
domain: governance
question: What role-backup ratio prevents capture or single-point authority?

capability_field_addressed:
  - governance_anticapture.role_backup_coverage
  - governance_anticapture.role_concentration_score
  - risk_resilience.single_point_authority

recommended_threshold:
  green:
    critical_roles_with_backup: 100_percent
    high_power_functions_separated: true
    same_person_controls_money_records_conflict_or_membership: false
    emergency_roles_have_backups: true
  warn:
    - critical roles with backup below 100 percent
    - one person holds two high-power roles
  fail:
    - one person controls money, records, conflict process, or survival access
    - emergency role has no backup
    - data/admin credentials controlled by one person

required_structure_module:
  - role registry
  - backup role registry
  - conflict-of-interest disclosures
  - access control
  - succession plan
  - audit/review cycle

required_operating_protocol:
  - term/review cycle
  - backup training
  - credential escrow or shared admin access
  - recusal
  - role concentration audit

labor_impact:
  - training and role-shadowing burden
  - reduced emergency burden
  - reduces founder/expert dependency

resource_impact:
  - documentation system
  - access control system
  - training time
  - external audit/review where needed

failure_modes:
  - founder capture
  - administrator capture
  - expert capture
  - one-person emergency plan
  - lost credentials or institutional memory

external_review_needed:
  - legal/accounting review for money roles
  - privacy/security review for data roles
  - governance consultant or mediator for high-conflict systems

simulation_scenarios_to_test:
  - founder_exit
  - admin_capture
  - finance_steward_exit
  - conflict_steward_conflict_of_interest
  - emergency_lead_unavailable

source_quality_confidence:
  evidence_quality: moderate
  translation_confidence: moderate
  regulatory_strength: professional_practice

source_ids:
  - FEMA_ICS_SPAN_CONTROL
  - NIST_PRIVACY_FRAMEWORK
```

---

## 10. Decision Authority and Records

```yaml
domain: governance
question: Which decisions require resident consent, supermajority, external review, immediate authority, and what records must be public/private/anonymized?

capability_field_addressed:
  - governance_anticapture.decision_domain_clarity
  - governance_anticapture.records_transparency
  - governance_anticapture.privacy_classification

recommended_threshold:
  green:
    operational_decisions: delegated roles/circles
    policy_decisions: domain circle consent with review
    budget_decisions: finance circle plus member thresholds
    constitutional_decisions: resident vote/supermajority
    land_asset_debt_decisions: supermajority plus external review
    emergency_decisions: narrow authority with sunset
    public_to_members:
      - budgets
      - reserve status
      - maintenance backlog
      - role registry
      - policy registry
      - non-sensitive decision log
    private_role_limited:
      - health/support details
      - conflict details
      - financial hardship
      - legal matters
      - credentials
    anonymized:
      - high-need support coverage
      - care labor burden
      - social isolation signals
      - affordability stress
  warn:
    - decision domains unclear
    - no retention policy
    - no role-based access
  fail:
    - land sale, major debt, expulsion, or asset transfer possible by ordinary role decision
    - health/conflict/financial hardship public by default
    - common-power records hidden

required_structure_module:
  - decision domain registry
  - records classification policy
  - role-based access
  - audit log
  - external review trigger registry

required_operating_protocol:
  - classify decision
  - route to correct authority
  - classify record at creation
  - review/appeal where applicable
  - resident access to own records
  - privacy breach response

labor_impact:
  - admin burden
  - reduces meeting burden by routing routine decisions
  - prevents gossip governance

resource_impact:
  - records software
  - secure storage
  - legal/accounting review budget

failure_modes:
  - surveillance commons
  - budget opacity
  - health disclosure
  - emergency bypass
  - high-stakes decisions made casually

external_review_needed:
  - legal review for land/debt/tenure/expulsion
  - privacy/security review
  - accounting review

simulation_scenarios_to_test:
  - major_debt_proposal
  - land_sale_pressure
  - privacy_breach
  - budget_opacity
  - admin_exit_with_credentials

source_quality_confidence:
  evidence_quality: moderate
  translation_confidence: moderate
  regulatory_strength: professional_practice

source_ids:
  - CORNELL_PROCEDURAL_DUE_PROCESS
  - NIST_PRIVACY_FRAMEWORK
  - GSN_RESALE_FORMULAS
```

---


# MOBILITY

## 11. Complete Accessible-Route Coverage

```yaml
domain: mobility_access
question: What counts as complete accessible-route coverage between housing, food, care, sanitation, water, governance, and emergency access?

capability_field_addressed:
  - mobility_access.accessible_route_coverage
  - mobility_access.essential_access_status
  - care_health.high_need_access

recommended_threshold:
  green:
    essential_accessible_route_coverage: 100_percent
    essential_spaces:
      - housing
      - food commons
      - care room
      - toilets/bathing/laundry
      - potable water points
      - emergency pickup
      - governance/common house
      - safe room
      - resident-facing waste/sanitation dropoff
  warn:
    - coverage 95 to 99 percent
    - accessible route much longer than primary route
  fail:
    - any essential space lacks accessible route
    - emergency route inaccessible
    - high-need access depends on informal help

required_structure_module:
  - accessible route map
  - surface/grade/width metadata
  - emergency access map
  - rest point map
  - route maintenance protocol

required_operating_protocol:
  - accessibility audit
  - route inspection
  - weather clearance
  - route blockage reporting
  - high-need resident access review

labor_impact:
  - route inspection and maintenance labor
  - weather clearing labor
  - accessible detour management

resource_impact:
  - paths/surfaces
  - lighting
  - benches/rest nodes
  - drainage
  - snow/ice tools where relevant

failure_modes:
  - second-class accessible route
  - route blocked during emergency
  - food/care/water unreachable
  - path maintenance ignored
  - stairs become hidden gate

external_review_needed:
  - accessibility professional/code review
  - civil/landscape review
  - fire/EMS access review
  - insurance/liability review

simulation_scenarios_to_test:
  - wheelchair_resident_day
  - elder_high_need_day
  - storm_route_blockage
  - nighttime_care_access
  - evacuation
  - food_delivery_to_high_need_resident

source_quality_confidence:
  evidence_quality: high
  translation_confidence: high_for_coverage_requirement
  regulatory_strength: binding_or_guideline_depending_context

source_ids:
  - ACCESS_BOARD_ACCESSIBLE_ROUTES
```

---

## 12. Max Distance and Time to Daily Needs

```yaml
domain: mobility_access
question: What max distance/time to daily needs is reasonable for non-drivers, elders, disabled residents, and children?

capability_field_addressed:
  - mobility_access.daily_need_distance
  - mobility_access.non_driver_dignity
  - labor_time.errand_time_burden

recommended_threshold:
  green:
    1_minute:
      - safe exit
      - immediate high-need hygiene/help where relevant
    3_minutes:
      - pod commons
      - accessible dropoff
      - emergency water distribution
      - high-need care support where possible
    5_minutes:
      - food commons or pickup
      - laundry
      - quiet room
      - tool cache
      - primary common house/social node
      - garden access
    10_minutes:
      - transit/shuttle stop
      - district commons
      - larger workshop
  warn:
    - essentials above 5 minutes for high-need residents
    - transit/shuttle above 10 minutes
  fail:
    - non-drivers cannot access food/care/pharmacy/clinic
    - daily needs require private car

required_structure_module:
  - distance/friction calculator
  - accessible route map
  - neighborhood centers
  - shuttle/cart/shared vehicle where needed
  - service radius dashboard

required_operating_protocol:
  - periodic route audit
  - care transport plan
  - grocery/pharmacy/clinic trip protocol
  - high-need access review
  - route closure fallback

labor_impact:
  - reduced errand burden if local
  - shuttle/cart operation burden if not local
  - care transport labor must be tracked

resource_impact:
  - paths
  - covered routes
  - carts/bikes/shared vehicles
  - route lighting
  - seating/rest points

failure_modes:
  - cheap land creates transport poverty
  - high-need residents stranded
  - accessible route too long
  - informal driver dependency
  - transportation cost erases housing savings

external_review_needed:
  - accessibility review
  - transportation planning review
  - insurance review for shared vehicles
  - local transit/shuttle partner review

simulation_scenarios_to_test:
  - no_private_car_resident
  - elder_pharmacy_trip
  - care_transport_failure
  - weather_blocked_route
  - shared_vehicle_unavailable
  - scale_to_730_transport_burden

source_quality_confidence:
  evidence_quality: moderate
  translation_confidence: moderate
  regulatory_strength: heuristic_with_TOD_and_accessibility_support

source_ids:
  - ITDP_TOD_STANDARD
  - ACCESS_BOARD_ACCESSIBLE_ROUTES
```

---

## 13. Emergency Responder Access Without Car-Centric Design

```yaml
domain: mobility_access
question: What emergency vehicle or emergency responder access is required without making the whole plan car-centric?

capability_field_addressed:
  - mobility_access.emergency_access_status
  - risk_resilience.evacuation_access
  - care_health.EMS_access

recommended_threshold:
  green:
    - fire/EMS access reviewed
    - emergency pickup points mapped
    - pedestrian core protected from routine through-traffic
    - service/emergency routes separated where possible
    - accessible evacuation route exists
    - high-need transport plan exists
  warn:
    - emergency route doubles as main social courtyard
    - no backup route
    - no route clearance role
  fail:
    - fire/EMS route unreviewed
    - no emergency pickup point
    - no high-need evacuation plan
    - pedestrian-only design blocks emergency response

required_structure_module:
  - emergency route map
  - pickup/dropoff points
  - service edge
  - route clearance plan
  - high-need transport plan
  - emergency access dashboard

required_operating_protocol:
  - fire/EMS review
  - route clearance assignment
  - severe weather clearance
  - evacuation drill
  - shared vehicle/fuel/charge readiness

labor_impact:
  - emergency route checks
  - route clearance during weather
  - evacuation support labor
  - drill labor

resource_impact:
  - reinforced paths or access roads
  - signage/lighting
  - emergency communication
  - accessible vehicles/carts

failure_modes:
  - car-free ideology blocks EMS
  - emergency route used for parking/storage
  - high-need residents left behind
  - service vehicles dominate social core

external_review_needed:
  - fire marshal / EMS review
  - civil engineer review
  - accessibility review
  - insurance/liability review

simulation_scenarios_to_test:
  - ambulance_to_care_room
  - fire_access_blocked
  - flood_route_closure
  - high_need_evacuation
  - snow_or_debris_blockage

source_quality_confidence:
  evidence_quality: moderate
  translation_confidence: moderate
  regulatory_strength: binding_or_professional_review_depending_jurisdiction

source_ids:
  - FEMA_NATIONAL_RESILIENCE_GUIDANCE
  - ACCESS_BOARD_ACCESSIBLE_ROUTES
```

---

## 14. Route Quality and Mobility Support Modules

```yaml
domain: mobility_access
question: What surface, grade, lighting, rest-point, weather, width, and support modules should the model track?

capability_field_addressed:
  - mobility_access.route_quality_score
  - mobility_access.support_module_coverage
  - mobility_access.green_status

recommended_threshold:
  green:
    essential_accessible_route_coverage: 100_percent
    emergency_route_coverage: 100_percent
    route_map_exists: true
    care_transport_plan_exists: true
    rest_nodes_present: true
    repair_protocol_exists: true
    route_surface: firm_stable_slip_resistant
    primary_routes_lit: true
  warn:
    - coverage 95 to 99 percent
    - no rest nodes
    - no shuttle/cart backup
    - route repair backlog
    - accessible route penalty
  fail:
    - essential accessible route coverage below 95 percent
    - no emergency route
    - no care transport
    - no non-driver support where external access is car-dependent

required_structure_module:
  - route map
  - shuttle/cart/shared vehicle node
  - covered paths where climate requires
  - rest nodes
  - mobility repair protocol
  - bike/cart storage
  - emergency access dashboard

required_operating_protocol:
  - booking/checkout for shared mobility
  - maintenance schedule
  - driver/operator rules
  - high-need request protocol
  - incident reporting
  - route repair work orders

labor_impact:
  - mobility steward labor
  - path maintenance labor
  - driver/shuttle labor
  - repair labor

resource_impact:
  - carts/bikes/shared vehicles
  - charging/fuel
  - storage
  - insurance
  - path and lighting maintenance

failure_modes:
  - mobility devices unavailable
  - informal driver dependency
  - carts broken/no maintenance
  - no covered/rest route for high-need residents
  - shared vehicle uninsured

external_review_needed:
  - insurance review
  - accessibility review
  - vehicle/shuttle legal review
  - employment review for drivers if paid/staffed

simulation_scenarios_to_test:
  - shared_cart_failure
  - driver_unavailable
  - wheelchair_route_blocked
  - clinic_trip
  - medicine_pickup
  - scale_to_730_transport_burden

source_quality_confidence:
  evidence_quality: moderate
  translation_confidence: moderate
  regulatory_strength: heuristic_with_accessibility_support

source_ids:
  - ACCESS_BOARD_ACCESSIBLE_ROUTES
  - CDC_DISABILITY_EMERGENCY_KIT
```

---


# LEGAL / LAND / FINANCE

## 15. Tenure Models and Resident Rights

```yaml
domain: legal_land_finance
question: What tenure models best preserve resident security, prevent speculative capture, and what minimum resident rights should be explicit before pass?

capability_field_addressed:
  - legal_land_finance.land_security_status
  - legal_land_finance.anti_speculation_status
  - legal_land_finance.resident_rights_status

recommended_threshold:
  green:
    - mission-locked land or CLT-like stewardship
    - written resident occupancy/use rights
    - limited-equity or resale formula where equity exists
    - due process before loss of access
    - asset lock or transfer restrictions
    - explicit privacy, repair request, participation, exit, accommodation, anti-retaliation, financial privacy, and conflict process
    - external legal review
  warn:
    - founder/investor land ownership
    - exit formula unclear
    - hardship process unclear
    - rights exist only in prose
  fail:
    - no secure land control
    - residents have no written use rights
    - core assets can be sold for private gain without review
    - loss of housing/access by founder or clique discretion
    - uncapped appreciation destroys future affordability

required_structure_module:
  - land stewardship entity
  - resident housing/use-right entity
  - operating commons entity
  - asset lock
  - resale/exit formula
  - resident rights document
  - due-process policy

required_operating_protocol:
  - onboarding legal rights summary
  - transfer/resale process
  - exit process
  - member review for land/debt/asset decisions
  - hardship and appeal process

labor_impact:
  - legal/admin role burden
  - records steward needed
  - external professional coordination
  - reduces displacement uncertainty

resource_impact:
  - legal costs
  - accounting costs
  - reserves
  - insurance
  - administrative records

failure_modes:
  - land becomes landlord
  - founder capture
  - investor capture
  - debt default forces sale
  - residents lose access without process

external_review_needed:
  - attorney
  - housing/cooperative/CLT counsel
  - tax advisor
  - lender/underwriter
  - insurance broker

simulation_scenarios_to_test:
  - founder_exit
  - land_sale_pressure
  - resident_exit
  - debt_pressure
  - investor_capture_attempt
  - dissolution
  - payment_hardship
  - accommodation_request

source_quality_confidence:
  evidence_quality: moderate
  translation_confidence: high
  regulatory_strength: legal_review_required

source_ids:
  - GSN_CLT
  - GSN_RESALE_FORMULAS
  - LOCAL_HOUSING_SOLUTIONS_LEC
  - IRS_501C3_ORGANIZATIONAL_TEST
  - CORNELL_PROCEDURAL_DUE_PROCESS
```

---

## 16. Reserves, Affordability, and Anti-Displacement

```yaml
domain: legal_land_finance
question: What reserves, affordability thresholds, and anti-displacement protections should the model use?

capability_field_addressed:
  - legal_land_finance.reserve_status
  - legal_land_finance.affordability_burden
  - legal_land_finance.anti_displacement_status

recommended_threshold:
  green:
    operating_reserve_months: 3_to_6
    replacement_reserve: funded_from_day_one
    emergency_repair_reserve: exists
    insurance_deductible_reserve: exists
    hardship_reserve: preferred
    housing_plus_utilities_cost: below_30_percent_of_income
    reserves_included_in_cost: true
    exit_formula: written
    hardship_policy: written
  warn:
    operating_reserve_months: below_3
    housing_plus_utilities: 30_to_50_percent_of_income
    replacement_reserve_not_asset_based
    hardship_reserve_absent
    exit formula unclear
  fail:
    no operating reserve
    no replacement reserve for class A assets
    housing_plus_utilities_above_50_percent_without_subsidy_or_hardship_plan
    reserves excluded from affordability
    no exit process
    hardship leads to immediate displacement

required_structure_module:
  - operating reserve
  - replacement reserve
  - emergency repair reserve
  - deductible reserve
  - hardship/stabilization process
  - affordability calculator
  - exit formula
  - resale restriction
  - due process policy

required_operating_protocol:
  - monthly reserve status
  - annual capital needs review
  - reserve drawdown approval
  - reserve replenishment trigger
  - resident income band testing
  - hardship/privacy process
  - payment plan/grace process

labor_impact:
  - finance steward workload
  - admin/records work
  - reduces emergency labor and displacement crisis

resource_impact:
  - increases monthly cost
  - reduces financial fragility
  - supports maintenance/recovery

failure_modes:
  - false affordability
  - deferred maintenance
  - sudden special assessments
  - debt crisis
  - hardship becomes displacement
  - future affordability collapse

external_review_needed:
  - CPA/accounting
  - attorney
  - lender/CDFI
  - insurance broker
  - capital needs assessment professional

simulation_scenarios_to_test:
  - roof_replacement
  - water_system_failure
  - insurance_deductible_event
  - income_loss
  - bad_year_assessment
  - resident_exit
  - land_value_spike

source_quality_confidence:
  evidence_quality: high_for_30_50_cost_burden
  translation_confidence: moderate_for_total_CIaC_burden
  regulatory_strength: professional_practice

source_ids:
  - HUD_CHAS_COST_BURDEN
  - EPA_ASSET_MANAGEMENT_WATER_WASTEWATER
  - GSN_RESALE_FORMULAS
  - LOCAL_HOUSING_SOLUTIONS_LEC
```

---

## 17. External Review Blockers

```yaml
domain: legal_land_finance
question: Which legal/financial assumptions must remain external-review blockers?

capability_field_addressed:
  - legal_land_finance.external_review_blockers
  - governance_anticapture.asset_lock_status
  - risk_resilience.promotion_blockers

recommended_threshold:
  green:
    all_required_external_reviews_completed_or_marked_not_applicable:
      - entity structure
      - land control
      - tenure/occupancy agreements
      - asset lock/dissolution
      - fundraising/securities
      - debt/collateral
      - tax status
      - insurance
      - zoning/permits
      - employment/labor
      - privacy
  warn:
    - review required but simulation-only mode still acceptable
  fail:
    - real-world promotion attempted with unresolved legal/finance blockers
    - tax exemption assumed
    - securities/fundraising assumptions unreviewed
    - insurance unavailable/unmodeled

required_structure_module:
  - review blocker registry
  - professional review status
  - assumptions dashboard
  - promotion gate

required_operating_protocol:
  - no real-world claim unless review status clear
  - review checklist
  - review expiration/recheck date
  - unresolved blocker display

labor_impact:
  - professional coordination labor
  - documentation burden
  - prevents reckless claims

resource_impact:
  - legal fees
  - accounting fees
  - insurance costs
  - permit costs

failure_modes:
  - overclaiming
  - unsafe implementation
  - legal/medical/engineering risk
  - public trust loss

external_review_needed:
  - attorney
  - CPA
  - lender/CDFI
  - insurance broker
  - zoning/land-use authority
  - employment lawyer if paid roles exist

simulation_scenarios_to_test:
  - promotion_attempt
  - public_fundraise
  - land_acquisition
  - debt_financing
  - insurance_denial
  - zoning_denial

source_quality_confidence:
  evidence_quality: high_for_need_to_not_overclaim
  translation_confidence: high
  regulatory_strength: binding_or_professional_review

source_ids:
  - IRS_501C3_ORGANIZATIONAL_TEST
  - GSN_CLT
  - HUD_CHAS_COST_BURDEN
```

---

# RISK RESILIENCE

## 18. Mandatory Hazards and Dependency Graph

```yaml
domain: risk_resilience
question: What hazards and dependency graph content should be mandatory?

capability_field_addressed:
  - risk_resilience.hazard_register_coverage
  - risk_resilience.dependency_graph_completeness
  - risk_resilience.single_point_failure_count

recommended_threshold:
  green:
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
    dependency_graph_includes:
      - resource_flows
      - labor_roles
      - external_suppliers
      - critical_infrastructure
      - governance_authority
      - high-need support
      - professional review dependencies
      - reserves
      - transport/access routes
      - data/admin access
  warn:
    - not all mandatory hazards modeled
    - no compound scenarios
    - external dependencies unmapped
    - labor roles omitted
  fail:
    - no hazard register
    - no dependency graph
    - no high-need scenario
    - critical functions cannot be traced to assets/roles/providers

required_structure_module:
  - hazard register
  - scenario library
  - dependency graph
  - critical function map
  - external dependency registry
  - role and asset registry

required_operating_protocol:
  - annual risk review
  - scenario run schedule
  - after-action review
  - owner role for each hazard
  - update graph after module changes

labor_impact:
  - scenario/drill labor
  - risk review labor
  - emergency role training burden
  - documentation labor

resource_impact:
  - buffers
  - reserves
  - emergency supplies
  - communications
  - training time

failure_modes:
  - single-hazard optimism
  - hidden dependency
  - cascade not detected
  - no recovery plan
  - governance authority omitted

external_review_needed:
  - emergency management review
  - fire/EMS review
  - public health review
  - insurance review
  - local climate/hazard review

simulation_scenarios_to_test:
  - all mandatory hazards
  - heat_wave_plus_grid_outage
  - illness_wave_plus_care_burnout
  - water_contamination_plus_delivery_failure
  - finance_shock_plus_repair_shock

source_quality_confidence:
  evidence_quality: high
  translation_confidence: moderate_to_high
  regulatory_strength: guideline

source_ids:
  - NIST_COMMUNITY_RESILIENCE_GUIDE
  - FEMA_NATIONAL_RESILIENCE_GUIDANCE
  - SENDAI_FRAMEWORK
```

---

## 19. Recovery Playbooks, Graceful Degradation, and RTOs

```yaml
domain: risk_resilience
question: What minimum recovery playbooks, degradation rules, and recovery-time targets should be modeled?

capability_field_addressed:
  - risk_resilience.recovery_playbook_count
  - risk_resilience.graceful_degradation_status
  - risk_resilience.recovery_time_objectives

recommended_threshold:
  green:
    minimum_recovery_playbooks:
      - water_contamination_recovery
      - energy_outage_recovery
      - illness_wave_recovery
      - food_disruption_recovery
      - fire_or_shelter_loss_recovery
      - financial_shock_recovery
      - care_support_failure_recovery
      - governance_conflict_or_capture_recovery
    playbook_count: 8
    graceful_degradation:
      - service levels defined
      - rationing rules defined
      - priority loads defined
      - fallback services defined
      - high-need protections defined
      - privacy/due process preserved
      - labor surge tracked
    recovery_time_targets:
      potable_water_floor: immediate_or_under_24h_with_reserve
      critical_energy_floor: 24_to_72h_protected
      emergency_food_floor: immediate
      sanitation_floor: immediate_emergency_mode
      medication_continuity: immediate
      care_support: same_day
      communications: under_24h
  warn:
    recovery_playbooks: 4_to_7
    recovery_time_unknown: true
    high_need_or_finance_playbook_missing: true
  fail:
    recovery_playbooks: fewer_than_4
    no playbook for water, energy, illness, or financial shock
    optional systems protected before vulnerable residents
    no rationing/fallback logic
    no bridge for potable water, sanitation, medication, or high-need care

required_structure_module:
  - recovery playbook library
  - service level matrix
  - priority load list
  - fallback service map
  - buffer bridge calculations
  - emergency mode manager
  - after-action review log

required_operating_protocol:
  - playbook review cycle
  - trigger criteria
  - resource/reserve use
  - resident communication
  - recovery owner
  - reserve replenishment
  - rest/recovery after crisis labor

labor_impact:
  - preparation labor
  - recovery labor
  - after-action review labor
  - should include rest/recovery after crisis work

resource_impact:
  - reserves
  - emergency supplies
  - professional support
  - documentation

failure_modes:
  - emergency response without recovery
  - reserves not replenished
  - high-need neglect
  - emergency authoritarianism
  - same failure repeats

external_review_needed:
  - emergency management
  - public health
  - insurance
  - legal/finance
  - clinical/professional depending playbook

simulation_scenarios_to_test:
  - 24h_outage
  - 72h_outage
  - water_contamination_7days
  - sanitation_failure
  - medication_cold_chain_failure
  - financial_repair_delay
  - emergency_authority_extension

source_quality_confidence:
  evidence_quality: high
  translation_confidence: moderate
  regulatory_strength: guideline

source_ids:
  - NIST_COMMUNITY_RESILIENCE_GUIDE
  - FEMA_NATIONAL_RESILIENCE_GUIDANCE
  - SENDAI_FRAMEWORK
```

---

## 20. Automatic Promotion Blockers

```yaml
domain: risk_resilience
question: Which failures should block promotion automatically?

capability_field_addressed:
  - risk_resilience.promotion_blockers
  - capability_gate.failures

recommended_threshold:
  automatic_block_if:
    - no tested potable water path or unresolved water review trigger
    - no sanitation/blackwater plan
    - no critical energy floor
    - no emergency food floor
    - high-need residents not modeled
    - no accessible route to essentials
    - no due process
    - no emergency power sunset
    - no land/tenure rights
    - reserves excluded from affordability
    - no hazard register
    - no dependency graph
    - no recovery playbooks for water/energy/illness/food/finance
    - safety-critical task without training gate
    - model claims legal/medical/engineering validity without review

required_structure_module:
  - promotion gate
  - review blocker registry
  - capability gate
  - resource gate
  - scenario coverage gate

required_operating_protocol:
  - block real-world promotion
  - require source/review status
  - show public provisionality
  - record unresolved blockers
  - allow simulation-only mode

labor_impact:
  - documentation/review labor
  - prevents reckless demo claims
  - increases trustworthiness

resource_impact:
  - no direct resource impact
  - may require professional review budget

failure_modes:
  - overclaiming
  - public trust loss
  - unsafe implementation
  - legal/medical/engineering risk
  - vulnerable residents harmed

external_review_needed:
  - all relevant professional reviews based on blocker type

simulation_scenarios_to_test:
  - promotion_attempt_with_unresolved_blockers
  - public_demo_mode
  - scenario_pass_but_review_fail
  - legal_finance_unreviewed
  - high_need_unmodeled

source_quality_confidence:
  evidence_quality: high_for_need_to_not_overclaim
  translation_confidence: high
  regulatory_strength: professional_practice_to_binding

source_ids:
  - NIST_COMMUNITY_RESILIENCE_GUIDE
  - FEMA_NATIONAL_RESILIENCE_GUIDANCE
  - CORNELL_PROCEDURAL_DUE_PROCESS
  - HUD_CHAS_COST_BURDEN
```

---


# LABOR / TIME

## 21. Commons Labor Upper Bound

```yaml
domain: labor_time
question: What is a dignified upper bound for required commons labor per resident per week?

capability_field_addressed:
  - labor_time.commons_labor_hours_per_resident
  - labor_time.life_burden_score
  - labor_time.burnout_risk

recommended_threshold:
  green:
    required_commons_labor_per_resident_per_week: 4_to_8_hours
    routine_care_labor_included: true
    governance_hours_bounded: true
  warn:
    required_commons_labor_per_resident_per_week: 8_to_10_hours
    hidden_labor_risk: medium
  fail:
    required_commons_labor_per_resident_per_week: above_12_hours_by_default
    required_labor_plus_wage_labor_pushes_total_above_55_hours_weekly
    labor_untracked: true

required_structure_module:
  - labor ledger
  - role scheduler
  - hidden labor tracker
  - care labor tracker
  - emergency labor tracker
  - protected time dashboard

required_operating_protocol:
  - weekly labor accounting
  - role assignment and backup
  - labor concentration audit
  - burnout trigger
  - paid/external support threshold
  - opt-out/accommodation process

labor_impact:
  - central proof metric
  - includes cleaning, food, care, maintenance, governance, training, emergency labor
  - excludes optional passion work

resource_impact:
  - may require paid roles
  - may require automation/tools
  - may reduce cash cost but must not hide labor cost

failure_modes:
  - wage bureaucracy replaced by commons bureaucracy
  - conscientious people carry floor
  - unpaid care labor
  - hidden gendered work
  - protected time disappears

external_review_needed:
  - employment/labor review if required or paid work creates legal exposure
  - disability/accommodation review
  - governance review for contribution rules

simulation_scenarios_to_test:
  - normal_week
  - bad_week
  - care_surge
  - governance_conflict_month
  - maintenance_emergency
  - required_work_plus_wage_work

source_quality_confidence:
  evidence_quality: moderate
  translation_confidence: moderate
  regulatory_strength: heuristic_with_health_and_time_use_support

source_ids:
  - BLS_ATUS_2024
  - WHO_ILO_LONG_WORKING_HOURS
  - OECD_WORK_LIFE_BALANCE
```

---

## 22. Labor Type Separation and Hidden Burden

```yaml
domain: labor_time
question: How should the model distinguish paid work reduction, commons labor, hidden labor, care labor, emergency labor, and prevent invisible burden?

capability_field_addressed:
  - labor_time.labor_type_ledger
  - labor_time.hidden_labor_status
  - labor_time.required_wage_hours
  - labor_time.labor_concentration_score

recommended_threshold:
  green:
    labor_categories_tracked:
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
    hidden_labor_status: low
    accommodation_process: confidential
    role_scheduler_active: true
  warn:
    emotional_support_or_scheduling_labor_untracked: true
    emergency_labor_untracked: true
    same_small_group_does_majority_of_care_cleaning_or_governance: true
  fail:
    care_cleaning_food_governance_or_maintenance_labor_untracked: true
    savings_depend_on_unpaid_hidden_labor: true
    high_need_residents_penalized_for_lower_labor_capacity: true
    labor_credits_become_social_credit: true

required_structure_module:
  - labor ledger
  - category taxonomy
  - time entry or estimated model
  - scenario labor surge tracker
  - fairness dashboard
  - accommodation process
  - optional vs required classifier

required_operating_protocol:
  - classify every recurring task
  - estimate untracked domains
  - review gender/status imbalance
  - separate optional from required labor
  - count emergency/recovery labor
  - monthly fairness audit

labor_impact:
  - increases measurement burden
  - enables fairer distribution
  - prevents false savings

resource_impact:
  - may reveal need for paid roles
  - may change affordability calculations

failure_modes:
  - hidden care work
  - invisible admin
  - kitchen/cleanup burden ignored
  - emergency labor treated as free
  - passion time reclassified as obligation

external_review_needed:
  - employment/labor law if work is required or paid
  - accessibility/accommodation review
  - governance review
  - privacy review

simulation_scenarios_to_test:
  - normal_week_labor_ledger
  - hidden_labor_detection
  - care_labor_concentration
  - emergency_labor_surge
  - optional_event_labor_drift
  - accommodation_request

source_quality_confidence:
  evidence_quality: high_for_time_use_categories
  translation_confidence: high
  regulatory_strength: research_inferred

source_ids:
  - BLS_ATUS_2024
  - OECD_WORK_LIFE_BALANCE
  - WHO_ILO_LONG_WORKING_HOURS
```

---

## 23. Meaningful Free-Time Increase

```yaml
domain: labor_time
question: What amount of free time increase is meaningful enough to count as a model improvement?

capability_field_addressed:
  - labor_time.free_time_increase
  - labor_time.passion_time_increase
  - labor_time.life_burden_reduction_score

recommended_threshold:
  green:
    required_wage_hours_reduction: at_least_25_percent_vs_baseline
    total_compulsory_labor_reduction: positive
    free_time_increase: at_least_5_hours_per_week
    passion_or_self_directed_time_increase: at_least_3_hours_per_week
    protected_sleep_recovery: not_reduced
  warn:
    free_time_increase: 1_to_5_hours_per_week
    gains_erased_in_bad_week: true
  fail:
    free_time_not_increased
    required_wage_hours_not_reduced
    total_compulsory_labor_increases
    free_time_gain_depends_on_hidden_labor

required_structure_module:
  - conventional baseline comparison
  - weekly time budget
  - free/passion/recovery time tracker
  - bad-week model
  - household/care burden model

required_operating_protocol:
  - compare against baseline household type
  - run normal and bad week
  - show confidence/assumptions
  - count hidden labor before declaring improvement

labor_impact:
  - primary project proof metric
  - required commons labor must be lower than wage/commute/admin burden removed
  - free time should not be consumed by governance or care surge

resource_impact:
  - may require upfront infrastructure spending
  - may require shared services
  - may require paid roles to protect free time

failure_modes:
  - lower cash cost but higher labor
  - free time appears only for high-status residents
  - bad week erases gains
  - passion time becomes market pressure

external_review_needed:
  - none for simulation
  - employment/labor review if used for real obligations
  - economic review for baseline comparison

simulation_scenarios_to_test:
  - conventional_renter_baseline
  - civic_floor_normal_week
  - bad_week
  - illness_week
  - financial_shock
  - scale_80_to_730_free_time

source_quality_confidence:
  evidence_quality: moderate
  translation_confidence: moderate
  regulatory_strength: heuristic

source_ids:
  - BLS_ATUS_2024
  - WHO_ILO_LONG_WORKING_HOURS
  - OECD_WORK_LIFE_BALANCE
  - UKRI_FOUR_DAY_WEEK
```

---

## 24. Labor Requiring Trained Roles

```yaml
domain: labor_time
question: What labor should require trained roles instead of generic resident contribution?

capability_field_addressed:
  - labor_time.trained_role_requirement
  - education_skill.training_gate_status
  - maintenance_repair.safety_boundary_status

recommended_threshold:
  green:
    trained_role_required_for:
      - water testing/sample collection
      - sanitation/PPE/human waste exposure
      - food safety lead
      - care steward/privacy/high-need support
      - first aid/CPR/AED
      - power tools and hazardous tools
      - energy outage mode
      - battery/generator area access
      - governance conflict/safeguarding
      - emergency roles
      - shared vehicle operation
  warn:
    - task has safety/privacy/public-health implications but training gate unclear
  fail:
    - safety-critical task assigned to generic resident contribution
    - licensed/professional work assigned to residents

required_structure_module:
  - skill lattice
  - training gate engine
  - role registry
  - professional handoff matrix
  - incident log

required_operating_protocol:
  - classify tasks by risk
  - require training before assignment
  - refresh training
  - block untrained assignment
  - record practice/evidence
  - define professional boundary

labor_impact:
  - training burden
  - reduces injury and failure risk
  - may require paid/professional roles

resource_impact:
  - training materials
  - PPE
  - professional service budget
  - tool access controls

failure_modes:
  - unsafe amateurism
  - credential/expert capture
  - one trained person overloaded
  - hidden training burden

external_review_needed:
  - OSHA/safety review where workers/volunteers are covered
  - public health review for water/sanitation/food
  - licensed trade review
  - clinical/legal review where applicable

simulation_scenarios_to_test:
  - untrained_task_assignment
  - expert_exit
  - training_expired
  - emergency_role_unavailable
  - hazardous_tool_incident

source_quality_confidence:
  evidence_quality: high
  translation_confidence: high
  regulatory_strength: binding_or_professional_practice_depending_task

source_ids:
  - OSHA_TRAINING_UNDERSTANDABLE
  - OSHA_LOCKOUT_TAGOUT
  - CDC_HUMAN_WASTE_WORKER_SAFETY
```

---

## 25. Labor Pass, Warn, Fail Thresholds

```yaml
domain: labor_time
question: What thresholds turn labor from pass to warn to fail?

capability_field_addressed:
  - labor_time.pass_warn_fail_status
  - labor_time.life_burden_score
  - labor_time.burnout_risk

recommended_threshold:
  green:
    required_commons_labor_per_resident_per_week: 4_to_8_hours
    governance_hours_per_resident_per_month: 1_to_3
    maintenance_hours_per_resident_per_month: 1_to_3
    care_labor_visible: true
    free_time_gain: at_least_5_hours_per_week
    required_wage_hours_reduction: at_least_25_percent
  warn:
    required_commons_labor_per_resident_per_week: 8_to_10_hours
    governance_hours_per_resident_per_month: above_5
    maintenance_hours_per_resident_per_month: above_5
    care_labor_concentration: medium
    free_time_gain: 1_to_5_hours
  fail:
    required_commons_labor_per_resident_per_week: above_12_hours_by_default
    governance_hours_per_resident_per_month: above_8
    maintenance_hours_per_resident_per_month: above_8_unless_paid_staffed
    care_labor_untracked: true
    free_time_not_increased: true
    required_wage_hours_not_reduced: true
    total_required_labor_plus_wage_labor_regularly_above_55_hours

required_structure_module:
  - labor/time ledger
  - baseline comparison
  - protected time dashboard
  - burnout indicators
  - trained role matrix
  - paid support threshold

required_operating_protocol:
  - weekly and monthly reporting
  - bad-week stress test
  - role assignment review
  - labor concentration audit
  - intervention if warn persists
  - fail if hidden labor or burnout unaddressed

labor_impact:
  - defines system proof
  - prevents false savings
  - may force node duplication, simplification, or paid roles

resource_impact:
  - paid roles may increase cost
  - automation/tools may reduce labor
  - smaller nodes may increase capital but reduce burden

failure_modes:
  - system only works by consuming residents
  - liberated time never appears
  - bad weeks collapse floor
  - labor burden shifts to vulnerable people

external_review_needed:
  - employment/labor review for required or paid work
  - disability/accommodation review
  - economic review for baseline model

simulation_scenarios_to_test:
  - normal_week
  - bad_week
  - illness_wave
  - maintenance_emergency
  - governance_conflict_month
  - founder_exit
  - scale_80_300_730_1500

source_quality_confidence:
  evidence_quality: moderate
  translation_confidence: moderate
  regulatory_strength: heuristic_with_health_time_use_support

source_ids:
  - WHO_ILO_LONG_WORKING_HOURS
  - BLS_ATUS_2024
  - OECD_WORK_LIFE_BALANCE
  - UKRI_FOUR_DAY_WEEK
```

---

## 26. Cross-Domain Capability Translation Matrix

| Domain | Green requires | Warn when | Fail when | Scale action |
|---|---|---|---|---|
| Care Health | care room, medication continuity, care meals, high-need support, external care path | care labor or backup weak | claims clinic role or high-need support absent | duplicate local care, federate clinic |
| Governance | due process, role backup, records, emergency sunset | role concentration or meeting burden rises | no due process or emergency sunset | federate |
| Mobility | 100% accessible essential routes, care/food/water access, non-driver plan | route penalty or distance burden | essential access missing | duplicate local access, federate transit |
| Legal/Finance | secure tenure, asset lock, reserves, affordability, external review | reserve/exit/tenure unclear | speculative capture or no written rights | federate professional review |
| Risk/Resilience | hazard register, dependency graph, playbooks, buffers, graceful degradation | scenario coverage incomplete | no floor continuity or recovery path | duplicate buffers, federate response |
| Labor/Time | bounded labor, hidden labor tracked, free time increases, wage burden reduced | labor burden rising | hidden labor or no life return | simplify, duplicate, pay, federate |

---

## 27. Recommended Capability Fields for `CapabilityState`

```yaml
care_health:
  nonclinical_care_floor: pass_warn_fail
  high_need_support_coverage: percentage
  medication_continuity_status: pass_warn_fail
  care_meal_protocol_status: pass_warn_fail
  illness_wave_readiness: pass_warn_fail
  care_labor_burden_status: pass_warn_fail

governance_anticapture:
  due_process_status: pass_warn_fail
  emergency_power_sunset: boolean
  role_backup_coverage: percentage
  role_concentration_score: 0_to_10
  decision_domain_clarity: pass_warn_fail
  records_privacy_status: pass_warn_fail

mobility_access:
  accessible_route_coverage: percentage
  essential_access_minutes_max: number
  accessible_route_penalty: number
  non_driver_access_status: pass_warn_fail
  emergency_access_status: pass_warn_fail
  mobility_support_module_status: pass_warn_fail

legal_land_finance:
  tenure_security_status: pass_warn_fail
  resident_rights_status: pass_warn_fail
  reserve_status: pass_warn_fail
  affordability_burden_status: pass_warn_fail
  anti_displacement_status: pass_warn_fail
  external_review_blockers: list

risk_resilience:
  hazard_register_coverage: percentage
  dependency_graph_completeness: percentage
  recovery_playbook_count: number
  graceful_degradation_status: pass_warn_fail
  recovery_time_objective_status: pass_warn_fail
  promotion_blocker_count: number

labor_time:
  commons_labor_hours_per_resident_per_week: number
  required_wage_hours_reduction_percent: number
  free_time_increase_hours_per_week: number
  passion_time_increase_hours_per_week: number
  hidden_labor_status: pass_warn_fail
  labor_concentration_score: 0_to_10
  burnout_risk_score: 0_to_10
```

---

## 28. Status and Next Step

```yaml
status: approved_as_research_input
not_yet:
  - final verified policy
  - legal review
  - medical review
  - accessibility compliance review
  - employment/labor review
  - emergency management approval

recommended_next_artifacts:
  - capability_policy.schema.json
  - capability_policies/ciac_capability_policy_v0.yaml
  - tests/test_capability_policy.py
  - viewer warnings from this report
  - scenario pack for six domains
```
