# CIaC Rolling Progress Metrics

These metrics are working estimates, not formal proof. Update them at the end of each sprint so the project does not drift into either false confidence or endless churn.

## Current Scores

| Track | Current Estimate | Meaning |
| --- | ---: | --- |
| Inspectable simulation proof of concept | 100% | CIaC can generate one coherent demo pack that exposes baseline, scenarios, foundation checks, candidate variants, and optimizer selection. |
| Mature commune virtualization data contract | 100% | CIaC exports a versioned visualization handoff bundle with stable runtime and optimization entrypoints. |
| Faithful pattern optimization engine | 100% | CIaC can search candidate configurations, calibrate selected objective scores, and block unratified weight profiles. |

## What 100% Means

### Inspectable Simulation Proof Of Concept

100% means the project can generate one coherent demo pack that a person can inspect without reading Python source:

- baseline 365-day run,
- water stress replay,
- food/procurement stress replay,
- energy stress replay,
- labor and maintenance pressure,
- review blockers,
- foundation gate,
- runtime bundle,
- static viewer,
- visualization handoff bundle.

The first demo-pack target is met. Future work should improve viewer interaction or add evidence-backed model fidelity, not inflate the foundation scope.

### Mature Commune Virtualization Data Contract

100% means the runtime JSON contract is stable enough for a richer web/game/Unreal-style virtualization:

- stable bundle manifest,
- explicit spatial graph,
- explicit pattern/system instances,
- baseline and replay timelines,
- foundation gate status,
- scenario overlays,
- warning and review states,
- optimization candidate metadata,
- scale profile metadata,
- optimizer report metadata,
- versioned visualization bundle entrypoints.

The first virtualization contract target is met for the micro-commons proof of concept. Future contract changes should be explicit schema-version updates.

### Faithful Pattern Optimization Engine

100% means CIaC can generate and compare candidate infrastructure configurations inside declared assumptions:

- parametric pattern variants,
- objective functions,
- hard constraints,
- candidate generation,
- deterministic scoring,
- tradeoff reports,
- scale tests,
- no hidden review, labor, governance, or external dependency.

The first optimizer-engine target is met as a software/data contract. Real-world optimization remains blocked until sourced objective math, professional review, and resident-approved weight profiles exist.

## Larger Sprint Chunks

The next phase should use larger chunks that move all three metrics, instead of small single-warning cleanup.

### Chunk A: Optimization Readiness

Status: implemented as Sprint 42.

Target movement:

- Inspectable simulation proof: 75% -> 80% complete
- Virtualization contract: 60% -> 68% complete
- Optimization engine: 35-45% -> 50% complete

Deliverables:

- `PatternVariant` or equivalent schema for tunable pattern parameters.
- Optimization objective and constraint schema.
- Read-only optimization readiness report.
- At least water, food reserve, and energy reserve expose safe provisional variant fields.

Exit gate:

- CIaC can say which pattern variables are tunable and which are locked by review/safety constraints. Met by `micro_commons_optimization_readiness.json`.

### Chunk B: Candidate Plan Generation

Status: implemented as Sprint 43.

Target movement:

- Inspectable simulation proof: 80% -> 85% complete
- Virtualization contract: 68% -> 75% complete
- Optimization engine: 50% -> 65% complete

Deliverables:

- Generate a small matrix of candidate plans from declared variants.
- Compile and simulate each candidate deterministically.
- Preserve all generated candidate artifacts as JSON.
- Compare candidates against baseline objectives.

Exit gate:

- CIaC can compare at least three viable candidate configurations without hand-authoring each whole plan. Met by `micro_commons_candidate_matrix.json`.

### Chunk C: Tradeoff And Scale Reports

Status: implemented as Sprint 44.

Target movement:

- Inspectable simulation proof: 85% -> 90% complete
- Virtualization contract: 75% -> 85% complete
- Optimization engine: 65% -> 80% complete

Deliverables:

- Tradeoff report showing cost/labor/resilience/external-dependency differences.
- Scale profile for 5, 10, 25, and 50 households.
- Explicit scaling assumptions for shared systems.
- Viewer-ready candidate summary export.

Exit gate:

- CIaC can explain which candidate is best under which objective and how it changes as population scales. Met by `micro_commons_tradeoff_scale.json`.

### Chunk D: Optimizer Loop

Status: implemented as Sprint 45.

Target movement:

- Inspectable simulation proof: 90% -> 95%
- Virtualization contract: 85% -> 92%
- Optimization engine: 80% -> 90%

Deliverables:

- Deterministic optimizer command.
- Ranked candidate configurations.
- Constraint failure explanations.
- Objective sensitivity checks.
- Regression tests for optimization stability.

Exit gate:

- CIaC can produce a ranked infrastructure configuration set from authored goals and constraints. Met by `micro_commons_optimizer_report.json`.

### Chunk E: Virtualization Contract Freeze

Status: implemented as Sprint 46.

Target movement:

- Inspectable simulation proof: 95% -> 100%
- Virtualization contract: 92% -> 100%
- Optimization engine: 90% -> 95%

Deliverables:

- Versioned runtime/optimization bundle.
- Schema snapshots for viewer consumers.
- Demo pack with baseline, replays, candidate comparisons, and selected optimized plan.
- Clear non-proof language retained across all artifacts.

Exit gate:

- A mature visualization can consume CIaC output without reverse-engineering internal Python structures. Met by `micro_commons_visualization_bundle.json`.

### Chunk F: Bounded Search Optimizer

Status: implemented as Sprint 47.

Target movement:

- Inspectable simulation proof: stays 100%
- Virtualization contract: stays 100%
- Optimization engine: 95% -> 98%

Deliverables:

- Deterministic `optimize-search` command.
- Family-level search over water, food, and energy reserve tunables.
- Candidate counts for generated, viable, and rejected combinations.
- Binding constraint report.
- Locked safety/review assumptions retained in search output.
- Regression tests for search shape and schema stability.

Exit gate:

- CIaC can search a bounded configuration space, reject hard-constraint failures, and explain the selected candidate. Met by `micro_commons_search_optimizer_report.json`.

### Chunk G: Objective Calibration

Status: implemented as Sprint 48.

Target movement:

- Inspectable simulation proof: stays 100%
- Virtualization contract: stays 100%
- Optimization engine: 98% -> 99%

Deliverables:

- Objective calibration profile schema.
- Objective calibration report schema.
- `objective-calibration` command.
- Calibration profile for minimum-dignity objectives.
- Formula id, input list, evidence status, review requirement, interpretation, and false-precision warning for each selected-candidate objective.
- Regression tests for missing calibration and schema stability.

Exit gate:

- CIaC can explain what every selected-candidate objective score means and what evidence status supports it. Met by `micro_commons_objective_calibration.json`.

### Chunk H: Weight Governance

Status: implemented as Sprint 49.

Target movement:

- Inspectable simulation proof: stays 100%
- Virtualization contract: stays 100%
- Optimization engine: 99% -> 100%

Deliverables:

- Weight governance profile schema.
- Weight governance report schema.
- `weight-governance` command.
- Draft weight profile for `minimum_dignity_v0`.
- Promotion blocker for unratified resident consent and unaccepted professional review.
- Regression tests for draft-blocking and ratified-path behavior.

Exit gate:

- CIaC can represent weight authority, compare governed weights to the optimization profile, and block unratified recommendations. Met by `micro_commons_weight_governance.json`.

## Rules For Updating Metrics

- Increase a score only when tests and generated artifacts support the claim.
- Keep review, legal, health, engineering, and consent limits visible even if a score improves.
- Do not count purely visual polish toward optimization progress unless it stabilizes the data contract.
- Do not count new realism detail unless it improves generation, comparison, scaling, or inspection.
