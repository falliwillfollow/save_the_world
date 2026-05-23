# Civic Infrastructure as Code

CIaC is a Python/YAML/JSON toolkit for modeling the minimum civic infrastructure a small or scaling commons would need to support dignified daily life.

The project treats infrastructure as inspectable civic patterns: water, food, energy, shelter, sanitation, labor, governance, review duties, and modular technology candidates. It compiles those patterns into plans, runs provisional simulations and stress scenarios, searches bounded improvements, and exports runtime bundles for a visual inspection layer.

CIaC is deliberately cautious. It is not a building manual, engineering certification, permit package, health approval, legal opinion, finance plan, or resident-consent process. Its value is making assumptions, flows, bottlenecks, and review blockers visible.

## Current Capabilities

- Validate authored patterns, module registries, profiles, scenarios, and generated reports.
- Compile the demo micro-commons from site, seasonal, household, spatial, and pattern inputs.
- Simulate normal-year resource flows with production, use, storage release/refill, curtailment, maintenance, labor, and failure/review states.
- Replay stress scenarios such as drought, water contamination, crop failure, energy outage, sanitation failure, and labor loss.
- Search bounded optimizer candidates while preserving dignity floors and review locks.
- Materialize selected search candidates into cycle reports and runtime bundles.
- Scale node pools from seed scale through village and larger populations, including ad hoc slider-selected populations.
- Recommend node-aware topology actions such as scale-down, replicate village cells, add district/town layers, or reduce labor concentration.
- Serve a web viewer that runs yearly inspection cycles, persists completed browser runs, and regenerates backend artifacts for the active population.
- Export viewer-ready resource timelines that expose source, use, net flow, reserve release, reserve refill, curtailed surplus, capacity, and percent-full storage.

## Repository Map

- `ciac/`: Python package and CLI.
- `schemas/`: public JSON/YAML contracts.
- `patterns/`: authored civic infrastructure patterns.
- `module_registries/`: module slots, interfaces, node sizing, and scale posture.
- `examples/site_profiles/`: demo site profile.
- `seasonal_profiles/`, `household_profiles/`, `spatial_profiles/`: context profiles.
- `scenarios/`: stress scenario inputs.
- `optimization_profiles/`, `calibration_profiles/`, `governance_profiles/`: optimizer controls and governance checks.
- `water_plans/`, `food_plans/`, `energy_plans/`, `role_plans/`: subsystem plans.
- `viewer/`: browser inspection app.
- `docs/`: vision notes, module reports, progress notes, and sprint history.
- `tests/`: regression tests for compiler, schemas, simulation, optimizer, viewer, scaling, and report contracts.

Generated outputs belong in `examples/generated/` and `reports/`. They are disposable and ignored by git.

## Install

```powershell
py -3.10 -m pip install -e .
```

Verify the project:

```powershell
py -3.10 -m unittest discover -s tests
py -3.10 -m ciac validate patterns
```

## Quick Start

Create the generated-output folder:

```powershell
New-Item -ItemType Directory -Force examples/generated
```

Compile the demo plan:

```powershell
py -3.10 -m ciac compile examples/site_profiles/micro_commons_5_households.yaml patterns --seasonal-profile seasonal_profiles/humid_temperate_provisional.yaml --household-profile household_profiles/micro_commons_households_v0.yaml --spatial-profile spatial_profiles/micro_commons_spatial_v0.yaml --output examples/generated/micro_commons_plan.json
```

Run a baseline year:

```powershell
py -3.10 -m ciac simulate examples/generated/micro_commons_plan.json --days 365 --output examples/generated/micro_commons_simulation.json
```

Run a stress replay:

```powershell
py -3.10 -m ciac simulate examples/generated/micro_commons_plan.json --days 365 --scenario scenarios/water_contamination_response_v2.yaml --output examples/generated/water_contamination_response_v2_replay_simulation.json
```

Export a runtime bundle for the viewer:

```powershell
py -3.10 -m ciac export-runtime examples/generated/micro_commons_plan.json examples/generated/micro_commons_simulation.json --output examples/generated/micro_commons_runtime_bundle.json
```

## Viewer Loop

Start the CIaC viewer server:

```powershell
py -3.10 -m ciac viewer-server --port 8765
```

Open:

```text
http://localhost:8765/viewer/
```

The viewer is the active inspection loop. It loads generated artifacts, lets the operator choose a population on the slider, runs a simulated year, records the completed browser run, and regenerates population-specific backend artifacts from the same configured state.

When served through `ciac viewer-server`, a completed webapp year writes or refreshes artifacts such as:

- `examples/generated/micro_commons_viewer_session_report.json`
- `examples/generated/micro_commons_cycle_iteration.json`
- `examples/generated/micro_commons_runtime_bundle.json`
- `examples/generated/micro_commons_node_scaling.json`
- `examples/generated/micro_commons_topology_recommendation.json`
- `examples/generated/micro_commons_food_labor_report.json`
- `examples/generated/micro_commons_complexity_report.json`
- `examples/generated/micro_commons_artifact_cohesion.json`

The browser slider population is therefore not just a UI decoration. It becomes the active population context used by simulation, node scaling, topology, food labor, cycle review, and artifact-cohesion checks.

## Resource Semantics

The viewer resource cards show reserves, not magic totals. For water, food, and energy, the UI exposes:

- current stored reserve and capacity
- percent full and per-resident storage
- daily source, use, and net flow
- reserve release when daily source is insufficient
- reserve refill when daily source exceeds use
- curtailed surplus when storage is already full
- unmet demand when source plus reserve cannot cover use

This means a stable water number can be correct if natural source flow is covering daily use while storage remains full. Once demand exceeds source, storage declines; once source exceeds demand again, storage refills. The runtime bundle now carries these moving parts explicitly so a future visual layer can show the system without hidden water or opaque balances.

## Capability Semantics

Resource simulation tracks water, food, energy, storage, and flows. Capability simulation tracks non-resource civic conditions such as governance, labor, care, access, legal-finance resilience, skill coverage, social/coercion risk, and graceful degradation.

Capability outputs are provisional modeling aids. They do not satisfy professional review, legal review, resident consent, accessibility compliance, safety validation, or real-world trust. See [Capability State Layer](docs/capability_state_layer.md).

## Scaling And Topology

CIaC models infrastructure as node pools rather than one endlessly growing facility. At small scale, some slots can remain seed/default patterns. At village scale, slots activate node counts. Above node capacity, the model prefers replicated village cells and thin federation over centralized megastructures.

Generate node scaling for authored and ad hoc populations:

```powershell
py -3.10 -m ciac node-scaling module_registries/micro_commons_default_v0.yaml --scale-profile scale_profiles/micro_commons_scale_targets_v0.yaml --people 730 --output examples/generated/micro_commons_node_scaling.json
```

Recommend topology for the active population:

```powershell
py -3.10 -m ciac topology-recommend examples/generated/micro_commons_node_scaling.json --population 730 --food-labor examples/generated/micro_commons_food_labor_report.json --complexity examples/generated/micro_commons_complexity_report.json --output examples/generated/micro_commons_topology_recommendation.json
```

The scaling posture is abundance-first: local dignity floors should reduce routine scarcity and dependency while larger layers add shared capability, review, and coordination.

## Optimization And Cycles

The optimizer searches declared tunables. It does not invent infrastructure, erase review duties, or lower survival reserves to make a score look better.

Run bounded search:

```powershell
py -3.10 -m ciac optimize-search examples/generated/micro_commons_plan.json patterns optimization_profiles/minimum_dignity_v0.yaml --scenario scenarios/water_contamination_response_v2.yaml --scenario scenarios/crop_failure.yaml --scenario scenarios/energy_outage_reserve_v2.yaml --days 365 --output examples/generated/micro_commons_search_optimizer_report.json
```

Materialize the selected candidate into a cycle report:

```powershell
py -3.10 -m ciac apply-search-candidate examples/generated/micro_commons_plan.json examples/generated/micro_commons_search_optimizer_report.json --review-status examples/generated/micro_commons_review_status.json --scenario scenarios/water_contamination_response_v2.yaml --scenario scenarios/crop_failure.yaml --scenario scenarios/energy_outage_reserve_v2.yaml --pattern-dir patterns --optimization-profile optimization_profiles/minimum_dignity_v0.yaml --days 365 --output examples/generated/micro_commons_cycle_iteration.json
```

Cycle reports include the applied plan, fresh simulation, stress replays, runtime bundle, next search report, and operator/review blockers. Failed applied simulations are blocked from acceptance.

## Useful Checks

Validate authored inputs:

```powershell
py -3.10 -m ciac validate patterns
py -3.10 -m ciac validate module_registries
py -3.10 -m ciac validate scale_profiles
py -3.10 -m ciac validate seasonal_profiles
py -3.10 -m ciac validate household_profiles
py -3.10 -m ciac validate spatial_profiles
py -3.10 -m ciac validate scenarios
py -3.10 -m ciac validate optimization_profiles
py -3.10 -m ciac validate calibration_profiles
py -3.10 -m ciac validate governance_profiles
```

Check generated viewer artifacts as one coherent flow:

```powershell
py -3.10 -m ciac artifact-cohesion examples/generated --output examples/generated/micro_commons_artifact_cohesion.json
```

Evaluate module compatibility and implementation gates:

```powershell
py -3.10 -m ciac module-compatibility examples/generated/micro_commons_plan.json module_registries/micro_commons_default_v0.yaml --technology-module tech_modules/agrivoltaic_shade_pasture_water_efficiency.yaml --output examples/generated/micro_commons_module_compatibility.json
py -3.10 -m ciac scalability-gate examples/generated/micro_commons_plan.json tech_modules/agrivoltaic_shade_pasture_water_efficiency.yaml --module-registry module_registries/micro_commons_default_v0.yaml --output examples/generated/agrivoltaic_shade_pasture_water_efficiency_scalability_gate.json
py -3.10 -m ciac implement-module examples/generated/micro_commons_plan.json tech_modules/agrivoltaic_shade_pasture_water_efficiency.yaml --module-registry module_registries/micro_commons_default_v0.yaml --days 365 --output examples/generated/agrivoltaic_module_implementation.json
```

Run subsystem reports:

```powershell
py -3.10 -m ciac water examples/generated/micro_commons_plan.json water_plans/micro_commons_water_reserve_v2.yaml --output examples/generated/micro_commons_water_v2.json
py -3.10 -m ciac energy examples/generated/micro_commons_plan.json energy_plans/micro_commons_energy_reserve_v2.yaml --output examples/generated/micro_commons_energy_v2.json
py -3.10 -m ciac nutrition examples/generated/micro_commons_plan.json food_plans/micro_commons_basic.yaml --output examples/generated/micro_commons_nutrition.json
py -3.10 -m ciac roles examples/generated/micro_commons_plan.json role_plans/micro_commons_roles_v2.yaml --output examples/generated/micro_commons_roles_v2.json
```

## How To Read Status

- `pass`: no tracked blocker under current assumptions.
- `warn`: visible caution that should remain visible.
- `fail`: blocking condition under current assumptions.
- `ready_with_warnings`: suitable for inspection, not real-world approval.
- `provisional`: value or conclusion still needs evidence, review, governance, or consent.

If an output says engineering, public health, legal, finance, safety, governance, or resident consent review is required, CIaC is naming a stop condition. It is not satisfying it.

## Documentation

- [Simulation foundation goal](docs/simulation_foundation_goal.md)
- [Progress metrics](docs/progress_metrics.md)
- [Modeling backlog](docs/modeling_backlog.md)
- [Sprint history](docs/sprint_history.md)
- [Module reports](docs/module_reports/)

## Development

Python 3.10 is the target runtime. Dependencies are intentionally small: `PyYAML` and `jsonschema`.

Run all tests:

```powershell
py -3.10 -m unittest discover -s tests
```

The authored source of truth is the Python package, schemas, YAML inputs, docs, tests, and viewer files. Generated artifacts are reproducible working state, not permanent source.
