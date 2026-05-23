# CIaC Food Module: Hybrid Food Commons

**Module ID:** `food.hybrid_food_commons.v0_1`  
**Status:** Draft requirement module  
**Purpose:** Define the default food system for a scalable Minimum Viable Dignified Infrastructure complex.  
**Primary design question:** What food infrastructure best reduces cost, daily labor, fragility, and isolation while preserving dignity, nutrition, pleasure, autonomy, and resilience?

---

## 1. Core Thesis

The CIaC food baseline should **not** be total self-sufficiency.

Total food self-sufficiency is seductive but misleading. It can overburden residents, exaggerate land productivity, require specialized farming knowledge, fail under bad weather, and turn a dignified life project into a labor-intensive farm project.

The recommended baseline is a **Hybrid Food Commons**:

```text
shared kitchen and dining
+ private food autonomy
+ bulk staple purchasing
+ regional farm / CSA / food hub relationships
+ onsite high-value fresh food production
+ greenhouse or high tunnel season extension
+ dry / cold / root storage
+ preservation kitchen
+ nutrition-aware meal planning
+ food safety procedures
+ waste reduction and compost loop
+ emergency food buffer
```

The goal is to reduce food dependency, not pretend the settlement is an island.

The food system should make healthy, satisfying food easier and cheaper while preserving choice.

---

## 2. Guiding Sentence

> Grow what returns dignity, buy what returns time, preserve what returns resilience, and share meals without making togetherness mandatory.

---

## 3. Strategic Decision

The best default model is:

# A shared food commons that produces fresh abundance onsite but sources staple calories regionally.

This means:

```yaml
food_strategy:
  onsite_priority:
    - herbs
    - greens
    - vegetables
    - fruit
    - eggs_if_low_burden_and_legal
    - culturally meaningful crops
    - therapeutic gardens
    - educational gardens

  regional_procurement_priority:
    - grains
    - legumes
    - oils
    - dairy_if_used
    - meat_if_used
    - bulk pantry staples
    - backup produce
    - preserved goods

  avoid_as_default:
    - total_self_sufficiency_claims
    - high_tech_vertical_farming
    - energy_intensive_hydroponics_as_baseline
    - resident_labor_intensive_farming_as_hidden_tax
    - mandatory_communal_meals
    - no_private_food_autonomy
```

### Rationale

Calories are easier and cheaper to buy in bulk than to grow at small scale.

Freshness, beauty, health, education, and community are where onsite production excels.

The food commons should therefore use onsite production for what is most humanly valuable, not for heroic calorie independence.

---

## 4. Research Anchors

This module is grounded in the following research and precedent categories.

### 4.1 Nutrition baseline

The Dietary Guidelines for Americans are the federal nutrition cornerstone for food-based recommendations, diet-related chronic disease prevention, and nutrient needs. The 2025-2030 edition emphasizes whole, healthy, nutritious foods and limiting highly processed foods, added sugars, and refined carbohydrates.

**Design implication:** The food module should optimize for simple, whole-food dietary patterns rather than specialty diets, supplements, or food-tech novelty.

### 4.2 Food cost baseline

The USDA Food Plans provide monthly food-at-home cost benchmarks. Recent reports show that even the Thrifty Food Plan requires hundreds of dollars per adult per month, making food a meaningful part of the wage-dependency stack.

**Design implication:** The module should compare CIaC food costs against USDA food-plan baselines, not only against grocery receipts.

### 4.3 Food waste opportunity

USDA states that over one-third of all available food in the United States goes uneaten through loss or waste, and estimates food waste at 30-40% of the food supply.

**Design implication:** Waste reduction, inventory visibility, batch cooking, preservation, and planned leftovers are core infrastructure, not moral scolding.

### 4.4 Community meals precedent

Cohousing research suggests that communalizing meals has potential to reduce and rebalance household food labor. Common meals are also one of the core social practices in cohousing.

**Design implication:** Shared meals should be a default affordance because they reduce duplicated labor and create social glue. They should remain opt-in because mandatory meals can become coercive.

### 4.5 Community kitchen precedent

Community kitchens have been studied as public-health and food-security interventions that can reduce isolation, improve food access, and support social and nutritional wellbeing.

**Design implication:** A shared kitchen is not merely an amenity. It is a resilience engine, social condenser, and labor reducer.

### 4.6 Regional food resilience

USDA local and regional food system resources include food hubs, CSA models, local sourcing, shared kitchens, and resilience playbooks.

**Design implication:** The food commons should connect to local and regional food systems instead of attempting isolation.

### 4.7 CSA risk-sharing model

USDA describes Community Supported Agriculture as a model where a community pledges support to a farm operation, with growers and consumers sharing risks and benefits.

**Design implication:** CIaC should not own every food-production function. It can create long-term procurement relationships that share risk with nearby growers.

### 4.8 Food preservation safety

USDA / National Center for Home Food Preservation resources document canning, freezing, drying, pickling, and other preservation methods.

**Design implication:** Preservation is essential, but it must be handled through validated procedures and food-safety training.

### 4.9 Food safety

The FDA Food Code is the major reference model for retail and food-service safety, including date marking, time / temperature control, equipment, and illness-risk reduction.

**Design implication:** Any shared kitchen must include food-safety logic, cleaning logs, allergen tracking, temperature logs, and local health-code review where applicable.

---

## 5. Recommended Scale

The food module should support the same first serious population as the housing module.

```yaml
population:
  minimum_meaningful_scale: 50
  ideal_first_model: 80
  upper_bound_before_replication: 150
```

### Scale Logic

```text
Below 50:
  shared meals and bulk buying help, but specialized food roles are fragile.

Around 80:
  common kitchen, storage, garden, procurement, preservation, and role backup become realistic.

Above 150:
  food operations risk becoming institutional unless split into multiple food pods or meal houses.
```

### Scaling Method

Use multiple food commons nodes rather than one endlessly growing cafeteria.

```yaml
scaling:
  50-100_residents:
    food_nodes: 1
    common_kitchen: 1
    garden_team: 1
    procurement_team: 1

  100-150_residents:
    food_nodes: 1_primary_plus_1_secondary
    common_kitchen: 1
    satellite_pantry_or_pod_kitchen: optional

  above_150_residents:
    recommendation: replicate_village_block
    reason: avoid_institutional_food_system
```

---

## 6. Default Prototype

```yaml
default_prototype:
  name: hybrid_food_commons_80
  residents: 80

  core_facilities:
    - common_kitchen
    - common_dining
    - dry_pantry
    - cold_storage
    - root_storage_or_cool_pantry
    - preservation_kitchen
    - greenhouse_or_high_tunnel
    - garden_beds
    - compost_area
    - delivery_and_wash_pack_zone
    - private_food_autonomy_in_units

  food_sourcing:
    onsite_fresh_produce_target: 40-70_percent_of_seasonal_fresh_produce
    onsite_calorie_target: 10-25_percent_of_total_calories
    regional_staple_target: 60-80_percent_of_total_calories
    emergency_buffer_target: 30_days_minimum
    preferred_resilience_buffer: 90_days_shelf_stable_staples

  common_meals:
    dinners_per_week: 3-5
    breakfasts_or_lunches: optional
    mandatory_participation: false
    private_meal_autonomy: required
```

---

## 7. The Best Solution: Food Commons Hub

The central implementation should be a **Food Commons Hub** attached to the common house.

It should combine five functions:

```text
1. Common kitchen and dining
2. Procurement and bulk pantry
3. Fresh food production and garden interface
4. Preservation and storage
5. Food safety and nutrition operations
```

### 7.1 Spatial Requirements

```yaml
food_commons_hub:
  required_zones:
    common_kitchen:
      purpose:
        - shared_meals
        - batch_cooking
        - emergency_meal_production
        - teaching
        - preservation_prep

    common_dining:
      purpose:
        - voluntary_shared_meals
        - social_glue
        - celebration
        - intergenerational_contact

    dry_pantry:
      purpose:
        - grains
        - legumes
        - oils
        - spices
        - shelf_stable_reserve
        - household_bulk_refill

    cold_storage:
      purpose:
        - perishables
        - dairy_if_used
        - prepared_foods
        - produce_buffer
        - medication_backup_if_needed

    root_storage_or_cool_pantry:
      purpose:
        - potatoes
        - onions
        - winter_squash
        - apples
        - fermented_foods_where_safe
        - low_energy_storage

    preservation_kitchen:
      purpose:
        - canning_where_safe
        - dehydration
        - freezing
        - pickling
        - fermentation_where_trained
        - value_added_foods

    wash_pack_zone:
      purpose:
        - garden_harvest_cleaning
        - sorting
        - weighing
        - distribution
        - dirty_clean_flow_separation

    compost_and_organics_zone:
      purpose:
        - food_scrap_recovery
        - soil_cycle
        - waste_reduction
```

### 7.2 Location Requirements

```yaml
location_requirements:
  adjacent_to:
    - common_house
    - dining_space
    - delivery_access
    - garden_path
    - compost_route

  separated_from:
    - sleeping_units_by_noise_buffer
    - sanitation_failure_risk
    - workshop_dust_and_chemical_zones

  must_have:
    - accessible_entry
    - service_entry
    - cleanable_surfaces
    - adequate_ventilation
    - pest_resistant_storage
    - emergency_power_for_cold_storage
```

---

## 8. Private Food Autonomy

Shared food infrastructure must not eliminate private food autonomy.

```yaml
private_food_autonomy:
  required:
    - residents_can_prepare_private_meals
    - residents_can_store_personal_food
    - residents_can_skip_common_meals
    - dietary_needs_are_respected
    - cultural_food_practices_are_supported
    - no_food_shaming
    - no_mandatory_communal_eating

  unit_level_minimum:
    - small_refrigeration_or_access_to_lockable_cold_storage
    - pantry_storage
    - tea_coffee_breakfast_capacity
    - ability_to_reheat_food
```

### Principle

```text
Shared meals should feel like relief, not surveillance.
```

---

## 9. Food Production Strategy

The food system should produce fresh, high-value, high-dignity foods onsite.

It should not try to grow all staple calories in the first model.

### 9.1 Onsite Production Priorities

```yaml
onsite_production:
  tier_1_required:
    - herbs
    - salad_greens
    - cooking_greens
    - tomatoes
    - peppers
    - cucumbers
    - beans
    - squash
    - carrots
    - onions_or_alliums
    - berries_where_climate_allows

  tier_2_preferred:
    - fruit_trees
    - perennial_herbs
    - edible_landscape
    - medicinal_or_tea_garden_where_safe
    - mushroom_growing_if_trained
    - greenhouse_seedlings

  tier_3_optional:
    - eggs
    - aquaponics
    - hydroponics
    - small_grain_trial
    - staple_crop_field
    - animal_protein_systems
```

### 9.2 Production Systems

```yaml
production_systems:
  default:
    - raised_or_in_ground_beds
    - greenhouse_or_high_tunnel
    - perennial_food_landscape
    - compost_supported_soil_building
    - rainwater_irrigation_where_legal_and_safe
    - drip_irrigation

  optional_after_proof:
    - controlled_environment_agriculture
    - aquaponics
    - larger_scale_orchard
    - mushroom_room
    - poultry_for_eggs
```

### 9.3 Why Greenhouse / High Tunnel Before Vertical Farm

A greenhouse or high tunnel extends seasons while remaining legible, repairable, and compatible with ordinary horticulture.

Vertical farming and highly automated hydroponics can be useful in some contexts, but they increase energy, maintenance, parts, monitoring, and technical skill burden.

```yaml
controlled_environment_gate:
  reject_as_default_if:
    - requires_high_energy_input
    - requires_specialized_vendor_parts
    - requires_daily_technical_monitoring
    - produces_low_calorie_output
    - has_unclear_labor_savings
    - creates_fragile_dependency
```

---

## 10. Procurement Strategy

The food commons should use regional relationships for staples and resilience.

```yaml
procurement_strategy:
  required_channels:
    - bulk_wholesale_or_cooperative_purchasing
    - local_or_regional_farms
    - CSA_or_direct_farm_contracts
    - food_hub_where_available
    - emergency_retail_fallback

  staple_categories:
    - grains
    - legumes
    - oils
    - flour
    - oats
    - rice
    - pasta
    - canned_tomatoes
    - nut_butters_or_seed_butters
    - shelf_stable_proteins
    - spices
    - salt
    - sugar_or_sweetener
    - coffee_tea_if_desired

  perishables:
    - dairy_if_used
    - eggs
    - meat_if_used
    - fresh_fruit
    - fresh_vegetables
```

### Procurement Principle

```text
Do not ask a small settlement to do what regional agriculture already does well.
```

The app should model **dependency diversity**, not purity.

```yaml
dependency_diversity:
  max_single_supplier_share:
    normal_target: 40_percent
    warning_threshold: 60_percent
    fail_threshold: 80_percent

  required_fallbacks:
    - at_least_two_staple_suppliers
    - at_least_one_emergency_retail_supplier
    - at_least_one_regional_farm_relationship
    - shelf_stable_buffer
```

---

## 11. Meal System

Shared meals are one of the food module's highest-leverage patterns.

They reduce duplicated cooking labor, reduce food waste, improve social continuity, and support care during illness or stress.

But they must remain voluntary.

```yaml
common_meal_system:
  default_frequency:
    common_dinners_per_week: 3-5
    common_breakfasts_per_week: 0-2
    common_lunches_per_week: 0-2

  participation:
    mandatory: false
    opt_in: true
    opt_out: always_allowed

  labor_model:
    rotating_cook_teams: true
    paid_or_creditable_food_work: allowed
    invisible_care_labor_counted: required
    gendered_labor_detection: required

  meal_design:
    whole_food_baseline: true
    plant_forward_default: true
    omnivore_compatible: true
    allergies_tracked: true
    cultural_variation_supported: true
    leftovers_planned: true
```

### Meal Roles

```yaml
meal_roles:
  meal_planner:
    tasks:
      - menu_plan
      - dietary_constraints
      - inventory_use
      - budget_tracking

  cook_team:
    tasks:
      - prep
      - cooking
      - service

  cleanup_team:
    tasks:
      - dishes
      - sanitation
      - leftovers
      - compost_sorting

  food_safety_lead:
    tasks:
      - temperature_logs
      - allergen_tracking
      - date_marking
      - illness_exclusion
      - cleaning_checklists
```

---

## 12. Nutrition Standard

The food module should support health without becoming paternalistic.

```yaml
nutrition_standard:
  baseline:
    - whole_food_pattern
    - vegetables_daily
    - fruits_daily
    - adequate_protein
    - adequate_fiber
    - adequate_calories
    - culturally_flexible_meals
    - low_ultra_processed_default

  avoid:
    - mandatory_diet_ideology
    - moralizing_food_choices
    - one_size_fits_all_meal_plan
    - medical_diet_claims_without_professional_review

  must_support:
    - allergies
    - diabetes_or_cardiometabolic_needs_where_declared
    - vegetarian
    - vegan
    - religious_restrictions
    - sensory_needs
    - eating_disorder_sensitivity
```

### App Boundary

The app may plan meals against nutrition baselines.

The app must not claim to provide medical nutrition therapy unless reviewed by qualified professionals.

---

## 13. Storage and Resilience

Storage is the heart of food resilience.

A beautiful garden without storage is fragile.

```yaml
food_storage:
  minimum_buffer:
    shelf_stable_days: 30
    cold_fresh_days: 7
    emergency_water_for_food_prep_days: defined_by_water_module

  preferred_buffer:
    shelf_stable_days: 90
    cold_fresh_days: 14
    preserved_seasonal_food_days: 30-60

  storage_types:
    dry_pantry:
      required: true
      examples:
        - grains
        - legumes
        - oils
        - canned_goods
        - spices

    cold_storage:
      required: true
      emergency_power: required
      examples:
        - produce
        - dairy_if_used
        - prepared_meals
        - perishables

    freezer_storage:
      preferred: true
      emergency_power: preferred
      examples:
        - preserved_produce
        - prepared_meals
        - meat_if_used
        - bread

    root_storage:
      preferred: true
      examples:
        - potatoes
        - onions
        - squash
        - apples
        - carrots_where_suitable

    preserved_food_storage:
      required: true
      examples:
        - canned_foods
        - dehydrated_foods
        - fermented_foods_where_safe
```

### Storage Gate

```yaml
storage_gate:
  fail_if:
    - no_shelf_stable_buffer
    - no_food_inventory_visibility
    - no_pest_control_plan
    - no_allergen_separation_plan
    - no_cold_storage_backup_for_critical_foods

  warn_if:
    - less_than_30_days_shelf_stable_staples
    - cold_storage_depends_on_single_power_source
    - pantry_is_not_access_controlled
    - no_rotation_system
```

---

## 14. Preservation System

Preservation should reduce waste and bad-year fragility.

It must not become unsafe folk practice.

```yaml
preservation_system:
  methods:
    low_complexity:
      - freezing
      - dehydration
      - refrigerator_pickling
      - meal_batch_freezing
      - dry_storage

    medium_complexity:
      - water_bath_canning_for_approved_foods
      - pressure_canning_for_approved_foods
      - fermentation_with_training
      - root_cellaring

    advanced_or_review_required:
      - meat_curing
      - dairy_processing
      - shelf_stable_low_acid_foods
      - commercial_sale_of_preserved_goods

  required_controls:
    - validated_recipes
    - batch_logs
    - date_marking
    - storage_conditions
    - spoilage_discard_rules
    - training_records
```

### Preservation Principle

```text
Preservation is infrastructure only when it is safe, repeatable, documented, and not dependent on one expert.
```

---

## 15. Food Safety Requirements

The food commons should adopt food-service safety practices even when not legally classified as a public restaurant.

```yaml
food_safety:
  required:
    - handwashing_stations
    - cleaning_and_sanitizing_schedule
    - time_temperature_controls
    - date_marking
    - allergen_management
    - illness_exclusion_policy
    - pest_control
    - food_storage_separation
    - cooking_and_cooling_logs_for_shared_meals
    - local_health_department_review_where_required

  training:
    required_roles:
      - food_safety_lead
      - backup_food_safety_lead
    preferred_certifications:
      - food_handler_training
      - manager_level_food_safety_for_leads

  app_outputs:
    - cleaning_checklist
    - temperature_log_template
    - allergen_matrix
    - batch_log
    - local_review_required_flag
```

### Safety Boundary

The app must not certify food safety.

It should identify risks, required controls, and professional / regulatory review requirements.

---

## 16. Waste Reduction and Compost Loop

Food waste reduction is a core food commons function.

```yaml
waste_reduction:
  strategies:
    - inventory_visibility
    - expiration_alerts
    - first_in_first_out_storage
    - meal_planning_from_inventory
    - planned_leftovers
    - batch_cooking
    - preservation_of_surplus
    - donation_or_external_sharing_where_legal
    - composting_of_safe_organics

  app_metrics:
    food_waste_kg_per_week: number
    edible_food_waste_kg_per_week: number
    compostable_waste_kg_per_week: number
    avoided_purchase_value: number
    meals_recovered_from_surplus: number
```

### Compost Boundary

Compost belongs at the interface of the food module, sanitation/waste module, and soil module.

The food module should track scraps and organics.

The sanitation/waste module should govern compost safety and pathogen controls.

---

## 17. Labor and Time Model

The food module exists partly to return time to people.

It must count labor honestly.

```yaml
food_labor_model:
  labor_categories:
    - procurement
    - inventory
    - meal_planning
    - cooking
    - cleaning
    - gardening
    - harvesting
    - preservation
    - food_safety_logging
    - compost_handling
    - training
    - care_meals_for_ill_or_elder_residents

  required_metrics:
    total_food_labor_hours_per_week: number
    food_labor_hours_per_resident_per_week: number
    required_specialist_hours_per_week: number
    unpaid_care_food_labor_hours: number
    gender_or_role_imbalance_flag: boolean
    burnout_risk: low_medium_high
```

### Labor Rule

```text
Food infrastructure has failed if it reduces grocery bills by quietly increasing unpaid drudgery.
```

### Target

```yaml
labor_targets:
  common_food_labor_per_resident:
    target: 2-5_hours_per_week
    warning_above: 6_hours_per_week
    fail_above: 8_hours_per_week_unless_voluntary_or_paid

  specialist_dependency:
    fail_if:
      - no_backup_for_food_safety_lead
      - no_backup_for_procurement_lead
      - no_backup_for_garden_lead
```

---

## 18. Automation-Favoring Requirements

Automation should simplify the food commons. It should not turn the food system into a fragile technology stack.

```yaml
automation_requirements:
  inventory_system:
    required: true
    purpose:
      - stock_visibility
      - expiration_tracking
      - meal_planning
      - reserve_tracking

  meal_planning_engine:
    required: true
    purpose:
      - use_available_food
      - meet_nutrition_baseline
      - respect_dietary_constraints
      - reduce_waste
      - generate_shopping_lists

  procurement_planner:
    required: true
    purpose:
      - bulk_ordering
      - supplier_diversity
      - cost_tracking
      - seasonal_planning

  garden_planner:
    required: true
    purpose:
      - crop_calendar
      - harvest_forecast
      - seed_start_schedule
      - labor_forecast

  simple_sensor_layer:
    preferred: true
    purpose:
      - cold_storage_temperature
      - greenhouse_temperature
      - soil_moisture
      - irrigation_alerts

  preservation_logger:
    required: true
    purpose:
      - batch_tracking
      - date_marking
      - validated_process_notes
      - spoilage_prevention

  role_scheduler:
    required: true
    purpose:
      - cooking_rotations
      - cleaning_rotations
      - garden_work
      - fair_labor_distribution

  avoid:
    - black_box_food_AI
    - automatic_module_recommendation_without_life_burden_gate
    - complex_hydroponics_without_maintenance_model
    - vendor_locked_smart_kitchen_system
```

### Automation Principle

```text
Automate memory, planning, reminders, inventory, and forecasting before automating food production.
```

---

## 19. Scenario Simulations

The food module must support stress simulations.

```yaml
food_scenarios:
  normal_year:
    tests:
      - routine_meal_operations
      - garden_yield
      - procurement_cost
      - common_meal_frequency
      - waste_rate
      - resident_satisfaction

  crop_failure:
    tests:
      - onsite_produce_loss
      - replacement_cost
      - buffer_capacity
      - menu_substitution
      - labor_reallocation

  drought_year:
    tests:
      - irrigation_reduction
      - crop_priority
      - water_food_tradeoff
      - purchase_dependency

  supply_chain_disruption:
    tests:
      - staple_buffer_days
      - supplier_diversity
      - local_procurement_fallback
      - emergency_menu

  energy_outage:
    tests:
      - cold_storage_survival
      - freezer_loss_risk
      - emergency_power
      - shelf_stable_meal_plan

  illness_wave:
    tests:
      - reduced_cook_team_capacity
      - care_meal_demand
      - sanitation_protocol
      - delivery_to_units

  food_safety_incident:
    tests:
      - traceability
      - batch_recall
      - illness_exclusion
      - cleaning_reset
      - professional_review

  conflict_or_labor_dropout:
    tests:
      - role_backup
      - meal_frequency_reduction
      - paid_food_work_substitution
      - minimum_food_floor
```

---

## 20. Food Gates

The app should fail or warn based on food-system viability.

```yaml
food_gates:
  dignity_gate:
    fail_if:
      - no_private_food_autonomy
      - mandatory_shared_meals
      - dietary_needs_not_supported
      - no_accessible_food_access_for_disabled_or_elder_residents

  nutrition_gate:
    fail_if:
      - calorie_baseline_not_met
      - protein_baseline_not_met
      - no_plan_for_children_elders_or_medically_vulnerable_residents
      - meal_plan_is_punitive_or_austere

  resilience_gate:
    fail_if:
      - less_than_14_days_emergency_food
      - no_shelf_stable_staple_buffer
      - no_supplier_fallback
      - no_power_backup_for_critical_cold_storage

    warn_if:
      - less_than_30_days_shelf_stable_food
      - onsite_production_claim_exceeds_modeled_labor_capacity
      - crop_failure_has_no_replacement_plan

  labor_gate:
    fail_if:
      - food_labor_per_resident_exceeds_8_hours_per_week_by_default
      - critical_food_role_has_no_backup
      - common_meal_labor_is_untracked
      - care_meal_labor_is_untracked

    warn_if:
      - food_labor_per_resident_exceeds_6_hours_per_week
      - garden_operations_depend_on_one_person
      - food_safety_logging_depends_on_one_person

  safety_gate:
    fail_if:
      - no_food_safety_lead
      - no_temperature_logging_for_shared_meals
      - no_allergen_controls
      - no_cleaning_schedule
      - preservation_methods_are_unvalidated

  complexity_gate:
    warn_if:
      - high_tech_growing_system_has_no_maintenance_model
      - vendor_locked_food_technology
      - excessive_number_of_dietary_variants_without_labor_plan
      - too_many_supplier_contracts_for_available_admin_capacity

  waste_gate:
    warn_if:
      - food_waste_above_15_percent
      - no_inventory_system
      - no_leftover_plan
      - no_preservation_plan_for_surplus
```

---

## 21. App Modeling Boundary

The app should model food at the level of **pattern operations**, not culinary micromanagement.

### The App Should Model

```text
population demand
nutrition baseline
food cost baseline
source mix
procurement channels
storage capacity
emergency buffer days
meal frequency
labor burden
common meal schedules
garden area
crop categories
expected harvest ranges
seasonality
cold storage dependency
preservation capacity
food waste
supplier risk
food safety controls
simulation scenarios
```

### The App Should Not Claim to Solve by Default

```text
medical nutrition therapy
precise individual diet prescriptions
commercial kitchen licensing
restaurant certification
food business compliance
animal slaughter compliance
exact crop yield guarantees
exact soil fertility recommendations
complete self-sufficiency
```

### Principle

```text
The app should identify what must be true for food dignity and resilience.
Qualified humans and local authorities must validate health, safety, agricultural, and legal implementation.
```

---

## 22. Required Data Model

```yaml
FoodCommons:
  id: string
  population_served: integer
  sourcing:
    onsite_production_percent_calories: number
    onsite_production_percent_fresh_produce: number
    regional_procurement_percent_calories: number
    retail_fallback_percent: number
    supplier_count: integer
    largest_supplier_share_percent: number

  facilities:
    common_kitchen: boolean
    common_dining: boolean
    dry_pantry_capacity_days: number
    cold_storage_capacity_days: number
    freezer_capacity_days: number
    root_storage_capacity_days: number
    preservation_kitchen: boolean
    greenhouse_or_high_tunnel: boolean
    garden_area_m2: number
    compost_interface: boolean

  meals:
    common_meals_per_week: integer
    mandatory_meals: boolean
    private_food_autonomy: boolean
    dietary_constraint_count: integer
    allergen_controls: boolean

  nutrition:
    calorie_baseline_met: boolean
    protein_baseline_met: boolean
    fiber_baseline_met: boolean
    fresh_produce_servings_target_met: boolean
    child_elder_needs_modeled: boolean

  labor:
    total_food_labor_hours_per_week: number
    labor_hours_per_resident_per_week: number
    specialist_dependency_count: integer
    care_meal_hours_per_week: number
    unpaid_labor_imbalance_flag: boolean

  safety:
    food_safety_lead: string
    backup_food_safety_lead: string
    temperature_logs: boolean
    allergen_matrix: boolean
    cleaning_schedule: boolean
    preservation_validated: boolean
    local_review_required: boolean

  resilience:
    shelf_stable_buffer_days: number
    emergency_menu_available: boolean
    critical_cold_storage_backup_hours: number
    crop_failure_replacement_plan: boolean
    drought_food_plan: boolean
    energy_outage_food_plan: boolean

  outputs:
    monthly_food_cost_per_resident: number
    common_meal_cost_per_serving: number
    food_waste_percent: number
    dignity_score: number
    resilience_score: number
    life_burden_reduction_score: number
    complexity_score: number
```

---

## 23. Required App Outputs

```yaml
required_outputs:
  - food_system_summary
  - food_source_mix
  - nutrition_baseline_report
  - monthly_food_cost_estimate
  - labor_burden_report
  - common_meal_schedule
  - storage_capacity_report
  - emergency_food_buffer_days
  - supplier_dependency_report
  - garden_and_greenhouse_plan
  - preservation_capacity_report
  - food_safety_controls_report
  - waste_reduction_report
  - scenario_failure_report
  - role_backup_report
  - professional_review_requirements
  - visualization_bundle_metadata
```

---

## 24. Role Model

```yaml
food_roles:
  food_steward:
    purpose: overall food commons coordination
    required_backup: true

  procurement_steward:
    purpose: supplier relationships, bulk purchasing, budget tracking
    required_backup: true

  kitchen_steward:
    purpose: common meals, kitchen readiness, cook team coordination
    required_backup: true

  food_safety_steward:
    purpose: logs, allergen controls, cleaning procedures, illness exclusion
    required_backup: true

  garden_steward:
    purpose: planting, harvest, irrigation, soil coordination
    required_backup: true

  preservation_steward:
    purpose: safe preservation, batch logs, surplus planning
    required_backup: true

  pantry_steward:
    purpose: inventory, stock rotation, reserves, access
    required_backup: true

  care_meal_steward:
    purpose: meal support for illness, elder care, postpartum, injury, grief, crisis
    required_backup: true
```

### Role Rule

```text
No survival-critical food role may depend on one person.
```

---

## 25. Visualization Requirements

The food module should export enough data for a virtual world or dashboard to show how food works.

```yaml
visualization_requirements:
  spatial_objects:
    - common_kitchen
    - common_dining
    - dry_pantry
    - cold_storage
    - root_storage
    - greenhouse
    - garden_beds
    - orchard_or_perennials
    - compost_zone
    - delivery_route
    - wash_pack_zone

  overlays:
    - food_source_mix
    - storage_days_remaining
    - labor_burden
    - crop_health
    - harvest_forecast
    - waste_flow
    - emergency_food_buffer
    - food_safety_warning
    - supplier_risk

  scenario_playback:
    - drought_year
    - crop_failure
    - energy_outage
    - illness_wave
    - supply_disruption
```

---

## 26. Relationship to Housing Module

The food module depends heavily on the Dignified Village Block housing layout.

```yaml
housing_dependencies:
  common_house:
    required_for:
      - common_kitchen
      - common_dining
      - food_storage_access

  private_units:
    required_for:
      - private_food_autonomy
      - meal_opt_out
      - resident_dignity

  courtyards:
    useful_for:
      - herb_gardens
      - small_edible_landscapes
      - informal meals
      - child_elder_food_culture

  workshop:
    useful_for:
      - food_equipment_repair
      - garden_tool_repair
      - preservation_rack_building

  mobility:
    required_for:
      - delivery_access
      - accessible_food_access
      - garden_to_kitchen_routes
```

---

## 27. Best Default Requirements Summary

```yaml
MinimumViableFoodCommons:
  population:
    first_serious_model: 80
    valid_range: 50-150

  philosophy:
    total_self_sufficiency: false
    hybrid_food_commons: true
    private_food_autonomy: required
    common_meals: opt_in_default
    whole_food_pattern: preferred
    plant_forward_omnivore_compatible: true

  facilities:
    common_kitchen: required
    common_dining: required
    dry_pantry: required
    cold_storage: required
    root_or_cool_storage: preferred
    preservation_kitchen: required
    greenhouse_or_high_tunnel: required
    gardens: required
    compost_interface: required

  targets:
    onsite_fresh_produce: 40-70_percent_seasonal
    onsite_calories: 10-25_percent
    shelf_stable_buffer: 30_days_minimum
    shelf_stable_buffer_preferred: 90_days
    common_dinners: 3-5_per_week
    food_labor_per_resident: 2-5_hours_per_week_target

  automation:
    inventory_system: required
    meal_planner: required
    procurement_planner: required
    garden_planner: required
    preservation_logger: required
    role_scheduler: required
    simple_sensor_layer: preferred

  gates:
    dignity_gate: required
    nutrition_gate: required
    resilience_gate: required
    labor_gate: required
    safety_gate: required
    complexity_gate: required
    waste_gate: required
```

---

## 28. Design Maxims

```text
Do not confuse food resilience with total food self-sufficiency.

Do not reduce grocery costs by creating hidden unpaid labor.

Do not make common meals mandatory.

Do not eliminate private food autonomy.

Do not let food become a site of moral surveillance.

Do not build the baseline around fragile food technology.

Do not grow staple calories at heroic effort if regional farmers can supply them efficiently.

Do not treat food safety as optional because the community is small.

Do not let one charismatic gardener or cook become a single point of failure.

Use shared meals to return time.

Use gardens to return freshness, beauty, skill, and seasonal meaning.

Use bulk purchasing to return money.

Use storage to return resilience.

Use preservation to return value from surplus.

Use automation to remember, forecast, and coordinate, not to dominate.

Use food as one of the main ways the civic floor feels abundant.
```

---

## 29. Open Questions for Iteration

```text
1. Should the baseline be vegetarian, omnivore-compatible, or menu-plural?
2. What is the acceptable monthly food-cost target per resident?
3. What percentage of meals should be common by default?
4. Should animal systems be excluded from v0, optional in v1, or included for eggs?
5. Should the app model food as a cash-cost reduction system, a health system, a resilience system, or all three?
6. How much onsite land should be reserved per resident for gardens?
7. How strict should the food-safety gates be for private-membership communities?
8. Should the model support food enterprise, such as selling preserves or market-garden products, or keep v0 internal-only?
9. How should cultural food differences be represented without overcomplicating menu planning?
10. How should food labor be compensated, credited, or rotated?
```

---

## 30. Source Notes

The research basis for this draft includes:

- USDA Food and Nutrition Service, Dietary Guidelines for Americans, 2025-2030.
- USDA Food and Nutrition Service, USDA Food Plans and monthly cost reports.
- USDA Food Loss and Waste resources.
- USDA National Agricultural Library, Community Supported Agriculture.
- USDA Agricultural Marketing Service, Local and Regional Food System Resources.
- FDA Food Code resources.
- National Center for Home Food Preservation / University of Georgia Cooperative Extension preservation resources.
- Cohousing research on common meals and household labor.
- Community kitchen research on social and nutritional health.
- FAO agroecology framework and principles of diversity, resilience, efficiency, recycling, and circular / solidarity economy.
