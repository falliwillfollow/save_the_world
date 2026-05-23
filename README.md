# Civic Infrastructure as Code

CIaC is a Python/YAML/JSON toolkit for describing and stress-testing the minimum civic infrastructure a small commons would need to support dignified daily life.

The current demo target is a **5-household, 10-15 person rural or peri-urban micro-commons**. CIaC models infrastructure as structured civic patterns, compiles those patterns into a plan, runs provisional simulations and stress scenarios, and exports JSON that a richer visualization layer can consume.

It is deliberately cautious. CIaC is not a building manual, legal guide, engineering certification, public-health approval, permit package, cost estimate, or resident-consent process. The project is useful because it makes assumptions visible, not because it makes them true.

## What You Can Do

- Validate authored civic patterns, plans, profiles, scenarios, and reports.
- Compile a site profile plus infrastructure patterns into a dependency-aware civic plan.
- Simulate normal-year resource flows, maintenance, labor, storage, failures, and review blockers.
- Replay stress scenarios such as drought, contamination, energy outage, crop failure, sanitation failure, and labor loss.
- Evaluate water, food, energy, labor, governance, review, and foundation readiness reports.
- Generate candidate infrastructure configurations and run bounded optimizer search.
- Probe whether the same minimum-dignity model scales to 150 and 1500 people.
- Calibrate optimizer objectives and block unratified weight profiles.
- Export runtime and visualization bundles for a future web/game/Unreal-style viewer.

## Current Status

The micro-commons proof of concept has reached the current data-contract targets:

- Inspectable simulation proof of concept: `100%`
- Mature commune virtualization data contract: `100%`
- Faithful pattern optimization engine: `100%`

Those numbers mean the software/data contract is complete for the current proof of concept. They do not mean the modeled community is safe, legal, buildable, funded, consented to, or optimized in the real world.

The current optimizer can search, rank, calibrate, and then block unratified recommendations. The default weight governance report is intentionally `not_ratified`.

## Repository Map

- `ciac/`: Python package and CLI implementation.
- `schemas/`: JSON Schema-compatible public contracts.
- `patterns/`: authored civic infrastructure patterns.
- `examples/site_profiles/`: demo site profile.
- `seasonal_profiles/`, `household_profiles/`, `spatial_profiles/`: authored context profiles.
- `scenarios/`: stress scenario inputs.
- `water_plans/`, `food_plans/`, `energy_plans/`, `role_plans/`: subsystem plan inputs.
- `optimization_profiles/`, `calibration_profiles/`, `governance_profiles/`: optimizer control inputs.
- `viewer/`: static inspection viewer for generated runtime artifacts.
- `tests/`: regression tests for schemas, compiler, simulation, scenarios, reports, optimizer, and viewer contracts.
- `docs/`: project goals, metrics, backlog, and [sprint history](docs/sprint_history.md).

Generated outputs belong in `examples/generated/` and `reports/`. Those folders are intentionally ignored by git.

## Install

From the repository root:

```powershell
py -3.10 -m pip install -e .
```

Then verify the project:

```powershell
py -3.10 -m unittest discover -s tests
py -3.10 -m ciac validate patterns
```

## Quick Start

Create the generated-output folder:

```powershell
New-Item -ItemType Directory -Force examples/generated
```

Compile the demo micro-commons plan:

```powershell
py -3.10 -m ciac compile examples/site_profiles/micro_commons_5_households.yaml patterns --seasonal-profile seasonal_profiles/humid_temperate_provisional.yaml --household-profile household_profiles/micro_commons_households_v0.yaml --spatial-profile spatial_profiles/micro_commons_spatial_v0.yaml --output examples/generated/micro_commons_plan.json
```

Run the baseline simulation:

```powershell
py -3.10 -m ciac simulate examples/generated/micro_commons_plan.json --days 365 --output examples/generated/micro_commons_simulation.json
py -3.10 -m ciac simulate examples/generated/micro_commons_plan.json --days 14 --output examples/generated/baseline_14d_simulation.json
```

Run a stress scenario:

```powershell
py -3.10 -m ciac simulate examples/generated/micro_commons_plan.json --days 14 --scenario scenarios/water_contamination_response_v2.yaml --output examples/generated/water_contamination_response_v2_replay_simulation.json
```

Compare baseline and stress replay:

```powershell
py -3.10 -m ciac compare-simulations examples/generated/baseline_14d_simulation.json examples/generated/water_contamination_response_v2_replay_simulation.json --output examples/generated/water_contamination_response_v2_replay_comparison.json
```

## Optimization Path

The optimizer is intentionally transparent and bounded. It does not invent technology choices; it searches declared provisional tunables and preserves hard constraints, review locks, and governance status.

Food, water, and critical energy are treated as dignity floors, not quality-of-life knobs to turn down. The bounded search will not recommend lowering authored survival reserves to make cost, labor, or simplicity scores look better. Efficiency work should come from better production, storage health, distribution, transport, replenishment, repair, and reliability patterns.

Generate a candidate matrix:

```powershell
py -3.10 -m ciac candidate-matrix examples/generated/micro_commons_plan.json patterns optimization_profiles/minimum_dignity_v0.yaml --scenario scenarios/water_contamination_response_v2.yaml --scenario scenarios/crop_failure.yaml --scenario scenarios/energy_outage_reserve_v2.yaml --days 365 --output examples/generated/micro_commons_candidate_matrix.json
```

Run bounded search:

```powershell
py -3.10 -m ciac optimize-search examples/generated/micro_commons_plan.json patterns optimization_profiles/minimum_dignity_v0.yaml --scenario scenarios/water_contamination_response_v2.yaml --scenario scenarios/crop_failure.yaml --scenario scenarios/energy_outage_reserve_v2.yaml --days 365 --output examples/generated/micro_commons_search_optimizer_report.json
```

Probe scale pressure at 12, 150, and 1500 people:

```powershell
py -3.10 -m ciac tradeoff-scale examples/generated/micro_commons_plan.json examples/generated/micro_commons_candidate_matrix.json patterns scale_profiles/micro_commons_scale_targets_v0.yaml --output examples/generated/micro_commons_tradeoff_scale.json
```

Model infrastructure as node pools that can scale up or down:

```powershell
py -3.10 -m ciac node-scaling module_registries/micro_commons_default_v0.yaml --scale-profile scale_profiles/micro_commons_scale_targets_v0.yaml --output examples/generated/micro_commons_node_scaling.json
```

Add operator-selected populations to the report with `--people`:

```powershell
py -3.10 -m ciac node-scaling module_registries/micro_commons_default_v0.yaml --scale-profile scale_profiles/micro_commons_scale_targets_v0.yaml --people 978 --output examples/generated/micro_commons_node_scaling.json
```

The node scaling report treats each registry slot as a civic infrastructure node pool. At micro scale it prefers seed/default patterns; at village scale it activates one node; above node capacity it recommends replicated village nodes with narrow federation rather than one centralized megastructure.

CIaC's scaling posture is abundance-first: local dignity floors should reduce routine scarcity conflict and dependence on adversarial services. Governance, legal, consent, and review systems are modeled as boundary infrastructure, while district, town, city, and regional layers should add shared capability without replacing resilient local basics.

Recommend the next topology action for a population:

```powershell
py -3.10 -m ciac topology-recommend examples/generated/micro_commons_node_scaling.json --population 150 --food-labor examples/generated/micro_commons_food_labor_report.json --complexity examples/generated/micro_commons_complexity_report.json --output examples/generated/micro_commons_topology_recommendation.json
```

For a slider-selected population, pass the same number:

```powershell
py -3.10 -m ciac topology-recommend examples/generated/micro_commons_node_scaling.json --population 978 --food-labor examples/generated/micro_commons_food_labor_report.json --complexity examples/generated/micro_commons_complexity_report.json --output examples/generated/micro_commons_topology_recommendation_978.json
```

Topology recommendations are node-aware: they can choose scale-down seed mode, pre-plan a second village cell, replicate node pools, add district/town capability layers, federate a thin control plane, or reduce labor concentration.

Check that the generated viewer artifacts are coherent as one flow:

```powershell
py -3.10 -m ciac artifact-cohesion examples/generated --output examples/generated/micro_commons_artifact_cohesion.json
```

This report verifies the default viewer files exist, validate, and agree across report boundaries: optimizer selection to cycle iteration, calibration to weights, node-scaling population to topology recommendation, and duplicate non-canonical topology artifacts.

Make objective scoring inspectable:

```powershell
py -3.10 -m ciac objective-calibration examples/generated/micro_commons_search_optimizer_report.json calibration_profiles/minimum_dignity_objectives_v0.yaml --output examples/generated/micro_commons_objective_calibration.json
```

Evaluate weight governance:

```powershell
py -3.10 -m ciac weight-governance optimization_profiles/minimum_dignity_v0.yaml examples/generated/micro_commons_objective_calibration.json governance_profiles/minimum_dignity_weights_draft_v0.yaml --output examples/generated/micro_commons_weight_governance.json
```

The final command currently exits with `1` because the demo weights are not ratified. That is expected and healthy.

Materialize the selected search candidate into a next-cycle runtime bundle:

```powershell
py -3.10 -m ciac apply-search-candidate examples/generated/micro_commons_plan.json examples/generated/micro_commons_search_optimizer_report.json --review-status examples/generated/micro_commons_review_status.json --scenario scenarios/water_contamination_response_v2.yaml --scenario scenarios/crop_failure.yaml --scenario scenarios/energy_outage_reserve_v2.yaml --pattern-dir patterns --optimization-profile optimization_profiles/minimum_dignity_v0.yaml --days 365 --output examples/generated/micro_commons_cycle_iteration.json
```

This produces a `CycleIterationReport` with the applied plan, fresh simulation, re-run stress scenarios, an applied runtime bundle, and a next search report nested inside it. The default authority mode is `operator_directed`: a single user may iterate provisional model changes for objective improvement inside the simulator, while real-world promotion remains blocked until review, consent, and safety duties are satisfied.

## Viewer

The viewer consumes generated runtime artifacts. To inspect only, a plain static server works. To persist completed webapp year runs and regenerate population-specific backend reports from the webapp state, use the CIaC viewer server:

```powershell
py -3.10 -m ciac viewer-server --port 8765
```

Then open:

```text
http://localhost:8765/viewer/
```

The viewer is an inspection surface for JSON outputs. It is not a site plan, safety claim, permit artifact, or approval workflow.

When served through `ciac viewer-server`, each completed webapp year writes `examples/generated/micro_commons_viewer_session_report.json`, runs the simulator from the webapp population context, materializes the selected search candidate into `examples/generated/micro_commons_cycle_iteration.json`, and regenerates food labor, complexity, node-scaling, topology recommendation, and artifact-cohesion reports for the active population. The browser slider and completed run are the configured state for those layers; terminal commands are still available for development, but are not required for the viewer testing loop.

The current viewer also loads the generated optimizer artifacts when available. The Optimization panel shows the selected search candidate, how it differs from the all-current plan, the objective calibration status, and the weight-governance blocker that prevents draft weights from being treated as approved recommendations.

The Cycle panel demonstrates the intended usability loop: run one simulated year in about 20 seconds, review the recommended change, submit it, and run the next cycle. If `examples/generated/micro_commons_cycle_iteration.json` exists, the next cycle switches to the applied runtime bundle from that report.

Each completed webapp year writes a `ViewerRunReport` when served with `ciac viewer-server`. If the viewer is served with `python -m http.server`, runs are recorded in browser storage only and Codex cannot inspect them as generated artifacts.

When served with `ciac viewer-server`, each completed webapp year also regenerates the population-dependent reports used by the Scalability panel: node scaling, topology recommendation, and artifact cohesion. This keeps browser runs and generated logs aligned without manually running terminal commands after each test.

The Involuntary Labor panel shows the current optimization direction: reduce mandatory commons upkeep after food, water, shelter, sanitation, and critical energy dignity floors are protected. The remaining capacity is not total free time, because the simulator intentionally does not yet model food preparation choices, sleep quality, self-education, outside work, private household labor, or voluntary social contribution.

## Common Commands

Validate a file or directory:

```powershell
py -3.10 -m ciac validate patterns
py -3.10 -m ciac validate optimization_profiles
py -3.10 -m ciac validate calibration_profiles
py -3.10 -m ciac validate governance_profiles
py -3.10 -m ciac validate tech_modules
```

Pressure-test an evidence-backed sustainability technology module:

```powershell
py -3.10 -m ciac technology-pressure-test examples/generated/micro_commons_plan.json tech_modules/agrivoltaic_shade_pasture_water_efficiency.yaml --output examples/generated/agrivoltaic_shade_pasture_water_efficiency_pressure_test.json
```

Technology modules are how CIaC will ingest published sustainability methods. A module must preserve dignity floors first; then it can expose evidence-backed performance statistics and modeled impacts for later multivariate simulation. The first seed module uses published agrivoltaics field data as evidence, but does not count pasture biomass as human food until a crop/nutrition conversion model exists.

The first housing module spec lives at `docs/module_reports/ciac_housing_module_dignified_village_block.md`. Its current infrastructure implementation is the `dignified_village_block` civic pattern: a repeatable, pod-based housing block that preserves private lockable units while pooling common-house, food, laundry, workshop, care, and courtyard infrastructure. It is available for scale modeling, but the 5-household demo still uses `starter_dwelling` until a dedicated larger-site profile is authored.

The first food module spec lives at `docs/module_reports/ciac_food_module_hybrid_food_commons.md`. Its current infrastructure implementation is the `hybrid_food_commons` civic pattern: a village-scale food hub that combines voluntary shared meals, regional staple procurement, onsite fresh production, pantry/cold/preserved storage, food-safety controls, and private food autonomy. It is available for 50-150 resident scale modeling, while the 5-household demo keeps the simpler kitchen, greenhouse, and staple-reserve pieces.

The first water module spec lives at `docs/module_reports/ciac_water_module_resilient_water_commons.md`. Its current infrastructure implementation is the `resilient_water_commons` civic pattern: a conservative village-scale water commons that keeps potable water reviewed and boring, uses rainwater as a nonpotable resilience layer, tracks emergency storage, and makes metering, leak detection, drought response, testing, and backup power explicit interfaces. It is available for 50-150 resident scale modeling, while the 5-household demo keeps the smaller well, rainwater, and emergency-reserve pieces.

The first sanitation and waste module spec lives at `docs/module_reports/ciac_sanitation_waste_module_hygienic_circular_commons.md`. Its current infrastructure implementation is the `hygienic_circular_commons` civic pattern: a village-scale sanitation and waste operations layer that keeps blackwater conservative and reviewed, supports dignified toilet and bathing access, separates organics and material streams, protects hazardous and medical waste paths, and makes cleaning, PPE, role backup, and unpleasant labor visible. It is available for 50-150 resident scale modeling, while the 5-household demo keeps the smaller shared bathhouse and composting pieces.

The first energy module spec lives at `docs/module_reports/ciac_energy_module_critical_load_energy_commons.md`. Its current infrastructure implementation is the `critical_load_energy_commons` civic pattern: a village-scale energy commons that reduces demand first, uses grid and solar where viable, stores energy for critical loads, exposes outage runtime and load shedding, and keeps battery, fire, interconnection, thermal, and electrical review explicit. It is available for 50-150 resident scale modeling, while the 5-household demo keeps the smaller solar shed and critical-load reserve pieces.

The first maintenance and repair module spec lives at `docs/module_reports/ciac_maintenance_repair_module_maintainable_commons_spine.md`. Its current infrastructure implementation is the `maintainable_commons_spine` civic pattern: a village-scale maintenance system that turns asset registry, work orders, spare parts, tool access, professional handoff, safety boundaries, backlog visibility, labor tracking, and budget reserves into first-class infrastructure. It is available for 50-150 resident scale modeling, while the 5-household demo keeps the smaller tool library and workshop pieces.

The first governance and anti-capture module spec lives at `docs/module_reports/ciac_governance_anticapture_module_commons_stewardship_protocol.md`. Its current infrastructure implementation is the `commons_stewardship_protocol` civic pattern: a resident-governed commons protocol that protects core assets, defines membership and exit rights, separates decision domains, delegates operations to circles, requires finance transparency, limits emergency authority, and keeps conflict, privacy, and anti-capture safeguards explicit. It is available for 50-150 resident scale modeling; real-world legal form, consent, and governance ratification remain external review requirements.

The first labor and time module spec lives at `docs/module_reports/ciac_labor_time_module_life_burden_ledger.md`. Its current infrastructure implementation is the `life_burden_ledger` civic pattern: a total-life-burden accounting layer that compares conventional and CIaC weeks, separates wage work from commons work, counts care, maintenance, governance, emergency, and private labor, protects free and passion time, and flags hidden labor, unfair concentration, burnout, and bad-week burden. It is available for 50-150 resident scale modeling; resident consent, privacy, accommodation, and labor fairness review remain external requirements.

The first legal, land, and finance module spec lives at `docs/module_reports/ciac_legal_land_finance_module_anti_speculative_civic_floor.md`. Its current infrastructure implementation is the `anti_speculative_civic_floor` civic pattern: an anti-speculative stewardship layer that separates land control, resident tenure, operating commons, capital stack, reserves, debt risk, insurance, tax, securities review, and affordability drift so the civic floor cannot quietly become an extraction machine. It is available for 50-150 resident scale modeling; final entity selection, legal documents, financing, tax treatment, insurance, zoning, and fundraising compliance remain external professional review requirements.

The first materials and fabrication module spec lives at `docs/module_reports/ciac_materials_fabrication_module_standardized_low_burden_build_system.md`. Its current infrastructure implementation is the `standardized_low_burden_build_system` civic pattern: a repeatable build-system layer for panelized or hybrid timber construction, structural grids, wet cores, service spines, prefab-ready BOMs, fabrication handoff, low-toxicity material palettes, embodied-carbon tracking, salvage planning, and maintenance-access metadata. It is available for 50-150 resident scale modeling; final structural engineering, fire/code approval, envelope/moisture design, fabrication shop drawings, permits, warranties, and contractor means and methods remain external professional responsibilities.

The first mobility and access module spec lives at `docs/module_reports/ciac_mobility_access_module_pedestrian_first_access_commons.md`. Its current infrastructure implementation is the `pedestrian_first_access_commons` civic pattern: a car-light access layer that prioritizes walking, rolling, universal routes, short internal distances, perimeter vehicle access, shared carts/bikes/vehicles, delivery/service routes, emergency access, care trips, evacuation planning, and transportation cost visibility. It is available for 50-150 resident scale modeling; final civil engineering, fire apparatus access, accessibility compliance, insurance, parking code, transit/shuttle contracts, and public right-of-way approvals remain external professional responsibilities.

The first education and skill module spec lives at `docs/module_reports/ciac_education_skill_module_civic_skill_lattice.md`. Its current infrastructure implementation is the `civic_skill_lattice` civic pattern: a role-based learning layer for resident onboarding, task/knowledge/skill mapping, safety training gates, apprenticeships, practice logs, backup-role development, knowledge-base continuity, external credential boundaries, and learning-burden visibility. It is available for 50-150 resident scale modeling; final schooling compliance, professional licensing, OSHA-like certification, food safety certification, medical training, employment credentialing, and child/youth education obligations remain external review requirements.

The first social and cultural commons module spec lives at `docs/module_reports/ciac_social_cultural_commons_module_belonging_without_coercion.md`. Its current infrastructure implementation is the `belonging_without_coercion_commons` civic pattern: a low-coercion belonging layer for third places, optional common meals, quiet rooms, arts and making, resident-led events, cultural pluralism, hospitality, anti-clique access, opt-out protection, aggregate loneliness support, and social labor visibility. It is available for 50-150 resident scale modeling; friendship, religion, therapy, mental health diagnosis, abuse investigation, public-event permitting, and personal happiness remain outside app authority and require appropriate human or professional processes.

The first risk and resilience module spec lives at `docs/module_reports/ciac_risk_resilience_module_graceful_degradation_engine.md`. Its current infrastructure implementation is the `graceful_degradation_engine` civic pattern: a whole-system resilience layer for hazard registers, critical function maps, dependency graphs, service levels, scenario libraries, buffers, early warnings, emergency modes, recovery playbooks, after-action learning, climate adaptation, high-need resident protection, and anti-capture checks under stress. It is available for 50-150 resident scale modeling; official emergency management certification, fire/public-health authority decisions, insurance underwriting, clinical triage, law enforcement, utility planning, and legal emergency powers remain outside app authority.

Evaluate which infrastructure slots are modular and ready for research-backed swaps:

```powershell
py -3.10 -m ciac module-compatibility examples/generated/micro_commons_plan.json module_registries/micro_commons_default_v0.yaml --technology-module tech_modules/agrivoltaic_shade_pasture_water_efficiency.yaml --output examples/generated/micro_commons_module_compatibility.json
```

The registry describes the default posture for water, food, energy, and sanitation, then lists the interfaces a preauthored module must satisfy to become drag-and-drop. Planning-phase research can use the registry's interface requirements without making research discovery part of the yearly application loop.

Generate evidence-search briefs from model bottlenecks:

```powershell
py -3.10 -m ciac research-needs examples/generated/micro_commons_plan.json examples/generated/micro_commons_simulation.json --module-registry module_registries/micro_commons_default_v0.yaml --output examples/generated/micro_commons_research_needs.json
```

The first generated brief is `food_local_production_gap_v0`: the greenhouse produces food, but not enough to prevent annual staple-reserve drawdown. Treat this as planning-phase evidence work, not an automatic request from the application to search the web or rewrite the plan.

Evaluate whether a discovered module can scale inside CIaC:

```powershell
py -3.10 -m ciac scalability-gate examples/generated/micro_commons_plan.json tech_modules/agrivoltaic_shade_pasture_water_efficiency.yaml --module-registry module_registries/micro_commons_default_v0.yaml --output examples/generated/agrivoltaic_shade_pasture_water_efficiency_scalability_gate.json
```

The agrivoltaics seed has published evidence and preserves dignity floors, but currently fails scalability because CIaC lacks edible-serving, labor, and crop-specific adapter interfaces for it. That is intentional: modules must pass gates before optimization can use them.

Evaluate module-contract complexity before scaling the village model:

```powershell
py -3.10 -m ciac complexity-report module_registries/micro_commons_default_v0.yaml patterns --output examples/generated/micro_commons_complexity_report.json
```

The complexity report uses the registry's reusable interface bundles and module tiers to show which slots have large contract surfaces, heavy dependency fan-out, high review burden, or recurring labor pressure. It is a scalability diagnostic, not a reason to delete dignity, safety, privacy, or review requirements.

Evaluate whether the village food commons hides too much recurring labor:

```powershell
py -3.10 -m ciac food-labor module_registries/micro_commons_default_v0.yaml patterns --output examples/generated/micro_commons_food_labor_report.json
```

The food labor report decomposes `hybrid_food_commons` into procurement, storage, preservation, common meal, cleanup, garden coordination, safety, and scheduling work. It checks per-resident weekly burden and shows why food should replicate as village nodes above roughly 150 residents instead of becoming one centralized kitchen.

Materialize a module into a provisional implemented simulation candidate:

```powershell
py -3.10 -m ciac implement-module examples/generated/micro_commons_plan.json tech_modules/agrivoltaic_shade_pasture_water_efficiency.yaml --module-registry module_registries/micro_commons_default_v0.yaml --days 365 --output examples/generated/agrivoltaic_module_implementation.json
```

This command refuses to alter the plan unless a preauthored module passes the scalability gate and declares explicit direct simulator effects such as `food_servings_per_day`, `water_liters_per_day`, and `energy_kwh_per_day`. A blocked report is a successful safety outcome: it means CIaC preserved the boundary between planning evidence and executable infrastructure assumptions.

Evaluate subsystem plans:

```powershell
py -3.10 -m ciac water examples/generated/micro_commons_plan.json water_plans/micro_commons_water_reserve_v2.yaml --output examples/generated/micro_commons_water_v2.json
py -3.10 -m ciac energy examples/generated/micro_commons_plan.json energy_plans/micro_commons_energy_reserve_v2.yaml --output examples/generated/micro_commons_energy_v2.json
py -3.10 -m ciac nutrition examples/generated/micro_commons_plan.json food_plans/micro_commons_basic.yaml --output examples/generated/micro_commons_nutrition.json
py -3.10 -m ciac roles examples/generated/micro_commons_plan.json role_plans/micro_commons_roles_v2.yaml --output examples/generated/micro_commons_roles_v2.json
```

Export a visualization handoff bundle:

```powershell
py -3.10 -m ciac export-visualization examples/generated/micro_commons_runtime_bundle.json examples/generated/micro_commons_foundation_gate.json examples/generated/micro_commons_candidate_matrix.json examples/generated/micro_commons_tradeoff_scale.json examples/generated/micro_commons_optimizer_report.json --output examples/generated/micro_commons_visualization_bundle.json
```

## How To Read The Outputs

CIaC reports use conservative language:

- `pass` means the current model did not find a tracked blocker.
- `warn` means the issue is visible and should stay visible.
- `fail` means the model found a blocking condition under the current assumptions.
- `ready_with_warnings` means suitable for inspection, not real-world approval.
- `provisional` means the value or conclusion still needs evidence, review, or governance.

If an output says review, engineering, public health, legal, or resident consent is required, CIaC is naming a stop condition. It is not satisfying it.

## Documentation

- [Simulation foundation goal](docs/simulation_foundation_goal.md): the project’s current target and complexity gate.
- [Rolling progress metrics](docs/progress_metrics.md): what the completion percentages mean.
- [Modeling backlog](docs/modeling_backlog.md): candidate future work and triage rules.
- [Sprint history](docs/sprint_history.md): the implementation timeline that used to live in this README.

## Development Notes

Python 3.10 is the target runtime. The package dependencies are intentionally small: `PyYAML` and `jsonschema`.

Run all tests:

```powershell
py -3.10 -m unittest discover -s tests
```

Generated artifacts are disposable and ignored by git. The authored source of truth is the Python package, schemas, YAML inputs, docs, tests, and viewer files.
