# CIaC Deep Research Part 2, Residential, Mental Health, Common House, and Social Scale, Updated

**Research ID:** `ciac_scaling_thresholds_part_2_v0_2`  
**Supersedes:** `ciac_scaling_thresholds_part_2_v0_1`  
**Parent:** `ciac_scaling_thresholds_part_1_v0_2`  
**Purpose:** Deepen the human-scale evidence for residential clustering, privacy, perceived crowding, common-house sizing, dining scale, quiet space, mental-health protection, and social thresholds.  
**Status:** Approved research input, not final verified policy.  
**Primary CIaC use:** refine `housing`, `social_cultural`, `mobility_access`, `labor_time`, `governance`, `care_health`, `node_scaling`, `topology_optimizer`, and 3D world warnings.

---

## 0. What Changed in v0.2

```yaml
updates:
  source_traceability:
    change: added source IDs and traceable source registry
    reason: thresholds need review-grade source references before becoming policy logic

  evidence_normalization:
    change: split evidence_quality, translation_confidence, regulatory_strength
    reason: avoid ambiguous composite labels

  threshold_separation:
    change: each topic now separates emergency_minimum, dignified_minimum, comfortable_range, soft_threshold, hard_threshold, and failure_threshold
    reason: emergency sheltering or WASH references must not be used as normal dignity thresholds
```

---

## 1. Source Registry

```yaml
source_registry:
  - id: WHO_HOUSING_2018
    title: WHO Housing and Health Guidelines
    organization: World Health Organization
    year: 2018
    url: https://www.who.int/publications/i/item/9789241550376
    supports:
      - crowding
      - inadequate_living_space
      - accessibility
      - indoor_environmental_quality

  - id: WHO_HOUSING_CROWDING_NCBI
    title: Household crowding, WHO Housing and Health Guidelines chapter
    organization: WHO / NCBI Bookshelf
    url: https://www.ncbi.nlm.nih.gov/books/NBK535289/
    supports:
      - crowding_as_mismatch_between_dwelling_and_household
      - mental_and_physical_health_impacts
      - crowding_depends_on_design_and_household_needs

  - id: SURGEON_GENERAL_SOCIAL_CONNECTION
    title: Our Epidemic of Loneliness and Isolation
    organization: U.S. Surgeon General / HHS
    url: https://www.hhs.gov/sites/default/files/surgeon-general-social-connection-advisory.pdf
    supports:
      - built_environment_affects_social_connection
      - housing_transport_green_space_and_local_institutions_matter

  - id: DUNBAR_SOCIAL_LAYERS
    title: Dunbar social brain / social-layer research
    organization: research_literature
    url: https://royalsocietypublishing.org/doi/10.1098/rstb.2015.0093
    supports:
      - social_layers_5_15_50_150_500_1500

  - id: GREEN_HOUSE_SMALL_HOUSE
    title: Green House / small-house elder-care model
    organization: Green House Project / long-term-care practice
    url: https://thegreenhouseproject.org/
    supports:
      - high_care_small_house_10_to_12_residents
      - private_room_bath_homelike_living

  - id: COHOUSING_ASSOCIATION
    title: What is Cohousing
    organization: Cohousing Association of the United States
    url: https://www.cohousing.org/what-cohousing/cohousing/
    supports:
      - private_homes_plus_shared_spaces
      - community_interaction_plus_privacy

  - id: COHOUSING_HEALTH_SCOPING
    title: Cohousing, health and wellbeing scoping review
    organization: peer_reviewed_literature
    url: https://www.sciencedirect.com/science/article/pii/S0272494420306850
    supports:
      - cohousing_as_health_and_wellbeing_relevant
      - evidence_is_promising_but_contextual

  - id: EVANS_BUILT_ENVIRONMENT_MENTAL_HEALTH
    title: Built environment and mental health research
    organization: peer_reviewed_literature
    url: https://pubmed.ncbi.nlm.nih.gov/14709704/
    supports:
      - housing_design_and_crowding_affect_stress
      - environmental_control_and_privacy_matter

  - id: ROLLINGS_EVANS_CROWDING_DESIGN
    title: Perceived crowding, design moderators, and mental health
    organization: peer_reviewed_literature
    url: https://pubmed.ncbi.nlm.nih.gov/24962309/
    supports:
      - perceived_crowding_differs_from_density
      - design_features_moderate_crowding

  - id: OLDENBURG_THIRD_PLACE
    title: Third place concept
    organization: theory/practice literature
    url: https://www.pps.org/article/roldenburg
    supports:
      - informal_voluntary_places_beyond_home_and_work
      - social_comfort_requires_low_pressure_access

  - id: NAEYC_RATIOS_GROUP_SIZE
    title: Staff-to-child ratio and group size recommendations
    organization: NAEYC
    url: https://www.naeyc.org/
    supports:
      - child_group_size_reference_where_children_are_modeled
```

---

## 2. Core Finding

```yaml
core_finding:
  statement: >
    CIaC should scale by repeated small social and residential cells, not by enlarging
    one building, one common house, one dining hall, or one assembly.

nested_layers:
  intimate_support: 3-5
  care_or_close_operational_group: 5-8
  small_house_or_elder_household: 8-12
  residential_pod: 12-24
  familiar_neighborhood_cell: 30-50
  village_block: 80-150
  district_federation: 300-500
  town_city_layer: 900-1500
  regional_membrane: 1500+
```

---

## 3. Residential Hall / Building Size

```yaml
domain: residential_life
node_type: residential_pod
question: How many people can share one residential hall/building before privacy, stress, sleep quality, conflict, or perceived crowding degrade?
scale_action: duplicate

thresholds:
  emergency_minimum:
    value: not_applicable
    notes: Emergency sheltering references are not valid as normal residential dignity thresholds.

  dignified_minimum:
    value: private_room_or_private_unit_with_ability_to_withdraw
    action_if_missing: fail

  comfortable_range:
    min: 12
    max: 24
    unit: residents_per_pod

  soft_threshold:
    value: 24
    unit: residents_per_pod
    action: warn_and_plan_duplicate

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
  - control_over_social_exposure

evidence_quality: moderate
translation_confidence: moderate
regulatory_strength: research_inferred
source_ids:
  - WHO_HOUSING_2018
  - WHO_HOUSING_CROWDING_NCBI
  - GREEN_HOUSE_SMALL_HOUSE
  - COHOUSING_ASSOCIATION
  - EVANS_BUILT_ENVIRONMENT_MENTAL_HEALTH

notes_for_CIaC:
  - The most important residential threshold is not building size alone, it is whether the building is subdivided into private retreats and small social cells.
  - Larger physical buildings may be acceptable if socially subdivided.
  - The 3D world should show pods, thresholds, quiet spaces, and acoustic buffers rather than one monolithic residence hall.
optimizer_preference:
  - duplicate_residential_pod
  - add_pod_micro_commons
  - add_quiet_space
  - improve_private_retreat
ui_warning: Residential pod is beyond comfortable cluster size. Duplicate or subdivide.
```

---

## 4. Household Cluster Size by Population Type

```yaml
domain: household_cluster
node_type: household_cluster
question: What is the recommended maximum size of a residential household cluster for adults, families, elders, children, or mixed-age communities?
scale_action: duplicate

thresholds:
  emergency_minimum:
    value: not_applicable
    notes: Emergency sheltering is not a normal residential model.

  dignified_minimum:
    value: private_retreat_plus_appropriate_hygiene_access
    action_if_missing: fail

  comfortable_range:
    adults_shared_suite: 4-8
    elder_high_care_house: 8-12
    families_mixed_age_cluster: 12-24
    mixed_age_pod: 16-24
    children_youth: professional_review_required

  soft_threshold:
    adults_shared_suite: 8
    elder_high_care_house: 10
    mixed_age_pod: 24

  hard_threshold:
    adults_shared_suite: 12
    elder_high_care_house: 12-14
    mixed_age_pod: 30
    children_youth: any_unreviewed_childcare_group_above_legal_or_best_practice_ratio

  failure_threshold:
    condition: vulnerable_population_clustered_without_care_privacy_or_safeguarding
    action: fail

human_factor_driver:
  - vulnerability
  - care_needs
  - privacy
  - safeguarding
  - family_autonomy

evidence_quality: moderate
translation_confidence: moderate
regulatory_strength: professional_practice
source_ids:
  - GREEN_HOUSE_SMALL_HOUSE
  - NAEYC_RATIOS_GROUP_SIZE
  - WHO_HOUSING_CROWDING_NCBI
  - COHOUSING_ASSOCIATION

notes_for_CIaC:
  - Do not use one pod target for all populations.
  - Household mix should affect scaling.
  - Elder/high-care population shrinks the comfortable node size.
  - Family-heavy clusters need more private bathrooms, acoustic separation, and outdoor threshold space.
optimizer_preference:
  - duplicate_by_household_type
  - shrink_high_care_node
  - add_family_private_unit_capacity
ui_warning: Household mix requires smaller or more specialized residential clusters.
```

---

## 5. Precedent Lessons

```yaml
domain: unit_precedents
node_type: precedent_translation
question: What unit sizes are supported by cohousing, dormitory, monastery, kibbutz, boarding school, elder-care, military barracks, and intentional community research?
scale_action: hybrid

thresholds:
  emergency_minimum:
    value: not_applicable
    notes: Institutional or emergency precedents are cautionary, not dignity baselines.

  dignified_minimum:
    value: private_retreat_plus_voluntary_shared_life
    action_if_missing: fail

  comfortable_range:
    cohousing: private_dwelling_plus_common_house
    adult_shared_suite: 4-8
    elder_small_house: 8-12
    residential_pod: 12-24

  soft_threshold:
    condition: shared_kitchen_or_bathroom_serves_more_than_small_pod_without_scheduling_or_privacy
    action: warn

  hard_threshold:
    condition: barracks_or_dormitory_sleeping_used_as_default_adult_model
    action: fail

  failure_threshold:
    condition: no_private_retreat_or_mandatory_communal_dining_or_no_exit_rights
    action: fail

human_factor_driver:
  - dignity
  - autonomy
  - privacy
  - voluntary_participation
  - cultural_fit

evidence_quality: mixed
translation_confidence: moderate
regulatory_strength: research_inferred
source_ids:
  - COHOUSING_ASSOCIATION
  - GREEN_HOUSE_SMALL_HOUSE
  - WHO_HOUSING_CROWDING_NCBI

notes_for_CIaC:
  - Cohousing and elder small-house models are positive references.
  - Barracks and institutional dormitories are cautionary references.
  - Monastery/kibbutz precedents are culturally specific and should not become universal models.
optimizer_preference:
  - preserve_private_unit
  - share_infrastructure_by_choice
  - reject_institutional_sleeping_model
ui_warning: This layout resembles institutional housing rather than a dignity floor.
```

---

## 6. Shared Bathrooms, Kitchens, Laundry, Lounges, and Quiet Spaces

```yaml
domain: shared_facility_ratio
node_type: shared_residential_facility
question: How many residents can share bathrooms, kitchens, laundry, lounges, and quiet spaces before quality of life drops?
scale_action: hybrid

thresholds:
  emergency_minimum:
    toilet_reference: 1_toilet_per_20_people
    notes: Emergency WASH reference only, not dignified normal.
    source_ids:
      - SPHERE_WASH

  dignified_minimum:
    bathrooms: private_or_semi_private_hygiene_access
    kitchens: private_food_autonomy_plus_shared_kitchen_option
    laundry: local_access_without_long_waits
    lounge: pod_or_neighborhood_common_space
    quiet_space: at_least_one_low_social_energy_space_per_village_block

  comfortable_range:
    bathroom_small_pod_shared: 4-6_residents_per_fixture
    pod_kitchen: 12-24_residents_with_scheduling
    common_kitchen: 50-100_residents_with_trained_operations
    dining_wave: 24-60_diners
    pod_lounge: 12-24_residents
    quiet_space: one_central_plus_pod_nooks_preferred

  soft_threshold:
    - shared_bathroom_serves_more_than_6_normal_conditions
    - pod_kitchen_serves_more_than_24
    - common_kitchen_serves_more_than_80-100
    - dining_wave_above_60
    - no_quiet_room_for_80_plus_residents

  hard_threshold:
    - emergency_toilet_ratio_used_as_normal_design
    - no_private_or_semi_private_hygiene_path
    - no_private_food_autonomy
    - no_quiet_retreat_space

  failure_threshold:
    condition: shared_facility_access_requires_social_performance_for_basic_hygiene_food_or_rest
    action: fail

human_factor_driver:
  - dignity
  - privacy
  - hygiene
  - scheduling
  - social_overload

evidence_quality: mixed
translation_confidence: moderate
regulatory_strength: guideline
source_ids:
  - SPHERE_WASH
  - FDA_FOOD_CODE_2022
  - COHOUSING_ASSOCIATION
  - WHO_HOUSING_CROWDING_NCBI

notes_for_CIaC:
  - Emergency sanitation ratios should never be treated as comfortable normal life.
  - Kitchens can scale operationally more than socially.
  - Quiet rooms should duplicate before social halls enlarge.
optimizer_preference:
  - duplicate_hygiene_access
  - add_meal_waves
  - duplicate_quiet_space
ui_warning: Shared facility ratio is approaching emergency or institutional conditions. Add local dignified access.
```

---

## 7. Single Shared Building vs Multiple Clusters

```yaml
domain: cluster_vs_single_building
node_type: residential_building_topology
question: At what population does one shared residential building become worse than multiple smaller clusters with shared outdoor/common space?
scale_action: duplicate

thresholds:
  emergency_minimum:
    value: not_applicable

  dignified_minimum:
    value: residential_identity_subdivided_into_private_units_and_small_pods

  comfortable_range:
    one_small_shared_building: 8-24_residents
    one_clustered_building_with_subpods: 30-80_residents
    multiple_pod_village_block: 80-150_residents

  soft_threshold:
    - 30 residents without sub-pods
    - 50 residents without multiple threshold/common areas
    - 80 residents without 3-4 residential pods
    - 100 residents without multiple outdoor commons

  hard_threshold:
    - 150 residents under one shared residential identity
    - one shared entrance_or_common_room_controls_all_social_access
    - one dining_quiet_social_system_for_all_residents

  failure_threshold:
    condition: one_large_building_forces_social_exposure_and_eliminates_retreat
    action: fail

human_factor_driver:
  - social_overload
  - territoriality
  - privacy
  - path_conflict
  - identity_scale

evidence_quality: moderate
translation_confidence: moderate
regulatory_strength: research_inferred
source_ids:
  - WHO_HOUSING_CROWDING_NCBI
  - EVANS_BUILT_ENVIRONMENT_MENTAL_HEALTH
  - COHOUSING_ASSOCIATION
  - DUNBAR_SOCIAL_LAYERS

notes_for_CIaC:
  - A larger physical structure can be acceptable if socially subdivided.
  - The world viewer should display cluster boundaries and courtyard identities.
optimizer_preference:
  - create_multiple_residential_pods
  - add_courtyard_thresholds
  - avoid_monolithic_hall
ui_warning: One residential building is becoming a social bottleneck. Subdivide into pods or duplicate clusters.
```

---

## 8. Perceived Crowding vs Physical Density

```yaml
domain: perceived_crowding
node_type: perceived_crowding_score
question: How does perceived crowding differ from physical density, and what design features reduce harm?
scale_action: resize_then_duplicate

thresholds:
  emergency_minimum:
    value: not_applicable

  dignified_minimum:
    required_features:
      - private_retreat
      - acoustic_sleep_protection
      - ability_to_withdraw
      - daylight_or_nature_access
      - control_over_social_exposure

  comfortable_range:
    strong_mitigators:
      - private_room_or_unit
      - acoustic_separation
      - multiple_social_intensity_spaces
      - daylight
      - nature_views
      - outdoor_access
      - storage
      - thermal_comfort
      - ventilation
      - route_choice
      - quiet_room

  soft_threshold:
    condition: high_density_without_multiple_mitigators
    action: warn

  hard_threshold:
    condition: high_density_without_private_retreat_or_acoustic_strategy_or_quiet_space
    action: duplicate_or_fail

  failure_threshold:
    condition: no_control_over_social_exposure_or_no_private_retreat
    action: fail

human_factor_driver:
  - control
  - retreat
  - noise
  - daylight
  - nature_access
  - perceived_crowding

evidence_quality: moderate
translation_confidence: moderate
regulatory_strength: research_inferred
source_ids:
  - WHO_HOUSING_CROWDING_NCBI
  - EVANS_BUILT_ENVIRONMENT_MENTAL_HEALTH
  - ROLLINGS_EVANS_CROWDING_DESIGN

notes_for_CIaC:
  - Add perceived crowding score separate from physical density.
  - High density can be tolerable when control, privacy, and retreat are strong.
  - UI should show crowding risk even when area-per-person looks acceptable.
optimizer_preference:
  - improve_privacy_controls
  - add_quiet_space
  - add_acoustic_buffer
  - duplicate_pods_if_design_controls_insufficient
ui_warning: Density may be acceptable on paper, but perceived crowding risk is high due to insufficient retreat, daylight, acoustic control, or choice.
```

---

## 9. Mental-Health Protective Spatial Features

```yaml
domain: mental_health_spatial_features
node_type: mental_health_protective_design
question: What spatial features protect mental health at higher density?
scale_action: duplicate

thresholds:
  emergency_minimum:
    value: shelter_safety_and_basic_privacy
    notes: emergency minimum is not a healthy normal condition

  dignified_minimum:
    required:
      - private_retreat
      - quiet_space
      - daylight
      - nature_access
      - acoustic_sleep_protection
      - resident_control_over_participation

  comfortable_range:
    preferred:
      - private_units
      - pod_micro_commons
      - central_quiet_room
      - multiple_social_intensity_spaces
      - safe_outdoor_access
      - greenery
      - legible_paths
      - noninstitutional_materials
      - good_air_quality
      - thermal_comfort
      - storage

  soft_threshold:
    condition: any_pod_lacks_quiet_or_retreat_space
    action: warn

  hard_threshold:
    condition: no_private_retreat_or_no_quiet_space_or_no_nature_access
    action: fail

  failure_threshold:
    condition: illness_grief_or_care_requires_public_visibility
    action: fail

human_factor_driver:
  - mental_health
  - privacy
  - grief
  - care
  - sensory_load
  - autonomy

evidence_quality: moderate
translation_confidence: moderate
regulatory_strength: research_inferred
source_ids:
  - SURGEON_GENERAL_SOCIAL_CONNECTION
  - WHO_HOUSING_2018
  - EVANS_BUILT_ENVIRONMENT_MENTAL_HEALTH
  - ROLLINGS_EVANS_CROWDING_DESIGN

notes_for_CIaC:
  - Mental health design features should become a capability effect or gate.
  - Missing quiet space should be a hard warning at village-block scale.
optimizer_preference:
  - add_quiet_room
  - add_private_retreat
  - add_green_threshold_space
ui_warning: Mental-health protective features are missing or insufficient at this density.
```

---

## 10. Common House Scaling

```yaml
domain: common_house_scaling
node_type: common_house_network
question: Should a community of 300, 700, or 1500 have one common house, several neighborhood commons, or both?
scale_action: hybrid

thresholds:
  emergency_minimum:
    value: emergency_gathering_or_safe_room
    notes: emergency shelter function is separate from common-house social function

  dignified_minimum:
    value: accessible_third_place_per_neighborhood_or_village_block

  comfortable_range:
    80_residents:
      pattern: one_common_house_plus_pod_micro_commons
    300_residents:
      pattern: 3_to_4_neighborhood_common_houses_plus_district_venue
    700_residents:
      pattern: 7_to_9_neighborhood_commons_plus_district_cultural_learning_workshop_venues
    1500_residents:
      pattern: 10_to_20_neighborhood_commons_plus_town_city_layer_and_regional_membrane

  soft_threshold:
    value: 100
    unit: residents_served_by_one_common_house
    action: warn_and_plan_neighborhood_commons

  hard_threshold:
    value: 150
    unit: residents_served_by_one_common_house_as_only_social_heart
    action: duplicate_common_house

  failure_threshold:
    condition: one_common_house_is_sole_social_cultural_care_governance_node_above_150
    action: fail

human_factor_driver:
  - social_comfort
  - third_place_access
  - clique_risk
  - institutional_feel
  - belonging

evidence_quality: low
translation_confidence: moderate
regulatory_strength: heuristic
source_ids:
  - OLDENBURG_THIRD_PLACE
  - COHOUSING_ASSOCIATION
  - SURGEON_GENERAL_SOCIAL_CONNECTION
  - DUNBAR_SOCIAL_LAYERS

notes_for_CIaC:
  - Common house should duplicate by neighborhood.
  - Larger venues may exist at district/town layers but should not replace neighborhood commons.
optimizer_preference:
  - duplicate_common_house
  - add_district_venue_only_after_neighborhood_commons
ui_warning: One common house is serving too many residents as a single social heart. Add neighborhood commons.
```

---

## 11. What Duplicates First as Population Scales

```yaml
domain: duplication_priority
node_type: human_safety_duplication_order
question: When scaling population, what should duplicate first to preserve psychological safety?
scale_action: hybrid

duplicate_first:
  - residential_pods
  - quiet_rooms
  - bathrooms_hygiene_access
  - neighborhood_commons
  - care_rooms_check_in_points
  - food_pickup_dining_points
  - social_threshold_spaces
  - accessible_routes
  - emergency_water_distribution_points
  - local_tool_caches

duplicate_second:
  - kitchen_production_capacity
  - laundry_nodes
  - workshop_nodes
  - social_cultural_spaces
  - learning_rooms
  - governance_circles

federate_not_duplicate_first:
  - advanced_workshops
  - professional_clinics
  - legal_finance_administration
  - district_food_procurement
  - regional_energy
  - transit_spine
  - hospitals_universities

do_not_scale_linearly:
  - common_meals
  - direct_assembly
  - care_labor
  - conflict_resolution
  - social_events
  - maintenance_backlog
  - kitchen_cleanup
  - resident_onboarding

evidence_quality: moderate
translation_confidence: moderate
regulatory_strength: heuristic
source_ids:
  - WHO_HOUSING_CROWDING_NCBI
  - DUNBAR_SOCIAL_LAYERS
  - SURGEON_GENERAL_SOCIAL_CONNECTION
  - NIST_COMMUNITY_RESILIENCE_GUIDE

notes_for_CIaC:
  - The optimizer should duplicate human-sensitive functions earlier than technical functions.
  - Efficiency functions can centralize more than psychological-safety functions.
```

---

## 12. CIaC Implementation Translation

```yaml
recommended_node_policy_updates:
  residential_pod:
    minimum: 12
    preferred: 20
    maximum: 24
    hard_max: 30
    action_above_max: duplicate
    source_ids:
      - WHO_HOUSING_CROWDING_NCBI
      - COHOUSING_ASSOCIATION

  elder_high_care_pod:
    minimum: 6
    preferred: 10
    maximum: 12
    hard_max: 14
    action_above_max: duplicate
    source_ids:
      - GREEN_HOUSE_SMALL_HOUSE

  common_house:
    minimum: 30
    preferred: 80
    maximum: 100
    hard_max: 150
    action_above_max: duplicate_neighborhood_commons_and_federate_district_venue
    source_ids:
      - COHOUSING_ASSOCIATION
      - OLDENBURG_THIRD_PLACE

  common_meal_wave:
    minimum: 12
    preferred: 40
    maximum: 60
    hard_max: 80
    action_above_max: add_meal_wave_or_duplicate_dining

  quiet_room:
    minimum: 1_per_village_block
    preferred: 1_per_pod_plus_central
    action_above_80: duplicate

  pod_lounge_micro_commons:
    preferred: 1_per_residential_pod
    action: duplicate_with_pod
```

---

## 13. UI / 3D World Recommendations

```yaml
viewer_overlays:
  perceived_crowding:
    show:
      - pod_population
      - private_retreat_status
      - acoustic_risk
      - quiet_space_access
      - path_social_exposure

  social_scale:
    show:
      - intimate_groups
      - pod_groups
      - neighborhood_commons
      - village_block
      - district_federation

  common_house:
    show:
      - residents_served
      - active_dining_wave
      - open_unprogrammed_hours
      - clique_capture_warning
      - quiet_alternative_availability

  life_mode:
    show:
      - free_time_destinations_beyond_home
      - quiet_room_use
      - maker_art_study_social_nature_use
      - required_work_vs_self_directed_time

warnings:
  pod_overloaded:
    message: This pod is exceeding comfortable residential scale. Duplicate or subdivide.

  no_private_retreat:
    message: Private retreat is missing or insufficient. Dignity floor at risk.

  common_house_institutional:
    message: Common house is serving too many residents as one social node. Add neighborhood commons.

  perceived_crowding:
    message: Density may be acceptable, but crowding risk is high due to lack of retreat, daylight, acoustic control, or choice.

  quiet_space_missing:
    message: No low-social-energy retreat space is available at this scale.

  one_social_heart:
    message: One social center is insufficient above village-block scale. Duplicate neighborhood commons.
```

---

## 14. Suggested Tests

```yaml
tests:
  residential_pod_threshold:
    input_population_per_pod: 25
    expected: soft_warning

  residential_pod_hard:
    input_population_per_pod: 31
    expected: duplicate_required

  high_care_pod_hard:
    input_population_per_high_care_pod: 14
    expected: duplicate_required

  common_house_threshold:
    residents_served: 120
    expected: warn_duplicate_neighborhood_commons

  common_house_hard:
    residents_served: 151
    expected: hard_duplicate

  perceived_crowding_score:
    density: high
    private_retreat: true
    acoustic_strategy: true
    quiet_room: true
    expected: warn_not_fail

  perceived_crowding_fail:
    density: high
    private_retreat: false
    acoustic_strategy: false
    quiet_room: false
    expected: fail

  social_scale_300:
    population: 300
    expected:
      - multiple_neighborhood_commons
      - district_venue
      - no_single_common_house
```

---

## 15. Status

```yaml
status: approved_as_research_input
not_yet:
  - final_verified_policy
  - professional_architectural_standard
  - clinical_mental_health_standard
  - code_or_zoning_standard
next_step:
  - create_scaling_policy_schema_and_machine_readable_yaml
```
