# CIaC Capability Thresholds Research Pack, Part 3: Coding-Agent Execution Plan

**Research ID:** `ciac_capability_thresholds_research_pack_part_3_v0_1`  
**Parent artifacts:**  
- `ciac_capability_thresholds_research_pack_part_1_v0_1.md`  
- `ciac_capability_thresholds_research_pack_part_2_v0_1.md`  

**Purpose:** Convert the capability-threshold research and policy translation into an executable implementation plan for a coding agent.  
**Status:** Implementation plan, not final legal, medical, accessibility, labor, finance, emergency-management, engineering, or public-health approval.  
**Primary CIaC use:** add a policy-driven capability gate layer to the repo without breaking the existing `CapabilityState`, simulation, runtime bundle, world viewer, or tests.

---

## 0. One-Sentence Agent Goal

Implement a policy-driven capability gate system so CIaC can evaluate care, governance, mobility, legal/finance, risk/resilience, and labor/time capabilities using machine-readable pass/warn/fail/promotion-block rules sourced from the new research pack.

---

## 1. Problem Statement

CIaC now has a working `CapabilityState` layer, but capability logic is still early and partially hardcoded. The research pack defines richer thresholds for:

```text
Care Health
Governance / Anti-Capture
Mobility / Access
Legal / Land / Finance
Risk / Resilience
Labor / Time
```

The next repo step is to turn these into a versioned policy file and a gate engine.

The system must distinguish:

```yaml
simulation_only:
  meaning: Model can visualize or reason about the capability.

review_blocked:
  meaning: Model can simulate it, but real-world promotion is blocked until external review.

promotion_ready:
  meaning: Internal gates pass and no unresolved review blockers exist for the claim being made.
```

---

## 2. Non-Goals

Do not implement these in this sprint:

```text
Do not replace the current CapabilityState.
Do not remove existing capability gates until policy gates are stable.
Do not claim legal, clinical, accessibility, emergency, labor, finance, or engineering validity.
Do not build a full expert system.
Do not make the viewer hide provisionality.
Do not use capability scores as proof of real-world readiness.
Do not require all modules to perfectly satisfy all policy fields immediately.
Do not block simulation mode because professional review is missing.
```

The policy engine should support simulation while blocking promotion claims.

---

## 3. Files to Add

```text
schemas/capability_policy.schema.json

capability_policies/
  ciac_capability_policy_v0.yaml

ciac/
  capability_policy.py

scenarios/capability/
  care_health_illness_wave.yaml
  governance_emergency_power_drift.yaml
  mobility_access_route_blockage.yaml
  legal_finance_reserve_shock.yaml
  risk_resilience_compound_failure.yaml
  labor_time_hidden_burden.yaml

tests/
  test_capability_policy.py
  test_capability_gate_policy.py
  test_capability_scenarios.py

docs/
  capability_policy_v0.md
```

---

## 4. Files Likely to Modify

```text
ciac/capabilities.py
ciac/capability_gate.py              # if exists; otherwise create
ciac/simulation.py
ciac/world_manifest.py
ciac/runtime_bundle.py               # or equivalent runtime export path
viewer/world3d/src/...               # warning/evidence panels
README.md
```

Do not assume exact file names for runtime export or viewer panels. Inspect the repo and adapt to existing naming conventions.

---

## 5. Capability Policy Schema

### 5.1 Add `schemas/capability_policy.schema.json`

The schema should be permissive enough for iteration, but strict on the key contract.

Required top-level fields:

```json
{
  "policy_id": "string",
  "version": "string",
  "status": "string",
  "source_registry": [],
  "domains": {},
  "promotion_blockers": [],
  "scenario_requirements": {},
  "ui_warnings": {}
}
```

Suggested JSON Schema:

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "CIaC Capability Policy",
  "type": "object",
  "required": [
    "policy_id",
    "version",
    "status",
    "source_registry",
    "domains",
    "promotion_blockers",
    "scenario_requirements",
    "ui_warnings"
  ],
  "properties": {
    "policy_id": { "type": "string" },
    "version": { "type": "string" },
    "status": {
      "type": "string",
      "enum": ["provisional", "reviewed", "deprecated"]
    },
    "source_registry": {
      "type": "array",
      "items": { "$ref": "#/$defs/source" }
    },
    "domains": {
      "type": "object",
      "additionalProperties": { "$ref": "#/$defs/domain_policy" }
    },
    "promotion_blockers": {
      "type": "array",
      "items": { "$ref": "#/$defs/promotion_blocker" }
    },
    "scenario_requirements": {
      "type": "object",
      "additionalProperties": {
        "type": "object",
        "properties": {
          "required": {
            "type": "array",
            "items": { "type": "string" }
          }
        }
      }
    },
    "ui_warnings": {
      "type": "object",
      "additionalProperties": { "$ref": "#/$defs/ui_warning" }
    }
  },
  "$defs": {
    "source": {
      "type": "object",
      "required": ["id", "title", "url", "supports"],
      "properties": {
        "id": { "type": "string" },
        "title": { "type": "string" },
        "organization": { "type": "string" },
        "url": { "type": "string" },
        "evidence_quality": {
          "type": "string",
          "enum": ["high", "moderate", "low", "mixed"]
        },
        "supports": {
          "type": "array",
          "items": { "type": "string" }
        }
      }
    },
    "domain_policy": {
      "type": "object",
      "required": ["capability_fields", "gates"],
      "properties": {
        "capability_fields": {
          "type": "array",
          "items": { "type": "string" }
        },
        "required_structures": {
          "type": "array",
          "items": { "type": "string" }
        },
        "required_protocols": {
          "type": "array",
          "items": { "type": "string" }
        },
        "external_review_blockers": {
          "type": "array",
          "items": { "type": "string" }
        },
        "scenarios": {
          "type": "array",
          "items": { "type": "string" }
        },
        "ui_warnings": {
          "type": "array",
          "items": { "type": "string" }
        },
        "gates": {
          "type": "array",
          "items": { "$ref": "#/$defs/capability_gate" }
        }
      }
    },
    "capability_gate": {
      "type": "object",
      "required": [
        "gate_id",
        "capability_field",
        "pass_condition",
        "warn_condition",
        "fail_condition",
        "promotion_block_condition",
        "source_ids"
      ],
      "properties": {
        "gate_id": { "type": "string" },
        "capability_field": { "type": "string" },
        "pass_condition": { "type": ["object", "array", "string", "number", "boolean"] },
        "warn_condition": { "type": ["object", "array", "string", "number", "boolean"] },
        "fail_condition": { "type": ["object", "array", "string", "number", "boolean"] },
        "promotion_block_condition": { "type": ["object", "array", "string", "number", "boolean"] },
        "evidence_quality": {
          "type": "string",
          "enum": ["high", "moderate", "low", "mixed"]
        },
        "translation_confidence": {
          "type": "string",
          "enum": ["high", "moderate", "low"]
        },
        "regulatory_strength": {
          "type": "string",
          "enum": ["binding", "guideline", "professional_practice", "research_inferred", "heuristic"]
        },
        "source_ids": {
          "type": "array",
          "items": { "type": "string" }
        }
      }
    },
    "promotion_blocker": {
      "type": "object",
      "required": ["id", "domain", "severity"],
      "properties": {
        "id": { "type": "string" },
        "domain": { "type": "string" },
        "severity": {
          "type": "string",
          "enum": ["block", "warn"]
        },
        "description": { "type": "string" }
      }
    },
    "ui_warning": {
      "type": "object",
      "required": ["message"],
      "properties": {
        "message": { "type": "string" },
        "severity": {
          "type": "string",
          "enum": ["info", "warn", "fail", "block"]
        },
        "domain": { "type": "string" }
      }
    }
  }
}
```

---

## 6. Capability Policy YAML Scaffold

### 6.1 Add `capability_policies/ciac_capability_policy_v0.yaml`

Initial scaffold should include all six domains and enough gates to test the policy engine. It does not need every final nuance on day one.

```yaml
policy_id: ciac_capability_policy_v0
version: v0.1
status: provisional

source_registry:
  - id: CDC_DISABILITY_EMERGENCY_KIT
    title: Building an Emergency Kit for People with Disabilities
    organization: CDC
    url: https://www.cdc.gov/disability-emergency-preparedness/people-with-disabilities/build-a-kit.html
    evidence_quality: high
    supports:
      - medication_continuity
      - refrigerated_medication_backup
      - assistive_device_power
      - emergency_health_documents

  - id: CORNELL_PROCEDURAL_DUE_PROCESS
    title: Procedural Due Process
    organization: Cornell Legal Information Institute
    url: https://www.law.cornell.edu/wex/procedural_due_process
    evidence_quality: moderate
    supports:
      - notice
      - neutral_review
      - opportunity_to_respond

  - id: ACCESS_BOARD_ACCESSIBLE_ROUTES
    title: ADA Guide, Accessible Routes
    organization: U.S. Access Board
    url: https://www.access-board.gov/ada/guides/chapter-4-accessible-routes/
    evidence_quality: high
    supports:
      - accessible_route_requirements

  - id: HUD_CHAS_COST_BURDEN
    title: CHAS Background
    organization: HUD User
    url: https://www.huduser.gov/portal/datasets/cp/CHAS/bg_chas.html
    evidence_quality: high
    supports:
      - housing_cost_burden_30_percent
      - severe_cost_burden_50_percent

  - id: NIST_COMMUNITY_RESILIENCE_GUIDE
    title: Community Resilience Planning Guide
    organization: NIST
    url: https://www.nist.gov/community-resilience/planning-guide
    evidence_quality: high
    supports:
      - dependency_graph
      - recovery_goals
      - critical_functions

  - id: BLS_ATUS_2024
    title: American Time Use Survey, 2024 Results
    organization: Bureau of Labor Statistics
    url: https://www.bls.gov/news.release/atus.nr0.htm
    evidence_quality: high
    supports:
      - work_time
      - household_labor
      - care_labor
      - leisure_time

domains:
  care_health:
    capability_fields:
      - care_health.nonclinical_care_floor
      - care_health.high_need_support_coverage
      - care_health.medication_continuity_status
      - care_health.illness_wave_readiness
    required_structures:
      - care_room
      - first_aid_station
      - medication_refrigeration_point
      - external_healthcare_registry
    required_protocols:
      - nonclinical_support_scope
      - privacy_and_consent
      - medication_cold_chain
      - illness_wave_protocol
    external_review_blockers:
      - clinical_boundary_review
      - privacy_review
      - liability_review
    gates:
      - gate_id: care_nonclinical_floor
        capability_field: care_health.nonclinical_care_floor
        pass_condition:
          care_room: true
          first_aid_station: true
          external_care_path: true
          no_clinical_claims: true
        warn_condition:
          trained_backup_missing: true
        fail_condition:
          no_private_care_space: true
          claims_to_replace_professional_care: true
        promotion_block_condition:
          clinical_boundary_unreviewed_and_public_claim_made: true
        evidence_quality: moderate
        translation_confidence: moderate
        regulatory_strength: professional_practice
        source_ids:
          - CDC_DISABILITY_EMERGENCY_KIT

  governance_anticapture:
    capability_fields:
      - governance_anticapture.due_process_status
      - governance_anticapture.emergency_power_sunset
      - governance_anticapture.role_backup_coverage
      - governance_anticapture.records_privacy_status
    required_structures:
      - decision_log
      - policy_registry
      - role_registry
      - records_classification_policy
    required_protocols:
      - notice_and_response
      - impartial_review
      - emergency_power_sunset
      - role_concentration_audit
    external_review_blockers:
      - loss_of_access_or_expulsion_legal_review
      - privacy_review
    gates:
      - gate_id: due_process_minimum
        capability_field: governance_anticapture.due_process_status
        pass_condition:
          notice: true
          opportunity_to_respond: true
          impartial_review: true
          recordkeeping: true
          appeal_path: true
        warn_condition:
          appeal_path_missing: true
          recusal_rule_missing: true
        fail_condition:
          loss_of_access_without_notice_review_or_appeal: true
        promotion_block_condition:
          membership_or_occupancy_decision_without_legal_review: true
        evidence_quality: moderate
        translation_confidence: moderate
        regulatory_strength: research_inferred
        source_ids:
          - CORNELL_PROCEDURAL_DUE_PROCESS

  mobility_access:
    capability_fields:
      - mobility_access.accessible_route_coverage
      - mobility_access.essential_access_minutes_max
      - mobility_access.emergency_access_status
    required_structures:
      - accessible_route_map
      - distance_friction_calculator
      - emergency_route_map
    required_protocols:
      - accessibility_audit
      - route_inspection
      - route_clearance
    external_review_blockers:
      - accessibility_code_review
      - fire_EMS_access_review
    gates:
      - gate_id: accessible_route_coverage
        capability_field: mobility_access.accessible_route_coverage
        pass_condition:
          essential_accessible_route_coverage: 100_percent
        warn_condition:
          essential_accessible_route_coverage_between_95_and_99: true
        fail_condition:
          any_essential_space_lacks_accessible_route: true
        promotion_block_condition:
          public_demo_claims_accessibility_with_unresolved_route_failure: true
        evidence_quality: high
        translation_confidence: high
        regulatory_strength: binding
        source_ids:
          - ACCESS_BOARD_ACCESSIBLE_ROUTES

  legal_land_finance:
    capability_fields:
      - legal_land_finance.tenure_security_status
      - legal_land_finance.reserve_status
      - legal_land_finance.affordability_burden_status
      - legal_land_finance.external_review_blockers
    required_structures:
      - land_stewardship_model
      - written_resident_rights
      - operating_reserve
      - replacement_reserve
      - affordability_calculator
    required_protocols:
      - resident_rights_onboarding
      - reserve_drawdown_and_replenishment
      - external_review_blocker_tracking
    external_review_blockers:
      - entity_structure
      - land_control
      - occupancy_agreements
      - tax_status
      - insurance
      - zoning_permitting
    gates:
      - gate_id: affordability_burden
        capability_field: legal_land_finance.affordability_burden_status
        pass_condition:
          housing_plus_utilities_below_30_percent_income: true
          transport_included: true
          reserves_included: true
        warn_condition:
          housing_plus_utilities_30_to_50_percent_income: true
        fail_condition:
          housing_plus_utilities_above_50_percent_without_subsidy_or_hardship_plan: true
          affordability_depends_on_unpaid_hidden_labor: true
        promotion_block_condition:
          public_affordability_claim_without_cost_burden_and_reserve_model: true
        evidence_quality: high
        translation_confidence: moderate
        regulatory_strength: guideline
        source_ids:
          - HUD_CHAS_COST_BURDEN

  risk_resilience:
    capability_fields:
      - risk_resilience.hazard_register_coverage
      - risk_resilience.dependency_graph_completeness
      - risk_resilience.recovery_playbook_count
      - risk_resilience.graceful_degradation_status
    required_structures:
      - hazard_register
      - dependency_graph
      - recovery_playbook_library
      - service_level_matrix
    required_protocols:
      - annual_risk_review
      - scenario_run_schedule
      - after_action_review
      - reserve_replenishment
    external_review_blockers:
      - emergency_management_review
      - fire_EMS_review
      - public_health_review
    gates:
      - gate_id: dependency_graph
        capability_field: risk_resilience.dependency_graph_completeness
        pass_condition:
          includes:
            - resource_flows
            - labor_roles
            - external_suppliers
            - critical_infrastructure
            - governance_authority
            - high_need_support
            - reserves
            - transport_access_routes
        warn_condition:
          external_dependencies_unmapped: true
          labor_roles_omitted: true
        fail_condition:
          no_dependency_graph: true
          critical_functions_untraceable: true
        promotion_block_condition:
          public_system_claim_without_dependency_graph: true
        evidence_quality: high
        translation_confidence: high
        regulatory_strength: guideline
        source_ids:
          - NIST_COMMUNITY_RESILIENCE_GUIDE

  labor_time:
    capability_fields:
      - labor_time.commons_labor_hours_per_resident_per_week
      - labor_time.hidden_labor_status
      - labor_time.free_time_increase_hours_per_week
      - labor_time.trained_role_requirement_status
    required_structures:
      - labor_ledger
      - role_scheduler
      - hidden_labor_tracker
      - protected_time_dashboard
    required_protocols:
      - weekly_labor_accounting
      - monthly_fairness_audit
      - labor_concentration_review
      - optional_vs_required_labor_classifier
    external_review_blockers:
      - employment_labor_review_if_work_is_required_or_paid
      - disability_accommodation_review
      - privacy_review_for_labor_data
    gates:
      - gate_id: commons_labor_upper_bound
        capability_field: labor_time.commons_labor_hours_per_resident_per_week
        pass_condition:
          value_range: 4_to_8
        warn_condition:
          value_range: 8_to_10
        fail_condition:
          value_above: 12
        promotion_block_condition:
          public_life_burden_reduction_claim_while_labor_above_fail: true
        evidence_quality: moderate
        translation_confidence: moderate
        regulatory_strength: heuristic
        source_ids:
          - BLS_ATUS_2024

promotion_blockers:
  - id: no_high_need_support_model
    domain: care_health
    severity: block
    description: High-need support is not modeled.

  - id: no_accessible_route_to_essentials
    domain: mobility_access
    severity: block
    description: Essential accessible route coverage is incomplete.

  - id: no_due_process
    domain: governance_anticapture
    severity: block
    description: Commons decision process lacks due process.

  - id: reserves_excluded_from_affordability
    domain: legal_land_finance
    severity: block
    description: Affordability excludes reserves.

  - id: no_hazard_register_or_dependency_graph
    domain: risk_resilience
    severity: block
    description: Resilience claim lacks hazard register or dependency graph.

  - id: safety_critical_task_without_training_gate
    domain: labor_time
    severity: block
    description: Safety-critical task has no training gate.

scenario_requirements:
  care_health:
    required:
      - injury_event
      - medication_refrigeration_outage
      - illness_wave
      - high_need_evacuation
      - care_steward_exit
      - care_labor_burnout

  governance_anticapture:
    required:
      - member_expulsion_case
      - emergency_power_extension
      - founder_exit
      - admin_capture
      - major_debt_or_land_sale
      - privacy_breach

  mobility_access:
    required:
      - wheelchair_resident_day
      - elder_pharmacy_trip
      - fire_EMS_access
      - route_blockage
      - no_private_car_resident
      - shared_vehicle_failure

  legal_land_finance:
    required:
      - income_loss
      - reserve_drawdown
      - insurance_shock
      - debt_pressure
      - resident_exit
      - land_sale_pressure

  risk_resilience:
    required:
      - water_contamination
      - 72_hour_energy_outage
      - food_disruption
      - illness_wave
      - fire_or_shelter_loss
      - financial_shock
      - compound_heat_grid_outage

  labor_time:
    required:
      - normal_week
      - bad_week
      - hidden_labor_detection
      - care_labor_concentration
      - governance_conflict_month
      - maintenance_emergency
      - scale_80_300_730_1500

ui_warnings:
  care_no_external_path:
    domain: care_health
    severity: warn
    message: Care room lacks a clear external professional care path. This remains simulation-only.

  medication_unprotected:
    domain: care_health
    severity: fail
    message: Medication continuity is not protected by critical energy, privacy, or pharmacy access.

  governance_due_process_missing:
    domain: governance_anticapture
    severity: fail
    message: Commons decision lacks notice, review, appeal, or recordkeeping.

  emergency_power_no_sunset:
    domain: governance_anticapture
    severity: block
    message: Emergency authority has no sunset. Promotion blocked.

  accessible_route_gap:
    domain: mobility_access
    severity: fail
    message: Essential route coverage is below the 100% accessibility target.

  tenure_insecure:
    domain: legal_land_finance
    severity: fail
    message: Resident rights or land tenure are not explicit enough to pass.

  reserve_shortfall:
    domain: legal_land_finance
    severity: warn
    message: Reserves are missing or excluded from affordability. Cost model is not credible.

  hazard_register_missing:
    domain: risk_resilience
    severity: block
    message: Hazard register or dependency graph is missing. Resilience claim blocked.

  hidden_labor:
    domain: labor_time
    severity: fail
    message: Savings appear to depend on hidden or untracked labor.

  free_time_not_proven:
    domain: labor_time
    severity: warn
    message: Life burden reduction is not proven because free time or wage-hour reduction is not demonstrated.
```

---

## 7. Python Loader

### 7.1 Add `ciac/capability_policy.py`

Responsibilities:

```text
Load capability policy YAML.
Validate against schema.
Expose domains, gates, scenarios, promotion blockers, source registry, and UI warnings.
Normalize gate conditions into a common object shape.
Provide helper functions for CapabilityGate.
```

Suggested API:

```python
from pathlib import Path
from typing import Any

def load_capability_policy(path: str | Path | None = None) -> dict[str, Any]:
    ...

def validate_capability_policy(policy: dict[str, Any]) -> list[str]:
    ...

def get_domain_policy(policy: dict[str, Any], domain: str) -> dict[str, Any]:
    ...

def iter_gates(policy: dict[str, Any], domain: str | None = None):
    ...

def get_promotion_blockers(policy: dict[str, Any]) -> list[dict[str, Any]]:
    ...

def get_required_scenarios(policy: dict[str, Any], domain: str | None = None) -> list[str]:
    ...

def get_ui_warning(policy: dict[str, Any], warning_id: str) -> dict[str, Any] | None:
    ...
```

Default path:

```text
capability_policies/ciac_capability_policy_v0.yaml
```

---

## 8. Capability Gate Engine Changes

### 8.1 Current state

The repo already has `CapabilityState` and a v0 capability gate. Preserve it.

### 8.2 Target state

Add a policy-driven gate evaluator that can produce:

```yaml
CapabilityPolicyGateReport:
  kind: CapabilityPolicyGateReport
  policy_id: ciac_capability_policy_v0
  status: pass | warn | fail | promotion_blocked
  domain_statuses:
    care_health:
      status: pass | warn | fail | promotion_blocked
      gates: []
  warnings: []
  failures: []
  promotion_blockers: []
  unknowns: []
  source_ids: []
```

### 8.3 Evaluation strategy

Do not build a complex rules engine yet.

For v0:

```text
1. Gate conditions are declarative.
2. Evaluator checks whether capability_state has matching booleans/numbers/statuses.
3. Unknown fields produce warn/unknown unless the gate is a promotion blocker.
4. Existing hardcoded gates remain fallback.
```

Suggested function:

```python
def evaluate_policy_gates(
    capability_state: dict[str, Any],
    policy: dict[str, Any],
    *,
    mode: str = "simulation"
) -> dict[str, Any]:
    ...
```

Modes:

```yaml
mode:
  simulation:
    missing external review is warning/review_blocked, not fail

  promotion:
    missing external review or promotion_block_condition becomes promotion_blocked
```

Status resolution:

```python
priority = ["promotion_blocked", "fail", "warn", "pass"]
```

---

## 9. Scenario Pack

Add YAML scenario stubs under:

```text
scenarios/capability/
```

### 9.1 `care_health_illness_wave.yaml`

```yaml
scenario_id: care_health_illness_wave
domain: care_health
description: Tests whether the community can support illness without forcing sick residents into common meals or public disclosure.
required_capability_fields:
  - care_health.illness_wave_readiness
  - care_health.care_meal_protocol_status
  - care_health.medication_continuity_status
  - labor_time.hidden_labor_status
shocks:
  care_health:
    care_meal_demand_delta: 0.25
    care_steward_capacity_delta: -0.25
  labor_time:
    care_labor_hours_delta: 2
expected_gates:
  - illness_wave_readiness
  - care_nonclinical_floor
```

### 9.2 `governance_emergency_power_drift.yaml`

```yaml
scenario_id: governance_emergency_power_drift
domain: governance_anticapture
description: Tests emergency authority sunset and capture resistance.
required_capability_fields:
  - governance_anticapture.emergency_power_sunset
  - governance_anticapture.role_backup_coverage
  - governance_anticapture.records_privacy_status
shocks:
  governance_anticapture:
    emergency_mode_active: true
    emergency_extension_requested: true
expected_gates:
  - emergency_power_sunset
  - role_backup_and_concentration
```

### 9.3 `mobility_access_route_blockage.yaml`

```yaml
scenario_id: mobility_access_route_blockage
domain: mobility_access
description: Tests accessible route redundancy and high-need access during route blockage.
required_capability_fields:
  - mobility_access.accessible_route_coverage
  - mobility_access.emergency_access_status
  - mobility_access.non_driver_access_status
shocks:
  mobility_access:
    primary_route_blocked: true
    accessible_route_penalty_delta: 2
expected_gates:
  - accessible_route_coverage
  - emergency_access
```

### 9.4 `legal_finance_reserve_shock.yaml`

```yaml
scenario_id: legal_finance_reserve_shock
domain: legal_land_finance
description: Tests whether reserve and affordability logic survives a repair/insurance shock.
required_capability_fields:
  - legal_land_finance.reserve_status
  - legal_land_finance.affordability_burden_status
  - legal_land_finance.anti_displacement_status
shocks:
  legal_land_finance:
    emergency_repair_cost: true
    operating_reserve_months_delta: -1
expected_gates:
  - reserve_status
  - affordability_burden
```

### 9.5 `risk_resilience_compound_failure.yaml`

```yaml
scenario_id: risk_resilience_compound_failure
domain: risk_resilience
description: Tests a compound heat, grid outage, and care-support stress.
required_capability_fields:
  - risk_resilience.hazard_register_coverage
  - risk_resilience.dependency_graph_completeness
  - risk_resilience.graceful_degradation_status
  - care_health.high_need_support_coverage
shocks:
  risk_resilience:
    grid_outage_hours: 72
    extreme_heat: true
  care_health:
    high_need_support_demand_delta: 0.2
expected_gates:
  - mandatory_hazard_register
  - dependency_graph
  - graceful_degradation
```

### 9.6 `labor_time_hidden_burden.yaml`

```yaml
scenario_id: labor_time_hidden_burden
domain: labor_time
description: Tests hidden care, cleaning, governance, and emergency labor under a bad week.
required_capability_fields:
  - labor_time.commons_labor_hours_per_resident_per_week
  - labor_time.hidden_labor_status
  - labor_time.labor_concentration_score
  - labor_time.free_time_increase_hours_per_week
shocks:
  labor_time:
    commons_labor_hours_per_resident_per_week_delta: 3
    care_labor_concentration_delta: 2
    free_time_increase_hours_per_week_delta: -3
expected_gates:
  - commons_labor_upper_bound
  - labor_type_separation
  - meaningful_free_time
```

---

## 10. Simulation Integration

Modify simulation output to include policy gate status.

Add to output:

```json
{
  "capability_policy": {
    "policy_id": "ciac_capability_policy_v0",
    "version": "v0.1",
    "mode": "simulation",
    "status": "pass|warn|fail|promotion_blocked",
    "domain_statuses": {},
    "promotion_blockers": [],
    "warnings": [],
    "failures": [],
    "unknowns": []
  }
}
```

Existing fields should remain:

```json
"capability_state": {}
"capability_gate": {}
"capability_warnings": []
"capability_failures": []
```

Do not break current viewer or runtime bundle.

---

## 11. Runtime Bundle Integration

Runtime bundle should expose:

```json
"capabilities": {
  "state": {},
  "gate": {},
  "policy_gate": {},
  "policy_id": "ciac_capability_policy_v0",
  "promotion_mode": "simulation_only|review_blocked|promotion_ready"
}
```

Promotion mode resolution:

```yaml
promotion_ready:
  condition:
    - policy_gate.status == pass
    - promotion_blockers empty
    - required external reviews complete or not applicable

review_blocked:
  condition:
    - policy_gate pass_or_warn
    - unresolved external review blockers exist

simulation_only:
  condition:
    - model useful for visualization
    - not safe for real-world claim
```

---

## 12. World Viewer Integration

### 12.1 Evidence cards

Add policy context to evidence cards:

```json
{
  "capability_policy": {
    "domain": "care_health",
    "status": "review_blocked",
    "gates": ["care_nonclinical_floor", "medication_continuity"],
    "source_ids": ["CDC_DISABILITY_EMERGENCY_KIT"],
    "external_review_needed": ["clinical_boundary_review", "privacy_review"]
  }
}
```

### 12.2 Viewer warning panel

Show:

```text
Capability Warnings
Promotion Blockers
External Reviews Needed
Simulation-only Claims
Source IDs
```

### 12.3 Visual distinction

Use distinct states:

```yaml
pass:
  display: green

warn:
  display: yellow

fail:
  display: red

promotion_blocked:
  display: purple_or_lock_icon

simulation_only:
  display: gray_badge

review_blocked:
  display: amber_lock_badge
```

Do not let green simulation gates imply real-world buildability.

---

## 13. Tests

### 13.1 `tests/test_capability_policy.py`

```yaml
tests:
  - policy_file_exists
  - policy_schema_validates
  - all_source_ids_unique
  - all_gate_source_ids_exist_in_source_registry
  - all_domains_have_gates
  - all_promotion_blockers_have_domain_and_severity
  - scenario_requirements_include_all_six_domains
```

### 13.2 `tests/test_capability_gate_policy.py`

```yaml
tests:
  - care_floor_fails_without_external_care_path
  - medication_continuity_fails_without_critical_energy
  - due_process_fails_without_notice_review_appeal
  - emergency_power_blocks_without_sunset
  - accessible_route_coverage_100_passes
  - accessible_route_coverage_95_warns
  - any_essential_route_missing_fails
  - affordability_above_50_fails_without_subsidy
  - dependency_graph_missing_fails
  - commons_labor_4_to_8_passes
  - commons_labor_above_12_fails
  - hidden_labor_untracked_fails
```

### 13.3 `tests/test_capability_scenarios.py`

```yaml
tests:
  - every_required_scenario_file_exists
  - every_scenario_has_id_domain_description
  - every_scenario_required_capability_field_exists_in_policy
  - every_scenario_expected_gate_exists_in_policy
  - scenario_shocks_parse
```

---

## 14. Documentation

Add `docs/capability_policy_v0.md` with:

```text
purpose
relationship to CapabilityState
simulation_only vs review_blocked vs promotion_ready
policy schema
how gates work
how promotion blockers work
how scenario requirements work
how viewer warnings use the policy
how to add a new gate
what the policy does not prove
```

Add a README note:

```markdown
## Capability Policy

CIaC now supports a provisional capability policy layer. The policy evaluates non-resource civic capabilities such as care, governance, mobility, legal/finance resilience, risk, and labor/time. It can classify model states as pass, warn, fail, or promotion-blocked. A green simulation result does not certify real-world safety, legality, accessibility, clinical validity, affordability, or buildability.
```

---

## 15. Implementation Order

```yaml
phase_1_schema_and_policy:
  - create schemas/capability_policy.schema.json
  - create capability_policies/ciac_capability_policy_v0.yaml
  - add validation test

phase_2_loader:
  - create ciac/capability_policy.py
  - load default policy
  - validate policy
  - expose domains, gates, blockers, scenarios, warnings

phase_3_policy_gate:
  - update or create ciac/capability_gate.py
  - implement evaluate_policy_gates
  - support mode: simulation and promotion
  - preserve existing hardcoded gates as fallback

phase_4_scenarios:
  - add six scenario YAML files
  - validate scenario requirements
  - add tests

phase_5_simulation_runtime:
  - add policy_gate to simulation output
  - add capability policy status to runtime bundle

phase_6_viewer:
  - add policy status to evidence cards
  - add promotion-blocked and review-blocked badges
  - map ui_warnings

phase_7_docs_tests:
  - add docs/capability_policy_v0.md
  - update README
  - run full test suite
```

---

## 16. Acceptance Criteria

The implementation is complete when:

```yaml
acceptance_criteria:
  - capability_policy.schema.json exists and validates the policy YAML
  - capability_policies/ciac_capability_policy_v0.yaml exists
  - every gate source_id resolves to source_registry
  - capability_policy.py loads and validates the policy
  - capability_gate can evaluate policy gates
  - simulation output includes capability_policy report
  - runtime bundle includes policy_gate and promotion mode
  - viewer can display pass/warn/fail/promotion_blocked policy status
  - six capability scenarios exist and validate
  - tests pass
  - existing behavior remains backward-compatible
```

---

## 17. Suggested Commit Plan

```text
commit 1:
  add capability policy schema and initial policy YAML

commit 2:
  add capability policy loader and validation tests

commit 3:
  add policy-driven gate evaluation

commit 4:
  add capability scenario pack and tests

commit 5:
  connect policy gate to simulation and runtime bundle

commit 6:
  expose policy status in world viewer evidence cards

commit 7:
  add docs and README note

commit 8:
  test cleanup and compatibility fixes
```

---

## 18. Final Safety Language

Add this language to any generated policy report and viewer evidence panel:

```text
Capability policy results are provisional modeling aids. They do not certify real-world safety, legality, accessibility, clinical validity, affordability, labor compliance, engineering validity, public-health compliance, resident consent, or buildability. Promotion to real-world use requires the listed external reviews.
```

---

## 19. Next Possible Artifact

After this execution plan, the next useful artifact would be:

```text
ciac_capability_policy_v0_seed_files.zip
```

or individual starter files:

```text
schemas/capability_policy.schema.json
capability_policies/ciac_capability_policy_v0.yaml
scenarios/capability/*.yaml
tests/test_capability_policy.py
```
