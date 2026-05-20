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

The static viewer consumes generated runtime artifacts. After producing the runtime bundle, serve the repository root:

```powershell
py -3.10 -m http.server 8765
```

Then open:

```text
http://localhost:8765/viewer/
```

The viewer is an inspection surface for JSON outputs. It is not a site plan, safety claim, permit artifact, or approval workflow.

The current viewer also loads the generated optimizer artifacts when available. The Optimization panel shows the selected search candidate, how it differs from the all-current plan, the objective calibration status, and the weight-governance blocker that prevents draft weights from being treated as approved recommendations.

The Cycle panel demonstrates the intended usability loop: run one simulated year in about 20 seconds, review the recommended change, submit it, and run the next cycle. If `examples/generated/micro_commons_cycle_iteration.json` exists, the next cycle switches to the applied runtime bundle from that report.

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

Evaluate which infrastructure slots are modular and ready for research-backed swaps:

```powershell
py -3.10 -m ciac module-compatibility examples/generated/micro_commons_plan.json module_registries/micro_commons_default_v0.yaml --technology-module tech_modules/agrivoltaic_shade_pasture_water_efficiency.yaml --output examples/generated/micro_commons_module_compatibility.json
```

The registry describes the default posture for water, food, energy, and sanitation, then lists the interfaces a research module must satisfy to become drag-and-drop. AI tooling can later use the registry's research queries to scan recent papers, extract performance statistics, and draft candidate modules without weakening the default dignity floor.

Generate evidence-search briefs from model bottlenecks:

```powershell
py -3.10 -m ciac research-needs examples/generated/micro_commons_plan.json examples/generated/micro_commons_simulation.json --module-registry module_registries/micro_commons_default_v0.yaml --output examples/generated/micro_commons_research_needs.json
```

The first generated brief is `food_local_production_gap_v0`: the greenhouse produces food, but not enough to prevent annual staple-reserve drawdown. The output is meant to become the prompt/input for AI-assisted literature discovery.

Draft a provisional technology module from that brief with OpenAI:

```powershell
py -3.10 -m ciac draft-research-module examples/generated/micro_commons_research_needs.json --output examples/generated/food_local_production_gap_draft_module.json
```

This command reads `OPENAI_API_KEY` from the environment and uses the Responses API. It defaults to `gpt-5.5`, can be overridden with `--model` or `CIAC_OPENAI_MODEL`, and may use web search unless `--no-web-search` is passed. Drafted modules are still provisional and must pass validation and scalability gates before they can affect optimization.

Evaluate whether a discovered module can scale inside CIaC:

```powershell
py -3.10 -m ciac scalability-gate examples/generated/micro_commons_plan.json tech_modules/agrivoltaic_shade_pasture_water_efficiency.yaml --module-registry module_registries/micro_commons_default_v0.yaml --output examples/generated/agrivoltaic_shade_pasture_water_efficiency_scalability_gate.json
```

The agrivoltaics seed has published evidence and preserves dignity floors, but currently fails scalability because CIaC lacks edible-serving, labor, and crop-specific adapter interfaces for it. That is intentional: research can suggest modules, but modules must pass gates before optimization can use them.

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
