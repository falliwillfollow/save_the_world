# Capability Policy v0

CIaC now includes a provisional capability policy layer for non-resource civic capabilities: care, governance, mobility, legal/finance, risk resilience, and labor/time.

The policy lives at `capability_policies/ciac_capability_policy_v0.yaml` and is validated by `schemas/capability_policy.schema.json`.

## Purpose

The capability policy turns research thresholds into executable model gates. It does not replace `CapabilityState`; it evaluates the existing state with a stricter, sourced policy layer.

## Status Modes

- `pass`: The modeled field satisfies the provisional policy threshold.
- `warn`: The model remains useful for simulation, but an important capability is missing, incomplete, unknown, or below target.
- `fail`: The modeled state contradicts a critical threshold.
- `promotion_blocked`: In promotion mode, the model cannot support real-world readiness claims until the blocker is resolved.

Runtime bundles also expose:

- `simulation_only`: useful for visualization and reasoning, not a real-world claim.
- `review_blocked`: internally useful but blocked by missing policy or external review.
- `promotion_ready`: internal policy gates pass and no promotion blockers remain.

## What It Does Not Prove

Capability policy results are provisional modeling aids. They do not certify real-world safety, legality, accessibility, clinical validity, affordability, labor compliance, engineering validity, public-health compliance, resident consent, or buildability.

## Adding A Gate

1. Add the capability field to the domain's `capability_fields`.
2. Add an executable gate with `pass_condition`, `warn_condition`, `fail_condition`, and `promotion_block_condition`.
3. Use simple clauses such as `equals`, `not_equals`, `min`, `max`, `above`, `below`, `between`, or `missing`.
4. Attach source IDs from `source_registry`.
5. Add or update tests in `tests/test_capability_policy.py` or `tests/test_capability_gate_policy.py`.

## Scenario Pack

The initial capability scenarios live under `scenarios/capability/`. They are not full stochastic simulations yet; they are structured stress-test contracts that name required fields, shocks, and expected gates.
