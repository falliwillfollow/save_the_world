# CIaC Maintenance & Repair Module: Maintainable Commons Spine

**Module ID:** `maintenance_repair.maintainable_commons_spine.v0_1`  
**Status:** Draft requirement module  
**Purpose:** Define the default maintenance and repair system for a scalable Minimum Viable Dignified Infrastructure complex.  
**Primary design question:** What maintenance infrastructure best keeps the civic floor working, reduces surprise failures, distributes labor fairly, preserves safety, and avoids turning residents into unpaid facility staff or heroic DIY generalists?

---

## 1. Core Thesis

The CIaC maintenance baseline should **not** be heroic DIY.

A resilient community cannot depend on one handy founder, one charismatic mechanic, one spreadsheet, or residents improvising repairs on safety-critical systems.

The recommended baseline is a **Maintainable Commons Spine**:

```text
asset registry
+ criticality ranking
+ preventive maintenance schedules
+ condition monitoring where useful
+ work orders
+ spare parts inventory
+ repair documentation
+ role backup
+ professional handoff thresholds
+ tool library
+ training paths
+ safety procedures
+ maintenance budget and reserve
+ failure reporting
+ visible backlog
+ design-for-maintainability gates
```

The goal is not to eliminate professional trades.

The goal is to make the commons easy to inspect, easy to repair, hard to neglect, and honest about what residents should not touch.

---

## 2. Guiding Sentence

> A civic floor is only real if it can be maintained by ordinary people, supported by professionals, without burning out either group.

---

## 3. Strategic Decision

The best default model is:

# A CMMS-lite civic maintenance system with reliability-centered logic for critical assets.

```yaml
maintenance_strategy:
  core_system:
    - asset_registry
    - QR_or_tagged_assets
    - recurring_work_orders
    - inspection_checklists
    - spare_parts_thresholds
    - maintenance_backlog
    - safety_controls
    - professional_handoff_rules
    - labor_tracking
    - budget_reserve_tracking
    - failure_mode_log

  maintenance_modes:
    reactive:
      use_for:
        - low_criticality_items
        - low_cost_items
        - non_safety_failures
    preventive:
      use_for:
        - predictable_wear_items
        - filters
        - pumps
        - valves
        - HVAC
        - batteries
        - roof_and_envelope_inspections
    predictive_or_condition_based:
      use_for:
        - high_value_or_high_criticality_assets
        - pumps
        - batteries
        - cold_storage
        - water_systems
        - energy_systems
    reliability_centered:
      use_for:
        - safety_critical_assets
        - water
        - sanitation
        - energy_storage
        - critical_care_power
        - structural_envelope
        - food_cold_storage

  avoid_as_default:
    - no_asset_registry
    - maintenance_by_memory
    - hidden_backlog
    - single_person_dependency
    - residents_doing_licensed_work
    - false_precision_sensor_stacks
    - predictive_AI_without_maintenance_data
    - repair_culture_without_safety_boundaries
```

### Rationale

Maintenance is where the project either becomes real or collapses.

The civic floor cannot be judged by how it looks when new. It must be judged by how it behaves after five years of use, bad weather, resident turnover, equipment wear, missed tasks, supply shortages, conflict, and ordinary forgetfulness.

---

## 4. Research Anchors

This module is grounded in the following research and precedent categories.

### 4.1 Operations and maintenance best practices

The U.S. Department of Energy Federal Energy Management Program has long published O&M best practices for operational efficiency, energy and water efficiency, cost reduction, and maintenance management.

**Design implication:** Maintenance should be treated as a formal program, not an afterthought.

### 4.2 Strategic O&M planning

The Whole Building Design Guide describes an O&M plan as a living tool for reducing lifecycle O&M costs, extending system lifespans, reducing issue response times, and communicating maintenance strategy.

**Design implication:** The app should generate a living O&M plan, not static checklists.

### 4.3 Asset management for water and wastewater

EPA describes asset management for water and wastewater systems as a process that helps ensure planned maintenance occurs and assets can be repaired, replaced, or upgraded on time with money available.

**Design implication:** CIaC must model maintenance reserve funds, replacement schedules, and lifecycle planning, especially for water and wastewater assets.

### 4.4 Maintenance approach taxonomy

DOE/FEMP resources distinguish reactive/corrective maintenance, preventive maintenance, predictive maintenance, and reliability-centered maintenance.

**Design implication:** The app should not use one maintenance strategy for everything. It should select the simplest appropriate mode based on criticality, failure consequence, cost, and detectability.

### 4.5 Reliability-centered maintenance

NASA describes reliability-centered maintenance as a process to determine the most effective maintenance approach, using data and system performance to reduce failure probability and improve design and maintenance.

**Design implication:** Critical systems should use failure-mode thinking, not calendar-only checklists.

### 4.6 Hazardous energy control

OSHA lockout/tagout rules cover servicing and maintenance where unexpected energization or release of stored energy could cause injury, and establish minimum requirements for controlling hazardous energy.

**Design implication:** The module must draw a hard safety boundary around electrical, mechanical, pressure, thermal, stored-energy, and hazardous systems.

### 4.7 Design for maintainability

WBDG emphasizes involving O&M staff in design phases, anticipating what it will take to maintain and operate facilities, and addressing operating budgets early.

**Design implication:** Maintainability should be a design gate before a pattern is approved.

### 4.8 Moisture, mold, and building health

EPA and WBDG mold/moisture guidance emphasize identifying moisture sources, correcting them, using PPE where needed, and protecting occupants and workers.

**Design implication:** Building envelope, roof, plumbing leak detection, humidity, and mold response belong in core maintenance, not cosmetic building care.

---

## 5. Recommended Scale

The maintenance and repair module should support the same first serious population as the housing, food, water, sanitation, energy, and care modules.

```yaml
population:
  minimum_meaningful_scale: 50
  ideal_first_model: 80
  upper_bound_before_replication: 150
```

### Scale Logic

```text
Below 50:
  maintenance may depend too heavily on a few skilled residents.

Around 80:
  maintenance teams, role backup, tool library, spares inventory, professional service relationships, and recurring work orders become realistic.

Above 150:
  maintenance may require formal staffing, contractor frameworks, and more rigorous facilities management.
```

### Scaling Method

Maintenance should scale by village block cells, with federation-level shared expertise.

```yaml
scaling:
  50-100_residents:
    maintenance_node: 1
    maintenance_team: 4-8_trained_residents
    professional_service_relationships: required

  100-150_residents:
    maintenance_node: 1_plus_specialized_subroles
    maintenance_team: 8-12_people
    paid_part_time_facilities_role: preferred

  above_150_residents:
    recommendation: replicate_village_block_or_formalize_facilities_department
```

---

## 6. Default Prototype

```yaml
default_prototype:
  name: maintainable_commons_spine_80
  residents: 80

  core_facilities:
    - maintenance_room
    - tool_library
    - spare_parts_storage
    - repair_bench
    - dirty_work_area
    - PPE_station
    - lockable_hazardous_tools_storage
    - documentation_station
    - maintenance_dashboard
    - receiving_and_staging_area
    - contractor_access_point

  core_systems:
    - asset_registry
    - QR_or_tag_system
    - work_order_system
    - preventive_maintenance_calendar
    - critical_asset_watchlist
    - spare_parts_min_max_inventory
    - professional_handoff_matrix
    - safety_procedure_library
    - incident_and_failure_log
    - maintenance_budget_and_reserve
    - training_and_certification_tracker

  targets:
    routine_maintenance_labor_per_resident: 1-3_hours_per_month
    warning_above: 5_hours_per_resident_per_month
    fail_above: 8_hours_per_resident_per_month_unless_staffed_or_paid
    emergency_response_coverage: always_assigned
    critical_role_backup: required
    critical_asset_documentation: 100_percent
```

---

## 7. Maintenance Service Levels

The app should model maintenance as service levels.

```yaml
maintenance_service_levels:
  emergency_only:
    includes:
      - respond_to_active_failures
      - isolate_hazards
      - call_professionals
      - temporary_workarounds
    dignity_status: unacceptable_as_default

  basic_maintenance:
    includes:
      - asset_registry
      - recurring_checklists
      - basic_work_orders
      - safety_boundaries
      - spare_parts_for_common_failures
      - contractor_contacts
    dignity_status: minimum

  resilient_maintenance:
    includes:
      - criticality_ranking
      - preventive_and_condition_based_tasks
      - role_backup
      - failure_mode_tracking
      - budget_reserves
      - training_paths
      - maintenance_dashboard
      - design_feedback_loop
    dignity_status: default_target

  professionalized_facilities:
    includes:
      - paid_facilities_staff
      - CMMS
      - contracted_service_levels
      - commissioning_retrocommissioning
      - formal_asset_management_plan
    dignity_status: required_at_larger_scale_or_high_complexity
```

### Principle

```text
The project fails if the community can only keep working by waiting for things to break.
```

---

## 8. Asset Registry

The asset registry is the core of the maintenance module.

Every maintainable object should be registered, tagged, and connected to documentation.

```yaml
asset_registry:
  required_fields:
    - asset_id
    - name
    - module
    - location
    - owner_or_steward
    - backup_steward
    - criticality_class
    - installation_date
    - expected_life
    - warranty_info
    - vendor_or_manufacturer
    - manual_or_documentation_link
    - maintenance_interval
    - inspection_checklist
    - spare_parts
    - professional_service_required
    - safety_notes
    - failure_modes
    - last_service_date
    - next_service_due
    - replacement_reserve_requirement

  tagging:
    required: true
    preferred:
      - QR_code
      - NFC_tag_where_useful
      - visible_asset_label
```

### Asset Registry Principle

```text
If the community cannot name, locate, inspect, and replace an asset, it does not truly own it.
```

---

## 9. Criticality Classes

The app should rank assets by failure consequence.

```yaml
criticality_classes:
  class_A_life_safety_or_civic_floor:
    examples:
      - potable_water_pump
      - water_treatment
      - wastewater_system
      - critical_battery_storage
      - food_cold_storage
      - care_room_power
      - fire_safety_systems
      - structural_envelope_waterproofing
    requirements:
      - backup_steward
      - professional_review
      - preventive_or_RCM_plan
      - spare_or_service_plan
      - failure_response_plan
      - dashboard_visibility

  class_B_major_operational:
    examples:
      - common_kitchen_equipment
      - laundry
      - greenhouse_irrigation
      - HVAC_heat_pumps
      - access_control
      - network_core
    requirements:
      - preventive_maintenance
      - spare_parts_or_service_contract
      - role_backup
      - work_order_tracking

  class_C_comfort_and_convenience:
    examples:
      - furniture
      - interior_finishes
      - noncritical_lighting
      - garden_tools
      - minor_appliances
    requirements:
      - inspection_or_repair_queue
      - replace_or_repair_decision

  class_D_discretionary:
    examples:
      - decorative_features
      - optional_maker_equipment
      - entertainment_equipment
    requirements:
      - reactive_maintenance_allowed
      - no_critical_budget_priority
```

### Criticality Principle

```text
Do not maintain everything equally. Maintain what protects the floor first.
```

---

## 10. Maintenance Modes

The app should select maintenance mode by asset class, failure consequence, and available data.

```yaml
maintenance_modes:
  reactive_corrective:
    description: fix_when_broken
    use_for:
      - low_cost_noncritical_assets
      - assets_with_low_failure_consequence
      - items_where_preventive_work_costs_more_than_failure
    avoid_for:
      - potable_water
      - sanitation
      - critical_energy
      - food_cold_storage
      - care_health_support

  preventive:
    description: time_or_usage_based_tasks
    use_for:
      - filters
      - belts
      - batteries_inspections
      - pumps
      - valves
      - roof_gutter_checks
      - HVAC_service
      - fire_safety_equipment
      - water_testing_schedules

  predictive_condition_based:
    description: maintenance_based_on_measured_condition
    use_for:
      - batteries
      - pumps
      - cold_storage_temperature
      - leak_detection
      - energy_inverters
      - water_tank_levels
      - HVAC_performance
    caution:
      - requires_reliable_sensors
      - requires_data_review
      - should_not_replace_human_inspection

  reliability_centered:
    description: strategy_based_on_failure_modes_and_consequence
    use_for:
      - class_A_assets
      - high_cost_high_consequence_assets
      - systems_with_multiple_failure_modes
    requires:
      - failure_modes
      - detectability
      - consequence_rating
      - maintenance_task_justification
      - periodic_review
```

---

## 11. Work Order System

The app should create a simple work order system that can scale.

```yaml
work_order_system:
  required_fields:
    - work_order_id
    - title
    - asset_id
    - location
    - module
    - requestor
    - priority
    - safety_risk
    - description
    - photos_or_notes
    - assigned_role
    - backup_assignee
    - due_date
    - status
    - parts_needed
    - professional_required
    - completion_notes
    - verification
    - labor_hours
    - cost
    - recurrence_link_if_any

  priorities:
    P0_emergency:
      response: immediate
      examples:
        - active_leak_affecting_structure
        - sewage_backup
        - electrical_hazard
        - no_potable_water
        - critical_cold_storage_failure
        - medical_power_failure

    P1_critical:
      response: same_day
      examples:
        - pump_warning
        - battery_alarm
        - roof_leak
        - heat_failure_in_safe_room
        - food_storage_temperature_risk

    P2_important:
      response: 1-7_days
      examples:
        - appliance_issue
        - minor_plumbing_leak
        - recurring_sensor_warning
        - door_lock_problem

    P3_routine:
      response: scheduled
      examples:
        - filter_change
        - inspection
        - lubrication
        - inventory_restock

    P4_improvement:
      response: backlog_review
      examples:
        - comfort_upgrade
        - cosmetic_repair
        - optional_optimization
```

### Work Order Principle

```text
A problem that lives only in someone's memory is not yet being maintained.
```

---

## 12. Professional Handoff Matrix

The app must know when residents should stop and call professionals.

```yaml
professional_handoff_matrix:
  resident_allowed:
    examples:
      - visual_inspections
      - filter_changes_where_safe
      - cleaning
      - basic_tool_repair
      - battery_status_review_without_opening_equipment
      - tightening_noncritical_fixtures
      - garden_tool_maintenance
    requirements:
      - training
      - checklist
      - PPE_where_needed

  trained_steward_allowed:
    examples:
      - pump_precheck_without_electrical_work
      - valve_exercise
      - water_testing_sample_collection
      - nonhazardous_minor_repairs
      - appliance_basic_maintenance
      - cold_storage_temperature_check
    requirements:
      - documented_training
      - safety_checklist
      - backup_person

  licensed_or_qualified_professional_required:
    examples:
      - electrical_panel_work
      - battery_storage_service
      - generator_installation_or_transfer_switch
      - potable_water_treatment_design
      - well_repair
      - septic_or_wastewater_system_work
      - structural_repair
      - roof_structural_work
      - fire_safety_systems
      - gas_or_combustion_equipment
      - refrigerant_handling
      - mold_remediation_beyond_minor_scope
      - hazardous_materials
      - medical_equipment
    requirements:
      - contractor_contact
      - permit_or_authority_review_where_required
      - completion_documentation
```

### Handoff Principle

```text
Repair culture is not permission to exceed competence.
```

---

## 13. Tool Library and Repair Space

The tool library should reduce private duplication and make repair easier.

```yaml
tool_library:
  required:
    - inventory
    - checkout_system
    - maintenance_schedule_for_tools
    - safety_training_for_hazardous_tools
    - lockable_storage
    - PPE
    - consumables_inventory
    - broken_tool_quarantine
    - repair_or_replace_decision_log

  tool_classes:
    class_1_general:
      examples:
        - hand_tools
        - measuring_tools
        - ladders_low_risk
        - cleaning_tools
      access: general_after_orientation

    class_2_trained_use:
      examples:
        - power_tools
        - pressure_washer
        - larger_ladders
        - garden_machinery
      access: training_required

    class_3_restricted:
      examples:
        - chainsaw
        - welding_equipment
        - high_voltage_test_tools
        - confined_space_equipment
      access: qualified_or_professional_only

  repair_space:
    required:
      - workbench
      - lighting
      - ventilation
      - dust_control_where_needed
      - first_aid_kit
      - fire_extinguisher
      - PPE_station
      - material_scrap_sorting
      - hazardous_material_controls
```

### Tool Principle

```text
Shared tools reduce cost only when they are easy to find, safe to use, and actually maintained.
```

---

## 14. Spare Parts and Consumables

A resilient maintenance system needs the right parts before failure.

```yaml
spare_parts_inventory:
  required:
    - min_max_levels
    - supplier_links
    - reorder_points
    - shelf_life
    - storage_location
    - compatible_asset_ids
    - criticality
    - substitute_options
    - emergency_stock_flag

  priority_parts:
    water:
      - filters
      - seals
      - test_kits
      - valves
      - pump_parts_where_appropriate

    food:
      - cold_storage_sensors
      - gaskets
      - thermometers
      - cleaning_supplies
      - preservation_consumables

    sanitation:
      - PPE
      - cleaning_supplies
      - gloves
      - bins
      - pump_parts_where_appropriate

    energy:
      - fuses_or_approved_parts
      - monitoring_sensors
      - air_filters
      - generator_consumables_if_present
      - battery_system_service_contacts

    housing:
      - weatherstripping
      - sealants
      - fasteners
      - filters
      - door_hardware
      - leak_detection_sensors

    care:
      - first_aid_supplies
      - PPE
      - batteries
      - cold_packs
      - emergency_lighting
```

### Spare Parts Principle

```text
A $20 missing part should not disable a survival-critical system.
```

---

## 15. Design for Maintainability

The app should reject patterns that cannot be maintained.

```yaml
design_for_maintainability:
  required:
    - safe_access_to_service_points
    - labeled_shutoffs
    - accessible_filters
    - visible_leak_paths
    - inspectable_roof_and_envelope
    - equipment_clearances
    - replaceable_components
    - standard_fasteners_where_possible
    - documentation_before_approval
    - professional_service_access
    - no_hidden_single_point_failures

  warn_if:
    - equipment_requires_destructive_access
    - proprietary_parts_have_long_lead_times
    - no_local_service_provider
    - maintenance_requires_special_tools_without_plan
    - service_points_are_above_safe_reach
    - pipes_or_wires_are_impossible_to_trace
    - system_is_beautiful_but_uninspectable
```

### Maintainability Principle

```text
A beautiful system that cannot be inspected is a future crisis.
```

---

## 16. Documentation Standard

Every system should have resident-facing and professional-facing documentation.

```yaml
documentation_standard:
  resident_facing:
    - what_this_is
    - what_it_does
    - warning_signs
    - what_residents_can_do
    - what_residents_must_not_do
    - who_to_contact
    - emergency_shutdown_or_isolation_where_safe

  steward_facing:
    - inspection_checklist
    - preventive_tasks
    - maintenance_interval
    - parts_list
    - troubleshooting_flow
    - escalation_threshold
    - safety_requirements
    - labor_time_estimate

  professional_facing:
    - installation_records
    - permits_or_reviews
    - manufacturer_manuals
    - schematics_or_as_builts
    - service_history
    - commissioning_report
    - warranty_info
```

### Documentation Principle

```text
The settlement should survive resident turnover.
```

---

## 17. Safety System

Maintenance safety must be explicit.

```yaml
maintenance_safety:
  required:
    - PPE_matrix
    - lockout_tagout_or_hazardous_energy_protocol_where_applicable
    - ladder_and_work_at_height_rules
    - confined_space_warning
    - electrical_boundary_rules
    - battery_storage_boundary_rules
    - chemical_storage_rules
    - tool_safety_training
    - incident_reporting
    - stop_work_authority
    - first_aid_station
    - emergency_contacts

  stop_work_triggers:
    - electrical_hazard
    - sewage_or_human_waste_exposure
    - structural_instability
    - mold_beyond_minor_scope
    - unknown_chemical
    - battery_alarm_or_damage
    - gas_or_combustion_risk
    - working_at_height_without_controls
    - no_training_for_task
    - resident_feels_unsafe

  stop_work_authority:
    rule: any_resident_or_worker_may_pause_work_for_safety_concerns
```

### Safety Principle

```text
Maintenance that injures people has failed even if it fixes the asset.
```

---

## 18. Moisture, Mold, and Envelope Maintenance

Building health is health infrastructure.

```yaml
moisture_mold_envelope:
  required:
    - roof_inspections
    - gutter_and_drainage_inspections
    - foundation_drainage_checks
    - plumbing_leak_response
    - humidity_monitoring_where_needed
    - bathroom_and_kitchen_ventilation_checks
    - window_and_door_seal_checks
    - water_intrusion_log
    - mold_response_threshold
    - professional_remediation_threshold

  response_targets:
    active_leak:
      response: immediate_isolation_and_repair_plan
    wet_material:
      response: dry_quickly_and_document
    visible_mold:
      response: identify_moisture_source_first
    recurring_moisture:
      response: design_review_not_repeated_cleanup
```

### Moisture Principle

```text
The cheapest mold remediation is preventing water from being trapped where no one can see it.
```

---

## 19. Interfaces With Other Modules

### 19.1 Housing Interface

```yaml
housing_maintenance_interface:
  required:
    - envelope_inspection
    - roof_access
    - drainage_maintenance
    - door_window_hardware
    - acoustic_privacy_preservation
    - accessibility_feature_maintenance
    - common_space_cleanliness
    - repair_queue_for_units
```

```text
Housing dignity decays without maintenance.
```

### 19.2 Food Interface

```yaml
food_maintenance_interface:
  required:
    - cold_storage_maintenance
    - kitchen_equipment_service
    - thermometer_calibration
    - preservation_equipment
    - pest_control
    - garden_tool_maintenance
    - wash_pack_maintenance
```

```text
Food resilience depends on boring equipment staying boring.
```

### 19.3 Water Interface

```yaml
water_maintenance_interface:
  required:
    - testing_schedule
    - pump_maintenance
    - valve_exercise
    - leak_detection
    - cistern_cleaning
    - filter_changes
    - sampling_points
    - delivered_water_fallback
```

```text
Water safety is a maintenance program, not a one-time installation.
```

### 19.4 Sanitation Interface

```yaml
sanitation_maintenance_interface:
  required:
    - toilet_and_bathroom_maintenance
    - wastewater_service_schedule
    - greywater_checklists_where_enabled
    - compost_area_maintenance
    - waste_station_cleaning
    - hazardous_waste_storage
```

```text
Sanitation neglect becomes public health risk quickly.
```

### 19.5 Energy Interface

```yaml
energy_maintenance_interface:
  required:
    - critical_load_panel_documentation
    - battery_monitoring
    - inverter_service
    - generator_exercise_if_present
    - HVAC_filters
    - heat_pump_service
    - energy_dashboard
```

```text
Energy resilience requires maintenance before the outage.
```

### 19.6 Care & Health Interface

```yaml
care_maintenance_interface:
  required:
    - care_room_readiness
    - AED_battery_pads_if_present
    - medication_refrigeration_monitoring
    - emergency_lighting
    - mobility_device_storage
    - accessible_route_repairs
    - PPE_stock
```

```text
Care infrastructure must be ready before someone needs care.
```

### 19.7 Governance Interface

```yaml
governance_maintenance_interface:
  required:
    - maintenance_budget_approval
    - role_rotation
    - dispute_process_for_private_unit_repairs
    - escalation_rules
    - transparency_of_backlog
    - anti_blame_culture
    - contractor_selection_policy
```

```text
Maintenance fails when nobody has authority, money, or responsibility to act.
```

---

## 20. Labor and Time Model

The maintenance module must count labor honestly and distinguish voluntary tinkering from required civic upkeep.

```yaml
maintenance_labor_model:
  labor_categories:
    - inspections
    - preventive_tasks
    - corrective_repairs
    - emergency_response
    - cleaning_of_maintenance_areas
    - tool_library_management
    - parts_inventory
    - contractor_coordination
    - documentation
    - training
    - budget_review
    - failure_analysis
    - seasonal_preparation

  required_metrics:
    total_maintenance_labor_hours_per_month: number
    labor_hours_per_resident_per_month: number
    critical_asset_labor_hours: number
    unpleasant_or_dirty_labor_hours: number
    skilled_labor_dependency_hours: number
    contractor_hours: number
    volunteer_hours: number
    paid_hours: number
    backlog_hours: number
    emergency_hours: number
    labor_concentration_score: number
    burnout_risk: low_medium_high
```

### Labor Targets

```yaml
labor_targets:
  routine_maintenance_labor_per_resident:
    target: 1-3_hours_per_month
    warning_above: 5_hours_per_month
    fail_above: 8_hours_per_month_unless_staffed_or_paid

  emergency_labor:
    target: rare
    warning_if:
      - emergency_hours_exceed_20_percent_of_total_maintenance_hours
      - same_people_handle_most_emergencies

  backlog:
    warning_if:
      - critical_backlog_exists_longer_than_7_days
      - P2_backlog_grows_for_3_consecutive_months
      - total_backlog_exceeds_capacity_next_30_days
```

### Labor Principle

```text
A low-cost commons is not low-cost if it quietly converts residents into unpaid facilities staff.
```

---

## 21. Maintenance Budget and Reserve

Maintenance must have money attached.

```yaml
maintenance_budget_reserve:
  required:
    - annual_maintenance_budget
    - replacement_reserve
    - emergency_repair_reserve
    - critical_spares_budget
    - professional_service_budget
    - insurance_interface
    - reserve_review_schedule

  budget_categories:
    - routine_consumables
    - preventive_service
    - professional_contractors
    - spare_parts
    - tool_replacement
    - emergency_repairs
    - lifecycle_replacements
    - training
    - safety_equipment

  reserve_rules:
    fail_if:
      - no_replacement_reserve_for_class_A_assets
      - no_emergency_repair_reserve
      - professional_service_costs_unmodeled
      - maintenance_budget_depends_on_donations_only
```

### Budget Principle

```text
A system without a maintenance reserve is borrowing from its future residents.
```

---

## 22. Automation-Favoring Requirements

Automation should remove memory burden, reveal backlog, and protect the floor.

```yaml
automation_requirements:
  asset_registry:
    required: true
    purpose:
      - know_what_exists
      - connect_assets_to_tasks
      - store_documentation
      - track_lifecycle

  work_order_system:
    required: true
    purpose:
      - capture_requests
      - assign_tasks
      - prioritize
      - track_completion
      - record_labor_and_cost

  preventive_scheduler:
    required: true
    purpose:
      - recurring_tasks
      - seasonal_tasks
      - test_dates
      - filter_changes
      - inspections

  critical_asset_dashboard:
    required: true
    purpose:
      - show_class_A_status
      - show_open_P0_P1_work
      - show_next_due_tasks
      - show unresolved risks

  spare_parts_inventory:
    required: true
    purpose:
      - min_max_levels
      - reorder_points
      - supplier_links
      - emergency_stock

  professional_handoff_engine:
    required: true
    purpose:
      - flag_licensed_work
      - block_unsafe_task_assignment
      - attach contractor contacts
      - document permits_or_reviews

  failure_mode_logger:
    required: true
    purpose:
      - record_failures
      - identify_repeat_issues
      - support_design_feedback
      - update_maintenance_strategy

  mobile_QR_interface:
    preferred: true
    purpose:
      - scan_asset
      - view_checklist
      - submit_issue
      - attach_photo
      - see_contact

  condition_monitoring:
    preferred_for_class_A_assets: true
    purpose:
      - leak_alerts
      - temperature_alerts
      - tank_levels
      - battery_status
      - pump_runtime
      - humidity

  avoid:
    - AI_assigning_hazardous_tasks_without_safety_gate
    - predictive_AI_without_data
    - hidden_backlog
    - vendor_locked_CMMS_with_no_export
    - automation_that_residents_cannot_understand
```

### Automation Principle

```text
Automate memory, scheduling, evidence, and escalation. Do not automate away responsibility.
```

---

## 23. Maintenance Roles

```yaml
maintenance_roles:
  maintenance_steward:
    purpose: overall maintenance coordination and backlog ownership
    required_backup: true

  asset_registry_steward:
    purpose: asset records, labels, documentation, lifecycle data
    required_backup: true

  work_order_steward:
    purpose: triage, assignment, priority review, completion verification
    required_backup: true

  tool_library_steward:
    purpose: tools, checkout, safety, repair, consumables
    required_backup: true

  spares_inventory_steward:
    purpose: min-max stock, reorders, supplier list, storage
    required_backup: true

  safety_steward:
    purpose: PPE, stop-work authority, hazardous task boundaries, training
    required_backup: true

  professional_handoff_steward:
    purpose: contractors, permits, service calls, licensed work tracking
    required_backup: true

  seasonal_preparation_steward:
    purpose: winterization, storm season, heat season, drought readiness
    required_backup: true

  failure_review_steward:
    purpose: root cause review, repeated failures, design feedback
    required_backup: true
```

### Role Rule

```text
No critical asset may have only one person who knows how it works.
```

---

## 24. Scenario Simulations

The maintenance and repair module must support stress simulations.

```yaml
maintenance_repair_scenarios:
  normal_year:
    tests:
      - preventive_task_completion
      - work_order_volume
      - backlog_growth
      - labor_distribution
      - budget_use
      - spare_parts_turnover
      - contractor_response

  deferred_maintenance:
    tests:
      - missed_tasks
      - cascading_failures
      - cost_increase
      - resident_comfort_impact
      - critical_asset_risk

  key_maintainer_exit:
    tests:
      - knowledge_loss
      - backup_role_readiness
      - documentation_quality
      - professional_handoff

  supply_chain_delay:
    tests:
      - spare_parts_availability
      - substitute_options
      - downtime
      - critical_floor_impact

  storm_event:
    tests:
      - roof_and_drainage
      - power_outage_response
      - water_intrusion
      - debris_clearance
      - emergency_repairs

  winterization_failure:
    tests:
      - frozen_pipes
      - heating_failures
      - safe_room_use
      - repair_burden
      - water_sanitation_impact

  heat_wave:
    tests:
      - HVAC_load
      - safe_room_readiness
      - filter_maintenance
      - energy_system_stress

  sanitation_failure:
    tests:
      - professional_response
      - PPE
      - emergency_toilets
      - cleaning_labor
      - exposure_risk

  tool_library_breakdown:
    tests:
      - missing_tools
      - unsafe_tools
      - repair_delays
      - resident_frustration
```

---

## 25. Maintenance & Repair Gates

The app should fail or warn based on maintenance viability.

```yaml
maintenance_repair_gates:
  asset_registry_gate:
    fail_if:
      - no_asset_registry
      - class_A_assets_not_registered
      - no_location_for_critical_assets
      - no_documentation_for_critical_assets

    warn_if:
      - no_QR_or_visible_tagging
      - expected_life_unknown_for_major_assets

  critical_asset_gate:
    fail_if:
      - no_criticality_ranking
      - no_maintenance_plan_for_class_A_assets
      - no_failure_response_plan
      - no_backup_steward
      - no_professional_service_path

  safety_gate:
    fail_if:
      - residents_assigned_to_licensed_or_hazardous_work
      - no_stop_work_authority
      - no_PPE_for_required_tasks
      - no_hazardous_energy_boundary
      - no_incident_reporting

  backlog_gate:
    fail_if:
      - open_P0_emergency
      - P1_critical_unresolved_beyond_same_day_without_mitigation
      - critical_backlog_unowned
      - backlog_hidden_from_governance

    warn_if:
      - P2_backlog_growing
      - repeated_failures_without_root_cause_review
      - emergency_work_exceeds_20_percent_of_total

  labor_gate:
    fail_if:
      - maintenance_labor_untracked
      - routine_labor_above_8_hours_per_resident_per_month_unless_staffed
      - same_person_handles_multiple_critical_roles_without_backup

    warn_if:
      - routine_labor_above_5_hours_per_resident_per_month
      - unpleasant_labor_concentrated
      - volunteer_labor_substitutes_for_needed_paid_role

  budget_gate:
    fail_if:
      - no_emergency_repair_reserve
      - no_replacement_reserve_for_class_A_assets
      - professional_service_costs_unmodeled

    warn_if:
      - maintenance_budget_under_actual_trend
      - reserve_drawdown_without_replenishment_plan

  maintainability_gate:
    fail_if:
      - critical_asset_not_safely_accessible
      - maintenance_requires_destructive_access
      - no_local_or_remote_professional_support_for_critical_system
      - proprietary_system_has_no_exit_plan

    warn_if:
      - service_points_hard_to_reach
      - specialized_parts_have_long_lead_time
      - system_is_beautiful_but_uninspectable

  documentation_gate:
    fail_if:
      - no_resident_warning_instructions_for_class_A_assets
      - no_professional_records_for_critical_systems
      - no_emergency_contact_or_shutdown_info

  automation_gate:
    warn_if:
      - no_work_order_system
      - no_preventive_scheduler
      - no_spare_parts_inventory
      - no_exportable_data
      - automation_is_vendor_locked_without_backup
```

---

## 26. App Modeling Boundary

The app should model maintenance and repair at the level of **asset management, task scheduling, labor, safety boundaries, criticality, budget, and professional handoff**, not trade-level repair procedures.

### The App Should Model

```text
asset registry
criticality classes
maintenance modes
inspection schedules
work orders
backlog
failure modes
spare parts
tool library
labor burden
role backup
safety boundaries
professional handoff
maintenance budget
replacement reserve
seasonal preparation
scenario failures
design-for-maintainability warnings
```

### The App Should Not Claim to Solve by Default

```text
licensed electrical work
structural repair design
septic repair
potable water treatment engineering
battery repair
generator installation
gas line work
refrigerant handling
mold remediation beyond minor scope
hazardous materials
medical equipment repair
permit compliance
contractor licensing
```

### Principle

```text
The app should identify what must be maintained, who is responsible, when action is due, what safety boundary applies, and when a professional is required.
```

---

## 27. Required Data Model

```yaml
MaintenanceRepairCommons:
  id: string
  population_served: integer

  asset_registry:
    assets_total: integer
    class_A_assets: integer
    class_A_assets_documented_percent: number
    assets_tagged_percent: number
    manuals_available_percent: number
    replacement_reserve_assets_percent: number

  work_orders:
    open_P0: integer
    open_P1: integer
    open_P2: integer
    open_P3: integer
    open_P4: integer
    completed_this_month: integer
    overdue_tasks: integer
    repeated_failure_count: integer

  labor:
    total_maintenance_hours_per_month: number
    hours_per_resident_per_month: number
    emergency_hours_percent: number
    volunteer_hours: number
    paid_hours: number
    contractor_hours: number
    labor_concentration_score: number
    burnout_risk: low | medium | high

  safety:
    PPE_available: boolean
    stop_work_authority: boolean
    hazardous_energy_protocol: boolean
    incident_log: boolean
    safety_training_complete_percent: number
    restricted_tasks_matrix: boolean

  inventory:
    spare_parts_items: integer
    critical_spares_stocked_percent: number
    below_min_stock_items: integer
    supplier_records_available_percent: number
    emergency_consumables_days: number

  budget:
    annual_maintenance_budget: number
    monthly_actual_spend: number
    emergency_repair_reserve: number
    replacement_reserve: number
    professional_service_budget: number
    reserve_status: pass | warn | fail

  roles:
    maintenance_steward: string
    backup_maintenance_steward: string
    asset_registry_steward: string
    backup_asset_registry_steward: string
    safety_steward: string
    backup_safety_steward: string
    professional_handoff_steward: string
    backup_professional_handoff_steward: string

  automation:
    asset_registry_system: boolean
    work_order_system: boolean
    preventive_scheduler: boolean
    critical_asset_dashboard: boolean
    spare_parts_inventory: boolean
    professional_handoff_engine: boolean
    failure_mode_logger: boolean
    mobile_QR_interface: boolean

  outputs:
    maintenance_readiness_status: pass | warn | fail
    critical_asset_status: pass | warn | fail
    backlog_status: pass | warn | fail
    safety_status: pass | warn | fail
    maintenance_burden_score: number
    maintainability_score: number
    lifecycle_resilience_score: number
    life_burden_reduction_score: number
    complexity_score: number
```

---

## 28. Required App Outputs

```yaml
required_outputs:
  - maintenance_system_summary
  - asset_registry_report
  - critical_asset_report
  - preventive_maintenance_calendar
  - work_order_backlog_report
  - spare_parts_inventory_report
  - tool_library_report
  - safety_boundary_report
  - professional_handoff_report
  - maintenance_labor_burden_report
  - maintenance_budget_and_reserve_report
  - repeated_failure_report
  - seasonal_preparation_report
  - design_for_maintainability_report
  - scenario_failure_report
  - role_backup_report
  - visualization_bundle_metadata
```

---

## 29. Visualization Requirements

The maintenance and repair module should export enough data for a virtual world or dashboard to show what must be maintained and where risk is accumulating.

```yaml
visualization_requirements:
  spatial_objects:
    - maintenance_room
    - tool_library
    - spare_parts_storage
    - PPE_station
    - critical_assets
    - service_points
    - shutoffs
    - inspection_routes
    - contractor_access_points
    - hazardous_areas
    - repeated_failure_locations

  overlays:
    - asset_criticality
    - open_work_orders
    - overdue_maintenance
    - service_access
    - spare_parts_status
    - safety_boundaries
    - professional_required
    - backlog_heatmap
    - moisture_or_leak_alerts
    - maintenance_labor_burden

  scenario_playback:
    - deferred_maintenance
    - key_maintainer_exit
    - supply_chain_delay
    - storm_event
    - winterization_failure
    - heat_wave
    - sanitation_failure
    - tool_library_breakdown
```

---

## 30. Best Default Requirements Summary

```yaml
MinimumViableMaintenanceRepairCommons:
  population:
    first_serious_model: 80
    valid_range: 50-150

  philosophy:
    maintenance_as_civic_spine: true
    heroic_DIY: false
    professional_handoff: required
    visible_backlog: required
    labor_counting: required
    safety_boundaries: required

  facilities:
    maintenance_room: required
    tool_library: required
    spare_parts_storage: required
    repair_bench: required
    PPE_station: required
    documentation_station: required
    hazardous_tool_storage: required

  systems:
    asset_registry: required
    work_order_system: required
    preventive_scheduler: required
    critical_asset_dashboard: required
    spare_parts_inventory: required
    failure_mode_logger: required
    professional_handoff_matrix: required
    maintenance_budget_reserve: required

  targets:
    routine_maintenance_labor_per_resident: 1-3_hours_per_month
    warning_above: 5_hours_per_month
    fail_above: 8_hours_per_month_unless_staffed
    class_A_documentation: 100_percent
    critical_role_backup: 100_percent
    emergency_repair_reserve: required
    replacement_reserve_for_class_A_assets: required

  gates:
    asset_registry_gate: required
    critical_asset_gate: required
    safety_gate: required
    backlog_gate: required
    labor_gate: required
    budget_gate: required
    maintainability_gate: required
    documentation_gate: required
    automation_gate: required
```

---

## 31. Design Maxims

```text
Do not build what cannot be maintained.

Do not let maintenance live in one person's head.

Do not confuse repair culture with permission to do licensed work.

Do not wait for critical assets to fail.

Do not hide backlog.

Do not hide dirty or tedious labor.

Do not let a $20 part disable a survival-critical system.

Do not make residents babysit fragile technology.

Do not let beauty block inspection.

Do not choose proprietary systems without an exit plan.

Register every asset that matters.

Rank assets by consequence of failure.

Schedule the boring work.

Stock the obvious parts.

Call professionals before residents exceed competence.

Count the labor.

Fund the reserve.

Review repeated failures.

Feed maintenance lessons back into design.

Make the civic floor easier to maintain every year.
```

---

## 32. Open Questions for Iteration

```text
1. Should the first prototype use a custom CMMS-lite implementation or integrate with an existing open-source tool?
2. Should maintenance labor be treated as commons contribution, paid work, or a hybrid?
3. What routine maintenance burden is morally acceptable per resident per month?
4. Should a paid part-time facilities steward be required at 80 residents or only above 100?
5. How strict should the app be about proprietary systems and vendor lock-in?
6. Should every physical module be blocked until it provides asset registry fields?
7. What reserve formula should the app use for Class A assets?
8. Should residents be allowed to opt into higher-risk tool training?
9. How should private unit repairs be handled when they affect shared infrastructure?
10. Should maintenance data be public to all residents, role-limited, or split by sensitivity?
11. Should the app simulate deferred maintenance as a mandatory scenario for every plan?
12. What maintenance failure would make the model morally invalid?
```

---

## 33. Source Notes

The research basis for this draft includes:

- U.S. Department of Energy Federal Energy Management Program, Operations and Maintenance Best Practices guidance.
- Whole Building Design Guide, Operation and Maintenance Planning.
- EPA, Asset Management for Water and Wastewater Utilities.
- DOE/FEMP maintenance approach taxonomy, reactive, preventive, predictive, and reliability-centered maintenance.
- NASA Reliability-Centered Maintenance guidance for facilities and collateral equipment.
- OSHA Control of Hazardous Energy, Lockout/Tagout, 29 CFR 1910.147.
- WBDG guidance on involving O&M staff in design and anticipating operations and maintenance needs.
- EPA and WBDG guidance on mold, moisture, building health, and remediation planning.
