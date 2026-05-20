# Civic Infrastructure as Code

CIaC turns the master specification into a small Python/YAML/JSON foundation:

- authored civic patterns in YAML
- JSON Schema-compatible public contracts
- validation for civic data
- deterministic dependency-aware compilation
- first-pass validity gates
- provisional normal-year simulation
- authored seasonal simulation profiles
- authored household labor and demand profiles
- authored spatial readiness profiles and layout graph output
- minimum viable reserve patterns for water, food, and critical energy
- provisional stress scenario reports
- provisional food and nutrition reports
- provisional review evidence tracking
- human-readable Markdown review packets
- viewer-oriented runtime bundle exports
- static runtime viewer
- simulation foundation gate reports
- optimization readiness reports
- deterministic optimizer reports
- bounded search optimizer reports
- objective calibration reports
- weight governance reports
- versioned visualization handoff bundles
- JSON output suitable for later simulation and Unreal visualization

This is not a building manual, legal guide, or engineering certification system. Seed values are provisional unless explicitly sourced in later work.

## Planning Docs

- [Simulation foundation goal](docs/simulation_foundation_goal.md): the current target, stop conditions, and complexity gate.
- [Rolling progress metrics](docs/progress_metrics.md): sprint-to-sprint estimates for simulation, virtualization, and optimization readiness.
- [Modeling backlog](docs/modeling_backlog.md): prioritized simulation modeling work before visual buildout.

## Current Goal

The current project goal is to mature CIaC from an inspectable 5-household simulation into a repeatable infrastructure-pattern logic engine that can feed richer commune virtualization and later optimization.

Rolling progress estimates:

- Inspectable simulation proof of concept: ~100%
- Mature commune virtualization data contract: ~100%
- Faithful pattern optimization engine: ~100%

Further modeling should pass a complexity gate: add detail only when it prevents false confidence, closes a survival-critical accounting gap, clarifies simulation behavior, stabilizes the JSON/viewer contract, or reduces a measured failure without hiding review, labor, governance, or external dependency.

Warnings are allowed when they are explicit, visible, and not hiding unmet survival demand. CIaC should not keep adding infrastructure patterns just because a report can name another future realism gap.

## Quick Start

```powershell
py -3.10 -m ciac validate patterns
py -3.10 -m ciac compile examples/site_profiles/micro_commons_5_households.yaml patterns --seasonal-profile seasonal_profiles/humid_temperate_provisional.yaml --household-profile household_profiles/micro_commons_households_v0.yaml --spatial-profile spatial_profiles/micro_commons_spatial_v0.yaml
py -3.10 -m ciac simulate examples/generated/micro_commons_plan.json --review-status examples/generated/micro_commons_review_status.json
py -3.10 -m ciac simulate examples/generated/micro_commons_plan.json --days 14 --scenario scenarios/water_contamination_response_v2.yaml --review-status examples/generated/micro_commons_review_status.json
py -3.10 -m ciac compare-simulations examples/generated/micro_commons_simulation.json examples/generated/water_contamination_response_v2_replay_simulation.json
py -3.10 -m ciac replay-matrix examples/generated/water_contamination_response_v2_replay_comparison.json examples/generated/drought_reserve_v2_replay_comparison.json
py -3.10 -m ciac redesign-matrix examples/generated/micro_commons_plan.json examples/generated/micro_commons_replay_matrix.json
py -3.10 -m ciac scenario examples/generated/micro_commons_plan.json scenarios/drought.yaml
py -3.10 -m ciac nutrition examples/generated/micro_commons_plan.json food_plans/micro_commons_basic.yaml
py -3.10 -m ciac water examples/generated/micro_commons_plan.json water_plans/micro_commons_basic.yaml
py -3.10 -m ciac energy examples/generated/micro_commons_plan.json energy_plans/micro_commons_basic.yaml
py -3.10 -m ciac roles examples/generated/micro_commons_plan.json role_plans/micro_commons_basic.yaml
py -3.10 -m ciac audit examples/generated/micro_commons_plan.json --gates examples/generated/micro_commons_gates.json --simulation examples/generated/micro_commons_simulation.json --nutrition examples/generated/micro_commons_nutrition.json --water examples/generated/micro_commons_water.json --energy examples/generated/micro_commons_energy.json --roles examples/generated/micro_commons_roles.json --scenario examples/generated/drought_scenario.json
py -3.10 -m ciac redesign examples/generated/micro_commons_audit.json examples/generated/micro_commons_plan.json
py -3.10 -m ciac compare examples/generated/micro_commons_audit.json examples/generated/micro_commons_audit_v2.json
py -3.10 -m ciac export-md examples/generated/micro_commons_plan.json --audit examples/generated/micro_commons_audit_v5.json --dossier examples/generated/micro_commons_dossier.json --review examples/generated/micro_commons_review_status.json --output reports/micro_commons_review_packet.md
py -3.10 -m ciac export-runtime examples/generated/micro_commons_plan.json examples/generated/micro_commons_simulation.json --scenario examples/generated/water_contamination_response_v2_scenario.json --output examples/generated/micro_commons_runtime_bundle.json
py -3.10 -m ciac foundation-gate examples/generated/micro_commons_plan.json examples/generated/micro_commons_simulation.json examples/generated/micro_commons_runtime_bundle.json examples/generated/micro_commons_replay_matrix.json --review-status examples/generated/micro_commons_review_status.json
py -3.10 -m ciac optimization-readiness patterns optimization_profiles/minimum_dignity_v0.yaml
py -3.10 -m ciac candidate-matrix examples/generated/micro_commons_plan.json patterns optimization_profiles/minimum_dignity_v0.yaml --scenario scenarios/water_contamination_response_v2.yaml --scenario scenarios/crop_failure.yaml --scenario scenarios/energy_outage_reserve_v2.yaml --review-status examples/generated/micro_commons_review_status.json
py -3.10 -m ciac tradeoff-scale examples/generated/micro_commons_plan.json examples/generated/micro_commons_candidate_matrix.json patterns scale_profiles/micro_commons_scale_targets_v0.yaml
py -3.10 -m ciac optimize examples/generated/micro_commons_candidate_matrix.json optimization_profiles/minimum_dignity_v0.yaml --tradeoff-scale examples/generated/micro_commons_tradeoff_scale.json
py -3.10 -m ciac optimize-search examples/generated/micro_commons_plan.json patterns optimization_profiles/minimum_dignity_v0.yaml --scenario scenarios/water_contamination_response_v2.yaml --scenario scenarios/crop_failure.yaml --scenario scenarios/energy_outage_reserve_v2.yaml --review-status examples/generated/micro_commons_review_status.json
py -3.10 -m ciac objective-calibration examples/generated/micro_commons_search_optimizer_report.json calibration_profiles/minimum_dignity_objectives_v0.yaml
py -3.10 -m ciac weight-governance optimization_profiles/minimum_dignity_v0.yaml examples/generated/micro_commons_objective_calibration.json governance_profiles/minimum_dignity_weights_draft_v0.yaml
py -3.10 -m ciac export-visualization examples/generated/micro_commons_runtime_bundle.json examples/generated/micro_commons_foundation_gate.json examples/generated/micro_commons_candidate_matrix.json examples/generated/micro_commons_tradeoff_scale.json examples/generated/micro_commons_optimizer_report.json --output examples/generated/micro_commons_visualization_bundle.json
py -3.10 -m http.server 8765
py -3.10 -m unittest discover -s tests
```

Write generated plans to `examples/generated/` if you want files on disk:

```powershell
py -3.10 -m ciac compile examples/site_profiles/micro_commons_5_households.yaml patterns --seasonal-profile seasonal_profiles/humid_temperate_provisional.yaml --household-profile household_profiles/micro_commons_households_v0.yaml --spatial-profile spatial_profiles/micro_commons_spatial_v0.yaml --output examples/generated/micro_commons_plan.json
py -3.10 -m ciac gates examples/generated/micro_commons_plan.json
py -3.10 -m ciac simulate examples/generated/micro_commons_plan.json --days 365 --review-status examples/generated/micro_commons_review_status.json --output examples/generated/micro_commons_simulation.json
py -3.10 -m ciac simulate examples/generated/micro_commons_plan.json --days 14 --scenario scenarios/water_contamination_response_v2.yaml --review-status examples/generated/micro_commons_review_status.json --output examples/generated/water_contamination_response_v2_replay_simulation.json
py -3.10 -m ciac compare-simulations examples/generated/micro_commons_simulation.json examples/generated/water_contamination_response_v2_replay_simulation.json --output examples/generated/water_contamination_response_v2_replay_comparison.json
py -3.10 -m ciac replay-matrix examples/generated/energy_outage_reserve_v2_replay_comparison.json examples/generated/water_contamination_response_v2_replay_comparison.json examples/generated/sanitation_failure_replay_comparison.json examples/generated/resident_exit_labor_loss_replay_comparison.json examples/generated/drought_reserve_v2_replay_comparison.json examples/generated/crop_failure_replay_comparison.json --output examples/generated/micro_commons_replay_matrix.json
py -3.10 -m ciac redesign-matrix examples/generated/micro_commons_plan.json examples/generated/micro_commons_replay_matrix.json --output examples/generated/micro_commons_matrix_redesign.json
py -3.10 -m ciac scenario examples/generated/micro_commons_plan.json scenarios/drought.yaml --output examples/generated/drought_scenario.json
py -3.10 -m ciac nutrition examples/generated/micro_commons_plan.json food_plans/micro_commons_basic.yaml --output examples/generated/micro_commons_nutrition.json
py -3.10 -m ciac water examples/generated/micro_commons_plan.json water_plans/micro_commons_basic.yaml --output examples/generated/micro_commons_water.json
py -3.10 -m ciac energy examples/generated/micro_commons_plan.json energy_plans/micro_commons_basic.yaml --output examples/generated/micro_commons_energy.json
py -3.10 -m ciac roles examples/generated/micro_commons_plan.json role_plans/micro_commons_basic.yaml --output examples/generated/micro_commons_roles.json
py -3.10 -m ciac audit examples/generated/micro_commons_plan.json --gates examples/generated/micro_commons_gates.json --simulation examples/generated/micro_commons_simulation.json --nutrition examples/generated/micro_commons_nutrition.json --water examples/generated/micro_commons_water.json --energy examples/generated/micro_commons_energy.json --roles examples/generated/micro_commons_roles.json --scenario examples/generated/drought_scenario.json --scenario examples/generated/water_contamination_scenario.json --output examples/generated/micro_commons_audit.json
py -3.10 -m ciac redesign examples/generated/micro_commons_audit.json examples/generated/micro_commons_plan.json --output examples/generated/micro_commons_redesign.json
py -3.10 -m ciac water examples/generated/micro_commons_plan.json water_plans/micro_commons_water_reserve_v2.yaml --output examples/generated/micro_commons_water_v2.json
py -3.10 -m ciac scenario examples/generated/micro_commons_plan.json scenarios/drought_reserve_v2.yaml --output examples/generated/drought_reserve_v2_scenario.json
py -3.10 -m ciac audit examples/generated/micro_commons_plan.json --gates examples/generated/micro_commons_gates.json --simulation examples/generated/micro_commons_simulation.json --nutrition examples/generated/micro_commons_nutrition.json --water examples/generated/micro_commons_water_v2.json --energy examples/generated/micro_commons_energy.json --roles examples/generated/micro_commons_roles.json --scenario examples/generated/drought_reserve_v2_scenario.json --scenario examples/generated/water_contamination_scenario.json --output examples/generated/micro_commons_audit_v2.json
py -3.10 -m ciac compare examples/generated/micro_commons_audit.json examples/generated/micro_commons_audit_v2.json --output examples/generated/micro_commons_comparison.json
py -3.10 -m ciac energy examples/generated/micro_commons_plan.json energy_plans/micro_commons_energy_reserve_v2.yaml --output examples/generated/micro_commons_energy_v2.json
py -3.10 -m ciac scenario examples/generated/micro_commons_plan.json scenarios/energy_outage_reserve_v2.yaml --output examples/generated/energy_outage_reserve_v2_scenario.json
py -3.10 -m ciac audit examples/generated/micro_commons_plan.json --gates examples/generated/micro_commons_gates.json --simulation examples/generated/micro_commons_simulation.json --nutrition examples/generated/micro_commons_nutrition.json --water examples/generated/micro_commons_water_v2.json --energy examples/generated/micro_commons_energy_v2.json --roles examples/generated/micro_commons_roles.json --scenario examples/generated/drought_reserve_v2_scenario.json --scenario examples/generated/water_contamination_scenario.json --scenario examples/generated/energy_outage_reserve_v2_scenario.json --output examples/generated/micro_commons_audit_v3.json
py -3.10 -m ciac compare examples/generated/micro_commons_audit_v2.json examples/generated/micro_commons_audit_v3.json --output examples/generated/micro_commons_comparison_v2_to_v3.json
py -3.10 -m ciac roles examples/generated/micro_commons_plan.json role_plans/micro_commons_roles_v2.yaml --output examples/generated/micro_commons_roles_v2.json
py -3.10 -m ciac audit examples/generated/micro_commons_plan.json --gates examples/generated/micro_commons_gates.json --simulation examples/generated/micro_commons_simulation.json --nutrition examples/generated/micro_commons_nutrition.json --water examples/generated/micro_commons_water_v2.json --energy examples/generated/micro_commons_energy_v2.json --roles examples/generated/micro_commons_roles_v2.json --scenario examples/generated/drought_reserve_v2_scenario.json --scenario examples/generated/water_contamination_scenario.json --scenario examples/generated/energy_outage_reserve_v2_scenario.json --output examples/generated/micro_commons_audit_v4.json
py -3.10 -m ciac compare examples/generated/micro_commons_audit_v3.json examples/generated/micro_commons_audit_v4.json --output examples/generated/micro_commons_comparison_v3_to_v4.json
py -3.10 -m ciac scenario examples/generated/micro_commons_plan.json scenarios/water_contamination_response_v2.yaml --output examples/generated/water_contamination_response_v2_scenario.json
py -3.10 -m ciac audit examples/generated/micro_commons_plan.json --gates examples/generated/micro_commons_gates.json --simulation examples/generated/micro_commons_simulation.json --nutrition examples/generated/micro_commons_nutrition.json --water examples/generated/micro_commons_water_v2.json --energy examples/generated/micro_commons_energy_v2.json --roles examples/generated/micro_commons_roles_v2.json --scenario examples/generated/drought_reserve_v2_scenario.json --scenario examples/generated/water_contamination_response_v2_scenario.json --scenario examples/generated/energy_outage_reserve_v2_scenario.json --output examples/generated/micro_commons_audit_v5.json
py -3.10 -m ciac compare examples/generated/micro_commons_audit_v4.json examples/generated/micro_commons_audit_v5.json --output examples/generated/micro_commons_comparison_v4_to_v5.json
py -3.10 -m ciac dossier examples/generated/micro_commons_audit_v5.json examples/generated/micro_commons_plan.json --output examples/generated/micro_commons_dossier.json
py -3.10 -m ciac review examples/generated/micro_commons_dossier.json review_registers/micro_commons_placeholder.yaml --output examples/generated/micro_commons_review_status.json
py -3.10 -m ciac export-md examples/generated/micro_commons_plan.json --audit examples/generated/micro_commons_audit_v5.json --dossier examples/generated/micro_commons_dossier.json --review examples/generated/micro_commons_review_status.json --output reports/micro_commons_review_packet.md
py -3.10 -m ciac export-runtime examples/generated/micro_commons_plan.json examples/generated/micro_commons_simulation.json --scenario examples/generated/water_contamination_response_v2_scenario.json --scenario examples/generated/energy_outage_reserve_v2_scenario.json --output examples/generated/micro_commons_runtime_bundle.json
py -3.10 -m ciac foundation-gate examples/generated/micro_commons_plan.json examples/generated/micro_commons_simulation.json examples/generated/micro_commons_runtime_bundle.json examples/generated/micro_commons_replay_matrix.json --review-status examples/generated/micro_commons_review_status.json --comparison examples/generated/water_contamination_response_v2_replay_comparison.json --comparison examples/generated/crop_failure_replay_comparison.json --comparison examples/generated/energy_outage_reserve_v2_replay_comparison.json --output examples/generated/micro_commons_foundation_gate.json
py -3.10 -m ciac optimization-readiness patterns optimization_profiles/minimum_dignity_v0.yaml --output examples/generated/micro_commons_optimization_readiness.json
py -3.10 -m ciac candidate-matrix examples/generated/micro_commons_plan.json patterns optimization_profiles/minimum_dignity_v0.yaml --scenario scenarios/water_contamination_response_v2.yaml --scenario scenarios/crop_failure.yaml --scenario scenarios/energy_outage_reserve_v2.yaml --review-status examples/generated/micro_commons_review_status.json --days 365 --output examples/generated/micro_commons_candidate_matrix.json
py -3.10 -m ciac tradeoff-scale examples/generated/micro_commons_plan.json examples/generated/micro_commons_candidate_matrix.json patterns scale_profiles/micro_commons_scale_targets_v0.yaml --output examples/generated/micro_commons_tradeoff_scale.json
py -3.10 -m ciac optimize examples/generated/micro_commons_candidate_matrix.json optimization_profiles/minimum_dignity_v0.yaml --tradeoff-scale examples/generated/micro_commons_tradeoff_scale.json --output examples/generated/micro_commons_optimizer_report.json
py -3.10 -m ciac optimize-search examples/generated/micro_commons_plan.json patterns optimization_profiles/minimum_dignity_v0.yaml --scenario scenarios/water_contamination_response_v2.yaml --scenario scenarios/crop_failure.yaml --scenario scenarios/energy_outage_reserve_v2.yaml --review-status examples/generated/micro_commons_review_status.json --days 365 --output examples/generated/micro_commons_search_optimizer_report.json
py -3.10 -m ciac objective-calibration examples/generated/micro_commons_search_optimizer_report.json calibration_profiles/minimum_dignity_objectives_v0.yaml --output examples/generated/micro_commons_objective_calibration.json
py -3.10 -m ciac weight-governance optimization_profiles/minimum_dignity_v0.yaml examples/generated/micro_commons_objective_calibration.json governance_profiles/minimum_dignity_weights_draft_v0.yaml --output examples/generated/micro_commons_weight_governance.json
py -3.10 -m ciac export-visualization examples/generated/micro_commons_runtime_bundle.json examples/generated/micro_commons_foundation_gate.json examples/generated/micro_commons_candidate_matrix.json examples/generated/micro_commons_tradeoff_scale.json examples/generated/micro_commons_optimizer_report.json --output examples/generated/micro_commons_visualization_bundle.json
```

## Sprint 1 Gates

- Truth before beauty: no visual prototype precedes validation and dependency checks.
- No unsafe certainty: legal, engineering, health, water, sanitation, structural, and electrical values remain provisional.
- No hidden dependencies: survival-critical prerequisites must be explicit.
- No governance blind spot: commons survival systems require stewardship, audit, backup, and capture-risk fields.
- No labor fantasy: build and recurring labor are required fields.
- No promotion without gates: draft patterns are not validated real-world recommendations.

## Sprint 2 Simulation

`ciac simulate` consumes compiled plans only. It does not re-read pattern YAML, so the compiled plan remains the exchange format for later simulation and Unreal visualization.

The current simulation is deterministic and provisional. It emits daily state, a shared resource ledger, scheduled maintenance, resident labor burden, high-consequence risks, bottlenecks, recommendations, confidence, and unknowns. It does not yet model site-specific seasonality, physical storage limits, weather, stochastic failures, jurisdictional code compliance, or complete nutrition.

## Sprint 3 Scenarios

`ciac scenario` runs provisional stress scenarios against compiled plans. Scenario files live in `scenarios/` and modify resource balances, labor capacity, emergency work, and triggered risks.

Initial scenarios include drought, water contamination, energy outage, crop failure, sanitation failure, and resident exit/labor loss. These reports are pressure tests, not safety certifications.

## Sprint 4 Nutrition

`ciac nutrition` evaluates a provisional food plan against a compiled plan. It reports calories per person, protein per person, local food percentage, stored calorie days, shortage timeline, fallback procurement needs, dietary risk warnings, and bottlenecks.

The current nutrition layer is still intentionally humble. It does not model micronutrients, allergies, cultural diet, spoilage, crop calendars, harvest labor peaks, food safety, or medical dietary needs.

## Sprint 5 Water

`ciac water` evaluates a provisional water resilience plan against a compiled plan. It reports potable and nonpotable storage days, normal balance, drought balance, contamination fallback window, testing protocol status, demand reduction needed, safety warnings, bottlenecks, and redesign recommendations.

The current water layer does not model aquifer recharge, rainfall sequence, seasonal drawdown, plumbing design, water chemistry, pathogen transport, or jurisdiction-specific water law.

## Sprint 6 Energy

`ciac energy` evaluates a provisional energy resilience plan against a compiled plan. It reports normal daily balance, critical-load battery autonomy, outage survival, load shedding order, cloudy-weather solar reduction, refrigeration risk, backup energy gap, maintenance status, safety warnings, bottlenecks, and redesign recommendations.

The current energy layer does not model hourly solar curves, battery degradation, inverter limits, surge loads, wiring design, thermal behavior, electrical code, or qualified engineering review.

## Sprint 7 Roles

`ciac roles` evaluates provisional role rotation and labor fairness against a compiled plan. It reports assigned role schedules, unfilled roles, overloaded residents, single-point-of-failure roles, backup coverage, care work accounting, fairness score, burnout warnings, and redesign recommendations.

The current role layer is a planning aid only. It does not model consent, resident preference, conflict, illness, emotional labor, learning curves, task quality, or actual governance authority.

## Sprint 8 Audit

`ciac audit` aggregates generated reports into one provisional readiness decision. It reports subsystem statuses, survival-critical blockers, noncritical warnings, required redesigns, top risks, next sprint recommendations, and a promotion decision.

Promotion decisions are deliberately conservative: failed survival-critical evidence returns `do_not_promote`; warnings return `revise_before_pilot`; a clean pass returns `candidate_for_review`, never real-world approval.

## Sprint 9 Redesign

`ciac redesign` turns an audit report into provisional redesign candidates. It groups blockers by subsystem and proposes concrete changes, expected effects, tradeoffs, new assumptions, files to edit, and acceptance criteria.

Redesign reports are the iteration loop: edit the source plans, regenerate reports, rerun the audit, and compare blocker count before doing visualization or real-world planning.

## Sprint 10 Compare

`ciac compare` compares two audit reports. It reports blocker count before/after, status changes by subsystem, resolved blockers, remaining blockers, new blockers, warning deltas, promotion decision delta, and whether the first water-reserve redesign acceptance criteria passed.

The included v2 water reserve plan is still provisional. It demonstrates the iteration loop; it is not a claim that the water design is real-world safe.

## Sprint 11 Energy Variant

`energy_plans/micro_commons_energy_reserve_v2.yaml` demonstrates the next redesign iteration. It increases usable battery reserve, reduces modeled critical loads, and adds provisional backup energy.

The v3 audit uses improved water and improved energy evidence. It should still refuse promotion while role backup/fairness and water contamination remain unresolved.

## Sprint 12 Roles Variant

`role_plans/micro_commons_roles_v2.yaml` demonstrates the next governance redesign iteration. It trains a second energy steward, protects a high-care resident from primary commons assignments, and improves backup coverage.

The v4 audit should still refuse promotion while water contamination remains unresolved.

## Sprint 13 Contamination Variant

`scenarios/water_contamination_response_v2.yaml` demonstrates the next response redesign. It assumes stronger reserve, backup treatment, notices, and retesting.

The v5 audit can move from `do_not_promote` to `revise_before_pilot` if all survival-critical blockers are removed, but it still remains provisional and not approved for real-world use.

## Sprint 14 Dossier

`ciac dossier` turns an audit into a pilot-review dossier. It groups unresolved warnings, required professional reviews, legal unknowns, evidence gaps, governance questions, required documents, go/no-go checks, and things that must never be inferred from the model.

The dossier is a review package generator, not a permit, certification, consent process, or construction approval.

## Sprint 15 Review Register

`ciac review` compares a pilot dossier with a review evidence register. It reports which required reviews are covered, missing, rejected, expired, or still carrying unresolved issues.

Review status tracks evidence workflow only. CIaC does not validate credentials, professional conclusions, legal sufficiency, or safety.

## Sprint 16 Markdown Export

`ciac export-md` turns the compiled plan, audit, dossier, and review status JSON artifacts into a human-readable review packet.

The Markdown packet is disposable presentation output. The generated JSON artifacts remain the source of truth for downstream automation, simulation, and future visualization.

## Sprint 17 Daily Simulation State

`ciac simulate` now includes a day-by-day `daily_states` timeline, a shared `resource_ledger`, and event `timeline` while preserving the aggregate `resource_balance`, `labor`, and `maintenance` summaries.

This is the first runtime substrate for later visual buildout: tanks, batteries, pantry equivalents, sanitation capacity, labor, maintenance, and unmet needs can now be inspected over time as JSON.

## Sprint 18 Seasonal Profiles

`ciac compile --seasonal-profile` embeds an authored `SeasonalProfile` into the compiled plan so `ciac simulate` can vary resource production, resource consumption, and maintenance labor by season.

The included `seasonal_profiles/humid_temperate_provisional.yaml` is a provisional planning profile, not weather, crop, rainfall, aquifer, or solar-design evidence.

## Sprint 19 Maintenance And Degradation

`ciac simulate` now tracks daily maintenance capacity, completed tasks, deferred tasks, backlog, overdue days, and provisional system degradation.

Deferred maintenance can reduce production, increase modeled consumption, create active maintenance risks, and add timeline events. The degradation model is intentionally provisional; it is a pressure-test signal, not measured reliability engineering.

## Sprint 20 Household Profiles

`ciac compile --household-profile` embeds an authored `HouseholdProfile` into the compiled plan so `ciac simulate` can derive population, care load, protected labor, available commons labor, and household demand adjustments from structured data.

The included `household_profiles/micro_commons_households_v0.yaml` is a provisional social model, not resident consent, labor assignment, medical review, or participation agreement.

## Sprint 21 Failure Mode Runtime

`ciac simulate` and `ciac scenario` now turn scenario-triggered pattern failure modes into runtime failure objects with active days, resource effects, response labor, mitigation text, and unresolved review dependencies.

Failures such as `battery_fault`, `contaminated_source`, `stored_water_contamination`, `crop_failure`, and `foodborne_illness` can now reduce output, increase burden, appear in daily state, and show up in scenario timelines. The effects are provisional pressure-test assumptions, not engineering, medical, public-health, or legal determinations.

## Sprint 22 Spatial Readiness

`ciac compile --spatial-profile` embeds an authored `SpatialProfile` and emits a `layout_graph` with zones, pattern placements, access routes, adjacency and separation edges, hazard flags, and unresolved spatial issues.

The included `spatial_profiles/micro_commons_spatial_v0.yaml` is a provisional placement graph, not a survey, site plan, permit drawing, fire access plan, utility design, accessibility review, or construction layout.

## Sprint 23 Runtime Bundle Export

`ciac export-runtime` packages a compiled plan, simulation run, and optional scenario runs into one viewer-oriented `RuntimeBundle`.

The bundle includes manifest metadata, site/layout data, systems, compressed daily timeline entries, scenario failures, viewer hints, and explicit non-proof warnings. It is the handoff contract for a future web, game, or Unreal visualization layer; the source JSON artifacts remain authoritative.

## Sprint 24 Static Runtime Viewer

`viewer/` contains a static inspection surface for `RuntimeBundle` JSON. Serve the repository root with `py -3.10 -m http.server 8765` and open `http://localhost:8765/viewer/`.

The viewer shows the layout graph, systems by zone, resource state by day, maintenance state, active failures, scenario summaries, and warnings. It is not a real-world site plan, safety proof, permit artifact, or consent process.

## Sprint 25 Viewer Playback Polish

The static viewer now adds day playback, selected-system details, scenario failure overlays, spatial-warning highlights, and a compact failure-reason panel.

The viewer remains an inspection tool for generated JSON, not a claim that the proposed commons is safe, buildable, permitted, or consented to.

## Sprint 26 Minimum Viable Resource Baseline

The seed pattern set now includes three deliberately plain reserve systems: `emergency_water_reserve`, `staple_food_reserve`, and `critical_load_reserve`.

These are simulation buffers, not best-fit technology endorsements. They keep the normal-year micro-commons run above zero for water, food, and energy while preserving provisional labels, review dependencies, stewardship fields, maintenance burden, and failure modes.

The intent is minimum viable dignified existence: enough modeled reserve capacity to inspect a living system over time without pretending the current numbers are engineered, permitted, or nutritionally complete.

## Sprint 27 Storage And Inventory State

Reserve patterns now declare explicit provisional storage specs for water, food, and energy: capacity, initial fill, reserve floor, max daily release, max daily refill, refill mode, and access rule.

`ciac simulate` draws from storage only when daily production cannot meet daily demand, refills storage only from modeled surplus, and exposes `raw_net`, `storage_release`, `storage_refill`, `curtailment`, daily `storage_state`, and top-level `storage` summaries.

This makes the baseline more simulation-like without adding complexity. The model still does not prove potable safety, nutrition, battery sizing, spoilage, hourly loads, weather sequence, procurement reliability, or legal compliance.

## Sprint 28 Storage Quality Clock

Storage specs now include a provisional quality clock: check interval, unsafe-after threshold, loss rate after unsafe, risk text, and recovery action.

Completed maintenance checks reset the clock. Deferred reserve maintenance can push storage from `pass` to `warn` or `fail`, add timeline warnings, and eventually reduce usable stored quantity. This is still a coarse inspection model, not health, food-safety, battery, or engineering validation.

## Sprint 29 Storage Recovery Playbooks

Storage quality specs now include recovery role, labor hours, duration, and review dependency.

When a store crosses into failed quality, `ciac simulate` emits daily `storage_recovery_tasks`, counts their hours in labor burden, summarizes recovery work under top-level `storage.recovery`, and exports the tasks through the runtime bundle for viewer inspection.

Recovery playbooks are provisional workflow signals only. They do not prove that contaminated water is safe, spoiled food is handled correctly, damaged batteries are safe, or required professional review has happened.

## Sprint 30 Bounded Recovery State

Storage recovery is now stateful. A failed store opens one recovery task, tracks worked hours, remaining hours, days active, and daily labor used, then blocks on the declared review dependency instead of silently resolving.

Recovery tasks now compete for available daily labor after maintenance and active failure response. The simulation exposes `in_progress`, `stalled_labor`, and `blocked_review` recovery states, plus summary counts and remaining work under `storage.recovery`.

This is still not review validation. It only makes the workflow burden and unresolved stop condition visible.

## Sprint 31 Review Dependency Runtime

`ciac simulate` now accepts `--review-status` and embeds a provisional `review_context` in the simulation output.

Storage recovery tasks check their declared review dependency. Recovery can resolve only when the review-status report marks that domain `accepted`, with no unresolved issues and no expired or rejected evidence marker. Otherwise completed recovery work remains `blocked_review`.

Accepted review evidence in CIaC still means "the register says accepted"; it is not credential validation, legal sufficiency, or professional approval.

## Sprint 32 Scenario Review Context

Scenario YAML can now declare `review_context_overrides` for stress cases such as failed retests, unavailable reviewers, contested evidence, emergency waivers, or mutual-aid review pathways.

`ciac scenario` reports a structured `review_context`, adds review-context events to the failure timeline, and recommends review fallback work when scenario-specific evidence blocks recovery. Runtime bundles and the static viewer expose these scenario review events alongside ordinary scenario failures.

Scenario review context is a simulation stress input only. It is not an actual professional review, legal determination, public-health clearance, or permission to treat a failed system as safe.

## Sprint 33 Scenario Replay Simulation

`ciac simulate` now accepts `--scenario <scenario.yaml>` and applies scenario resource modifiers, emergency labor tasks, triggered runtime failures, and review-context overrides inside the daily simulation loop.

Daily states now include `scenario_events`, and simulation output includes `scenario_context`. This creates a first scenario replay path before visual buildout: a contamination response can now drain stores, consume labor, activate failures, and remain blocked by a failed retest over actual simulated days.

Scenario replay is still deterministic and provisional. It is a pressure-test trace, not a weather model, outage model, epidemiology model, emergency operating plan, or public-health judgment.

## Sprint 34 Replay Comparison

`ciac compare-simulations` compares a baseline simulation with a scenario replay.

The comparison reports status changes, resource deltas, storage deltas, labor deltas, unmet-demand increases, active failure days, storage recovery deltas, review-context deltas, bottlenecks, and a short summary. It is intended to answer the practical question: what did the scenario actually do to the modeled commons?

Replay comparison is still only as trustworthy as the two generated simulation artifacts. It does not validate the underlying assumptions or make a failed replay safe.

## Sprint 35 Replay Matrix

`ciac replay-matrix` ranks multiple `SimulationComparisonReport` artifacts.

The matrix reports one row per scenario comparison, total stress score, per-day stress score, unmet-demand delta, emergency labor, active failure-day delta, blocked review domains, top bottlenecks, and an overall top stressor. This is the first small dashboard-like prioritization layer before visual buildout.

Stress scores are coarse prioritization signals only. They are not probabilities, safety ratings, or real-world risk scores.

## Sprint 36 Matrix Redesign

`ciac redesign-matrix` turns a `ReplayMatrixReport` into targeted redesign candidates.

The current report prioritizes minimum viable changes: food model closure and recovery clock, short-window energy load shedding, and review evidence cleanup. Each candidate names target scenarios, minimum viable change, expected effect, tradeoffs, files to edit, acceptance criteria, and evidence from the matrix.

These are redesign prompts, not implementation, engineering review, or approval. The next step is to edit the source YAML for the first candidate and rerun the matrix.

## Sprint 37 Food Reserve Redesign Loop

The first matrix candidate has been implemented as a source-data change.

`staple_food_reserve` now models a stronger protected staple inventory and procurement floor. `crop_failure` now uses bounded runtime failure overrides so fallback procurement turns crop loss into a 30-day acute response instead of a 120-day emergency labor state.

After regenerating the replay matrix, crop failure dropped from the top stressor to the fourth-ranked total stressor. The next matrix redesign priority is now `water_response_buffer_and_isolation_floor`.

## Sprint 38 Water Response Buffer Loop

The second matrix candidate has been implemented as a source-data change.

`emergency_water_reserve` now models a larger protected reserve and higher emergency release path. The water reserve plan and contamination, drought, and sanitation scenarios now include bounded response assumptions for protected floor, isolation, rationing, and backup treatment workflows.

After regenerating the replay matrix, water unmet demand drops to `0` for contamination, drought, and sanitation replays. Failed review still blocks water recovery; the model does not treat a failed retest as safe. The next matrix redesign priority is now `scenario_labor_surge_buffer`.

## Sprint 39 Scenario Labor Surge Buffer Loop

The third matrix candidate has been implemented as a source-data and planner-priority change.

Scenario YAML now supports explicit `labor_support` events for provisional mutual-aid, pickup, monitoring, cleanup, and logistics labor. The simulation applies those hours to available commons labor without changing resident population or hiding the event from daily scenario timelines.

After regenerating the replay matrix with the household labor profile and review status, labor unmet demand drops to `0` across crop failure, drought, sanitation failure, water contamination, energy outage, and resident-exit replays. The matrix now warns instead of stress-failing. The next matrix redesign priority is `food_model_closure_and_recovery_clock`, followed by short-window energy outage load shedding and review evidence cleanup.

## Sprint 40 Simulation Foundation Gate

`ciac foundation-gate` evaluates whether the generated artifact set is ready for visual buildout under the simulation foundation goal.

The gate checks the normal-year baseline, minimum dignity ledger coverage, water/food/energy stress replay coverage, unmet survival demand, runtime bundle completeness, review blocker visibility, and warning legibility. It returns `not_ready`, `ready_with_warnings`, or `ready`.

The current generated report is `ready_with_warnings`: tracked unmet resource demand is `0` across the replay matrix, the runtime bundle has a 365-day baseline timeline and six scenario summaries, and review/partial-model limitations remain visible instead of being treated as resolved.

## Sprint 41 Foundation Demo Viewer Pass

The static viewer now loads the generated `FoundationGateReport` alongside the `RuntimeBundle`.

The viewer shows the foundation gate status, check evidence, warning checks, runtime scenario count, replay matrix status, and the explicit non-proof warning. This keeps the visual layer modest: it is an inspection dashboard for the current simulation foundation, not a polished world, technology endorsement, permit artifact, or safety claim.

## Sprint 42 Optimization Readiness

`ciac optimization-readiness` evaluates whether patterns expose enough metadata for a future optimizer.

The first readiness pass adds optional optimization metadata to the water, food, and energy reserve patterns: tunable parameters, locked review-bound parameters, scaling mode, and optimization objective tags. The `minimum_dignity_v0` optimization profile declares provisional objectives, hard constraints, and scale targets.

The current generated report is `ready_with_warnings`: the reserve patterns are tunable enough for candidate generation, while potable safety, food safety/nutrition completeness, and electrical safety remain locked behind review dependencies.

## Sprint 43 Candidate Plan Generation

`ciac candidate-matrix` generates and compares a small deterministic set of candidate configurations from declared pattern tunables.

The first candidate matrix compares the current plan, a balanced reserve increase, and a high-resilience reserve configuration across the baseline plus water contamination, crop failure, and energy outage stress replays. All three candidates are viable under hard constraints. Under the current minimum-dignity weights, the current authored plan ranks highest because stress survival is already adequate and larger reserves add provisional cost, footprint, labor, and review burden.

This is still not a full optimizer. It is the first generated candidate comparison loop that can feed scaling, tradeoff reports, and later mature visualization.

## Sprint 44 Tradeoff And Scale Reports

`ciac tradeoff-scale` explains candidate tradeoffs across declared scale targets.

The first scale profile tests 5, 10, 25, and 50 households. The generated report identifies objective leaders, reserve scaling requirements, review-required parameters, and viewer-ready candidate summaries. Under the current provisional objective weights, the current plan leads cost and recurring-labor objectives, while the high-resilience reserve candidate leads resilience-oriented objectives.

This report still scales declared provisional parameters only. It is not a site topology, cost estimate, engineering design, or governance approval.

## Sprint 45 Optimizer Loop

`ciac optimize` ranks generated candidate configurations against the authored optimization profile.

The first optimizer report selects `current_plan` under the current minimum-dignity weights because survival demand is already covered and larger reserves add cost, footprint, recurring burden, and review pressure. Its sensitivity checks still show the system behaving honestly: when resilience is weighted more heavily, `high_resilience_reserve` becomes the leader.

This is a deterministic candidate selector, not proof of best real-world infrastructure. It only optimizes within declared provisional pattern tunables, hard constraints, review locks, and generated candidate artifacts.

## Sprint 46 Visualization Contract Freeze

`ciac export-visualization` freezes the current simulation and optimizer artifacts into one versioned handoff bundle.

The generated `VisualizationBundle` carries stable entrypoints for the site graph, runtime daily states, systems, scenarios, foundation checks, candidate summaries, optimizer rankings, sensitivity checks, and constraint explanations. It selects `current_plan` under the current objective weights while preserving the resilience flip and every provisional/review warning.

This is the point where a richer commune virtualization can consume CIaC output without reverse-engineering the Python internals. It is still not a safety proof, engineering design, permit package, cost estimate, or resident-consent artifact.

## Sprint 47 Search Optimizer

`ciac optimize-search` runs a bounded family-level search across declared water, food, and energy reserve tunables.

The first search report evaluates 64 combinations across lean, current, balanced, and max reserve-family levels. It keeps 36 viable candidates, rejects 28 combinations that fail hard survival-demand constraints, preserves locked safety/review assumptions, and reports the binding constraints that shape the search.

This pushes CIaC beyond ranking hand-shaped candidates, but it is still not a general solver. Search remains limited to declared provisional tunables and coarse objective scores until future work adds sourced objective calibration and governance-approved weights.

## Sprint 48 Objective Calibration

`ciac objective-calibration` evaluates whether the selected search candidate's objective scores have explicit calibration rules.

The first calibration profile maps every selected-candidate objective to a formula id, input list, evidence status, review requirement, interpretation, and false-precision warning. The generated report has no missing selected metrics, but remains `provisional_calibrated` because the formulas are proxy models and the objective weights are not resident-ratified or professionally reviewed.

This makes optimizer scoring inspectable and challengeable. It does not make the proxy formulas true, sourced, jurisdiction-ready, or consented.

## Sprint 49 Weight Governance

`ciac weight-governance` evaluates whether the optimization weights are authorized for use.

The first weight governance profile mirrors the current `minimum_dignity_v0` objective weights, but marks them as draft. The generated report is `not_ratified`, with promotion blocked, because resident consent and professional review have not started. That is intentional: CIaC can now represent governance approval without pretending it has happened.

This completes the optimizer control loop as a software/data contract: search, rank, calibrate, and then block unratified recommendations. It does not make the current demo weights approved.
