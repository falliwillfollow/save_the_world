# CIaC Implementation Plan: Capability State Layer

**Plan ID:** `sprint_52_capability_state_layer_v0_1`  
**Target repo:** `falliwillfollow/save_the_world`  
**Prepared for:** coding agent implementation  
**Status:** actionable planning draft  
**Primary goal:** Extend the current resource-based simulator so mature village-block modules can affect the civic floor through dignity, labor, governance, care, access, legal/finance, social/cultural, education, maintenance, and resilience capabilities.

---

## 1. Executive Summary

The repo now contains a mature pattern library for the dignified village block, but the runtime still primarily understands modules through resource effects such as:

```text
water_liters_per_day
energy_kwh_per_day
food_servings_per_day
```

That is correct for early water/food/energy simulation, but it is too narrow for modules like:

```text
life_burden_ledger
commons_stewardship_protocol
community_care_commons
anti_speculative_civic_floor
civic_skill_lattice
belonging_without_coercion_commons
graceful_degradation_engine
```

These modules do not prove their value by producing water, food, or energy. They prove value by reducing hidden labor, improving role backup, protecting high-need residents, lowering capture risk, preserving privacy, increasing legal/finance visibility, and improving graceful degradation.

The next required implementation is therefore a **Capability State Layer**.

---

## 2. Core Problem

### Current model

The existing simulation has a strong resource substrate:

```text
sources
uses
storage
reserve release/refill
curtailment
maintenance
labor
failure/review states
scenario replay
```

The technology-module implementation path currently applies explicit direct resource effects and blocks modules that declare no nonzero resource effect or reduce a dignity-floor resource.

This is good for early technology candidates.

### Missing model

The matured CIaC module library also needs civic capabilities such as:

```text
privacy
role backup
governance legitimacy
anti-capture protection
care continuity
high-need resident support
accessible routes
transport dignity
skill redundancy
maintenance readiness
legal/finance resilience
social belonging without coercion
graceful degradation
```

The simulator needs to represent these capabilities as first-class state.

---

## 3. Design Principle

> A non-resource module must be able to improve or worsen the simulated civic floor without pretending to produce water, food, or energy.

This layer should not replace the existing resource simulator. It should sit beside it.

```text
ResourceState:
  water
  food
  energy
  storage
  flows
  failures

CapabilityState:
  dignity
  labor
  governance
  care
  access
  legal_finance
  maintenance
  education
  social_cultural
  risk_resilience
```

---

## 4. Non-Goals

Do **not** do these in this sprint:

```text
Do not build Unreal integration.
Do not redesign the whole simulator.
Do not add more module concepts.
Do not require all existing patterns to have complete capability effects immediately.
Do not remove current resource_effects behavior.
Do not make capability scores look like real-world proof.
Do not create a social-credit system.
Do not automate resident rights, medical judgment, legal judgment, or safety certification.
```

The goal is a minimal but extensible state layer.

---

## 5. New Concept: Capability Effects

Add optional `capability_effects` to `CivicPattern`.

These effects describe how a pattern/module changes civic-floor capabilities.

### Example

```yaml
capability_effects:
  labor_time:
    required_wage_hours_delta_percent: -20
    commons_labor_hours_per_resident_per_week_delta: 4
    hidden_labor_risk_delta: -2
    burnout_risk_delta: -1

  governance:
    due_process_defined: true
    emergency_power_sunset_defined: true
    capture_risk_delta: -2
    role_backup_coverage_delta: 0.15

  care_health:
    high_need_support_coverage_delta: 0.20
    medication_continuity_supported: true
    care_meal_protocol_supported: true

  resilience:
    scenario_coverage_delta: 5
    dependency_graph_coverage_delta: 0.25
    recovery_playbook_count_delta: 3
```

---

## 6. Capability Domains

Use these top-level domains for v0.

```yaml
capability_domains:
  dignity_privacy:
    purpose: private retreat, opt-out, acoustic/privacy protection, dignity floors

  labor_time:
    purpose: wage dependency, commons labor, hidden labor, burnout, free time

  governance_anticapture:
    purpose: due process, asset lock, role backup, emergency sunset, capture risk

  care_health:
    purpose: high-need residents, medication continuity, care meals, telehealth, first aid

  mobility_access:
    purpose: accessible routes, non-driver dignity, emergency access, transport burden

  legal_land_finance:
    purpose: land security, affordability, reserves, debt risk, insurance/tax review

  maintenance_repair:
    purpose: asset registry, class A coverage, backlog, spares, professional handoff

  education_skill:
    purpose: skill redundancy, onboarding, safety gates, knowledge base, training burden

  social_cultural:
    purpose: belonging, opt-out protection, anti-clique, third places, cultural flourishing

  risk_resilience:
    purpose: hazard register, dependency graph, service levels, buffers, recovery, scenarios

  materials_fabrication:
    purpose: maintainability, code path, embodied impact, panelization, build readiness
```

---

## 7. Effect Types

Support a small set of value types.

```yaml
effect_value_types:
  numeric_delta:
    examples:
      capture_risk_delta: -2
      hidden_labor_risk_delta: -1
      commons_labor_hours_per_week_delta: 4

  numeric_absolute:
    examples:
      common_space_ratio: 0.25
      protein_buffer_days: 30

  boolean_flag:
    examples:
      due_process_defined: true
      private_food_autonomy: true
      emergency_power_sunset_defined: true

  coverage_ratio_delta:
    examples:
      role_backup_coverage_delta: 0.15
      accessible_route_coverage_delta: 0.2

  count_delta:
    examples:
      scenario_coverage_delta: 5
      recovery_playbook_count_delta: 3

  enum_status:
    examples:
      land_security_status: provisional
      legal_review_status: required

  warning_flag:
    examples:
      review_required: true
      consent_required: true
      professional_review_required: true
```

Keep this deliberately simple.

---

## 8. New Object: CapabilityState

Add a new runtime object.

### Suggested file

```text
ciac/capabilities.py
```

### Responsibilities

```text
- Define default capability state.
- Normalize capability effects from patterns.
- Apply effects to state.
- Clamp ratios/scores into sensible ranges.
- Emit status/warnings/failures.
- Produce a capability ledger for reports and viewer bundles.
```

### Minimal structure

```python
CapabilityState = dict[str, Any]
CapabilityEffects = dict[str, Any]
CapabilityLedgerEntry = dict[str, Any]
```

Avoid premature dataclass complexity unless the existing codebase favors it.

### Baseline state

Create a function:

```python
def default_capability_state(population: int | None = None) -> dict[str, Any]:
    ...
```

Suggested defaults should be provisional and conservative.

Example:

```python
{
    "kind": "CapabilityState",
    "version": "v0",
    "provisional": True,
    "domains": {
        "dignity_privacy": {
            "privacy_floor": "unknown",
            "private_retreat_supported": False,
            "opt_out_protected": False,
            "dignity_risk_score": 5,
        },
        "labor_time": {
            "required_wage_hours_reduction_percent": 0,
            "commons_labor_hours_per_resident_per_week": 0,
            "hidden_labor_risk_score": 5,
            "burnout_risk_score": 5,
            "free_time_increase_supported": False,
        },
        ...
    },
    "ledger": [],
    "warnings": [],
    "failures": [],
}
```

---

## 9. Schema Changes

### 9.1 Update `schemas/civic_pattern.schema.json`

Add optional `capability_effects`.

Do not make it required yet.

Recommended schema shape:

```json
"capability_effects": {
  "type": "object",
  "additionalProperties": {
    "type": "object",
    "additionalProperties": {
      "oneOf": [
        {"type": "number"},
        {"type": "integer"},
        {"type": "boolean"},
        {"type": "string"},
        {"type": "array"},
        {"type": "object"}
      ]
    }
  }
}
```

Keep schema permissive for v0 so existing pattern validation is not brittle.

### 9.2 Add `schemas/capability_state.schema.json`

Minimal required fields:

```json
{
  "kind": "CapabilityState",
  "version": "v0",
  "provisional": true,
  "domains": {},
  "ledger": [],
  "warnings": [],
  "failures": []
}
```

### 9.3 Optional: add `schemas/capability_report.schema.json`

Use this if reports are already schema-validated.

---

## 10. Compiler Changes

### Target file

```text
ciac/compiler.py
```

### Required change

When compiling patterns, collect capability effects into `simulation_inputs`.

Existing resource effects should remain untouched.

Add:

```python
simulation_inputs["capability_effects_by_pattern"] = {
    pattern_id: pattern.get("capability_effects", {})
    for pattern in selected_patterns
}
```

Also preserve pattern-level provenance.

```python
simulation_inputs["capability_metadata_by_pattern"] = {
    pattern_id: {
        "name": pattern.get("name", pattern_id),
        "scale": pattern.get("scale", ""),
        "provisional": pattern.get("provisional", True),
    }
}
```

### Backward compatibility

If no pattern declares `capability_effects`, compile should still succeed and `capability_effects_by_pattern` should be `{}`.

---

## 11. Simulation Changes

### Target file

```text
ciac/simulation.py
```

### Required change

At simulation start:

```python
from .capabilities import default_capability_state, apply_capability_effects

capability_state = default_capability_state(population=population)
```

Then apply compiled pattern effects:

```python
for pattern_id, effects in simulation_inputs.get("capability_effects_by_pattern", {}).items():
    capability_state = apply_capability_effects(
        capability_state,
        pattern_id=pattern_id,
        effects=effects,
        source="selected_pattern",
    )
```

### Scenario support

If scenario files later include capability shocks, apply those too.

For v0, support this optional structure:

```yaml
capability_shocks:
  labor_time:
    commons_labor_hours_per_resident_per_week_delta: 2
    burnout_risk_delta: 1
  governance_anticapture:
    emergency_power_drift_risk_delta: 2
```

### Simulation output

Add to simulation output:

```json
"capability_state": {...},
"capability_warnings": [],
"capability_failures": []
```

Do not break existing output keys.

---

## 12. Module Implementation Changes

### Target file

```text
ciac/module_implementation.py
```

### Current behavior to preserve

The current implementation applies explicit direct resource effects from technology modules, compares baseline vs implemented simulations, and blocks modules with no nonzero direct resource effect.

### Required change

Do not require non-resource civic modules to declare resource effects if they declare capability effects.

Change blocker logic from:

```text
must have nonzero direct resource effect
```

to:

```text
must have either:
  - nonzero direct resource effect
  - nonempty capability_effects
```

### Suggested logic

```python
def _capability_effects(module: dict[str, Any]) -> dict[str, Any]:
    return module.get("modeled_impacts", {}).get("capability_effects", {}) or module.get("capability_effects", {}) or {}

def _has_nonzero_resource_effect(effects: dict[str, float]) -> bool:
    return any(value != 0 for value in effects.values())

def _has_capability_effects(effects: dict[str, Any]) -> bool:
    return bool(effects)

def _effect_blockers(resource_effects, capability_effects):
    blockers = []
    if not _has_nonzero_resource_effect(resource_effects) and not _has_capability_effects(capability_effects):
        blockers.append("Declare at least one nonzero direct CIaC resource effect or one capability_effect before implementation.")
    ...
```

### Applied plan

In `_implemented_plan`, add:

```python
simulation_inputs["capability_effects_by_pattern"][module_pattern_id] = capability_effects
```

### Report output

Add:

```json
"applied_capability_effects": {...}
```

Keep `"applied_effects"` for existing resource effects.

---

## 13. Foundation Gate v2

### Target

Find the existing foundation/floor gate code. If there is no isolated module, create:

```text
ciac/capability_gate.py
```

or:

```text
ciac/foundation_gate.py
```

depending on existing code organization.

### Purpose

Evaluate civic-floor capability failures alongside resource failures.

### Initial gate domains

```yaml
foundation_capability_gates:
  dignity_privacy:
    fail_if:
      - private_retreat_supported is false for village-block pattern
      - opt_out_protected is false where social/cultural module is active

  labor_time:
    fail_if:
      - hidden_labor_risk_score >= 8
      - burnout_risk_score >= 8
      - commons_labor_hours_per_resident_per_week > 12

  governance_anticapture:
    fail_if:
      - due_process_defined is false
      - emergency_power_sunset_defined is false where risk module active
      - capture_risk_score >= 8

  care_health:
    fail_if:
      - high_need_support_coverage < minimum threshold
      - medication_continuity_supported is false where care module active

  mobility_access:
    fail_if:
      - accessible_route_coverage < 1.0 for essential spaces
      - emergency_access_supported is false

  legal_land_finance:
    fail_if:
      - land_security_status == "fail"
      - reserve_modeling_supported is false
      - debt_risk_score >= 8

  risk_resilience:
    fail_if:
      - dependency_graph_supported is false
      - scenario_coverage_count < minimum
      - recovery_playbook_count == 0
```

### Output shape

```json
{
  "kind": "CapabilityGateReport",
  "status": "pass|warn|fail",
  "domain_statuses": {
    "labor_time": {"status": "warn", "messages": [...]}
  },
  "failures": [],
  "warnings": [],
  "unknowns": []
}
```

### Principle

Unknowns should usually warn, not fail, unless the unknown is safety-critical.

---

## 14. Capability Effect Application Rules

Implement a simple deterministic reducer.

### Numeric deltas

If key ends with `_delta`, add the value to the base key without `_delta`.

Example:

```yaml
capture_risk_delta: -2
```

updates:

```yaml
capture_risk_score
```

or:

```yaml
capture_risk
```

Prefer explicit mapping for v0 to avoid magic.

### Booleans

If `true`, set true.

If `false`, only set false when the effect explicitly intends to remove a capability. To avoid accidental degradation, treat false values as declarations unless key is in `capability_negative_flags`.

Recommended: for v0, use booleans mostly as positive support flags.

### Coverage ratios

Clamp to `[0.0, 1.0]`.

```python
def clamp_ratio(value): return max(0.0, min(1.0, value))
```

### Risk scores

Clamp to `[0, 10]`, where higher is worse.

```python
def clamp_score(value): return max(0, min(10, value))
```

### Ledger

Every applied effect should produce a ledger row:

```json
{
  "pattern_id": "life_burden_ledger",
  "domain": "labor_time",
  "field": "hidden_labor_risk_score",
  "operation": "delta",
  "value": -2,
  "before": 5,
  "after": 3,
  "source": "selected_pattern"
}
```

---

## 15. Add Capability Effects to Initial Patterns

Do not update all patterns at once.

Start with these four:

```text
patterns/life_burden_ledger.yaml
patterns/commons_stewardship_protocol.yaml
patterns/community_care_commons.yaml
patterns/graceful_degradation_engine.yaml
```

### 15.1 `life_burden_ledger.yaml`

Add:

```yaml
capability_effects:
  labor_time:
    labor_time_ledger_supported: true
    hidden_labor_tracking_supported: true
    protected_time_tracking_supported: true
    wage_dependency_calculator_supported: true
    hidden_labor_risk_delta: -2
    burnout_risk_delta: -1
    governance_burden_visibility_supported: true
```

### 15.2 `commons_stewardship_protocol.yaml`

Add:

```yaml
capability_effects:
  governance_anticapture:
    due_process_defined: true
    emergency_power_sunset_defined: true
    role_registry_supported: true
    asset_lock_monitoring_supported: true
    conflict_ladder_supported: true
    capture_risk_delta: -2
    role_backup_coverage_delta: 0.10
```

### 15.3 `community_care_commons.yaml`

Add:

```yaml
capability_effects:
  care_health:
    care_room_supported: true
    medication_continuity_supported: true
    care_meal_protocol_supported: true
    high_need_support_coverage_delta: 0.20
    illness_wave_protocol_supported: true
  labor_time:
    care_labor_visibility_supported: true
    care_burnout_risk_delta: -1
```

### 15.4 `graceful_degradation_engine.yaml`

Add:

```yaml
capability_effects:
  risk_resilience:
    hazard_register_supported: true
    dependency_graph_supported: true
    service_level_matrix_supported: true
    scenario_coverage_delta: 10
    recovery_playbook_count_delta: 5
    graceful_degradation_supported: true
  governance_anticapture:
    emergency_power_sunset_defined: true
  labor_time:
    emergency_labor_tracking_supported: true
```

Keep all values provisional.

---

## 16. Reports and Runtime Bundle

### Add to simulation reports

Include:

```json
"capability_state": {...}
```

### Add to runtime bundle

If there is an export-runtime path, add:

```json
"capabilities": {
  "state": {...},
  "domain_statuses": {...},
  "ledger": [...],
  "warnings": [...],
  "failures": [...]
}
```

### Viewer minimum

Do not build a full viewer UI yet.

Just make the data available so the web viewer can later display:

```text
Capability floor status
Domain statuses
Top warnings
Top failures
Capability ledger
```

---

## 17. CLI Additions

Optional but useful:

```text
py -3.10 -m ciac capability-report examples/generated/micro_commons_plan.json --output examples/generated/micro_commons_capabilities.json
```

If CLI scope is too much, skip this and rely on simulation output.

---

## 18. Tests

Add focused tests. Do not create giant integration tests first.

### New tests

```text
tests/test_capabilities.py
tests/test_capability_schema.py
tests/test_module_implementation_capabilities.py
tests/test_foundation_capability_gate.py
tests/test_simulation_capability_state.py
```

### Test cases

#### 18.1 Apply simple capability effects

Input:

```python
effects = {
    "labor_time": {
        "hidden_labor_tracking_supported": True,
        "hidden_labor_risk_delta": -2
    }
}
```

Assert:

```text
hidden_labor_tracking_supported == true
hidden_labor_risk_score decreases
ledger contains entry
```

#### 18.2 Non-resource module is allowed

A test module with:

```yaml
modeled_impacts:
  direct_resource_effects:
    water_liters_per_day: 0
    energy_kwh_per_day: 0
    food_servings_per_day: 0
  capability_effects:
    governance_anticapture:
      due_process_defined: true
```

Should not be blocked for missing resource effects.

#### 18.3 Resource degradation still blocked

A module with:

```yaml
direct_resource_effects:
  water_liters_per_day: -10
```

Should still be blocked.

#### 18.4 Simulation emits capability state

Compile and simulate a plan with `life_burden_ledger`.

Assert simulation output includes:

```text
capability_state
capability_state.domains.labor_time
capability_state.ledger
```

#### 18.5 Capability gate can fail

Create state with:

```yaml
governance_anticapture:
  due_process_defined: false
```

Assert gate returns `fail` or `warn` based on active module profile.

#### 18.6 Backward compatibility

Existing tests should pass without modifying old patterns.

Run:

```text
py -3.10 -m unittest discover -s tests
py -3.10 -m ciac validate patterns
```

---

## 19. Backward Compatibility Requirements

This sprint must not break:

```text
compile
simulate
export-runtime
optimize-search
apply-search-candidate
module-compatibility
scalability-gate
implement-module
viewer-server
existing tests
existing patterns with no capability_effects
existing technology modules with only resource effects
```

The capability layer is additive.

---

## 20. Implementation Order

### Phase 1: Schema and parser

1. Update `schemas/civic_pattern.schema.json`.
2. Add `schemas/capability_state.schema.json`.
3. Add `ciac/capabilities.py`.
4. Add unit tests for capability effect application.

### Phase 2: Compiler integration

1. Update compile path to collect `capability_effects_by_pattern`.
2. Ensure compiled plan includes empty capability map if none exist.
3. Add compiler test.

### Phase 3: Simulation integration

1. Initialize capability state in simulation.
2. Apply selected pattern capability effects.
3. Add capability state to simulation output.
4. Add simulation test.

### Phase 4: Module implementation integration

1. Allow modules with capability effects but no resource effects.
2. Apply module capability effects into implemented plan.
3. Include `applied_capability_effects` in report.
4. Add tests.

### Phase 5: Capability gate

1. Implement `CapabilityGateReport`.
2. Connect it to simulation output or foundation gate output.
3. Add tests for pass/warn/fail.

### Phase 6: Pattern updates

1. Add minimal `capability_effects` to four seed civic modules.
2. Validate patterns.
3. Keep all effects provisional.

### Phase 7: Runtime bundle

1. Export capability state in runtime bundle.
2. Add cohesion test if artifact-cohesion currently validates runtime shape.

---

## 21. Acceptance Criteria

A coding agent is done when all are true:

```text
1. Existing resource simulation still passes existing tests.
2. `capability_effects` validates as optional CivicPattern data.
3. Simulation output includes a `capability_state`.
4. A non-resource module can be implemented without declaring water/food/energy effects.
5. Resource-negative effects are still blocked.
6. Capability effects produce a ledger.
7. Capability gate report can return pass/warn/fail.
8. At least four mature civic modules declare minimal provisional capability effects.
9. Runtime bundle exports capability state.
10. The test suite passes.
```

---

## 22. Suggested Commit Plan

```text
commit 1:
  Add capability schema and ciac/capabilities.py

commit 2:
  Wire compiler and simulation to emit capability_state

commit 3:
  Update module_implementation to allow capability-only modules

commit 4:
  Add capability gate report

commit 5:
  Add initial capability_effects to four patterns

commit 6:
  Export capabilities in runtime bundle and add tests

commit 7:
  Update README or docs with capability layer explanation
```

---

## 23. Documentation Update

Add a new doc:

```text
docs/capability_state_layer.md
```

Suggested content:

```text
- Why the capability layer exists
- Relationship to resource simulation
- Supported domains
- How capability_effects work
- How gates work
- What capability scores do not prove
- How to add capability effects to a pattern
```

Add a short README note after Resource Semantics:

```markdown
## Capability Semantics

Resource simulation tracks water, food, energy, storage, and flows. Capability simulation tracks non-resource civic conditions such as governance, labor, care, access, legal-finance resilience, skill coverage, social/coercion risk, and graceful degradation. Capability outputs are provisional and do not satisfy professional review, legal review, resident consent, or real-world validation.
```

---

## 24. Important Safety Language

Include this in capability reports:

```text
Capability scores are provisional modeling aids. They do not prove real-world dignity, safety, legal validity, health outcomes, consent, accessibility compliance, resident trust, or anti-capture success. They expose assumptions and blockers for review.
```

---

## 25. Future Work After This Sprint

Do not implement these until v0 capability state is stable:

```text
- Scenario-specific capability shocks
- Full village-block 80-person reference profile
- Capability optimizer objectives
- Viewer capability dashboard
- Dependency graph execution model
- High-need resident aggregate support modeling
- Emergency governance sunset state machine
- Social/cultural anti-clique simulation
- Legal/finance reserve shock simulator
- Unreal handoff metadata for capabilities
```

---

## 26. One-Sentence Agent Goal

Implement a backward-compatible capability state layer so CIaC can simulate and gate non-resource civic modules, proving that dignity, labor, governance, care, access, finance, education, social trust, and resilience can affect the civic floor without pretending to be water, food, or energy.
