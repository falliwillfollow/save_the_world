# CIaC Deep Research Part 1: Scaling Thresholds and Node Actions

**Research ID:** `ciac_scaling_thresholds_part_1_v0_1`  
**Purpose:** Convert interdisciplinary evidence into provisional scale thresholds for CIaC modules.  
**Status:** First-pass research synthesis, not engineering, legal, health, or code certification.  
**Use:** Feed `module_registries`, `node_scaling`, `topology_optimizer`, world viewer warnings, and optimizer preferences.

---

## 0. Interpretation Rules

These thresholds are **decision heuristics**, not laws. Most evidence does not map cleanly onto CIaC because CIaC combines cohousing, cooperative housing, emergency planning, public-health infrastructure, elder-care design, skill lattices, local food systems, and civic governance. Where direct evidence is weak, this report labels the evidence quality accordingly.

### Evidence Quality Scale

```yaml
high:
  meaning: strong official guideline, regulatory threshold, or well-established professional standard

moderate:
  meaning: peer-reviewed evidence or consistent practice precedent, but not directly CIaC-specific

low:
  meaning: design practice, analogy, expert judgment, or weak/indirect evidence

mixed:
  meaning: evidence exists but points in different directions or depends heavily on context
```

### Scale Action Types

```yaml
resize:
  meaning: increase capacity of the same node

duplicate:
  meaning: add another local node of the same type

federate:
  meaning: create a higher-level coordination layer above multiple local nodes

hybrid:
  meaning: resize a core function, duplicate local access, and/or federate specialized capacity
```

---

## 1. Executive Threshold Summary

```yaml
natural_social_layers:
  intimate_support: 5
  close_operational_group: 8-12
  household_cluster: 10-24
  neighborhood_cell: 30-50
  village_block: 50-150
  district: 300-500
  town_city_layer: 900-1500
  regional_membrane: 1500+

core_CIaC_rule:
  - Do not scale one community indefinitely.
  - Replicate household/neighborhood cells before they become institutional.
  - Federate specialized services above the village-block layer.
```

The most useful model for CIaC is a **nested civic ecology**:

```text
room / unit
  -> household cluster
  -> residential pod
  -> village block
  -> district capability
  -> town/city layer
  -> regional membrane
```

---

## 2. Residential Life

```yaml
domain: residential_life
question: How many people can share one residential hall/building before privacy, sleep, conflict, perceived crowding, or stress degrade?
recommended_range:
  high_care_or_elder_household: 8-12 residents
  mixed_adult_residential_pod: 12-24 residents
  neighborhood_residential_cluster: 30-50 residents
  village_block_total: 50-150 residents
soft_threshold:
  - 24 residents per pod: begin warning for shared kitchen/lounge/bath/privacy load
  - 50 residents in one residential building/cluster: warn for institutional feel unless subdivided into houses/pods
  - 80-100 residents: require multiple residential pods, not one hall
hard_threshold:
  - 12 residents for high-care elder household before duplication
  - 30 residents per residential pod without sub-clustering
  - 150 residents as one social/residential unit
scale_action: hybrid
why: Small, home-like groups are better supported for elders/high-care residents; crowding harm depends on mismatch between residents, rooms, privacy, and design.
evidence_quality: moderate
sources:
  - WHO Housing and Health Guidelines
  - Green House / small-house nursing home model
  - Cohousing practice
  - Dunbar social-layer research
notes_for_CIaC:
  - Default residential pod should remain 12-24 residents.
  - High-care/elder pod should use 8-12 residents.
  - 80-person village block should be 4 residential pods of ~20.
  - UI warning: Residential node is exceeding pod scale. Duplicate residential cluster.
```

---

## 3. Mental Health and Social Scale

```yaml
domain: mental_health_social_scale
question: What group sizes support stable familiarity, trust, belonging, informal care, and low social overload?
recommended_range:
  support_circle: 5-8
  working_circle_or_close_care_group: 8-12
  familiar_social_cell: 15-30
  neighborhood_cell: 30-50
  village_block: 80-150
  district_federation: 300-500
  town_city_layer: 900-1500
soft_threshold:
  - 30 people: informal familiarity weakens unless subdivided
  - 50 people: social life needs multiple circles/nooks/rhythms
  - 150 people: do not expect whole-community intimacy
hard_threshold:
  - 150 residents: federate social/governance/care into multiple local cells
  - 500 residents: district layer required
  - 1500 residents: town/city layer and regional membrane required
scale_action: hybrid
why: Dunbar-style layers around 5, 15, 50, 150, 500, and 1500 are useful scaffolding. Perceived crowding is mediated by control, retreat, daylight, nature, and privacy.
evidence_quality: moderate
sources:
  - Dunbar social layers
  - WHO crowding guidance
  - Surgeon General loneliness advisory
  - Cohousing practice
notes_for_CIaC:
  - Use social cells, not one giant community.
  - UI should show: whole-community familiarity no longer expected above 150.
  - Optimizer should prefer duplicated commons/social pods above 150.
```

---

## 4. Common House / Third Place

```yaml
domain: common_house_third_place
question: How large can a common house or shared dining hall get before it stops functioning as a socially comfortable commons?
recommended_range:
  common_meal_group: 24-60 diners
  village_common_house: 50-100 residents served
  maximum_single_common_house_social_identity: 150 residents
  district_common_layer: multiple common houses plus specialized venues
soft_threshold:
  - 60 diners at once: warn that meal becomes dining-hall-like unless table clustering/service waves exist
  - 100 residents served by one common house: require sub-gathering spaces and open hours
  - 150 residents: duplicate neighborhood commons
hard_threshold:
  - 150 residents: one common house cannot be the only social heart
  - 300 residents: district needs multiple commons plus specialized venues
scale_action: hybrid
why: Cohousing common houses work because they support voluntary social life around private homes. Dining halls can scale food production but quickly feel institutional socially.
evidence_quality: low_to_moderate
sources:
  - Cohousing practice
  - Third-place theory
  - Campus/institutional dining as cautionary analogy
notes_for_CIaC:
  - Common house can resize up to village-block level, but duplicate above 150.
  - Dining can centralize production but decentralize eating/pickup.
  - UI warning: Common house is becoming institutional; add neighborhood commons.
```

---

## 5. Food Systems

```yaml
domain: food_systems
question: Which food functions scale centrally, and which should duplicate by neighborhood?
recommended_range:
  neighborhood_kitchen_or_food_commons: 50-100 residents
  shared_dining_comfort_zone: 24-60 diners per meal wave
  central_procurement_storage_node: 150-500 residents
  district_preservation_or_processing_node: 300-1500 residents
soft_threshold:
  - 80 residents per food commons: warn for kitchen/dining/labor scheduling
  - 100 residents per neighborhood kitchen: duplicate or add meal waves
  - 300 residents: add district procurement/preservation logistics
hard_threshold:
  - 150 residents per one shared kitchen/dining node
  - 500 residents without district food logistics
  - any shared food node without food-safety logs, allergen controls, cleaning schedule, and trained backup
scale_action: hybrid
why: Storage/procurement/cold storage/preservation can scale, but kitchens and dining create labor, hygiene, scheduling, and social bottlenecks.
evidence_quality: moderate
sources:
  - FDA Food Code 2022
  - Shared-use kitchen research
  - Cohousing common meal practice
notes_for_CIaC:
  - Keep food node max around 80-100 residents.
  - At 300+, add district procurement/preservation.
  - Protein Commons should be local for learning/acceptance but federated for advanced microbial/industrial layers.
```

---

## 6. Water Systems

```yaml
domain: water_systems
question: Which water systems duplicate for redundancy, which scale centrally, and what thresholds trigger public-health review?
recommended_range:
  emergency_access_point: within immediate neighborhood / 1-3 minute walk
  local_storage_or_distribution_node: 50-150 residents
  central_treatment_node: can scale if professionally operated and regulated
  emergency_potable_buffer: 1 gallon/person/day minimum emergency storage, 14 days preferred
  essential_health_water: 20 liters/person/day minimum emergency health/hygiene planning
soft_threshold:
  - 25 people served by a private/common drinking-water system: public water system review likely triggered in the US
  - 50-100 residents: duplicate emergency distribution points
  - 150 residents: do not rely on one access point or one operator
hard_threshold:
  - 25 people served 60 days/year: US public-water-system definition may apply
  - no tested potable source
  - no emergency potable reserve
  - no contamination response
  - no backup operator
scale_action: hybrid
why: Water can centralize technically, but access, emergency distribution, testing, and redundancy should be distributed. Public health review becomes central very early.
evidence_quality: high
sources:
  - EPA public water system definition
  - CDC emergency water storage guidance
  - WHO emergency water quantity guidance
  - EPA/CDC well testing guidance
  - EPA onsite non-potable water reuse guidance
notes_for_CIaC:
  - Duplicate emergency tanks/distribution points by neighborhood.
  - Federate treatment/operator oversight above village scale.
  - UI should flag public-water-system threshold around 25 people.
```

---

## 7. Sanitation and Waste

```yaml
domain: sanitation_waste
question: Which sanitation functions must remain decentralized, and which waste functions can centralize?
recommended_range:
  toilets: in-unit or within immediate residential pod
  emergency/communal toilet max: 20 people/toilet preferred emergency standard
  toilet_distance: under 50 meters as emergency maximum, much closer for dignity
  waste_dropoff: 15-50 meters depending stream and odor/pest risk
  compost_processing: village/district edge node
  hazardous_waste: centralized controlled node
soft_threshold:
  - any shared toilet more than 30-50 meters from dwelling: warn
  - more than 20 people per communal toilet in emergency: warn/fail depending context
  - more than 80-150 residents per sanitation cell: duplicate local access
hard_threshold:
  - no approved blackwater plan
  - no accessible toilets
  - no handwashing
  - no cleaning labor model
  - no pathogen-risk chain
  - no emergency sanitation fallback
scale_action: hybrid
why: Toilets, bathing, hygiene, and handwashing need local access. Compost, recycling, hazardous waste, and some treatment can centralize if safe and professionally reviewed.
evidence_quality: high_for_emergency_minima; moderate_for_CIaC_translation
sources:
  - Sphere Handbook WASH standards
  - UNHCR settlement planning
  - WHO Sanitation Safety Planning
notes_for_CIaC:
  - Duplicate toilets/bathing locally.
  - Centralize compost/hazardous waste only at service edge.
  - UI should distinguish emergency minimum from dignified normal.
```

---

## 8. Care and Health

```yaml
domain: care_health
question: How many people can one care room, health steward, or care team support, and when should care duplicate?
recommended_range:
  high_care_household: 8-12 residents
  care_room_neighborhood_service: 50-100 residents
  basic care steward / support liaison: 30-60 active high-touch cases, not all residents
  village_block_care_node: 80-150 residents
  district_clinic_partnership: 300-1500 residents
soft_threshold:
  - 80-100 residents per care room: warn for scheduling/privacy/illness separation
  - 150 residents: duplicate care room or add neighborhood care points
  - any high-care population concentrated without small-house logic: warn
hard_threshold:
  - no private/quiet care space
  - no medication continuity
  - no transport-to-care plan
  - no high-need resident function-based support
  - no backup care role
  - illness isolation impossible
scale_action: hybrid
why: High-care living needs small-house logic. Non-clinical care liaison functions can scale, but privacy, medication cold chain, illness support, and emotional safety require local duplication.
evidence_quality: moderate
sources:
  - Green House / small-house nursing home evidence
  - Community health worker evidence and caseload practice
  - CDC disability emergency preparedness guidance
notes_for_CIaC:
  - Care rooms duplicate by village block.
  - Advanced clinic partnerships federate at district layer.
  - UI should flag care privacy and high-need support, not just room count.
```

---

## 9. Governance

```yaml
domain: governance
question: What is the maximum useful size for direct assembly, consent circles, deliberation panels, and federated governance?
recommended_range:
  operational_decision_group: 5-7
  circle_or_stewardship_team: 5-12
  jury_or_appeal_panel: 12-24
  neighborhood_assembly: 30-80
  whole_village_membership_body: 50-150
  above_150: federated circles/councils
  above_500: district governance layer
  above_1500: town/city layer and regional membrane
soft_threshold:
  - 12 people in operational circle: warn for discussion efficiency
  - 24 people in deliberative panel: split or formal facilitation
  - 80 people in direct assembly: participation quality warning
  - 150 people: federation required
hard_threshold:
  - one assembly governs routine decisions above 150
  - one role controls money, records, conflict, or survival system
  - no due process
  - no emergency power sunset
  - no role backups
scale_action: federate
why: Small groups work better for discussion-rich decisions. Citizens' juries commonly use 12-24 people. Whole-population governance can remain for constitutional matters, but operations should federate.
evidence_quality: moderate
sources:
  - Citizens' jury resources
  - Collective intelligence decision guidance
  - Sociocracy practice
  - Dunbar social layers
notes_for_CIaC:
  - Direct governance should stop being default above 80-150.
  - Above 150, optimizer should federate by circle/neighborhood.
  - UI should show direct assembly burden rising.
```

---

## 10. Maintenance and Tools

```yaml
domain: maintenance_tools
question: Which maintenance functions centralize, which duplicate locally, and what service radius is acceptable?
recommended_range:
  daily_tool_access: within 1-3 minute walk
  neighborhood_tool_cache: 50-150 residents
  central_workshop: 150-500 residents
  advanced_workshop_fabrication: district layer 300-1500
  emergency_repair_supplies: duplicated by node
  specialist_repair: federated
soft_threshold:
  - 80-150 residents: one tool library/workshop begins to bottleneck
  - 300 residents: add district workshop/logistics
  - any Class A system without local spares/response role: warn
hard_threshold:
  - no asset registry
  - no critical spares
  - no professional handoff
  - no local emergency tools
  - one maintainer or one workshop supports 500+ residents without federation
scale_action: hybrid
why: Direct evidence is weak, but reliability practice is clear: critical repairs need local access and role backup; advanced tools can centralize. Duplication improves response but increases inventory burden.
evidence_quality: low_to_moderate
sources:
  - DOE/FEMP O&M guidance
  - EPA asset management for water/wastewater utilities
  - OSHA hazardous energy / lockout-tagout principles
notes_for_CIaC:
  - Duplicate emergency tools and common hand tools.
  - Federate advanced workshop.
  - UI should show response time risk and single workshop bottleneck.
```

---

## 11. Mobility and Access

```yaml
domain: mobility_access
question: What should be within 1, 3, 5, 10, and 15 minutes, especially for elders, children, disabled residents, and high-care households?
recommended_range:
  1_minute:
    - toilet/bathroom access for high-need residents
    - unit threshold / safe exit
    - emergency call/help point where relevant
  3_minutes:
    - common house or pod commons
    - care room/dropoff for high-need residents
    - accessible dropoff
    - emergency water distribution point
  5_minutes:
    - food commons
    - laundry
    - quiet room
    - workshop/tool cache
    - garden access
    - primary social commons
  10_minutes:
    - transit or shuttle stop target
    - district commons
    - larger workshop
    - market / public venue
    - clinic partnership node where feasible
  15_minutes:
    - larger regional amenities if transit/service is strong
soft_threshold:
  - 500 m / about 10 minutes to frequent transit
  - essential spaces exceeding 3-5 minutes for elders/high-need residents
  - accessible routes much longer than non-accessible routes
hard_threshold:
  - no accessible route to essential spaces
  - no emergency/service access
  - non-drivers cannot access food/care/pharmacy/clinic
  - transportation costs erase housing savings
scale_action: hybrid
why: TOD metrics use 500 m as roughly 10 minutes, but CIaC essential internal functions should be closer because residents include elders, disabled people, injured people, children, and care tasks.
evidence_quality: high_for_accessibility_law_and_TOD_metrics; moderate_for_CIaC_radius_translation
sources:
  - ITDP TOD Standard
  - ADA / U.S. Access Board accessibility standards
  - AARP livable communities resources
  - HUD Location Affordability concepts
notes_for_CIaC:
  - Essential floor functions should be within 3-5 minutes internally.
  - 10-minute threshold applies more to transit/district functions than bathrooms/food/care.
  - UI should show accessible distance penalty separately from raw distance.
```

---

## 12. Education / Skill / Work

```yaml
domain: education_skill_work
question: What learning group sizes work best for skill-sharing, apprenticeships, childcare, workshops, and peer learning?
recommended_range:
  peer_learning_group: 3-6
  hands_on_skill_group: 4-8
  apprenticeship_pair_or_triad: 1 mentor to 1-3 learners
  workshop_class: 8-12
  child_group_sizes:
    infants: max 8 with 1:4 ratio
    toddlers: max 12 with 1:6 ratio
    preschool: max 20 with 1:10 ratio
    kindergarten: max 24 with 1:12 ratio
  village_learning_node: 50-150 residents
  district_learning_partnership: 300-1500 residents
soft_threshold:
  - 8 learners in hands-on safety training: warn
  - 12 learners in tool/apprenticeship session: split
  - 150 residents without skill lattice and backup role tracking: warn
hard_threshold:
  - safety-critical task without training gate
  - one expert without backup
  - childcare group above best-practice ratios without professional review
  - training burden hidden from labor/time model
scale_action: hybrid
why: Small-group and peer-learning evidence favors small groups for active learning, often around 4-6. Apprenticeship depends on mentored practice. Childcare ratios are best-practice and often regulated.
evidence_quality: moderate_to_high
sources:
  - NAEYC staff-child ratio and class-size recommendations
  - Small-group active learning research
  - Department of Labor apprenticeship model
  - NIST NICE task/knowledge/skill structure
notes_for_CIaC:
  - Duplicate local skill nodes for onboarding and safety.
  - Federate advanced training partnerships.
  - UI should flag expert-dependency and expired training.
```

---

## 13. Emergency and Resilience

```yaml
domain: emergency_resilience
question: Which systems should duplicate for failure isolation, and how should fallback systems scale differently from normal systems?
recommended_range:
  local_buffers:
    - water
    - food
    - critical energy
    - emergency sanitation
    - first aid
    - communications
    - role backups
  federated_resilience:
    - district clinic partnership
    - advanced maintenance
    - legal/finance reserves
    - logistics
    - regional energy / watershed / hospitals
soft_threshold:
  - any critical function dependent on one node/operator
  - 150+ residents without replicated buffers
  - 300+ residents without district coordination
  - 1500 residents without regional membrane
hard_threshold:
  - no hazard register
  - no dependency graph
  - no recovery plan
  - no high-need resident emergency plan
  - no emergency power sunset
  - no reserve activation logic
scale_action: hybrid
why: NIST and FEMA emphasize critical functions, dependencies, cascading consequences, recovery goals, and whole-community planning. CIaC should use distributed local buffers and federate specialized response above the village block.
evidence_quality: high_for_resilience_framework; moderate_for_CIaC_thresholds
sources:
  - NIST Community Resilience Planning Guide
  - FEMA National Resilience Guidance
  - Sendai Framework for Disaster Risk Reduction
notes_for_CIaC:
  - Fallback systems must duplicate more than normal efficiency systems.
  - UI should show single point of failure and recovery objective missing.
```

---

## 14. CIaC Translation Matrix

| Module | Natural scaling type | Base node | Soft threshold | Hard threshold | Service-radius constraint | Primary driver | Optimizer preference |
|---|---:|---:|---:|---:|---|---|---|
| Residential pods | duplicate | 12-24 residents | 24/pod | 30/pod, 150/block | 1-3 min to pod commons | privacy, sleep, crowding | duplicate pod |
| Village block | hybrid | 50-150 residents | 100 | 150 | 3-5 min to essentials | familiarity, governance, access | replicate block |
| Common house | hybrid | 50-100 residents | 100 | 150 | 3-5 min | social comfort, access | duplicate neighborhood commons |
| Shared dining | duplicate/hybrid | 24-60 diners/wave | 60 | 100-150 | 3-5 min or pickup | institutional feel, labor | meal waves + duplicate dining |
| Food commons | hybrid | 50-100 residents | 80 | 150 | 3-5 min to pickup | labor, hygiene, food safety | duplicate kitchen/pickup; federate procurement |
| Protein commons | hybrid | 50-100 residents | 80 | 150 | food node adjacent | safety, acceptance, labor | duplicate simple layers; federate advanced protein |
| Potable water | hybrid | 50-150 local distribution | 25 triggers review | no tested source | 1-3 min emergency point | public health, redundancy | central reviewed source + duplicate reserves |
| Sanitation | duplicate/hybrid | toilets local, treatment central | 20 people/toilet emergency | >50m toilet emergency | ideally 1-3 min, emergency max 50m | hygiene, dignity | duplicate access; centralize treatment |
| Care room | duplicate/federate | 50-100 residents | 100 | 150 | 3-5 min | privacy, infection, high-need support | duplicate care rooms; federate clinic |
| Governance circle | federate | 5-12 | 12 | 24 for deliberation, 150 direct assembly | N/A | participation quality | circles + councils |
| Maintenance/tools | hybrid | 50-150 local cache | 150 | 300 without district workshop | 1-3 min daily tools | response time, autonomy | duplicate caches; federate advanced shop |
| Mobility/access | hybrid | village block | essentials >5 min | no accessible essential route | 1/3/5/10 min tiers | access, disability, time burden | duplicate centers before long travel |
| Education/skill | hybrid | 50-150 learning cell | 8 hands-on learners | no backup skill | 3-5 min for local learning | safety, competence | duplicate local skill nodes; federate credentials |
| Social/cultural | duplicate/hybrid | 30-80 social cell | 100 | 150 | 3-5 min | belonging, opt-out, clique risk | duplicate social nodes |
| Risk/resilience | hybrid | village block cell | 150 | 300 district needed | buffers local | cascade, recovery | duplicate buffers, federate coordination |

---

## 15. UI Warning Language

```yaml
residential_pod_over_soft:
  message: Residential pod is exceeding comfortable cluster size. Add another pod or subdivide.

common_house_over_soft:
  message: Common house is approaching institutional scale. Add neighborhood commons or meal waves.

food_node_over_soft:
  message: Food commons is approaching kitchen/labor bottleneck. Duplicate pickup/kitchen capacity.

water_review_trigger:
  message: Population may trigger public-water-system review. Require legal/public-health review.

sanitation_access_warning:
  message: Toilets or hygiene access exceed dignity/service-radius threshold.

care_node_warning:
  message: Care access, privacy, or illness separation may require another care room.

governance_over_soft:
  message: Direct assembly burden rising. Federate into circles or delegated roles.

maintenance_bottleneck:
  message: One workshop/tool node is serving too many residents. Add local tool cache or district workshop.

mobility_distance_warning:
  message: Essential daily functions exceed walk/roll threshold, especially for high-need residents.

education_skill_warning:
  message: Safety-critical roles lack trained backups or training group is too large.

resilience_single_point_failure:
  message: Critical function depends on one node, role, or external provider.
```

---

## 16. Recommended Next Research Parts

```yaml
part_2:
  title: Residential, mental health, and social architecture
  focus:
    - residential pod size
    - common house size
    - crowding mitigation
    - social group thresholds
    - private/common balance

part_3:
  title: Food, water, sanitation, and care service nodes
  focus:
    - service radius
    - public health thresholds
    - local duplication vs centralization
    - regulatory transitions

part_4:
  title: Governance, education, maintenance, mobility, and resilience
  focus:
    - group decision thresholds
    - training sizes
    - maintenance service layers
    - emergency duplication
    - federation thresholds

part_5:
  title: Repo implementation translation
  focus:
    - update module_registry node policies
    - update topology thresholds
    - UI warning messages
    - optimizer action preferences
    - tests
```

---

## 17. Primary Source List

- WHO Housing and Health Guidelines, household crowding and housing-health recommendations.
- Green House / small-house nursing home model research.
- Cohousing Association / cohousing design practice.
- Dunbar social-layer research.
- U.S. Surgeon General advisory on loneliness and social connection.
- FDA Food Code 2022.
- CDC emergency water storage guidance.
- WHO emergency water quantity guidance.
- EPA public water system definitions.
- EPA/CDC private well testing guidance.
- EPA onsite non-potable water reuse research.
- Sphere Handbook WASH standards.
- UNHCR settlement planning guidance.
- WHO Sanitation Safety Planning.
- NIST Community Resilience Planning Guide.
- FEMA National Resilience Guidance.
- Sendai Framework for Disaster Risk Reduction.
- ITDP TOD Standard.
- U.S. Access Board / ADA Accessibility Standards.
- NAEYC staff-child ratio and group-size recommendations.
- Citizens' Jury resources from Involve / Participedia / EPA.
- Collective intelligence decision-making guidance.
