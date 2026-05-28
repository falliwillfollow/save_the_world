# CIaC Sprint 56 Execution Plan: Life Manifest and Abundance Mode

**Plan ID:** `sprint_56_life_manifest_abundance_mode_v0_1`  
**Target repo:** `falliwillfollow/save_the_world`  
**Audience:** coding agent / implementation agent  
**Status:** actionable execution plan  
**Primary objective:** Make CIaC bilingual: machine-consumable underneath, human-narrative visible on top.  
**North star:** CIaC makes infrastructure legible enough for automation, and humane enough to return life to people.

---

## 0. One-Sentence Goal

Build a **Life Manifest** and **Automation Manifest** layer that translates CIaC’s machine-readable civic floor into a human-visible story of time returned, anxiety reduced, and automation serving the resident instead of absorbing the resident.

---

## 1. Product Thesis

CIaC is becoming a machine-readable civic infrastructure model. It already has patterns, capabilities, scenarios, scaling, runtime bundles, and a 3D world. The missing bridge is a narrative compiler.

The system should not only answer:

```text
Does the infrastructure pass?
```

It should also answer:

```text
What does passing give back to a person?
What burden disappears?
What anxiety is reduced?
What dream becomes possible?
What can automation safely handle?
What must remain human-sovereign?
```

---

## 2. Core Framing

CIaC is an **infrastructure compiler for post-labor abundance**.

It translates:

```text
human needs
  housing, food, water, sanitation, care, mobility, privacy, belonging

into civic systems
  modules, thresholds, gates, service radii, reserves, labor ledgers

into machine-readable instructions
  manifests, schedules, policies, scenarios, capability states

into automation targets
  AI planning, robotics tasks, maintenance queues, fabrication workflows

with one purpose
  return time and dignity to the human occupant
```

---

## 3. New Public-Facing Concept: Life Returned

The public metric should be emotionally legible:

```text
Life Returned = hours per week returned to self-directed life
```

This is paired with internal metrics:

```text
Life Burden Reduction
Capability Gate Status
Promotion Blockers
```

The system should make the argument visible:

```text
Default life:
  wage labor
  commute
  errands
  solo domestic survival
  emergency fragility
  little creative time

Civic floor life:
  bounded commons contribution
  shared food / care / maintenance
  lower required wage labor
  visible support systems
  more creative / study / rest / discovery time
```

---

## 4. Non-Goals

Do not do these in this sprint:

```text
Do not redesign the simulator.
Do not build a full AI agent or robotics control system.
Do not claim real-world abundance has been proven.
Do not make automation sovereign over residents.
Do not allow automation tasks to decide consent, expulsion, diagnosis, legal validity, punishment, or human worth.
Do not require real personal user data.
Do not make the Life Manifest dependent on a perfect conventional baseline.
Do not remove Life / Systems / Stress modes.
Do not over-polish visuals before the narrative contract works.
```

---

## 5. Files to Add

```text
schemas/
  life_manifest.schema.json
  automation_manifest.schema.json

ciac/
  life_manifest.py
  automation_manifest.py

examples/life_manifests/
  life_manifest_80_v0.json
  automation_manifest_80_v0.json

viewer/world3d/src/modes/
  AbundanceMode.jsx

viewer/world3d/src/components/
  LifeReturnedCard.jsx
  TimeBudgetWheel.jsx
  AutomationSubstratePanel.jsx
  HumanSovereigntyPanel.jsx
  ResidentStoryCard.jsx
  BaselineComparisonPanel.jsx

docs/
  life_manifest_abundance_mode.md

tests/
  test_life_manifest.py
  test_automation_manifest.py
  test_abundance_mode_contract.py
```

Adapt paths if the repo has different viewer conventions.

---

## 6. Files Likely to Modify

```text
ciac/world_manifest.py
ciac/runtime_bundle.py          # or equivalent runtime export path
ciac/simulation.py              # only if needed to expose labor/free-time values
viewer/world3d/src/App.jsx
viewer/world3d/src/components/ModeSwitcher.jsx
viewer/world3d/src/components/InfoCard.jsx
viewer/world3d/src/world/WorldManifestLoader.js
README.md
```

---

## 7. New Artifact: Life Manifest

### 7.1 Purpose

The Life Manifest is the human-narrative twin of the runtime bundle and world manifest.

It answers:

```text
Who lives here?
What burden did they have before?
What changes under the civic floor?
What time is returned?
What anxiety is reduced?
What support systems become visible?
What remains provisional?
```

### 7.2 Required Top-Level Fields

```yaml
LifeManifest:
  kind: LifeManifest
  version: v0
  manifest_id: string

  source:
    runtime_bundle_path: string | null
    world_manifest_path: string | null
    capability_policy_id: string | null
    generated_at: string | null
    provisional: boolean

  population:
    residents: integer
    households: integer | null

  scale:
    scale_class: micro_commons | village_block | multi_block_district | town_city_layer | regional_membrane
    active_layers: list[string]
    implied_village_blocks: number

  public_thesis:
    tagline: string
    short: string
    long: string

  metrics:
    life_returned_hours_per_week: number
    required_wage_hours_reduction_percent: number
    free_time_increase_hours_per_week: number
    passion_time_increase_hours_per_week: number
    commons_labor_hours_per_resident_per_week: number
    hidden_labor_status: pass | warn | fail | unknown
    capability_gate_status: pass | warn | fail | promotion_blocked | unknown

  resident_archetypes:
    - id: string
      label: string
      archetype: string
      baseline_life: BaselineLife
      civic_floor_life: CivicFloorLife
      life_returned: LifeReturned
      narrative_beats: list[NarrativeBeat]
      warnings: list[string]

  baseline_model:
    description: string
    assumptions: list[string]
    conventional_life_burdens: list[string]

  civic_floor_model:
    description: string
    support_systems: list[string]
    automation_assists: list[string]
    human_sovereignty_boundaries: list[string]

  life_returned:
    summary: string
    hours_per_week: number
    meaningful_uses:
      - art
      - study
      - care
      - rest
      - nature
      - invention
      - friendship

  scenes:
    - id: normal_day
      title: Normal Day
      mode: life
      beats: list[NarrativeBeat]

  scenario_story_beats:
    - id: outage
      scenario_id: string
      title: 72-Hour Outage
      beats: list[NarrativeBeat]

  warnings:
    - id: string
      message: string
      severity: info | warn | fail | block

  promotion_blockers:
    - id: string
      domain: string
      message: string

  provisionality:
    statement: string
    external_reviews_required: list[string]
```

---

## 8. New Artifact: Automation Manifest

### 8.1 Purpose

The Automation Manifest is the machine-facing twin.

It answers:

```text
What can AI, software automation, or robotics help with?
What triggers the task?
What data does it need?
What output does it produce?
What human review is required?
What must automation never decide?
```

### 8.2 Required Top-Level Fields

```yaml
AutomationManifest:
  kind: AutomationManifest
  version: v0
  manifest_id: string

  source:
    runtime_bundle_path: string | null
    world_manifest_path: string | null
    generated_at: string | null
    provisional: boolean

  automation_thesis:
    tagline: "Machines handle the repeating burden. Humans keep the non-repeatable life."
    description: string

  allowed_automation_domains:
    - scheduling
    - monitoring
    - inventory
    - route_planning
    - routine_inspection
    - task_reminders
    - scenario_testing
    - hidden_burden_detection
    - logistics_support
    - maintenance_queueing

  blocked_automation_domains:
    - resident_consent
    - expulsion_or_loss_of_access
    - clinical_diagnosis
    - legal_judgment
    - punishment
    - emotional_coercion
    - private_life_inference
    - governance_legitimacy
    - determining_human_worth

  tasks:
    - id: string
      domain: string
      actor: AI_scheduler | human | robot_assisted | human_reviewed_AI
      trigger: weekly | scenario | threshold | manual
      input_data: list[string]
      output: string
      human_review_required: boolean
      review_gate: string | null
      privacy_level: public | member_visible | role_limited | private
      failure_mode: string
      visible_in_world: boolean

  human_sovereignty_boundaries:
    - id: no_automated_expulsion
      rule: Automation may flag a governance issue, but may not remove housing/access rights.

  review_gates:
    - id: clinical_boundary_review
      domain: care_health
      required_for:
        - medication_continuity
        - care_plan_suggestions

  warnings:
    - id: string
      message: string
      severity: info | warn | fail | block
```

---

## 9. Python Exporter: `ciac/life_manifest.py`

### 9.1 Responsibilities

```text
Load runtime bundle, world manifest, and capability state.
Generate resident archetype narratives.
Generate baseline vs civic-floor time budgets.
Compute Life Returned.
Extract capability warnings and promotion blockers.
Generate normal-day and stress-scenario story beats.
Write `LifeManifest` JSON.
Validate against schema.
```

### 9.2 Suggested API

```python
from pathlib import Path
from typing import Any

def build_life_manifest(
    runtime_bundle: dict[str, Any],
    world_manifest: dict[str, Any] | None = None,
    *,
    population: int | None = None,
    baseline_profile: str = "default_renter_creator",
) -> dict[str, Any]:
    ...

def default_resident_archetypes(population: int) -> list[dict[str, Any]]:
    ...

def build_baseline_life(archetype: str, baseline_profile: str) -> dict[str, Any]:
    ...

def build_civic_floor_life(
    archetype: str,
    runtime_bundle: dict[str, Any],
    world_manifest: dict[str, Any] | None,
) -> dict[str, Any]:
    ...

def compute_life_returned(
    baseline_life: dict[str, Any],
    civic_floor_life: dict[str, Any],
) -> dict[str, Any]:
    ...

def build_story_beats(
    resident_archetypes: list[dict[str, Any]],
    runtime_bundle: dict[str, Any],
) -> list[dict[str, Any]]:
    ...

def write_life_manifest(manifest: dict[str, Any], path: str | Path) -> None:
    ...
```

### 9.3 CLI

Add one of these, depending on repo CLI conventions:

```bash
py -3.10 -m ciac export-life-manifest \
  --runtime examples/generated/webapp_runtime_bundle.json \
  --world examples/world_manifests/civic_floor_80_v0.world.json \
  --output examples/life_manifests/life_manifest_80_v0.json \
  --population 80
```

---

## 10. Python Exporter: `ciac/automation_manifest.py`

### 10.1 Responsibilities

```text
Load runtime bundle, world manifest, capability state, and optionally capability policy.
Generate automation task registry.
Classify tasks by allowed/blocked domains.
Add human review requirements.
Add privacy levels.
Add review gates.
Write `AutomationManifest` JSON.
Validate against schema.
```

### 10.2 Suggested API

```python
def build_automation_manifest(
    runtime_bundle: dict[str, Any],
    world_manifest: dict[str, Any] | None = None,
    capability_policy: dict[str, Any] | None = None,
) -> dict[str, Any]:
    ...

def default_automation_tasks() -> list[dict[str, Any]]:
    ...

def human_sovereignty_boundaries() -> list[dict[str, Any]]:
    ...

def validate_no_blocked_automation_tasks(manifest: dict[str, Any]) -> list[str]:
    ...

def write_automation_manifest(manifest: dict[str, Any], path: str | Path) -> None:
    ...
```

---

## 11. Resident Archetypes

Use archetypes, not real people.

Initial archetypes:

```yaml
resident_archetypes:
  - id: artist_service_worker
    label: Artist / Service Worker
    purpose: Shows time returned to creative life.

  - id: elder_independent
    label: Independent Elder
    purpose: Shows care, mobility, medication, and social support.

  - id: burned_out_knowledge_worker
    label: Burned-Out Knowledge Worker
    purpose: Shows exit from high-anxiety wage identity.

  - id: student_apprentice
    label: Student / Apprentice
    purpose: Shows learning without debt-heavy pipeline.

  - id: caregiver_parent
    label: Caregiver / Parent
    purpose: Shows hidden care labor made visible and supported.

  - id: maintenance_steward
    label: Maintenance Steward
    purpose: Shows necessary work remaining dignified, bounded, and trained.
```

---

## 12. Baseline Time Budget Defaults

These are provisional demo defaults and must be labeled as assumptions.

```yaml
baseline_profiles:
  default_renter_creator:
    wage_hours_per_week: 42
    commute_hours_per_week: 6
    errands_admin_hours_per_week: 5
    domestic_survival_hours_per_week: 12
    care_labor_hours_per_week: 2
    recovery_hours_per_week: 7
    passion_time_hours_per_week: 4
    anxiety_sources:
      - rent
      - transportation
      - food_cost
      - health_fragility
      - emergency_fragility
      - isolation

  civic_floor_default:
    wage_hours_per_week: 24
    commons_labor_hours_per_week: 6
    commute_hours_per_week: 2
    errands_admin_hours_per_week: 2
    domestic_survival_hours_per_week: 5
    care_labor_hours_per_week: 1
    recovery_hours_per_week: 9
    passion_time_hours_per_week: 18
```

The exporter should allow overrides later. For v0, hardcoded defaults are acceptable if clearly marked provisional.

---

## 13. Life Returned Calculation

```python
life_returned_hours = (
    civic_floor_life["passion_time_hours_per_week"]
    + civic_floor_life.get("recovery_hours_per_week", 0)
) - (
    baseline_life["passion_time_hours_per_week"]
    + baseline_life.get("recovery_hours_per_week", 0)
)
```

Also compute:

```yaml
compulsory_burden_baseline:
  wage_hours + commute_hours + errands_admin + domestic_survival + required_care

compulsory_burden_civic:
  wage_hours + commons_labor + commute_hours + errands_admin + domestic_survival + required_care

life_burden_reduction_hours:
  baseline_compulsory - civic_compulsory

required_wage_hours_reduction_percent:
  (baseline_wage - civic_wage) / baseline_wage * 100
```

Do not overstate precision. Output should include:

```yaml
confidence: provisional
assumptions: [...]
```

---

## 14. Automation Task Registry

Initial tasks for `AutomationManifest`:

```yaml
automation_tasks:
  - id: water_quality_check_schedule
    domain: water
    actor: AI_scheduler
    trigger: weekly
    human_review_required: true
    review_gate: public_health
    privacy_level: member_visible
    output: water_testing_task

  - id: food_inventory_balance
    domain: food
    actor: AI_scheduler
    trigger: daily
    human_review_required: true
    review_gate: food_safety
    privacy_level: role_limited
    output: food_inventory_warning

  - id: care_meal_route
    domain: care_health
    actor: human_reviewed_AI
    trigger: care_meal_request
    human_review_required: true
    review_gate: privacy
    privacy_level: role_limited
    output: delivery_schedule

  - id: maintenance_queue_prioritization
    domain: maintenance_repair
    actor: AI_scheduler
    trigger: work_order_created
    human_review_required: true
    review_gate: safety
    privacy_level: member_visible
    output: prioritized_work_queue

  - id: hidden_labor_detection
    domain: labor_time
    actor: human_reviewed_AI
    trigger: weekly
    human_review_required: true
    review_gate: labor_fairness
    privacy_level: anonymized_or_role_limited
    output: labor_burden_warning

  - id: scenario_stress_test
    domain: risk_resilience
    actor: AI_simulation_runner
    trigger: manual_or_scheduled
    human_review_required: true
    review_gate: resilience_review
    privacy_level: member_visible
    output: scenario_report

  - id: resident_story_projection
    domain: social_cultural
    actor: AI_narrative_compiler
    trigger: manifest_generation
    human_review_required: true
    review_gate: public_demo_review
    privacy_level: public_archetype_only
    output: archetype_story
```

Blocked tasks:

```yaml
blocked_automation_tasks:
  - decide_expulsion_or_loss_of_access
  - diagnose_resident_health
  - determine_legal_validity
  - determine_human_worth_or_contribution_value
  - override_resident_consent
  - infer_private_life_or_social_status_without_consent
  - punish_or_rank_residents
  - make_final_governance_decision
```

---

## 15. Viewer: Add Abundance Mode

### 15.1 Mode Switcher

Add a fourth mode:

```text
Life | Systems | Stress | Abundance
```

### 15.2 Abundance Mode UI

Components:

```text
LifeReturnedCard
TimeBudgetWheel
AutomationSubstratePanel
HumanSovereigntyPanel
ResidentStoryCard
BaselineComparisonPanel
```

### 15.3 Display Requirements

Abundance Mode should show:

```text
selected resident archetype
baseline time budget
civic floor time budget
Life Returned hours/week
compulsory burden reduction
automation-assist tasks
blocked automation domains
promotion blockers / provisionality
```

### 15.4 Visual Behavior

In the 3D scene:

```text
highlight automated/automatable infrastructure tasks
show routine burden flows fading into automation substrate
show human spaces brightened: studio, garden, quiet room, social commons, learning room
show lock icons for human-sovereign domains
```

Do not imply AI controls residents.

---

## 16. World Manifest Integration

Extend `world_manifest.json` or attach by reference:

```json
{
  "linked_manifests": {
    "life_manifest": "examples/life_manifests/life_manifest_80_v0.json",
    "automation_manifest": "examples/life_manifests/automation_manifest_80_v0.json"
  }
}
```

Or include as runtime bundle pointers.

The viewer should be able to load:

```text
world_manifest
life_manifest
automation_manifest
```

independently.

---

## 17. Evidence Cards

Object click cards should gain a narrative/automation section when the manifests are loaded.

Example:

```yaml
Common House:
  human_narrative:
    - reduces isolated meal burden
    - creates optional third place
    - supports care meals during illness
  automation_assist:
    - schedule meal shifts
    - inventory alerts
    - care meal routing
  human_sovereignty:
    - participation is optional
    - no automated social scoring
```

Example:

```yaml
Care Room:
  human_narrative:
    - protects privacy during illness or recovery
    - supports medication continuity
  automation_assist:
    - check refrigeration status
    - route care meals
    - remind steward of follow-up tasks
  blocked_automation:
    - diagnosis
    - care eligibility denial
```

---

## 18. Tests

### 18.1 `tests/test_life_manifest.py`

```yaml
tests:
  - life_manifest_schema_validates
  - generated_life_manifest_has_required_top_level_fields
  - resident_archetypes_exist
  - each_archetype_has_baseline_and_civic_life
  - life_returned_is_computed
  - manifest_contains_provisionality_statement
  - manifest_contains_promotion_blockers_field
```

### 18.2 `tests/test_automation_manifest.py`

```yaml
tests:
  - automation_manifest_schema_validates
  - automation_manifest_has_allowed_and_blocked_domains
  - every_task_has_actor_trigger_output_review_gate_privacy_level
  - human_review_required_for_sensitive_tasks
  - blocked_domains_include_expulsion_diagnosis_legal_judgment_consent_human_worth
  - no_task_id_matches_blocked_domain
```

### 18.3 `tests/test_abundance_mode_contract.py`

```yaml
tests:
  - viewer_can_load_life_manifest_fixture
  - viewer_can_load_automation_manifest_fixture
  - abundance_mode_available
  - life_returned_card_receives_metric
  - human_sovereignty_panel_receives_blocked_domains
  - automation_panel_receives_tasks
```

Adapt viewer tests to existing test setup. If frontend tests are not configured, use JSON/schema tests plus documented manual validation.

---

## 19. Documentation

Add `docs/life_manifest_abundance_mode.md`.

Sections:

```text
Purpose
Why Life Manifest exists
Why Automation Manifest exists
Relationship to runtime bundle and world manifest
Abundance Mode UI
Life Returned metric
Baseline assumptions
Human sovereignty boundaries
What automation may do
What automation may not do
What this does not prove
How to generate manifests
How to run viewer
Future n8n workflows
Future robotics interface
```

README note:

```markdown
## Life Manifest and Abundance Mode

CIaC now includes an experimental Life Manifest and Automation Manifest layer. These translate machine-readable civic infrastructure into human-visible narratives of life burden reduction, time returned, and automation support. Abundance Mode in the 3D viewer shows what recurring infrastructure work can be made legible to automation while preserving human-sovereign domains such as consent, governance legitimacy, care meaning, privacy, and creative purpose.
```

---

## 20. n8n Future Workflow Specs

Add later, not necessarily in this sprint:

```text
n8n/workflow_specs/life_manifest_generation_pipeline.md
n8n/workflow_specs/abundance_demo_snapshot_pipeline.md
n8n/workflow_specs/automation_task_review_pipeline.md
```

Concept:

```text
runtime bundle generated
  -> generate life manifest
  -> generate automation manifest
  -> validate human sovereignty boundaries
  -> render abundance mode snapshot
  -> publish demo card
  -> create review issues for missing gates
```

---

## 21. Acceptance Criteria

```yaml
acceptance_criteria:
  - life_manifest.schema.json exists
  - automation_manifest.schema.json exists
  - ciac/life_manifest.py generates valid example
  - ciac/automation_manifest.py generates valid example
  - sample life and automation manifests are committed
  - Life Returned metric exists and is computed
  - automation tasks are explicitly review-gated
  - blocked automation domains are enforced in tests
  - Abundance Mode appears in viewer
  - Abundance Mode can display time budget and automation/human sovereignty panels
  - provisionality language appears in docs and/or viewer
  - existing tests pass
```

---

## 22. Suggested Commit Plan

```text
commit 1:
  add life_manifest and automation_manifest schemas

commit 2:
  add life_manifest.py and tests

commit 3:
  add automation_manifest.py and tests

commit 4:
  add sample manifests for population 80

commit 5:
  add Abundance Mode viewer components

commit 6:
  connect manifests to viewer/world manifest loading

commit 7:
  add docs and README note

commit 8:
  polish tests and provisionality copy
```

---

## 23. Final Safety Language

Include this in manifests and viewer:

```text
This is a provisional civic simulation. Life Returned, automation tasks, and capability states are modeling aids only. They do not certify real-world safety, legality, accessibility, clinical validity, affordability, labor compliance, engineering validity, resident consent, public-health compliance, or buildability.
```

---

## 24. Final Product Sentence

The sprint is successful if the product can visibly say:

```text
Machines handle the repeating burden.
Humans keep the non-repeatable life.
```
