# CIaC Modeling Backlog

This backlog lists modeling work that can move CIaC closer to a real simulation before visual buildout. It is subordinate to the [simulation foundation goal](simulation_foundation_goal.md): do not implement backlog items just because they are realistic or interesting.

The near-term target is a deterministic, inspectable civic simulation loop: given a compiled plan, site profile, scenario, and actor schedule, CIaC should step through time and expose resource balances, labor burden, maintenance events, failures, mitigations, and unresolved safety/governance questions as structured JSON.

Rolling completion estimates and larger sprint chunks are tracked in [progress_metrics.md](progress_metrics.md).

## Backlog Triage Rule

Promote a backlog item only if it does at least one of the following:

- prevents false confidence,
- closes a survival-critical accounting gap,
- makes runtime or viewer behavior easier to inspect,
- stabilizes the JSON contract for later visualization,
- reduces a measured failure without hiding review, labor, governance, or external dependency.

Keep everything else parked.

## Critical Path To Simulation

1. **Time-Step World State**
   - Define a `SimulationState` shape with day, season, resident count, system statuses, stored resources, active risks, completed maintenance, and unmet needs.
   - Add a deterministic stepping function that advances one day at a time.
   - Keep all outputs JSON-serializable for later visualization.

2. **Resource Ledger**
   - Replace current report-only balances with a shared daily ledger for water, energy, food, sanitation capacity, labor hours, and cash/procurement.
   - Track production, consumption, storage, losses, imports, emergency reserves, and unmet demand.
   - Preserve provisional labels for every assumed rate.

3. **Seasonality And Weather Inputs**
   - Add simple seasonal profiles for rainfall, solar availability, temperature band, crop production, and maintenance constraints.
   - Start with authored YAML profiles, not live weather.
   - Make scenario files able to override seasonal assumptions.

4. **Maintenance And Degradation**
   - Turn maintenance cycles from static compiled fields into scheduled simulation events.
   - Add skipped-maintenance effects: reduced output, increased risk probability, downtime, or explicit unknown.
   - Track backlog accumulation and labor contention.

5. **Resident Role And Labor Engine**
   - Convert role plans into daily or weekly assignments.
   - Model availability, care load, training coverage, backup activation, overload, and refusal/exit events.
   - Keep governance constraints visible: no resident should silently become survival-critical without backup and consent evidence.

6. **Failure Mode Activation**
   - Convert pattern failure modes into scenario-triggerable events.
   - Represent failures as state changes with severity, affected systems, required response, labor cost, repair time, and unresolved professional review dependencies.
   - Distinguish simulated stress from real-world safety validation.

7. **Household And Population Profiles**
   - Add lightweight household profiles: adults, children, elders, disabled residents, dietary needs, care needs, skill coverage, and protected labor limits.
   - Use these to drive demand and labor availability instead of a single population count.

8. **Spatial Readiness Data**
   - Add minimal site layout metadata before visualization: zones, approximate distances, adjacency constraints, access routes, slope/flood flags, and utility relationships.
   - This is not a 3D scene yet; it is the data a 3D scene will need.

## Modeling Backlog

### Water

- Seasonal rainfall profile and catchment yield.
- Well drawdown and conservative recharge placeholder.
- Potable and nonpotable storage as separate state variables.
- Daily testing/boil/treatment status.
- Contamination event response with isolation, reserve drawdown, retesting, and external supply.
- Greywater and sanitation coupling.
- Explicit public-health review dependency for any safety claim.

### Energy

- Hourly or day-part load classes: critical, essential, discretionary, workshop.
- Solar generation by season and cloudy-day scenario.
- Battery state of charge, reserve floor, inverter/load cap, and degradation placeholder.
- Backup generation or mutual-aid charging as constrained imports.
- Refrigeration spoilage risk tied to outage duration.
- Electrical review dependency for load calculations and safety.

### Food And Nutrition

- Minimum viable staple reserve pattern is in the seed set; next model this as inventory, shelf life, and drawdown instead of daily-equivalent production.
- Crop calendar and seasonal harvest windows.
- Stored food inventory by calorie/protein class.
- Spoilage and refrigeration dependency.
- Procurement trips, cost placeholder, and external supply interruption.
- Dietary constraints and culturally acceptable diet flags.
- Food safety review dependency for shared kitchen/storage.

### Sanitation And Health

- Capacity state for bathhouse, composting, greywater, and handwashing.
- Cleaning and inspection schedule as labor-bearing tasks.
- Failure events: overload, pathogen concern, odor/vector warning, winter slowdown.
- Emergency shutdown state and external service requirement.
- Sanitation/public-health review dependency for any real-world claim.

### Shelter And Built Systems

- Occupancy capacity by household type.
- Heating/cooling demand placeholder tied to season.
- Accessibility constraints and care needs.
- Repair backlog and weather vulnerability.
- Structural/building review dependency for dwellings and shared facilities.

### Labor And Governance

- Daily role assignment and backup coverage.
- Skill training progression and minimum coverage thresholds.
- Burnout accumulation and recovery.
- Care labor accounting.
- Emergency authority activation and audit requirement.
- Resident refusal, exit, and conflict events as first-class governance states.

### Risk And Emergency Response

- Scenario library with drought, contamination, outage, crop failure, sanitation failure, resident exit, storm/flood, heat/cold stress, injury/illness, and supply-chain disruption.
- Risk activation rules from pattern failure modes.
- Response playbooks with labor, resource, governance, and review dependencies.
- Recovery time and residual risk tracking.

### Economics And Procurement

- Initial build cost placeholders by pattern.
- Recurring operating cost ledger.
- Procurement dependencies for food, parts, fuel, lab tests, professional reviews, and emergency services.
- Cash shortfall or supply interruption scenarios.

### Spatial And Site Constraints

- Site zones and distance relationships.
- Access routes for emergency services, delivery, waste removal, and disabled residents.
- Flood, slope, contamination, setback, and utility constraints as data fields.
- Export-ready layout graph for later Unreal or map visualization.

## Sprint Candidates

### Sprint 17: Simulation State And Daily Ledger

Status: implemented as the first daily runtime substrate.

Build the central simulation loop and shared resource ledger. This is the best next step toward seeing CIaC in action because every later model can plug into it.

Acceptance criteria:
- `ciac simulate` emits daily state summaries, not only aggregate totals.
- Water, energy, food, sanitation capacity, and labor share one ledger structure.
- A deterministic 30-day run is snapshot-tested.
- Unmet demand and reserve depletion are visible by day.

### Sprint 18: Seasonal Profiles

Status: implemented as authored seasonal multipliers embedded at compile time.

Add authored seasonal profiles and connect them to water, energy, and food production.

Acceptance criteria:
- Site profiles can reference a seasonal profile YAML.
- Simulation output changes by season.
- Drought and cloudy-weather scenarios override seasonal inputs cleanly.

### Sprint 19: Maintenance And Degradation

Status: implemented as daily maintenance capacity, backlog, overdue tracking, and provisional degradation.

Turn maintenance cycles into scheduled events that affect system performance when skipped.

Acceptance criteria:
- Maintenance tasks appear on the simulation timeline.
- Missed maintenance increases risk or reduces output.
- Labor contention can cause maintenance backlog.

### Sprint 20: Household Profiles And Labor Availability

Status: implemented as authored household profiles with care load, protected labor, available commons labor, and demand adjustments.

Replace the single population count with household demand and availability profiles.

Acceptance criteria:
- Demand is derived from household composition.
- Protected labor limits are honored.
- Care load reduces available commons labor.
- Role coverage failures are visible in the daily state.

### Sprint 21: Failure Mode Runtime

Status: implemented as scenario-triggered runtime failures with resource effects, response labor, active daily state, and review dependencies.

Make pattern failure modes executable inside scenarios.

Acceptance criteria:
- Scenario events can activate pattern failure modes.
- Failures produce state changes, response tasks, downtime, and recovery.
- Survival-critical unresolved failures block promotable simulation status.

### Sprint 22: Spatial Readiness Layer

Status: implemented as authored spatial profiles and compiled layout graphs.

Add a layout graph that is still non-visual but ready for later visualization.

Acceptance criteria:
- Patterns can declare zones, adjacency needs, access needs, and hazards.
- The compiler emits a layout graph.
- The simulation can reference distances or access constraints.

### Sprint 23: Runtime Bundle Export

Status: implemented as a viewer-oriented bundle manifest for plan, layout, simulation, and scenario artifacts.

Package current runtime artifacts into one stable JSON handoff contract.

Acceptance criteria:
- Bundle includes manifest, site/layout, systems, compressed timeline, scenario deltas, viewer hints, and unknowns.
- Source artifacts remain authoritative.
- Bundle validates as `RuntimeBundle`.

### Sprint 24: Static Runtime Viewer

Status: implemented as a local static web viewer for `RuntimeBundle` artifacts.

Render the bundle without creating a 3D or Unreal layer.

Acceptance criteria:
- Viewer loads the generated runtime bundle.
- Layout zones, systems, resources, maintenance, failures, scenarios, and warnings are inspectable.
- Viewer remains explicitly provisional and does not imply real-world readiness.

### Sprint 25: Viewer Playback Polish

Status: implemented as day playback, selected-system details, scenario overlays, warning highlights, and failure reasons.

Improve the first viewer into a more useful inspection dashboard.

Acceptance criteria:
- Day playback is available.
- Selecting a system reveals hazards, access needs, critical resources, warnings, and scenario failures.
- Spatial warnings and scenario failures are visible on the map.
- Failure reasons are summarized without hiding provisional status.

### Sprint 26: Minimum Viable Resource Baseline

Status: implemented as plain reserve patterns for emergency water, staple food, and critical energy.

Add just enough resource buffer to move the normal-year simulation from shortage inspection into viable baseline inspection, without selecting elaborate best-fit infrastructure too early.

Acceptance criteria:
- Water, food, and energy reserve patterns validate like ordinary civic patterns.
- The 5-household site profile includes the reserves explicitly.
- Normal-year simulation keeps water, food, and energy balances above zero.
- Each reserve still declares stewardship, review dependencies, maintenance, failure modes, and provisional assumptions.

### Sprint 27: Storage And Inventory State

Status: implemented as provisional storage specs and daily drawdown/refill state.

Make reserves finite and inspectable without adding a complex logistics model.

Acceptance criteria:
- Reserve patterns declare capacity, initial fill, reserve floor, max release, max refill, refill mode, and access rule.
- The compiler emits `storage_by_pattern`.
- `ciac simulate` exposes raw daily balance separately from storage release/refill.
- Daily state and runtime bundles include storage state for viewer inspection.
- Scenario balances account for storage buffers without double-counting drawdown.

### Sprint 28: Storage Quality Clock

Status: implemented as maintenance-linked quality checks, warning/failure thresholds, and provisional post-unsafe quantity loss.

Make stored resources age enough to expose neglected inspection and rotation, while keeping the model small.

Acceptance criteria:
- Storage specs declare check interval, unsafe-after threshold, post-unsafe loss rate, risk, and recovery action.
- Completed reserve maintenance resets quality clocks.
- Deferred checks can make storage warn or fail.
- Daily state, storage summaries, runtime bundles, and the viewer expose quality status.
- Tests cover a deferred reserve check becoming a storage quality warning.

### Sprint 29: Storage Recovery Playbooks

Status: implemented as explicit recovery tasks with role, labor, duration, and review dependency.

Make failed storage produce visible work instead of only a status flag.

Acceptance criteria:
- Storage quality specs declare recovery role, labor hours, duration, and review dependency.
- Failed storage quality emits daily `storage_recovery_tasks`.
- Recovery labor contributes to daily and summary labor burden.
- Runtime bundles and the viewer expose recovery tasks.
- Tests cover a failed potable reserve creating recovery work.

### Sprint 30: Bounded Recovery State

Status: implemented as stateful recovery task progress, labor contention, and review blocking.

Make recovery tasks carry state across days instead of reappearing as isolated daily work.

Acceptance criteria:
- A failed store opens one recovery task.
- Recovery tracks worked hours, remaining hours, and days active.
- Daily spare labor after maintenance and active failure response works recovery down.
- Recovery can be `in_progress`, `stalled_labor`, or `blocked_review`.
- Summary output reports active task count, worked hours, remaining hours, review-blocked count, and stalled days.
- Tests cover multi-day recovery progress and review blocking.

### Sprint 31: Review Dependency Runtime

Status: implemented as optional review-status input to simulation and recovery review gating.

Make professional review evidence a runtime condition for resolving recovery, rather than an external report only.

Acceptance criteria:
- `ciac simulate` accepts `--review-status`.
- Simulation output includes `review_context`.
- Recovery tasks include review dependency state.
- Recovery resolves only when the dependency is accepted, not expired or rejected, and has no unresolved issues.
- Tests cover accepted evidence resolving recovery and unresolved evidence keeping recovery blocked.

### Sprint 32: Scenario Review Context

Status: implemented as scenario-authored review stress inputs and report output.

Make review evidence itself stress-testable at scenario level.

Acceptance criteria:
- Scenario YAML can declare `review_context_overrides`.
- Scenario reports include a structured `review_context`.
- Failure timelines include review context events.
- Blocked review domains produce bottlenecks and redesign recommendations.
- Runtime bundles and the viewer expose scenario review events.
- Tests cover a failed retest blocking review recovery in a contamination scenario.

### Sprint 33: Scenario Replay Simulation

Status: implemented as `ciac simulate --scenario` with daily replay effects.

Apply scenario stressors inside the daily simulation loop instead of only producing side reports.

Acceptance criteria:
- `ciac simulate` accepts a scenario YAML path.
- Daily resource production and consumption reflect scenario multipliers and deltas.
- Scenario emergency tasks appear as daily events and labor burden.
- Triggered failures still affect resources and labor during replay.
- Review-context overrides can block recovery even when a review-status report would otherwise accept the dependency.
- Runtime bundles preserve replay `scenario_context` and daily `scenario_events`.

### Sprint 34: Replay Comparison

Status: implemented as `ciac compare-simulations`.

Compare normal simulation output against a scenario replay so the scenario's effect is legible without reading every daily state.

Acceptance criteria:
- The CLI compares two `SimulationRun` artifacts.
- Output reports resource, storage, labor, unmet-need, failure-day, recovery, and review-context deltas.
- Stress failures return a nonzero CLI status while still writing the report.
- Output validates as `SimulationComparisonReport`.
- Tests cover stress-failed, stable, CLI, and shape behavior.

### Sprint 35: Replay Matrix

Status: implemented as `ciac replay-matrix`.

Rank multiple replay comparisons so the most threatening modeled stressors are visible together.

Acceptance criteria:
- The CLI accepts one or more `SimulationComparisonReport` artifacts.
- Output validates as `ReplayMatrixReport`.
- Matrix rows include scenario, status, total stress score, per-day stress score, unmet demand, emergency labor, active failure days, blocked review counts, and top bottlenecks.
- Rankings identify the top stressor.
- Tests cover ranked, stable, empty-input, and CLI behavior.

### Sprint 36: Matrix Redesign

Status: implemented as `ciac redesign-matrix`.

Translate top replay-matrix stressors into small, testable redesign candidates.

Acceptance criteria:
- The CLI accepts a compiled plan and `ReplayMatrixReport`.
- Output validates as `MatrixRedesignReport`.
- Candidates include target scenarios, minimum viable change, expected effect, tradeoffs, files to edit, acceptance criteria, and matrix evidence.
- Candidate priority favors minimum viable dignified existence over complex best-fit technology.
- Tests cover validation, priority, candidate coverage, CLI, and shape behavior.

### Sprint 37: Food Reserve Redesign Loop

Status: implemented as source YAML updates plus regenerated replay matrix.

Apply the first matrix redesign candidate and measure whether it improves the stress ranking.

Acceptance criteria:
- `staple_food_reserve` declares a stronger protected staple inventory and procurement floor.
- `crop_failure` declares bounded runtime failure overrides for acute response duration and labor.
- Crop failure replay comparison shows reduced labor pressure and active failure days.
- Replay matrix no longer ranks crop failure as the top total stressor.
- Matrix redesign advances the next priority to water response buffer work.

### Sprint 38: Water Response Buffer Loop

Status: implemented as source YAML updates plus regenerated replay matrix.

Apply the water response candidate and measure whether contamination, drought, and sanitation replays preserve minimum water access.

Acceptance criteria:
- `emergency_water_reserve` declares a larger protected reserve and higher emergency release path.
- Water reserve plan increases response buffer targets and demand reduction.
- Contamination, drought, and sanitation scenarios include bounded runtime failure overrides.
- Contamination, drought, and sanitation replay comparisons report zero water unmet demand.
- Failed water review remains blocked; the model does not convert failed retest into safety clearance.
- Matrix redesign advances the next priority to labor surge buffer work.

### Sprint 39: Scenario Labor Surge Buffer Loop

Status: implemented as source YAML updates, scenario schema extension, simulation support events, and planner-priority cleanup.

Make emergency labor spikes explicit without silently treating residents as spare capacity.

Acceptance criteria:
- Scenario YAML can declare `labor_support` events with source, hours, start day, duration, and notes.
- Simulation applies support hours to available commons labor without changing resident population.
- Daily scenario events expose the labor-support event.
- Replay comparisons report zero labor unmet demand across crop failure, drought, sanitation failure, water contamination, energy outage, and resident-exit stress replays.
- Matrix redesign stops recommending the labor surge candidate once no replay reports labor unmet demand.

### Sprint 40: Simulation Foundation Gate

Status: implemented as `ciac foundation-gate` plus a generated `FoundationGateReport`.

Turn the simulation foundation goal into an explicit artifact-level readiness check.

Acceptance criteria:
- The CLI accepts compiled plan, baseline simulation, runtime bundle, replay matrix, optional review status, and optional comparison reports.
- Output validates as `FoundationGateReport`.
- The report checks baseline health, minimum dignity ledger coverage, water/food/energy replay coverage, unmet survival demand, runtime viewer contract, review visibility, and warning legibility.
- The current generated artifact set reports `ready_with_warnings`, not `not_ready`.
- Tests cover current readiness, stress failure regression, CLI output, and schema validation.

### Sprint 41: Foundation Demo Viewer Pass

Status: implemented as a static viewer update.

Make the foundation gate visible in the existing viewer before adding any new civic modeling.

Acceptance criteria:
- The viewer loads `micro_commons_foundation_gate.json` by default beside the runtime bundle.
- The viewer exposes foundation status, check evidence, warning checks, baseline length, replay matrix status, and bundled scenario count.
- The viewer preserves explicit non-proof language.
- Tests cover default artifact references, UI sections, styles, and generated gate readiness.

### Sprint 42: Optimization Readiness

Status: implemented as pattern optimization metadata, optimization profile, CLI report, and generated artifact.

Make future optimization possible without yet generating candidate plans.

Acceptance criteria:
- Civic patterns can optionally declare optimization tunables, locked parameters, scaling mode, and objectives.
- `emergency_water_reserve`, `staple_food_reserve`, and `critical_load_reserve` expose provisional tunable parameters.
- Safety/review-bound claims remain locked behind review dependencies.
- `OptimizationProfile` declares provisional objectives, constraints, and scale targets.
- `ciac optimization-readiness` outputs a valid `OptimizationReadinessReport`.
- The generated report advances rolling metrics to 80%, 68%, and 50%.

### Sprint 43: Candidate Plan Generation

Status: implemented as `ciac candidate-matrix`.

Generate and compare a small candidate plan matrix from declared reserve tunables.

Acceptance criteria:
- The CLI accepts compiled plan, pattern directory, optimization profile, optional scenarios, optional review status, and baseline days.
- Candidate generation produces current, balanced reserve, and high-resilience reserve configurations.
- Each candidate runs baseline simulation and selected stress replays.
- Hard constraints reject candidates with unmet survival demand, missing review locks, or hidden labor ledger.
- Output validates as `CandidatePlanMatrixReport`.
- The generated report advances rolling metrics to 85%, 75%, and 65%.

### Sprint 44: Tradeoff And Scale Reports

Status: implemented as `ciac tradeoff-scale`.

Explain candidate tradeoffs and scaling pressure before implementing the optimizer loop.

Acceptance criteria:
- Add a `ScaleProfile` for 5, 10, 25, and 50 household targets.
- The CLI accepts compiled plan, candidate matrix, pattern directory, and scale profile.
- Output validates as `TradeoffScaleReport`.
- The report identifies objective leaders across candidates.
- The report scales declared candidate parameters according to pattern scaling metadata.
- The report includes viewer-ready candidate summaries.
- The generated report advances rolling metrics to 90%, 85%, and 80%.

### Sprint 45: Optimizer Loop

Status: implemented as `ciac optimize`.

Rank generated candidate configurations against authored goals and constraints before freezing the visualization contract.

Acceptance criteria:
- The CLI accepts a candidate matrix, optimization profile, optional tradeoff/scale report, and output path.
- Output validates as `OptimizerReport`.
- The report ranks candidates deterministically and selects only candidates with no hard constraint failures.
- Constraint warnings and failures identify the specific constraint involved.
- Sensitivity checks show whether the selected candidate changes when an objective weight is emphasized.
- The generated report advances rolling metrics to 95%, 92%, and 90%.

### Sprint 46: Visualization Contract Freeze

Status: implemented as `ciac export-visualization`.

Freeze the current runtime and optimization artifacts into a single versioned visualization handoff.

Acceptance criteria:
- The CLI accepts runtime bundle, foundation gate, candidate matrix, tradeoff/scale report, optimizer report, and output path.
- Output validates as `VisualizationBundle`.
- The bundle exposes stable entrypoints for site, systems, daily timeline, scenarios, foundation checks, candidate summaries, rankings, sensitivity checks, and constraint explanations.
- The bundle preserves selected candidate, objective sensitivity behavior, review warnings, and non-proof language.
- The generated report advances rolling metrics to 100%, 100%, and 95%.

### Sprint 47: Search Optimizer

Status: implemented as `ciac optimize-search`.

Move from ranking three hand-shaped candidate modes to bounded deterministic search across reserve-family parameter combinations.

Acceptance criteria:
- The CLI accepts compiled plan, pattern directory, optimization profile, optional scenarios, optional review status, baseline days, top count, and output path.
- Output validates as `SearchOptimizerReport`.
- The search space groups tunables by water, food, and energy reserve family.
- The report lists generated, viable, and rejected candidate counts.
- Top candidates include family levels, parameter deltas, objective scores, tradeoffs, and constraint results.
- Binding constraints identify hard survival-demand failures and soft repeatability warnings.
- Locked safety/review assumptions remain explicit.
- The generated report advances rolling metrics to 100%, 100%, and 98%.

### Sprint 48: Objective Calibration

Status: implemented as `ciac objective-calibration`.

Make optimizer scores inspectable before adding broader pattern-family search.

Acceptance criteria:
- Add an `ObjectiveCalibrationProfile` schema.
- Add an `ObjectiveCalibrationReport` schema.
- The CLI accepts a search optimizer report, calibration profile, and optional output path.
- The report validates as `ObjectiveCalibrationReport`.
- Every selected-candidate objective has a formula id, input list, evidence status, review requirement, interpretation, and false-precision warning.
- Missing metric calibration returns `missing_calibration`.
- Governance status keeps weight authority, resident consent, and review status visible.
- The generated report advances rolling metrics to 100%, 100%, and 99%.

### Sprint 49: Weight Governance

Status: implemented as `ciac weight-governance`.

Represent objective-weight authority and block unratified optimizer recommendations.

Acceptance criteria:
- Add a `WeightGovernanceProfile` schema.
- Add a `WeightGovernanceReport` schema.
- The CLI accepts an optimization profile, objective calibration report, weight governance profile, and optional output path.
- The report validates as `WeightGovernanceReport`.
- The report compares governed weights against optimization-profile weights.
- Draft resident consent and professional review statuses block promotion.
- A ratified test path can promote only when weights are ratified and objective calibration is accepted.
- The generated report advances rolling metrics to 100%, 100%, and 100%.

## Current Simulation Foundation Status

The project now has validation, compilation, subsystem reports, scenarios, audit, dossier, review status, Markdown export, a daily simulation ledger, authored seasonal multipliers, maintenance backlog/degradation, household-level labor/demand profiles, runtime failure effects, a spatial layout graph, a viewer-ready runtime bundle, a static viewer, minimum viable reserves, finite storage state, storage quality clocks, storage recovery playbooks, bounded recovery progress, runtime review gating, scenario-level review context, scenario replay, replay comparison, a replay matrix, matrix-derived redesign candidates, measured food/water/labor redesign loops, a foundation gate report, a viewer panel for that foundation gate, optimization-readiness metadata for reserve patterns, a generated candidate matrix, a tradeoff/scale report, an optimizer report, a versioned visualization bundle, a bounded search optimizer report, an objective calibration report, and a weight governance report.

The current matrix is `stress_warn`, not `stress_failed`: tracked unmet resource demand is zero across the generated stress replays, while long active failure windows, partial food modeling, short-window energy outage intensity, and review evidence gaps remain visible warnings. The current foundation gate is `ready_with_warnings`.

Next work should not be automatic churn. The foundation and optimizer data-contract targets are complete for the micro-commons proof of concept. Future work should either build the richer visualization against the bundle or deliberately expand optimizer fidelity with sourced evidence and optional pattern families.

Avoid new modeling detail unless it makes the bundle more faithful, closes a measurable optimization gap, or supports the next visualization milestone.
