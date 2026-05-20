# CIaC Simulation Foundation Goal

CIaC is not trying to become a complete engineering simulator before visual buildout. The near-term goal is narrower:

**Produce one credible, inspectable minimum-dignified-existence simulation loop for a 5-household micro-commons.**

That loop should make water, food, energy, sanitation, labor, maintenance, failures, recovery, governance, and review blockers visible enough to reason about as structured data. It does not need to optimize technology choices, certify safety, prove legality, or model every real-world dependency.

## Foundation Outcome

The simulation foundation is good enough for visual buildout when:

1. The normal-year baseline can run without hidden survival-resource failure.
2. Stress scenarios expose unmet demand, active failures, recovery work, labor pressure, and review blockers as explicit JSON.
3. Water, food, energy, sanitation, and labor each have a minimum viable state model, not just a narrative report.
4. Remaining warnings are named limitations, not silent assumptions.
5. The runtime bundle and viewer can inspect the system over time without reading Python source.
6. Every high-stakes value remains provisional unless backed by later jurisdictional, engineering, legal, health, or resident-consent review.

## Stop Conditions

Do not keep iterating just because a generated report has a warning. A warning is acceptable when it is:

- explicit in generated JSON,
- visible in the viewer or review packet,
- not hiding unmet survival demand,
- tied to a clear future evidence requirement, and
- not needed for the next visual or interaction milestone.

The current foundation can move toward visual buildout once the viewer can demonstrate:

- baseline resource flows over time,
- one water stress replay,
- one food or procurement stress replay,
- one energy stress replay,
- maintenance or recovery work competing for labor,
- review evidence blocking unsafe recovery claims.

## Complexity Gate

Add new modeling detail only when it does at least one of these:

- prevents false confidence,
- closes a survival-critical accounting gap,
- makes simulation behavior clearer to inspect,
- stabilizes the JSON contract for later visualization,
- reduces a measured failure without hiding review, labor, governance, or external dependency.

Do not add detail only because it is realistic, interesting, visually impressive, or technically possible.

## Minimum Viable Dignity Scope

Minimum viable dignified existence means the model should preserve:

- drinking, cooking, and hygiene water visibility,
- basic food coverage and procurement fallback visibility,
- critical energy visibility for refrigeration, communication, lighting, and controls,
- sanitation capacity and public-health review visibility,
- shelter and shared-facility maintenance visibility,
- resident labor limits, care load, refusal/exit, and backup visibility,
- governance stewardship and review requirements for survival-critical systems.

It does not mean complete autonomy, optimal technology, full nutrition science, complete building design, jurisdiction-specific compliance, or emergency-plan certification.

## Current Position

As of Sprint 40, the project has a working deterministic simulation substrate with:

- compiled civic plans,
- daily resource ledgers,
- finite reserve state,
- storage quality and recovery clocks,
- household labor and demand profiles,
- seasonal multipliers,
- runtime failure effects,
- scenario replay,
- replay comparison,
- replay matrix,
- matrix-derived redesign candidates,
- review-status gating,
- runtime bundle export,
- static viewer inspection,
- a foundation gate report that checks readiness for visual buildout,
- a viewer panel that exposes the foundation gate result and warning evidence,
- optimization-readiness metadata for the minimum water, food, and energy reserve patterns,
- a generated candidate matrix for current, balanced-reserve, and high-resilience configurations,
- a tradeoff/scale report for 5, 10, 25, and 50 household targets,
- a deterministic optimizer report with ranked candidates, constraint explanations, and objective sensitivity checks,
- a versioned visualization bundle that exposes stable runtime and optimization entrypoints,
- a bounded search optimizer report that explores reserve-family combinations and rejects hard constraint failures,
- an objective calibration report that makes selected-candidate scores traceable to explicit proxy formulas and evidence status,
- a weight governance report that blocks unratified optimizer recommendations.

The current matrix is a warning state, not a failed state: generated stress replays report zero unmet resource demand across the tracked ledger resources, while still preserving long active failure windows, partial food modeling, short-window energy intensity, and review evidence gaps as visible warnings.

The current foundation gate is `ready_with_warnings`. That is useful. The visualization handoff can now proceed against a versioned bundle, while future modeling work should be chosen because it improves optimizer fidelity or the next viewer milestone, not because the matrix can always invent another candidate.

## Rolling Metrics

The current sprint-to-sprint estimates live in [progress_metrics.md](progress_metrics.md):

- Inspectable simulation proof of concept: ~100%
- Mature commune virtualization data contract: ~100%
- Faithful pattern optimization engine: ~100%

Future sprints should move these metrics in larger chunks toward repeatable pattern optimization, not just clear individual warnings.
