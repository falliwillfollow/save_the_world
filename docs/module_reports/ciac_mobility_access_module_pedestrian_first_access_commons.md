# CIaC Mobility & Access Module: Pedestrian-First Access Commons

**Module ID:** `mobility_access.pedestrian_first_access_commons.v0_1`  
**Status:** Draft requirement module  
**Purpose:** Define the default mobility, access, circulation, transportation, delivery, emergency access, and accessibility system for a scalable Minimum Viable Dignified Infrastructure complex.  
**Primary design question:** What mobility system best reduces car dependency, lowers cash and time burden, preserves accessibility and emergency access, supports daily dignity, and connects residents to the wider world without turning the village block into either suburban sprawl or an isolated retreat?

---

## 1. Core Thesis

The CIaC mobility baseline should **not** be car-first site planning.

Car-first design quietly recreates many of the burdens CIaC is trying to remove: high monthly cost, parking land waste, asphalt heat, danger, isolation for non-drivers, long walking distances, fragile access to care, and dependency on insurance, fuel, repairs, debt, and individual vehicle ownership.

The recommended baseline is a **Pedestrian-First Access Commons**:

```text
walkable internal village block
+ universal accessible routes
+ vehicle access at the perimeter
+ emergency and service access preserved
+ shared carts and cargo bikes
+ accessible drop-off points
+ delivery and maintenance routes
+ regional transit or shuttle connection
+ shared vehicle pool where needed
+ clinic / pharmacy / grocery access plan
+ low-parking, not no-access
+ mobility dashboard and scheduling
+ evacuation and access-functional-needs planning
```

The goal is not to ban vehicles.

The goal is to make daily life possible, pleasant, and dignified without requiring every adult to own and operate a private car.

---

## 2. Guiding Sentence

> Put people, care, and daily life at the center; put cars, trucks, and service vehicles at the edge unless they are needed for access, emergency, delivery, or dignity.

---

## 3. Strategic Decision

The best default model is:

# A pedestrian-first internal commons with perimeter vehicle access, universal design, shared mobility, and strong external connections.

```yaml
mobility_access_strategy:
  internal_pattern:
    recommended:
      - pedestrian_first_paths
      - accessible_routes_to_all_essential_spaces
      - short_daily_distances
      - common_house_as_path_intersection
      - courtyards_and_thresholds
      - carts_bikes_and_mobility_devices_allowed
      - emergency_access_designed_in
      - service_routes_separated_where_possible

  perimeter_pattern:
    recommended:
      - vehicle_parking_at_edges
      - accessible_dropoffs_near_housing_and_common_house
      - delivery_loading_points
      - emergency_vehicle_routes
      - maintenance_service_access
      - shared_vehicle_node
      - bike_and_cargo_bike_storage

  external_pattern:
    recommended:
      - transit_or_shuttle_connection
      - shared_vehicle_pool
      - care_transport_plan
      - grocery_pharmacy_clinic_trip_plan
      - regional bike/trail connection where safe
      - fallback ride services
      - evacuation transport plan

  avoid_as_default:
    - driveways_to_every_unit
    - parking_dominant_site_plan
    - isolated_rural_site_with_no_non_car_access
    - no_accessible_routes
    - romantic_car_free_site_without_emergency_service_access
    - long_paths_between_homes_and_daily_needs
    - hidden_transport_costs
    - inaccessible_courtyards_or_common_spaces
    - no_plan_for_non_drivers
```

### Rationale

Transportation is not only movement. It is a hidden tax on time, money, energy, health, land, safety, and social possibility.

A dignified village block should let residents meet most daily needs through walking, rolling, carts, bikes, shared logistics, and planned regional connections.

---

## 4. Research Anchors

This module is grounded in the following research and precedent categories.

### 4.1 Complete Streets

FHWA Complete Streets guidance emphasizes designing and operating streets to be safe and accessible for all users, including people of all ages, abilities, and transportation modes.

**Design implication:** CIaC should treat walking, rolling, biking, transit, service, delivery, and emergency movement as planned users, not afterthoughts.

### 4.2 NACTO street design

NACTO's Urban Street Design Guide presents a toolbox for safer, more livable streets. Its shared-street guidance supports places where pedestrian activity is high and vehicle volumes are low or discouraged.

**Design implication:** The internal circulation system can behave like a slow shared street or woonerf-like commons, but must remain carefully designed for visibility, drainage, accessibility, emergency access, and maintenance.

### 4.3 ADA and accessible routes

U.S. Access Board ADA guidance includes minimum accessible-route and ramp clearances, including 36 inch minimum clear width for many accessible routes and ramp runs, subject to additional life-safety or context-specific requirements.

**Design implication:** CIaC should exceed minimum accessibility wherever practical and must never rely on picturesque paths that exclude wheelchair users, elders, parents with strollers, or injured residents.

### 4.4 Transit-oriented development

ITDP's TOD Standard is organized around principles such as Walk, Cycle, Connect, Transit, Mix, Densify, Compact, and Shift.

**Design implication:** CIaC's village block should use the same logic at settlement scale: short distances, connected paths, mixed daily functions, density sufficient for shared services, and reduced car dominance.

### 4.5 Smart Growth

EPA Smart Growth principles include mixing land uses, compact building design, walkable neighborhoods, open space preservation, and a variety of transportation choices.

**Design implication:** The mobility module should connect land use and transportation rather than treating transportation as a separate afterthought.

### 4.6 Housing and transportation affordability

HUD's Location Affordability Index treats housing and transportation costs together because lower housing costs can be offset by higher transportation costs.

**Design implication:** CIaC must include transportation cost in affordability. A cheap rural site that forces every resident to own a car may not actually reduce life burden.

### 4.7 Bikeway selection

FHWA bikeway selection guidance links bicycle facility type to vehicle speed and volume, generally requiring more separation as speeds and traffic volumes rise.

**Design implication:** Internal low-speed paths can be shared, but external bike connections on higher-speed roads require protected or separated infrastructure, not painted optimism.

### 4.8 Access and functional needs

FEMA and emergency planning guidance emphasize planning for transportation and access needs for people with disabilities, older adults, children, medical needs, service animals, and people who rely on assistive equipment.

**Design implication:** Mobility planning must include evacuation, clinic access, medication access, accessible vehicles, backup drivers, and device charging.

---

## 5. Recommended Scale

The mobility and access module should support the same first serious population as the other CIaC modules.

```yaml
population:
  minimum_meaningful_scale: 50
  ideal_first_model: 80
  upper_bound_before_replication: 150
```

### Scale Logic

```text
Below 50:
  shared vehicles, shuttles, and route scheduling may be underutilized.

Around 80:
  shared carts, cargo bikes, accessible vehicle access, delivery consolidation, clinic/pharmacy trips, and vehicle pooling become realistic.

Above 150:
  internal mobility, parking, service access, and transit connections may require more formal transportation management.
```

### Scaling Method

Replicate human-scale village blocks and connect them with mobility corridors.

```yaml
scaling:
  50-100_residents:
    internal_paths: 1_connected_network
    vehicle_edges: 1-3
    shared_vehicle_node: required_where_external_access_is_car_dependent
    bike_cart_storage: required

  100-150_residents:
    internal_paths: network_with_secondary_loops
    service_routes: defined
    shared_vehicle_node: required
    mobility_steward_team: 2-4_people

  above_150_residents:
    recommendation: replicate_village_blocks_and_link_with_transit_shuttle_or_greenway
```

---

## 6. Default Prototype

```yaml
default_prototype:
  name: pedestrian_first_access_commons_80
  residents: 80

  site_pattern:
    internal_life:
      - pedestrian_first
      - universal_access
      - low_speed_shared_paths
      - shaded_routes
      - weather_resilient_paths
      - short_distances_to_daily_needs

    edge_access:
      - perimeter_parking
      - accessible_dropoffs
      - emergency_vehicle_loop_or_spurs
      - delivery_loading
      - maintenance_access
      - shared_vehicle_node
      - bike_cargo_bike_storage

    external_access:
      - transit_or_shuttle_plan
      - care_transport_plan
      - grocery_pharmacy_clinic_plan
      - bike_route_safety_review
      - regional_trip_pooling
      - evacuation_transport_plan

  targets:
    max_distance_unit_to_common_house: 2-4_minutes_walk_or_roll
    max_distance_unit_to_food_commons: 2-4_minutes_walk_or_roll
    max_distance_unit_to_care_room: 3-5_minutes_walk_or_roll
    max_distance_unit_to_accessible_dropoff: 1-3_minutes_walk_or_roll_where_possible
    max_distance_unit_to_waste_sorting: close_but_not_nuisance
    internal_vehicle_speed: walking_speed_or_very_low_speed
    private_vehicle_dependency: minimized
    accessible_route_coverage: 100_percent_of_essential_spaces
```

---

## 7. Mobility Service Levels

The app should model mobility as service levels.

```yaml
mobility_service_levels:
  emergency_access:
    includes:
      - EMS_access
      - fire_access
      - evacuation
      - accessible_transport_for_high_need_residents
      - critical_supply_delivery
    dignity_status: non_negotiable

  basic_dignity:
    includes:
      - accessible_routes_to_home_common_house_food_care_sanitation
      - safe_paths
      - lighting
      - resting_points
      - accessible_dropoffs
      - routine_delivery_access
      - ability_for_non_drivers_to_meet_daily_needs
    dignity_status: default_minimum

  low_burden_daily_life:
    includes:
      - short_internal_trips
      - shared carts
      - bikes_and_cargo_bikes
      - consolidated errands
      - shared vehicle or shuttle
      - external service access
      - delivery coordination
      - low parking burden
    dignity_status: target

  regional_autonomy:
    includes:
      - transit_or_shuttle
      - regional bike/trail access where safe
      - shared vehicle pool
      - clinic_and_pharmacy trips
      - social and cultural trips
      - employment access
    dignity_status: preferred

  car_dependent:
    includes:
      - every adult needs private vehicle
      - daily needs outside walking range
      - no transit/shuttle/shared vehicle plan
    dignity_status: warning_or_failure
```

### Principle

```text
The mobility system is dignified only if non-drivers can still live fully.
```

---

## 8. Spatial Mobility Pattern

The village block should use a clear spatial hierarchy.

```yaml
spatial_pattern:
  pedestrian_core:
    purpose:
      - daily social life
      - child and elder safety
      - quiet
      - walking and rolling
      - courtyard connection
      - common-house access
    vehicles:
      - emergency_only
      - service_only_by_time_window
      - mobility_assist_allowed
      - carts_allowed
      - bikes_low_speed

  service_edge:
    purpose:
      - deliveries
      - waste pickup
      - maintenance vehicles
      - fire/EMS access
      - accessible dropoff
      - shared vehicles
    design:
      - clear turning and staging
      - does_not_dominate_core
      - screened_where_possible
      - accessible_routes_to_core

  regional_connection:
    purpose:
      - transit
      - shuttle
      - shared vehicle
      - bike network
      - care transport
      - employment and city access
    design:
      - safe path to stop or pickup
      - sheltered waiting
      - lighting
      - schedule visibility
```

### Spatial Principle

```text
Daily life should be pedestrian-first; service and emergency movement should be designed, not wished away.
```

---

## 9. Universal Access Requirements

Accessibility is a baseline, not an accommodation afterthought.

```yaml
universal_access:
  required:
    - accessible_route_to_every_essential_space
    - accessible_private_units
    - accessible_common_house
    - accessible_food_commons
    - accessible_care_room
    - accessible_laundry
    - accessible_workshop_or_equivalent_access
    - accessible_waste_sorting_or_assisted_service
    - accessible_dropoff_points
    - curb_ramps_or_level_transitions
    - firm_stable_slip_resistant_surfaces
    - lighting
    - resting_points
    - snow_ice_or_weather_management_where_relevant
    - wayfinding
    - emergency_access_for_mobility_limited_residents

  preferred:
    - routes_exceeding_minimum_width
    - two_wheelchairs_passing_points
    - shade_and_benches
    - handrails_where_grade_requires
    - tactile_and_visual_wayfinding
    - step_free_entries_to_all_common_spaces
    - accessible garden beds or equivalent participation

  app_boundary:
    - app_models_accessibility_requirements_and_flags
    - licensed_design_professionals_validate_code_and_ADA_FHA_local_accessibility_requirements
```

### Universal Access Principle

```text
If the path to the commons excludes someone, the commons is not common.
```

---

## 10. Walking and Rolling Network

The internal network should be short, legible, shaded, and safe.

```yaml
walking_rolling_network:
  required:
    - continuous_paths
    - direct_routes_to_daily_needs
    - loop_options
    - accessible_surface
    - drainage
    - lighting
    - resting_points
    - clear_sightlines
    - winter_or_rain_strategy_where_relevant
    - child_safe_edges
    - route_to_emergency_pickup

  route_types:
    primary_access_route:
      connects:
        - residential_pods
        - common_house
        - food_commons
        - care_room
        - accessible_dropoff
        - emergency_points
      requirements:
        - accessible
        - lit
        - weather_resilient
        - maintained_first_after_storms

    secondary_social_path:
      connects:
        - courtyards
        - gardens
        - quiet spaces
        - workshop
      requirements:
        - accessible_where_possible
        - pleasant
        - optional

    service_path:
      connects:
        - delivery
        - waste
        - maintenance
        - workshop
        - storage
      requirements:
        - durable
        - conflict_minimized_with_social_core
        - vehicle_or_cart_compatible
```

### Path Principle

```text
The most important places should be the easiest places to reach.
```

---

## 11. Shared Street / Woonerf-Like Internal Lane

Where vehicles must enter the core, the design should force low speed and pedestrian priority.

```yaml
shared_internal_lane:
  allowed_if:
    - vehicle_volumes_low
    - speeds_physically_calmed
    - pedestrian_priority_clear
    - accessible_route_preserved
    - drainage_handled
    - emergency_service_reviewed
    - delivery_windows_defined_where_needed

  design_features:
    - narrow_vehicle_path
    - visual_cues_for_pedestrian_priority
    - textured_or_differentiated_surface_where_accessibility_allows
    - no_high_speed_geometry
    - limited_parking
    - clear_edge_zones
    - lighting
    - sightlines
    - mountable_or_reinforced_edges_for_emergency_access_where_reviewed

  fail_if:
    - vehicles_can_move_at_suburban_street_speeds
    - pedestrians_forced_to_yield_by_design
    - accessible_route_unclear
    - children_elder_common_areas_exposed_to_through_traffic
```

### Shared Lane Principle

```text
A shared lane is not a road with wishful signage. The geometry must make carelessness difficult.
```

---

## 12. Bicycle, Cargo Bike, and Cart Strategy

Small vehicles can replace many car trips inside and near the village block.

```yaml
bike_cart_strategy:
  required:
    - secure_bike_storage
    - cargo_bike_storage
    - mobility_cart_storage
    - charging_for_e_bikes_and_mobility_devices
    - repair_stand
    - basic_parts_inventory
    - safe_internal_routes
    - rules_for_speed_and_yielding
    - weather_protected_storage

  shared_fleet:
    preferred:
      - cargo_bikes
      - hand_carts
      - garden_carts
      - mobility_golf_cart_or_NEV_where_legal_and_needed
      - trailers
      - bike_share_or_pool

  external_bike_access:
    required_review:
      - vehicle_speed
      - traffic_volume
      - shoulder_or_lane_presence
      - separated_path_availability
      - intersection_safety
      - lighting
      - winter_weather
      - comfort_for_interested_but_concerned_riders

  fail_if:
    - external_bike_route_requires_high_speed_mixed_traffic_without_review
    - cargo_bikes_have_no_storage_or_maintenance
    - e_bike_charging_has_no_fire_safety_policy
```

### Bike/Cart Principle

```text
Cargo bikes and carts work when they are closer than cars, easier than errands, and maintained like real infrastructure.
```

---

## 13. Parking Strategy

Parking should support access without consuming the place.

```yaml
parking_strategy:
  default:
    - perimeter_parking
    - reduced_private_parking_ratio
    - shared_vehicle_priority
    - accessible_spaces_near_dropoffs
    - visitor_parking_limited
    - service_and_delivery_zones
    - no_driveways_to_each_unit
    - no_large_surface_lot_at_center

  parking_categories:
    resident_private_vehicles:
      status: minimized_not_forbidden
      location: edge

    shared_vehicles:
      status: prioritized
      location: visible_edge_node

    accessible_parking:
      status: required
      location: closest_feasible_to_accessible_routes

    service_delivery:
      status: required
      location: edge_or_service_lane

    emergency:
      status: required
      location: route_not_parking

    bikes_cargo_bikes:
      status: required
      location: closer_than_car_parking

  app_outputs:
    - parking_count
    - parking_land_area
    - cost_per_space
    - heat_island_risk
    - walking_distance_from_parking
    - accessible_parking_compliance_flag
    - shared_vehicle_substitution_rate
```

### Parking Principle

```text
Cars may be useful. Parking should not become the village's largest room.
```

---

## 14. Shared Vehicle and Shuttle Strategy

A car-light system still needs regional access.

```yaml
shared_vehicle_shuttle:
  required_if:
    - transit_access_poor
    - clinics_or_grocery_or_pharmacy_not_walkable
    - residents_include_non_drivers
    - rural_or_periurban_site
    - employment_access_requires_vehicle

  shared_vehicle_pool:
    preferred:
      - 1_vehicle_per_15_to_30_residents_initial_range
      - at_least_one_accessible_or_high_access_vehicle_where_needed
      - booking_system
      - maintenance_plan
      - insurance_review
      - driver_eligibility_rules
      - cost_allocation
      - cleaning_and_refueling_or_charging_rules

  shuttle:
    optional:
      - fixed_day_grocery_pharmacy_route
      - clinic_trip_day
      - transit_connection
      - school_or_education_connection
      - regional_market_connection

  ride_support:
    preferred:
      - volunteer_driver_pool_with_safeguards
      - paid_driver_option
      - paratransit_or_demand_response_integration_where_available
      - emergency_taxi_or_rideshare_fund
```

### Shared Vehicle Principle

```text
A car-light life requires shared access to cars when cars are genuinely needed.
```

---

## 15. Delivery, Freight, and Service Access

Daily life needs goods movement.

```yaml
delivery_service_access:
  required:
    - delivery_dropoff_zone
    - package_storage
    - cold_chain_delivery_plan_where_food_or_meds_need_it
    - large_delivery_staging
    - maintenance_vehicle_access
    - waste_pickup_access
    - moving_truck_access
    - fire_and_EMS_routes
    - service_time_windows_where_core_conflict_exists

  preferred:
    - consolidated_delivery_point
    - cargo_cart_transfer_from_edge_to_core
    - covered_package_room
    - refrigerated_lockers_if_food_or_med_delivery_common
    - signage_and_wayfinding_for_drivers
    - delivery_route_not_through_child_play_core

  fail_if:
    - service_vehicles_must_regularly_drive_through_main_social_courtyard
    - deliveries_block_emergency_access
    - no_plan_for_large_items_or_move_ins
    - waste_collection_conflicts_with food or care routes
```

### Freight Principle

```text
A low-car place still needs a dignified goods system.
```

---

## 16. Emergency Access and Evacuation

Emergency access is non-negotiable.

```yaml
emergency_access:
  required:
    - EMS_route
    - fire_access_review
    - emergency_vehicle_turnaround_or_approved_access
    - accessible_evacuation_routes
    - evacuation_assembly_points
    - high_need_resident_transport_plan
    - emergency_pickup_points
    - route_lighting
    - route_clearance_after_storms
    - communication_tree
    - backup_route_where_possible

  must_model:
    - fire_truck_access_constraints
    - ambulance_access_to_care_room_and_housing_pods
    - evacuation_of_mobility_limited_residents
    - flood_fire_storm_blockage
    - winter_or_debris_obstruction
    - shared_vehicle_availability
    - fuel_or_charging_state
    - service_animal_and_medical_equipment_transport

  fail_if:
    - pedestrian_core_blocks_emergency_response
    - no_accessible_evacuation_plan
    - no_transport_plan_for_high_need_residents
    - route_width_turning_surface_or_clearance_unreviewed
```

### Emergency Principle

```text
A peaceful pedestrian core must still be reachable when someone is hurt.
```

---

## 17. Wayfinding, Lighting, and Safety

Mobility is also cognition, perception, and confidence.

```yaml
wayfinding_lighting_safety:
  required:
    - clear_path_names_or_markers
    - unit_and_common_space_wayfinding
    - emergency_wayfinding
    - lighting_on_primary_routes
    - glare_control
    - dark_sky_or_light_pollution_consideration
    - sightlines
    - resting_points
    - slip_trip_hazard_management
    - snow_leaf_mud_management_where_relevant
    - nighttime_access_to_care_room_and_common_house

  preferred:
    - tactile_wayfinding_where_useful
    - high_contrast_markings
    - audible_or_digital_wayfinding_support
    - landmark_based_navigation
    - visual_connection_to_common_house
    - benches_near decision points
```

### Wayfinding Principle

```text
A path is accessible only if people can find it, trust it, and use it in the dark, in stress, and in bad weather.
```

---

## 18. External Location Scoring

The app should evaluate site location before optimizing internal paths.

```yaml
external_location_scoring:
  required_metrics:
    - distance_to_grocery
    - distance_to_pharmacy
    - distance_to_primary_care
    - distance_to_urgent_care_or_hospital
    - distance_to_transit_stop_or_shuttle_pickup
    - distance_to_school_or_learning_site_if_relevant
    - distance_to_employment_centers_or_remote_work_viability
    - distance_to_social_cultural_destinations
    - distance_to_public_trails_or_nature
    - road_safety_for_biking_walking
    - delivery_service_availability
    - emergency_response_time_estimate
    - winter_or_weather_access_risk

  scoring:
    excellent:
      - daily_needs_access_without_private_car
      - safe_walk_bike_transit_options

    acceptable:
      - daily_needs_met_with_shared_vehicle_or_scheduled_shuttle
      - emergency_and_care_access_strong

    warning:
      - non_drivers_dependent_on_ad_hoc_rides
      - clinic_pharmacy_grocery_access_fragile

    fail:
      - site_isolated_without_transport_plan
      - emergency_response_or_evacuation_unresolved
      - high_need_residents_cannot_reach_care
```

### Location Principle

```text
Cheap land is expensive if it forces every life need through a car.
```

---

## 19. Transportation Cost Model

The app must include transportation in affordability.

```yaml
transportation_cost_model:
  required_costs:
    private_vehicle:
      - loan_or_depreciation
      - insurance
      - fuel_or_charging
      - maintenance
      - registration_taxes_fees
      - parking
      - repairs
      - replacement_reserve

    shared_vehicle:
      - purchase_or_lease
      - insurance
      - maintenance
      - fuel_or_charging
      - cleaning
      - booking_software
      - driver_policy
      - replacement_reserve

    shuttle_or_transit:
      - passes
      - operating_cost
      - driver_labor
      - vehicle_cost
      - contract_cost
      - schedule_coverage

    bike_cart:
      - purchase
      - maintenance
      - storage
      - charging_if_e_bike
      - safety_equipment
      - replacement

  outputs:
    - monthly_transport_cost_per_resident
    - private_vehicle_dependency_score
    - vehicle_ownership_reduction_potential
    - required_wage_hours_for_transport
    - transport_cost_plus_housing_cost
    - affordability_comparison
```

### Cost Principle

```text
Housing affordability is false if transportation costs quietly take back the savings.
```

---

## 20. Interfaces With Other Modules

### 20.1 Housing Interface

```yaml
housing_mobility_interface:
  required:
    - unit_to_common_house_distance
    - accessible_routes
    - private_unit_thresholds
    - guest_access
    - moving_access
    - acoustic_buffer_from_service_routes
```

```text
Housing layout determines whether daily life feels close or exhausting.
```

### 20.2 Food Interface

```yaml
food_mobility_interface:
  required:
    - garden_to_kitchen_route
    - delivery_access
    - bulk_food_unloading
    - pantry_access
    - care_meal_delivery_routes
    - compost_route
    - grocery_fallback_trip_plan
```

```text
Food resilience depends on moving food without turning every meal into logistics.
```

### 20.3 Water Interface

```yaml
water_mobility_interface:
  required:
    - water_system_service_access
    - emergency_water_distribution_route
    - cistern_or_well_access
    - drought_delivery_route
```

```text
A water backup plan must include how water reaches people.
```

### 20.4 Sanitation Interface

```yaml
sanitation_mobility_interface:
  required:
    - waste_pickup_route
    - compost_route
    - hazardous_waste_transport
    - emergency_toilet_access
    - cleaning_supply_routes
```

```text
Waste routes should not cross the heart of daily dignity unless designed carefully.
```

### 20.5 Energy Interface

```yaml
energy_mobility_interface:
  required:
    - EV_or_shared_vehicle_charging
    - e_bike_charging
    - emergency_power_for_access_lighting
    - powered_gates_if_any
    - route_lighting
    - mobility_device_charging
```

```text
Mobility fails if the devices and shared vehicles are not charged when needed.
```

### 20.6 Care Interface

```yaml
care_mobility_interface:
  required:
    - accessible_dropoff
    - EMS_route
    - clinic_transport
    - pharmacy_pickup
    - medication_delivery
    - evacuation_of_high_need_residents
    - mobility_device_storage
```

```text
Care access fails when transport is improvised.
```

### 20.7 Maintenance Interface

```yaml
maintenance_mobility_interface:
  required:
    - contractor_access
    - tool_and_parts_routes
    - storm_clearance_priority_routes
    - service_vehicle_staging
    - path_maintenance
    - snow_leaf_mud_management
```

```text
A path that is not maintained is not a path.
```

### 20.8 Governance Interface

```yaml
governance_mobility_interface:
  required:
    - shared_vehicle_policy
    - driver_eligibility
    - parking_rules
    - accessibility_commitments
    - delivery_rules
    - emergency_authority
    - conflict_process_for_access_issues
```

```text
Mobility rules should protect access, not become status battles over parking.
```

### 20.9 Legal Land & Finance Interface

```yaml
legal_finance_mobility_interface:
  required:
    - easements
    - road_access_rights
    - parking_requirements
    - fire_access
    - ADA_FHA_local_accessibility_review
    - shared_vehicle_insurance
    - liability
    - transit_or_shuttle_contracts
```

```text
Access is legal as well as physical.
```

### 20.10 Labor & Time Interface

```yaml
labor_time_mobility_interface:
  required:
    - commute_reduction
    - errand_time_reduction
    - care_trip_time
    - vehicle_maintenance_labor
    - shuttle_driver_labor
    - path_maintenance_labor
```

```text
The best mobility system returns time before residents notice it exists.
```

---

## 21. Automation-Favoring Requirements

Automation should make mobility easy to coordinate, but not surveillance-heavy.

```yaml
automation_requirements:
  access_map_generator:
    required: true
    purpose:
      - accessible_route_map
      - emergency_route_map
      - service_route_map
      - walking_distance_map
      - care_transport_route

  distance_friction_calculator:
    required: true
    purpose:
      - measure_daily_trip_distance
      - identify burden hotspots
      - flag long paths
      - score common space access

  shared_vehicle_scheduler:
    required_where_shared_vehicle_exists: true
    purpose:
      - booking
      - maintenance
      - driver_eligibility
      - trip pooling
      - cost allocation

  shuttle_trip_planner:
    preferred: true
    purpose:
      - grocery_pharmacy_clinic_routes
      - transit_connection
      - recurring trip planning
      - demand aggregation

  delivery_manager:
    preferred: true
    purpose:
      - package notification
      - bulk delivery windows
      - cold chain items
      - service access

  emergency_access_dashboard:
    required: true
    purpose:
      - evacuation routes
      - high_need transport coverage
      - emergency vehicle clearance
      - shared vehicle fuel or charge status
      - route blockage alerts

  bike_cart_fleet_manager:
    preferred: true
    purpose:
      - checkout
      - maintenance
      - charging
      - repair
      - availability

  transportation_cost_calculator:
    required: true
    purpose:
      - private vehicle cost
      - shared vehicle cost
      - shuttle cost
      - housing_transport affordability
      - wage hour impact

  avoid:
    - tracking_resident_location_by_default
    - using_mobility_data_for_social_control
    - AI_denying_access_to_transport_without_appeal
    - hidden_priority_for_high_status_residents
    - car_free_scoring_that_ignores_disability
```

### Automation Principle

```text
Automate coordination, access visibility, cost comparison, and emergency readiness. Do not automate surveillance.
```

---

## 22. Mobility & Access Roles

```yaml
mobility_access_roles:
  mobility_steward:
    purpose: overall mobility system coordination
    required_backup: true

  accessibility_steward:
    purpose: accessible routes, barriers, accommodations, route audits
    required_backup: true

  shared_vehicle_steward:
    purpose: vehicle booking, maintenance, insurance, driver rules
    required_backup: true

  bike_cart_steward:
    purpose: cargo bikes, carts, storage, repairs, charging
    required_backup: true

  delivery_service_steward:
    purpose: package, freight, food, medicine, waste/service access coordination
    required_backup: true

  emergency_access_steward:
    purpose: EMS/fire routes, evacuation, high-need transport, route clearance
    required_backup: true

  external_connection_steward:
    purpose: transit, shuttle, clinic/pharmacy/grocery trips, regional access
    required_backup: true

  path_maintenance_steward:
    purpose: path surfaces, lighting, snow/ice/leaves/mud, benches, wayfinding
    required_backup: true
```

### Role Rule

```text
No resident's access to food, care, or safety should depend on one informal driver.
```

---

## 23. Scenario Simulations

The mobility and access module must support stress simulations.

```yaml
mobility_access_scenarios:
  normal_week:
    tests:
      - walking_distances
      - shared_vehicle_use
      - errand_time
      - care_transport
      - deliveries
      - parking_use
      - path_maintenance

  no_private_car_resident:
    tests:
      - grocery_access
      - pharmacy_access
      - clinic_access
      - social_access
      - employment_access
      - emergency_access

  wheelchair_or_mobility_device_resident:
    tests:
      - accessible_routes
      - grade
      - surface
      - bathroom_food_care_access
      - emergency_evacuation
      - snow_or_debris_clearance

  elder_high_need_resident:
    tests:
      - dropoff_distance
      - resting_points
      - care_room_access
      - transport_to_care
      - medication_pickup
      - evacuation_support

  illness_or_injury_week:
    tests:
      - temporary_mobility_loss
      - meal_delivery
      - care_transport
      - role_substitution
      - accessible routes

  severe_weather:
    tests:
      - path_blockage
      - route_clearance
      - delivery_delay
      - emergency_access
      - shared_vehicle_availability

  evacuation_event:
    tests:
      - vehicle_capacity
      - high_need_transport
      - pickup_points
      - route_blockage
      - communication
      - service_animals_and_medical_equipment

  shared_vehicle_failure:
    tests:
      - backup_vehicle
      - ride_service
      - trip rescheduling
      - clinic appointment risk
      - food procurement risk

  resident_growth:
    tests:
      - path congestion
      - parking pressure
      - vehicle pool sizing
      - shuttle demand
      - service access conflict
```

---

## 24. Mobility & Access Gates

The app should fail or warn based on mobility viability.

```yaml
mobility_access_gates:
  accessibility_gate:
    fail_if:
      - essential_spaces_not_connected_by_accessible_route
      - no_accessible_dropoff
      - no_plan_for_mobility_device_users
      - care_room_not_accessible
      - food_commons_not_accessible
      - evacuation_not_accessible

    warn_if:
      - accessible_routes_are_significantly_longer_than_nonaccessible_routes
      - resting_points_missing
      - weather_clearance_plan_missing

  car_dependency_gate:
    fail_if:
      - residents_need_private_car_for_daily_food_care_or_basic_needs
      - non_drivers_cannot_live_independently
      - site_isolated_without_shared_transport_plan

    warn_if:
      - monthly_transport_cost_erases_housing_savings
      - shared_vehicle_pool_underdeveloped
      - transit_or_shuttle_connection_weak

  emergency_access_gate:
    fail_if:
      - EMS_fire_access_unreviewed
      - no_evacuation_plan
      - no_high_need_transport_plan
      - service_vehicle_routes_block_emergency_routes
      - route_clearance_unassigned

  pedestrian_core_gate:
    fail_if:
      - internal_vehicles_can_move_fast_through_social_core
      - child_elder_commons_exposed_to_through_traffic
      - no_lighting_on_primary_routes
      - paths_create_hidden_or_unsafe_zones

    warn_if:
      - parking_dominates_core
      - path_distances_exceed_targets
      - service_routes_cross_primary_social_spaces

  cost_gate:
    fail_if:
      - transport_cost_unmodeled
      - shared_vehicle_insurance_unmodeled
      - parking_cost_unmodeled
      - shuttle_or_driver_labor_unmodeled

    warn_if:
      - parking_land_area_high
      - private_vehicle_costs_shifted_to_residents
      - shared_mobility_replacement_reserve_missing

  care_access_gate:
    fail_if:
      - no_clinic_pharmacy_transport_plan
      - no_medication_pickup_or_delivery_plan
      - no_EMS_route_to_care_room
      - high_need_residents_not_modeled

  delivery_service_gate:
    fail_if:
      - no_food_delivery_or_bulk_unloading_plan
      - no_waste_pickup_route
      - no_maintenance_vehicle_access
      - no_package_or_cold_chain_plan_where_needed

  labor_gate:
    fail_if:
      - mobility_system_requires_untracked_driver_labor
      - path_maintenance_labor_untracked
      - emergency_transport_depends_on_one_person

    warn_if:
      - shared_vehicle_admin_burden_high
      - shuttle_labor_unfunded
      - path_clearing_labor_exceeds_capacity

  privacy_gate:
    fail_if:
      - mobility_tracking_exposes_health_or_personal_status
      - shared_vehicle_data_used_for_social_control
      - high_need_transport_requests_public_by_default
```

---

## 25. App Modeling Boundary

The app should model mobility and access at the level of **site topology, path distances, accessibility, service routes, emergency access, shared mobility, cost, labor, and external connections**, not final civil engineering or traffic design.

### The App Should Model

```text
walking and rolling distances
accessible route coverage
path hierarchy
vehicle edge access
parking count and land use
emergency routes
delivery routes
waste/service routes
bike/cart network
shared vehicle pool
clinic/pharmacy/grocery access
transit/shuttle options
evacuation transport
transportation costs
mobility labor burden
weather and route maintenance
scenario failures
professional review requirements
```

### The App Should Not Claim to Solve by Default

```text
final road engineering
fire apparatus access approval
traffic engineering certification
ADA/FHA/local accessibility compliance certification
civil drainage design
parking code compliance
public road improvements
transit agency agreements
vehicle insurance underwriting
paratransit eligibility
driver employment classification
public right-of-way permitting
```

### Principle

```text
The app should identify what must be true for mobility dignity and access. Civil engineers, accessibility professionals, fire officials, insurers, local authorities, and transportation partners must validate implementation.
```

---

## 26. Required Data Model

```yaml
MobilityAccessCommons:
  id: string
  population_served: integer

  internal_network:
    pedestrian_first: boolean
    accessible_route_coverage_percent: number
    primary_path_length_meters: number
    max_unit_to_common_house_minutes: number
    max_unit_to_food_commons_minutes: number
    max_unit_to_care_room_minutes: number
    max_unit_to_accessible_dropoff_minutes: number
    lighting_primary_routes: boolean
    resting_points_count: integer
    path_weather_plan: boolean

  vehicle_access:
    perimeter_parking: boolean
    parking_spaces_total: integer
    accessible_parking_spaces: integer
    shared_vehicle_spaces: integer
    delivery_loading_zone: boolean
    maintenance_vehicle_access: boolean
    emergency_vehicle_access_review_status: unknown | required | reviewed | approved | failed
    service_routes_defined: boolean

  shared_mobility:
    shared_vehicle_count: integer
    accessible_shared_vehicle_available: boolean
    cargo_bikes_count: integer
    carts_count: integer
    e_bike_charging: boolean
    mobility_device_charging: boolean
    booking_system: boolean
    maintenance_plan: boolean
    insurance_review: boolean

  external_access:
    transit_access_status: none | weak | acceptable | strong
    shuttle_plan: boolean
    grocery_access_minutes: number
    pharmacy_access_minutes: number
    primary_care_access_minutes: number
    urgent_care_or_hospital_access_minutes: number
    clinic_transport_plan: boolean
    pharmacy_pickup_plan: boolean
    regional_bike_route_safety_status: unknown | poor | acceptable | strong
    delivery_service_available: boolean

  emergency_evacuation:
    EMS_route: boolean
    fire_access_review: boolean
    evacuation_plan: boolean
    high_need_transport_plan: boolean
    emergency_pickup_points: integer
    backup_route: boolean
    shared_vehicle_charge_or_fuel_tracking: boolean

  cost_labor:
    monthly_transport_cost_per_resident: number
    private_vehicle_dependency_score: number
    parking_land_area_m2: number
    shared_vehicle_admin_hours_per_month: number
    shuttle_driver_hours_per_month: number
    path_maintenance_hours_per_month: number
    errand_time_hours_per_resident_per_week: number
    commute_time_hours_per_resident_per_week: number

  automation:
    access_map_generator: boolean
    distance_friction_calculator: boolean
    shared_vehicle_scheduler: boolean
    shuttle_trip_planner: boolean
    delivery_manager: boolean
    emergency_access_dashboard: boolean
    bike_cart_fleet_manager: boolean
    transportation_cost_calculator: boolean

  outputs:
    mobility_dignity_status: pass | warn | fail
    accessibility_status: pass | warn | fail
    emergency_access_status: pass | warn | fail
    car_dependency_status: pass | warn | fail
    transportation_affordability_status: pass | warn | fail
    external_access_status: pass | warn | fail
    life_burden_reduction_score: number
    complexity_score: number
```

---

## 27. Required App Outputs

```yaml
required_outputs:
  - mobility_access_summary
  - internal_path_network_report
  - accessible_route_report
  - common_space_distance_report
  - vehicle_edge_access_report
  - parking_land_use_report
  - emergency_access_report
  - evacuation_transport_report
  - shared_vehicle_report
  - bike_cart_fleet_report
  - delivery_service_access_report
  - external_location_score
  - grocery_pharmacy_clinic_access_report
  - transportation_cost_report
  - housing_plus_transport_affordability_report
  - mobility_labor_burden_report
  - scenario_failure_report
  - professional_review_requirements
  - visualization_bundle_metadata
```

---

## 28. Visualization Requirements

The mobility module should export enough data for a virtual world, dashboard, or site simulator.

```yaml
visualization_requirements:
  spatial_objects:
    - primary_paths
    - secondary_paths
    - accessible_routes
    - courtyards
    - common_house
    - food_commons
    - care_room
    - accessible_dropoffs
    - emergency_routes
    - service_routes
    - delivery_zones
    - parking_edges
    - shared_vehicle_node
    - bike_cart_storage
    - transit_or_shuttle_pickup
    - evacuation_points
    - resting_points
    - route_lighting

  overlays:
    - walking_time
    - accessible_route_coverage
    - car_free_daily_needs
    - vehicle_conflict_zones
    - emergency_access
    - delivery_routes
    - high_need_transport
    - parking_land_area
    - path_maintenance_priority
    - route_blockage
    - transportation_cost
    - external_access_risk

  scenario_playback:
    - normal_week
    - no_private_car_resident
    - wheelchair_or_mobility_device_resident
    - elder_high_need_resident
    - illness_or_injury_week
    - severe_weather
    - evacuation_event
    - shared_vehicle_failure
    - resident_growth
```

---

## 29. Best Default Requirements Summary

```yaml
MinimumViableMobilityAccessCommons:
  population:
    first_serious_model: 80
    valid_range: 50-150

  philosophy:
    pedestrian_first_internal_life: true
    car_light_not_car_denial: true
    universal_access_required: true
    emergency_service_access_required: true
    non_driver_dignity_required: true
    transportation_cost_in_affordability: true

  internal_layout:
    pedestrian_core: required
    accessible_routes_to_all_essential_spaces: required
    common_house_within_short_walk_roll: required
    food_commons_within_short_walk_roll: required
    care_room_accessible: required
    shaded_lit_weather_resilient_paths: required
    resting_points: required

  edge_access:
    perimeter_parking: required
    accessible_dropoffs: required
    emergency_routes: required
    delivery_loading: required
    maintenance_vehicle_access: required
    shared_vehicle_node: required_where_external_access_car_dependent

  shared_mobility:
    carts: required
    bike_cargo_bike_storage: required
    shared_vehicle_pool: preferred_or_required_by_site
    accessible_transport_plan: required
    shuttle_or_transit_connection: preferred

  external_access:
    grocery_pharmacy_clinic_plan: required
    care_transport_plan: required
    transit_or_shuttle_review: required
    regional_bike_route_review: required
    evacuation_plan: required

  automation:
    access_map_generator: required
    distance_friction_calculator: required
    transportation_cost_calculator: required
    emergency_access_dashboard: required
    shared_vehicle_scheduler: required_where_shared_fleet_exists
    delivery_manager: preferred
    bike_cart_fleet_manager: preferred

  gates:
    accessibility_gate: required
    car_dependency_gate: required
    emergency_access_gate: required
    pedestrian_core_gate: required
    cost_gate: required
    care_access_gate: required
    delivery_service_gate: required
    labor_gate: required
    privacy_gate: required
```

---

## 30. Design Maxims

```text
Do not make every resident buy a car to access dignity.

Do not call land affordable if transportation costs eat the savings.

Do not make car-free ideology override disability, care, delivery, or emergency access.

Do not put parking at the heart of the village.

Do not make accessible routes longer, uglier, or more exposed than ordinary routes.

Do not make high-need residents depend on one informal driver.

Do not let service vehicles dominate daily life.

Do not hide transportation labor.

Do not make a rural site look cheap by ignoring grocery, pharmacy, clinic, and emergency access.

Put homes close to daily needs.

Put cars at the edge.

Put accessible dropoffs where bodies actually need them.

Put emergency routes in the plan from day one.

Put bikes and carts closer than cars.

Put transportation costs into affordability.

Make the non-driver life normal.

Make the path to care obvious.

Make movement feel like relief, not another tax.
```

---

## 31. Open Questions for Iteration

```text
1. Should the default prototype assume rural, peri-urban, or urban-edge land?
2. What maximum walking/rolling distance to the common house is acceptable?
3. Should shared vehicles be required in v0 or conditional on site isolation?
4. What private parking ratio should the app allow before warning?
5. Should the model include electric neighborhood vehicles or golf-cart-like mobility where legal?
6. Should bike/cargo-bike infrastructure be required even for rural sites?
7. How should the app score external access if transit is absent but shared vehicles are strong?
8. Should the system prefer sites near existing transit even if land cost is higher?
9. How should shuttle labor be paid or rotated?
10. Should emergency access geometry be modeled approximately or only flagged for professional review?
11. How should non-drivers participate in governance decisions about parking?
12. What mobility failure would make the entire CIaC design morally invalid?
```

---

## 32. Source Notes

The research basis for this draft includes:

- FHWA Complete Streets design model guidance.
- NACTO Urban Street Design Guide and shared street guidance.
- U.S. Access Board ADA Standards and accessible-route / ramp guidance.
- ITDP TOD Standard principles: Walk, Cycle, Connect, Transit, Mix, Densify, Compact, Shift.
- EPA Smart Growth principles.
- HUD Location Affordability Index and housing-plus-transportation affordability concepts.
- FHWA Bikeway Selection Guide.
- FEMA whole-community and access/functional needs transportation planning guidance.
