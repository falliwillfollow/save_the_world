# CIaC Deep Research Part 4, Governance, Maintenance, Mobility, Education, and Resilience

**Research ID:** `ciac_scaling_thresholds_part_4_v0_1`  
**Parent:** `ciac_scaling_thresholds_part_1_v0_2`, `ciac_scaling_thresholds_part_2_v0_2`, `ciac_scaling_thresholds_part_3_v0_1`  
**Purpose:** Deepen operating-system thresholds for governance, maintenance/tools, mobility/access, education/skill/work, and emergency/resilience.  
**Status:** Research synthesis for CIaC scaling policy, not final verified policy, legal guidance, safety certification, accessibility compliance, emergency-management approval, or employment/education law guidance.  
**Primary CIaC use:** refine `governance_anticapture`, `maintenance_repair`, `mobility_access`, `education_skill`, `risk_resilience`, `labor_time`, `node_scaling`, `topology_optimizer`, world viewer warnings, optimizer action preferences, and scenario tests.

---

## 0. What This Part Covers

```yaml
covered_domains:
  - governance
  - maintenance_and_tools
  - mobility_and_access
  - education_skill_work
  - emergency_and_resilience

primary_questions:
  - What group sizes support good decision-making, consent, deliberation, and conflict resolution?
  - Which governance functions should federate, and which should remain local?
  - Which maintenance/tool functions should duplicate locally versus centralize?
  - What walking/rolling radius should the model use for daily needs and high-need residents?
  - What learning/apprenticeship group sizes and safety gates should CIaC use?
  - Which systems should duplicate specifically for failure isolation?
  - How should fallback systems scale differently from normal systems?
```

---

## 1. Method and Evidence Normalization

This part uses the normalized evidence fields from earlier parts.

```yaml
evidence_quality:
  high: official guideline, regulatory threshold, or well-established professional standard
  moderate: peer-reviewed evidence, consistent practice precedent, or strong indirect professional consensus
  low: design practice, analogy, or weak/indirect evidence
  mixed: evidence exists but depends heavily on context

translation_confidence:
  high: direct translation to CIaC is reasonable
  moderate: useful but context-dependent
  low: speculative and should trigger review

regulatory_strength:
  binding: legal or regulatory category may be triggered
  guideline: official guidance or humanitarian/professional standard
  professional_practice: common practice in a field
  research_inferred: derived from research but not itself a formal standard
  heuristic: CIaC rule of thumb requiring future validation
```

Threshold classes:

```yaml
emergency_minimum: short-term survival/crisis reference
dignified_minimum: CIaC floor under normal or constrained conditions
comfortable_range: preferred normal operating range
soft_threshold: warning/review/planning threshold
hard_threshold: must duplicate, federate, fail, or require professional review
failure_threshold: condition that makes the model invalid or blocked
```

---

## 2. Source Registry

```yaml
source_registry:
  - id: CITIZENS_JURY_INVOLVE
    title: Citizens' Jury
    organization: Involve
    url: https://www.involve.org.uk/resource/citizens-jury
    supports:
      - citizens_jury_12_to_24_participants
      - small_deliberative_group_for_common_ground

  - id: PARTICIPEDIA_CITIZENS_JURY
    title: Citizens' Jury
    organization: Participedia
    url: https://participedia.net/method/155
    supports:
      - citizens_jury_12_to_25_participants
      - small_size_supports_quality_deliberation_and_trust

  - id: EPA_PUBLIC_PARTICIPATION_CITIZEN_JURIES
    title: Public Participation Guide, Citizen Juries
    organization: U.S. Environmental Protection Agency
    url: https://www.epa.gov/international-cooperation/public-participation-guide-citizen-juries
    supports:
      - representative_jury_approximately_8_to_12_people
      - paid_juror_time_commitment
      - deliberative_recommendation_process

  - id: DUNBAR_SOCIAL_LAYERS
    title: Dunbar social brain / social-layer research
    organization: research_literature
    url: https://royalsocietypublishing.org/doi/10.1098/rstb.2015.0093
    supports:
      - social_layers_5_15_50_150_500_1500
      - nested_social_scale

  - id: SOCIOCRACY_FOR_ALL
    title: Sociocracy overview
    organization: Sociocracy for All
    url: https://www.sociocracyforall.org/sociocracy/
    supports:
      - circles
      - consent_decision_making
      - roles
      - double_linking

  - id: DOE_FEMP_OM_BEST_PRACTICES
    title: Operations & Maintenance Best Practices Guide
    organization: U.S. Department of Energy, Federal Energy Management Program
    url: https://www.energy.gov/sites/prod/files/2020/04/f74/omguide_complete-w-eo-disclaimer.pdf
    supports:
      - operations_and_maintenance_as_efficiency_and_reliability_practice
      - preventive_predictive_reliability_centered_maintenance_logic

  - id: DOE_FEMP_OM_FEDERAL_FACILITIES
    title: Operations and Maintenance in Federal Facilities
    organization: U.S. Department of Energy
    url: https://www.energy.gov/cmei/femp/operations-and-maintenance-federal-facilities
    supports:
      - O_and_M_cost_effective_for_reliability_safety_energy_water_efficiency
      - inadequate_maintenance_causes_waste

  - id: EPA_ASSET_MANAGEMENT_WATER_WASTEWATER
    title: Asset Management for Water and Wastewater Utilities
    organization: U.S. Environmental Protection Agency
    url: https://19january2021snapshot.epa.gov/sustainable-water-infrastructure/asset-management-water-and-wastewater-utilities_.html
    supports:
      - planned_maintenance
      - assets_repaired_replaced_upgraded_on_time
      - enough_money_to_pay_for_repair_replacement

  - id: OSHA_LOCKOUT_TAGOUT
    title: Control of Hazardous Energy, 29 CFR 1910.147
    organization: Occupational Safety and Health Administration
    url: https://www.osha.gov/laws-regs/regulations/standardnumber/1910/1910.147
    supports:
      - hazardous_energy_control_during_servicing_and_maintenance
      - professional_safety_boundary_for_dangerous_tasks

  - id: OSHA_TRAINING_UNDERSTANDABLE
    title: Training Standards Policy Statement
    organization: Occupational Safety and Health Administration
    url: https://www.osha.gov/laws-regs/standardinterpretations/2010-04-28
    supports:
      - training_must_use_language_and_vocabulary_workers_understand
      - safety_training_legibility

  - id: ITDP_TOD_STANDARD
    title: TOD Standard
    organization: Institute for Transportation and Development Policy
    url: https://tod.itdp.org/tod-standard/tod-standard-framework.html
    supports:
      - frequent_transit_stop_within_500_m
      - rapid_transit_within_1000_m
      - accessibility_to_strollers_and_disabilities

  - id: ITDP_TOD_STANDARD_PDF
    title: TOD Standard PDF
    organization: Institute for Transportation and Development Policy
    url: https://itdp.org/wp-content/uploads/2017/06/TOD_Standard_EN.pdf
    supports:
      - 500_meters_about_10_minute_walk
      - 1000_meters_about_20_minute_walk

  - id: ACCESS_BOARD_ACCESSIBLE_ROUTES
    title: Chapter 4, Accessible Routes
    organization: U.S. Access Board
    url: https://www.access-board.gov/ada/guides/chapter-4-accessible-routes/
    supports:
      - accessible_route_clear_width_36_inches_minimum_with_limited_exceptions
      - accessibility_route_design_minimum

  - id: ACCESS_BOARD_ADA_STANDARDS
    title: ADA Standards
    organization: U.S. Access Board
    url: https://www.access-board.gov/ada/
    supports:
      - accessible_routes
      - route_widths
      - turning_clearances
      - play_area_route_clearances

  - id: NAEYC_RATIO_GROUP_SIZE
    title: Staff-to-Child Ratio and Class Size
    organization: NAEYC
    url: https://www.naeyc.org/sites/default/files/globally-shared/downloads/PDFs/accreditation/early-learning/staff_child_ratio_0.pdf
    supports:
      - infant_ratio_1_to_4_max_group_8
      - toddler_ratio_1_to_6_max_group_12
      - preschool_ratio_1_to_10_max_group_20
      - kindergarten_ratio_1_to_12_max_group_24

  - id: DOL_REGISTERED_APPRENTICESHIP
    title: Registered Apprenticeship Program
    organization: U.S. Department of Labor / Apprenticeship.gov
    url: https://www.apprenticeship.gov/employers/registered-apprenticeship-program
    supports:
      - paid_work_experience
      - mentorship
      - progressive_wage_increases
      - classroom_instruction
      - portable_nationally_recognized_credentials

  - id: NIST_NICE_FRAMEWORK
    title: NICE Framework
    organization: NIST / CISA NICCS
    url: https://niccs.cisa.gov/tools/nice-framework
    supports:
      - task_knowledge_skill_structure
      - competency_mapping

  - id: NIST_COMMUNITY_RESILIENCE_GUIDE
    title: Community Resilience Planning Guide for Buildings and Infrastructure Systems
    organization: NIST
    url: https://www.nist.gov/community-resilience/planning-guide
    supports:
      - social_and_economic_functions_linked_to_infrastructure
      - resilience_planning
      - dependencies_and_recovery_goals

  - id: FEMA_NATIONAL_RESILIENCE_GUIDANCE
    title: National Resilience Guidance
    organization: FEMA
    url: https://www.fema.gov/emergency-managers/national-preparedness/plan/resilience-guidance
    supports:
      - whole_community_resilience
      - resilience_principles_and_steps
      - cross_sector_resilience

  - id: FEMA_NATIONAL_RESILIENCE_GUIDANCE_PDF
    title: National Resilience Guidance PDF
    organization: FEMA
    url: https://www.fema.gov/sites/default/files/documents/fema_national-resilience-guidance_august2024.pdf
    supports:
      - whole_community_approach
      - resilience_across_sectors
      - resilience_planning_process

  - id: SENDAI_FRAMEWORK
    title: Sendai Framework for Disaster Risk Reduction 2015-2030
    organization: UNDRR
    url: https://www.undrr.org/publication/sendai-framework-disaster-risk-reduction-2015-2030
    supports:
      - understand_disaster_risk
      - strengthen_risk_governance
      - invest_in_risk_reduction
      - enhance_preparedness_response_recovery
```

---

## 3. Executive Translation Summary

```yaml
governance:
  natural_scaling_type: federate
  duplicate_locally:
    - circles
    - mediation/conflict panels
    - neighborhood assemblies
    - role backups
  federate:
    - coordination circle
    - councils
    - constitutional member process
    - legal/finance review
  base_node:
    circle: 5-12 people
    deliberative_panel: 12-24 people
    neighborhood_assembly: 30-80 people
  hard_threshold: 150 residents without federation

maintenance_tools:
  natural_scaling_type: hybrid
  duplicate_locally:
    - emergency tool caches
    - daily tools
    - class_A spare parts
    - local inspection roles
  federate:
    - advanced workshop
    - specialist maintenance
    - fabrication
    - professional contracts
  base_node: 50-150 residents
  district_threshold: 300+ residents

mobility_access:
  natural_scaling_type: hybrid
  duplicate_locally:
    - accessible routes
    - food/care/dropoff access
    - bike/cart storage
    - emergency access points
  federate:
    - transit spine
    - shuttle
    - district mobility hub
    - regional transport
  internal_essentials: 1-5 minutes
  transit_reference: 500m / about 10 minutes

education_skill_work:
  natural_scaling_type: hybrid
  duplicate_locally:
    - onboarding
    - safety training
    - small skill groups
    - apprentice/mentor pairs
  federate:
    - credentials
    - external partnerships
    - advanced workshops
  hands_on_group: 4-8 learners
  workshop_class: 8-12 learners

emergency_resilience:
  natural_scaling_type: hybrid
  duplicate_locally:
    - food/water/energy/sanitation buffers
    - first aid
    - communications
    - role backups
  federate:
    - district emergency coordination
    - regional mutual aid
    - hospitals
    - utility and watershed coordination
  village_block_threshold: 150
  district_threshold: 300
  regional_threshold: 1500
```

---

# GOVERNANCE

## 4. Operational Circle Size

```yaml
domain: governance
node_type: operational_circle
question: What group sizes support consent, operational decision-making, and ongoing stewardship?
scale_action: federate

thresholds:
  emergency_minimum:
    value: emergency_roles_with_defined_authority_and_sunset
    purpose: fast action without permanent emergency rule

  dignified_minimum:
    value: role_registry_due_process_transparent_records_and_backup_roles
    purpose: residents must understand who can decide what

  comfortable_range:
    min: 5
    max: 12
    unit: people_per_operational_circle

  soft_threshold:
    value: 12
    unit: people_in_operational_circle
    action: warn_split_or_delegate

  hard_threshold:
    value: 15
    unit: people_in_discussion_heavy_operational_circle
    action: split_circle_or_create_subrole_structure

  failure_threshold:
    condition: routine_operations_require_full_population_assembly
    action: fail_above_village_block_or_warn_below_village_block

human_factor_driver:
  - participation_quality
  - meeting_burden
  - role_clarity
  - operational_speed
  - anti_capture

evidence_quality: moderate
translation_confidence: moderate
regulatory_strength: professional_practice
source_ids:
  - SOCIOCRACY_FOR_ALL
  - DUNBAR_SOCIAL_LAYERS

notes_for_CIaC:
  - Circles are for ongoing domain operations: food, water, maintenance, care, energy, social/cultural.
  - The optimizer should not enlarge a circle indefinitely; it should split work into subroles or linked circles.
  - Circle size should be treated as governance labor and capability state, not just headcount.

optimizer_preference:
  - create_domain_circle
  - split_circle_above_12
  - add_backup_roles
  - federate_coordination_circle
ui_warning: Operational circle is becoming too large for consent or effective stewardship. Split or delegate roles.
```

---

## 5. Deliberation / Jury / Appeal Panel Size

```yaml
domain: governance
node_type: deliberative_panel
question: What group sizes support deliberation, jury/appeal panels, and conflict review?
scale_action: federate

thresholds:
  emergency_minimum:
    value: emergency_safeguarding_path_for_immediate_harm
    purpose: serious harm cannot wait for deliberative process

  dignified_minimum:
    value: impartial_panel_with_due_process_and_appeal_path
    purpose: residents should not lose rights by mob decision or clique pressure

  comfortable_range:
    min: 8
    max: 24
    unit: participants_per_panel

  soft_threshold:
    value: 12
    unit: participants
    action: ensure_facilitation_and_scope

  hard_threshold:
    value: 24
    unit: participants
    action: split_panel_or_formalize_process

  failure_threshold:
    condition: expulsion_loss_of_access_or_major_penalty_without_notice_evidence_response_impartial_review_or_appeal
    action: fail

human_factor_driver:
  - due_process
  - trust
  - fairness
  - conflict_resolution
  - anti_clique_protection

evidence_quality: moderate
translation_confidence: high
regulatory_strength: professional_practice
source_ids:
  - CITIZENS_JURY_INVOLVE
  - PARTICIPEDIA_CITIZENS_JURY
  - EPA_PUBLIC_PARTICIPATION_CITIZEN_JURIES

notes_for_CIaC:
  - Use 8-24 as a deliberative panel range, not daily governance.
  - Serious harm still requires safeguarding and possible external authority.
  - Panels should be selected and documented; they should not be informal friend groups.

optimizer_preference:
  - create_deliberative_panel
  - require_due_process
  - external_mediation_for_high_risk_cases
ui_warning: Deliberative or appeal process is too large, informal, or lacks due process.
```

---

## 6. Direct Assembly / Membership Body Size

```yaml
domain: governance
node_type: direct_assembly
question: What is the maximum useful size of a direct assembly before participation quality drops?
scale_action: federate

thresholds:
  emergency_minimum:
    value: emergency_authority_with_sunset_and_review
    purpose: avoid full assembly paralysis during crisis

  dignified_minimum:
    value: resident_membership_rights_and_constitutional_vote_path
    purpose: members retain legitimacy for major decisions

  comfortable_range:
    neighborhood_assembly:
      min: 30
      max: 80
      unit: residents
    village_membership_body:
      min: 50
      max: 150
      unit: residents

  soft_threshold:
    value: 80
    unit: direct_assembly_participants
    action: warn_for_participation_quality_and_meeting_burden

  hard_threshold:
    value: 150
    unit: residents_under_one_direct_assembly_for_routine_decisions
    action: federate_into_neighborhood_assemblies_circles_and_council

  failure_threshold:
    condition: one_direct_assembly_makes_routine_operational_decisions_above_150_or_emergency_authority_has_no_sunset
    action: fail

human_factor_driver:
  - participation_quality
  - meeting_burden
  - legitimacy
  - anti_capture
  - operational_speed

evidence_quality: moderate
translation_confidence: moderate
regulatory_strength: research_inferred
source_ids:
  - DUNBAR_SOCIAL_LAYERS
  - SOCIOCRACY_FOR_ALL

notes_for_CIaC:
  - Direct assembly can still ratify constitutional decisions.
  - Routine decisions should federate before the whole body becomes too large.
  - At 300+, governance should be district/federation logic, not larger meetings.

optimizer_preference:
  - keep_member_vote_for_constitutional_matters
  - federate_routine_governance
  - split_neighborhood_assemblies
ui_warning: Direct assembly burden is rising. Federate routine governance into circles and councils.
```

---

## 7. Governance Functions That Should Never Centralize

```yaml
domain: governance
node_type: anti_capture_governance_functions
question: Which governance functions should never centralize into one role or room?
scale_action: federate

thresholds:
  emergency_minimum:
    value: emergency_roles_with_audit_log_and_sunset

  dignified_minimum:
    value:
      - role_separation
      - backup_roles
      - conflict_of_interest_policy
      - transparent_records
      - due_process
      - external_escalation_path

  comfortable_range:
    protected_functions:
      - money
      - records
      - conflict_process
      - membership_or_expulsion
      - land_or_asset_transfer
      - emergency_authority
      - care_privacy
      - data_access

  soft_threshold:
    condition: same_person_or_small_group_controls_two_or_more_high_power_functions
    action: warn_capture_risk

  hard_threshold:
    condition: one_person_controls_money_records_conflict_process_or_survival_systems
    action: fail

  failure_threshold:
    condition: emergency_power_can_change_constitutional_rules_or_remove_opponents_without_review
    action: fail

human_factor_driver:
  - anti_capture
  - legitimacy
  - due_process
  - resident_rights
  - privacy

evidence_quality: moderate
translation_confidence: high
regulatory_strength: professional_practice
source_ids:
  - SOCIOCRACY_FOR_ALL
  - FEMA_NATIONAL_RESILIENCE_GUIDANCE

notes_for_CIaC:
  - CapabilityState should track role concentration.
  - World viewer can show role concentration as governance risk overlay.
  - This should be a hard gate, not just an optimizer preference.

optimizer_preference:
  - separate_roles
  - add_backup_roles
  - add_external_review_triggers
ui_warning: Governance capture risk: one role or group controls too many high-power functions.
```

---

# MAINTENANCE AND TOOLS

## 8. Local Tool Cache and Daily Tools

```yaml
domain: maintenance_tools
node_type: local_tool_cache
question: Which maintenance functions need local duplication for response time and resident autonomy?
scale_action: duplicate

thresholds:
  emergency_minimum:
    value: local_emergency_tools_for_class_A_system_isolation_and_basic_response
    purpose: isolate hazards, stop leaks, support emergency repairs

  dignified_minimum:
    value: local_tool_cache_work_order_access_safety_rules_and_basic_spares
    purpose: residents can report and handle safe ordinary tasks without one expert

  comfortable_range:
    min: 50
    max: 150
    unit: residents_per_local_tool_cache

  soft_threshold:
    value: 150
    unit: residents_per_tool_cache
    action: warn_for_access_bottleneck

  hard_threshold:
    value: 300
    unit: residents_without_additional_cache_or_service_node
    action: duplicate_tool_cache_or_create_district_workshop

  failure_threshold:
    condition: no_local_tools_for_emergency_isolation_no_PPE_no_tool_access_rules_or_no_work_order_path
    action: fail

human_factor_driver:
  - response_time
  - autonomy
  - safety
  - repairability
  - labor_burden

evidence_quality: low
translation_confidence: moderate
regulatory_strength: heuristic
source_ids:
  - DOE_FEMP_OM_BEST_PRACTICES
  - EPA_ASSET_MANAGEMENT_WATER_WASTEWATER

notes_for_CIaC:
  - Daily/common tools should be closer than advanced tools.
  - Local tool caches should duplicate by village block.
  - Tool access must not bypass training gates.

optimizer_preference:
  - duplicate_local_tool_cache
  - keep_advanced_tools_federated
  - enforce_tool_safety_training
ui_warning: Local tool access is over capacity or too distant. Add a tool cache or service node.
```

---

## 9. Central Workshop and Advanced Fabrication

```yaml
domain: maintenance_tools
node_type: central_workshop
question: What maintenance shops, tool libraries, spare parts stores, and repair teams can scale centrally?
scale_action: hybrid

thresholds:
  emergency_minimum:
    value: not_applicable_for_advanced_tools
    notes: Advanced workshop is not the emergency floor.

  dignified_minimum:
    value: access_to_repair_support_without_forcing_private_ownership_of_tools

  comfortable_range:
    village_workshop:
      min: 80
      max: 150
      unit: residents
    district_workshop:
      min: 300
      max: 500
      unit: residents
    advanced_fabrication:
      min: 500
      max: 1500
      unit: residents

  soft_threshold:
    value: 300
    unit: residents_without_district_workshop
    action: warn

  hard_threshold:
    value: 500
    unit: residents_without_district_or_federated_workshop
    action: federate_advanced_workshop

  failure_threshold:
    condition: advanced_or_dangerous_tools_used_without_training_PPE_or_professional_boundary
    action: fail

human_factor_driver:
  - autonomy
  - repair_capacity
  - safety
  - specialization
  - tool_duplication_cost

evidence_quality: low
translation_confidence: moderate
regulatory_strength: professional_practice
source_ids:
  - DOE_FEMP_OM_BEST_PRACTICES
  - OSHA_LOCKOUT_TAGOUT
  - OSHA_TRAINING_UNDERSTANDABLE

notes_for_CIaC:
  - Advanced workshop can centralize more than emergency tool access.
  - CNC, welding, high-voltage diagnostics, and hazardous tools require controlled access.
  - Use federation to avoid every block needing specialized equipment.

optimizer_preference:
  - federate_advanced_workshop
  - duplicate_basic_tool_cache
  - add_training_gate
ui_warning: Advanced workshop or hazardous tool access needs training, PPE, and federation rather than uncontrolled scaling.
```

---

## 10. Asset Registry, Spares, and Maintenance Labor

```yaml
domain: maintenance_tools
node_type: asset_management
question: How does maintenance labor scale with number of nodes versus size of nodes?
scale_action: hybrid

thresholds:
  emergency_minimum:
    value: class_A_asset_list_and_emergency_response_roles
    purpose: critical systems must be known and isolatable

  dignified_minimum:
    value:
      - asset_registry
      - preventive_schedule
      - work_order_system
      - critical_spares
      - professional_handoff
      - maintenance_reserve

  comfortable_range:
    class_A_documentation: 100_percent
    critical_spares_stocked: high
    routine_labor: 1_to_3_hours_per_resident_per_month
    warning_labor: 5_hours_per_resident_per_month
    fail_labor: 8_hours_per_resident_per_month_unless_staffed_or_paid

  soft_threshold:
    condition: class_A_maintenance_overdue_or_spares_below_minimum
    action: warn

  hard_threshold:
    condition: no_asset_registry_or_no_professional_handoff_or_no_replacement_reserve
    action: fail

  failure_threshold:
    condition: maintenance_depends_on_one_person_or_residents_assigned_hazardous_work_without_training
    action: fail

human_factor_driver:
  - reliability
  - response_time
  - burnout
  - safety
  - lifecycle_cost

evidence_quality: high
translation_confidence: high
regulatory_strength: professional_practice
source_ids:
  - DOE_FEMP_OM_FEDERAL_FACILITIES
  - EPA_ASSET_MANAGEMENT_WATER_WASTEWATER
  - OSHA_LOCKOUT_TAGOUT

notes_for_CIaC:
  - Maintenance scaling is not purely linear; more nodes increase local autonomy but multiply inspection tasks.
  - Large nodes centralize expertise but can create single points of failure.
  - CapabilityState should track maintenance labor, class A coverage, backlog, spares, and professional handoff.

optimizer_preference:
  - balance_node_duplication_with_maintenance_burden
  - prefer_local_critical_spares
  - federate_specialized_service_contracts
ui_warning: Maintenance system lacks asset registry, spares, reserves, or safe professional handoff.
```

---

# MOBILITY AND ACCESS

## 11. Internal Daily-Need Distance Tiers

```yaml
domain: mobility_access
node_type: internal_access_radius
question: What should be within 1 minute, 3 minutes, 5 minutes, 10 minutes, and 15 minutes?
scale_action: duplicate

thresholds:
  emergency_minimum:
    value: accessible_emergency_route_and_evacuation_support
    purpose: all residents reachable by emergency response

  dignified_minimum:
    value:
      1_minute:
        - unit_threshold
        - safe_exit
        - high_need_hygiene_or_help_point_where_needed
      3_minutes:
        - pod_commons
        - accessible_dropoff
        - emergency_water_distribution
        - care_room_for_high_need_residents_where_possible
      5_minutes:
        - food_commons
        - laundry
        - quiet_room
        - tool_cache
        - garden
        - primary_social_commons

  comfortable_range:
    value:
      10_minutes:
        - transit_or_shuttle_stop
        - district_commons
        - larger_workshop
      15_minutes:
        - larger_regional_amenities_if_transit_or_shuttle_is_strong

  soft_threshold:
    condition: essential_daily_need_exceeds_3_to_5_minutes_for_elders_children_disabled_or_high_care_households
    action: warn

  hard_threshold:
    condition: no_accessible_route_to_essential_spaces
    action: fail

  failure_threshold:
    condition: non_drivers_cannot_access_food_care_pharmacy_or_clinic
    action: fail

human_factor_driver:
  - accessibility
  - disability_support
  - elder_support
  - time_burden
  - care_access

evidence_quality: moderate
translation_confidence: moderate
regulatory_strength: heuristic
source_ids:
  - ITDP_TOD_STANDARD
  - ITDP_TOD_STANDARD_PDF
  - ACCESS_BOARD_ACCESSIBLE_ROUTES
  - ACCESS_BOARD_ADA_STANDARDS

notes_for_CIaC:
  - ITDP 500 m / 10-minute logic is useful for transit, not internal toilet/food/care access.
  - CIaC daily essentials must be closer than conventional TOD thresholds.
  - Accessible-route penalty should be modeled separately from ordinary walking distance.

optimizer_preference:
  - duplicate_neighborhood_center
  - shorten_accessible_routes
  - add_local_care_food_tool_nodes
ui_warning: Essential daily functions exceed walk/roll threshold, especially for high-need residents.
```

---

## 12. Accessible Routes, Grade, Surface, Weather, Lighting, Seating

```yaml
domain: mobility_access
node_type: accessible_route_quality
question: How do grade, surface, weather, lighting, seating, and route redundancy alter service-radius assumptions?
scale_action: resize_then_duplicate

thresholds:
  emergency_minimum:
    value: emergency_accessible_evacuation_route
    purpose: residents can exit or receive help

  dignified_minimum:
    value:
      - firm_stable_slip_resistant_route
      - accessible_widths_and_turning_clearances
      - lighting
      - resting_points
      - weather_management
      - route_redundancy_for_blockage
      - no_second_class_accessible_route

  comfortable_range:
    preferred:
      - routes_exceed_minimum_width_where_possible
      - benches_or_resting_points
      - shade
      - winter_or_rain_clearance
      - tactile_visual_wayfinding
      - accessible_route_not_longer_or_less_pleasant_than_primary_route

  soft_threshold:
    condition: accessible_route_much_longer_less_safe_or_less_pleasant_than_nonaccessible_route
    action: warn

  hard_threshold:
    condition: essential_space_lacks_accessible_route_or_route_blocks_emergency_access
    action: fail

  failure_threshold:
    condition: high_need_resident_access_depends_on_informal_help_due_to_route_design
    action: fail

human_factor_driver:
  - disability_access
  - elder_access
  - weather_resilience
  - route_safety
  - dignity

evidence_quality: high
translation_confidence: moderate
regulatory_strength: binding_or_guideline
source_ids:
  - ACCESS_BOARD_ACCESSIBLE_ROUTES
  - ACCESS_BOARD_ADA_STANDARDS

notes_for_CIaC:
  - Minimum ADA route dimensions are floors, not CIaC preferred comfort.
  - The world viewer should show accessible-route coverage and access penalties.
  - Route quality can shrink or expand effective radius.

optimizer_preference:
  - improve_accessible_route_quality
  - duplicate_node_if_accessible_distance_too_long
  - add_resting_points
ui_warning: Accessible route is missing, too long, unsafe, or less dignified than ordinary route.
```

---

## 13. Neighborhood Centers vs Single Center

```yaml
domain: mobility_access
node_type: neighborhood_center
question: At what population/area does the model need neighborhood centers instead of a single center?
scale_action: duplicate

thresholds:
  emergency_minimum:
    value: emergency_service_points_distributed_by_block_or_neighborhood

  dignified_minimum:
    value: daily_needs_within_3_to_5_minutes_for_each_residential_cluster

  comfortable_range:
    village_block:
      population: 50-150
      pattern: one_common_core_plus_pods
    district:
      population: 300-500
      pattern: multiple_neighborhood_centers_plus_district_spine
    town_city:
      population: 900-1500
      pattern: neighborhood_centers_plus_town_civic_layer

  soft_threshold:
    value: 150
    unit: residents_with_one_center
    action: warn_duplicate_neighborhood_center

  hard_threshold:
    value: 300
    unit: residents_with_single_center
    action: duplicate_centers_and_create_district_spine

  failure_threshold:
    condition: daily_needs_require_long_trip_to_single_center_above_village_scale
    action: fail_or_major_warning

human_factor_driver:
  - access
  - time_burden
  - elder_disability_support
  - social_scale
  - crowding_at_center

evidence_quality: moderate
translation_confidence: moderate
regulatory_strength: heuristic
source_ids:
  - ITDP_TOD_STANDARD
  - DUNBAR_SOCIAL_LAYERS
  - NIST_COMMUNITY_RESILIENCE_GUIDE

notes_for_CIaC:
  - A single center is appropriate for a village block, not for a district.
  - Above 300, the topology should show centers, not one larger center.
  - Scale slider should duplicate centers before expanding footprint linearly.

optimizer_preference:
  - duplicate_neighborhood_center
  - add_district_spine
  - preserve_short_daily_trip_lengths
ui_warning: Population/area exceeds single-center logic. Add neighborhood centers.
```

---

# EDUCATION / SKILL / WORK

## 14. Skill-Sharing and Hands-On Learning Group Size

```yaml
domain: education_skill_work
node_type: skill_group
question: What learning group sizes work best for skill-sharing, apprenticeships, workshops, and peer learning?
scale_action: duplicate

thresholds:
  emergency_minimum:
    value: safety_orientation_and_emergency_role_training
    purpose: residents know how to avoid harm and get help

  dignified_minimum:
    value:
      - role_based_training
      - safety_gates
      - understandable_instructions
      - practice_logs
      - backup_roles
      - no_hidden_training_labor

  comfortable_range:
    peer_learning_group: 3-6
    hands_on_skill_group: 4-8
    workshop_class: 8-12
    apprentice_ratio: 1_mentor_to_1_to_3_learners

  soft_threshold:
    value: 8
    unit: learners_in_hands_on_safety_training
    action: warn_split_group

  hard_threshold:
    value: 12
    unit: learners_in_tool_or_apprenticeship_session
    action: split_group_or_add_instructor

  failure_threshold:
    condition: safety_critical_task_assigned_without_training_gate_or_instructions_not_understandable
    action: fail

human_factor_driver:
  - safety
  - competence
  - attention
  - practice_quality
  - resident_autonomy

evidence_quality: moderate
translation_confidence: moderate
regulatory_strength: professional_practice
source_ids:
  - OSHA_TRAINING_UNDERSTANDABLE
  - DOL_REGISTERED_APPRENTICESHIP
  - NIST_NICE_FRAMEWORK

notes_for_CIaC:
  - The exact group sizes are heuristic except for regulated child-care contexts.
  - Hands-on safety training should be small enough for demonstration and correction.
  - Skill graph should use task/knowledge/skill mapping and practice evidence.

optimizer_preference:
  - duplicate_training_session
  - add_mentor
  - block_unsafe_task_assignment
ui_warning: Training group is too large for hands-on safety or skill acquisition.
```

---

## 15. Apprenticeship and Mentorship

```yaml
domain: education_skill_work
node_type: apprenticeship_path
question: Which education/workshop spaces can scale centrally, and which need neighborhood duplication?
scale_action: hybrid

thresholds:
  emergency_minimum:
    value: no_apprentice_as_sole_operator_for_safety_critical_task

  dignified_minimum:
    value:
      - observe_assist_supervised_independent_teach_back_progression
      - mentor_assignment
      - practice_log
      - paid_or_credited_training_when_it_becomes_core_labor
      - backup_role_development

  comfortable_range:
    mentor_to_learner:
      min: 1_to_1
      max: 1_to_3
    local_learning_node:
      min: 50
      max: 150
      unit: residents
    district_training_partnership:
      min: 300
      max: 1500
      unit: residents

  soft_threshold:
    condition: mentor_supports_more_than_3_active_apprentices_for_hands_on_roles
    action: warn

  hard_threshold:
    condition: one_expert_has_no_backup_or_apprentice_pipeline
    action: fail

  failure_threshold:
    condition: apprenticeship_used_as_unpaid_labor_that_should_be_paid_or_credentialed
    action: fail

human_factor_driver:
  - skill_redundancy
  - safety
  - expert_capture
  - labor_fairness
  - continuity

evidence_quality: moderate
translation_confidence: moderate
regulatory_strength: professional_practice
source_ids:
  - DOL_REGISTERED_APPRENTICESHIP
  - OSHA_TRAINING_UNDERSTANDABLE
  - NIST_NICE_FRAMEWORK

notes_for_CIaC:
  - Local learning nodes should teach floor operations.
  - District layer can federate credentials and external partnerships.
  - Training labor must be counted in Labor & Time.

optimizer_preference:
  - add_apprentice_pipeline
  - add_backup_role
  - federate_credential_partnership
ui_warning: Critical skill has no backup or apprentice pipeline.
```

---

## 16. Childcare and Youth Learning Group Size

```yaml
domain: education_skill_work
node_type: child_youth_learning
question: What group sizes work best for childcare and youth learning?
scale_action: duplicate

thresholds:
  emergency_minimum:
    value: child_safety_and_supervision_path
    purpose: children cannot be treated as informal background participants

  dignified_minimum:
    value:
      - age_appropriate_supervision
      - safeguarding
      - legal_review
      - professional_or_trained_caregiver_support
      - parent_guardian_consent

  comfortable_range:
    infants:
      ratio: 1_adult_to_4_children
      max_group_size: 8
    toddlers:
      ratio: 1_adult_to_6_children
      max_group_size: 12
    preschool:
      ratio: 1_adult_to_10_children
      max_group_size: 20
    kindergarten:
      ratio: 1_adult_to_12_children
      max_group_size: 24

  soft_threshold:
    condition: group_approaches_NAEYC_best_practice_maximum
    action: warn_and_plan_duplication

  hard_threshold:
    condition: group_exceeds_NAEYC_reference_without_professional_legal_review
    action: fail_or_block

  failure_threshold:
    condition: childcare_or_schooling_claimed_without_legal_safeguarding_and_staffing_review
    action: fail

human_factor_driver:
  - child_safety
  - safeguarding
  - attention
  - legal_compliance
  - caregiver_burden

evidence_quality: high
translation_confidence: high_for_childcare_reference
regulatory_strength: guideline_to_binding_depending_jurisdiction
source_ids:
  - NAEYC_RATIO_GROUP_SIZE

notes_for_CIaC:
  - CIaC should not casually model childcare as informal labor.
  - Child/youth learning can exist, but childcare/schooling requires legal/professional review.
  - Use NAEYC as a best-practice reference, not a universal legal rule.

optimizer_preference:
  - duplicate_child_group
  - require_safeguarding_review
  - add_trained_staff
ui_warning: Child/youth group exceeds best-practice ratio or lacks safeguarding/professional review.
```

---

## 17. Workshop Autonomy vs Over-Specialization

```yaml
domain: education_skill_work
node_type: resident_workshop_autonomy
question: When does a workshop become too large or specialized to serve ordinary resident autonomy?
scale_action: hybrid

thresholds:
  emergency_minimum:
    value: local_basic_repair_learning_and_tool_access
    purpose: residents can learn and perform safe basic repair

  dignified_minimum:
    value:
      - ordinary_resident_access_to_safe_basic_tools
      - training_gate_for_dangerous_tools
      - workshop_not_captured_by_experts
      - multiple_learning_formats

  comfortable_range:
    neighborhood_workshop:
      min: 50
      max: 150
      unit: residents
    district_workshop:
      min: 300
      max: 500
      unit: residents
    specialized_fabrication:
      min: 500
      max: 1500
      unit: residents

  soft_threshold:
    condition: workshop_usage_requires_specialist_permission_for_basic_tasks
    action: warn

  hard_threshold:
    condition: ordinary_residents_have_no_safe_access_to_basic_repair_or_learning_space
    action: fail

  failure_threshold:
    condition: hazardous_tools_accessible_without_training_or_specialized_shop_captures_all_repair_capacity
    action: fail

human_factor_driver:
  - autonomy
  - skill_growth
  - repair_culture
  - safety
  - expert_capture

evidence_quality: low
translation_confidence: moderate
regulatory_strength: heuristic
source_ids:
  - OSHA_TRAINING_UNDERSTANDABLE
  - DOL_REGISTERED_APPRENTICESHIP
  - DOE_FEMP_OM_BEST_PRACTICES

notes_for_CIaC:
  - Preserve ordinary autonomy with local safe tools.
  - Federate high-risk advanced tools.
  - Viewer should distinguish open workshop, trained-use area, and professional-only area.

optimizer_preference:
  - duplicate_basic_workshop
  - federate_specialized_tools
  - add_training_gates
ui_warning: Workshop is becoming too specialized or unsafe for ordinary resident autonomy.
```

---

# EMERGENCY AND RESILIENCE

## 18. Local Redundancy for Failure Isolation

```yaml
domain: emergency_resilience
node_type: local_redundancy
question: Which systems should duplicate specifically for failure isolation, not daily efficiency?
scale_action: duplicate

thresholds:
  emergency_minimum:
    required_local_buffers:
      - emergency_water
      - emergency_food
      - critical_energy
      - emergency_sanitation
      - first_aid
      - communications
      - local_tools
      - role_backups

  dignified_minimum:
    value:
      - failure_isolation_by_node
      - high_need_resident_support
      - accessible_evacuation
      - recovery_plan
      - emergency_authority_sunset

  comfortable_range:
    village_block:
      - local_buffers
      - local_roles
      - local emergency distribution
    district:
      - mutual aid
      - logistics
      - advanced maintenance
    regional:
      - hospitals
      - watershed
      - utilities
      - universities
      - specialized emergency support

  soft_threshold:
    value: 150
    unit: residents_without_local_redundancy
    action: warn

  hard_threshold:
    value: 300
    unit: residents_without_district_coordination
    action: federate_resilience

  failure_threshold:
    condition: one_node_failure_can_remove_water_food_energy_sanitation_or_care_floor_for_entire_population
    action: fail

human_factor_driver:
  - failure_isolation
  - cascading_risk
  - high_need_protection
  - recovery
  - emergency_burden

evidence_quality: high
translation_confidence: moderate
regulatory_strength: guideline
source_ids:
  - NIST_COMMUNITY_RESILIENCE_GUIDE
  - FEMA_NATIONAL_RESILIENCE_GUIDANCE
  - SENDAI_FRAMEWORK

notes_for_CIaC:
  - Redundancy should be justified by failure isolation, not daily efficiency.
  - Optimizer should sometimes duplicate less-efficiently if it reduces catastrophic cascade.
  - CapabilityState should track single-point failures.

optimizer_preference:
  - duplicate_local_buffers
  - add_backup_roles
  - federate_district_response
ui_warning: Critical system lacks local redundancy for failure isolation.
```

---

## 19. Distributed vs Centralized Reserves

```yaml
domain: emergency_resilience
node_type: reserve_topology
question: What is the evidence for distributed reserves versus centralized reserves?
scale_action: hybrid

thresholds:
  emergency_minimum:
    value:
      - local_accessible_reserve_for_immediate_floor
      - central_or_federated_reserve_for_bulk_backup

  dignified_minimum:
    value:
      - reserves_accessible_to_high_need_residents
      - reserve_inventory_visible
      - replenishment_plan
      - role_backup
      - distribution_route

  comfortable_range:
    distributed:
      - emergency_water
      - emergency_food_pickup
      - first_aid
      - communications
      - local_tools
    centralized_or_federated:
      - bulk_food
      - large_generator_or_fuel_contract
      - advanced_spares
      - regional_mutual_aid
      - insurance_and_finance_reserves

  soft_threshold:
    condition: all_reserves_in_one_location_or_under_one_role
    action: warn

  hard_threshold:
    condition: reserve_not_accessible_during_likely_failure_or_no_replenishment_plan
    action: fail

  failure_threshold:
    condition: centralized_reserve_blocks_high_need_resident_access_or_creates_single_point_of_failure
    action: fail

human_factor_driver:
  - access
  - redundancy
  - distribution
  - high_need_support
  - recovery

evidence_quality: moderate
translation_confidence: moderate
regulatory_strength: professional_practice
source_ids:
  - NIST_COMMUNITY_RESILIENCE_GUIDE
  - FEMA_NATIONAL_RESILIENCE_GUIDANCE

notes_for_CIaC:
  - Use hybrid reserve topology: local immediate buffers plus federated bulk reserves.
  - Stress scenarios should simulate blocked routes and operator absence.
  - Viewer should show reserve accessibility, not only reserve quantity.

optimizer_preference:
  - distribute_immediate_reserves
  - centralize_bulk_reserves_with_distribution_plan
  - add_replenishment_path
ui_warning: Reserve is centralized, inaccessible, or lacks replenishment/distribution plan.
```

---

## 20. Fallback Systems vs Normal Systems

```yaml
domain: emergency_resilience
node_type: fallback_system
question: How should fallback systems scale differently from normal systems?
scale_action: hybrid

thresholds:
  emergency_minimum:
    value:
      - fallback_water
      - fallback_food
      - fallback_sanitation
      - fallback_energy
      - fallback_communications
      - fallback_care
      - evacuation_or_external_support

  dignified_minimum:
    value:
      - fallback_mode_is_time_limited
      - privacy_and_due_process_protected
      - high_need_residents_prioritized
      - labor_surge_counted
      - recovery_plan_defined

  comfortable_range:
    normal_system:
      optimize_for: efficiency_quality_low_burden
    fallback_system:
      optimize_for: simplicity_access_redundancy_failure_isolation

  soft_threshold:
    condition: fallback_system_requires_same_infrastructure_as_normal_system
    action: warn

  hard_threshold:
    condition: fallback_system_not_independent_enough_to_survive_normal_system_failure
    action: fail

  failure_threshold:
    condition: fallback_mode_sacrifices_consent_due_process_or_high_need_resident_support
    action: fail

human_factor_driver:
  - resilience
  - simplicity
  - human_rights_under_stress
  - recovery
  - labor_surge

evidence_quality: high
translation_confidence: moderate
regulatory_strength: guideline
source_ids:
  - NIST_COMMUNITY_RESILIENCE_GUIDE
  - FEMA_NATIONAL_RESILIENCE_GUIDANCE
  - SENDAI_FRAMEWORK

notes_for_CIaC:
  - Fallback systems should be smaller, simpler, local, and legible.
  - Do not optimize fallback systems for normal convenience.
  - Stress Mode should visually show fallback activation and recovery path.

optimizer_preference:
  - separate_fallback_from_normal_dependencies
  - preserve_rights_under_emergency
  - add_recovery_playbook
ui_warning: Fallback system is too dependent on the normal system it is meant to replace.
```

---

## 21. Resilience Governance and Emergency Authority

```yaml
domain: emergency_resilience
node_type: emergency_governance
question: What minimum governance redundancy should exist for emergency and resilience functions?
scale_action: federate

thresholds:
  emergency_minimum:
    value:
      - emergency_roles
      - communication_tree
      - authority_limits
      - incident_log
      - sunset_clause

  dignified_minimum:
    value:
      - emergency_powers_time_limited
      - after_action_review
      - due_process_preserved_except_narrow_immediate_safety_actions
      - no_constitutional_changes_during_emergency
      - anti_capture_monitoring

  comfortable_range:
    village_block:
      - emergency_roles_and_backups
      - local incident log
      - local communication
    district:
      - mutual aid coordination
      - external authority liaison
      - logistics
    regional:
      - public emergency management interface
      - utility_health_hospital coordination

  soft_threshold:
    condition: emergency_role_has_no_backup_or_after_action_review_absent
    action: warn

  hard_threshold:
    condition: emergency_power_has_no_sunset_or_can_change_core_rights
    action: fail

  failure_threshold:
    condition: emergency_authority_can_be_used_for_factional_advantage_or_asset_capture
    action: fail

human_factor_driver:
  - anti_capture
  - emergency_speed
  - rights
  - legitimacy
  - recovery_learning

evidence_quality: high
translation_confidence: moderate
regulatory_strength: guideline
source_ids:
  - FEMA_NATIONAL_RESILIENCE_GUIDANCE
  - SENDAI_FRAMEWORK
  - NIST_COMMUNITY_RESILIENCE_GUIDE

notes_for_CIaC:
  - Emergency governance belongs in both governance and risk modules.
  - Emergency powers should activate quickly but expire automatically.
  - Viewer should show emergency mode timer and sunset status.

optimizer_preference:
  - add_emergency_sunset
  - add_backup_roles
  - federate_external_authority_liaison
ui_warning: Emergency authority lacks backup, sunset, or anti-capture controls.
```

---

## 22. Part 4 CIaC Translation Matrix

| Domain | Node | Natural scaling type | Base node | Soft threshold | Hard threshold | Service-radius constraint | Primary driver | Optimizer preference |
|---|---|---:|---:|---:|---:|---|---|---|
| Governance | operational circle | federate | 5-12 people | 12 | 15 | N/A | meeting quality, role clarity | split circle, delegate roles |
| Governance | deliberative panel | federate | 8-24 people | 12 | 24 | N/A | due process, trust | panel + external mediation |
| Governance | direct assembly | federate | 30-80 local, 50-150 village | 80 | 150 | N/A | participation, legitimacy | federate routine governance |
| Governance | anti-capture roles | federate | separated roles | 2+ high-power functions centralized | one role controls money/records/conflict | N/A | anti-capture | split roles, add audits |
| Maintenance | local tool cache | duplicate | 50-150 residents | 150 | 300 | 1-3 min for common tools | response/autonomy | duplicate cache |
| Maintenance | central workshop | hybrid | 150-500 residents | 300 | 500 | district accessible | specialization | federate advanced workshop |
| Maintenance | asset registry | hybrid | all class A assets | overdue critical tasks | no registry/reserve/spares | N/A | reliability | add registry, spares, reserve |
| Mobility | internal essentials | duplicate | neighborhood | >3-5 min | no accessible route | 1/3/5 min tiers | access/time burden | duplicate local nodes |
| Mobility | transit/district access | federate | 500m / 10 min target | >500m to frequent transit/shuttle | non-drivers excluded | 10 min target | external access | shuttle/transit/mobility hub |
| Mobility | accessible route quality | resize/duplicate | all essential routes | accessible route penalty | no accessible route | accessible path | disability dignity | improve route or duplicate node |
| Education | hands-on skill group | duplicate | 4-8 learners | 8 | 12 | local learning room | safety/attention | split groups |
| Education | apprenticeship | hybrid | 1 mentor to 1-3 learners | >3 active learners | no backup/expert exit | local/district | skill redundancy | apprentice pipeline |
| Education | childcare/youth | duplicate | age-specific ratios | near max | above max without review | local/safeguarded | child safety | duplicate/staff/review |
| Resilience | local redundancy | duplicate | village block | 150 | 300 no district | local buffers | failure isolation | duplicate buffers |
| Resilience | reserve topology | hybrid | local + bulk | all reserves one place | inaccessible reserve | local access | recovery | distribute immediate reserve |
| Resilience | fallback systems | hybrid | independent backup | shared dependencies | fallback fails with normal system | local | cascade prevention | independent fallback |
| Resilience | emergency governance | federate | block/district | no backup | no sunset | N/A | anti-capture under stress | sunset + review |
```

---

## 23. UI Warning Language

```yaml
warnings:
  governance_circle_large:
    message: Operational circle is becoming too large for consent or effective stewardship. Split or delegate roles.

  deliberative_panel_large:
    message: Deliberative or appeal process is too large, informal, or lacks due process.

  direct_assembly_burden:
    message: Direct assembly burden is rising. Federate routine governance into circles and councils.

  governance_capture:
    message: Governance capture risk: one role or group controls too many high-power functions.

  local_tool_cache_overload:
    message: Local tool access is over capacity or too distant. Add a tool cache or service node.

  advanced_tool_safety:
    message: Advanced workshop or hazardous tool access needs training, PPE, and federation.

  asset_management_missing:
    message: Maintenance system lacks asset registry, spares, reserves, or safe professional handoff.

  essential_access_distance:
    message: Essential daily functions exceed walk/roll threshold, especially for high-need residents.

  accessible_route_penalty:
    message: Accessible route is missing, too long, unsafe, or less dignified than ordinary route.

  single_center_overload:
    message: Population or area exceeds single-center logic. Add neighborhood centers.

  training_group_too_large:
    message: Training group is too large for hands-on safety or skill acquisition.

  skill_backup_missing:
    message: Critical skill has no backup or apprentice pipeline.

  childcare_review_required:
    message: Child/youth group exceeds best-practice ratio or lacks safeguarding/professional review.

  workshop_expert_capture:
    message: Workshop is becoming too specialized or unsafe for ordinary resident autonomy.

  local_redundancy_missing:
    message: Critical system lacks local redundancy for failure isolation.

  reserve_topology_risk:
    message: Reserve is centralized, inaccessible, or lacks replenishment/distribution plan.

  fallback_dependency:
    message: Fallback system is too dependent on the normal system it is meant to replace.

  emergency_governance_risk:
    message: Emergency authority lacks backup, sunset, or anti-capture controls.
```

---

## 24. Suggested Tests

```yaml
tests:
  governance_circle_soft:
    people_in_circle: 13
    expected: warning

  governance_circle_hard:
    people_in_circle: 16
    expected: split_required

  deliberative_panel_hard:
    people_in_panel: 25
    expected: split_or_formalize

  direct_assembly_150:
    population: 151
    routine_decisions_by_direct_assembly: true
    expected: fail

  capture_role_concentration:
    same_role_controls:
      - money
      - records
      - conflict
    expected: fail

  local_tool_cache_soft:
    residents_per_tool_cache: 160
    expected: warning

  central_workshop_hard:
    residents_without_district_workshop: 501
    expected: federate_required

  no_asset_registry:
    class_A_assets_present: true
    asset_registry: false
    expected: fail

  access_essential_over_5:
    high_need_resident_food_access_minutes: 7
    expected: warning_or_duplicate_node

  no_accessible_route:
    essential_space_accessible_route: false
    expected: fail

  single_center_300:
    population: 300
    centers: 1
    expected: duplicate_centers_required

  hands_on_training_large:
    learners: 9
    expected: warning

  hands_on_training_hard:
    learners: 13
    expected: split_required

  apprenticeship_no_backup:
    critical_role_expert_count: 1
    apprentice_pipeline: false
    expected: fail

  childcare_ratio_exceeded:
    preschool_children: 21
    adults: 2
    professional_review: false
    expected: fail_or_block

  resilience_single_point:
    entire_population_depends_on_one_water_node: true
    expected: fail

  reserve_centralized:
    all_reserves_one_location: true
    route_blockage_scenario: true
    expected: warning_or_fail

  fallback_same_dependency:
    backup_power_depends_on_failed_grid: true
    expected: fail

  emergency_no_sunset:
    emergency_power_sunset: false
    expected: fail
```

---

## 25. Repo Implementation Notes

```yaml
suggested_policy_files:
  - scale_policies/ciac_scaling_policy_v0.yaml
  - schemas/scaling_policy.schema.json

node_scaling_updates:
  - add governance circle max thresholds
  - add direct assembly/federation threshold
  - add local tool cache thresholds
  - add accessible service radius constraints
  - add training group thresholds
  - add resilience redundancy thresholds

topology_optimizer_updates:
  - prefer federated governance above 150
  - duplicate neighborhood centers above 150_to_300
  - federate advanced workshop above 300_to_500
  - duplicate local buffers before central reserves
  - penalize fallback systems sharing same dependencies as normal systems

world_manifest_updates:
  - show governance scale warnings
  - show local tool cache coverage
  - show accessible route penalties
  - show learning group/training gates
  - show reserve topology and fallback dependency overlays
  - show emergency authority sunset timer/status

capability_state_updates:
  governance:
    - circle_size_status
    - direct_assembly_burden
    - role_concentration_score
    - due_process_status
    - emergency_sunset_status
  maintenance:
    - local_tool_cache_coverage
    - class_A_asset_registry_status
    - critical_spares_status
    - professional_handoff_status
  mobility:
    - essential_access_minutes
    - accessible_route_penalty
    - non_driver_access_status
  education:
    - training_group_size_status
    - apprentice_pipeline_status
    - childcare_review_status
  resilience:
    - local_redundancy_status
    - reserve_topology_status
    - fallback_independence_status
    - emergency_governance_status
```

---

## 26. Status

```yaml
status: approved_as_research_input
not_yet:
  - final_verified_policy
  - legal_review
  - accessibility_compliance_review
  - emergency_management_review
  - employment_or_training_law_review
  - childcare_licensing_review
next_step:
  - part_5_repo_implementation_translation
  - then_scaling_policy_v0_yaml_and_schema
```
