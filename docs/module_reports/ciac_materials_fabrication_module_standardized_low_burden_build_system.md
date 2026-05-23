# CIaC Materials & Fabrication Module: Standardized Low-Burden Build System

**Module ID:** `materials_fabrication.standardized_low_burden_build_system.v0_1`  
**Status:** Draft requirement module  
**Purpose:** Define the default materials, fabrication, construction-system, and automation requirements for a scalable Minimum Viable Dignified Infrastructure complex.  
**Primary design question:** What construction system best delivers dignified housing and shared infrastructure with low waste, low embodied burden, high repeatability, professional reviewability, repairability, and automation support, without trapping the project in exotic material risk or bespoke architecture?

---

## 1. Core Thesis

The CIaC materials baseline should **not** begin with exotic construction.

A novel society does not require novel physics.

The recommended baseline is a **Standardized Low-Burden Build System**:

```text
panelized light wood or hybrid mass timber
+ repeated structural grid
+ standardized unit modules
+ stacked wet cores
+ service spines
+ high-performance envelope
+ low-embodied-carbon material preference
+ offsite fabrication where useful
+ standard trades compatibility
+ open BIM / IFC metadata
+ prefab-ready bill of materials
+ design-for-maintenance
+ design-for-disassembly
+ salvage and reuse streams
+ professional review gates
```

The goal is not to create a spectacular building system.

The goal is to build a dignified, repeatable, affordable, maintainable village block with as little heroic labor and material waste as possible.

---

## 2. Guiding Sentence

> Use novel organization before novel materials; use standard materials in smarter patterns before asking residents, builders, lenders, insurers, or code officials to trust a fragile experiment.

---

## 3. Strategic Decision

The best default model is:

# Panelized light-wood / hybrid mass-timber kit-of-parts with passive-envelope principles and offsite-fabrication readiness.

```yaml
materials_fabrication_strategy:
  default_structural_system:
    preferred:
      - panelized_light_wood
      - modular_light_wood
      - hybrid_light_wood_mass_timber
      - mass_timber_for_common_house_or_larger_spans_where_viable
      - standardized_kit_of_parts

  envelope_strategy:
    preferred:
      - high_insulation
      - airtightness
      - thermal_bridge_reduction
      - high_performance_windows_where_economic
      - balanced_ventilation_or_reviewed_ventilation_strategy
      - moisture_safe_assemblies
      - climate_specific_wall_roof_floor_assemblies

  fabrication_strategy:
    preferred:
      - offsite_panelization
      - CNC_or_factory_cut_components_where_economic
      - repeatable_wall_floor_roof_panels
      - standardized_wet_core_modules
      - prefab_ready_BOM
      - open_model_interchange
      - field_assembly_by_normal_trades

  material_priority:
    - safe
    - code_familiar
    - durable
    - repairable
    - low_waste
    - low_embodied_carbon
    - locally_available_where_possible
    - standard_size_compatible
    - professionally_reviewable
    - non_toxic_or_low_toxicity
    - disassemblable_where_practical

  avoid_as_default:
    - unreviewed_experimental_structures
    - shipping_container_gimmicks
    - heroic_DIY_as_baseline
    - bespoke_one_off_architecture
    - complex_custom_joints_without_engineering
    - materials_without_local_trades
    - materials_without_insurance_or_lender_acceptance
    - aesthetics_that_reduce_maintainability
    - total_dependence_on_one_proprietary_vendor
```

### Rationale

The CIaC project is already socially, legally, operationally, and financially ambitious.

The first build system should reduce complexity, not add it.

---

## 4. Research Anchors

This module is grounded in the following research and precedent categories.

### 4.1 Offsite construction

HUD's offsite construction research roadmap describes documented benefits of offsite construction including schedule improvements, quality control, worker safety, and reductions in waste.

**Design implication:** CIaC should support offsite panelization and modular workflows, but must remain aware of transportation, financing, inspection, and local code barriers.

### 4.2 Offsite construction standards

ICC/MBI 1200-2021 addresses planning, design, fabrication, transportation, and assembly of commercial and residential offsite construction elements. ICC/MBI 1205-2021 addresses inspection and regulatory compliance for offsite construction.

**Design implication:** The app should model offsite construction as a regulated process with inspection and compliance gates, not as informal kit-building.

### 4.3 Mass timber

WoodWorks notes that mass timber can reduce foundation costs due to its lighter weight compared with full concrete structures and can provide labor savings through smaller crews and faster installation.

**Design implication:** Mass timber is strong for common houses, larger shared spans, mid-rise residential elements, and low-carbon goals, but it should be evaluated by cost, supply, code path, fire protection, acoustics, moisture risk, and local expertise.

### 4.4 Low embodied carbon

EPA defines low embodied carbon materials as materials with lower greenhouse gas emissions associated with extraction, processing, transportation, and manufacturing.

**Design implication:** The app should track embodied carbon at pattern level and prefer lower-impact materials when they do not undermine safety, cost, durability, or maintainability.

### 4.5 Passive building principles

Passive House principles include high insulation, airtightness, thermal-bridge-free detailing, high-performance windows/doors, and mechanical ventilation with heat recovery.

**Design implication:** CIaC should not necessarily require full Passive House certification in v0, but should use passive-envelope logic because energy resilience begins with lower demand.

### 4.6 Open-source / digital fabrication precedent

WikiHouse uses digital fabrication to create timber components that can be assembled quickly and precisely, with modular CNC-cut timber blocks.

**Design implication:** WikiHouse is a useful precedent for open design, digitally fabricated parts, and distributed manufacturing, but should be treated as an optional pattern or inspiration, not the default structural system until code, engineering, cost, and local fabrication are validated.

### 4.7 Construction and demolition reuse

EPA says recovering used but valuable construction and demolition materials for further use can save money and protect natural resources.

**Design implication:** The app should include deconstruction, salvage, and reuse streams, but must distinguish structural reuse, nonstructural reuse, and decorative reuse.

---

## 5. Recommended Scale

The materials and fabrication module should support the same first serious population as the other CIaC modules.

```yaml
population:
  minimum_meaningful_scale: 50
  ideal_first_model: 80
  upper_bound_before_replication: 150
```

### Scale Logic

```text
Below 50:
  prefabrication and custom kit development may not amortize well unless using an existing system.

Around 80:
  repeated pods, units, wall panels, wet cores, and common-house elements create enough repetition for automation and cost control.

Above 150:
  fabrication complexity, procurement, labor coordination, fire/life-safety, inspections, and staging may require professionalized construction management.
```

### Scaling Method

Replicate a tested village-block kit rather than reinventing each settlement.

```yaml
scaling:
  50-100_residents:
    kit: one_village_block_kit
    repeated_pods: 3-5
    unit_types: 4-8
    shared_buildings: 2-4

  100-150_residents:
    kit: one_larger_or_two_interlinked_blocks
    repeated_pods: 5-8
    unit_types: 6-10
    prefabrication: strongly_preferred

  above_150_residents:
    recommendation: replicate_village_blocks_or_professionalize_as_campus_scale
```

---

## 6. Default Prototype

```yaml
default_prototype:
  name: standardized_low_burden_build_system_80
  residents: 80

  buildings:
    residential_pods:
      count: 4
      residents_per_pod: 20
      structure: panelized_light_wood_or_hybrid
      unit_type_count: 6_max_target

    common_house:
      structure: hybrid_light_wood_mass_timber_or_panelized
      spans: evaluated_for_common_dining_kitchen_meeting_space
      priority: durable_beautiful_repairable

    workshop_maintenance_barn:
      structure: simple_post_frame_light_wood_or_prefab_steel_with_review
      priority: utility_repairability_low_cost

    greenhouse_high_tunnel:
      structure: standard_agricultural_or_greenhouse_system
      priority: simple_repairable_parts

    storage_service_buildings:
      structure: simple_panelized_or_standard_shed_system
      priority: low_cost_weatherproof_maintainable

  construction_system:
    structural_grid: required
    repeated_panels: required
    stacked_wet_cores: required
    service_spines: required
    panelization_ratio_target: 60-85_percent
    custom_detail_ratio_warning_above: 20_percent
    professional_engineering_review: required

  material_baseline:
    primary: light_wood_framing_or_panelized_wood
    secondary: mass_timber_where_value_justified
    foundations: site_specific_low_carbon_concrete_where_possible
    insulation: climate_safe_low_toxicity_reviewed
    exterior_cladding: durable_repairable_low_maintenance
    interior_finishes: low_VOC_durable_repairable
    fasteners: standardized
```

---

## 7. Material Selection Hierarchy

The app should select materials by function, not ideology.

```yaml
material_selection_hierarchy:
  1_health_safety:
    criteria:
      - structural_safety
      - fire_safety
      - moisture_safety
      - indoor_air_quality
      - toxicity
      - code_acceptance

  2_durability:
    criteria:
      - lifespan
      - water_resistance
      - pest_resistance
      - repairability
      - maintenance_interval
      - warranty_or_proven_track_record

  3_affordability:
    criteria:
      - first_cost
      - installed_cost
      - lifecycle_cost
      - labor_cost
      - replacement_cost
      - local_availability

  4_automation_fit:
    criteria:
      - standard_dimensions
      - panelization
      - CNC_or_factory_cut_compatibility
      - BIM_object_support
      - BOM_generation
      - repeatable_connections

  5_embodied_impact:
    criteria:
      - embodied_carbon
      - recycled_content
      - renewability
      - EPD_availability
      - transport_distance
      - end_of_life_path

  6_beauty_and_livability:
    criteria:
      - warmth
      - tactility
      - acoustics
      - daylight_interaction
      - repair_visibility
      - human_preference

  7_circularity:
    criteria:
      - disassembly
      - salvageability
      - reuse
      - recycling
      - compostability_where_appropriate
```

### Material Principle

```text
A material is not better because it is natural, high-tech, cheap, or beautiful. It is better when it serves safety, dignity, affordability, maintainability, and lifecycle coherence together.
```

---

## 8. Construction System Families

The app should compare construction systems at pattern level.

```yaml
construction_system_families:
  panelized_light_wood:
    default_status: primary_baseline
    strengths:
      - code_familiar
      - common_trades
      - prefabrication_ready
      - low_embodied_carbon_relative_to_steel_concrete
      - repairable
      - cost_familiar
      - suitable_for_repeated_pods
    risks:
      - moisture_detailing
      - fire_acoustic_requirements
      - quality_varies_by_builder
      - labor_availability
    best_use:
      - residential_pods
      - small_common_structures
      - service_buildings

  modular_volumetric:
    default_status: optional_evaluate
    strengths:
      - high_factory_completion
      - faster_site_assembly
      - quality_control
      - schedule_reduction
    risks:
      - transportation_limits
      - crane_and_staging
      - financing_draw_mismatch
      - manufacturer_dependency
      - design_constraints
    best_use:
      - repeated_unit_modules
      - bathrooms_or_wet_cores
      - remote_sites_where_transport_works

  mass_timber:
    default_status: preferred_where_value_justified
    strengths:
      - low_embodied_carbon_potential
      - fast_installation
      - smaller_crews
      - beautiful_exposed_structure
      - larger_spans
      - lighter_foundations_than_concrete_steel
    risks:
      - upfront_cost
      - supply_chain
      - fire_code_details
      - acoustic_details
      - moisture_protection_during_construction
      - engineering_review
    best_use:
      - common_house
      - larger_shared_spaces
      - midrise_or_higher_density_elements
      - expressive_civic_spaces

  open_source_CNC_timber:
    default_status: optional_pilot
    strengths:
      - digitally_fabricated
      - open_design_potential
      - local_CNC_fabrication
      - fast_assembly
      - agent_readable_files
    risks:
      - code_acceptance
      - engineering_certification
      - plywood_OSB_supply_and_quality
      - moisture
      - limited_project_track_record
      - connection_performance_review
    best_use:
      - small_structures
      - prototype_pods
      - noncritical_buildings_first
      - educational_demonstration

  straw_bale_hempcrete_earth:
    default_status: optional_climate_code_review
    strengths:
      - low_embodied_carbon_potential
      - good_insulation_or_thermal_mass_depending_system
      - natural_material_appeal
      - possible_local_materials
    risks:
      - moisture_sensitivity
      - code_acceptance
      - skilled_labor
      - slower_construction
      - lender_insurance_acceptance
      - inspection_familiarity
    best_use:
      - regionally_validated_projects
      - noncritical_or_low_risk_structures
      - later_iterations_after_review

  steel_or_concrete:
    default_status: use_when_necessary
    strengths:
      - durability
      - code_familiarity
      - fire_resistance
      - long_spans
      - foundations
      - wet_or_high_abuse_areas
    risks:
      - high_embodied_carbon
      - cost
      - thermal_bridging
      - harder_repair_for_nonprofessionals
    best_use:
      - foundations
      - retaining
      - fire_or_wet_areas
      - workshop_or_infrastructure_where_needed
```

---

## 9. Recommended Baseline Assembly Logic

The app should favor a simple, high-repeatability assembly system.

```yaml
baseline_assembly_logic:
  structural_grid:
    required: true
    target:
      - repeated_bay_widths
      - repeated_wall_panel_dimensions
      - repeated_floor_roof_spans
      - minimized_custom_framing

  units:
    target_unit_type_count: 4-8
    warn_above: 10
    fail_above: 14_without_strong_reason

  wet_cores:
    required: true
    strategy:
      - stack_bathrooms
      - cluster_kitchens
      - align_laundry
      - service_access_from_corridor_or_utility_spine
      - minimize_pipe_runs

  service_spine:
    required: true
    includes:
      - plumbing
      - electrical_distribution
      - data
      - ventilation
      - maintenance_access
      - shutoff_access

  panel_library:
    required: true
    panel_types:
      - exterior_wall
      - interior_wall
      - roof
      - floor
      - service_wall
      - wet_core_wall
      - window_panel
      - door_panel
      - acoustic_wall

  connection_library:
    required: true
    requirements:
      - engineered
      - inspectable
      - replaceable_where_possible
      - standardized_fasteners
      - documented_torque_or_installation_requirements_where_needed

  assembly_sequence:
    required: true
    phases:
      - foundation_or_base
      - service_stubups
      - structural_panels
      - roof_weatherproofing
      - envelope_sealing
      - rough_services
      - inspections
      - interiors
      - commissioning
```

### Assembly Principle

```text
A good CIaC building should feel like an intelligent product, not a custom miracle.
```

---

## 10. Envelope Standard

The envelope is the first energy system.

```yaml
envelope_standard:
  required:
    - climate_zone_specific_assembly
    - continuous_air_barrier
    - continuous_water_resistive_barrier
    - thermal_bridge_reduction
    - adequate_insulation
    - vapor_control_strategy
    - moisture_drying_path
    - high_quality_windows_and_doors
    - ventilation_strategy
    - blower_door_or_air_leakage_test_where_feasible
    - commissioning_checklist

  preferred:
    - passive_house_informed_detailing
    - ERV_or_HRV_where_climate_and_design_support
    - exterior_continuous_insulation_where_viable
    - rainscreen_cladding_where_climate_supports
    - shade_and_solar_control
    - durable_roof_overhangs_where_appropriate

  fail_if:
    - assembly_has_no_moisture_strategy
    - no_ventilation_strategy_for_airtight_building
    - thermal_bridge_details_unreviewed
    - envelope_design_cannot_be_inspected
```

### Envelope Principle

```text
Do not solve with batteries what the envelope could have prevented.
```

---

## 11. Foundations and Site Interface

Foundations should be conservative, site-specific, and low-carbon where possible.

```yaml
foundation_site_interface:
  required:
    - geotechnical_review
    - drainage_plan
    - frost_depth_or_climate_review
    - floodplain_review
    - groundwater_review
    - radon_review_where_regionally_relevant
    - termite_or_pest_review_where_relevant
    - accessibility_grade_strategy
    - future_service_access

  preferred:
    - minimize_concrete_where_safe
    - low_embodied_carbon_concrete_mix_where_available
    - pier_or_screw_pile_where_appropriate_and_reviewed
    - slab_edge_thermal_breaks_where_needed
    - durable_drainage
    - replaceable_deck_and_path_components

  app_boundary:
    - app_models_foundation_strategy_and_review_requirements
    - professional_engineer_designs_final_foundation
```

### Foundation Principle

```text
The cheapest structure becomes expensive if the site interface is wrong.
```

---

## 12. Interior Materials

Interior finishes should be durable, low-toxicity, repairable, and warm.

```yaml
interior_materials:
  required:
    - low_VOC_or_low_emission_materials
    - durable_flooring_in_common_areas
    - repairable_wall_finishes
    - cleanable_kitchen_and_care_surfaces
    - acoustic_treatment_where_needed
    - moisture_resistant_bathroom_materials
    - replaceable_components
    - non_slip_surfaces_where_relevant
    - accessible_hardware

  preferred:
    - natural_or_warm_tactile_surfaces
    - exposed_mass_timber_where_safe_and_cost_effective
    - modular_casework
    - standard_door_window_hardware
    - demountable_partitions_where_useful
    - washable_common_space_finishes

  avoid:
    - fragile_aesthetic_finishes_in_high_use_areas
    - toxic_or_high_offgassing_products
    - proprietary_replacement_parts_for_basic_interiors
    - finishes_that_hide_water_damage
```

### Interior Principle

```text
Dignity is not luxury, but people should not have to live inside materials that feel disposable, toxic, or institutional.
```

---

## 13. Acoustic and Privacy Materials

Materials must protect privacy, not only structure.

```yaml
acoustic_privacy_materials:
  required:
    - acoustic_separation_between_private_units
    - acoustic_buffer_between_common_spaces_and_sleeping_areas
    - impact_noise_strategy_for_floors
    - mechanical_noise_control
    - workshop_noise_buffer
    - laundry_noise_buffer
    - care_room_acoustic_privacy

  preferred:
    - resilient_channels_or_acoustic_details_where_needed
    - mass_layers_where_needed
    - soft_common_space_finishes
    - quiet_doors_and_hardware
    - courtyard_noise_model

  fail_if:
    - private_units_have_no_acoustic_strategy
    - workshop_or_common_kitchen_noise_reaches_sleeping_units
    - care_room_privacy_compromised
```

### Acoustic Principle

```text
Privacy is partly built out of sound control.
```

---

## 14. Fire, Moisture, Pest, and Durability Gates

Material choices must pass basic hazard gates.

```yaml
hazard_durability_gates:
  fire_gate:
    fail_if:
      - structural_system_has_no_code_path
      - fire_ratings_unmodeled
      - battery_or_mechanical_rooms_not_separated_as_required
      - egress_impacted_by_material_choice
      - untreated_combustible_details_unreviewed

  moisture_gate:
    fail_if:
      - material_vulnerable_to_moisture_without_protection
      - no_drying_path
      - no_construction_phase_weather_protection
      - no_leak_detection_or_inspection_access
      - humid_climate_assembly_unreviewed

  pest_gate:
    fail_if:
      - material_or_detail_invites_pests_without_controls
      - food_storage_or waste zones not pest-resistant
      - wood_in_ground_contact_without_review
      - termite_region_without_strategy

  durability_gate:
    fail_if:
      - critical_material_life_shorter_than_replacement_plan
      - no_maintenance_interval
      - no_spare_or_repair_path
      - product_discontinued_or_vendor_locked_for_basic_components
```

### Hazard Principle

```text
Low-carbon and low-cost materials are failures if they rot, burn, poison, or invite pests because the system ignored context.
```

---

## 15. Fabrication Workflow

The app should generate fabrication-ready information without pretending to replace construction documents.

```yaml
fabrication_workflow:
  model_inputs:
    - population
    - pod_count
    - unit_mix
    - structural_grid
    - climate_zone
    - material_system
    - module_library
    - local_code_profile
    - fabrication_method
    - transport_limits
    - site_access
    - assembly_sequence

  generated_outputs:
    - module_schedule
    - panel_schedule
    - bill_of_materials
    - cut_list_if_supported
    - transport_package_list
    - staging_plan
    - assembly_sequence
    - inspection_points
    - professional_review_requirements
    - waste_estimate
    - embodied_carbon_estimate
    - maintenance_asset_seed_list
    - IFC_or_BIM_metadata
    - Unreal_visualization_metadata

  required_review:
    - architect_or_designer
    - structural_engineer
    - MEP_engineer_where_needed
    - fire_code_review
    - building_official
    - fabricator
    - contractor
```

### Fabrication Principle

```text
The app can prepare the recipe. Licensed and qualified humans must approve the kitchen, ingredients, and cooking process.
```

---

## 16. BIM / IFC / Data Requirements

The materials module must be machine-readable.

```yaml
data_requirements:
  BIM_IFC:
    preferred: true
    purpose:
      - professional_review
      - quantity_takeoff
      - clash_detection
      - lifecycle_asset_seeding
      - downstream_visualization

  object_metadata:
    required_fields:
      - object_id
      - material_type
      - assembly_type
      - manufacturer_or_generic_spec
      - dimensions
      - quantity
      - embodied_carbon_factor_if_known
      - fire_rating_if_applicable
      - acoustic_rating_if_applicable
      - moisture_risk_notes
      - maintenance_interval
      - expected_life
      - replacement_path
      - salvage_or_disassembly_path

  interoperability:
    required:
      - JSON_or_YAML_export
      - CSV_BOM_export
      - open_schema
      - versioned_pattern_library
      - no_single_vendor_file_dependency

  visualization:
    required:
      - simplified_mesh_bundle
      - material_tags
      - assembly_tags
      - maintenance_access_zones
      - construction_phase_states
```

### Data Principle

```text
A material that the system cannot count, inspect, or replace is not truly part of the civic model.
```

---

## 17. Bill of Materials and Procurement

The app should make procurement legible and substitution-aware.

```yaml
BOM_procurement:
  required:
    - material_category
    - quantity
    - unit
    - dimension
    - grade_or_spec
    - acceptable_substitutes
    - local_availability_status
    - lead_time
    - cost_range
    - waste_factor
    - supplier_options
    - warranty
    - maintenance_implication
    - embodied_carbon_data_if_available
    - professional_review_flag

  substitution_rules:
    allowed_if:
      - same_or_better_safety
      - compatible_with_assembly
      - compatible_with_fire_moisture_acoustic_requirements
      - professional_review_where_structural_or_life_safety
      - maintenance_path_preserved
      - documentation_updated

    prohibited_if:
      - structural_performance_unknown
      - fire_rating_invalidated
      - moisture_strategy_invalidated
      - toxic_exposure_increased
      - proprietary_lock_in_unacceptable
      - code_path_lost
```

### Procurement Principle

```text
Substitution is where good designs often fail. The app must treat material swaps as engineering events, not shopping choices.
```

---

## 18. Waste Reduction and Cut Optimization

Construction waste should be designed out early.

```yaml
construction_waste_reduction:
  required:
    - standard_sheet_and_lumber_dimension_awareness
    - panel_cut_optimization_where_supported
    - repeated_modules
    - accurate_BOM
    - offcut_reuse_plan
    - packaging_waste_plan
    - site_sorting_plan
    - deconstruction_or_salvage_plan
    - construction_waste_tracking

  preferred:
    - factory_cut_or_panelized_components
    - reusable_shipping_racks
    - material_takeback_programs
    - modular_fasteners
    - demountable_interior_partitions
    - salvage_yard_integration

  app_outputs:
    - estimated_waste_percent
    - offcut_plan
    - salvageable_material_list
    - landfill_risk
    - reuse_opportunities
```

### Waste Principle

```text
Waste is usually a design decision made before construction begins.
```

---

## 19. Salvage, Reuse, and Deconstruction

Reuse is valuable, but must be risk-classified.

```yaml
salvage_reuse:
  reuse_classes:
    structural_reuse:
      default_status: professional_review_required
      examples:
        - beams
        - columns
        - structural_lumber
        - steel
      requirements:
        - grading_or_engineering
        - code_acceptance
        - documentation

    nonstructural_reuse:
      default_status: preferred_where_safe
      examples:
        - doors
        - cabinets
        - fixtures
        - flooring
        - brick_pavers
        - shelving
      requirements:
        - lead_asbestos_toxicity_screening_where_relevant
        - condition_check
        - repair_plan

    landscape_site_reuse:
      default_status: preferred_where_safe
      examples:
        - stone
        - brick
        - gravel
        - timbers_where_safe
      requirements:
        - contamination_check
        - drainage_compatibility

    decorative_reuse:
      default_status: allowed
      examples:
        - trim
        - art_materials
        - furniture
      requirements:
        - safety_check

  design_for_deconstruction:
    preferred:
      - mechanical_fasteners
      - accessible_connections
      - material_labeling
      - avoid_unnecessary_adhesives
      - component_replacement_without_demolition
      - disassembly_sequence_documented
```

### Reuse Principle

```text
Reuse is not automatically virtuous. It must be safe, documented, and appropriate to the risk class.
```

---

## 20. Local Fabrication and Automation

Automation should reduce cost, waste, and complexity, not create techno-dependence.

```yaml
local_fabrication:
  possible_methods:
    - regional_panel_shop
    - modular_factory
    - CNC_router_shop
    - timber_fabricator
    - community_workshop_for_nonstructural_components
    - maker_space_for_furniture_fixtures_signage
    - salvage_and_repair_shop

  best_targets_for_local_fabrication:
    - wall_panels
    - roof_panels_where_reviewed
    - simple_casework
    - shelving
    - beds_and_storage
    - tables
    - garden_infrastructure
    - signage
    - nonstructural_partitions
    - repair_parts_templates

  professional_fabrication_required:
    - structural_panels_without_approved_system
    - mass_timber_elements
    - trusses
    - fire_rated_assemblies
    - windows_doors
    - MEP_systems
    - battery_enclosures
    - pressure_or_water_treatment_components

  automation_requirements:
    - machine_readable_BOM
    - parametric_module_library
    - cut_sheets
    - nesting_optimization
    - quality_control_checklists
    - tolerances
    - assembly_instructions
    - inspection_points
```

### Automation Principle

```text
Automate the repetitive and legible. Do not automate past review, tolerances, or safety.
```

---

## 21. Standardization vs Variety

The app must balance standardization with human delight.

```yaml
standardization_variety:
  standardize:
    - structural_bays
    - wet_cores
    - service_spines
    - wall_panel_types
    - window_door_sizes_where_possible
    - stairs_and_access_components
    - kitchens_and_bathroom_modules
    - fasteners
    - maintenance_access
    - asset_metadata

  allow_variety:
    - exterior_colors_within_palette
    - courtyard_character
    - interior finishes within approved families
    - unit_furniture_layouts
    - gardens
    - art
    - shading_devices
    - porches_thresholds
    - nonstructural partitions

  warn_if:
    - custom_variation_increases_cost_without_livability_gain
    - unit_variation_breaks_panelization
    - aesthetic_detail_blocks_maintenance
    - variety_creates_inequity_between_residents
```

### Variety Principle

```text
Standardize the skeleton. Humanize the skin, thresholds, gardens, and interiors.
```

---

## 22. Tooling and Construction Labor

The build system should not require rare skills for ordinary tasks.

```yaml
tooling_labor:
  required:
    - crew_skill_profile
    - tool_requirements
    - training_requirements
    - safety_requirements
    - assembly_tolerances
    - weather_protection_plan
    - crane_or_lift_requirements
    - staging_area
    - transport_constraints
    - quality_control_points

  preferred:
    - normal_trade_compatibility
    - smaller_crews_where_safe
    - repeatable_tasks
    - short_training_for_noncritical_assembly
    - professional_lead_for_critical_assembly
    - resident_participation_only_where_safe_and_voluntary

  avoid:
    - relying_on_resident_labor_for_critical_path
    - requiring_rare_specialist_for_basic_repairs
    - field_customization_for_every_unit
    - unclear_tolerances
    - weather_exposed_mass_timber_or_panels_without_plan
```

### Labor Principle

```text
Resident participation is beautiful when voluntary and safe; it is exploitation when needed to make the budget work.
```

---

## 23. Cost Model

The materials module must distinguish first cost, installed cost, operating cost, and lifecycle cost.

```yaml
cost_model:
  required_costs:
    - material_first_cost
    - fabrication_cost
    - transport_cost
    - site_staging_cost
    - installation_labor
    - crane_or_equipment
    - waste_disposal
    - professional_review
    - inspection
    - maintenance
    - replacement
    - insurance_or_lender_premium_if_unusual
    - contingency

  output_metrics:
    - cost_per_square_foot_or_meter
    - cost_per_resident
    - cost_per_unit_type
    - cost_per_pod
    - cost_per_common_space
    - cost_per_lifecycle_year
    - cost_delta_vs_baseline
    - labor_hours_saved
    - schedule_days_saved
    - waste_reduction_percent
    - embodied_carbon_delta

  warning_conditions:
    - low_material_cost_high_labor_cost
    - cheap_material_high_maintenance
    - novel_material_insurance_unknown
    - offsite_savings_erased_by_transport
    - custom_detail_cost_creep
    - lifecycle_replacement_unfunded
```

### Cost Principle

```text
The cheapest material is not cheap if it costs time, trust, insurance, maintenance, or replacement later.
```

---

## 24. Interfaces With Other Modules

### 24.1 Housing Interface

```yaml
housing_materials_interface:
  required:
    - pod_structural_system
    - private_unit_assemblies
    - acoustic_privacy
    - common_space_durability
    - wet_core_modules
    - service_spines
    - accessibility_components
```

```text
The housing concept becomes real only when the build system can repeat it affordably.
```

### 24.2 Food Interface

```yaml
food_materials_interface:
  required:
    - cleanable_kitchen_surfaces
    - durable_dining_finishes
    - food_storage_materials
    - greenhouse_system
    - wash_pack_surfaces
    - pest_resistant_storage
```

```text
Food infrastructure needs materials that clean easily and do not invite pests or contamination.
```

### 24.3 Water Interface

```yaml
water_materials_interface:
  required:
    - pipe_chase_access
    - wet_area_moisture_protection
    - cistern_or_tank_materials
    - pump_room_materials
    - leak_detection_access
    - freeze_protection
```

```text
Water belongs in accessible, inspectable places, not hidden inside beautiful future mold.
```

### 24.4 Sanitation Interface

```yaml
sanitation_materials_interface:
  required:
    - cleanable_bathroom_surfaces
    - waste_sorting_area_durability
    - compost_area_materials
    - hazardous_waste_lockup
    - washable_laundry_finishes
```

```text
Sanitation spaces need to be durable before they are picturesque.
```

### 24.5 Energy Interface

```yaml
energy_materials_interface:
  required:
    - roof_solar_readiness
    - battery_room_material_review
    - mechanical_room_access
    - envelope_performance
    - thermal_bridge_control
    - safe_room_materials
```

```text
Energy resilience starts with the materials around the people, not the battery afterthought.
```

### 24.6 Care Interface

```yaml
care_materials_interface:
  required:
    - low_VOC_finishes
    - cleanable_care_room_surfaces
    - acoustic_privacy
    - accessible_hardware
    - non_slip_surfaces
    - medication_refrigeration_location
```

```text
Care spaces should be calm, cleanable, accessible, and non-institutional.
```

### 24.7 Maintenance Interface

```yaml
maintenance_materials_interface:
  required:
    - asset_registry_seeding
    - service_access
    - standard_parts
    - replacement_paths
    - inspection_panels
    - maintenance_clearances
    - documentation
```

```text
The materials module must make the maintenance module easier, not busier.
```

### 24.8 Legal Land & Finance Interface

```yaml
legal_finance_materials_interface:
  required:
    - code_path
    - lender_acceptance_risk
    - insurance_acceptance_risk
    - capital_cost
    - replacement_reserve
    - warranties
    - professional_review
```

```text
A construction system that cannot be financed, insured, or permitted is not a civic baseline.
```

### 24.9 Labor & Time Interface

```yaml
labor_time_materials_interface:
  required:
    - build_labor
    - maintenance_labor
    - repair_labor
    - resident_participation_boundary
    - hidden_labor_risk
    - schedule_duration
```

```text
Materials should return time by reducing repeated labor, not steal time through complicated upkeep.
```

---

## 25. Automation-Favoring Requirements

Automation should generate options, estimates, conflicts, and handoffs.

```yaml
automation_requirements:
  parametric_layout_engine:
    required: true
    purpose:
      - generate_pod_layouts
      - repeat_unit_types
      - align_wet_cores
      - minimize_custom_panels
      - test_common_space_ratios

  materials_selector:
    required: true
    purpose:
      - evaluate_material_families
      - rank_by_safety_cost_carbon_maintenance
      - flag_code_insurance_lender_risk
      - suggest_standard_substitutions

  BOM_generator:
    required: true
    purpose:
      - quantity_takeoff
      - cost_estimation
      - procurement
      - waste_estimation
      - reserve_seed_data

  embodied_carbon_estimator:
    required: true
    purpose:
      - compare_material_options
      - flag_high_impact_components
      - track_EPD_availability
      - support_low_embodied_carbon choices

  fabrication_planner:
    required: true
    purpose:
      - panel_schedule
      - cut_sheets
      - nesting
      - transport_packaging
      - staging_plan
      - assembly_sequence

  review_gate_engine:
    required: true
    purpose:
      - structural_review
      - fire_review
      - envelope_review
      - moisture_review
      - code_review
      - fabricator_review

  BIM_IFC_export:
    preferred: true
    purpose:
      - professional_handoff
      - asset_registry_seed
      - coordination
      - visualization

  Unreal_visualization_export:
    preferred: true
    purpose:
      - human_scale_review
      - construction_phase_visualization
      - maintenance_access_visualization

  avoid:
    - AI_choosing_structural_materials_without_engineering_review
    - hidden_substitution_risk
    - black_box_cost_estimates
    - proprietary_design_files_without_export
    - overoptimized_forms_that_build_poorly
```

### Automation Principle

```text
Automate counting, comparing, sequencing, and handoff. Do not automate professional accountability out of the loop.
```

---

## 26. Roles

```yaml
materials_fabrication_roles:
  materials_steward:
    purpose: material families, specs, substitutions, documentation
    required_backup: true

  fabrication_steward:
    purpose: panelization, fabrication vendors, cut sheets, staging
    required_backup: true

  BIM_data_steward:
    purpose: model metadata, IFC exports, BOM integrity, asset seeding
    required_backup: true

  embodied_carbon_steward:
    purpose: carbon comparisons, EPD tracking, low-carbon substitutions
    required_backup: true

  constructability_steward:
    purpose: assembly sequence, crew needs, site logistics, weather protection
    required_backup: true

  code_review_liaison:
    purpose: architect, engineer, building official, fire review
    required_backup: true

  salvage_reuse_steward:
    purpose: reuse materials, deconstruction plan, salvage sourcing
    required_backup: true

  maintenance_design_liaison:
    purpose: service access, replacement paths, asset registry seeding
    required_backup: true
```

### Role Rule

```text
No one may swap a structural, fire, moisture, or life-safety material without documented review.
```

---

## 27. Scenario Simulations

The materials and fabrication module must support stress simulations.

```yaml
materials_fabrication_scenarios:
  normal_build:
    tests:
      - BOM_accuracy
      - panelization_ratio
      - construction_sequence
      - labor_hours
      - waste
      - review_gates
      - cost

  material_price_spike:
    tests:
      - substitution_options
      - cost_increase
      - affordability_impact
      - code_risk
      - embodied_carbon_change

  supply_chain_delay:
    tests:
      - lead_time
      - alternate_supplier
      - schedule_delay
      - weather_exposure
      - financing_carry_cost

  fabricator_unavailable:
    tests:
      - alternate_fabricator
      - site_built_fallback
      - quality_control
      - cost_delta
      - schedule_delay

  moisture_event_during_construction:
    tests:
      - weather_protection
      - exposed_mass_timber_or_panels
      - drying_plan
      - mold_risk
      - inspection

  code_review_failure:
    tests:
      - noncompliant_assembly
      - fire_rating_gap
      - structural_detail_gap
      - redesign_cost
      - delay

  maintenance_after_5_years:
    tests:
      - envelope_inspection
      - cladding_repair
      - service_access
      - replacement_parts
      - moisture_detection
      - finish_durability

  deconstruction_end_of_life:
    tests:
      - salvageable_components
      - landfill_fraction
      - disassembly_sequence
      - material_value
      - hazardous_materials
```

---

## 28. Materials & Fabrication Gates

The app should fail or warn based on build-system viability.

```yaml
materials_fabrication_gates:
  code_path_gate:
    fail_if:
      - structural_system_has_no_code_path
      - fire_rating_path_missing
      - professional_review_absent
      - material_not_accepted_by_authority_and_no_alternative

    warn_if:
      - code_path_requires_variance
      - local_trades_unfamiliar
      - inspector_acceptance_uncertain

  automation_gate:
    fail_if:
      - no_BOM
      - no_repeatable_module_library
      - no_assembly_sequence
      - no_material_metadata
      - no_review_gate_engine

    warn_if:
      - too_many_custom_panels
      - unit_type_count_too_high
      - fabrication_files_vendor_locked
      - manual_takeoff_required_for_core_system

  affordability_gate:
    fail_if:
      - material_system_exceeds_cost_target_without_life_burden_gain
      - lifecycle_cost_unmodeled
      - maintenance_cost_unmodeled
      - construction_labor_required_unavailable

    warn_if:
      - offsite_savings_erased_by_transport
      - custom_details_drive_cost
      - material_price_volatility_high

  maintainability_gate:
    fail_if:
      - service_points_inaccessible
      - critical_components_not_replaceable
      - moisture_prone_assembly_uninspectable
      - proprietary_basic_components_no_exit_path

    warn_if:
      - specialized_tools_required_for_common_repairs
      - long_lead_replacement_parts
      - beauty_blocks_access

  embodied_impact_gate:
    fail_if:
      - high_embodied_carbon_system_chosen_without_reason
      - no_embodied_carbon_tracking
      - unnecessary_concrete_or_steel_without_functional_need

    warn_if:
      - EPD_data_missing
      - long_distance_transport_high
      - material_substitution_increases_carbon_significantly

  durability_gate:
    fail_if:
      - no_moisture_strategy
      - no_fire_strategy
      - no_pest_strategy
      - no_expected_life
      - no_replacement_plan

  health_gate:
    fail_if:
      - high_toxicity_material_in_living_or_care_space_without_review
      - no_ventilation_strategy
      - no_low_emission_interior_material_policy
      - mold_risk_unreviewed

  labor_gate:
    fail_if:
      - construction_budget_depends_on_required_unpaid_resident_labor
      - specialized_installation_labor_unavailable
      - safety_training_absent_for_resident_participation

    warn_if:
      - resident_labor_needed_for_schedule
      - assembly_complexity_high
      - weather_protection_labor_unmodeled

  reuse_gate:
    warn_if:
      - no_deconstruction_plan
      - no_construction_waste_plan
      - salvage_reuse_claims_not_classified_by_risk
```

---

## 29. App Modeling Boundary

The app should model materials and fabrication at the level of **system selection, pattern assemblies, BOM, cost, embodied impact, review gates, maintainability, and fabrication handoff**, not final architectural or engineering documents.

### The App Should Model

```text
construction system family
structural grid
module library
panel library
wet core stacking
service spine logic
material families
BOM
cost ranges
embodied carbon estimates
waste estimates
fabrication workflows
assembly sequence
maintenance access
salvage and reuse class
professional review gates
visualization metadata
```

### The App Should Not Claim to Solve by Default

```text
final structural engineering
architectural construction documents
fire-rated assembly certification
building permit approval
seismic design
wind design
foundation engineering
HVAC design
electrical design
plumbing design
shop drawings
warranty qualification
contractor means and methods
code official approval
```

### Principle

```text
The app should identify the safest, simplest, most repeatable build pattern and what professionals must review before it becomes real.
```

---

## 30. Required Data Model

```yaml
MaterialsFabricationCommons:
  id: string
  population_served: integer

  construction_system:
    primary_system: panelized_light_wood | modular_light_wood | mass_timber | hybrid | CNC_timber | other
    code_path_status: unknown | provisional | reviewed | approved | failed
    professional_review_required: boolean
    structural_grid_defined: boolean
    unit_type_count: integer
    panelization_ratio_percent: number
    custom_detail_ratio_percent: number
    wet_cores_stacked: boolean
    service_spine_defined: boolean

  material_palette:
    primary_structure_material: string
    secondary_structure_material: string
    foundation_strategy: string
    insulation_family: string
    cladding_family: string
    interior_finish_family: string
    roofing_family: string
    window_door_strategy: string
    low_VOC_policy: boolean
    low_embodied_carbon_policy: boolean

  fabrication:
    fabrication_method: site_built | panelized | volumetric_modular | CNC | hybrid
    BOM_available: boolean
    cut_sheets_available: boolean
    assembly_sequence_available: boolean
    transport_plan: boolean
    staging_plan: boolean
    quality_control_checklists: boolean
    inspection_points_defined: boolean

  cost:
    estimated_material_cost: number
    estimated_fabrication_cost: number
    estimated_installation_labor_cost: number
    estimated_transport_cost: number
    estimated_total_build_cost: number
    estimated_lifecycle_cost: number
    cost_per_resident: number
    cost_per_square_meter_or_foot: number
    contingency_percent: number

  embodied_impact:
    embodied_carbon_estimate: number
    EPD_coverage_percent: number
    high_impact_materials_listed: boolean
    low_carbon_substitutions_available: boolean
    transport_impact_estimated: boolean

  durability_maintenance:
    expected_life_major_components: boolean
    maintenance_intervals_defined: boolean
    service_access_score: number
    replacement_path_defined: boolean
    moisture_strategy: boolean
    fire_strategy: boolean
    pest_strategy: boolean
    acoustic_strategy: boolean

  circularity:
    construction_waste_estimate_percent: number
    offcut_reuse_plan: boolean
    salvage_reuse_plan: boolean
    design_for_disassembly_score: number
    deconstruction_plan: boolean
    landfill_fraction_estimate: number

  automation:
    parametric_layout_engine: boolean
    materials_selector: boolean
    BOM_generator: boolean
    embodied_carbon_estimator: boolean
    fabrication_planner: boolean
    review_gate_engine: boolean
    BIM_IFC_export: boolean
    Unreal_visualization_export: boolean

  outputs:
    build_system_status: pass | warn | fail
    affordability_status: pass | warn | fail
    code_review_status: pass | warn | fail
    maintainability_status: pass | warn | fail
    embodied_impact_status: pass | warn | fail
    automation_readiness_score: number
    fabrication_readiness_score: number
    maintainability_score: number
    life_burden_reduction_score: number
    complexity_score: number
```

---

## 31. Required App Outputs

```yaml
required_outputs:
  - materials_system_summary
  - construction_system_comparison
  - recommended_material_palette
  - code_path_and_professional_review_report
  - structural_grid_and_module_report
  - panelization_report
  - wet_core_service_spine_report
  - BOM_and_procurement_report
  - cost_and_lifecycle_report
  - embodied_carbon_report
  - waste_reduction_report
  - fabrication_sequence_report
  - transport_and_staging_report
  - maintainability_report
  - salvage_reuse_deconstruction_report
  - substitution_risk_report
  - scenario_failure_report
  - visualization_bundle_metadata
```

---

## 32. Visualization Requirements

The materials module should export enough data for a virtual world, BIM viewer, or construction review dashboard.

```yaml
visualization_requirements:
  spatial_objects:
    - structural_grid
    - wall_panels
    - floor_panels
    - roof_panels
    - wet_cores
    - service_spines
    - common_house_structure
    - mass_timber_elements_if_any
    - maintenance_access_zones
    - assembly_staging_areas
    - transport_dropoff
    - salvage_storage
    - waste_sorting

  overlays:
    - material_types
    - panelization
    - custom_details
    - service_access
    - embodied_carbon_hotspots
    - fire_review_zones
    - moisture_risk_zones
    - acoustic_privacy_zones
    - replacement_paths
    - construction_sequence
    - review_required

  scenario_playback:
    - normal_build
    - material_price_spike
    - supply_chain_delay
    - fabricator_unavailable
    - moisture_event_during_construction
    - code_review_failure
    - maintenance_after_5_years
    - deconstruction_end_of_life
```

---

## 33. Best Default Requirements Summary

```yaml
MinimumViableMaterialsFabricationCommons:
  population:
    first_serious_model: 80
    valid_range: 50-150

  philosophy:
    novel_organization_before_novel_materials: true
    standard_trades_compatibility: required
    offsite_fabrication_ready: required
    exotic_materials_optional_later: true
    professional_review_required: true
    design_for_maintenance: required
    design_for_disassembly: preferred

  baseline:
    primary_system: panelized_light_wood
    secondary_system: hybrid_mass_timber_where_value_justified
    envelope: passive_house_informed_not_certification_required
    unit_strategy: repeated_unit_types
    wet_core_strategy: stacked
    service_strategy: service_spine
    data_strategy: BIM_IFC_or_open_metadata

  materials:
    low_embodied_carbon_policy: required
    low_VOC_interiors: required
    durable_common_space_finishes: required
    moisture_safe_assemblies: required
    acoustic_privacy_strategy: required
    standard_fasteners: required
    local_availability_check: required

  automation:
    parametric_layout_engine: required
    BOM_generator: required
    fabrication_planner: required
    embodied_carbon_estimator: required
    review_gate_engine: required
    BIM_IFC_export: preferred
    Unreal_visualization_export: preferred

  gates:
    code_path_gate: required
    automation_gate: required
    affordability_gate: required
    maintainability_gate: required
    embodied_impact_gate: required
    durability_gate: required
    health_gate: required
    labor_gate: required
    reuse_gate: required
```

---

## 34. Design Maxims

```text
Use novel organization before novel materials.

Use standard materials in smarter patterns.

Do not make the first civic floor depend on experimental construction.

Do not choose a material that cannot be permitted, insured, financed, maintained, or replaced.

Do not treat natural materials as automatically safe.

Do not treat high-tech materials as automatically better.

Do not confuse low first cost with low life burden.

Do not solve energy with machines before improving the envelope.

Do not hide water where it cannot be inspected.

Do not let beauty block service access.

Do not let custom details multiply.

Do not make resident labor the construction subsidy.

Do not let material substitution silently break the design.

Standardize the skeleton.

Humanize the thresholds.

Panelize what repeats.

Expose what needs maintenance.

Track embodied carbon.

Fund replacement.

Design for deconstruction.

Build the first version with materials the world already knows how to approve.
```

---

## 35. Open Questions for Iteration

```text
1. Should the default structural system be panelized light wood, or should hybrid mass timber be the default for the common house?
2. What panelization ratio should the app target before warning: 60%, 70%, or 80%?
3. Should Passive House certification be a goal, or should the app only require passive-informed envelope principles?
4. Should WikiHouse-style CNC timber be a v1 optional pilot or remain only a research precedent?
5. Which materials should be banned by default for toxicity, maintenance, or fire risk?
6. Should the app require Environmental Product Declarations for major materials or merely prefer them?
7. Should the app model local material availability by jurisdiction?
8. How much aesthetic customization should be allowed before automation savings collapse?
9. Should resident labor be allowed in construction, and if so, for what task classes?
10. What is the acceptable lifecycle cost premium for lower embodied carbon?
11. Should the system prefer local fabrication even if it costs more?
12. How strict should design-for-disassembly requirements be in v0?
13. What material or fabrication failure would make the entire CIaC design morally invalid?
```

---

## 36. Source Notes

The research basis for this draft includes:

- HUD offsite construction research roadmap.
- ICC/MBI 1200-2021 and 1205-2021 offsite construction standards.
- WoodWorks resources on mass timber in affordable multifamily housing.
- EPA low embodied carbon materials definitions and Buy Clean / low-carbon procurement resources.
- Passive House principles, including insulation, airtightness, high-performance windows and doors, thermal-bridge reduction, and heat-recovery ventilation.
- WikiHouse open-source digital fabrication precedent.
- EPA sustainable construction and demolition materials management guidance.
- Building deconstruction and reuse practices.
