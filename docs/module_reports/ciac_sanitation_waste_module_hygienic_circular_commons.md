# CIaC Sanitation & Waste Module: Hygienic Circular Commons

**Module ID:** `sanitation_waste.hygienic_circular_commons.v0_1`  
**Status:** Draft requirement module  
**Purpose:** Define the default sanitation and waste system for a scalable Minimum Viable Dignified Infrastructure complex.  
**Primary design question:** What sanitation and waste infrastructure best protects health, preserves dignity, reduces landfill dependence, supports food and soil loops, and remains maintainable without creating unsafe DIY systems or hidden drudgery?

---

## 1. Core Thesis

The CIaC sanitation baseline should **not** be experimental human-waste romanticism.

Human waste is a pathogen pathway before it is a resource. Any attempt to reclaim nutrients must be downstream of safety, legality, training, and professional review.

The recommended baseline is a **Hygienic Circular Commons**:

```text
dignified toilets and bathing
+ code-compliant blackwater treatment
+ safe greywater handling where legal
+ source-separated organics
+ composting of food and yard waste
+ material reuse and repair streams
+ recycling and hazardous-waste separation
+ sanitary cleaning systems
+ PPE and training for waste handlers
+ visible maintenance schedules
+ emergency sanitation fallback
+ professional review for all pathogen-bearing systems
```

The goal is not to make waste disappear.

The goal is to design waste streams so they do not become disease, shame, pollution, hidden labor, or ecological damage.

---

## 2. Guiding Sentence

> Sanitation is the health firewall of the civic floor. Circularity is valuable only after dignity and pathogen control are secured.

---

## 3. Strategic Decision

The best default model is:

# Conservative blackwater, useful greywater, strong organics recovery, and disciplined material streams.

```yaml
sanitation_strategy:
  blackwater_layer:
    priority: sacred_health_floor
    preferred_solutions:
      - public_sewer_where_available
      - permitted_septic_or_decentralized_wastewater_system
      - professionally_designed_cluster_system
    avoid_as_default:
      - DIY_humanure
      - unreviewed_composting_toilets
      - blackwater_reuse
      - informal_land_application
      - systems_requiring_daily_contact_with_human_waste

  greywater_layer:
    priority: fit_for_purpose_reuse
    preferred_uses_where_legal:
      - subsurface_irrigation
      - landscape_support
      - toilet_flushing_only_with_reviewed_treatment
    avoid_as_default:
      - edible_crop_contact
      - unmanaged_storage
      - indoor_exposure
      - cross_connection_with_potable_water

  organics_layer:
    priority: landfill_diversion_and_soil_support
    preferred_streams:
      - food_scraps
      - yard_waste
      - leaves
      - wood_chips
      - garden_residue
    controls:
      - pest_management
      - odor_management
      - carbon_nitrogen_balance
      - moisture
      - oxygen
      - temperature_where_needed

  materials_layer:
    priority: source_reduction_and_reuse
    preferred_order:
      - refuse_unnecessary_materials
      - reduce
      - repair
      - reuse
      - share
      - recycle
      - compost_organics
      - dispose_last
```

### Rationale

Sanitation is too high-stakes to optimize for ideology.

The civic system should feel clean, normal, private, and reliable to residents. Circular recovery should happen where the system can safely manage it.

---

## 4. Research Anchors

This module is grounded in the following research and precedent categories.

### 4.1 Decentralized wastewater systems

EPA describes septic and decentralized wastewater systems as systems that must be designed and maintained effectively to protect public health, preserve water resources, and support community vitality.

**Design implication:** CIaC should treat onsite wastewater as a serious utility, not a DIY side project.

### 4.2 Sanitation safety planning

WHO describes Sanitation Safety Planning as a risk-based approach for managing health risks across the sanitation chain, from containment to conveyance, treatment, reuse, or disposal.

**Design implication:** The module should model sanitation as a chain with hazards and exposure points, not as a single toilet choice.

### 4.3 Worker safety handling human waste

CDC guidance says workers handling human waste or sewage need proper PPE, training, handwashing access, and hygiene precautions.

**Design implication:** Any sanitation model that requires resident handling of sewage, sludge, contaminated solids, or human-waste-derived material must include PPE, training, role limits, and professional review.

### 4.4 Composting toilets

NSF evaluates composting toilets under NSF/ANSI Standard 41, and certified systems must meet performance requirements.

**Design implication:** Composting toilets can be allowed as a reviewed option, but not as an informal baseline. Certified systems and local code acceptance matter.

### 4.5 Food and organics waste

EPA estimates food is a large landfill stream and states that food in landfills generates methane, a powerful short-lived greenhouse gas. EPA also describes composting as requiring the right balance of carbon-rich and nitrogen-rich material, moisture, oxygen, particle size, and temperature.

**Design implication:** Organics diversion and composting belong in the baseline, but should focus first on food scraps, yard waste, and garden residue, not human waste.

### 4.6 Waste hierarchy and circularity

EPA’s sustainable materials management tools emphasize source reduction, reuse, recycling, composting, and landfill diversion.

**Design implication:** The app should not only ask “where does trash go?” It should ask why the material entered the settlement in the first place.

---

## 5. Recommended Scale

The sanitation and waste module should support the same first serious population as the housing, food, and water modules.

```yaml
population:
  minimum_meaningful_scale: 50
  ideal_first_model: 80
  upper_bound_before_replication: 150
```

### Scale Logic

```text
Below 50:
  sanitation can work, but maintenance and waste roles may be fragile.

Around 80:
  shared bath/laundry, organics recovery, recycling, hazardous-waste sorting, maintenance logs, and role backup become realistic.

Above 150:
  wastewater system classification, collection complexity, operator burden, organics volume, hauling contracts, and health oversight may increase sharply.
```

### Scaling Method

Replicate sanitation and waste cells by village block rather than centralizing everything into one informal mega-system.

```yaml
scaling:
  50-100_residents:
    wastewater_node: public_or_permitted_onsite_system
    organics_node: 1_primary
    materials_node: 1_sorting_area
    sanitation_team: 2-4_people

  100-150_residents:
    wastewater_node: professionally_reviewed_cluster_system
    organics_node: 1_primary_plus_overflow
    materials_node: 1_sorting_area_plus_reuse_storage
    sanitation_team: 4-6_people

  above_150_residents:
    recommendation: replicate_village_block_or_professionalize_sanitation_operations
```

---

## 6. Default Prototype

```yaml
default_prototype:
  name: hygienic_circular_commons_80
  residents: 80

  blackwater_solution:
    preferred: public_sewer_if_available
    alternate: permitted_professionally_designed_cluster_septic_or_decentralized_system
    composting_toilets: optional_reviewed_subsystem_not_default

  greywater_solution:
    default: code_compliant_discharge_to_wastewater_system
    optional: simple_reviewed_reuse_for_landscape_or_subsurface_irrigation
    advanced: treated_nonpotable_reuse_only_after_professional_review

  organics_solution:
    required:
      - source_separated_food_scraps
      - yard_waste
      - garden_residue
      - composting_or_regional_compost_service
      - pest_and_odor_controls

  materials_solution:
    required:
      - source_reduction_policy
      - repair_and_reuse_storage
      - recycling_sorting
      - landfill_waste_minimization
      - hazardous_waste_separation
      - sharps_and_medical_waste_protocol
      - e_waste_battery_paint_chemical_collection

  facilities:
    - dignified_private_or_semi_private_toilets
    - bathing_and_handwashing_facilities
    - cleaning_supply_storage
    - waste_sorting_station
    - organics_collection_points
    - compost_or_organics_processing_area
    - reuse_and_repair_storage
    - hazardous_waste_lockup
    - emergency_sanitation_kit
    - PPE_station
    - handwashing_station_near_dirty_work
    - maintenance_log_dashboard
```

---

## 7. Sanitation Service Levels

The app should model sanitation as service levels.

```yaml
sanitation_service_levels:
  emergency_minimum:
    includes:
      - safe_excreta_containment
      - handwashing
      - odor_control
      - privacy_screening
      - emergency_waste_storage_or_disposal
    duration: short_emergency_only
    dignity_status: emergency_only

  constrained_dignity:
    includes:
      - reliable_toilets
      - handwashing
      - basic_bathing
      - menstrual_hygiene_support
      - diaper_or_incontinence_waste_support
      - waste_collection
    dignity_status: acceptable_short_term

  normal_dignity:
    includes:
      - private_or_semi_private_flush_or_equivalent_toilets
      - comfortable_bathing
      - accessible_facilities
      - odor_free_waste_handling
      - regular_cleaning
      - safe_organics_and_material_sorting
    dignity_status: default_target

  enhanced_resilience:
    includes:
      - backup_toilets
      - greywater_reuse_where_safe
      - organics_composting
      - repair_reuse_loop
      - emergency_sanitation_supplies
      - care_support_for_high_need_residents
    dignity_status: preferred
```

### Principle

```text
Sanitation must never become a place where residents are asked to trade dignity for ecological virtue.
```

---

## 8. Human Waste Strategy

The app should clearly distinguish blackwater, excreta, greywater, organics, and ordinary solid waste.

```yaml
human_waste_strategy:
  blackwater:
    definition: toilet_waste_and_flushwater
    default_handling:
      - public_sewer
      - permitted_septic
      - professionally_designed_decentralized_wastewater_system
    resident_contact: avoid
    professional_review: required

  composting_toilets:
    default_status: optional_reviewed_subsystem
    allowed_only_if:
      - local_law_allows
      - certified_or_professionally_reviewed_system
      - operation_and_maintenance_plan
      - PPE_and_training
      - end_product_handling_plan
      - pathogen_risk_review
      - backup_toilet_plan
      - resident_acceptance
    not_allowed_as:
      - unreviewed_baseline
      - replacement_for_sanitation_professional_review
      - required_sacrifice_for_dignity

  urine_diversion:
    default_status: research_or_optional_reviewed_subsystem
    allowed_only_if:
      - local_law_allows
      - storage_or_treatment_plan
      - odor_control
      - cross_contamination_controls
      - agricultural_use_review
      - resident_acceptance
```

### Human Waste Principle

```text
Do not turn residents into wastewater operators unless the system, training, equipment, law, and consent actually support that role.
```

---

## 9. Greywater Strategy

Greywater can be useful, but it must be treated as potentially contaminated water.

```yaml
greywater_strategy:
  sources:
    lower_risk:
      - showers
      - bathroom_sinks
      - laundry_where_detergents_are_compatible

    higher_risk_or_excluded_by_default:
      - kitchen_sinks
      - dishwashers
      - diaper_laundry
      - infectious_illness_laundry
      - chemical_cleaning_loads

  default_handling:
    - discharge_to_approved_wastewater_system

  optional_reuse:
    allowed_uses_where_legal:
      - subsurface_irrigation
      - ornamental_landscape
      - orchard_or_perennial_support_after_review
      - toilet_flushing_only_with_reviewed_treatment
    avoid:
      - spray_irrigation
      - edible_leafy_crop_contact
      - storage_without_treatment
      - indoor_exposure
      - cross_connection_with_potable_water

  required_controls:
    - local_code_review
    - source_separation
    - labeling
    - backflow_prevention
    - maintenance_plan
    - use_restrictions
    - illness_event_bypass
```

### Greywater Principle

```text
Greywater reuse is a conservation tool, not an excuse to improvise public health.
```

---

## 10. Toilets, Bathing, and Hygiene

Sanitation dignity starts with ordinary embodied needs.

```yaml
toilets_bathing_hygiene:
  required:
    - private_or_semi_private_toilet_access
    - handwashing_at_or_near_toilets
    - accessible_toilets
    - accessible_bathing
    - menstrual_hygiene_disposal
    - diaper_and_incontinence_waste_plan
    - elder_and_disability_support
    - cleaning_schedule
    - odor_control
    - backup_toilet_plan

  preferred:
    - toilets_close_to_sleeping_areas_without_noise_intrusion
    - toilets_close_to_common_house
    - bathing_options_that_support_privacy_and_comfort
    - family_friendly_bathroom
    - gender_inclusive_private_stalls
```

### Hygiene Principle

```text
The resident experience should be normal, clean, private, and unremarkable.
```

---

## 11. Solid Waste Strategy

The solid waste system should prioritize source reduction and reuse before recycling.

```yaml
solid_waste_strategy:
  hierarchy:
    - source_reduction
    - refusal_of_unnecessary_materials
    - repair
    - reuse
    - sharing
    - recycling
    - composting_organics
    - disposal

  required_streams:
    - landfill_waste
    - recyclables
    - food_scraps
    - yard_waste
    - reusable_materials
    - repairable_items
    - hazardous_household_waste
    - e_waste
    - batteries
    - paints_solvents_chemicals
    - sharps_medical_waste_if_present
    - textiles
    - construction_scraps

  required_facilities:
    - labeled_sorting_station
    - covered_collection_bins
    - pest_resistant_food_scrap_bins
    - reuse_shelf_or_storage
    - repair_queue_area
    - hazardous_waste_lockup
    - hauling_pickup_or_dropoff_plan
```

### Waste Principle

```text
Waste sorting should be easier than throwing everything away.
```

---

## 12. Organics and Composting Strategy

Organics recovery should focus first on food scraps, yard waste, garden residue, and carbon materials.

```yaml
organics_strategy:
  required_streams:
    - fruit_and_vegetable_scraps
    - coffee_grounds
    - eggshells_where_accepted
    - yard_waste
    - leaves
    - wood_chips
    - garden_residue

  conditional_streams:
    meat_dairy_oils:
      default: exclude_from_small_open_compost
      allowed_if:
        - managed_commercial_or_enclosed_system
        - pest_control
        - odor_control
        - local_rules_allow

    compostable_packaging:
      default: exclude_unless_facility_accepts
      reason: many_items_require_industrial_composting

  required_controls:
    - carbon_source
    - nitrogen_source
    - moisture_management
    - oxygen_or_turning
    - particle_size_management
    - temperature_monitoring_where_needed
    - pest_exclusion
    - odor_control
    - finished_compost_use_plan
    - contamination_screening
```

### Compost Principle

```text
Compost is infrastructure only when it is managed, monitored, and used. A neglected pile is not circularity.
```

---

## 13. Cleaning and Disinfection

Cleaning labor must be visible, fair, safe, and not gendered by default.

```yaml
cleaning_system:
  required:
    - cleaning_schedule
    - bathroom_cleaning_protocol
    - kitchen_interface_protocol
    - laundry_sanitation_protocol
    - high_touch_surface_protocol
    - illness_wave_protocol
    - cleaning_supply_inventory
    - PPE_for_cleaning
    - chemical_storage
    - ventilation_for_chemical_use
    - training

  labor_tracking:
    required:
      - total_cleaning_hours_per_week
      - bathroom_cleaning_hours
      - waste_station_cleaning_hours
      - organics_area_cleaning_hours
      - high_need_care_cleaning_hours
      - gender_or_role_imbalance_flag
```

### Cleaning Principle

```text
A clean commons should not rely on invisible care labor.
```

---

## 14. Hazardous, Medical, and Special Waste

Special waste must be separated and handled conservatively.

```yaml
special_waste:
  hazardous_household_waste:
    examples:
      - paints
      - solvents
      - pesticides
      - cleaners
      - motor_oil
      - fluorescent_lamps
    required:
      - locked_storage
      - labeling
      - dropoff_or_collection_schedule

  batteries_and_e_waste:
    required:
      - fire_safe_storage
      - recycling_plan
      - no_landfill_default

  sharps_and_medical_waste:
    required_if_present:
      - sharps_container
      - medication_disposal_plan
      - biohazard_review_if_needed
      - care_module_interface

  construction_waste:
    required:
      - salvage_plan
      - reuse_storage
      - recycling_plan
      - hazardous_material_screening
```

### Special Waste Principle

```text
Low-waste living fails if hazardous streams are hidden inside ordinary trash.
```

---

## 15. Wastewater / Septic / Sewer Interface

The app should model wastewater at the pattern and capacity level, not final engineering.

```yaml
wastewater_interface:
  source_streams:
    - toilets
    - bathing
    - sinks
    - laundry
    - kitchen
    - cleaning

  preferred_treatment:
    public_sewer:
      use_if_available: true
      app_requirements:
        - connection_feasibility
        - capacity_review
        - cost_model
        - outage_or_backflow_plan

    septic_or_decentralized:
      use_if_no_sewer: true
      app_requirements:
        - soil_suitability_flag
        - professional_design_required
        - permit_required
        - inspection_required
        - maintenance_contract_or_trained_operator
        - reserve_area_or_repair_plan
        - water_use_compatibility
        - food_business_or_high_strength_wastewater_review

  fail_conditions:
    - no_approved_blackwater_plan
    - no_maintenance_plan
    - wastewater_system_under_sized
    - greywater_reuse_bypasses_legal_review
    - kitchen_common_house_load_not_modeled
```

### Wastewater Principle

```text
The app may decide that wastewater capacity is a blocker. It may not pretend to engineer the solution.
```

---

## 16. Interfaces With Other Modules

### 16.1 Water Module Interface

```yaml
water_interface:
  required:
    - toilet_flush_demand
    - handwashing_water
    - bathing_water
    - laundry_water
    - cleaning_water
    - greywater_generation
    - emergency_sanitation_water_plan
    - nonpotable_reuse_compatibility
```

```text
Water conservation that undermines hygiene is false efficiency.
```

### 16.2 Food Module Interface

```yaml
food_interface:
  required:
    - kitchen_wastewater_load
    - food_scrap_collection
    - compost_feedstock
    - wash_pack_wastewater
    - food_safety_cleaning_waste
    - pest_control_near_food_storage
```

```text
The food system and waste system must be designed as one loop, not two chores.
```

### 16.3 Housing Module Interface

```yaml
housing_interface:
  required:
    - toilet_distance_to_units
    - bathroom_privacy
    - acoustic_separation
    - cleaning_storage
    - waste_station_distance
    - service_access
    - accessible_routes
```

```text
Sanitation dignity is partly architectural.
```

### 16.4 Care & Health Module Interface

```yaml
care_health_interface:
  required:
    - higher_hygiene_needs
    - diaper_waste
    - incontinence_waste
    - medication_disposal
    - sharps
    - illness_wave_cleaning
    - isolation_room_waste
    - caregiver_laundry
```

```text
Sanitation averages fail medically vulnerable residents.
```

### 16.5 Energy Module Interface

```yaml
energy_interface:
  required:
    - sewage_pumps_if_any
    - ventilation
    - compost_aeration_if_any
    - greywater_treatment_if_any
    - lighting_for_waste_areas
    - emergency_power_for_critical_sanitation
```

```text
A sanitation system that fails in an outage must have a backup mode.
```

---

## 17. Labor and Time Model

The sanitation and waste module must count unpleasant labor honestly.

```yaml
sanitation_labor_model:
  labor_categories:
    - bathroom_cleaning
    - bathing_area_cleaning
    - waste_sorting_area_cleaning
    - organics_collection
    - compost_management
    - recycling_management
    - landfill_waste_handling
    - hazardous_waste_management
    - wastewater_system_inspection
    - greywater_system_maintenance
    - emergency_sanitation_management
    - illness_wave_disinfection
    - PPE_and_training

  required_metrics:
    total_sanitation_waste_labor_hours_per_week: number
    labor_hours_per_resident_per_week: number
    unpleasant_labor_hours_per_week: number
    pathogen_exposure_tasks_per_month: number
    unpaid_care_cleaning_hours: number
    gender_or_role_imbalance_flag: boolean
    burnout_risk: low_medium_high
```

### Labor Rule

```text
A circular waste system has failed if it externalizes dignity by making a few people handle everyone else's dirt invisibly.
```

### Target

```yaml
labor_targets:
  sanitation_waste_labor_per_resident:
    target: 0.5-2_hours_per_week
    warning_above: 3_hours_per_week
    fail_above: 5_hours_per_week_unless_voluntary_or_paid

  pathogen_exposure:
    target: minimized
    fail_if:
      - exposure_tasks_without_PPE
      - exposure_tasks_without_training
      - exposure_tasks_without_handwashing_access
```

---

## 18. Automation-Favoring Requirements

Automation should make sanitation legible, scheduled, and safe.

```yaml
automation_requirements:
  waste_stream_dashboard:
    required: true
    purpose:
      - track_waste_volumes
      - track_contamination
      - track_pickups
      - track_organics_flow

  cleaning_scheduler:
    required: true
    purpose:
      - bathrooms
      - common_areas
      - waste_stations
      - illness_wave_escalation

  maintenance_scheduler:
    required: true
    purpose:
      - septic_inspection
      - pumps
      - filters
      - compost_turning
      - bin_cleaning
      - hazardous_waste_dropoff

  organics_monitoring:
    preferred: true
    purpose:
      - temperature
      - moisture
      - odor_events
      - pest_events
      - volume

  role_scheduler:
    required: true
    purpose:
      - distribute_cleaning
      - prevent_single_person_dependency
      - track_unpleasant_labor_fairness

  incident_logger:
    required: true
    purpose:
      - sewage_backup
      - missed_pickup
      - contamination
      - pest_event
      - odor_event
      - exposure_event

  avoid:
    - AI_certified_sanitation_safety
    - black_box_waste_optimization
    - sensor_only_pathogen_claims
    - systems_that_require_constant_manual_tuning
```

### Automation Principle

```text
Automate reminders, logs, fairness, and visibility. Do not automate away responsibility for public health.
```

---

## 19. Scenario Simulations

The sanitation and waste module must support stress simulations.

```yaml
sanitation_waste_scenarios:
  normal_year:
    tests:
      - toilet_access
      - cleaning_labor
      - waste_volume
      - organics_processing
      - recycling_contamination
      - wastewater_maintenance
      - resident_satisfaction

  wastewater_backup:
    tests:
      - containment
      - shutdown
      - alternate_toilet_access
      - cleanup_protocol
      - professional_response
      - exposure_risk

  water_shortage:
    tests:
      - toilet_flush_reduction
      - emergency_toilet_plan
      - handwashing_protection
      - bathing_reduction
      - hygiene_dignity_impact

  energy_outage:
    tests:
      - pump_loss
      - ventilation_loss
      - lighting_loss
      - emergency_sanitation_mode
      - waste_storage_duration

  illness_wave:
    tests:
      - cleaning_escalation
      - isolation_waste
      - laundry_load
      - PPE_use
      - caregiver_burden
      - high_need_residents

  organics_failure:
    tests:
      - odor
      - pests
      - excess_food_scraps
      - hauling_fallback
      - compost_contamination

  resident_growth:
    tests:
      - toilet_capacity
      - wastewater_capacity
      - cleaning_labor
      - waste_station_capacity
      - hauling_frequency
      - regulatory_thresholds

  supply_disruption:
    tests:
      - trash_bag_shortage
      - cleaning_supply_shortage
      - PPE_shortage
      - hauling_interruption
      - emergency_storage
```

---

## 20. Sanitation & Waste Gates

The app should fail or warn based on sanitation and waste viability.

```yaml
sanitation_waste_gates:
  blackwater_safety_gate:
    fail_if:
      - no_approved_blackwater_plan
      - no_public_sewer_or_permitted_onsite_solution
      - human_waste_handling_without_PPE_training_and_review
      - composting_toilet_baseline_without_local_approval
      - wastewater_capacity_not_modeled

  dignity_gate:
    fail_if:
      - insufficient_toilet_access
      - no_private_or_semi_private_toilet_access
      - no_accessible_toilets
      - no_handwashing
      - no_menstrual_hygiene_support
      - no_diaper_or_incontinence_waste_plan_where_needed

    warn_if:
      - toilet_distance_excessive
      - bathroom_cleaning_labor_unassigned
      - shared_bathing_requires_social_exposure

  greywater_gate:
    fail_if:
      - greywater_reuse_without_code_review
      - cross_connection_risk
      - edible_crop_contact_without_review
      - storage_without_treatment_or_time_limit
      - no_illness_bypass

  organics_gate:
    fail_if:
      - food_scraps_collected_without_pest_control
      - compost_area_has_no_carbon_source
      - no_odor_or_pest_response
      - human_waste_added_to_compost_without_review

    warn_if:
      - no_compost_use_plan
      - no_temperature_or_process_tracking
      - meat_dairy_oils_added_to_open_small_scale_compost

  hazardous_waste_gate:
    fail_if:
      - batteries_mixed_with_trash
      - sharps_mixed_with_trash
      - chemicals_unlabeled
      - no_hazardous_waste_storage_or_dropoff_plan

  labor_gate:
    fail_if:
      - sanitation_waste_labor_per_resident_exceeds_5_hours_per_week_by_default
      - pathogen_exposure_without_training
      - cleaning_labor_untracked
      - sanitation_role_has_no_backup

    warn_if:
      - sanitation_waste_labor_per_resident_exceeds_3_hours_per_week
      - unpleasant_labor_concentrated_in_small_group
      - care_cleaning_labor_untracked

  complexity_gate:
    warn_if:
      - too_many_waste_streams_for_available_admin_capacity
      - composting_toilet_system_has_high_operator_burden
      - greywater_treatment_has_vendor_lock_in
      - waste_sorting_rules_are_too_complex_for_daily_use

  circularity_gate:
    warn_if:
      - landfill_waste_above_target
      - organics_not_diverted
      - no_reuse_or_repair_stream
      - no_source_reduction_policy
```

---

## 21. App Modeling Boundary

The app should model sanitation and waste at the level of **service, topology, stream separation, health risk, operations, and professional review**, not final engineering.

### The App Should Model

```text
toilet access
bathroom privacy
handwashing access
wastewater solution type
public sewer versus onsite system
greywater source separation
organics streams
compost capacity
solid waste streams
hazardous waste separation
cleaning labor
PPE needs
role backup
waste hauling
emergency sanitation
pathogen exposure points
scenario failures
professional review requirements
```

### The App Should Not Claim to Solve by Default

```text
septic system design
drainfield sizing
soil percolation testing
public sewer capacity certification
composting toilet legal approval
human-waste-derived compost safety certification
greywater treatment engineering
commercial waste hauling contracts
hazardous waste compliance
medical waste compliance
final health-code approval
```

### Principle

```text
The app should identify what must be true for sanitation dignity and safety.
Qualified professionals and local authorities must validate wastewater, public health, hazardous waste, and legal implementation.
```

---

## 22. Required Data Model

```yaml
SanitationWasteCommons:
  id: string
  population_served: integer

  human_waste:
    blackwater_solution_type: public_sewer | septic | decentralized_cluster | composting_toilet | other
    blackwater_status: unknown | provisional | reviewed | permitted | failed
    professional_review_required: boolean
    backup_toilet_plan: boolean
    composting_toilet_count: integer
    composting_toilet_certified_or_reviewed: boolean

  greywater:
    greywater_reuse_enabled: boolean
    greywater_sources:
      - shower
      - bathroom_sink
      - laundry
      - kitchen
    greywater_destination: wastewater_system | landscape | treatment_system | other
    code_review_complete: boolean
    cross_connection_prevention: boolean
    illness_bypass_plan: boolean

  hygiene:
    toilets_total: integer
    accessible_toilets: integer
    bathing_facilities_total: integer
    accessible_bathing_facilities: integer
    handwashing_points: integer
    menstrual_hygiene_support: boolean
    diaper_incontinence_plan: boolean

  organics:
    food_scrap_collection: boolean
    yard_waste_collection: boolean
    composting_on_site: boolean
    regional_compost_service: boolean
    compost_capacity_kg_per_week: number
    carbon_source_available: boolean
    pest_control_plan: boolean
    odor_control_plan: boolean
    finished_compost_use_plan: boolean

  materials:
    landfill_waste_kg_per_week: number
    recycling_kg_per_week: number
    reuse_repair_kg_per_week: number
    hazardous_waste_storage: boolean
    e_waste_collection: boolean
    battery_collection: boolean
    sharps_medical_waste_protocol: boolean

  cleaning:
    cleaning_schedule: boolean
    cleaning_labor_hours_per_week: number
    PPE_available: boolean
    chemical_storage_safe: boolean
    illness_wave_protocol: boolean

  labor:
    total_sanitation_waste_labor_hours_per_week: number
    labor_hours_per_resident_per_week: number
    unpleasant_labor_concentration_score: number
    pathogen_exposure_tasks_per_month: number
    gender_or_role_imbalance_flag: boolean

  roles:
    sanitation_steward: string
    backup_sanitation_steward: string
    organics_steward: string
    backup_organics_steward: string
    materials_steward: string
    backup_materials_steward: string
    cleaning_steward: string
    backup_cleaning_steward: string

  outputs:
    sanitation_safety_status: pass | warn | fail
    dignity_status: pass | warn | fail
    circularity_score: number
    maintenance_burden_score: number
    labor_fairness_score: number
    pathogen_risk_score: number
    complexity_score: number
    life_burden_reduction_score: number
```

---

## 23. Required App Outputs

```yaml
required_outputs:
  - sanitation_system_summary
  - blackwater_plan_report
  - greywater_plan_report
  - toilet_and_hygiene_access_report
  - solid_waste_stream_report
  - organics_composting_report
  - hazardous_waste_report
  - cleaning_labor_report
  - PPE_and_training_report
  - emergency_sanitation_plan
  - scenario_failure_report
  - role_backup_report
  - professional_review_requirements
  - visualization_bundle_metadata
```

---

## 24. Role Model

```yaml
sanitation_waste_roles:
  sanitation_steward:
    purpose: overall sanitation coordination, toilets, hygiene, wastewater interface
    required_backup: true

  wastewater_liaison:
    purpose: professional system maintenance, septic/sewer inspections, permits, repairs
    required_backup: true

  greywater_steward:
    purpose: greywater system checks where enabled
    required_backup: true

  organics_steward:
    purpose: food scraps, compost, yard waste, carbon source, pest/odor checks
    required_backup: true

  materials_steward:
    purpose: recycling, reuse, repair queue, landfill waste, hauling schedule
    required_backup: true

  hazardous_waste_steward:
    purpose: batteries, e-waste, chemicals, sharps, medical waste interfaces
    required_backup: true

  cleaning_steward:
    purpose: cleaning rotations, supplies, disinfection protocols, labor fairness
    required_backup: true

  emergency_sanitation_steward:
    purpose: emergency toilet kits, water shortage sanitation, outage plans
    required_backup: true
```

### Role Rule

```text
No unpleasant or pathogen-exposure role may become socially invisible.
```

---

## 25. Visualization Requirements

The sanitation and waste module should export enough data for a virtual world or dashboard to show how sanitation and waste work.

```yaml
visualization_requirements:
  spatial_objects:
    - toilets
    - bathing_areas
    - handwashing_points
    - wastewater_node
    - greywater_routes
    - waste_sorting_station
    - organics_collection_points
    - compost_area
    - recycling_area
    - reuse_repair_storage
    - hazardous_waste_lockup
    - emergency_sanitation_point
    - PPE_station
    - service_vehicle_route

  overlays:
    - blackwater_route
    - greywater_route
    - solid_waste_streams
    - organics_flow
    - hazardous_waste_locations
    - cleaning_schedule
    - labor_burden
    - pathogen_risk
    - odor_pest_alert
    - emergency_sanitation_status

  scenario_playback:
    - wastewater_backup
    - water_shortage
    - energy_outage
    - illness_wave
    - organics_failure
    - resident_growth
    - hauling_disruption
```

---

## 26. Best Default Requirements Summary

```yaml
MinimumViableSanitationWasteCommons:
  population:
    first_serious_model: 80
    valid_range: 50-150

  philosophy:
    sanitation_as_health_firewall: true
    circularity_after_safety: true
    human_waste_experimentation: false
    private_hygiene_dignity: required
    invisible_dirty_labor: forbidden

  blackwater:
    public_sewer_if_available: preferred
    permitted_professional_onsite_system_if_no_sewer: required
    composting_toilets: optional_reviewed_not_default
    resident_contact_with_human_waste: avoided

  greywater:
    default_discharge_to_approved_system: true
    reviewed_reuse_optional: true
    edible_crop_contact_default: false
    potable_cross_connection_allowed: false

  organics:
    food_scrap_collection: required
    yard_waste_collection: required
    compost_or_regional_compost_service: required
    pest_odor_controls: required
    human_waste_composting_default: false

  materials:
    source_reduction: required
    reuse_repair_stream: required
    recycling: required
    hazardous_waste_separation: required
    landfill_minimization: required

  automation:
    waste_stream_dashboard: required
    cleaning_scheduler: required
    maintenance_scheduler: required
    role_scheduler: required
    incident_logger: required
    organics_monitoring: preferred

  gates:
    blackwater_safety_gate: required
    dignity_gate: required
    greywater_gate: required
    organics_gate: required
    hazardous_waste_gate: required
    labor_gate: required
    complexity_gate: required
    circularity_gate: required
```

---

## 27. Design Maxims

```text
Do not make human waste experimental.

Do not confuse composting food scraps with composting excreta.

Do not make residents trade hygiene for ecological virtue.

Do not let sanitation become humiliating.

Do not hide dirty labor inside community spirit.

Do not create greywater systems people cannot understand.

Do not put circularity ahead of pathogen control.

Do not use composting toilets as default unless law, certification, maintenance, and resident consent support them.

Do not let one person become the sewer department.

Do not make waste sorting so complex that everyone fails.

Use public sewer or professional onsite wastewater systems for blackwater.

Use organics recovery for food and yard waste first.

Use reuse and repair to prevent waste before recycling.

Use automation to schedule, remind, log, and fairly distribute unpleasant work.

Use visual dashboards to make waste streams legible.

Use professional review wherever pathogens, permits, or hazardous waste are involved.
```

---

## 28. Open Questions for Iteration

```text
1. Should the default prototype assume public sewer, permitted septic, or selectable profiles?
2. Should composting toilets be excluded from v0 entirely or included as a reviewed optional subsystem?
3. Should greywater reuse be modeled in v0 or deferred until after water/sanitation basics are stable?
4. What toilet-to-resident ratio should the model use for normal dignity?
5. What bathing-to-resident ratio should the model use?
6. Should the module require private bathrooms in all dwelling units, or allow shared pod bathrooms if privacy is strong?
7. What landfill diversion target is realistic for the first model?
8. Should the system model commercial kitchen wastewater separately from household wastewater?
9. How should illness-wave cleaning labor be distributed without creating unfair burden?
10. Should organics processing be onsite compost, regional compost service, or a hybrid by default?
11. Should the model include animals, pet waste, and service animal waste in v0?
12. What legal-review threshold should trigger automatic failure versus warning?
```

---

## 29. Source Notes

The research basis for this draft includes:

- EPA septic and decentralized wastewater system resources.
- WHO Sanitation Safety Planning and safe use / disposal of wastewater, greywater, and excreta.
- CDC guidance for workers handling human waste and sewage.
- NSF composting toilet guidance and NSF/ANSI Standard 41.
- EPA composting guidance for food scraps and yard waste.
- EPA wasted food and landfill methane resources.
- EPA sustainable materials management and waste-stream transformation resources.
- OSHA and public-health guidance related to exposure risks from wastewater and sewage.
