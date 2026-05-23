# CIaC Water Module: Resilient Water Commons

**Module ID:** `water.resilient_water_commons.v0_1`  
**Status:** Draft requirement module  
**Purpose:** Define the default water system for a scalable Minimum Viable Dignified Infrastructure complex.  
**Primary design question:** What water infrastructure best guarantees safe potable water, reduces waste, survives bad years, supports food and sanitation, and remains maintainable without becoming a fragile high-tech system?

---

## 1. Core Thesis

The CIaC water baseline should **not** be romantic off-grid water independence.

Water is too sacred, too safety-critical, and too jurisdictionally constrained to treat as a lifestyle experiment.

The recommended baseline is a **Resilient Water Commons**:

```text
regulated public water where available
or professionally permitted and tested well water
+ safe potable storage
+ water-efficient fixtures
+ leak detection and metering
+ rainwater capture for non-potable uses
+ drought-aware irrigation
+ optional treated non-potable reuse where legal and professionally reviewed
+ emergency potable buffer
+ clear testing, inspection, and maintenance routines
+ visible water status dashboard
```

The goal is not water purity theater.

The goal is **safe, boring, resilient water**.

---

## 2. Guiding Sentence

> Potable water should be conservative, protected, tested, and boring; non-potable water can be innovative, but only if it reduces burden without adding unacceptable safety risk.

---

## 3. Strategic Decision

The best default model is:

# A dual-layer water commons with conservative potable supply and flexible non-potable resilience.

```yaml
water_strategy:
  potable_layer:
    priority: sacred_floor
    preferred_sources:
      - regulated_public_water
      - permitted_private_or_shared_well
      - delivered_potable_backup
    treatment:
      principle: contaminant_specific
      avoid: unnecessary_black_box_filtration

  non_potable_layer:
    priority: resilience_and_conservation
    preferred_sources:
      - roof_collected_rainwater
      - stormwater_where_legal_and_safe
      - treated_graywater_where_legal_and_professionally_reviewed
    preferred_uses:
      - irrigation
      - toilet_flushing_where_code_allows
      - laundry_cold_water_where_code_allows
      - washdown_where_safe
      - landscape_establishment

  avoid_as_default:
    - drinking_untreated_rainwater
    - untested_well_water
    - blackwater_reuse_as_baseline
    - atmospheric_water_generators_as_baseline
    - desalination_as_baseline
    - complex_vendor_locked_water_tech
    - single_source_water_dependency
```

### Rationale

Drinking water must prioritize health and reliability over novelty.

Rainwater and reuse are valuable, but they are best treated as non-potable conservation and resilience tools unless local law, professional design, and ongoing testing support potable use.

---

## 4. Research Anchors

This module is grounded in the following research and precedent categories.

### 4.1 Household water use

EPA WaterSense reports that each American uses an average of about 82 gallons of water per day at home, and that water-efficient fixtures and appliances can reduce use by at least 20%.

**Design implication:** CIaC should not accept conventional wasteful water use as inevitable. The model should use efficient fixtures, leak detection, shared laundry, efficient irrigation, and water budgeting.

### 4.2 Minimum emergency water

CDC emergency guidance recommends storing at least 1 gallon of water per person per day for 3 days and trying to store a 2-week supply if possible.

**Design implication:** The module should include a separate emergency potable buffer and should distinguish emergency drinking/cooking water from full normal water service.

### 4.3 Minimum health and hygiene water

WHO emergency water guidance indicates that roughly 20 liters per person per day is a minimum quantity of safe water for essential health and hygiene.

**Design implication:** The app should model multiple water service levels: survival, emergency minimum, constrained dignity, normal dignity, and abundance.

### 4.4 Private well responsibility

EPA and CDC guidance recommend annual testing of private wells for total coliform bacteria, nitrates, total dissolved solids, and pH, with additional testing based on local contaminants.

**Design implication:** Well water must include source protection, annual certified-lab testing, contaminant-specific treatment, and maintenance logs.

### 4.5 Rainwater safety

CDC states that rainwater is not necessarily safe to drink without removing germs and chemicals, and recommends testing and proper maintenance if rainwater is used for drinking, cooking, or bathing.

**Design implication:** Rainwater should default to non-potable use unless local law, treatment, maintenance, and testing support potable use.

### 4.6 Onsite non-potable water reuse

EPA describes onsite non-potable water reuse systems as systems that capture and treat sources such as wastewater, greywater, stormwater, or roof-collected rainwater for non-drinking uses.

**Design implication:** Onsite reuse can reduce potable demand, but it must be governed by treatment requirements, oversight, public-health review, and maintenance capacity.

### 4.7 Water reuse standards

NSF/ANSI 350 provides guidelines for onsite greywater and wastewater reuse treatment systems.

**Design implication:** Any reuse technology should prefer certified systems or professionally reviewed designs rather than improvised plumbing.

### 4.8 Plumbing and rainwater codes

ICC CodeNotes on rainwater harvesting references CSA B805/ICC 805 and explains that rainwater harvesting systems must be understood through plumbing-code and public-health requirements.

**Design implication:** The app should model rainwater at pattern level and flag professional/code review rather than pretending to generate final plumbing plans.

---

## 5. Recommended Scale

The water module should support the same first serious population as the housing and food modules.

```yaml
population:
  minimum_meaningful_scale: 50
  ideal_first_model: 80
  upper_bound_before_replication: 150
```

### Scale Logic

```text
Below 50:
  water systems may be too dependent on one operator and one source.

Around 80:
  storage, testing, maintenance, monitoring, and backup roles become realistic.

Above 150:
  water governance, regulatory classification, public-water-system thresholds, treatment complexity, and operations burden may increase sharply.
```

### Scaling Method

Water should scale through repeated village-block water cells rather than one brittle mega-system.

```yaml
scaling:
  50-100_residents:
    water_nodes: 1_primary
    backup_storage: required
    water_steward_team: 2-3_people

  100-150_residents:
    water_nodes: 1_primary_plus_backup
    submetered_zones: required
    nonpotable_separation: required

  above_150_residents:
    recommendation: replicate_village_block_or_professionalize_utility_operations
    reason: avoid_informal_public_utility_without_capacity
```

---

## 6. Default Prototype

```yaml
default_prototype:
  name: resilient_water_commons_80
  residents: 80

  potable_source:
    preferred: regulated_public_water_if_available
    alternate: permitted_shared_well_with_professional_design_and_testing
    emergency_backup: delivered_potable_water_or_stored_emergency_water

  nonpotable_sources:
    - roof_collected_rainwater
    - stormwater_capture_for_landscape_where_legal
    - treated_graywater_where_legal_and_reviewed

  facilities:
    - potable_water_entry_or_well_house
    - treatment_and_testing_station
    - potable_storage
    - nonpotable_cistern
    - pump_or_pressure_system
    - metered_distribution_zones
    - leak_detection_layer
    - irrigation_manifold
    - emergency_dispensing_point
    - sampling_points
    - maintenance_storage

  targets:
    normal_indoor_use_target: 35-55_gallons_per_person_per_day
    warning_above: 65_gallons_per_person_per_day
    conventional_reference: 82_gallons_per_person_per_day
    emergency_potable_minimum: 1_gallon_per_person_per_day
    emergency_potable_minimum_days: 14
    preferred_emergency_potable_days: 30
    essential_health_hygiene_reference: 20_liters_per_person_per_day
```

### Notes on Targets

The normal indoor use target is a modeling target, not a legal standard.

It assumes:
- efficient fixtures
- shared laundry
- leak detection
- no high-water lawns
- water-conscious operations
- potable water used only where potable water is needed

---

## 7. Water Service Levels

The app should model water as service levels, not a single number.

```yaml
water_service_levels:
  survival:
    potable_water: 1_gallon_per_person_per_day
    includes:
      - drinking
      - minimal_cooking
      - minimal_hygiene
    duration: short_emergency_only
    dignity_status: emergency_only

  essential_health:
    safe_water: 20_liters_per_person_per_day
    includes:
      - drinking
      - cooking
      - essential_hygiene
    dignity_status: constrained

  constrained_dignity:
    water: 20-35_gallons_per_person_per_day
    includes:
      - drinking
      - cooking
      - bathing
      - toilets_or_sanitation
      - basic_laundry
    dignity_status: acceptable_short_term

  normal_dignity:
    water: 35-55_gallons_per_person_per_day
    includes:
      - normal_hygiene
      - laundry
      - shared_kitchen
      - cleaning
      - efficient_fixtures
    dignity_status: default_target

  high_use_warning:
    water: above_65_gallons_per_person_per_day
    includes:
      - likely_waste
      - leaks
      - inefficient_fixtures
      - behavior_or_system_issue
    dignity_status: investigate
```

### Principle

```text
The system should reduce water waste without making residents feel punished for being clean, healthy, or comfortable.
```

---

## 8. Source Hierarchy

The water system should rank sources by safety, reliability, cost, maintenance burden, and legal feasibility.

```yaml
source_hierarchy:
  tier_1_preferred:
    regulated_public_water:
      use: potable_primary
      rationale: professionally treated_and_monitored
      app_requirement: consumer_confidence_report_or_local_quality_reference_where_available

  tier_2_preferred_where_public_water_absent:
    permitted_shared_well:
      use: potable_primary
      rationale: local_control_and_resilience
      app_requirement:
        - professional_siting
        - legal_permit
        - pump_and_treatment_design
        - certified_lab_testing
        - annual_testing
        - contamination_event_plan

  tier_3_resilience:
    stored_potable_water:
      use: emergency_backup
      rationale: short_term_continuity
      app_requirement:
        - rotation_schedule
        - protected_storage
        - emergency_distribution_plan

  tier_4_nonpotable:
    rainwater_capture:
      use: irrigation_toilet_laundry_where_legal
      rationale: reduces_potable_demand
      app_requirement:
        - first_flush_or_pre_filtration_where_appropriate
        - cistern_maintenance
        - nonpotable_labeling
        - cross_connection_prevention
        - health_department_or_code_review

  tier_5_nonpotable_advanced:
    onsite_reuse:
      use: toilet_irrigation_laundry_where_legal
      rationale: conservation_and_drought_resilience
      app_requirement:
        - certified_or_professionally_reviewed_system
        - monitoring
        - treatment_targets
        - maintenance_role
        - local_authority_approval
```

---

## 9. Potable Water Requirements

Potable water is the floor. It must not be compromised to chase sustainability points.

```yaml
potable_water:
  required:
    - known_source
    - legal_access
    - source_protection
    - treatment_if_needed
    - certified_lab_testing_where_private_source
    - annual_testing_schedule
    - emergency_testing_after_flood_or_repair
    - protected_storage_if_stored
    - sanitary_sampling_points
    - contamination_response_plan
    - alternate_supply_plan

  private_well_testing_minimum:
    annual:
      - total_coliform_bacteria
      - nitrates
      - total_dissolved_solids
      - pH

    event_based:
      - after_flooding
      - after_well_repair
      - after_sudden_taste_color_or_odor_change
      - after_nearby_contamination_event
      - after_unexplained_illness_cluster

    local_contaminants:
      requirement: consult_local_health_department
```

### Potable Water Principle

```text
No water system may be considered valid if residents cannot identify the source, testing status, treatment status, and fallback plan for drinking water.
```

---

## 10. Non-Potable Water Strategy

Non-potable water should reduce potable demand without introducing public-health confusion.

```yaml
nonpotable_water:
  preferred_uses:
    - irrigation
    - toilet_flushing_where_allowed
    - laundry_cold_water_where_allowed
    - washdown_where_safe
    - compost_system_support_where_safe
    - fire_reserve_where_designed

  required_controls:
    - clear_labeling
    - separate_piping
    - cross_connection_prevention
    - backflow_prevention
    - maintenance_logs
    - treatment_level_matched_to_use
    - public_health_review_where_required

  fail_if:
    - nonpotable_water_can_enter_potable_distribution
    - residents_cannot_tell_potable_from_nonpotable
    - no_maintenance_owner
    - no_testing_or_treatment_plan
```

### Non-Potable Principle

```text
Non-potable reuse is valuable only if nobody has to wonder whether the water is safe to drink.
```

---

## 11. Rainwater Capture

Rainwater capture is useful, but it should be treated honestly.

```yaml
rainwater_capture:
  default_status: nonpotable_resilience_layer

  preferred_uses:
    - garden_irrigation
    - greenhouse_irrigation
    - orchard_establishment
    - landscape_watering
    - toilet_flushing_where_code_allows
    - laundry_where_code_allows_and_treated

  required_components:
    - catchment_area_model
    - rainfall_model
    - gutter_and_pre_screening
    - first_flush_or_debris_management_where_appropriate
    - cistern
    - overflow_path
    - mosquito_and_pest_control
    - sediment_management
    - pump_or_gravity_distribution
    - nonpotable_labeling
    - maintenance_schedule

  potable_use:
    default: false
    allowed_only_if:
      - local_law_allows
      - professional_design
      - appropriate_filtration
      - disinfection
      - regular_testing
      - public_health_review
      - resident_training
```

### Rainwater Principle

```text
Rainwater should first make gardens, food resilience, and drought response stronger. It should not be assumed safe to drink.
```

---

## 12. Water Demand Categories

The app should separate demand categories.

```yaml
demand_categories:
  potable_required:
    - drinking
    - cooking
    - dishwashing_final_rinse
    - handwashing
    - bathing
    - medical_and_care_uses

  potable_or_approved_nonpotable_depending_on_code:
    - laundry
    - toilet_flushing
    - cleaning
    - irrigation_of_non_food_landscape

  special_review_required:
    - edible_crop_irrigation_with_reused_water
    - greenhouse_misting
    - animal_water
    - compost_or_sanitation_process_water
    - fire_suppression_storage
```

### Demand Principle

```text
Use potable water where human health requires it. Use fit-for-purpose water everywhere else when law, safety, and maintenance allow.
```

---

## 13. Storage and Resilience

Water storage must be split between potable emergency storage and non-potable operational storage.

```yaml
water_storage:
  potable_emergency_storage:
    minimum:
      gallons_per_person_per_day: 1
      days: 14
    preferred:
      gallons_per_person_per_day: 1
      days: 30
    for_80_residents:
      minimum_14_day_gallons: 1120
      preferred_30_day_gallons: 2400
    includes:
      - drinking
      - cooking
      - minimal_hygiene
    rotation_required: true

  essential_health_storage_reference:
    liters_per_person_per_day: 20
    for_80_residents:
      liters_per_day: 1600
      gallons_per_day_approx: 423
    note: useful_for_short_term_constrained_service_modeling

  normal_daily_demand_model:
    target_gallons_per_person_per_day: 35-55
    for_80_residents:
      target_daily_gallons: 2800-4400
    conventional_reference_gallons_per_person_per_day: 82
    conventional_80_resident_daily_gallons: 6560

  nonpotable_storage:
    purpose:
      - irrigation
      - drought_buffer
      - toilet_or_laundry_where_allowed
      - fire_or_washdown_where_designed
    sizing_inputs:
      - roof_catchment_area
      - rainfall_distribution
      - dry_spell_duration
      - irrigation_demand
      - overflow_management
```

---

## 14. Drought Strategy

Drought resilience should be designed as graceful degradation.

```yaml
drought_strategy:
  normal_conditions:
    - efficient_fixtures
    - rainwater_irrigation
    - soil_moisture_monitoring
    - mulching
    - drought_resistant_landscape
    - leak_detection

  drought_stage_1:
    triggers:
      - rainfall_deficit
      - cistern_below_50_percent
      - well_recharge_concern
    actions:
      - reduce_irrigation
      - prioritize_food_crops
      - pause_nonessential_washing
      - inspect_for_leaks
      - switch_to_drought_menu_in_food_module

  drought_stage_2:
    triggers:
      - cistern_below_25_percent
      - well_yield_reduction
      - local_water_restrictions
    actions:
      - eliminate_nonessential_irrigation
      - prioritize_potable_and_sanitation
      - purchase_or_deliver_water_if_needed
      - activate emergency water dashboard
      - reduce common laundry frequency if dignified alternatives exist

  drought_stage_3:
    triggers:
      - potable_source_threatened
      - emergency_storage_drawdown
      - health_or_sanitation_risk
    actions:
      - external assistance
      - emergency supply contracts
      - evacuation_or_temporary_relocation_plan_if_needed
```

### Drought Principle

```text
Comfort may degrade before food, sanitation, and health degrade. Dignity must not be casually sacrificed.
```

---

## 15. Leak Detection and Conservation

The cheapest water is often the water not wasted.

```yaml
conservation:
  required:
    - WaterSense_or_equivalent_low_flow_fixtures_where_available
    - efficient_toilets
    - efficient_showers
    - efficient_laundry
    - submetering_by_building_or_pod
    - leak_detection
    - visible_water_dashboard
    - irrigation_controls
    - drought_tolerant_landscape
    - no_default_high_water_lawns

  shared_infrastructure_advantages:
    - shared_laundry_reduces_duplicate_appliances
    - common_kitchen_reduces_duplicate_dishwashing
    - centralized_monitoring_detects_abnormal_use
    - maintenance_team_can_fix_leaks_quickly
```

### Conservation Principle

```text
Conservation should be mostly infrastructure, not resident guilt.
```

---

## 16. Food Module Interface

Water and food are tightly coupled.

```yaml
food_water_interface:
  required:
    - irrigation_budget
    - crop_priority_list
    - greenhouse_water_demand
    - drought_crop_plan
    - wash_pack_water_plan
    - food_safety_water_quality_requirement
    - emergency_menu_for_low_water_conditions

  edible_crop_irrigation:
    required_review:
      - source_quality
      - local_law
      - pathogen_risk
      - application_method
      - crop_contact_risk
```

### Interface Principle

```text
Food resilience cannot be modeled without water resilience.
```

---

## 17. Sanitation Module Interface

Water and sanitation must be co-designed.

```yaml
sanitation_water_interface:
  required:
    - toilet_flush_demand
    - composting_or_dry_toilet_option_where_legal
    - handwashing_potable_or_safe_water_requirement
    - greywater_generation
    - blackwater_separation
    - pathogen_risk
    - cleaning_water_demand
    - emergency_sanitation_water_plan

  special_warning:
    - reducing_water_use_must_not_break_sanitation_or_hygiene
```

### Interface Principle

```text
Water conservation that undermines hygiene is false efficiency.
```

---

## 18. Energy Module Interface

Water depends on energy for pumps, controls, treatment, monitoring, and cold-weather protection.

```yaml
energy_water_interface:
  critical_loads:
    - well_pump_or_booster_pump
    - treatment_system
    - monitoring_system
    - freeze_protection_where_needed
    - pressure_system
    - emergency_lighting_at_water_points

  required:
    - backup_power_for_critical_pumps
    - gravity_or_manual_fallback_where_possible
    - critical_load_shedding_priority
```

### Interface Principle

```text
A water system that cannot move water during an outage is not resilient.
```

---

## 19. Care and Health Interface

Some residents have higher water needs.

```yaml
care_health_water_interface:
  higher_need_groups:
    - infants
    - pregnant_residents
    - elders
    - disabled_residents
    - medically_vulnerable_residents
    - residents_with_wound_care_or_hygiene_needs
    - pets_or_service_animals_where_present

  required:
    - extra emergency allocation
    - accessible water access points
    - care-room water reliability
    - illness-wave hygiene plan
```

### Care Principle

```text
Averages are dangerous. Water planning must protect high-need residents.
```

---

## 20. Automation-Favoring Requirements

Automation should make the water system legible and safe.

```yaml
automation_requirements:
  water_dashboard:
    required: true
    purpose:
      - show_daily_use
      - show_storage_days_remaining
      - show_source_status
      - show_test_status
      - show_warnings

  submetering:
    required: true
    purpose:
      - detect_abnormal_use
      - find_leaks
      - understand_pod_demand
      - avoid blame_without_data

  leak_detection:
    required: true
    purpose:
      - early_alerts
      - reduce_water_loss
      - reduce_damage

  tank_level_monitoring:
    required: true
    purpose:
      - emergency_buffer_awareness
      - drought_response
      - irrigation_planning

  testing_schedule_engine:
    required: true
    purpose:
      - annual_tests
      - event_based_tests
      - lab_results_tracking
      - review_flags

  maintenance_scheduler:
    required: true
    purpose:
      - filter_changes
      - cistern_cleaning
      - pump_inspection
      - valve_exercise
      - backflow_prevention_review

  scenario_forecaster:
    required: true
    purpose:
      - drought_simulation
      - contamination_response
      - outage_response
      - source_loss_response

  avoid:
    - black_box_AI_water_safety_claims
    - treatment_recommendations_without_contaminant_data
    - fully_automated_decisions_that_affect_potable_safety
    - sensor_only_safety_without_lab_testing
```

### Automation Principle

```text
Automate visibility, reminders, alarms, and scenario planning. Do not automate away accountability for water safety.
```

---

## 21. Water Roles

```yaml
water_roles:
  water_steward:
    purpose: overall water commons coordination
    required_backup: true

  testing_steward:
    purpose: schedule tests, track lab results, trigger review
    required_backup: true

  maintenance_steward:
    purpose: filters, pumps, cisterns, meters, valves, leak repairs
    required_backup: true

  drought_steward:
    purpose: drought triggers, conservation stages, food-water coordination
    required_backup: true

  emergency_water_steward:
    purpose: emergency distribution, stored water rotation, delivered-water contracts
    required_backup: true

  public_health_liaison:
    purpose: health department, lab, code, and professional review coordination
    required_backup: true
```

### Role Rule

```text
No survival-critical water role may depend on one person.
```

---

## 22. Scenario Simulations

The water module must support stress simulations.

```yaml
water_scenarios:
  normal_year:
    tests:
      - daily_demand
      - fixture_efficiency
      - storage_turnover
      - leak_rate
      - testing_compliance
      - nonpotable_substitution

  drought_year:
    tests:
      - rainfall_deficit
      - cistern_drawdown
      - irrigation_reduction
      - food_module_impact
      - resident_comfort_impact
      - external_water_purchase_need

  potable_source_loss:
    tests:
      - emergency_buffer_days
      - delivered_water_plan
      - distribution_method
      - high_need_resident_protection
      - sanitation_impacts

  contamination_event:
    tests:
      - detection_time
      - boil_water_or_do_not_use_alert
      - alternate_water_distribution
      - retesting
      - system_flush
      - professional_review

  energy_outage:
    tests:
      - pump_power_loss
      - pressure_loss
      - backup_power_runtime
      - gravity_or_manual_fallback
      - cold_weather_freeze_risk

  pipe_leak_or_cistern_failure:
    tests:
      - leak_detection_time
      - water_loss
      - structural_damage_risk
      - repair_parts
      - isolation_valves

  flood_event:
    tests:
      - wellhead_contamination_risk
      - cistern_contamination
      - stormwater_overflow
      - testing_after_event
      - sanitation_cross_risk

  resident_growth:
    tests:
      - demand_increase
      - source_capacity
      - storage_capacity
      - testing_burden
      - regulatory_thresholds
```

---

## 23. Water Gates

The app should fail or warn based on water-system viability.

```yaml
water_gates:
  potable_safety_gate:
    fail_if:
      - potable_source_unknown
      - untested_private_source
      - no_contamination_response_plan
      - no_alternate_potable_supply
      - nonpotable_cross_connection_risk
      - treatment_recommended_without_contaminant_basis

  dignity_gate:
    fail_if:
      - normal_plan_below_essential_health_water_without_emergency_context
      - no_accessible_water_points
      - hygiene_needs_unmet
      - high_need_residents_not_modeled

    warn_if:
      - normal_dignity_target_below_35_gallons_per_person_per_day
      - emergency_plan_relies_on_extreme_conservation_for_more_than_short_duration

  resilience_gate:
    fail_if:
      - less_than_3_days_emergency_potable_water
      - no_backup_for_pump_or_treatment_system
      - no_drought_response_plan
      - no_event_based_testing_plan

    warn_if:
      - less_than_14_days_emergency_potable_water
      - one_source_dependency
      - no_nonpotable_substitution_for_irrigation
      - no_delivered_water_contract_or_fallback

  maintenance_gate:
    fail_if:
      - no_water_steward
      - no_backup_water_steward
      - no_testing_schedule
      - no_filter_or_cistern_maintenance_plan

    warn_if:
      - maintenance_requires_specialist_not_available
      - no_spare_parts_for_critical_components
      - sensor_system_has_no_manual_check

  complexity_gate:
    warn_if:
      - high_tech_treatment_system_without_operator_capacity
      - potable_rainwater_proposed_without_review
      - onsite_reuse_proposed_without_certified_or_professional_design
      - too_many_source_types_for_available_maintenance_capacity

  waste_gate:
    warn_if:
      - daily_use_above_65_gallons_per_person
      - no_submetering
      - no_leak_detection
      - no_irrigation_budget
      - no_water_efficient_fixtures
```

---

## 24. App Modeling Boundary

The app should model water at the level of **system topology, capacity, safety gates, and operations**, not final plumbing design.

### The App Should Model

```text
water source hierarchy
potable versus non-potable separation
daily demand by category
storage days
emergency buffer
rainwater capture potential
drought response stages
well testing schedule
contamination response
backup water supply
pump and energy dependency
fixture efficiency
leak detection
submetering
irrigation budget
maintenance schedule
professional review requirements
```

### The App Should Not Claim to Solve by Default

```text
final potable treatment design
well siting or drilling
hydrogeology
water rights
public water system classification
pipe sizing
pump sizing
backflow certification
cross-connection inspection
fire suppression engineering
legal compliance
lab testing interpretation without qualified review
```

### Principle

```text
The app should identify what must be true for water dignity and resilience.
Qualified professionals and local authorities must validate health, safety, water rights, engineering, and legal implementation.
```

---

## 25. Required Data Model

```yaml
WaterCommons:
  id: string
  population_served: integer

  sources:
    potable_primary_type: public_water | permitted_well | delivered | other
    potable_primary_status: unknown | provisional | tested | approved | failed
    potable_backup_type: stored | delivered | secondary_well | public_connection | other
    nonpotable_sources:
      rainwater: boolean
      stormwater: boolean
      treated_graywater: boolean
      reclaimed_water: boolean

  demand:
    gallons_per_person_per_day_target: number
    total_daily_demand_gallons: number
    potable_daily_demand_gallons: number
    nonpotable_daily_demand_gallons: number
    irrigation_daily_demand_gallons: number
    care_health_extra_demand_gallons: number

  storage:
    potable_emergency_storage_gallons: number
    potable_emergency_days: number
    normal_operational_storage_gallons: number
    nonpotable_storage_gallons: number
    rainwater_cistern_gallons: number

  safety:
    last_lab_test_date: string
    next_lab_test_due: string
    annual_testing_complete: boolean
    event_based_testing_required: boolean
    contaminants_tested:
      - total_coliform
      - nitrate
      - total_dissolved_solids
      - pH
    treatment_basis: contaminant_specific | precautionary | unknown
    contamination_response_plan: boolean
    cross_connection_prevention: boolean

  operations:
    water_steward: string
    backup_water_steward: string
    maintenance_schedule: boolean
    submetering: boolean
    leak_detection: boolean
    tank_level_monitoring: boolean
    testing_schedule_engine: boolean
    dashboard_available: boolean

  resilience:
    drought_plan: boolean
    delivered_water_fallback: boolean
    backup_power_for_pumps_hours: number
    gravity_or_manual_fallback: boolean
    nonpotable_substitution_percent: number
    high_need_residents_modeled: boolean

  outputs:
    water_safety_status: pass | warn | fail
    emergency_buffer_days: number
    normal_dignity_status: pass | warn | fail
    drought_resilience_score: number
    maintenance_burden_score: number
    complexity_score: number
    life_burden_reduction_score: number
```

---

## 26. Required App Outputs

```yaml
required_outputs:
  - water_system_summary
  - source_hierarchy_report
  - potable_safety_report
  - demand_budget_report
  - storage_capacity_report
  - emergency_buffer_days
  - rainwater_capture_report
  - nonpotable_reuse_report
  - drought_resilience_report
  - testing_schedule
  - maintenance_schedule
  - leak_and_metering_report
  - pump_energy_dependency_report
  - contamination_response_plan
  - professional_review_requirements
  - scenario_failure_report
  - visualization_bundle_metadata
```

---

## 27. Visualization Requirements

The water module should export enough data for a virtual world or dashboard to show how water works.

```yaml
visualization_requirements:
  spatial_objects:
    - potable_source
    - well_house_or_water_entry
    - treatment_station
    - potable_storage
    - nonpotable_cistern
    - rainwater_catchment_roofs
    - irrigation_zones
    - pump_room
    - sampling_points
    - emergency_water_point
    - overflow_paths

  overlays:
    - potable_distribution
    - nonpotable_distribution
    - daily_use_by_zone
    - storage_days_remaining
    - drought_stage
    - testing_status
    - leak_alert
    - contamination_alert
    - pump_power_dependency
    - maintenance_due

  scenario_playback:
    - drought_year
    - contamination_event
    - energy_outage
    - source_loss
    - flood_event
    - resident_growth
```

---

## 28. Best Default Requirements Summary

```yaml
MinimumViableWaterCommons:
  population:
    first_serious_model: 80
    valid_range: 50-150

  philosophy:
    potable_water_conservative: true
    rainwater_as_nonpotable_default: true
    reuse_as_optional_reviewed_layer: true
    total_water_independence_required: false
    visible_status_dashboard: required

  sources:
    public_water_if_available: preferred
    permitted_tested_well_if_no_public_water: preferred
    delivered_potable_backup: required
    rainwater_for_nonpotable: required_where_climate_and_law_allow
    treated_reuse: optional_after_review

  targets:
    normal_indoor_use: 35-55_gallons_per_person_per_day
    warning_above: 65_gallons_per_person_per_day
    emergency_potable: 1_gallon_per_person_per_day
    emergency_potable_minimum: 14_days
    emergency_potable_preferred: 30_days
    essential_health_reference: 20_liters_per_person_per_day

  facilities:
    potable_entry_or_well_house: required
    treatment_and_testing_station: required
    potable_storage: required
    nonpotable_cistern: preferred
    metered_distribution_zones: required
    leak_detection: required
    emergency_dispensing_point: required
    sampling_points: required

  automation:
    water_dashboard: required
    submetering: required
    leak_detection: required
    tank_level_monitoring: required
    testing_schedule_engine: required
    maintenance_scheduler: required
    scenario_forecaster: required

  gates:
    potable_safety_gate: required
    dignity_gate: required
    resilience_gate: required
    maintenance_gate: required
    complexity_gate: required
    waste_gate: required
```

---

## 29. Design Maxims

```text
Do not make drinking water experimental.

Do not drink untreated rainwater.

Do not use untested private well water.

Do not treat sensors as a replacement for lab testing.

Do not reduce water use by making hygiene humiliating.

Do not create a non-potable system residents cannot understand.

Do not add water-reuse complexity without maintenance capacity.

Do not let one person become the water system.

Do not model food resilience without water.

Do not model water resilience without energy.

Use public or professionally tested sources for potable water.

Use rainwater first to protect gardens and reduce potable demand.

Use storage to buy time.

Use metering and leak detection to avoid waste without blame.

Use automation to make water visible, not mysterious.

Use graceful degradation so water stress does not become human degradation.
```

---

## 30. Open Questions for Iteration

```text
1. Should the default prototype assume public water, permitted well, or both as selectable profiles?
2. What normal dignity target should the model use: 35, 45, or 55 gallons per person per day?
3. Should the first prototype include non-potable toilet flushing, or keep rainwater limited to irrigation?
4. Should greywater reuse live in the water module, sanitation module, or a dedicated reuse interface?
5. What emergency buffer is morally acceptable: 14 days, 30 days, or 90 days?
6. Should the app model water rights and withdrawal limits, or only flag them for legal review?
7. Should edible crop irrigation require potable water by default, or allow modeled non-potable sources with review?
8. How should water access be modeled for elders, disabled residents, infants, and illness waves?
9. How much operator training is acceptable before a water system becomes too complex?
10. Should a village block above 150 residents automatically trigger professional utility-operator requirements?
```

---

## 31. Source Notes

The research basis for this draft includes:

- EPA WaterSense statistics and facts on household water use and water-efficient products.
- CDC emergency water storage guidance.
- WHO emergency water quantity guidance.
- EPA private well testing and protection guidance.
- CDC private well testing and rainwater safety guidance.
- EPA onsite non-potable water reuse research and resources.
- NSF/ANSI 350 onsite residential and commercial water reuse treatment system standard.
- ICC CodeNotes on rainwater harvesting systems in the I-Codes.
- National Blue Ribbon Commission / Water Research Foundation guidance for onsite non-potable water systems.
