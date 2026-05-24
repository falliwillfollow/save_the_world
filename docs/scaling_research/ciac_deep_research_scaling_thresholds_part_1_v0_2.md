# CIaC Deep Research Part 1, Scaling Thresholds and Node Actions, Updated

**Research ID:** `ciac_scaling_thresholds_part_1_v0_2`  
**Supersedes:** `ciac_scaling_thresholds_part_1_v0_1`  
**Purpose:** Convert interdisciplinary evidence into provisional, machine-readable scaling thresholds for CIaC modules.  
**Status:** Approved research input, not final verified policy.  
**Use:** Feed `scaling_policy_v0`, `module_registries`, `node_scaling`, `topology_optimizer`, world viewer warnings, optimizer preferences, and future scenario tests.

---

## 0. What Changed in v0.2

This update addresses three review items:

```yaml
updates:
  source_traceability:
    change: added source IDs and source registry
    reason: thresholds need source-level traceability before driving optimizer behavior

  evidence_normalization:
    change: split evidence into evidence_quality, translation_confidence, and regulatory_strength
    reason: avoid composite labels such as low_to_moderate or high_for_emergency_minima

  threshold_separation:
    change: separated emergency_minimum, dignified_minimum, comfortable_range, and failure_threshold
    reason: emergency survival standards should not be confused with CIaC normal dignity standards
```

---

## 1. Interpretation Rules

These thresholds are **decision heuristics**, not final standards. CIaC combines housing, cohousing, public health, emergency management, governance, elder care, skill systems, local food systems, mobility, and resilience. Many source domains do not map cleanly onto CIaC. This report therefore separates evidence from translation.

### 1.1 Evidence Quality

```yaml
evidence_quality:
  high:
    meaning: official guideline, regulatory threshold, or well-established professional standard

  moderate:
    meaning: peer-reviewed research, consistent practice precedent, or strong indirect professional consensus

  low:
    meaning: design practice, analogy, expert judgment, or weak/indirect evidence

  mixed:
    meaning: evidence exists but points in different directions or depends heavily on context
```

### 1.2 Translation Confidence

```yaml
translation_confidence:
  high:
    meaning: direct translation to CIaC is reasonable

  moderate:
    meaning: translation is useful but depends on context or requires design judgment

  low:
    meaning: translation is speculative and should be treated as a prompt for review
```

### 1.3 Regulatory Strength

```yaml
regulatory_strength:
  binding:
    meaning: legal or regulatory category may be triggered

  guideline:
    meaning: official guidance or humanitarian/professional standard, not necessarily binding

  professional_practice:
    meaning: common practice in a field or design tradition

  research_inferred:
    meaning: derived from research but not itself a formal standard

  heuristic:
    meaning: CIaC modeling rule of thumb requiring future validation
```

### 1.4 Scale Actions

```yaml
scale_action:
  resize:
    meaning: increase capacity of same node

  duplicate:
    meaning: add another local node of the same type

  federate:
    meaning: create higher-level coordination layer across local nodes

  hybrid:
    meaning: resize some functions, duplicate local access, and federate specialized capacity
```

---

## 2. Threshold Object Shape for Future Policy File

Each policy item should eventually map to this structure:

```yaml
threshold_item:
  domain: string
  node_type: string
  question: string
  scale_action: resize | duplicate | federate | hybrid

  thresholds:
    emergency_minimum:
      value: any
      purpose: short_term_survival_or_crisis_reference
      source_ids: []

    dignified_minimum:
      value: any
      purpose: minimum_CIaC_floor_under_normal_or_constrained_conditions
      source_ids: []

    comfortable_range:
      min: any
      max: any
      purpose: preferred_normal_operating_range
      source_ids: []

    soft_threshold:
      value: any
      action: warn | review | plan_duplication | plan_federation
      source_ids: []

    hard_threshold:
      value: any
      action: fail | duplicate | federate | professional_review_required
      source_ids: []

    failure_threshold:
      condition: string
      action: fail | block | professional_review_required
      source_ids: []

  evidence_quality: high | moderate | low | mixed
  translation_confidence: high | moderate | low
  regulatory_strength: binding | guideline | professional_practice | research_inferred | heuristic
  human_factor_driver: []
  source_ids: []
  notes_for_CIaC: []
  optimizer_preference: []
  ui_warning: string
```

---

## 3. Source Registry

```yaml
source_registry:
  - id: WHO_HOUSING_2018
    title: WHO Housing and Health Guidelines
    organization: World Health Organization
    year: 2018
    url: https://www.who.int/publications/i/item/9789241550376
    supports:
      - household_crowding_is_health_relevant
      - inadequate_living_space_is_housing_health_issue
      - accessibility_and_temperature_are_housing_health_issues

  - id: WHO_HOUSING_CROWDING_NCBI
    title: Household crowding, WHO Housing and Health Guidelines chapter
    organization: WHO / NCBI Bookshelf
    url: https://www.ncbi.nlm.nih.gov/books/NBK535289/
    supports:
      - crowding_is_mismatch_between_dwelling_and_household
      - crowding_affects_physical_and_mental_health
      - crowding_depends_on_design_and_household_needs

  - id: EPA_PUBLIC_WATER_SYSTEM
    title: Information about Public Water Systems
    organization: U.S. Environmental Protection Agency
    url: https://www.epa.gov/dwreginfo/information-about-public-water-systems
    supports:
      - public_water_system_15_connections_or_25_people_60_days

  - id: CDC_EMERGENCY_WATER
    title: How to Create an Emergency Water Supply
    organization: U.S. Centers for Disease Control and Prevention
    url: https://www.cdc.gov/water-emergency/about/how-to-create-and-store-an-emergency-water-supply.html
    supports:
      - one_gallon_per_person_per_day
      - three_day_minimum
      - two_week_preferred_if_possible
      - higher_need_profiles_need_more_water

  - id: WHO_EMERGENCY_WATER_20L
    title: How much water is needed in emergencies
    organization: World Health Organization
    url: https://cdn.who.int/media/docs/default-source/wash-documents/who-tn-09-how-much-water-is-needed.pdf
    supports:
      - twenty_liters_per_person_per_day_essential_health_reference

  - id: FDA_FOOD_CODE_2022
    title: FDA Food Code 2022
    organization: U.S. Food and Drug Administration
    url: https://www.fda.gov/food/fda-food-code/food-code-2022
    supports:
      - shared_food_operations_need_time_temperature_controls
      - food_safety_logs
      - allergen_and_cleaning_controls

  - id: SPHERE_WASH
    title: Sphere Handbook, WASH Standards
    organization: Sphere Association
    url: https://handbook.spherestandards.org/
    supports:
      - emergency_WASH_minimums
      - toilet_access_emergency_reference
      - emergency_standards_not_normal_dignity

  - id: WHO_SANITATION_SAFETY_PLANNING
    title: Sanitation Safety Planning
    organization: World Health Organization
    url: https://www.who.int/publications/i/item/9789241549240
    supports:
      - sanitation_chain_risk_management
      - containment_conveyance_treatment_reuse_disposal

  - id: NIST_COMMUNITY_RESILIENCE_GUIDE
    title: Community Resilience Planning Guide for Buildings and Infrastructure Systems
    organization: NIST
    url: https://www.nist.gov/community-resilience/planning-guide
    supports:
      - community_resilience_planning
      - social_and_economic_functions_linked_to_infrastructure
      - recovery_goals_and_dependencies

  - id: FEMA_NATIONAL_RESILIENCE_GUIDANCE
    title: National Resilience Guidance
    organization: FEMA
    url: https://www.fema.gov/emergency-managers/national-preparedness/plan/resilience-guidance
    supports:
      - whole_community_resilience
      - maturity_model
      - resilience_planning_process

  - id: SENDAI_FRAMEWORK
    title: Sendai Framework for Disaster Risk Reduction 2015-2030
    organization: UNDRR
    url: https://www.undrr.org/publication/sendai-framework-disaster-risk-reduction-2015-2030
    supports:
      - understand_disaster_risk
      - strengthen_risk_governance
      - invest_in_risk_reduction
      - preparedness_response_recovery

  - id: ITDP_TOD_STANDARD
    title: TOD Standard
    organization: Institute for Transportation and Development Policy
    url: https://www.itdp.org/publication/tod-standard/
    supports:
      - walk_cycle_connect_transit_mix_densify_compact_shift
      - walkability_distance_logic

  - id: ACCESS_BOARD_ADA_STANDARDS
    title: ADA Accessibility Standards
    organization: U.S. Access Board
    url: https://www.access-board.gov/ada/
    supports:
      - accessible_routes
      - ramps
      - accessibility_minimums

  - id: NAEYC_RATIOS_GROUP_SIZE
    title: Staff-to-child ratio and class size recommendations
    organization: NAEYC
    url: https://www.naeyc.org/
    supports:
      - child_group_size_and_ratio_reference

  - id: SURGEON_GENERAL_SOCIAL_CONNECTION
    title: Our Epidemic of Loneliness and Isolation
    organization: U.S. Surgeon General / HHS
    url: https://www.hhs.gov/sites/default/files/surgeon-general-social-connection-advisory.pdf
    supports:
      - built_environment_affects_social_connection
      - social_connection_is_public_health_issue

  - id: DUNBAR_SOCIAL_LAYERS
    title: Dunbar social brain / social-layer research
    organization: research_literature
    url: https://royalsocietypublishing.org/doi/10.1098/rstb.2015.0093
    supports:
      - social_layers_5_15_50_150_500_1500

  - id: GREEN_HOUSE_SMALL_HOUSE
    title: Green House / small-house elder-care model
    organization: Green House Project / long-term-care research
    url: https://thegreenhouseproject.org/
    supports:
      - small_house_elder_care_10_to_12_residents
      - private_room_bath_homelike_care_logic

  - id: COHOUSING_ASSOCIATION
    title: What is Cohousing
    organization: Cohousing Association of the United States
    url: https://www.cohousing.org/what-cohousing/cohousing/
    supports:
      - private_homes_plus_shared_spaces
      - privacy_and_community_balance
```

---

## 4. Executive Threshold Summary

```yaml
natural_social_layers:
  intimate_support:
    comfortable_range: 3-5
    source_ids: [DUNBAR_SOCIAL_LAYERS]

  close_operational_group:
    comfortable_range: 8-12
    source_ids: [DUNBAR_SOCIAL_LAYERS]

  residential_pod:
    comfortable_range: 12-24
    source_ids: [WHO_HOUSING_CROWDING_NCBI, COHOUSING_ASSOCIATION]

  neighborhood_cell:
    comfortable_range: 30-50
    source_ids: [DUNBAR_SOCIAL_LAYERS]

  village_block:
    comfortable_range: 50-150
    source_ids: [DUNBAR_SOCIAL_LAYERS, COHOUSING_ASSOCIATION]

  district:
    comfortable_range: 300-500
    source_ids: [DUNBAR_SOCIAL_LAYERS, NIST_COMMUNITY_RESILIENCE_GUIDE]

  town_city_layer:
    comfortable_range: 900-1500
    source_ids: [DUNBAR_SOCIAL_LAYERS]

  regional_membrane:
    comfortable_range: 1500+
    source_ids: [NIST_COMMUNITY_RESILIENCE_GUIDE, FEMA_NATIONAL_RESILIENCE_GUIDANCE]

core_CIaC_rule:
  - Do not scale one community indefinitely.
  - Replicate household/neighborhood cells before they become institutional.
  - Federate specialized services above the village-block layer.
```

---

## 5. Residential Life

```yaml
domain: residential_life
node_type: residential_pod
question: How many people can share one residential hall/building before privacy, stress, sleep quality, conflict, or perceived crowding degrade?
scale_action: hybrid

thresholds:
  emergency_minimum:
    value: not_applicable
    notes: Emergency sheltering standards are not appropriate as normal residential dignity standards.

  dignified_minimum:
    value: private_room_or_private_unit_with_retreat_capacity
    purpose: Each resident or household must have private, lockable retreat.

  comfortable_range:
    min: 12
    max: 24
    unit: residents_per_pod

  soft_threshold:
    value: 24
    unit: residents_per_pod
    action: warn_and_plan_duplication

  hard_threshold:
    value: 30
    unit: residents_per_pod
    action: duplicate_or_subdivide

  failure_threshold:
    condition: no_private_retreat_or_no_acoustic_sleep_protection
    action: fail

human_factor_driver:
  - privacy
  - sleep_quality
  - perceived_crowding
  - conflict_risk
  - acoustic_control

evidence_quality: moderate
translation_confidence: moderate
regulatory_strength: research_inferred
source_ids:
  - WHO_HOUSING_2018
  - WHO_HOUSING_CROWDING_NCBI
  - GREEN_HOUSE_SMALL_HOUSE
  - COHOUSING_ASSOCIATION

notes_for_CIaC:
  - Default residential pod should remain 12-24 residents.
  - High-care or elder pod should use 8-12 residents.
  - 80-person village block should be 4 residential pods of about 20.
  - Avoid one large residential hall.
optimizer_preference:
  - duplicate_residential_pod
  - add_pod_micro_commons
  - preserve_private_room_or_unit
ui_warning: Residential pod is exceeding comfortable cluster size. Add another pod or subdivide.
```

---

## 6. Mental Health and Social Scale

```yaml
domain: mental_health_social_scale
node_type: social_cell
question: What group sizes support stable familiarity, trust, belonging, informal care, and low social overload?
scale_action: hybrid

thresholds:
  emergency_minimum:
    value: not_applicable
    notes: Emergency group size does not define belonging.

  dignified_minimum:
    value: access_to_small_recurring_social_cell
    purpose: Resident should have a familiar local group smaller than whole settlement.

  comfortable_range:
    values:
      support_circle: 3-8
      working_circle: 5-12
      familiar_cell: 15-30
      neighborhood_cell: 30-50
      village_block: 50-150

  soft_threshold:
    value: 50
    unit: residents_without_subcells
    action: warn_social_overload

  hard_threshold:
    value: 150
    unit: residents_without_federation
    action: federate_and_duplicate_social_cells

  failure_threshold:
    condition: single_whole_population_social_identity_required_above_150
    action: fail

human_factor_driver:
  - trust
  - informal_care
  - social_overload
  - belonging
  - privacy

evidence_quality: moderate
translation_confidence: moderate
regulatory_strength: research_inferred
source_ids:
  - DUNBAR_SOCIAL_LAYERS
  - SURGEON_GENERAL_SOCIAL_CONNECTION
  - WHO_HOUSING_CROWDING_NCBI
  - COHOUSING_ASSOCIATION

notes_for_CIaC:
  - Use social cells, not one giant community.
  - Above 150, do not expect whole-community intimacy.
  - Above 300, use district capabilities and federation.
optimizer_preference:
  - duplicate_neighborhood_commons
  - federate_governance_and_care
  - preserve_small_social_cells
ui_warning: Whole-community familiarity is no longer a valid assumption. Add neighborhood cells and federated coordination.
```

---

## 7. Common House / Third Place

```yaml
domain: common_house_third_place
node_type: common_house
question: How large can a common house or shared dining hall get before it stops functioning as a socially comfortable commons?
scale_action: hybrid

thresholds:
  emergency_minimum:
    value: sheltered_gathering_space_for_emergency_floor
    notes: Emergency gathering space is not the same as normal third-place function.

  dignified_minimum:
    value: low_pressure_third_place_accessible_to_each_neighborhood
    purpose: Residents need optional common life without mandatory togetherness.

  comfortable_range:
    min: 50
    max: 100
    unit: residents_served_per_common_house

  soft_threshold:
    value: 100
    unit: residents_served
    action: warn_add_neighborhood_commons_or_subspaces

  hard_threshold:
    value: 150
    unit: residents_served_by_single_common_house
    action: duplicate_common_house_or_federate_district_venue

  failure_threshold:
    condition: one_common_house_is_sole_social_node_above_150
    action: fail

human_factor_driver:
  - belonging
  - third_place_comfort
  - clique_risk
  - social_overload
  - access

evidence_quality: low
translation_confidence: moderate
regulatory_strength: heuristic
source_ids:
  - COHOUSING_ASSOCIATION
  - SURGEON_GENERAL_SOCIAL_CONNECTION

notes_for_CIaC:
  - Common house can resize to village-block scale.
  - Above 150, duplicate neighborhood commons.
  - District venues can supplement but not replace local third places.
optimizer_preference:
  - duplicate_neighborhood_common_house
  - add_meal_waves
  - add_quiet_room
ui_warning: Common house is approaching institutional scale. Add neighborhood commons or meal waves.
```

---

## 8. Food Systems

```yaml
domain: food_systems
node_type: food_commons
question: Which food functions scale centrally, and which should duplicate by neighborhood?
scale_action: hybrid

thresholds:
  emergency_minimum:
    value: emergency_menu_and_food_buffer
    purpose: Maintain basic food floor during stress.

  dignified_minimum:
    value: neighborhood_food_access_with_private_food_autonomy
    purpose: Food access should not require institutional dining or mandatory meals.

  comfortable_range:
    min: 50
    max: 100
    unit: residents_per_food_commons

  soft_threshold:
    value: 80
    unit: residents_per_food_commons
    action: warn_for_labor_scheduling_hygiene_bottleneck

  hard_threshold:
    value: 150
    unit: residents_per_one_shared_kitchen_dining_node
    action: duplicate_kitchen_pickup_or_meal_waves

  failure_threshold:
    condition: shared_food_node_without_food_safety_logs_allergen_controls_cleaning_schedule_or_trained_backup
    action: fail

human_factor_driver:
  - food_safety
  - labor_burden
  - scheduling
  - dining_comfort
  - dignity

evidence_quality: moderate
translation_confidence: moderate
regulatory_strength: guideline
source_ids:
  - FDA_FOOD_CODE_2022
  - COHOUSING_ASSOCIATION

notes_for_CIaC:
  - Storage, procurement, and preservation can federate.
  - Neighborhood kitchens, dining, pickup, and food labor should duplicate.
  - Protein Commons should be local for acceptance and safety, but advanced protein production can federate.
optimizer_preference:
  - duplicate_food_commons
  - federate_procurement
  - add_preservation_node
ui_warning: Food commons is approaching kitchen, dining, labor, or hygiene bottleneck. Duplicate pickup or kitchen capacity.
```

---

## 9. Water Systems

```yaml
domain: water_systems
node_type: potable_water
question: Which water systems should duplicate for redundancy, which can scale centrally, and how do public-health rules change?
scale_action: hybrid

thresholds:
  emergency_minimum:
    value: 1
    unit: gallon_per_person_per_day
    duration_minimum: 3_days
    preferred_duration: 14_days
    source_ids:
      - CDC_EMERGENCY_WATER

  dignified_minimum:
    value: 20
    unit: liters_per_person_per_day
    context: essential_health_and_hygiene_reference
    source_ids:
      - WHO_EMERGENCY_WATER_20L

  comfortable_range:
    value: locally_modeled_normal_dignity_water_budget
    notes: Determined by water module, fixtures, climate, care needs, and food system.

  soft_threshold:
    value: 25
    unit: people_served
    action: trigger_public_water_system_review
    source_ids:
      - EPA_PUBLIC_WATER_SYSTEM

  hard_threshold:
    condition: serves_25_people_or_15_connections_without_public_health_review
    action: professional_public_health_legal_review_required
    source_ids:
      - EPA_PUBLIC_WATER_SYSTEM

  failure_threshold:
    condition: no_tested_potable_source_or_no_contamination_response_or_no_emergency_reserve
    action: fail

human_factor_driver:
  - public_health
  - redundancy
  - access
  - emergency_resilience
  - care_needs

evidence_quality: high
translation_confidence: high
regulatory_strength: binding
source_ids:
  - EPA_PUBLIC_WATER_SYSTEM
  - CDC_EMERGENCY_WATER
  - WHO_EMERGENCY_WATER_20L

notes_for_CIaC:
  - Duplicate emergency water distribution points locally.
  - Central treatment may scale only with professional/public-health review.
  - Public water system review is likely far below CIaC village-block scale.
optimizer_preference:
  - central_reviewed_source
  - duplicate_emergency_reserve
  - federate_operator_oversight
ui_warning: Population may trigger public-water-system review. Require legal and public-health review.
```

---

## 10. Sanitation and Waste

```yaml
domain: sanitation_waste
node_type: sanitation_access
question: Which sanitation functions must remain decentralized, and which waste systems can centralize?
scale_action: hybrid

thresholds:
  emergency_minimum:
    value: 1_toilet_per_20_people
    maximum_distance: 50_meters
    source_ids:
      - SPHERE_WASH
    notes: Emergency reference only, not CIaC normal dignity.

  dignified_minimum:
    value: private_or_semi_private_hygiene_access_with_handwashing
    purpose: Normal dignity requires closer, more private access than emergency WASH standards.

  comfortable_range:
    value: in_unit_or_pod_level_toilets_and_bathing
    purpose: Toilets and bathing should be local; compost/hazardous waste can centralize.

  soft_threshold:
    condition: shared_toilet_more_than_30_to_50_meters_from_dwelling
    action: warn

  hard_threshold:
    condition: emergency_toilet_standard_used_as_normal_design
    action: fail

  failure_threshold:
    condition: no_approved_blackwater_plan_or_no_accessible_toilets_or_no_handwashing
    action: fail

human_factor_driver:
  - hygiene
  - dignity
  - public_health
  - accessibility
  - pathogen_control

evidence_quality: high
translation_confidence: moderate
regulatory_strength: guideline
source_ids:
  - SPHERE_WASH
  - WHO_SANITATION_SAFETY_PLANNING

notes_for_CIaC:
  - Toilets, handwashing, bathing, and laundry need local access.
  - Compost processing, recycling, greywater treatment, and hazardous waste can centralize with controls.
  - UI must label emergency minimums separately from dignified normal.
optimizer_preference:
  - duplicate_hygiene_access
  - centralize_controlled_processing
ui_warning: Sanitation access is using emergency minimum logic. Add dignified local hygiene access.
```

---

## 11. Care and Health

```yaml
domain: care_health
node_type: care_room
question: How many people can one care room, clinic room, health steward, or care team reasonably support?
scale_action: hybrid

thresholds:
  emergency_minimum:
    value: first_aid_and_emergency_escalation
    purpose: Emergency response only.

  dignified_minimum:
    value: private_care_space_medication_continuity_and_transport_to_care
    purpose: Care should not require public exposure.

  comfortable_range:
    min: 50
    max: 100
    unit: residents_per_care_room

  soft_threshold:
    value: 100
    unit: residents_per_care_room
    action: warn_for_privacy_scheduling_illness_separation

  hard_threshold:
    value: 150
    unit: residents_per_care_node
    action: duplicate_care_room_or_add_neighborhood_care_points

  failure_threshold:
    condition: no_private_care_space_or_no_medication_continuity_or_no_high_need_support
    action: fail

human_factor_driver:
  - privacy
  - infection_control
  - elder_support
  - disability_support
  - medication_continuity

evidence_quality: moderate
translation_confidence: moderate
regulatory_strength: professional_practice
source_ids:
  - GREEN_HOUSE_SMALL_HOUSE
  - CDC_EMERGENCY_WATER
  - SURGEON_GENERAL_SOCIAL_CONNECTION

notes_for_CIaC:
  - High-care residential groups should be 8-12.
  - Care rooms duplicate by village block.
  - District or regional clinical partnerships federate.
optimizer_preference:
  - duplicate_care_room
  - federate_clinical_partnership
ui_warning: Care access, privacy, or illness separation may require another care room.
```

---

## 12. Governance

```yaml
domain: governance
node_type: governance_circle
question: What is the maximum useful size of a direct assembly before participation quality drops?
scale_action: federate

thresholds:
  emergency_minimum:
    value: emergency_roles_with_sunset_and_review
    purpose: Fast action during crisis, not permanent authority.

  dignified_minimum:
    value: due_process_role_backup_transparent_records
    purpose: Protect residents from capture and arbitrary decisions.

  comfortable_range:
    operational_group: 5-7
    circle: 5-12
    jury_or_appeal_panel: 12-24
    neighborhood_assembly: 30-80
    village_membership_body: 50-150

  soft_threshold:
    value: 80
    unit: direct_assembly_participants
    action: warn_participation_quality

  hard_threshold:
    value: 150
    unit: residents_under_one_direct_assembly_for_routine_decisions
    action: federate_into_circles_and_neighborhood_assemblies

  failure_threshold:
    condition: one_role_controls_money_records_conflict_or_survival_system
    action: fail

human_factor_driver:
  - participation_quality
  - anti_capture
  - conflict_resolution
  - meeting_burden
  - legitimacy

evidence_quality: moderate
translation_confidence: moderate
regulatory_strength: research_inferred
source_ids:
  - DUNBAR_SOCIAL_LAYERS

notes_for_CIaC:
  - Whole-membership voting can remain for constitutional decisions.
  - Routine operations should move to circles/roles before 150 residents.
optimizer_preference:
  - federate_governance
  - create_operational_circles
  - preserve_member_rights_for_constitutional_matters
ui_warning: Direct assembly burden rising. Federate into circles or delegated roles.
```

---

## 13. Maintenance and Tools

```yaml
domain: maintenance_tools
node_type: tool_library_and_maintenance_node
question: What maintenance shops, tool libraries, spare parts stores, and repair teams can scale centrally?
scale_action: hybrid

thresholds:
  emergency_minimum:
    value: local_emergency_tools_and_professional_contacts
    purpose: Prevent critical failures from waiting on distant tools or one expert.

  dignified_minimum:
    value: local_tool_cache_asset_registry_spares_and_professional_handoff
    purpose: Residents should not depend on hidden experts or unavailable tools.

  comfortable_range:
    local_tool_cache: 50-150_residents
    central_workshop: 150-500_residents
    advanced_fabrication: 300-1500_residents

  soft_threshold:
    value: 150
    unit: residents_per_tool_cache_or_workshop
    action: warn_for_bottleneck

  hard_threshold:
    value: 500
    unit: residents_without_district_workshop_or_federation
    action: federate_advanced_maintenance

  failure_threshold:
    condition: no_asset_registry_or_no_critical_spares_or_no_professional_handoff
    action: fail

human_factor_driver:
  - response_time
  - autonomy
  - repairability
  - safety
  - skill_coverage

evidence_quality: low
translation_confidence: moderate
regulatory_strength: professional_practice
source_ids:
  - NIST_COMMUNITY_RESILIENCE_GUIDE

notes_for_CIaC:
  - Daily/common tools should duplicate locally.
  - Advanced workshop functions can federate.
  - Emergency Class A repair supplies should be local.
optimizer_preference:
  - duplicate_local_tool_cache
  - federate_advanced_workshop
ui_warning: One workshop/tool node is serving too many residents. Add local tool cache or district workshop.
```

---

## 14. Mobility and Access

```yaml
domain: mobility_access
node_type: daily_need_access
question: What should be within 1 minute, 3 minutes, 5 minutes, 10 minutes, and 15 minutes?
scale_action: hybrid

thresholds:
  emergency_minimum:
    value: accessible_evacuation_and_emergency_access
    purpose: Residents must be reachable in crisis.

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
    condition: essential_functions_exceed_3_to_5_minutes_for_high_need_residents
    action: warn

  hard_threshold:
    condition: no_accessible_route_to_essential_spaces_or_non_drivers_cannot_access_food_care_pharmacy_clinic
    action: fail

  failure_threshold:
    condition: transportation_costs_erase_housing_savings
    action: warn_or_fail_based_on_severity

human_factor_driver:
  - accessibility
  - disability
  - elder_support
  - time_burden
  - emergency_access

evidence_quality: high
translation_confidence: moderate
regulatory_strength: guideline
source_ids:
  - ITDP_TOD_STANDARD
  - ACCESS_BOARD_ADA_STANDARDS

notes_for_CIaC:
  - Internal daily needs should be closer than TOD transit metrics.
  - 10-minute threshold applies to transit/district functions, not toilets or food access.
optimizer_preference:
  - duplicate_neighborhood_center
  - reduce_accessible_distance_penalty
  - add_shared_mobility_if_external_access_weak
ui_warning: Essential daily functions exceed walk/roll threshold, especially for high-need residents.
```

---

## 15. Education, Skill, and Work

```yaml
domain: education_skill_work
node_type: skill_lattice
question: What learning group sizes work best for skill-sharing, apprenticeships, childcare, workshops, and peer learning?
scale_action: hybrid

thresholds:
  emergency_minimum:
    value: safety_orientation_and_emergency_role_training
    purpose: Residents must know how to avoid harm and get help.

  dignified_minimum:
    value: onboarding_skill_graph_training_gates_and_backup_roles
    purpose: No one should decode the commons by social osmosis.

  comfortable_range:
    peer_learning_group: 3-6
    hands_on_skill_group: 4-8
    apprenticeship_ratio: 1_mentor_to_1_to_3_learners
    workshop_class: 8-12

  soft_threshold:
    value: 8
    unit: learners_in_hands_on_safety_training
    action: warn_split_group

  hard_threshold:
    condition: safety_critical_task_without_training_gate_or_one_expert_without_backup
    action: fail

  failure_threshold:
    condition: training_burden_hidden_from_labor_time_model
    action: fail

human_factor_driver:
  - safety
  - competence
  - expert_dependency
  - learning_burden
  - resident_autonomy

evidence_quality: moderate
translation_confidence: moderate
regulatory_strength: professional_practice
source_ids:
  - NAEYC_RATIOS_GROUP_SIZE

notes_for_CIaC:
  - Local skill nodes should duplicate for onboarding and safety.
  - Advanced credentials can federate through partnerships.
optimizer_preference:
  - duplicate_local_skill_node
  - federate_advanced_training
ui_warning: Safety-critical roles lack trained backups or training group is too large.
```

---

## 16. Emergency and Resilience

```yaml
domain: emergency_resilience
node_type: risk_resilience_cell
question: Which systems should duplicate specifically for failure isolation, not daily efficiency?
scale_action: hybrid

thresholds:
  emergency_minimum:
    value:
      - water_buffer
      - food_buffer
      - critical_energy
      - emergency_sanitation
      - first_aid
      - communications
      - role_backup

  dignified_minimum:
    value:
      - hazard_register
      - dependency_graph
      - emergency_modes
      - high_need_resident_plan
      - recovery_plan
      - emergency_authority_sunset

  comfortable_range:
    local_buffers: village_block
    district_coordination: 300+
    regional_membrane: 1500+

  soft_threshold:
    value: 150
    unit: residents_without_replicated_buffers
    action: warn

  hard_threshold:
    value: 300
    unit: residents_without_district_coordination
    action: federate

  failure_threshold:
    condition: no_hazard_register_or_no_dependency_graph_or_no_recovery_plan_or_no_high_need_emergency_plan
    action: fail

human_factor_driver:
  - failure_isolation
  - cascade_prevention
  - high_need_support
  - recovery
  - anti_capture_under_stress

evidence_quality: high
translation_confidence: moderate
regulatory_strength: guideline
source_ids:
  - NIST_COMMUNITY_RESILIENCE_GUIDE
  - FEMA_NATIONAL_RESILIENCE_GUIDANCE
  - SENDAI_FRAMEWORK

notes_for_CIaC:
  - Fallback systems should duplicate more than normal efficiency systems.
  - Local buffers protect the floor; federation coordinates specialized response.
optimizer_preference:
  - duplicate_local_buffers
  - federate_resilience_coordination
ui_warning: Critical function depends on one node, role, or external provider.
```

---

## 17. CIaC Translation Matrix

| Module | Natural scaling type | Base node | Soft threshold | Hard threshold | Service-radius constraint | Primary driver | Optimizer preference |
|---|---:|---:|---:|---:|---|---|---|
| Residential pods | duplicate | 12-24 residents | 24/pod | 30/pod, 150/block | 1-3 min to pod commons | privacy, sleep, crowding | duplicate pod |
| Village block | hybrid | 50-150 residents | 100 | 150 | 3-5 min to essentials | familiarity, governance, access | replicate block |
| Common house | hybrid | 50-100 residents | 100 | 150 | 3-5 min | social comfort, access | duplicate neighborhood commons |
| Shared dining | duplicate/hybrid | 24-60 diners/wave | 60 | 100-150 | 3-5 min or pickup | institutional feel, labor | meal waves + duplicate dining |
| Food commons | hybrid | 50-100 residents | 80 | 150 | 3-5 min to pickup | labor, hygiene, food safety | duplicate kitchen/pickup; federate procurement |
| Protein commons | hybrid | 50-100 residents | 80 | 150 | food node adjacent | safety, acceptance, labor | duplicate simple layers; federate advanced protein |
| Potable water | hybrid | 50-150 local distribution | 25 triggers review | no tested source | 1-3 min emergency point | public health, redundancy | central reviewed source + duplicate reserves |
| Sanitation | duplicate/hybrid | toilets local, treatment central | 20 people/toilet emergency | emergency standard used as normal | ideally 1-3 min, emergency max 50m | hygiene, dignity | duplicate access; centralize treatment |
| Care room | duplicate/federate | 50-100 residents | 100 | 150 | 3-5 min | privacy, infection, high-need support | duplicate care rooms; federate clinic |
| Governance circle | federate | 5-12 | 12 | 24 for deliberation, 150 direct assembly | N/A | participation quality | circles + councils |
| Maintenance/tools | hybrid | 50-150 local cache | 150 | 300-500 without district workshop | 1-3 min daily tools | response time, autonomy | duplicate caches; federate advanced shop |
| Mobility/access | hybrid | village block | essentials >5 min | no accessible essential route | 1/3/5/10 min tiers | access, disability, time burden | duplicate centers before long travel |
| Education/skill | hybrid | 50-150 learning cell | 8 hands-on learners | no backup skill | 3-5 min for local learning | safety, competence | duplicate local skill nodes; federate credentials |
| Social/cultural | duplicate/hybrid | 30-80 social cell | 100 | 150 | 3-5 min | belonging, opt-out, clique risk | duplicate social nodes |
| Risk/resilience | hybrid | village block cell | 150 | 300 district needed | buffers local | cascade, recovery | duplicate buffers, federate coordination |

---

## 18. UI Warning Language

```yaml
warnings:
  residential_pod_over_soft:
    message: Residential pod is exceeding comfortable cluster size. Add another pod or subdivide.

  common_house_over_soft:
    message: Common house is approaching institutional scale. Add neighborhood commons or meal waves.

  food_node_over_soft:
    message: Food commons is approaching kitchen/labor bottleneck. Duplicate pickup/kitchen capacity.

  water_review_trigger:
    message: Population may trigger public-water-system review. Require legal/public-health review.

  sanitation_access_warning:
    message: Toilets or hygiene access are using emergency-minimum logic or exceed dignity thresholds.

  care_node_warning:
    message: Care access, privacy, or illness separation may require another care room.

  governance_over_soft:
    message: Direct assembly burden rising. Federate into circles or delegated roles.

  maintenance_bottleneck:
    message: One workshop/tool node is serving too many residents. Add local tool cache or district workshop.

  mobility_distance_warning:
    message: Essential daily functions exceed walk/roll threshold, especially for high-need residents.

  education_skill_warning:
    message: Safety-critical roles lack trained backups or training group is too large.

  resilience_single_point_failure:
    message: Critical function depends on one node, role, or external provider.
```

---

## 19. Recommended Next Research Parts

```yaml
part_2_update:
  title: Residential, mental health, common house, and social architecture
  required_changes:
    - use same normalized fields
    - add source IDs
    - split emergency/dignified/comfortable/failure thresholds

part_3:
  title: Food, water, sanitation, and care service nodes
  focus:
    - service radius
    - public health thresholds
    - local duplication vs centralization
    - regulatory transitions

part_4:
  title: Governance, education, maintenance, mobility, and resilience
  focus:
    - group decision thresholds
    - training sizes
    - maintenance service layers
    - emergency duplication
    - federation thresholds

part_5:
  title: Repo implementation translation
  focus:
    - scaling_policy.schema.json
    - scale_policies/ciac_scaling_policy_v0.yaml
    - node_scaling policy loader
    - topology optimizer preferences
    - UI warnings
    - tests
```

---

## 20. Status

```yaml
status: approved_as_research_input
not_yet:
  - final_verified_policy
  - optimizer_safe_without_schema
  - legally_or_professionally_reviewed
next_step:
  - create_scaling_policy_schema_and_machine_readable_yaml
```
