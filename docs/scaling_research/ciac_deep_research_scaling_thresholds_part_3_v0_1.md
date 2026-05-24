# CIaC Deep Research Part 3, Food, Water, Sanitation, and Care Service Nodes

**Research ID:** `ciac_scaling_thresholds_part_3_v0_1`  
**Parent:** `ciac_scaling_thresholds_part_1_v0_2` and `ciac_scaling_thresholds_part_2_v0_2`  
**Purpose:** Deepen service-infrastructure thresholds for food, water, sanitation/waste, and care/health.  
**Status:** Research synthesis for CIaC scaling policy, not final verified policy, engineering, legal, public-health, food-safety, plumbing, medical, or code certification.  
**Primary CIaC use:** refine `food`, `protein_commons`, `water`, `sanitation_waste`, `care_health`, `risk_resilience`, `node_scaling`, `topology_optimizer`, world viewer warnings, and optimizer action preferences.

---

## 0. What This Part Covers

```yaml
covered_domains:
  - food_systems
  - protein_commons_interfaces
  - water_systems
  - sanitation_and_waste
  - care_and_health

primary_questions:
  - Which functions scale centrally?
  - Which functions must duplicate locally?
  - Which thresholds are emergency-only versus dignified-normal?
  - Which thresholds trigger public-health, food-safety, medical, or legal review?
  - Which service-radius assumptions should CIaC use?
  - Which functions should the optimizer resize, duplicate, federate, or handle as hybrid systems?
```

---

## 1. Method and Evidence Normalization

This part uses the same normalized fields adopted in Part 1 v0.2 and Part 2 v0.2.

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

Threshold fields are separated as:

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
  - id: FDA_FOOD_CODE_2022
    title: FDA Food Code 2022
    organization: U.S. Food and Drug Administration
    url: https://www.fda.gov/food/fda-food-code/food-code-2022
    supports:
      - food_service_public_health_model
      - time_temperature_control
      - date_marking
      - cleaning_sanitizing
      - allergen_and_food_safety_controls

  - id: FDA_FOOD_CODE_CHANGES_2022
    title: Summary of Changes in the 2022 FDA Food Code
    organization: U.S. Food and Drug Administration
    url: https://www.fda.gov/food/fda-food-code/summary-changes-2022-fda-food-code
    supports:
      - ready_to_eat_TCS_date_marking
      - records_and_disposition_logic

  - id: USDA_SHARED_KITCHENS
    title: Shared Kitchens and Food Startups
    organization: USDA Agricultural Marketing Service
    url: https://www.ams.usda.gov/services/local-regional/research-publications/shared-kitchens-and-food-startups
    supports:
      - shared_kitchens_as_local_food_infrastructure
      - shared_kitchens_reduce_barriers_to_facilities_and_capital

  - id: USDA_LOCAL_REGIONAL_RESOURCES
    title: Local and Regional Food System Resources
    organization: USDA Agricultural Marketing Service
    url: https://www.ams.usda.gov/services/local-regional/research-publications/resources
    supports:
      - local_regional_food_system_resilience
      - food_hubs
      - shared_kitchens
      - regional_supply_chains

  - id: SHARED_KITCHEN_HAZARDS_2024
    title: Assessment of Hygiene Management Practices and Microbial/Chemical Hazards in Shared Kitchen Facilities
    organization: peer_reviewed_literature
    year: 2024
    url: https://pmc.ncbi.nlm.nih.gov/articles/PMC10969530/
    supports:
      - shared_kitchen_hygiene_management_risk
      - need_for_monitoring_and_food_safety_controls

  - id: EPA_PUBLIC_WATER_SYSTEM
    title: Information about Public Water Systems
    organization: U.S. Environmental Protection Agency
    url: https://www.epa.gov/dwreginfo/information-about-public-water-systems
    supports:
      - public_water_system_15_connections_or_25_people_60_days
      - public_or_private_ownership_does_not_avoid_PWS_category

  - id: EPA_PRIVATE_WELLS
    title: Protect Your Home's Water
    organization: U.S. Environmental Protection Agency
    url: https://www.epa.gov/privatewells/protect-your-homes-water
    supports:
      - annual_private_well_testing_total_coliform_nitrates_TDS_pH
      - local_contaminant_testing
      - owner_responsibility_for_private_well_safety

  - id: CDC_WELL_TESTING
    title: Guidelines for Testing Well Water
    organization: U.S. Centers for Disease Control and Prevention
    url: https://www.cdc.gov/drinking-water/safety/guidelines-for-testing-well-water.html
    supports:
      - annual_well_testing_total_coliform_nitrates_TDS_pH
      - state_certified_lab
      - local_health_department_guidance

  - id: CDC_EMERGENCY_WATER
    title: How to Create an Emergency Water Supply
    organization: U.S. Centers for Disease Control and Prevention
    url: https://www.cdc.gov/water-emergency/about/how-to-create-and-store-an-emergency-water-supply.html
    supports:
      - one_gallon_per_person_per_day
      - three_day_minimum
      - two_week_supply_if_possible
      - higher_need_profiles_need_more_water

  - id: WHO_EMERGENCY_WATER_20L
    title: How much water is needed in emergencies
    organization: World Health Organization
    url: https://cdn.who.int/media/docs/default-source/wash-documents/who-tn-09-how-much-water-is-needed.pdf
    supports:
      - twenty_liters_per_person_per_day_for_minimum_essential_health_and_hygiene

  - id: EPA_ONSITE_NONPOTABLE_REUSE
    title: Onsite Non-Potable Water Reuse Research
    organization: U.S. Environmental Protection Agency
    url: https://www.epa.gov/water-research/onsite-non-potable-water-reuse-research
    supports:
      - onsite_reuse_sources_wastewater_greywater_stormwater_roof_rainwater
      - non_drinking_reuse
      - need_for_risk_based_treatment

  - id: NSF_ANSI_350_REUSE
    title: NSF/ANSI 350 Onsite Residential and Commercial Water Reuse Treatment Systems
    organization: NSF / Water Quality Association summary
    url: https://wqa.org/wp-content/uploads/2022/09/2014_WaterReuse.pdf
    supports:
      - onsite_reuse_systems_need_evaluation
      - reuse_treatment_standard_reference

  - id: SPHERE_WASH_2018
    title: Sphere Handbook 2018, WASH Standards
    organization: Sphere Association
    url: https://spherestandards.org/wp-content/uploads/Sphere-Handbook-2018-EN.pdf
    supports:
      - WASH_minimum_standards
      - emergency_toilet_ratio_and_access_context

  - id: SPHERE_TOILET_20_50
    title: Sphere WASH guidance, toilet ratio and distance
    organization: Sphere / humanitarian WASH references
    url: https://ec.europa.eu/echo/files/evaluation/watsan2005/annex_files/Sphere/SPHERE2%20-%20chapter%202%20-%20Min%20standards%20in%20water%2C%20sanitation%20and%20hygiene%20prom.pdf
    supports:
      - maximum_20_people_per_toilet
      - toilets_no_more_than_50_m_from_dwellings
      - emergency_minimum_not_normal_dignity

  - id: UNHCR_WATSAN_20_LATRINE
    title: UNHCR Water and Sanitation Guidelines
    organization: UNHCR
    url: https://www.unhcr.org/sites/default/files/legacy-pdf/49d080df2.pdf
    supports:
      - maximum_20_people_per_communal_latrine
      - sanitation_emergency_access_guidance

  - id: WHO_SANITATION_SAFETY_PLANNING
    title: Sanitation Safety Planning
    organization: World Health Organization
    url: https://www.who.int/publications/i/item/9789241549240
    supports:
      - sanitation_chain_risk_management
      - containment_conveyance_treatment_reuse_disposal
      - health_risk_based_sanitation_management

  - id: CDC_HUMAN_WASTE_WORKER_SAFETY
    title: Workers Handling Human Waste or Sewage
    organization: U.S. Centers for Disease Control and Prevention
    url: https://www.cdc.gov/global-water-sanitation-hygiene/about/workers_handlingwaste.html
    supports:
      - PPE_training_handwashing_for_human_waste_handling
      - worker_exposure_controls

  - id: EPA_SEPTIC
    title: Septic Systems Overview
    organization: U.S. Environmental Protection Agency
    url: https://www.epa.gov/septic
    supports:
      - onsite_wastewater_requires_design_maintenance_public_health_protection

  - id: GREEN_HOUSE_MODEL
    title: The Green House Model of Nursing Home Care in Design and Implementation
    organization: peer_reviewed_literature / PMC
    url: https://pmc.ncbi.nlm.nih.gov/articles/PMC5338211/
    supports:
      - green_house_homes_house_10_to_12_elders
      - private_room_and_attached_bath
      - shared_central_living_space_and_open_kitchen

  - id: CDC_DISABILITY_EMERGENCY_KIT
    title: Building an Emergency Kit for People with Disabilities
    organization: U.S. Centers for Disease Control and Prevention
    url: https://www.cdc.gov/disability-emergency-preparedness/people-with-disabilities/build-a-kit.html
    supports:
      - one_week_prescription_medication_supply
      - cooler_for_refrigerated_medications
      - batteries_and_chargers_for_assistive_devices
      - mobility_devices_and_health_documents

  - id: HRSA_HEALTH_CENTER_PROGRAM
    title: About the Health Center Program
    organization: Health Resources and Services Administration
    url: https://bphc.hrsa.gov/about-health-center-program
    supports:
      - health_centers_provide_access_to_medical_dental_behavioral_vision_services
      - community_based_health_care_access

  - id: CDC_CHW_PREVENTING_CHRONIC_DISEASE
    title: Emerging Model for Community Health Worker-Based Chronic Care Management
    organization: CDC / Preventing Chronic Disease
    url: https://www.cdc.gov/pcd/issues/2020/19_0316.htm
    supports:
      - community_health_workers_can_provide_behavioral_support_and_care_navigation

  - id: IMPACT_CHW_RCT
    title: Evidence-Based Community Health Worker Program Addresses Unmet Social Needs
    organization: peer_reviewed_literature / PMC
    url: https://pmc.ncbi.nlm.nih.gov/articles/PMC8564553/
    supports:
      - structured_CHW_programs_can_improve_outcomes_and_return_on_investment
```

---

## 3. Executive Translation Summary

```yaml
food:
  natural_scaling_type: hybrid
  duplicate_locally:
    - neighborhood_kitchens
    - dining_or_meal_pickup
    - garden_plots
    - compost_collection
    - care_meal_distribution
  centralize_or_federate:
    - procurement
    - bulk_storage
    - cold_storage
    - preservation
    - food_safety_training
    - district_processing
  base_node: 50-100 residents
  soft_threshold: 80 residents
  hard_threshold: 150 residents per kitchen/dining node

water:
  natural_scaling_type: hybrid
  duplicate_locally:
    - emergency_distribution_points
    - storage/reserve access
    - shutoffs and sampling points
  centralize_or_federate:
    - treatment
    - testing oversight
    - professional operations
    - public-water-system compliance
  soft_threshold: 25 people served by drinking-water system
  hard_threshold: any PWS-scale system without review
  reserve_reference: 1 gallon/person/day emergency, 14 days preferred if possible

sanitation_waste:
  natural_scaling_type: hybrid
  duplicate_locally:
    - toilets
    - bathing
    - handwashing
    - laundry access
    - waste dropoff
  centralize_or_federate:
    - wastewater treatment
    - compost processing
    - recycling
    - hazardous waste
    - greywater treatment
  emergency_reference: 1 toilet per 20 people, maximum 50 m from dwelling
  CIaC_normal: much closer, private/semi-private, accessible

care_health:
  natural_scaling_type: hybrid
  duplicate_locally:
    - care rooms
    - check-in points
    - medication support
    - first aid
    - care meal distribution
  federate:
    - clinics
    - professional care
    - pharmacy partnerships
    - behavioral health
    - disability/aging services
  base_node: 50-100 residents
  hard_threshold: 150 residents without duplicated care room or neighborhood care access
```

---

# FOOD SYSTEMS

## 4. Food Function Scaling, Central vs Local

```yaml
domain: food_systems
node_type: food_commons_function_stack
question: Which food functions scale centrally, and which should duplicate by neighborhood?
scale_action: hybrid

thresholds:
  emergency_minimum:
    value: emergency_menu_and_protein_floor
    purpose: basic food continuity during stress
    source_ids:
      - FDA_FOOD_CODE_2022

  dignified_minimum:
    value: neighborhood_food_access_private_food_autonomy_and_opt_in_common_meals
    purpose: food should not require institutional dining or mandatory togetherness

  comfortable_range:
    local_food_commons:
      min: 50
      max: 100
      unit: residents_per_food_node
    dining_wave:
      min: 24
      max: 60
      unit: diners_per_wave
    district_procurement_storage:
      min: 150
      max: 500
      unit: residents_supported
    district_processing_preservation:
      min: 300
      max: 1500
      unit: residents_supported

  soft_threshold:
    value: 80
    unit: residents_per_food_commons
    action: warn_for_kitchen_dining_labor_and_food_safety_bottleneck

  hard_threshold:
    value: 150
    unit: residents_per_single_shared_kitchen_dining_node
    action: duplicate_food_node_or_federate_food_service

  failure_threshold:
    condition: shared_food_node_without_food_safety_logs_allergen_controls_cleaning_schedule_trained_backup_or_private_food_autonomy
    action: fail

human_factor_driver:
  - food_safety
  - kitchen_labor
  - dining_comfort
  - scheduling
  - private_food_autonomy
  - care_meal_reliability

evidence_quality: moderate
translation_confidence: moderate
regulatory_strength: guideline
source_ids:
  - FDA_FOOD_CODE_2022
  - FDA_FOOD_CODE_CHANGES_2022
  - USDA_SHARED_KITCHENS
  - SHARED_KITCHEN_HAZARDS_2024

notes_for_CIaC:
  - Procurement, bulk dry storage, preservation, and cold storage can centralize more than cooking and dining.
  - Kitchen production can resize somewhat, but dining/social experience should duplicate by neighborhood.
  - Meal pickup points should duplicate earlier than procurement.
  - Food-safety operations must become more formal as population and kitchen complexity rise.

optimizer_preference:
  - duplicate_neighborhood_food_node_when_over_80_to_100
  - add_meal_waves_before_one_large_dining_hall
  - federate_procurement_and_preservation_at_300_plus
  - keep_private_food_autonomy
ui_warning: Food commons is approaching kitchen, dining, labor, hygiene, or food-safety bottleneck. Duplicate local food access or federate back-end food logistics.
```

---

## 5. Shared Kitchen Bottleneck

```yaml
domain: food_systems
node_type: shared_kitchen
question: At what population does one shared kitchen become a bottleneck for labor, hygiene, scheduling, or food safety?
scale_action: hybrid

thresholds:
  emergency_minimum:
    value: limited_emergency_meal_production
    purpose: emergency feeding only; not normal food dignity

  dignified_minimum:
    value: safe_shared_kitchen_plus_private_food_autonomy
    purpose: no resident should be forced into one kitchen schedule to eat

  comfortable_range:
    min: 50
    max: 80
    unit: residents_per_shared_kitchen_for_common_meal_operations

  soft_threshold:
    value: 80
    unit: residents
    action: warn_for_labor_scheduling_and_cleaning_load

  hard_threshold:
    value: 100
    unit: residents
    action: require_meal_waves_pickup_or_second_kitchen

  failure_threshold:
    condition: one_shared_kitchen_supports_150_plus_residents_without_formal_food_safety_operations_and_redundant_access
    action: fail_or_professional_review_required

human_factor_driver:
  - labor
  - hygiene
  - scheduling
  - food_safety
  - resident_autonomy

evidence_quality: moderate
translation_confidence: moderate
regulatory_strength: guideline
source_ids:
  - FDA_FOOD_CODE_2022
  - USDA_SHARED_KITCHENS
  - SHARED_KITCHEN_HAZARDS_2024
  - FDA_FOOD_CODE_CHANGES_2022

notes_for_CIaC:
  - The limit is not just equipment capacity; it is cleaning, safe holding/cooling, scheduling, storage, allergen controls, and labor.
  - Food service may be centralized for production, but social dining and pickup should duplicate.
  - At higher scale, model kitchen as a licensed/shared-use or institutional food operation requiring local review.

optimizer_preference:
  - add_second_kitchen_or_satellite_pickup
  - add_food_safety_steward_and_backup
  - add_meal_waves
  - do_not_solve_by_increasing_one_dining_hall_indefinitely

ui_warning: Shared kitchen is becoming a labor, schedule, cleaning, or food-safety bottleneck.
```

---

## 6. Food Service Radius and Delivery

```yaml
domain: food_systems
node_type: food_service_radius
question: What is the evidence for kitchen, dining, meal pickup, and food-service radius limits?
scale_action: duplicate

thresholds:
  emergency_minimum:
    value: food_distribution_point_reachable_by_all_residents
    purpose: emergency access during stress

  dignified_minimum:
    value:
      meal_pickup_or_common_dining: within_3_to_5_minutes_walk_or_roll
      care_meal_delivery: door_or_pod_level_delivery
      bulk_food_delivery: service_edge_access

  comfortable_range:
    common_meal_dining: 2_to_5_minutes
    meal_pickup: 1_to_3_minutes_where_possible
    pantry_access: 3_to_5_minutes
    garden_to_kitchen_route: short_cart_route

  soft_threshold:
    condition: food_pickup_or_common_meal_exceeds_5_minutes_for_high_need_residents
    action: warn_and_add_pickup_node

  hard_threshold:
    condition: non_drivers_or_high_need_residents_cannot_access_food_without_informal_help
    action: fail

  failure_threshold:
    condition: care_meal_delivery_not_modeled_for_illness_injury_elder_or_disability_scenarios
    action: fail

human_factor_driver:
  - food_access
  - care
  - mobility
  - labor
  - dignity

evidence_quality: low
translation_confidence: moderate
regulatory_strength: heuristic
source_ids:
  - ITDP_TOD_STANDARD
  - ACCESS_BOARD_ADA_STANDARDS
  - CDC_DISABILITY_EMERGENCY_KIT

notes_for_CIaC:
  - There is not a strong food-specific radius standard; use CIaC internal mobility thresholds.
  - Food access should be more local than transit access.
  - For stress scenarios, model delivery to unit or pod for sick/high-need residents.

optimizer_preference:
  - duplicate_meal_pickup_points
  - shorten_accessible_food_routes
  - model_care_meal_delivery
ui_warning: Food access exceeds walk/roll threshold for high-need residents. Add meal pickup or delivery node.
```

---

## 7. Food Storage, Procurement, Preservation, and Cold Storage

```yaml
domain: food_systems
node_type: food_back_end
question: Which food functions can scale centrally?
scale_action: federate

thresholds:
  emergency_minimum:
    value: food_buffer_and_emergency_menu
    purpose: maintain food floor through supply disruption

  dignified_minimum:
    value: inventory_visibility_storage_rotation_and_private_food_autonomy
    purpose: avoid waste, coercion, and hidden food insecurity

  comfortable_range:
    village_block:
      dry_storage: local
      cold_storage: local_or_local_plus_district
      preservation: local_small_scale
    district:
      procurement: federated
      bulk_storage: federated
      preservation: federated
      commercial_scale_processing: professional_review
    town_city:
      logistics_and_supplier_diversity: federated

  soft_threshold:
    value: 150
    unit: residents
    action: add_procurement_and_storage_coordination

  hard_threshold:
    value: 300
    unit: residents
    action: district_food_logistics_required

  failure_threshold:
    condition: food_buffer_inventory_or_cold_storage_depend_on_one_room_one_power_source_or_one_operator
    action: fail_or_warn_based_on_resource_criticality

human_factor_driver:
  - resilience
  - waste_reduction
  - food_safety
  - procurement_efficiency
  - labor

evidence_quality: moderate
translation_confidence: moderate
regulatory_strength: professional_practice
source_ids:
  - USDA_LOCAL_REGIONAL_RESOURCES
  - USDA_SHARED_KITCHENS
  - FDA_FOOD_CODE_2022

notes_for_CIaC:
  - Back-end food logistics can scale more than social food life.
  - Cold storage needs energy resilience and monitoring.
  - District food logistics should not erase local food autonomy.

optimizer_preference:
  - federate_procurement_above_150_to_300
  - keep_neighborhood_pickup_and_dining_local
  - duplicate_critical_cold_storage_or_backup
ui_warning: Food storage/procurement has reached district scale. Add federated logistics without centralizing daily food life.
```

---

## 8. Protein Commons Scaling

```yaml
domain: protein_commons
node_type: local_protein_system
question: Which protein functions should duplicate locally and which can federate?
scale_action: hybrid

thresholds:
  emergency_minimum:
    value: emergency_protein_floor
    purpose: protein remains available during crop or supply failure

  dignified_minimum:
    value: diet_level_complete_protein_with_acceptance_and_opt_out
    purpose: residents must meet needs without coercion or hidden novel proteins

  comfortable_range:
    local_legume_soy_fermentation_duckweed_node: 50-100_residents
    district_advanced_fermentation_or_processing: 300-1500_residents
    future_microbial_protein: federation_or_regional_scale

  soft_threshold:
    value: 80
    unit: residents_per_local_protein_commons
    action: warn_for_operator_labor_and_food_safety_load

  hard_threshold:
    value: 150
    unit: residents_per_local_protein_system
    action: duplicate_or_federate

  failure_threshold:
    condition: protein_plan_lacks_amino_acid_digestibility_safety_acceptance_or_input_dependency_model
    action: fail

human_factor_driver:
  - nutrition
  - food_safety
  - resident_acceptance
  - ethics
  - input_dependency
  - labor

evidence_quality: moderate
translation_confidence: moderate
regulatory_strength: research_inferred
source_ids:
  - FDA_FOOD_CODE_2022
  - SHARED_KITCHEN_HAZARDS_2024
  - USDA_LOCAL_REGIONAL_RESOURCES

notes_for_CIaC:
  - Legume/soy/fermentation/duckweed layers can be local at village-block scale.
  - Advanced mycoprotein or microbial protein should federate until operationally simple and reviewed.
  - Insects remain optional and consent-gated.

optimizer_preference:
  - duplicate_simple_local_protein_node
  - federate_advanced_bioreactor_or_processing
  - preserve_opt_out
ui_warning: Protein Commons is exceeding local safe/accepted/labor-manageable scale. Duplicate simple layers or federate advanced production.
```

---

# WATER SYSTEMS

## 9. Public Water System Review Threshold

```yaml
domain: water_systems
node_type: potable_water_regulatory_threshold
question: How do public-health rules change as water service scales from household/community to public utility?
scale_action: federate

thresholds:
  emergency_minimum:
    value: safe_emergency_drinking_water
    source_ids:
      - CDC_EMERGENCY_WATER

  dignified_minimum:
    value: tested_potable_source_with_clear_status_and_fallback
    source_ids:
      - EPA_PRIVATE_WELLS
      - CDC_WELL_TESTING

  comfortable_range:
    value: professionally_reviewed_potable_system_appropriate_to_population

  soft_threshold:
    value: 25
    unit: people_served_by_drinking_water_system
    action: trigger_public_water_system_review
    source_ids:
      - EPA_PUBLIC_WATER_SYSTEM

  hard_threshold:
    condition: 15_service_connections_or_25_people_for_60_days_without_public_water_system_review
    action: fail_or_block_until_public_health_legal_review
    source_ids:
      - EPA_PUBLIC_WATER_SYSTEM

  failure_threshold:
    condition: no_tested_source_no_contamination_plan_or_no_alternate_supply
    action: fail

human_factor_driver:
  - public_health
  - legal_compliance
  - safety
  - trust
  - resilience

evidence_quality: high
translation_confidence: high
regulatory_strength: binding
source_ids:
  - EPA_PUBLIC_WATER_SYSTEM
  - EPA_PRIVATE_WELLS
  - CDC_WELL_TESTING

notes_for_CIaC:
  - A CIaC village block almost certainly exceeds the 25-person review trigger if it operates its own drinking-water system.
  - Public/private ownership does not avoid the PWS definition.
  - If connected to municipal water, model shifts to service agreement/resilience rather than private source responsibility.

optimizer_preference:
  - require_public_health_review
  - federate_operator_oversight
  - duplicate_emergency_distribution
ui_warning: Potable water service likely triggers public-water-system review. Block promotion until legal/public-health review is complete.
```

---

## 10. Well Testing and Local Potable Source

```yaml
domain: water_systems
node_type: well_or_private_source
question: Which testing and maintenance requirements apply to private/shared well-like sources?
scale_action: hybrid

thresholds:
  emergency_minimum:
    value: do_not_rely_on_untested_source
    action_if_missing: fail

  dignified_minimum:
    value: annual_testing_for_total_coliform_nitrates_TDS_pH_plus_local_contaminants
    source_ids:
      - EPA_PRIVATE_WELLS
      - CDC_WELL_TESTING

  comfortable_range:
    value: annual_testing_plus_event_based_testing_after_flood_repair_taste_color_odor_change_or_nearby_contamination

  soft_threshold:
    condition: well_source_serves_multiple_households_or_25_people
    action: public_health_review_and_testing_schedule_required

  hard_threshold:
    condition: shared_source_unreviewed_or_testing_overdue
    action: fail_or_block

  failure_threshold:
    condition: test_results_failed_without_treatment_or_alternate_supply
    action: fail

human_factor_driver:
  - potable_safety
  - trust
  - testing
  - public_health
  - resilience

evidence_quality: high
translation_confidence: high
regulatory_strength: guideline_to_binding_depending_population
source_ids:
  - EPA_PRIVATE_WELLS
  - CDC_WELL_TESTING
  - EPA_PUBLIC_WATER_SYSTEM

notes_for_CIaC:
  - Testing schedule should be visible in world viewer.
  - Water status should show tested/review_required/failed.
  - Lab results interpretation belongs to qualified humans/local authorities.

optimizer_preference:
  - require_testing_schedule
  - add_backup_source
  - add_alternate_supply_contract
ui_warning: Potable source lacks current testing or qualified review.
```

---

## 11. Emergency Water Reserve

```yaml
domain: water_systems
node_type: emergency_potable_reserve
question: What backup reserve sizing is recommended per person/day under outage or contamination conditions?
scale_action: duplicate

thresholds:
  emergency_minimum:
    value: 1
    unit: gallon_per_person_per_day
    duration_minimum: 3_days
    source_ids:
      - CDC_EMERGENCY_WATER

  dignified_minimum:
    value: 14_days_of_1_gallon_per_person_per_day_where_possible
    source_ids:
      - CDC_EMERGENCY_WATER

  comfortable_range:
    value: 20_liters_per_person_per_day_for_essential_health_and_hygiene_planning
    source_ids:
      - WHO_EMERGENCY_WATER_20L

  soft_threshold:
    condition: less_than_14_days_emergency_potable_storage
    action: warn

  hard_threshold:
    condition: less_than_3_days_emergency_potable_storage
    action: fail

  failure_threshold:
    condition: emergency_water_not_accessible_to_high_need_residents
    action: fail

human_factor_driver:
  - emergency_survival
  - hygiene
  - care_needs
  - access
  - contamination_response

evidence_quality: high
translation_confidence: high
regulatory_strength: guideline
source_ids:
  - CDC_EMERGENCY_WATER
  - WHO_EMERGENCY_WATER_20L

notes_for_CIaC:
  - Store emergency potable reserve by neighborhood or ensure distribution route.
  - Model high-need residents, heat, illness, pets/service animals, and medication needs as higher demand.
  - Distinguish 1 gallon/person/day emergency reserve from normal dignity water.

optimizer_preference:
  - duplicate_emergency_distribution_points
  - increase_reserve_days
  - protect_high_need_access
ui_warning: Emergency water reserve is below CIaC floor or not accessible to all residents.
```

---

## 12. Central vs Distributed Water Infrastructure

```yaml
domain: water_systems
node_type: water_distribution_topology
question: Which water systems should duplicate for redundancy and which can scale as a larger central node?
scale_action: hybrid

thresholds:
  emergency_minimum:
    duplicate_locally:
      - emergency_distribution_points
      - emergency_storage_access
      - manual_or_gravity_fallback_where_possible

  dignified_minimum:
    local_access:
      - clearly_marked_potable_points
      - accessible distribution
      - backup dispensing
      - contamination communication

  comfortable_range:
    central_or_federated:
      - treatment
      - testing oversight
      - source management
      - public-health reporting
    local_or_duplicated:
      - cisterns
      - emergency tanks
      - shutoffs
      - sampling points
      - distribution points

  soft_threshold:
    value: 50-100
    unit: residents_per_emergency_distribution_point
    action: duplicate_distribution_or_storage_access

  hard_threshold:
    value: 150
    unit: residents_without_multiple_distribution_points_or_backup_roles
    action: duplicate_and_federate

  failure_threshold:
    condition: one_source_one_pump_one_operator_or_one_distribution_point_for_entire_population
    action: fail_or_warn_based_on_scale

human_factor_driver:
  - redundancy
  - access
  - emergency_response
  - operator_capacity
  - public_health

evidence_quality: moderate
translation_confidence: moderate
regulatory_strength: professional_practice
source_ids:
  - NIST_COMMUNITY_RESILIENCE_GUIDE
  - EPA_PUBLIC_WATER_SYSTEM
  - CDC_EMERGENCY_WATER

notes_for_CIaC:
  - Central treatment can be efficient but must not create single-point failure.
  - Emergency distribution must be local and accessible.
  - Above village block, federate water operations.

optimizer_preference:
  - central_reviewed_treatment
  - duplicate_local_storage_distribution
  - add_operator_backup
ui_warning: Water system has a single-point failure or insufficient local emergency access.
```

---

## 13. Non-Potable Water Reuse

```yaml
domain: water_systems
node_type: nonpotable_reuse
question: Which water reuse systems can scale and when should they be local or centralized?
scale_action: hybrid

thresholds:
  emergency_minimum:
    value: not_required
    notes: Non-potable reuse is conservation/resilience layer, not drinking-water floor.

  dignified_minimum:
    value: clear_separation_between_potable_and_nonpotable_water
    action_if_missing: fail

  comfortable_range:
    local:
      - rainwater_irrigation
      - garden_nonpotable_storage
    reviewed_building_or_district_system:
      - toilet_flushing
      - laundry
      - greywater_reuse
      - stormwater_or_roof_rainwater_treatment

  soft_threshold:
    condition: reuse_system_serves_multiple_buildings_or_human_contact_uses
    action: professional_and_code_review_required

  hard_threshold:
    condition: cross_connection_risk_or_nonpotable_water_unclear_to_residents
    action: fail

  failure_threshold:
    condition: nonpotable_water_can_enter_potable_distribution
    action: fail

human_factor_driver:
  - public_health
  - conservation
  - drought_resilience
  - code_review
  - resident_legibility

evidence_quality: high
translation_confidence: moderate
regulatory_strength: guideline_to_binding_depending_jurisdiction
source_ids:
  - EPA_ONSITE_NONPOTABLE_REUSE
  - NSF_ANSI_350_REUSE

notes_for_CIaC:
  - Rainwater defaults to non-potable.
  - Reuse is valuable but should not be improvised.
  - Reuse can federate at building/district scale if professionally designed and maintained.

optimizer_preference:
  - nonpotable_for_irrigation_first
  - reviewed_reuse_for_toilets_laundry_second
  - block_any_cross_connection_risk
ui_warning: Non-potable reuse requires code/public-health review and clear separation from potable water.
```

---

# SANITATION AND WASTE

## 14. Toilet, Bathing, and Hygiene Access

```yaml
domain: sanitation_waste
node_type: toilet_bathing_hygiene_access
question: Which sanitation functions must remain decentralized for hygiene, access, and resilience?
scale_action: duplicate

thresholds:
  emergency_minimum:
    toilet_ratio: 1_toilet_per_20_people
    maximum_distance: 50_meters
    source_ids:
      - SPHERE_TOILET_20_50
      - UNHCR_WATSAN_20_LATRINE
    notes: Emergency reference only, not normal CIaC dignity.

  dignified_minimum:
    value:
      - private_or_semi_private_toilet_access
      - handwashing_near_toilet
      - accessible_toilets
      - bathing_access
      - menstrual_hygiene_support
      - diaper_incontinence_plan_where_needed

  comfortable_range:
    value:
      - in_unit_or_pod_level_toilets
      - bathing_near_residential_pods
      - laundry_within_3_to_5_minutes
      - hygiene_access_with_no_social_performance

  soft_threshold:
    condition: toilet_or_bathing_access_exceeds_3_to_5_minutes_or_relies_on_emergency_standard
    action: warn

  hard_threshold:
    condition: emergency_toilet_ratio_used_as_normal_design_or_no_accessible_toilet
    action: fail

  failure_threshold:
    condition: no_handwashing_no_safe_toilet_access_or_no_approved_blackwater_plan
    action: fail

human_factor_driver:
  - hygiene
  - dignity
  - disability_access
  - gender_safety
  - public_health

evidence_quality: high_for_emergency_minimum
translation_confidence: moderate
regulatory_strength: guideline
source_ids:
  - SPHERE_TOILET_20_50
  - UNHCR_WATSAN_20_LATRINE
  - WHO_SANITATION_SAFETY_PLANNING

notes_for_CIaC:
  - Emergency WASH standards are too low for normal dignity.
  - Toilets and bathing duplicate by residential pod/neighborhood.
  - In the 3D viewer, show toilet/hygiene access radius separately from waste processing.

optimizer_preference:
  - duplicate_local_toilets_bathing
  - add_accessible_hygiene_node
  - reject_emergency_standard_as_normal
ui_warning: Sanitation access is using emergency-minimum logic or exceeds dignified access radius.
```

---

## 15. Wastewater / Blackwater Treatment

```yaml
domain: sanitation_waste
node_type: blackwater_wastewater_treatment
question: Which sanitation functions can centralize, and when do regulatory categories change?
scale_action: federate

thresholds:
  emergency_minimum:
    value: safe_excreta_containment_and_handwashing
    source_ids:
      - SPHERE_WASH_2018

  dignified_minimum:
    value: approved_blackwater_plan_with_maintenance_and_backup
    source_ids:
      - WHO_SANITATION_SAFETY_PLANNING
      - EPA_SEPTIC

  comfortable_range:
    local_access:
      - toilets
      - handwashing
      - bathing
    central_or_professionalized:
      - wastewater_treatment
      - septic_or_decentralized_cluster_system
      - sewer_connection
      - sludge_or_solids_management

  soft_threshold:
    condition: onsite_system_serves_multiple_households_or_village_block
    action: professional_design_permit_and_maintenance_plan_required

  hard_threshold:
    condition: no_public_sewer_permitted_septic_or_professionally_reviewed_decentralized_solution
    action: fail

  failure_threshold:
    condition: human_waste_handled_by_residents_without_PPE_training_review_or_approved_process
    action: fail

human_factor_driver:
  - pathogen_control
  - public_health
  - legal_compliance
  - maintenance
  - dignity

evidence_quality: high
translation_confidence: high
regulatory_strength: binding
source_ids:
  - EPA_SEPTIC
  - WHO_SANITATION_SAFETY_PLANNING
  - CDC_HUMAN_WASTE_WORKER_SAFETY

notes_for_CIaC:
  - Treat blackwater as professional/public-health infrastructure.
  - Composting toilets may be optional reviewed systems, not baseline.
  - Human-waste handling by residents should trigger PPE/training/professional review.

optimizer_preference:
  - centralize_approved_treatment
  - duplicate_toilet_access
  - require_professional_handoff
ui_warning: Blackwater system lacks approved design, maintenance, or professional/public-health review.
```

---

## 16. Greywater and Reuse

```yaml
domain: sanitation_waste
node_type: greywater_reuse
question: Which greywater systems can centralize and which must remain simple/local?
scale_action: hybrid

thresholds:
  emergency_minimum:
    value: not_required
    notes: Greywater reuse is optional conservation/resilience, not a sanitation floor.

  dignified_minimum:
    value: greywater_must_not_create_pathogen_odor_or_cross_connection_risk

  comfortable_range:
    local_simple:
      - reviewed_subsurface_landscape_irrigation
    building_or_district_reviewed:
      - treated_toilet_flushing
      - treated_laundry_reuse
      - larger_nonpotable_systems

  soft_threshold:
    condition: greywater_storage_or_reuse_introduced
    action: code_public_health_review_required

  hard_threshold:
    condition: greywater_contacts_edible_crops_or_potable_distribution_without_review
    action: fail

  failure_threshold:
    condition: cross_connection_or_indoor_exposure_or_unmanaged_storage
    action: fail

human_factor_driver:
  - public_health
  - water_conservation
  - odor
  - code_review
  - maintenance

evidence_quality: high
translation_confidence: moderate
regulatory_strength: guideline_to_binding_depending_jurisdiction
source_ids:
  - EPA_ONSITE_NONPOTABLE_REUSE
  - NSF_ANSI_350_REUSE
  - WHO_SANITATION_SAFETY_PLANNING

notes_for_CIaC:
  - Greywater belongs at water/sanitation interface.
  - Default should be approved discharge unless review supports reuse.
  - Reuse must have illness bypass and maintenance owner.

optimizer_preference:
  - keep_simple_local_reuse_first
  - require_professional_review_for_treatment
  - block_cross_connection
ui_warning: Greywater reuse requires review and cannot compromise potable water or hygiene.
```

---

## 17. Solid Waste, Compost, Recycling, Hazardous Waste

```yaml
domain: sanitation_waste
node_type: waste_streams
question: Which waste systems can centralize?
scale_action: hybrid

thresholds:
  emergency_minimum:
    value: safe_waste_containment_and_collection
    purpose: prevent pests, contamination, injury, and blocked hygiene

  dignified_minimum:
    value:
      - local_waste_dropoff
      - pest_resistant_organics_collection
      - clear_recycling
      - hazardous_waste_separation
      - sharps_medical_waste_protocol_if_needed

  comfortable_range:
    local:
      - food_scrap_collection
      - waste_sorting
      - recycling_dropoff
      - household_hazardous_collection_point_with_locks
    central_or_federated:
      - compost_processing
      - recycling_aggregation
      - hazardous_waste_storage
      - e_waste_battery_collection
      - tool_wash

  soft_threshold:
    condition: waste_dropoff_exceeds_3_to_5_minutes_or_organics_bins_create_odor_pest_risk
    action: warn

  hard_threshold:
    condition: batteries_sharps_chemicals_or_medical_waste_mixed_with_ordinary_trash
    action: fail

  failure_threshold:
    condition: food_scraps_collected_without_pest_odor_or_collection_plan
    action: fail

human_factor_driver:
  - hygiene
  - pest_control
  - labor
  - safety
  - circularity

evidence_quality: moderate
translation_confidence: moderate
regulatory_strength: professional_practice
source_ids:
  - WHO_SANITATION_SAFETY_PLANNING
  - CDC_HUMAN_WASTE_WORKER_SAFETY
  - EPA_SEPTIC

notes_for_CIaC:
  - Waste dropoff should be local but not placed where odor/pests compromise dignity.
  - Compost processing can centralize at service edge or district edge.
  - Hazardous waste should centralize under lock/control.

optimizer_preference:
  - duplicate_dropoff_points
  - centralize_processing
  - separate_hazardous_streams
ui_warning: Waste stream is unsafe, too distant, or missing hazardous separation.
```

---

# CARE AND HEALTH

## 18. Care Room Scaling

```yaml
domain: care_health
node_type: care_room
question: How many people can one care room reasonably support?
scale_action: duplicate

thresholds:
  emergency_minimum:
    value: first_aid_station_emergency_contacts_and_transport_to_care
    purpose: short-term support only

  dignified_minimum:
    value:
      - private_care_space
      - accessible_bathroom_nearby
      - medication_continuity
      - telehealth_private_space
      - care_meal_protocol
      - transport_to_care

  comfortable_range:
    min: 50
    max: 100
    unit: residents_per_care_room

  soft_threshold:
    value: 100
    unit: residents_per_care_room
    action: warn_privacy_scheduling_infection_control

  hard_threshold:
    value: 150
    unit: residents_per_care_room
    action: duplicate_care_room_or_add_neighborhood_care_point

  failure_threshold:
    condition: no_private_care_space_no_medication_continuity_or_no_high_need_support
    action: fail

human_factor_driver:
  - privacy
  - infection_control
  - disability_support
  - elder_support
  - emotional_safety
  - medication_continuity

evidence_quality: moderate
translation_confidence: moderate
regulatory_strength: professional_practice
source_ids:
  - GREEN_HOUSE_MODEL
  - CDC_DISABILITY_EMERGENCY_KIT
  - HRSA_HEALTH_CENTER_PROGRAM

notes_for_CIaC:
  - Care rooms are not clinics; they are private support spaces and care coordination points.
  - Clinical services should federate to health centers/urgent care/hospital partnerships.
  - Care room access should be within 3-5 minutes for village block, closer for high-need residents.

optimizer_preference:
  - duplicate_care_room_above_100_to_150
  - federate_clinical_partnership
  - protect_privacy
ui_warning: Care room is approaching privacy, scheduling, or infection-control limits. Add local care point.
```

---

## 19. Neighborhood Care vs Central Clinic

```yaml
domain: care_health
node_type: care_network
question: What evidence exists for neighborhood-scale care access versus centralized care?
scale_action: hybrid

thresholds:
  emergency_minimum:
    value: emergency_access_to_professional_care_and_EMS
    purpose: CIaC does not replace medical care.

  dignified_minimum:
    value: nonclinical_local_support_plus_external_healthcare_relationships

  comfortable_range:
    local_neighborhood:
      - care_room
      - first_aid
      - medication_continuity
      - care_meals
      - check_ins
      - telehealth_private_space
    district:
      - visiting_practitioner_space
      - community_health_worker_style_liaison
      - transport_to_clinic
      - care coordination
    regional:
      - health_center
      - hospital
      - pharmacy
      - behavioral_health
      - specialist_services

  soft_threshold:
    value: 150
    unit: residents_without_local_care_duplication
    action: duplicate_local_care

  hard_threshold:
    value: 300
    unit: residents_without_district_care_coordination_or_clinic_partnership
    action: federate_care_network

  failure_threshold:
    condition: care_system_claims_to_replace_clinicians_or_lacks_external_care_path
    action: fail

human_factor_driver:
  - access
  - continuity
  - nonclinical_support
  - professional_boundary
  - high_need_residents

evidence_quality: moderate
translation_confidence: moderate
regulatory_strength: professional_practice
source_ids:
  - CDC_CHW_PREVENTING_CHRONIC_DISEASE
  - IMPACT_CHW_RCT
  - HRSA_HEALTH_CENTER_PROGRAM
  - CDC_DISABILITY_EMERGENCY_KIT

notes_for_CIaC:
  - Local care is support and coordination, not diagnosis/treatment.
  - District care can include CHW-style liaison and visiting provider interface.
  - Regional care must remain explicit.

optimizer_preference:
  - duplicate_local_care_rooms
  - federate_health_partnerships
  - block_clinical_overclaim
ui_warning: Care model is too centralized or lacks external professional healthcare path.
```

---

## 20. Medication Continuity and Cold-Chain Medication Storage

```yaml
domain: care_health
node_type: medication_continuity
question: How should medication continuity and refrigerated medication storage scale?
scale_action: hybrid

thresholds:
  emergency_minimum:
    value: at_least_one_week_prescription_medications_where_possible_plus_cooler_for_refrigerated_meds
    source_ids:
      - CDC_DISABILITY_EMERGENCY_KIT

  dignified_minimum:
    value:
      - privacy_preserving_medication_plan
      - refrigerated_medication_backup_power
      - pharmacy_relationship
      - refill_or_delivery_plan
      - cooler_cold_pack_fallback

  comfortable_range:
    local:
      - medication_refrigeration_point_per_village_block_or_care_room
      - emergency_charging_point
      - privacy_controls
    district:
      - pharmacy_pickup_route
      - care_transport
      - backup cold-chain logistics

  soft_threshold:
    condition: refrigerated_medications_present_without_critical_energy_mapping
    action: warn

  hard_threshold:
    condition: refrigerated_medications_not_on_critical_load_or_no_power_fallback
    action: fail

  failure_threshold:
    condition: medication_needs_require_public_disclosure_or_no_pharmacy_access_plan
    action: fail

human_factor_driver:
  - health_continuity
  - privacy
  - energy_resilience
  - transport
  - disability_support

evidence_quality: high
translation_confidence: high
regulatory_strength: guideline
source_ids:
  - CDC_DISABILITY_EMERGENCY_KIT

notes_for_CIaC:
  - Medication continuity belongs to care, energy, mobility, and privacy simultaneously.
  - Do not visualize individual medication needs in 3D viewer.
  - Aggregate high-need support only.

optimizer_preference:
  - duplicate_medication_backup_points
  - add_critical_load_mapping
  - add_pharmacy_transport_plan
ui_warning: Medication continuity or refrigerated medication backup is not protected.
```

---

## 21. Elder, Disability, and High-Need Support

```yaml
domain: care_health
node_type: high_need_support
question: When does a care function need duplication for privacy, access, infection control, or emotional safety?
scale_action: duplicate

thresholds:
  emergency_minimum:
    value:
      - function_based_high_need_registry_with_privacy
      - accessible_evacuation
      - medication_and_device_power_plan
      - care_transport

  dignified_minimum:
    value:
      - accessible_routes
      - care_room_privacy
      - support_without_public_diagnosis
      - care_meal_delivery
      - hygiene_support
      - backup_caregiver_role

  comfortable_range:
    local:
      - high_need_support_by_pod_or_village_block
      - care_room_with_accessible_bathroom
      - food_water_delivery
    high_care_residential:
      - 8_to_12_person_small_house_logic
      - private_room_bath
      - outdoor_access

  soft_threshold:
    condition: high_need_residents_travel_more_than_3_to_5_minutes_to_care_or_hygiene
    action: warn

  hard_threshold:
    condition: high_need_residents_not_modeled_or_support_depends_on_one_informal_person
    action: fail

  failure_threshold:
    condition: disability_or_elder_support_requires_public_health_status_exposure
    action: fail

human_factor_driver:
  - disability_access
  - elder_support
  - privacy
  - infection_control
  - caregiver_burden

evidence_quality: moderate
translation_confidence: moderate
regulatory_strength: guideline
source_ids:
  - CDC_DISABILITY_EMERGENCY_KIT
  - GREEN_HOUSE_MODEL
  - HRSA_HEALTH_CENTER_PROGRAM

notes_for_CIaC:
  - Use function-based support, not diagnosis-based public labeling.
  - Elder/high-care residents should trigger smaller residential nodes.
  - Care duplication should happen before care labor burns out.

optimizer_preference:
  - duplicate_care_access
  - shrink_high_care_cluster
  - add_backup_care_roles
ui_warning: High-need resident support is not adequately local, private, or backed up.
```

---

## 22. Illness Isolation and Infection Control

```yaml
domain: care_health
node_type: illness_wave_support
question: When does care need duplication for infection control or emotional safety?
scale_action: duplicate

thresholds:
  emergency_minimum:
    value: symptomatic_resident_support_meal_delivery_hand_hygiene_cleaning_escalation
    purpose: reduce spread while preserving care

  dignified_minimum:
    value:
      - care_room_or_recovery_space
      - meal_delivery
      - cleaning_escalation
      - privacy
      - nonpunitive_protocol
      - air_quality_or_ventilation_review

  comfortable_range:
    village_block:
      - one_care_room_plus_quiet_recovery_option
      - delivery_to_units_or_pods
    district:
      - overflow_recovery_or_visiting_provider_space
      - public_health_partnership

  soft_threshold:
    condition: one_care_room_cannot_separate_symptomatic_and_non_symptomatic_support
    action: warn

  hard_threshold:
    condition: illness_wave_protocol_absent_or_meal_delivery_absent_or_high_need_residents_unprotected
    action: fail

  failure_threshold:
    condition: sick_residents_must_use_crowded_common_meals_or_publicly_disclose_status_to_access_food
    action: fail

human_factor_driver:
  - infection_control
  - privacy
  - care_meals
  - social_nonpunishment
  - high_need_support

evidence_quality: moderate
translation_confidence: moderate
regulatory_strength: professional_practice
source_ids:
  - CDC_DISABILITY_EMERGENCY_KIT
  - HRSA_HEALTH_CENTER_PROGRAM
  - WHO_SANITATION_SAFETY_PLANNING

notes_for_CIaC:
  - Illness protocol should change routines, not punish people.
  - In the 3D viewer, illness scenario should shift common meals to delivery and highlight care/cleaning routes.
optimizer_preference:
  - add_care_delivery_routes
  - add_recovery_space
  - duplicate_care_room_above_threshold
ui_warning: Illness-wave support lacks privacy, delivery, cleaning escalation, or high-need protection.
```

---

## 23. Part 3 CIaC Translation Matrix

| Domain | Node | Natural scaling type | Base node | Soft threshold | Hard threshold | Service-radius constraint | Primary driver | Optimizer preference |
|---|---|---:|---:|---:|---:|---|---|---|
| Food | neighborhood food commons | hybrid | 50-100 residents | 80 | 150 | 3-5 min to food access | labor, hygiene, food safety | duplicate kitchen/pickup; federate procurement |
| Food | shared kitchen | hybrid | 50-80 residents | 80 | 100-150 | service edge + 3-5 min pickup | scheduling, cleaning, TCS food safety | add meal waves/second kitchen |
| Food | dining wave | duplicate | 24-60 diners | 60 | 80 | 3-5 min | institutional feel | meal waves + local dining |
| Food | storage/procurement | federate | 150-500 residents | 150 | 300 no logistics | service access | resilience, inventory | federate district logistics |
| Protein | local protein commons | hybrid | 50-100 residents | 80 | 150 | food node adjacent | safety, acceptance, labor | duplicate simple layers; federate advanced protein |
| Water | public water review | federate | N/A | 25 people | PWS-scale no review | N/A | regulation/public health | require review |
| Water | emergency potable reserve | duplicate | village block | <14 days | <3 days | 1-3 min emergency point | emergency survival | duplicate reserve points |
| Water | nonpotable reuse | hybrid | building/site | human contact uses | cross connection | clearly labeled | public health | review-gated reuse |
| Sanitation | toilet/bathing access | duplicate | pod/neighborhood | >3-5 min | emergency standard as normal | 1-3 min preferred, 50m emergency max | dignity/hygiene | duplicate local access |
| Sanitation | blackwater treatment | federate | professional system | multi-household onsite | no approved plan | service access | pathogen/control | approved central treatment |
| Sanitation | waste streams | hybrid | local dropoff | odor/distance | hazardous mixed trash | 3-5 min dropoff | hygiene/safety | local dropoff + central processing |
| Care | care room | duplicate | 50-100 residents | 100 | 150 | 3-5 min | privacy/infection/access | duplicate care rooms |
| Care | clinic partnership | federate | 300-1500 residents | 300 | no external care path | transit/transport | professional care | federate clinic/pharmacy |
| Care | medication continuity | hybrid | village block | cold meds not mapped | no power fallback | care room/local | health continuity | critical-load + privacy |
| Care | high-need support | duplicate | pod/block | >3-5 min care/hygiene | not modeled | 1-5 min | disability/elder support | duplicate care access |
```

---

## 24. UI Warning Language

```yaml
warnings:
  food_commons_bottleneck:
    message: Food commons is approaching kitchen, dining, labor, hygiene, or food-safety bottleneck. Duplicate local food access or federate back-end food logistics.

  kitchen_food_safety_review:
    message: Shared kitchen complexity requires food-safety review, logs, allergen controls, and trained backup.

  meal_radius_warning:
    message: Food access exceeds walk/roll threshold for high-need residents. Add meal pickup or delivery node.

  water_public_system_review:
    message: Potable water service likely triggers public-water-system review. Block promotion until legal/public-health review is complete.

  water_reserve_warning:
    message: Emergency potable water reserve is below CIaC floor or not accessible to all residents.

  water_cross_connection_fail:
    message: Non-potable water system creates cross-connection or resident legibility risk. Block until reviewed.

  sanitation_emergency_standard_warning:
    message: Sanitation access is using emergency-minimum logic or exceeds dignified access radius.

  blackwater_review_fail:
    message: Blackwater system lacks approved design, maintenance, or professional/public-health review.

  hazardous_waste_fail:
    message: Hazardous, sharps, battery, chemical, or medical waste is not separated safely.

  care_room_threshold:
    message: Care room is approaching privacy, scheduling, or infection-control limits. Add local care point.

  medication_continuity_fail:
    message: Medication continuity or refrigerated medication backup is not protected.

  high_need_support_fail:
    message: High-need resident support is not adequately local, private, or backed up.

  illness_wave_fail:
    message: Illness-wave support lacks privacy, delivery, cleaning escalation, or high-need protection.
```

---

## 25. Suggested Tests

```yaml
tests:
  food_node_soft:
    residents_per_food_node: 85
    expected: food_commons_bottleneck_warning

  food_node_hard:
    residents_per_food_node: 151
    expected: duplicate_or_federate_required

  shared_kitchen_safety:
    shared_kitchen_active: true
    food_safety_logs: false
    expected: fail

  public_water_review:
    people_served_by_potable_system: 25
    expected: public_health_review_required

  emergency_water_fail:
    emergency_potable_days: 2
    expected: fail

  private_well_testing:
    well_source: true
    annual_testing_current: false
    expected: fail_or_block

  sanitation_emergency_as_normal:
    toilet_ratio: 1_per_20
    normal_design: true
    expected: fail

  toilet_distance:
    distance_to_toilet_m: 60
    emergency_mode: true
    expected: fail

  care_room_soft:
    residents_per_care_room: 110
    expected: warning

  care_room_hard:
    residents_per_care_room: 151
    expected: duplicate_required

  medication_cold_chain:
    refrigerated_medications_present: true
    critical_energy_mapping: false
    expected: fail

  high_need_support_missing:
    high_need_residents_modeled: false
    expected: fail
```

---

## 26. Repo Implementation Notes

```yaml
suggested_policy_files:
  - scale_policies/ciac_scaling_policy_v0.yaml
  - schemas/scaling_policy.schema.json

suggested_engine_updates:
  node_scaling:
    - add emergency_minimum vs dignified_minimum threshold classes
    - support review_trigger thresholds like 25_person_public_water_system
    - allow service_radius constraints separate from node population

  topology_optimizer:
    - prefer duplicate for local food/care/sanitation access
    - prefer federate for procurement, treatment, clinics, advanced maintenance
    - penalize using emergency standards as normal

  world_manifest:
    - expose food, water, sanitation, and care service-radius overlays
    - show public-health review markers
    - show emergency vs normal dignity states separately

  capability_state:
    - add fields for food_safety_controls
    - water_public_health_review_required
    - sanitation_dignity_status
    - medication_continuity_status
    - high_need_support_coverage
```

---

## 27. Status

```yaml
status: approved_as_research_input
not_yet:
  - final_verified_policy
  - local_code_or_health_department_review
  - engineering_review
  - food_service_license_review
  - medical_or_clinical_review
next_step:
  - part_4_governance_maintenance_mobility_education_resilience
  - then_scaling_policy_v0_yaml
```
