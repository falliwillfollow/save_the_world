# CIaC Energy Module: Critical Load Energy Commons

**Module ID:** `energy.critical_load_energy_commons.v0_1`  
**Status:** Draft requirement module  
**Purpose:** Define the default energy system for a scalable Minimum Viable Dignified Infrastructure complex.  
**Primary design question:** What energy infrastructure best lowers recurring cost, preserves comfort and safety, survives outages, supports water/food/sanitation/care systems, and remains maintainable without becoming a fragile techno-utopian microgrid?

---

## 1. Core Thesis

The CIaC energy baseline should **not** be total off-grid independence.

Total off-grid energy can be expensive, maintenance-heavy, battery-intensive, legally complex, and fragile under long cloudy periods, winter heating peaks, or equipment failure.

The recommended baseline is a **Critical Load Energy Commons**:

```text
high-efficiency building envelope and appliances
+ grid connection where available
+ solar PV where site-appropriate
+ battery storage sized for critical loads
+ optional generator or fuel backup for long outages
+ demand management
+ critical-load panels
+ thermal resilience
+ energy monitoring
+ maintenance schedules
+ battery/fire safety review
+ graceful degradation during stress
```

The goal is not to prove purity.

The goal is to make energy mostly boring, affordable, low-carbon, resilient, and visible.

---

## 2. Guiding Sentence

> Reduce demand first, electrify wisely, power the critical floor, and let comfort degrade before health or safety degrade.

---

## 3. Strategic Decision

The best default model is:

# Efficient grid-connected electrification with solar + storage for critical loads.

```yaml
energy_strategy:
  demand_first:
    priority: highest
    methods:
      - passive_design
      - insulation_and_air_sealing
      - efficient_windows_where_economic
      - heat_pumps
      - heat_pump_water_heaters
      - LED_lighting
      - efficient_laundry
      - efficient_refrigeration
      - smart_load_scheduling
      - shared_appliances

  primary_supply:
    preferred:
      - grid_connection_where_available
      - rooftop_or_site_solar_PV_where_viable
      - community_solar_or_power_purchase_where_viable

  resilience_supply:
    preferred:
      - battery_storage_for_critical_loads
      - critical_load_panel
      - load_shedding
      - thermal_storage_or_passive_survivability
    optional:
      - generator_for_long_outages
      - renewable_fuel_backup
      - vehicle_to_load_or_vehicle_to_building_after_review

  avoid_as_default:
    - total_off_grid_claims
    - oversized_battery_systems_without_load_reduction
    - hydrogen_as_baseline
    - diesel_dependency_as_primary_design
    - complex_microgrid_without_operator_capacity
    - cryptocurrency_or_high_load_speculative_compute
    - energy_systems_that_require_constant_expert_tuning
```

### Rationale

A dignified village block does not need an ideology of energy independence. It needs a low-burden energy floor that keeps water, food, care, sanitation, refrigeration, communications, and safe temperatures working when the grid fails.

---

## 4. Research Anchors

This module is grounded in the following research and precedent categories.

### 4.1 Residential electricity baseline

The U.S. Energy Information Administration reports that the average U.S. household consumes roughly 10,500 to 10,800 kWh per year, varying substantially by climate and housing type.

**Design implication:** CIaC should not use generic single-family household demand as the default. A clustered village block should benefit from shared walls, shared appliances, shared laundry, shared kitchens, efficient envelopes, and active load management.

### 4.2 Heat pumps

The U.S. Department of Energy states that modern air-source heat pumps can reduce electricity use for heating by up to 75% compared with electric resistance heating.

**Design implication:** Heat pumps should be the default heating/cooling technology where climate, cost, and professional design support them.

### 4.3 Heat pump water heaters

DOE explains that heat pump water heaters move heat rather than generate it directly, making them two to three times more energy efficient than conventional electric resistance water heaters. ENERGY STAR guidance also reports large energy savings for certified heat pump water heaters.

**Design implication:** Domestic hot water should be modeled as a major shared load, and heat pump water heaters or central heat-pump water systems should be preferred where feasible.

### 4.4 Lighting

DOE notes that residential LEDs use at least 75% less energy and last up to 25 times longer than incandescent lighting.

**Design implication:** Lighting should not be treated as a major energy burden if efficient LEDs are used, but it remains a critical load for safety, wayfinding, care, and emergency operation.

### 4.5 Critical loads and resilience

Microgrid and resilience guidance commonly begins by identifying which loads must remain powered when utility power is lost. NREL REopt-style modeling supports optimization for financial performance and resilience, including PV, wind, storage, and backup generation to sustain critical loads.

**Design implication:** The energy module must distinguish normal loads, critical loads, comfort loads, and discretionary loads.

### 4.6 Emergency power planning

FEMA emergency power guidance emphasizes defining what functions need to remain operational during and after a disaster.

**Design implication:** The app should not start by sizing solar panels. It should start by defining which functions must survive an outage.

### 4.7 Battery safety

UL 9540 provides a safety basis for energy storage systems, and NFPA 855 provides installation safety requirements for stationary energy storage systems.

**Design implication:** Batteries belong in the baseline only as certified, professionally installed, fire-safety-reviewed systems.

---

## 5. Recommended Scale

The energy module should support the same first serious population as the housing, food, water, and sanitation modules.

```yaml
population:
  minimum_meaningful_scale: 50
  ideal_first_model: 80
  upper_bound_before_replication: 150
```

### Scale Logic

```text
Below 50:
  energy systems can work, but battery cost and operator capacity may be inefficient.

Around 80:
  shared thermal systems, common-house loads, food storage, water pumps, and battery resilience become meaningful.

Above 150:
  microgrid controls, switching, safety, utility interconnection, and operator burden may become more complex.
```

### Scaling Method

Replicate village-block energy cells rather than building one informal mega-utility.

```yaml
scaling:
  50-100_residents:
    energy_node: 1_primary
    critical_load_panel: required
    battery: preferred
    energy_steward_team: 2-4_people

  100-150_residents:
    energy_node: 1_primary_plus_subpanels
    critical_load_zones: required
    storage_or_backup: required
    professional_microgrid_review: likely

  above_150_residents:
    recommendation: replicate_village_block_or_professionalize_energy_operations
    reason: avoid_informal_utility_without_operator_capacity
```

---

## 6. Default Prototype

```yaml
default_prototype:
  name: critical_load_energy_commons_80
  residents: 80

  primary_configuration:
    grid_connected: true
    solar_PV: site_preferred
    battery_storage: critical_load_sized
    generator: optional_long_outage_backup
    fossil_fuel_primary_design: false

  demand_reduction:
    building_envelope: high_performance
    heating_cooling: heat_pumps
    water_heating: heat_pump_water_heaters_or_central_HPWH
    lighting: LEDs
    cooking: efficient_electric_or_induction_where_feasible
    laundry: efficient_shared_laundry
    refrigeration: efficient_shared_plus_private_minimum
    controls: load_monitoring_and_scheduling

  resilience_targets:
    critical_load_runtime_minimum: 24_hours
    critical_load_runtime_target: 72_hours
    critical_load_runtime_preferred_with_generation: 7_days
    thermal_safety_without_power: modeled
    outage_mode: graceful_degradation

  critical_loads:
    - water_pumps_or_pressure_system
    - potable_water_treatment_if_any
    - refrigeration_and_freezer_critical_storage
    - food_commons_cold_storage
    - care_health_room
    - communications_and_network
    - emergency_lighting
    - sanitation_pumps_or_controls_if_any
    - security_and_access_control_where_used
    - minimum_heating_or_cooling_for_safe_room
    - device_charging
```

---

## 7. Energy Service Levels

The app should model energy as service levels, not a single uptime number.

```yaml
energy_service_levels:
  emergency_floor:
    duration: 24-72_hours
    includes:
      - emergency_lighting
      - communications
      - device_charging
      - critical_refrigeration
      - water_pump_or_gravity_fallback
      - care_room_power
      - minimal_safe_room_heating_or_cooling
    dignity_status: emergency_only

  constrained_dignity:
    duration: 3-7_days_if_generation_available
    includes:
      - critical_loads
      - limited cooking
      - limited laundry only if needed
      - safe common room temperature
      - limited hot water
      - water_and_sanitation_controls
    dignity_status: acceptable_short_term

  normal_dignity:
    includes:
      - heating_and_cooling
      - hot_water
      - laundry
      - common_kitchen
      - refrigeration
      - lighting
      - personal_devices
      - workshop_basic_power
      - normal_communications
    dignity_status: default_target

  abundance_or_discretionary:
    includes:
      - high_power_workshop_tools
      - entertainment
      - EV_charging
      - maker_equipment
      - optional_compute
      - guest_loads
    dignity_status: shed_first_under_stress
```

### Principle

```text
Under energy stress, discretionary loads shed first, comfort loads second, critical health and survival loads last.
```

---

## 8. Load Taxonomy

The app should separate loads by purpose and shed priority.

```yaml
load_taxonomy:
  life_safety_critical:
    examples:
      - medical_devices
      - emergency_lighting
      - care_room_power
      - communications_for_emergency
      - fire_alarm_or_safety_systems
    shed_priority: never_without_life_safety_review

  infrastructure_critical:
    examples:
      - water_pumps
      - water_treatment
      - sanitation_pumps
      - cold_storage
      - network_core
    shed_priority: last

  dignity_critical:
    examples:
      - safe_room_heating_cooling
      - limited_hot_water
      - limited_cooking
      - accessible_lighting
      - device_charging
    shed_priority: late

  normal_comfort:
    examples:
      - full_HVAC
      - normal_laundry
      - normal_hot_water
      - private_appliances
      - entertainment
    shed_priority: middle

  discretionary:
    examples:
      - EV_charging
      - high_power_shop_tools
      - optional_compute
      - decorative_lighting
      - luxury_loads
    shed_priority: first
```

---

## 9. Demand Reduction Strategy

Energy resilience begins by needing less energy.

```yaml
demand_reduction_strategy:
  passive_first:
    required:
      - orientation_considered
      - shading
      - air_sealing
      - insulation
      - ventilation_strategy
      - thermal_zoning
      - summer_overheat_model
      - winter_safe_temperature_model

  efficient_systems:
    required:
      - heat_pump_heating_cooling_where_feasible
      - heat_pump_water_heating_where_feasible
      - LED_lighting
      - efficient_refrigeration
      - efficient_shared_laundry
      - efficient_pumps
      - smart_or_simple_load_scheduling

  shared_infrastructure_advantages:
    - shared_laundry_reduces_duplicate_appliance_load
    - common_kitchen_reduces_duplicate_cooking_load
    - shared_cold_storage_can_be_more_efficient_than_many_private_units
    - shared_walls_reduce_heating_and_cooling_load
    - centralized_monitoring_detects abnormal energy use
```

### Demand Principle

```text
The cheapest battery is the load you removed before sizing the battery.
```

---

## 10. Thermal Resilience

Thermal resilience is as important as electrical resilience.

```yaml
thermal_resilience:
  required:
    - passive_survivability_model
    - winter_minimum_safe_temperature_plan
    - summer_overheat_plan
    - safe_common_room
    - high_need_resident_plan
    - backup_heating_or_cooling_strategy
    - ventilation_during_outage

  preferred:
    - high_performance_envelope
    - operable_windows_where_air_quality_allows
    - shaded_courtyards
    - cool_roof_or_high_albedo_surfaces_where_climate_suitable
    - ceiling_fans
    - thermal_mass_where_appropriate
    - safe_room_with_backup_power
```

### Thermal Principle

```text
An outage should not immediately become a health emergency because the building envelope was weak.
```

---

## 11. Supply Architecture

The app should support several supply profiles.

```yaml
supply_profiles:
  grid_connected_efficiency_only:
    use_case: early_low_capital_baseline
    includes:
      - efficient_buildings
      - critical_load_panel_ready
      - monitoring
    weakness:
      - limited_outage_resilience

  grid_connected_solar:
    use_case: cost_reduction_and_low_carbon_energy
    includes:
      - solar_PV
      - net_metering_or_export_where_available
      - monitoring
    weakness:
      - no_power_during_outage_without_islanding_or_storage

  grid_connected_solar_storage:
    use_case: recommended_default_where_economic
    includes:
      - solar_PV
      - battery_storage
      - critical_load_panel
      - islanding_capability_where_allowed
      - load_shedding
    weakness:
      - battery_cost
      - safety_and_interconnection_complexity

  solar_storage_generator:
    use_case: long_outage_resilience
    includes:
      - solar_PV
      - battery
      - generator_or_fuel_backup
      - fuel_storage_or_contract
    weakness:
      - fuel_dependency
      - emissions
      - maintenance
      - noise

  off_grid:
    use_case: remote_sites_without_grid
    default_status: not_recommended_unless_necessary
    requirements:
      - professional_design
      - large_storage_or_generation
      - seasonal_model
      - backup_fuel_plan
      - operator_capacity
```

---

## 12. Critical Load Panel

A critical load panel is a core design requirement.

```yaml
critical_load_panel:
  required: true
  purpose:
    - separate_survival_loads_from_normal_loads
    - allow_battery_or_generator_backup
    - simplify_outage_mode
    - prevent_accidental_overload
    - make_resilience_visible

  must_include_where_present:
    - water_pump_or_controls
    - water_treatment
    - food_cold_storage
    - care_health_room
    - communications_core
    - emergency_lighting
    - sanitation_controls_or_pumps
    - limited_common_kitchen_power
    - safe_room_HVAC_or_fans
    - device_charging_area

  must_exclude_by_default:
    - EV_charging
    - high_power_workshop_tools
    - full_HVAC_everywhere
    - decorative_loads
    - nonessential_private_appliances
```

### Critical Panel Principle

```text
During an outage, the system should already know what matters.
```

---

## 13. Solar PV Strategy

Solar should be a major default candidate, but not an unquestioned requirement.

```yaml
solar_PV_strategy:
  preferred_where:
    - good_solar_resource
    - roof_or_site_area_available
    - acceptable_shading
    - utility_interconnection_possible
    - maintenance_access_safe
    - financial_model_positive_or_resilience_value_clear

  required_modeling:
    - annual_generation_estimate
    - seasonal_generation_estimate
    - shading_losses
    - roof_or_ground_mount_area
    - inverter_location
    - maintenance_access
    - interconnection_review
    - outage_behavior
    - battery_charging_contribution

  avoid:
    - treating_solar_as_backup_without_storage_or_islanding
    - placing_panels_where_maintenance_is_unsafe
    - oversizing_without_load_or_export_plan
```

### Solar Principle

```text
Solar is not resilience by itself. Solar becomes resilience when paired with islanding, storage, load control, and a critical-load plan.
```

---

## 14. Battery Storage Strategy

Battery storage should be sized for critical loads, not for normal-life fantasy during outages.

```yaml
battery_storage_strategy:
  default_role:
    - critical_load_backup
    - solar_self_consumption
    - demand_charge_management_where_relevant
    - outage_bridge
    - generator_runtime_reduction_if_generator_exists

  sizing_basis:
    - critical_load_kWh_per_day
    - desired_outage_hours
    - solar_recharge_expectation
    - seasonal_low_generation_period
    - battery_depth_of_discharge
    - temperature_derating
    - aging_degradation
    - reserve_margin

  required_safety:
    - UL_9540_listed_system
    - professional_installation
    - NFPA_855_or_local_code_review
    - fire_department_or_authority_review_where_required
    - ventilation_and_clearance_requirements
    - emergency_shutdown
    - signage
    - maintenance_access

  avoid:
    - DIY_battery_banks_as_default
    - uncertified_lithium_storage
    - indoor_unreviewed_storage_near_sleeping_areas
    - hidden_battery_rooms
    - no_fire_response_plan
```

### Battery Principle

```text
Batteries are civic infrastructure only when they are safe, listed, maintainable, and sized against declared critical loads.
```

---

## 15. Generator / Fuel Backup Strategy

Generators should be optional, honest, and treated as a long-outage bridge, not the moral center of the system.

```yaml
generator_strategy:
  default_status: optional_reviewed_backup

  use_when:
    - long_outage_resilience_required
    - battery_only_system_is_too_expensive
    - winter_solar_gap_is_large
    - critical_health_or_water_loads_need_extended_runtime
    - fuel_supply_can_be_stored_or_contractually_guaranteed

  required_controls:
    - outdoor_safe_location
    - carbon_monoxide_safety
    - noise_control
    - fuel_storage_safety
    - maintenance_schedule
    - exercise_schedule
    - transfer_switch_or_approved_interconnection
    - emissions_and_local_rules_review

  preferred_role:
    - recharge_batteries
    - run_critical_loads
    - reduce_total_fuel_use_through_hybrid_dispatch

  avoid:
    - generator_as_primary_daily_energy_source
    - indoor_operation
    - no_fuel_plan
    - no_CO_safety_plan
    - excessive_noise_near_housing
```

### Generator Principle

```text
A generator is a resilience tool, not a substitute for efficiency, solar, storage, or planning.
```

---

## 16. Energy Interfaces With Other Modules

### 16.1 Water Interface

```yaml
water_energy_interface:
  critical_loads:
    - well_pump
    - booster_pump
    - water_treatment
    - monitoring
    - freeze_protection
  required:
    - backup_power_runtime
    - manual_or_gravity_fallback_where_possible
    - water_dashboard_power
```

```text
A water system that cannot move water during an outage is not resilient.
```

### 16.2 Food Interface

```yaml
food_energy_interface:
  critical_loads:
    - cold_storage
    - freezer
    - preservation_equipment_where_needed
    - common_kitchen_minimum_power
    - food_safety_logs
  required:
    - outage_food_plan
    - cold_storage_temperature_monitoring
    - emergency_menu_without_full_power
```

```text
Food resilience fails if cold storage dies silently.
```

### 16.3 Sanitation Interface

```yaml
sanitation_energy_interface:
  critical_loads:
    - sewage_or_effluent_pumps_if_any
    - ventilation
    - greywater_treatment_if_any
    - emergency_lighting
    - cleaning_and_hot_water_minimum
  required:
    - backup_mode
    - outage_sanitation_plan
```

```text
Sanitation systems that depend on pumps or controls must be on the critical-load map.
```

### 16.4 Housing Interface

```yaml
housing_energy_interface:
  required:
    - thermal_envelope_model
    - safe_room_location
    - roof_or_site_solar_area
    - battery_room_or_location
    - service_spine
    - critical_panel_location
    - maintenance_access
```

```text
Energy resilience begins in the building form.
```

### 16.5 Care & Health Interface

```yaml
care_health_energy_interface:
  critical_loads:
    - medical_device_power
    - medication_refrigeration
    - care_room_lighting
    - communications
    - thermal_safe_room
  required:
    - high_need_resident_registry_with_privacy_protection
    - backup_device_charging
    - emergency_power_duration
```

```text
Average energy planning fails medically vulnerable residents.
```

---

## 17. Automation-Favoring Requirements

Automation should make energy visible, scheduled, and easy to operate.

```yaml
automation_requirements:
  energy_dashboard:
    required: true
    purpose:
      - daily_use
      - critical_load_status
      - battery_state_of_charge
      - solar_generation
      - outage_mode
      - warnings
      - cost_tracking

  submetering:
    required: true
    purpose:
      - identify_loads
      - detect_abnormal_use
      - track_pod_demand
      - avoid_blame_without_data

  critical_load_manager:
    required: true
    purpose:
      - shed_discretionary_loads
      - preserve_survival_loads
      - show_runtime_remaining
      - enforce_outage_modes

  maintenance_scheduler:
    required: true
    purpose:
      - filter_cleaning
      - inverter_check
      - battery_health
      - generator_exercise_if_present
      - sensor_check
      - thermal_system_maintenance

  scenario_forecaster:
    required: true
    purpose:
      - outage_duration_model
      - winter_low_solar_model
      - heat_wave_model
      - cold_snap_model
      - fuel_supply_model

  occupant_feedback:
    preferred: true
    purpose:
      - comfort_complaints
      - temperature_issue_detection
      - overcooling_or_overheating
      - dignity_check

  avoid:
    - AI_automatically_controlling_critical_loads_without_human_override
    - black_box_energy_optimization
    - hidden_shed_rules
    - vendor_locked_systems_that_cannot_export_data
```

### Automation Principle

```text
Automate visibility, forecasting, scheduling, and safe load shedding. Do not hide energy decisions from residents.
```

---

## 18. Energy Roles

```yaml
energy_roles:
  energy_steward:
    purpose: overall energy commons coordination
    required_backup: true

  critical_load_steward:
    purpose: maintain critical-load list, outage modes, load-shed rules
    required_backup: true

  solar_storage_steward:
    purpose: monitor PV, inverter, battery, maintenance, alarms
    required_backup: true

  generator_fuel_steward:
    purpose: generator readiness, fuel contracts, exercise schedule, CO safety
    required_backup: true
    required_if_generator_exists: true

  thermal_resilience_steward:
    purpose: safe room, heat wave/cold snap response, comfort monitoring
    required_backup: true

  utility_interconnection_liaison:
    purpose: utility, installer, inspector, permits, tariff changes
    required_backup: true
```

### Role Rule

```text
No critical energy function may depend on one person or one vendor login.
```

---

## 19. Labor and Time Model

Energy systems should reduce resident burden, not create constant troubleshooting.

```yaml
energy_labor_model:
  labor_categories:
    - dashboard_review
    - monthly_system_check
    - filter_maintenance
    - inverter_or_battery_alert_response
    - generator_exercise_if_present
    - fuel_inventory_if_present
    - outage_mode_drill
    - seasonal_thermal_review
    - professional_service_coordination

  required_metrics:
    total_energy_labor_hours_per_month: number
    labor_hours_per_resident_per_month: number
    specialist_dependency_count: integer
    vendor_dependency_score: number
    alarm_frequency_per_month: number
    burnout_risk: low_medium_high
```

### Labor Target

```yaml
labor_targets:
  routine_energy_labor:
    target: 0.1-0.5_hours_per_resident_per_month
    warning_above: 1_hour_per_resident_per_month
    fail_above: 2_hours_per_resident_per_month_unless_specialized_paid_role

  alert_burden:
    warn_if:
      - frequent_false_alarms
      - unclear_alarm_ownership
      - vendor_only_diagnostics
```

### Labor Principle

```text
A resilient energy system has failed if residents must constantly babysit it.
```

---

## 20. Scenario Simulations

The energy module must support stress simulations.

```yaml
energy_scenarios:
  normal_year:
    tests:
      - annual_consumption
      - seasonal_loads
      - solar_generation
      - battery_cycles
      - utility_cost
      - demand_peaks
      - maintenance_burden

  grid_outage_24_hours:
    tests:
      - critical_load_runtime
      - battery_state
      - food_cold_storage
      - water_pump_operation
      - communications
      - safe_room_temperature

  grid_outage_72_hours:
    tests:
      - load_shedding
      - solar_recharge
      - generator_need
      - battery_minimum_state
      - food_water_sanitation_continuity

  long_outage_7_days:
    tests:
      - fuel_dependency
      - comfort_degradation
      - safe_room_capacity
      - high_need_resident_support
      - maintenance_response

  winter_low_solar:
    tests:
      - heating_load
      - battery_recharge
      - generator_runtime
      - frozen_pipe_risk
      - safe_temperature

  summer_heat_wave:
    tests:
      - cooling_load
      - safe_room_capacity
      - overheat_risk
      - peak_demand
      - resident_health_risk

  equipment_failure:
    tests:
      - inverter_failure
      - battery_failure
      - generator_failure
      - heat_pump_failure
      - spare_parts
      - service_response_time

  resident_growth:
    tests:
      - load_increase
      - critical_load_increase
      - panel_capacity
      - solar_area
      - battery_capacity
      - operator_burden
```

---

## 21. Energy Gates

The app should fail or warn based on energy-system viability.

```yaml
energy_gates:
  critical_load_gate:
    fail_if:
      - no_critical_load_list
      - no_critical_load_panel_or_equivalent
      - water_or_food_or_care_loads_missing
      - outage_runtime_unknown
      - no_load_shedding_plan

  dignity_gate:
    fail_if:
      - no_safe_temperature_plan
      - no_high_need_resident_energy_plan
      - no_accessible_emergency_lighting
      - emergency_mode_eliminates_basic_communications

    warn_if:
      - normal_energy_plan_requires_austerity
      - hot_water_or_laundry_reduction_exceeds_dignified_short_term_limit

  resilience_gate:
    fail_if:
      - less_than_24_hours_critical_load_runtime
      - no_backup_for_pumps_or_cold_storage
      - no_outage_mode
      - no_manual_override
      - no_professional_review_for_islanding_or_storage

    warn_if:
      - less_than_72_hours_critical_load_runtime
      - solar_without_storage_presented_as_backup
      - no_long_outage_plan
      - no_generator_or_fuel_plan_in_high_outage_risk_area

  safety_gate:
    fail_if:
      - uncertified_battery_storage
      - no_battery_fire_safety_review
      - generator_has_no_CO_safety_plan
      - electrical_work_not_professionally_reviewed
      - resident_access_to_hazardous_electrical_equipment

  maintenance_gate:
    fail_if:
      - no_energy_steward
      - no_backup_energy_steward
      - no_maintenance_schedule
      - no_professional_service_path
      - critical_system_vendor_login_unavailable

    warn_if:
      - specialized_system_has_no_local_service_provider
      - high_alarm_burden
      - no_spare_parts_strategy

  complexity_gate:
    warn_if:
      - system_has_too_many_energy_sources_for_operator_capacity
      - microgrid_controls_are_black_box
      - hydrogen_or_advanced_storage_added_without_need
      - automation_rules_are_not_legible_to_residents

  cost_gate:
    warn_if:
      - storage_sized_for_full_normal_load_rather_than_critical_loads
      - capital_cost_high_without_life_burden_reduction
      - system_extends_payback_beyond_declared_threshold
      - maintenance_contract_cost_unmodeled
```

---

## 22. App Modeling Boundary

The app should model energy at the level of **load taxonomy, service levels, critical loads, resilience duration, cost, and operations**, not final electrical design.

### The App Should Model

```text
load categories
daily and seasonal demand
critical-load list
critical-load runtime
solar generation estimate
battery capacity estimate
grid dependence
outage modes
load shedding
thermal resilience
safe room capacity
generator fuel duration
maintenance schedules
battery/fire safety review requirements
utility interconnection flags
professional review requirements
```

### The App Should Not Claim to Solve by Default

```text
final electrical engineering
wire sizing
breaker sizing
load calculations for permit
NEC compliance
battery placement approval
utility interconnection approval
generator installation approval
fire code compliance
HVAC design
solar structural mounting design
arc flash studies
commercial microgrid controller design
```

### Principle

```text
The app should identify what must be true for energy dignity and resilience.
Qualified professionals and local authorities must validate electrical, fire, utility, structural, and mechanical implementation.
```

---

## 23. Required Data Model

```yaml
EnergyCommons:
  id: string
  population_served: integer

  demand:
    annual_kWh_estimate: number
    daily_kWh_average: number
    peak_kW_estimate: number
    critical_load_kWh_per_day: number
    critical_load_peak_kW: number
    heating_cooling_kWh_annual: number
    water_heating_kWh_annual: number
    food_cold_storage_kWh_daily: number
    water_pump_kWh_daily: number

  supply:
    grid_connected: boolean
    solar_PV_kW: number
    solar_annual_kWh_estimate: number
    battery_kWh_usable: number
    battery_kW_peak: number
    generator_kW: number
    generator_fuel_type: string
    generator_fuel_hours_at_critical_load: number
    community_solar_or_PPA: boolean

  resilience:
    critical_load_runtime_hours_no_sun: number
    critical_load_runtime_hours_with_solar: number
    outage_mode_defined: boolean
    load_shedding_plan: boolean
    safe_room_powered: boolean
    high_need_residents_modeled: boolean
    manual_override: boolean

  efficiency:
    heat_pumps_enabled: boolean
    heat_pump_water_heating_enabled: boolean
    LED_lighting: boolean
    efficient_laundry: boolean
    efficient_refrigeration: boolean
    envelope_performance_status: unknown | provisional | modeled | reviewed

  safety:
    battery_certification_status: unknown | UL_9540 | equivalent | failed
    battery_fire_review: boolean
    generator_CO_safety_plan: boolean
    professional_electrical_review: boolean
    utility_interconnection_review: boolean
    emergency_shutdown: boolean

  operations:
    energy_dashboard: boolean
    submetering: boolean
    critical_load_manager: boolean
    maintenance_schedule: boolean
    scenario_forecaster: boolean
    energy_steward: string
    backup_energy_steward: string

  outputs:
    normal_energy_status: pass | warn | fail
    critical_load_status: pass | warn | fail
    energy_cost_per_resident_month: number
    outage_resilience_score: number
    thermal_resilience_score: number
    maintenance_burden_score: number
    complexity_score: number
    life_burden_reduction_score: number
```

---

## 24. Required App Outputs

```yaml
required_outputs:
  - energy_system_summary
  - load_taxonomy_report
  - critical_load_report
  - normal_energy_demand_report
  - energy_cost_report
  - solar_generation_report
  - battery_storage_report
  - outage_runtime_report
  - thermal_resilience_report
  - generator_fuel_report_if_present
  - safety_review_requirements
  - maintenance_schedule
  - scenario_failure_report
  - role_backup_report
  - professional_review_requirements
  - visualization_bundle_metadata
```

---

## 25. Visualization Requirements

The energy module should export enough data for a virtual world or dashboard to show how energy works.

```yaml
visualization_requirements:
  spatial_objects:
    - solar_arrays
    - battery_storage_location
    - inverter_location
    - critical_load_panel
    - utility_interconnection
    - generator_location_if_present
    - safe_room
    - water_pump_load
    - cold_storage_load
    - care_room_load
    - energy_dashboard

  overlays:
    - normal_loads
    - critical_loads
    - discretionary_loads
    - solar_generation
    - battery_state_of_charge
    - outage_runtime_remaining
    - load_shed_status
    - thermal_safe_zones
    - maintenance_due
    - safety_warnings

  scenario_playback:
    - 24_hour_outage
    - 72_hour_outage
    - 7_day_outage
    - winter_low_solar
    - summer_heat_wave
    - battery_failure
    - generator_failure
    - resident_growth
```

---

## 26. Best Default Requirements Summary

```yaml
MinimumViableEnergyCommons:
  population:
    first_serious_model: 80
    valid_range: 50-150

  philosophy:
    demand_reduction_first: true
    grid_connected_default: true
    total_off_grid_required: false
    critical_load_resilience: required
    full_normal_life_backup: not_required
    visible_energy_status: required

  efficiency:
    high_performance_envelope: required
    heat_pumps: preferred
    heat_pump_water_heaters: preferred
    LED_lighting: required
    efficient_shared_laundry: required
    efficient_refrigeration: required
    load_scheduling: required

  supply:
    grid_connection: preferred
    solar_PV: preferred_where_site_viable
    battery_storage: preferred_for_critical_loads
    generator: optional_for_long_outages
    fossil_primary: false

  targets:
    critical_load_runtime_minimum: 24_hours
    critical_load_runtime_target: 72_hours
    critical_load_runtime_preferred_with_generation: 7_days
    normal_energy_use: modeled_by_site_and_envelope
    discretionary_load_shed_first: true

  automation:
    energy_dashboard: required
    submetering: required
    critical_load_manager: required
    maintenance_scheduler: required
    scenario_forecaster: required
    occupant_feedback: preferred

  gates:
    critical_load_gate: required
    dignity_gate: required
    resilience_gate: required
    safety_gate: required
    maintenance_gate: required
    complexity_gate: required
    cost_gate: required
```

---

## 27. Design Maxims

```text
Do not start by sizing solar panels. Start by defining what must stay alive.

Do not call solar a backup unless islanding, storage, and load control are designed.

Do not size batteries for fantasy full-normal operation during outages.

Do not make residents choose between safety and comfort because the building envelope is weak.

Do not add energy technology that nobody can maintain.

Do not use uncertified batteries or informal electrical work.

Do not hide load-shedding rules.

Do not let one vendor account become the energy commons.

Do not make generator fuel the foundation of the system.

Reduce demand before adding supply.

Electrify where it reduces cost, emissions, maintenance, and fragility.

Power water, food, sanitation, care, communications, and safe temperature first.

Use shared infrastructure to reduce duplicated appliance burden.

Use automation to make energy legible.

Use graceful degradation so an outage becomes an inconvenience before it becomes a crisis.
```

---

## 28. Open Questions for Iteration

```text
1. Should the default prototype assume grid connection, or support grid-connected and off-grid profiles?
2. What critical-load runtime should be treated as morally acceptable: 24 hours, 72 hours, or 7 days?
3. Should a generator be included in v0 as optional, or deferred to resilience profiles?
4. Should EV charging be modeled in v0 or treated as discretionary future load?
5. Should the safe room be one common-house space or distributed safe rooms by pod?
6. What is the acceptable monthly energy-cost target per resident?
7. Should the model include embodied energy/carbon of batteries and solar panels?
8. Should the app integrate with NREL REopt or similar tools later, or keep an internal simplified estimator?
9. How should medically necessary electrical loads be represented without exposing private health data?
10. Should the system prioritize lowest cost, lowest carbon, or highest resilience when these conflict?
```

---

## 29. Source Notes

The research basis for this draft includes:

- U.S. Energy Information Administration household electricity-use data.
- U.S. Department of Energy Energy Saver resources on heat pumps, heat pump water heaters, and LED lighting.
- ENERGY STAR resources on heat pump water heaters and appliance efficiency.
- NREL microgrid and REopt-style resilience guidance.
- FEMA emergency power planning guidance for critical facilities.
- UL 9540 energy storage system safety resources.
- UL 9540A battery energy storage fire-safety testing resources.
- NFPA 855 stationary energy storage installation safety requirements.
