# CIaC Food Module Supplement: Protein Commons

**Supplement ID:** `food.protein_commons_supplement.v0_1`  
**Parent module:** `food.hybrid_food_commons.v0_1`  
**Status:** Draft supplement  
**Purpose:** Extend the CIaC Food Module with a sustainable, ethical, resilient complete-protein system that minimizes external protein dependency without relying on factory farming, conventional livestock, or one fragile novel technology.

---

## 1. Core Thesis

The CIaC food system should not search for one perfect protein.

The recommended model is a **Protein Commons**:

```text
diet-level complete protein
+ staple legumes and grains
+ soy or equivalent complete plant protein
+ duckweed / water lentils as the preferred novel fresh protein layer
+ fermentation as a protein-upgrade and digestibility layer
+ microalgae as optional supplement
+ insects only behind ethics / safety / consent gates
+ hydrogen or microbial protein as future federation-scale infrastructure
+ amino acid modeling
+ digestibility modeling
+ input tracking
+ resident acceptance checks
+ food safety gates
```

The goal is not total isolation from all external inputs.

The goal is:

```text
no external protein dependency
minimal external nutrient dependency
no factory-farming dependency
no conventional livestock dependency
no single-source protein dependency
```

---

## 2. Guiding Sentence

> Build a protein ecology, not a protein monoculture.

A resilient protein system should have multiple overlapping sources that complement each other nutritionally, operationally, ethically, and culturally.

---

## 3. Strategic Decision

The best v1 path is:

```text
legumes + soy/equivalent complete plant protein + duckweed/water lentils + fermentation
```

```yaml
protein_commons_strategy:
  baseline:
    - legumes
    - soy_or_equivalent_complete_plant_protein
    - grains_and_seeds_for_diet_level_completeness
    - fermentation_for_digestibility_flavor_and_protein_upgrade

  preferred_novel_layer:
    - duckweed_water_lentils

  optional_supplement_layer:
    - microalgae

  optional_ethics_gated_layer:
    - edible_insects

  future_federation_layer:
    - hydrogen_oxidizing_bacterial_protein
    - precision_fermentation
    - other_microbial_protein_platforms

  avoid_as_default:
    - factory_farming
    - conventional_livestock_dependency
    - single_protein_dependency
    - insect_farming_without_resident_consent
    - high_tech_bioreactors_without_trained_operators
    - algae_or_duckweed_systems_without_contamination_controls
    - external_feedstock_dependency_without_modeling
    - protein_systems_residents_will_not_eat
```

---

## 4. Protein Target

The app should model protein at both population level and profile level.

```yaml
protein_target:
  adult_minimum_reference:
    protein: 0.8
    unit: grams_per_kg_body_weight_per_day

  planning_buffer:
    default: 20-40_percent_above_minimum

  higher_need_profiles:
    - elders
    - children_youth
    - pregnancy_lactation
    - illness_recovery
    - injury_recovery
    - heavy_labor
    - athletic_residents
    - residents_with_clinically_defined_needs
```

### 80-Resident Rough Planning Example

```text
Assume 70 kg average adult body weight.

0.8 g/kg/day = 56 g protein/person/day

80 residents:
  4.48 kg protein/day
  ~1.64 metric tons protein/year

With resilience / profile buffer:
  plan around 2.0-2.5 metric tons protein/year
```

This is a planning frame only. Actual modeling should account for household mix, age, health status, digestibility, and dietary pattern.

---

## 5. Complete Protein Principle

The app should optimize for **diet-level amino acid sufficiency**, not necessarily every single food being complete.

```yaml
complete_protein_model:
  required:
    - essential_amino_acid_targets
    - protein_quantity
    - digestibility_factor
    - dietary_pairing
    - resident_profile_adjustment
    - weekly_menu_basis
    - fallback_menu
    - cultural_food_flexibility

  allowed_patterns:
    single_complete_sources:
      - soy
      - duckweed_water_lentils_where_validated
      - mycoprotein_where_validated
      - microalgae_where_validated
      - insect_protein_where_approved_and_accepted

    diet_level_combinations:
      - legumes_plus_grains
      - beans_plus_corn
      - lentils_plus_wheat_or_rice
      - chickpeas_plus_sesame
      - peas_plus_oats
      - seeds_plus_legumes
```

> Completeness belongs to the diet, not necessarily to every bite.

---

## 6. Recommended Protein Stack

### Layer 1: Staple Plant Protein

```yaml
layer_1_staple_plant_protein:
  status: required

  sources:
    - soybeans
    - tofu
    - tempeh
    - lentils
    - chickpeas
    - dry_beans
    - field_peas
    - peanuts
    - sunflower_seeds
    - pumpkin_seeds
    - hemp_seeds_where_legal_and_available
    - oats
    - wheat
    - corn
    - rice_where_regionally_appropriate

  role:
    - baseline_protein
    - calories
    - fiber
    - pantry_stability
    - low_tech_storage
    - cultural_menu_flexibility

  app_requirements:
    - protein_quantity_model
    - amino_acid_pairing
    - storage_capacity
    - cooking_labor_model
    - allergen_controls
    - cultural_menu_variants
```

### Layer 2: Duckweed / Water Lentils

```yaml
layer_2_duckweed_water_lentils:
  status: preferred_v1_novel_layer

  examples:
    - Wolffia_species
    - Lemna_species
    - Mankai_type_water_lentils_where_available_and_legal

  role:
    - high_efficiency_fresh_green_protein
    - micronutrient_support
    - greenhouse_or_controlled_aquatic_production
    - resilience_against_land_crop_failure
    - local_protein_production

  strengths:
    - very_fast_growth
    - low_land_footprint
    - frequent_harvest
    - potentially_complete_amino_acid_profile
    - plant_based
    - no_animal_sentience_issue
    - compatible_with_controlled_environment_or_greenhouse_logic

  risks:
    - water_quality_control_required
    - heavy_metal_or_contaminant_accumulation
    - microbial_contamination
    - species_and_strain_variability
    - digestibility_variability
    - taste_and_texture_acceptance
    - regulatory_uncertainty
    - trained_operator_need

  app_requirements:
    - food_safe_water_source
    - controlled_growing_conditions
    - water_quality_testing
    - contamination_testing
    - harvest_protocol
    - drying_or_storage_protocol
    - menu_acceptance_testing
    - operator_training
    - backup_operator
    - regulatory_review_flag
```

### Layer 3: Fermentation Protein

```yaml
layer_3_fermentation_protein:
  status: preferred_v1_or_v2

  low_complexity:
    - tempeh
    - koji
    - miso
    - fermented_legume_products
    - fermented_grain_legume_pastes

  advanced_or_v2:
    - mycoprotein_style_fungal_biomass
    - controlled_substrate_fermentation
    - single_cell_protein_from_safe_feedstocks

  role:
    - improve_digestibility
    - diversify_flavor
    - upgrade_carbohydrate_or_legume_feedstocks
    - create_high_protein_foods_without_livestock
    - preserve_and_transform_surplus

  app_requirements:
    - approved_cultures_or_strains
    - feedstock_model
    - contamination_controls
    - batch_logs
    - temperature_and_time_controls
    - discard_rules
    - food_safety_training
    - operator_backup
    - professional_review_for_advanced_systems
```

### Layer 4: Microalgae Supplement

```yaml
layer_4_microalgae_supplement:
  status: optional_supplement

  examples:
    - spirulina
    - chlorella
    - other_approved_food_microalgae

  role:
    - protein_supplement
    - micronutrient_supplement
    - emergency_powder_or_fortification
    - smoothie_soup_sauce_addition

  best_use:
    - 5-15_percent_of_protein
    - emergency_shelf_stable_powder
    - fortification

  app_requirements:
    - use_as_supplement_not_staple_by_default
    - contaminant_testing
    - sourcing_or_production_review
    - serving_acceptance
    - allergen_or_intolerance_tracking
```

### Layer 5: Insect Protein

```yaml
layer_5_insect_protein:
  status: optional_ethics_safety_consent_gate

  examples:
    - crickets
    - mealworms
    - black_soldier_fly_larvae_for_feed_or_waste_processing
    - other_legally_approved_edible_insects

  role:
    - optional_human_protein
    - circular_waste_conversion
    - animal_feed_for_non-livestock_systems_where_allowed
    - fertilizer_frass_stream_where_safe

  allowed_only_if:
    - residents_explicitly_consent
    - legal_for_human_food_or_feed_use
    - feedstock_source_safe_and_legal
    - allergen_controls_present
    - processing_controls_present
    - containment_plan_present
    - ethics_review_completed
    - opt_out_food_autonomy_preserved

  app_default:
    human_food: false
    animal_feed_or_waste_processing: optional_reviewed
```

### Layer 6: Hydrogen / Microbial Protein

```yaml
layer_6_hydrogen_microbial_protein:
  status: future_federation_module

  examples:
    - hydrogen_oxidizing_bacterial_protein
    - power_to_protein
    - CO2_plus_hydrogen_plus_mineral_media_microbes
    - precision_fermentation_platforms

  role:
    - future_climate_independent_protein
    - regional_or_federation_scale_resilience
    - low_land_use_protein
    - crop_failure_backup

  app_default:
    village_block_dependency: false
    federation_research_track: true
```

---

## 7. Protein Commons Architecture

```yaml
ProteinCommons:
  facilities:
    staple_pantry:
      required: true
      role:
        - dry_legume_storage
        - grain_storage
        - seed_storage
        - soy_storage
        - emergency_protein_buffer

    protein_prep_kitchen:
      required: true
      role:
        - soaking
        - cooking
        - pressure_cooking
        - tofu_or_tempeh_prep_where_enabled
        - batch_cooking
        - allergen_separation

    fermentation_space:
      preferred: true
      role:
        - tempeh
        - koji
        - safe_controlled_fermentation
        - batch_logging
        - culture_storage

    duckweed_greenhouse_or_water_lentil_room:
      preferred_v1: true
      role:
        - controlled_aquatic_plant_production
        - harvest
        - rinse
        - drying_or_chilling
        - quality_control

    microalgae_corner:
      optional: true

    insect_unit:
      optional_ethics_gate: true
```

---

## 8. Input and Nutrient Loop Requirements

A local protein system is only honest if it tracks inputs.

```yaml
input_loop_requirements:
  required_inputs_to_track:
    - water
    - energy
    - nitrogen
    - phosphorus
    - potassium
    - trace_minerals
    - salt
    - carbon_or_carbohydrate_feedstock
    - starter_cultures
    - seeds_or_strains
    - cleaning_supplies
    - containers
    - testing_supplies
    - labor
    - equipment_replacement

  fail_if:
    - protein_system_claims_self_sufficiency_without_input_model
    - nutrient_depletion_unmodeled
    - feedstock_dependency_hidden
    - waste_or_byproduct_path_unknown
```

> A protein system is not self-sufficient if it hides its minerals, cultures, feedstocks, or testing supplies.

---

## 9. Ethics Requirements

```yaml
ethics_requirements:
  required:
    - no_factory_farming_dependency
    - no_conventional_livestock_dependency_as_baseline
    - animal_adjacent_sources_disclosed
    - resident_consent_for_insect_layer
    - opt_out_food_autonomy
    - sentience_uncertainty_acknowledged
    - no_coercive_food_norms
    - cultural_and_religious_food_respect

  fail_if:
    - animal_or_insect_layer_added_by_default_without_consent
    - residents_cannot_avoid_ethically_contested_food
    - food_choice_becomes_social_or_moral_surveillance
```

---

## 10. Safety Requirements

```yaml
safety_requirements:
  staple_legumes:
    controls:
      - dry_storage
      - pest_control
      - allergen_labeling
      - cooking_safety

  soy:
    controls:
      - allergen_controls
      - batch_labeling
      - fermentation_controls_where_tempeh_or_miso
      - storage_temperature

  duckweed_water_lentils:
    controls:
      - food_grade_water_source
      - contaminant_testing
      - microbial_testing_or_review
      - heavy_metal_review
      - species_identification
      - clean_harvest_protocol
      - rinse_protocol
      - storage_protocol
      - discard_rules

  fermentation:
    controls:
      - approved_cultures
      - time_temperature_controls
      - contamination_detection
      - batch_logs
      - discard_rules
      - trained_operator

  microalgae:
    controls:
      - culture_purity
      - water_quality
      - toxin_contamination_review
      - drying_storage

  insects:
    controls:
      - approved_species
      - approved_feedstock
      - containment
      - allergen_labeling
      - kill_processing_protocol
      - storage
      - pest_escape_prevention
      - legal_review

  fail_if:
    - no_food_safety_lead
    - no_batch_logs_for_fermentation_or_aquatic_production
    - no_testing_plan_for_aquatic_protein
    - no_allergen_controls
    - no_discard_rules
```

---

## 11. Labor Requirements

```yaml
labor_requirements:
  labor_categories:
    - staple_soaking_cooking
    - tofu_or_tempeh_production
    - fermentation_batch_prep
    - culture_maintenance
    - duckweed_harvest
    - duckweed_water_testing
    - drying_or_preservation
    - algae_maintenance
    - insect_unit_care_where_enabled
    - cleaning
    - batch_logging
    - menu_integration
    - operator_training

  required_metrics:
    protein_labor_hours_per_week: number
    protein_labor_hours_per_kg_protein: number
    specialist_hours_per_week: number
    operator_backup_count: number
    unpleasant_or_repetitive_labor_score: number
    hidden_labor_risk: low | medium | high

  fail_if:
    - novel_protein_layer_has_no_trained_backup
    - labor_burden_untracked
    - savings_depend_on_unpaid_hidden_labor
```

> A protein system is not liberating if it turns residents into unpaid bioreactor attendants.

---

## 12. Acceptance and Menu Integration

```yaml
acceptance_requirements:
  required:
    - resident_taste_testing
    - menu_integration
    - cultural_food_variants
    - opt_out_options
    - texture_and_flavor_review
    - children_elder_acceptance_review_where_relevant
    - allergy_intolerance_tracking
    - recipe_library

  fail_if:
    - protein_plan_is_nutritionally_valid_but_unacceptable_to_residents
    - novel_protein_source_hidden_in_food_without_disclosure
    - opt_out_unavailable
```

> Dignity includes wanting to eat the food.

---

## 13. Storage and Buffer Requirements

```yaml
protein_storage:
  required:
    - dry_legume_storage
    - dry_grain_storage
    - seed_or_nut_storage
    - soy_storage_or_procurement
    - preserved_protein_buffer
    - emergency_protein_menu
    - allergen_separation
    - pest_control
    - FIFO_rotation

  preferred:
    - dried_duckweed_powder
    - fermented_shelf_stable_products
    - frozen_tempeh_or_tofu
    - dehydrated_legume_meals
    - microalgae_powder
    - textured_plant_protein_where_acceptable

  targets:
    minimum_protein_buffer_days: 30
    preferred_protein_buffer_days: 90

  fail_if:
    - emergency_food_buffer_lacks_protein_floor
    - protein_storage_untracked
    - allergen_separation_absent
    - no_rotation_plan
```

---

## 14. Scenarios

```yaml
protein_commons_scenarios:
  normal_year:
    tests:
      - protein_quantity
      - amino_acid_coverage
      - labor
      - acceptance
      - cost
      - storage_rotation

  crop_failure:
    tests:
      - legume_shortfall
      - duckweed_continuity
      - fermentation_feedstock
      - emergency_buffer
      - menu_substitution

  duckweed_contamination:
    tests:
      - detection
      - harvest_shutdown
      - alternate_protein
      - water_system_review
      - discard_and_restart
      - resident_communication

  fermentation_contamination:
    tests:
      - batch_discard
      - traceability
      - operator_review
      - menu_substitution
      - training_update

  energy_outage:
    tests:
      - fermentation_temperature
      - cold_storage
      - drying
      - aquatic_system_pumps
      - emergency_protein_menu

  water_shortage:
    tests:
      - duckweed_reduction
      - cleaning_constraints
      - staple_shift
      - drought_menu

  operator_exit:
    tests:
      - backup_training
      - documentation
      - system_pause
      - external_support

  resident_acceptance_failure:
    tests:
      - menu_redesign
      - opt_out_demand
      - labor_cost_of_alternatives
      - cultural_food_review

  insect_ethics_dispute:
    tests:
      - consent_process
      - opt_out
      - separate_processing
      - governance_review
      - continuation_or_shutdown

  external_protein_cutoff:
    tests:
      - local_production_capacity
      - protein_buffer_days
      - amino_acid_coverage
      - high_need_profiles
      - rationing_without_dignity_loss
```

---

## 15. Protein Commons Gates

```yaml
protein_commons_gates:
  protein_quantity_gate:
    fail_if:
      - daily_protein_target_not_met
      - yearly_protein_capacity_below_population_need
      - high_need_profiles_unmodeled

  amino_acid_gate:
    fail_if:
      - essential_amino_acid_targets_not_met
      - diet_level_completeness_unmodeled
      - digestibility_unmodeled

  dependency_gate:
    fail_if:
      - one_source_dependency
      - external_protein_dependency_unmodeled
      - external_feedstock_dependency_unmodeled
      - nutrient_inputs_untracked

  ethics_gate:
    fail_if:
      - factory_farming_dependency
      - conventional_livestock_dependency_as_baseline
      - insect_layer_without_consent
      - animal_or_insect_source_hidden_from_residents

  safety_gate:
    fail_if:
      - duckweed_water_quality_uncontrolled
      - fermentation_controls_absent
      - insect_feedstock_unreviewed
      - algae_contamination_unreviewed
      - no_allergen_controls
      - no_batch_logs_for_high_risk_production

  labor_gate:
    fail_if:
      - protein_labor_untracked
      - technical_layer_has_no_trained_backup
      - savings_depend_on_hidden_labor
      - daily_specialist_attention_required_without_paid_or_rotated_role

  acceptance_gate:
    fail_if:
      - resident_acceptance_unmodeled
      - opt_out_unavailable
      - menu_lacks_cultural_flexibility
      - novel_protein_hidden_in_food

  resilience_gate:
    fail_if:
      - protein_buffer_below_minimum
      - no_emergency_protein_menu
      - contamination_event_has_no_substitution_plan
      - crop_failure_breaks_protein_floor

  complexity_gate:
    warn_if:
      - too_many_novel_layers_enabled_at_once
      - bioreactor_or_aquatic_system_exceeds_operator_capacity
      - equipment_vendor_lock_in
      - food_safety_burden_exceeds_labor_target
```

---

## 16. Data Model

```yaml
ProteinCommons:
  id: string
  population_served: integer

  targets:
    protein_grams_per_person_per_day: number
    total_protein_kg_per_day: number
    total_protein_kg_per_year: number
    planning_buffer_percent: number
    high_need_profiles_modeled: boolean

  source_mix:
    legumes_percent: number
    soy_percent: number
    grains_seeds_percent: number
    duckweed_percent: number
    fermentation_percent: number
    microalgae_percent: number
    insect_percent: number
    microbial_future_percent: number
    external_protein_percent: number

  amino_acids:
    essential_amino_acid_targets_met: boolean
    digestibility_adjusted: boolean
    limiting_amino_acid: string
    weekly_menu_complete: boolean
    emergency_menu_complete: boolean

  production_systems:
    staple_pantry: boolean
    soy_processing: boolean
    duckweed_system: boolean
    fermentation_system: boolean
    microalgae_system: boolean
    insect_system: boolean
    future_microbial_system: boolean

  inputs:
    water_liters_per_kg_protein: number
    energy_kWh_per_kg_protein: number
    land_m2_per_kg_protein: number
    external_feedstock_dependency: boolean
    mineral_input_dependency: boolean
    nutrient_loop_status: pass | warn | fail

  safety:
    food_safety_lead: string
    backup_food_safety_lead: string
    batch_logs: boolean
    allergen_controls: boolean
    duckweed_water_testing: boolean
    fermentation_controls: boolean
    insect_ethics_and_safety_review: boolean
    contamination_response_plan: boolean

  labor:
    protein_labor_hours_per_week: number
    protein_labor_hours_per_kg_protein: number
    trained_operators: integer
    backup_operators: integer
    hidden_labor_risk: low | medium | high

  acceptance:
    resident_acceptance_score: number
    opt_out_available: boolean
    cultural_menu_variants: boolean
    taste_testing_complete: boolean
    novel_protein_disclosure: boolean

  storage:
    protein_buffer_days: number
    dry_protein_storage_days: number
    preserved_protein_storage_days: number
    emergency_protein_menu: boolean
    FIFO_rotation: boolean

  outputs:
    protein_security_status: pass | warn | fail
    amino_acid_status: pass | warn | fail
    ethics_status: pass | warn | fail
    safety_status: pass | warn | fail
    labor_status: pass | warn | fail
    acceptance_status: pass | warn | fail
    resilience_status: pass | warn | fail
    complexity_score: number
    life_burden_reduction_score: number
```

---

## 17. Required App Outputs

```yaml
required_outputs:
  - protein_commons_summary
  - protein_target_report
  - amino_acid_coverage_report
  - source_mix_report
  - local_protein_capacity_report
  - input_dependency_report
  - duckweed_water_lentil_feasibility_report
  - fermentation_feasibility_report
  - microalgae_supplement_report
  - insect_ethics_safety_consent_report
  - future_microbial_protein_report
  - protein_storage_buffer_report
  - labor_burden_report
  - food_safety_controls_report
  - resident_acceptance_report
  - emergency_protein_menu
  - scenario_failure_report
  - professional_review_requirements
  - visualization_bundle_metadata
```

---

## 18. Visualization Requirements

```yaml
visualization_requirements:
  spatial_objects:
    - staple_pantry
    - protein_prep_kitchen
    - fermentation_space
    - duckweed_water_lentil_system
    - microalgae_unit
    - insect_unit_if_enabled
    - protein_storage
    - testing_station
    - batch_log_station

  overlays:
    - protein_source_mix
    - protein_buffer_days
    - amino_acid_status
    - input_dependency
    - contamination_risk
    - labor_burden
    - acceptance_score
    - ethics_gate_status
    - emergency_menu_status

  scenario_playback:
    - normal_year
    - crop_failure
    - duckweed_contamination
    - fermentation_contamination
    - energy_outage
    - water_shortage
    - operator_exit
    - resident_acceptance_failure
    - insect_ethics_dispute
    - external_protein_cutoff
```

---

## 19. Recommended v1 Implementation Path

The recommended first implementation should not enable every layer.

```yaml
v1_recommended_path:
  enable:
    - staple_legumes
    - soy_or_equivalent_complete_plant_protein
    - grain_seed_pairing
    - tempeh_or_low_complexity_fermentation
    - duckweed_water_lentil_feasibility_model
    - protein_buffer_tracking

  model_but_do_not_require:
    - microalgae
    - mycoprotein
    - insects
    - hydrogen_microbial_protein

  prohibit_as_dependency:
    - future_microbial_protein
    - insect_protein
    - advanced_bioreactors
    - any_unreviewed_novel_protein_system

  first_real_test:
    question: Can 80 residents meet protein and essential amino acid needs for one year with no external protein purchases after initial setup?
    conditions:
      - legume_crop_reduction_30_percent
      - duckweed_system_operational_70_percent_of_year
      - fermentation_system_operational
      - 30_day_protein_buffer
      - high_need_profiles_included
      - resident_acceptance_above_threshold
      - labor_within_target
```

---

## 20. Design Maxims

```text
Do not search for one perfect protein.

Do not confuse protein independence with food independence.

Do not hide mineral or feedstock inputs.

Do not make residents eat insects by default.

Do not make ethical uncertainty disappear through efficiency math.

Do not let novel protein become hidden technical labor.

Do not let a bioreactor become a new boss.

Do not rely on a protein people will not eat.

Do not claim complete protein without amino acid and digestibility modeling.

Do not claim self-sufficiency without input loops.

Use legumes for the floor.

Use duckweed for the novel plant layer.

Use fermentation to transform and upgrade staples.

Use algae as supplement, not savior.

Use insects only with consent and review.

Use microbial protein as future federation infrastructure.

Make the protein stack diverse enough to fail gracefully.
```

---

## 21. Open Questions for Iteration

```text
1. Should duckweed / water lentils be promoted from preferred v1 to required feasibility study?
2. Should soy be required as the complete plant baseline, or should the app support soy-free profiles?
3. What resident acceptance threshold is high enough for a novel protein source?
4. Should insect protein be included only as feed / waste processing, or also human food if residents consent?
5. What protein buffer target is appropriate: 30 days, 60 days, or 90 days?
6. Should the app model B12, iron, zinc, omega-3, and calcium alongside protein in this supplement?
7. Should mycoprotein be treated as v1 low-scale pilot or v2 advanced fermentation?
8. What input-dependency threshold invalidates a local protein claim?
9. Should the app require dietitian review for protein profiles serving children, elders, pregnancy, or illness recovery?
10. What protein-system failure makes the Food Module invalid rather than merely improvable?
```

---

## 22. Source Notes

The research basis for this supplement includes:

- Dietary Reference Intake protein targets and essential amino acid scoring patterns.
- Legume sustainability and protein research.
- Duckweed / water lentil research on protein content, essential amino acid profiles, fast growth, and contamination concerns.
- Research on Mankai / Wolffia and micronutrient potential.
- Mycoprotein and fungal fermentation research.
- Microalgae protein research, including spirulina and chlorella.
- FAO and regulatory resources on edible insects.
- Emerging research on hydrogen-oxidizing bacteria, microbial protein, and power-to-protein systems.
- Food safety principles for fermentation, aquatic food production, allergen control, and batch traceability.
