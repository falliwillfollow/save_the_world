# CIaC Housing Module: Dignified Village Block

**Module ID:** `housing.dignified_village_block.v0_1`  
**Status:** Draft requirement module  
**Purpose:** Define the default housing model for a scalable Minimum Viable Dignified Infrastructure complex.  
**Primary design question:** What housing form best balances privacy, shared abundance, construction efficiency, automation, resilience, and human beauty without recreating detached sprawl or institutional dormitory life?

---

## 1. Core Thesis

The CIaC housing baseline should not be detached single-family homes.

Detached single-family housing provides privacy and symbolic autonomy, but it is inefficient for the CIaC goal because it duplicates infrastructure, appliances, roofs, walls, utility runs, tools, kitchens, laundry, maintenance burdens, vehicle dependency, and isolation.

The recommended baseline is a **Dignified Village Block**:

```text
private dwellings or suites
+ clustered residential pods
+ shared common house
+ shared food and dining infrastructure
+ shared laundry
+ shared workshop and tool library
+ shared gardens and outdoor commons
+ edge vehicle access
+ pedestrian-first interior
+ modular / panelized construction
+ repeatable pod-based scaling
```

The goal is not to make people live communally by force.

The goal is to create a housing pattern where people retain private, dignified space while the expensive and wasteful burdens of daily life are quietly pooled, simplified, and automated around them.

---

## 2. Guiding Sentence

> Community at the doorstep, privacy behind the door.

Every resident should be able to withdraw, rest, work, grieve, sleep, create, or simply be alone without social performance.

Every resident should also have easy access to common spaces that make life easier, more beautiful, more resilient, and less expensive.

---

## 3. Recommended Scale

The first serious model should target a population large enough to support shared resilience but small enough to avoid city-scale bureaucracy.

```yaml
population:
  minimum_meaningful_scale: 50
  ideal_first_model: 80
  upper_bound_before_replication: 150
```

### Rationale

- **Below 50 residents:** too fragile, limited redundancy, weak care capacity, limited specialization.
- **Around 80 residents:** enough people for shared infrastructure, role backup, food operations, workshops, care, education, and social variety.
- **Above 150 residents:** risk of bureaucracy, anonymity, institutional feeling, and governance overhead.
- **Scaling method:** replicate village blocks rather than expanding one block indefinitely.

---

## 4. Recommended Typology

```yaml
typology:
  name: clustered_courtyard_pods
  avoid:
    - detached_single_family_sprawl
    - one_giant_institutional_block
    - dormitory_without_privacy
    - aesthetic_retreat_center_without_operations
    - isolated_tiny_home_scatter
```

### Spatial Pattern

The complex should be composed of multiple residential pods arranged around semi-private courtyards, with a central common house and shared operational infrastructure.

```text
Residential Pod -> Courtyard Cluster -> Common House -> Workshop / Food / Care Infrastructure -> Village Block
```

Each pod should feel like a small neighborhood.

The full complex should feel like a village.

---

## 5. Residential Pod Requirements

```yaml
residential_pod:
  residents_per_pod:
    minimum: 12
    target: 16-20
    maximum: 24

  required_features:
    - private_units
    - acoustic_privacy
    - daylight
    - lockable_doors
    - lockable_storage
    - bathroom_access
    - semi_private_threshold_space
    - direct_or_easy_access_to_outdoor_space
    - accessible_units
    - family_units
    - elder_friendly_units
```

### Pod Design Intent

A pod should not feel like a dorm hallway.

It should feel like a small cluster of homes around a humane threshold space.

Preferred forms:

```text
courtyard pod
garden walk pod
short gallery pod
clustered stair pod
atrium-lite pod
```

Avoid:

```text
long anonymous corridors
hotel-like repetition
windowless common areas
shared bathrooms as default for all residents
social spaces that residents must pass through to reach private space
```

---

## 6. Private Unit Standard

Every resident or household must have private, lockable, dignified space.

### Single Adult / Couple Unit

```yaml
private_unit_single_or_couple:
  required:
    - sleeping_area
    - sitting_or_work_area
    - daylight
    - ventilation
    - acoustic_separation
    - lockable_storage
    - private_or_semi_private_bathroom_access
    - small_food_autonomy
    - ability_to_withdraw

  preferred:
    - small_kitchenette_or_wet_bar
    - direct_view_to_greenery
    - operable_window
    - flexible_furniture_layout
```

### Family / Multi-Person Unit

```yaml
private_unit_family:
  required:
    - separate_sleeping_rooms
    - private_bathroom
    - private_kitchen_or_kitchenette
    - acoustic_separation_from_common_noise
    - child_safe_access_to_outdoor_space
    - storage_for_food_clothing_tools_and_school_materials

  preferred:
    - direct_access_to_courtyard
    - flexible_room_conversion
    - proximity_to_child_elder_commons
```

### Non-Negotiable Privacy Rule

```text
No resident should need to perform sociability in order to access sleep, hygiene, rest, or personal food autonomy.
```

---

## 7. Common Space Ratio

```yaml
common_space_ratio:
  minimum: 15%
  target: 20-30%
  warning_below: 12%
  warning_above: 35%
```

### Rationale

Too little common space creates a conventional apartment complex with token amenities.

Too much common space increases cost, cleaning labor, governance burden, and underused square footage.

The target is enough shared space to reduce duplicated private burdens without making communal life feel mandatory.

---

## 8. Required Common Spaces

The common program should be functional before decorative.

```yaml
required_common_spaces:
  common_kitchen_dining:
    priority: critical
    purpose:
      - shared meals
      - reduced cooking burden
      - social glue
      - food efficiency
      - emergency meal operations

  laundry:
    priority: critical
    purpose:
      - avoid duplicated appliances
      - reduce unit cost
      - centralize maintenance

  workshop_tool_library:
    priority: critical
    purpose:
      - repair
      - maintenance
      - fabrication
      - resident autonomy
      - reduced private tool ownership

  food_storage_preservation:
    priority: critical
    purpose:
      - bulk buying
      - crop storage
      - preserved food buffer
      - bad-year resilience

  quiet_library_room:
    priority: high
    purpose:
      - solitude
      - study
      - decompression
      - non-social shared space

  care_health_room:
    priority: high
    purpose:
      - illness isolation
      - first aid
      - telehealth
      - elder care support
      - visiting practitioner use

  cowork_learning_room:
    priority: medium_high
    purpose:
      - remote work
      - education
      - meetings
      - classes
      - shared knowledge work

  guest_rooms:
    priority: medium_high
    purpose:
      - visiting family
      - caregivers
      - temporary displacement
      - trial stays

  child_elder_friendly_commons:
    priority: high
    purpose:
      - intergenerational life
      - play
      - supervision
      - social continuity

  outdoor_courtyard_garden:
    priority: critical
    purpose:
      - beauty
      - informal encounter
      - play
      - food production
      - seasonal ritual
      - passive restoration
```

---

## 9. Common Space Scoring

Common spaces should be scored, not merely listed.

```yaml
common_space_scoring:
  visibility: 0-10
  accessibility: 0-10
  flexibility: 0-10
  distance_from_units: 0-10
  noise_conflict_risk: 0-10
  maintenance_burden: 0-10
  expected_frequency_of_use: 0-10
  dignity_contribution: 0-10
  resilience_contribution: 0-10
```

### Failure Conditions

A common space should be flagged if:

```text
it is hidden
it is too far from daily paths
it creates noise near sleeping spaces
it requires excessive cleaning
it serves status rather than daily life
it duplicates something better handled privately
it exists mainly for aesthetic marketing
```

---

## 10. Construction Strategy

The default construction strategy should favor automation, repeatability, professional review, and repairability.

```yaml
construction_strategy:
  preferred:
    - panelized_light_wood
    - modular_light_wood
    - mass_timber_where_economically_viable
    - hybrid_mass_timber_light_wood
    - kit_of_parts_construction

  avoid:
    - bespoke_one_off_architecture
    - shipping_container_gimmicks
    - unreviewed_experimental_structures
    - heroic_DIY_as_default
    - aesthetics_before_operability
    - detached_house_sprawl
```

### Construction Principle

> Use novel organization before novel physics.

The first innovation should be the arrangement, automation, and shared infrastructure model.

Do not make the baseline depend on exotic materials, unproven construction systems, or heroic self-building.

---

## 11. Automation-Favoring Requirements

The housing module should support automated layout generation, costing, simulation, and visualization.

```yaml
automation_requirements:
  structural_grid:
    required: true
    purpose: enables repeatable layouts and component reuse

  repeated_unit_types:
    required: true
    purpose: avoids custom design explosion

  panelized_components:
    required: true
    purpose: supports factory fabrication and digital estimation

  stacked_wet_cores:
    required: true
    purpose: reduces plumbing complexity and cost

  service_spine:
    required: true
    purpose: groups water, power, data, ventilation, and maintenance access

  interchangeable_room_modules:
    preferred: true
    purpose: supports changing household needs over time

  prefab_ready_bill_of_materials:
    required: true
    purpose: supports automated costing and procurement

  bim_ifc_export:
    preferred: true
    purpose: supports professional review and architecture workflows

  unreal_visualization_export:
    preferred: true
    purpose: supports virtual proof and human-scale review
```

---

## 12. Infrastructure Abstraction Boundary

The app should model infrastructure at the pattern level.

It should know enough to make intelligent design choices, but not attempt to replace licensed professionals.

### The App Should Model

```text
building topology
population capacity
private/common area ratios
walking distances
noise conflicts
daylight access
shared space access
wet core stacking
service spine logic
maintenance zones
professional review requirements
resilience dependencies
failure modes
labor burden
cost ranges
visualization exports
```

### The App Should Not Model by Default

```text
exact wire routing
breaker panel design
pipe diameters
HVAC duct sizing
foundation rebar schedules
fire-rated assembly certification
final code compliance
structural stamping
permit documents
```

### Principle

```text
The app should identify what must be true.
Professionals should determine the exact implementation where law, safety, and craft require it.
```

---

## 13. Mobility and Site Layout

The interior of the village block should be pedestrian-first.

```yaml
mobility:
  internal_life:
    preferred: pedestrian_first
    allowed:
      - carts
      - bikes
      - mobility_assist_devices
      - emergency_access

  vehicles:
    preferred_location: perimeter
    requirements:
      - delivery_access
      - emergency_access
      - accessible_dropoff
      - service_access
```

### Site Intent

Residents should be able to move through daily life without constant interaction with cars.

Vehicles should support the settlement, not define it.

---

## 14. Housing Gates

The housing module should fail or warn when the design violates core principles.

```yaml
housing_gates:
  privacy_gate:
    fail_if:
      - no_lockable_private_space
      - sleep_requires_shared_social_space
      - hygiene_access_is_unsafe_or_humiliating

  commons_gate:
    warn_if:
      - common_space_ratio_below_12_percent
      - common_space_ratio_above_35_percent
      - no_common_kitchen_dining
      - no_workshop_tool_library
      - no_quiet_room

  dignity_gate:
    fail_if:
      - insufficient_daylight
      - no_retreat_capacity
      - excessive_noise_near_sleeping_units
      - inaccessible_units_absent

  automation_gate:
    warn_if:
      - too_many_custom_unit_types
      - no_structural_grid
      - wet_cores_not_stacked
      - no_service_spine
      - no_prefab_ready_BOM

  resilience_gate:
    warn_if:
      - no_food_storage
      - no_care_health_room
      - no_guest_or_overflow_capacity
      - no_role_backup_for_building_maintenance
```

---

## 15. Simulation Inputs

The module should expose simulation parameters.

```yaml
simulation_inputs:
  population:
    residents_total: integer
    household_mix:
      single_adults: integer
      couples: integer
      families: integer
      elders: integer
      accessibility_needs: integer

  area:
    private_area_total_m2: number
    common_area_total_m2: number
    circulation_area_total_m2: number
    outdoor_common_area_m2: number

  construction:
    construction_system: enum
    unit_type_count: integer
    panelization_ratio: number
    estimated_build_cost: number
    estimated_build_labor_hours: number

  operations:
    cleaning_labor_hours_per_week: number
    maintenance_labor_hours_per_month: number
    common_kitchen_meals_per_week: number
    laundry_loads_per_week: number
    workshop_use_hours_per_week: number

  human_factors:
    privacy_score: number
    commons_access_score: number
    acoustic_risk_score: number
    daylight_score: number
    nature_access_score: number
    dignity_score: number
```

---

## 16. Required App Outputs

The app should generate outputs that can be reviewed by humans and downstream systems.

```yaml
required_outputs:
  - housing_topology_summary
  - pod_count_and_population_distribution
  - private_common_area_ratio
  - required_common_space_schedule
  - privacy_score
  - commons_access_score
  - maintenance_burden_score
  - automation_readiness_score
  - resilience_warnings
  - professional_review_requirements
  - estimated_cost_range
  - estimated_labor_range
  - visualization_bundle
  - unreal_handoff_metadata
```

---

## 17. Default Prototype

```yaml
default_prototype:
  name: dignified_village_block_80
  residents: 80

  residential_pods:
    count: 4
    residents_per_pod: 20

  shared_facilities:
    - common_house
    - common_kitchen_dining
    - laundry
    - workshop_tool_library
    - food_storage_preservation
    - care_health_room
    - quiet_library_room
    - cowork_learning_room
    - guest_rooms
    - child_elder_commons
    - courtyard_gardens

  mobility:
    interior: pedestrian_first
    vehicles: perimeter

  construction:
    baseline: panelized_light_wood_or_hybrid_mass_timber
    layout_logic:
      - structural_grid
      - repeated_unit_types
      - stacked_wet_cores
      - service_spine
      - prefab_ready_BOM
```

---

## 18. Design Maxims

```text
Do not make togetherness mandatory.

Do not optimize cost by humiliating residents.

Do not confuse austerity with dignity.

Do not solve housing by recreating dormitories.

Do not use novelty where standard trades already solve the problem.

Do not let the app pretend to replace architects, engineers, electricians, plumbers, code officials, or residents.

Use shared infrastructure to remove duplicated burden.

Use private space to protect autonomy.

Use common space to create reasons to come together.

Use automation to reduce complexity, not to add spectacle.

Use virtual modeling to expose weak points before real people depend on the system.
```

---

## 19. Relationship to Other CIaC Modules

This housing module depends on, informs, or constrains the following future modules:

```text
water
sanitation
energy
food
care
governance
maintenance
mobility
materials
finance
legal_land
simulation
visualization
```

Housing is not the whole system.

Housing is the spatial body in which the civic floor becomes livable.
