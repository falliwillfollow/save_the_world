# CIaC Governance & Anti-Capture Module: Commons Stewardship Protocol

**Module ID:** `governance_anticapture.commons_stewardship_protocol.v0_1`  
**Status:** Draft requirement module  
**Purpose:** Define the default governance and anti-capture system for a scalable Minimum Viable Dignified Infrastructure complex.  
**Primary design question:** What governance structure best protects the civic floor, prevents rent extraction and founder capture, keeps decisions legible, distributes authority, resolves conflict, and preserves individual freedom without becoming bureaucratic, cult-like, or landlord-like?

---

## 1. Core Thesis

The CIaC governance baseline should **not** be charismatic founder rule, vague consensus culture, informal friendship governance, landlord benevolence, or pure market contracting.

A dignified infrastructure commons requires rules, but the rules should feel like guardrails around survival infrastructure, not ideology imposed on daily life.

The recommended baseline is a **Commons Stewardship Protocol**:

```text
commons asset lock
+ resident membership
+ clear rights and responsibilities
+ limited governance domains
+ consent/circle operations for day-to-day stewardship
+ member voting for constitutional decisions
+ transparent budgets and maintenance backlogs
+ role rotation and backup
+ conflict resolution ladder
+ anti-capture rules
+ external professional/legal review
+ exit rights
+ emergency authority with sunset clauses
+ federation layer for scaling
```

The goal is not maximum participation in meetings.

The goal is **minimum governance sufficient to protect the floor**.

---

## 2. Guiding Sentence

> The commons must be strong enough to protect survival infrastructure, light enough not to dominate daily life, and transparent enough that power cannot hide.

---

## 3. Strategic Decision

The best default model is:

# A resident-governed commons with locked survival assets, delegated operational circles, and constitutional anti-capture rules.

```yaml
governance_strategy:
  legal_asset_layer:
    purpose: protect_land_and_survival_infrastructure_from_speculation
    preferred_patterns:
      - community_land_trust_like_land_stewardship
      - limited_equity_cooperative_elements
      - nonprofit_or_public_benefit_asset_lock_where_appropriate
      - long_term_ground_lease_or_use_rights
      - resale_or_transfer_restrictions
      - commons_asset_lock

  membership_layer:
    purpose: define_who_has_rights_and_obligations
    preferred_patterns:
      - resident_membership
      - steward_membership_for_nonresident_supporters_where_needed
      - clear_entry_exit_rules
      - one_resident_one_vote_for_constitutional_matters
      - anti-discrimination_and_access_rules

  operational_layer:
    purpose: make_daily decisions without endless assemblies
    preferred_patterns:
      - delegated_circles_or_stewardship_teams
      - consent_decision_making_for_domain_policies
      - double_linked_circle_structure
      - role_elections
      - review_cycles
      - transparent_minutes_and_dashboards

  protection_layer:
    purpose: prevent_capture_abuse_and_drift
    preferred_patterns:
      - role_rotation
      - conflict_of_interest_rules
      - term_limits
      - audit_rights
      - budget_transparency
      - no_private_control_of_survival_systems
      - independent_review_for_sensitive_disputes
      - emergency_power_sunset_clauses
      - external_legal_and_professional_review

  avoid_as_default:
    - founder_permanent_control
    - landlord_as_benevolent_sovereign
    - consensus_for_everything
    - no_formal_rules
    - governance_by_friend_group
    - opaque_finances
    - indefinite_emergency_powers
    - mandatory_ideological_conformity
    - expulsion_without_due_process
    - survival_access_conditioned_on_social_popularity
```

### Rationale

The central governance challenge is not how to make everyone agree.

The challenge is how to protect the civic floor from four failure modes:

```text
1. Capture: a person, faction, founder, investor, landowner, or administrator gains control over survival infrastructure.

2. Drift: maintenance, reserves, safety, and role backups slowly degrade because no one notices or acts.

3. Coercion: access to housing, food, care, or belonging becomes conditional on social obedience.

4. Bureaucracy: the system becomes so procedural that people spend their recovered life force maintaining the governance machine.
```

---

## 4. Research Anchors

This module is grounded in the following research and precedent categories.

### 4.1 Commons governance

Elinor Ostrom's commons work identifies recurring design principles in durable commons institutions, including clear boundaries, rules suited to local conditions, collective-choice participation, monitoring, graduated sanctions, low-cost conflict resolution, recognition of local rights to organize, and nested enterprises for larger systems.

**Design implication:** CIaC should not rely on vague goodwill. It needs defined boundaries, rule participation, monitoring, conflict resolution, and nested governance.

### 4.2 Community land trusts

Community land trusts separate land ownership from building/use rights, often using long-term ground leases and resale formulas to preserve permanent affordability.

**Design implication:** The land and survival-infrastructure layer should be protected from speculation and private windfall capture.

### 4.3 Cooperative governance

Cooperatives are member-owned and democratically controlled enterprises, generally organized to meet member needs rather than maximize investor return.

**Design implication:** Residents should hold democratic rights in the systems they depend on, but daily operations should not require everyone to vote on everything.

### 4.4 Sociocracy / consent-based circles

Sociocracy uses semi-autonomous circles, consent decision-making, elected roles, and double-linking between governance levels.

**Design implication:** CIaC can use circles for operational domains such as food, water, care, maintenance, and energy while reserving major constitutional decisions for the membership.

### 4.5 Asset locks and nonprofit/public-benefit protections

Charitable/nonprofit asset rules can require assets to remain dedicated to exempt or public purposes upon dissolution, depending on legal form and jurisdiction.

**Design implication:** The app should model asset-lock options and legal-review requirements, but never pretend to choose a final legal structure without counsel.

### 4.6 Restorative and conflict-resolution practices

Restorative processes emphasize accountability, harm repair, respectful voice, and restoration of trust where possible.

**Design implication:** Conflict handling should have a ladder: direct repair, mediation, restorative process, formal review, external authority, and legal escalation where required.

### 4.7 Whole-community resilience

Emergency-management frameworks emphasize planning with the whole community, including vulnerable populations and cross-sector capabilities.

**Design implication:** Governance must include high-need residents, not only the most available, loudest, healthiest, or most technically skilled members.

---

## 5. Recommended Scale

The governance module should support the same first serious population as the physical infrastructure modules.

```yaml
population:
  minimum_meaningful_scale: 50
  ideal_first_model: 80
  upper_bound_before_replication: 150
```

### Scale Logic

```text
Below 50:
  governance may be too personal and informal. Friendship, romance, status, or founder influence can dominate.

Around 80:
  membership, circles, elected roles, role backup, transparent records, and conflict systems become realistic without becoming city-scale bureaucracy.

Above 150:
  governance may require federation, professional administration, formal staff, stronger privacy controls, and more explicit legal structures.
```

### Scaling Method

Use nested village-block governance.

```yaml
scaling:
  50-100_residents:
    membership_body: 1
    operational_circles: 5-8
    coordination_circle: 1
    external_review: required_for_legal_finance_safety

  100-150_residents:
    membership_body: 1
    operational_circles: 8-12
    coordination_circle: 1
    resident_ombuds_or_safeguarding_role: preferred
    part_time_admin_or_operations_role: preferred

  above_150_residents:
    recommendation: replicate_village_block_and_federate
    reason: preserve_human_scale_and_prevent_bureaucratic_mass
```

---

## 6. Default Prototype

```yaml
default_prototype:
  name: commons_stewardship_protocol_80
  residents: 80

  legal_structure_profile:
    default_status: requires_legal_review
    candidate_patterns:
      - land_trust_or_CLT_like_stewardship
      - limited_equity_cooperative_for_housing_use_rights
      - nonprofit_or_public_benefit_entity_for_common_assets
      - operating_cooperative_for_shared_services
      - ground_lease_or_occupancy_agreements
    app_boundary: cannot_select_final_legal_structure_without_attorney

  governing_bodies:
    - resident_membership_body
    - coordination_circle
    - housing_circle
    - food_circle
    - water_sanitation_circle
    - energy_circle
    - maintenance_circle
    - care_health_circle
    - finance_reserve_circle
    - conflict_safeguarding_circle

  core_rules:
    - commons_asset_lock
    - one_resident_one_vote_for_constitutional_decisions
    - delegated_operational_authority
    - role_rotation
    - backup_roles
    - public_budget_and_maintenance_reports
    - conflict_of_interest_disclosure
    - no_private_control_of_survival_systems
    - emergency_authority_sunset
    - due_process_for_loss_of_membership_or_access
    - exit_rights
```

---

## 7. Governance Scope

The governance system should be limited to what it must govern.

```yaml
governance_scope:
  must_govern:
    - land_and_common_assets
    - survival_infrastructure
    - maintenance_and_repair
    - budgets_and_reserves
    - safety_rules
    - shared_spaces
    - role_rotation
    - conflict_processes
    - entry_exit_membership
    - emergency_response
    - professional_handoff
    - privacy_and_care_boundaries

  should_not_govern_by_default:
    - personal_beliefs
    - romantic_relationships_except_safety_or_harassment_issues
    - private_art_or_creative_life
    - diet_except_shared_food_safety_and_common_meals
    - spirituality
    - political_conformity
    - personal_work_or_business_except_externalities
    - private_visitors_except_safety_capacity_and_shared_space_rules
```

### Scope Principle

```text
The commons governs the floor, not the soul.
```

---

## 8. Constitutional Layer

The constitutional layer defines what ordinary governance cannot easily change.

```yaml
constitutional_layer:
  purpose: protect_core_rights_and_asset_integrity

  requires_member_supermajority_and_review:
    - sale_or_transfer_of_common_land
    - changes_to_asset_lock
    - changes_to_membership_rights
    - changes_to_exit_rights
    - changes_to_expulsion_process
    - assumption_of_major_debt
    - privatization_of_survival_infrastructure
    - change_to_voting_structure
    - merger_with_external_entity
    - dissolution
    - emergency_power_extension

  protected_principles:
    - minimum_dignified_life_floor
    - no_private_rent_extraction_from_survival_systems
    - resident_due_process
    - privacy_and_consent
    - accessibility_and_non-discrimination
    - maintenance_reserve_protection
    - transparent_finances
    - open_records_for_common_assets
```

### Constitutional Principle

```text
The most dangerous decisions should be slow, visible, and hard to capture.
```

---

## 9. Commons Asset Lock

The asset lock protects land and survival systems from speculation and private capture.

```yaml
commons_asset_lock:
  covered_assets:
    - land
    - common_house
    - water_system
    - sanitation_system
    - energy_system
    - food_commons
    - workshop_tool_library
    - care_health_room
    - maintenance_spares
    - critical_common_reserves

  default_rules:
    - assets_may_not_be_sold_for_private_distribution
    - survival_infrastructure_may_not_be_pledged_without_member_approval
    - transfer_requires_supermajority_and_external_legal_review
    - dissolution_assets_must_remain_dedicated_to_public_or_commons_purpose_where_legal_form_allows
    - resale_or_exit_value_rules_must_not_destroy_long_term_affordability
    - no_investor_class_control_over_core_assets

  app_outputs:
    - asset_lock_status
    - assets_at_capture_risk
    - legal_review_required
    - resale_or_transfer_rules
    - dissolution_risk_report
```

### Asset Lock Principle

```text
No one should be able to become rich by enclosing the floor.
```

---

## 10. Membership and Rights

Membership defines participation, access, and obligations.

```yaml
membership_model:
  member_types:
    resident_member:
      rights:
        - occupancy_or_use_right_subject_to_agreement
        - vote_on_constitutional_matters
        - participate_in_circle_selection
        - access_common_infrastructure
        - review_common_records
        - due_process
        - exit
      obligations:
        - pay_fair_assessments_or_contribute_as_agreed
        - follow_safety_rules
        - participate_in_minimum_commons_obligations_or_equivalent
        - respect_privacy_and_conflict_processes
        - maintain_shared_spaces

    nonresident_supporting_member:
      optional: true
      rights:
        - limited_advisory_participation
        - no_control_over_survival_infrastructure
      restrictions:
        - no_vote_on_resident_life_unless_defined
        - no_asset_capture_rights

    professional_or_partner_member:
      optional: true
      rights:
        - advisory_or_contractual_role_only
      restrictions:
        - no_governance_control_unless_explicit_and_limited

  entry:
    required:
      - transparent_application_or_onboarding
      - anti-discrimination_policy
      - trial_or_orientation_period
      - rights_and_obligations_explained
      - financial_obligations_disclosed
      - conflict_process_disclosed

  exit:
    required:
      - clear_notice_period
      - return_of_allowed_equity_or_deposit_terms
      - no_punitive_exit
      - continuity_plan_for_roles
      - personal_data_and_records_handling
```

### Membership Principle

```text
People must know what they are joining, what they can count on, what is expected, and how they can leave.
```

---

## 11. Decision Domains

The app should distinguish decision types.

```yaml
decision_domains:
  operational_decision:
    examples:
      - weekly_meal_schedule
      - maintenance_task_assignment
      - garden_plan
      - cleaning_rotation
      - tool_purchase_below_threshold
    method: circle_decision_or_role_authority
    speed: fast

  policy_decision:
    examples:
      - kitchen_use_policy
      - guest_policy
      - tool_library_rules
      - maintenance_prioritization_policy
      - common_meal_cost_policy
    method: consent_decision_in_domain_circle_with_review
    speed: moderate

  budget_decision:
    examples:
      - annual_operating_budget
      - reserve_allocation
      - assessment_change
      - major_purchase
    method: finance_circle_recommendation_plus_member_approval_by_threshold
    speed: moderate_to_slow

  constitutional_decision:
    examples:
      - land_sale
      - asset_lock_change
      - expulsion_policy
      - debt_above_threshold
      - dissolution
    method: supermajority_member_vote_plus_external_review
    speed: slow

  emergency_decision:
    examples:
      - water_contamination
      - power_outage
      - illness_wave
      - flood_or_fire
      - sewage_failure
    method: predefined_emergency_roles_with_sunset_and_review
    speed: immediate
```

### Decision Principle

```text
Not every decision deserves the same process.
```

---

## 12. Operational Circles

Operational circles allow specialized work without central bureaucracy.

```yaml
operational_circles:
  required:
    housing_circle:
      domain:
        - private_unit_interfaces
        - common_space_use
        - accessibility_issues
        - noise_and_layout_feedback

    food_circle:
      domain:
        - common_meals
        - pantry
        - procurement
        - gardens
        - food_safety_interface

    water_sanitation_circle:
      domain:
        - water_status
        - testing_schedule
        - sanitation_operations
        - waste_streams
        - public_health_escalation

    energy_circle:
      domain:
        - critical_loads
        - outage_mode
        - energy_dashboard
        - solar_storage
        - thermal_resilience

    maintenance_circle:
      domain:
        - asset_registry
        - work_orders
        - spares
        - contractor_coordination
        - safety_boundaries

    care_health_circle:
      domain:
        - care_room
        - illness_wave_protocol
        - care_meals
        - high_need_support
        - external_care_relationships

    finance_reserve_circle:
      domain:
        - operating_budget
        - reserves
        - assessments
        - audits
        - affordability_watch

    conflict_safeguarding_circle:
      domain:
        - conflict_ladder
        - mediation
        - restorative_processes
        - safeguarding
        - harassment_or_abuse_escalation
        - ombuds_interface

  coordination_circle:
    purpose:
      - coordinate_interdependencies
      - resolve_cross_circle_conflicts
      - track_gates
      - prepare_member_decisions
      - monitor_capture_risks

  double_linking:
    required: true
    purpose:
      - each_operational_circle_sends_delegate_to_coordination_circle
      - coordination_circle_has_link_to_operational_circles
      - information_flows_both_ways
```

### Circle Principle

```text
Delegate authority to the people closest to the work, but keep the links visible.
```

---

## 13. Role Design

Roles should be explicit, limited, reviewable, and backed up.

```yaml
role_design:
  required_fields:
    - role_id
    - purpose
    - domain
    - authority_limits
    - responsibilities
    - decision_rights
    - budget_authority
    - safety_boundaries
    - required_training
    - backup_role
    - term_length
    - review_date
    - conflict_of_interest_risks
    - removal_or_replacement_process

  role_rules:
    - no_permanent_control_of_survival_systems
    - all_critical_roles_have_backup
    - roles_have_term_limits_or_review_cycles
    - role_authority_is_documented
    - role_performance_is_reviewed
    - emergency_roles_sunset_after_event
    - paid_roles_have_accountability_rules
```

### Role Principle

```text
Power should be attached to roles, not personalities.
```

---

## 14. Finance Transparency and Reserves

Financial opacity is one of the fastest paths to capture.

```yaml
finance_transparency:
  required:
    - operating_budget
    - maintenance_budget
    - replacement_reserve
    - emergency_reserve
    - affordability_report
    - debt_report
    - insurance_report
    - assessment_schedule
    - financial_dashboard
    - annual_review
    - external_accounting_or_audit_threshold

  protected_funds:
    - maintenance_reserve
    - replacement_reserve
    - emergency_reserve
    - care_hardship_reserve_where_established

  prohibited_without_member_approval:
    - pledging_core_assets
    - taking_major_debt
    - using_reserves_for_discretionary_projects
    - insider_contracts
    - above_threshold_unbudgeted_spending

  app_outputs:
    - monthly_cost_per_resident
    - reserve_health
    - debt_exposure
    - assessment_burden
    - affordability_drift
    - insider_transaction_flags
```

### Finance Principle

```text
A commons with opaque money is already halfway captured.
```

---

## 15. Anti-Capture Rules

The anti-capture layer should treat capture as expected, not exceptional.

```yaml
anti_capture_rules:
  founder_capture:
    controls:
      - founder_roles_time_limited
      - founder_no_permanent_veto
      - succession_plan
      - documentation_transfer
      - independent_board_or_advisory_review_where_appropriate

  landowner_capture:
    controls:
      - land_in_asset_locked_entity
      - ground_lease_or_use_rights
      - resident_due_process
      - anti_eviction_abuse_rules
      - no_unilateral_rent_increase

  investor_capture:
    controls:
      - no_investor_control_over_core_assets
      - capped_return_if_external_capital_used
      - no_survival_infrastructure_as_speculative_asset
      - member_approval_for_debt_or_equity_like_obligations

  administrator_capture:
    controls:
      - transparent_records
      - role_rotation
      - budget_review
      - grievance_process
      - data_export
      - no_private_admin_access_to_core_systems_without oversight

  faction_capture:
    controls:
      - supermajority_for_constitutional_changes
      - minority_rights
      - conflict_process
      - external_mediation_available
      - anti-harassment_and_safeguarding

  expert_capture:
    controls:
      - professionals_advise_not_rule
      - resident_review
      - documentation_in_plain_language
      - second_opinion_thresholds
      - no_single_vendor_dependency

  social_capture:
    controls:
      - no_survival_access_conditioned_on_popularity
      - due_process
      - privacy_rules
      - anti-retaliation
      - external_advocacy_path
```

### Capture Principle

```text
Any power that controls shelter, food, water, care, energy, or belonging will eventually tempt someone to misuse it.
```

---

## 16. Conflict Resolution Ladder

Conflict is normal. The system should not pretend harmony is permanent.

```yaml
conflict_resolution_ladder:
  level_0_prevention:
    tools:
      - clear_roles
      - clear_shared_space_rules
      - transparent_records
      - onboarding
      - feedback_loops

  level_1_direct_repair:
    use_when:
      - low_severity_interpersonal_conflict
      - misunderstanding
      - minor_shared_space_issue
    support:
      - scripts
      - voluntary_direct_conversation
      - role_facilitator_if_requested

  level_2_mediation:
    use_when:
      - direct_repair_failed
      - recurring_conflict
      - role_or_task_dispute
    support:
      - trained_mediator
      - written_agreement
      - followup_date

  level_3_restorative_or_accountability_process:
    use_when:
      - harm_occurred
      - community_trust_affected
      - repair_possible
    support:
      - trained_facilitator
      - consent_of_harmed_party_where_required
      - accountability_plan
      - safety_boundaries

  level_4_formal_review:
    use_when:
      - safety_issue
      - harassment
      - repeated_rule_violation
      - financial_or_role_abuse
      - unresolved_shared_infrastructure_conflict
    support:
      - documented_process
      - impartial_reviewers
      - evidence
      - appeal_path

  level_5_external_authority:
    use_when:
      - violence
      - abuse
      - serious_harassment
      - criminal_issue
      - legal_rights_issue
      - health_or_safety_authority_needed
    support:
      - external_mediator
      - attorney
      - public_authority
      - law_enforcement_or_protective_services_where_appropriate

  prohibited:
    - mob_decision_without_due_process
    - expulsion_by_social_pressure
    - retaliation_against_complainants
    - forced_restorative_process_for_serious_harm
    - confidentiality_used_to_hide_abuse
```

### Conflict Principle

```text
A humane commons must be able to say both “repair is possible” and “some harms require protection and external authority.”
```

---

## 17. Due Process and Loss of Access

Loss of housing or survival access is too serious for informal governance.

```yaml
due_process:
  applies_to:
    - membership_termination
    - eviction_or_loss_of_occupancy
    - suspension_from_common_assets
    - removal_from_role_for_misconduct
    - major_financial_penalties

  required:
    - written_notice
    - stated_reasons
    - evidence_access_where_safe
    - opportunity_to_respond
    - impartial_review
    - appeal_path
    - reasonable_accommodation_review
    - external_legal_review_where_required
    - emergency_temporary_action_only_when_safety_requires

  emergency_temporary_action:
    allowed_if:
      - immediate_safety_risk
      - narrowly_tailored
      - time_limited
      - reviewed_quickly
      - documented
```

### Due Process Principle

```text
No one should lose the floor because a group is angry, tired, or socially aligned against them.
```

---

## 18. Emergency Governance

Emergencies require speed, but emergency powers are capture risks.

```yaml
emergency_governance:
  emergency_domains:
    - water_contamination
    - fire
    - flood
    - power_outage
    - illness_wave
    - sanitation_failure
    - violence_or_immediate_safety_threat
    - severe_weather
    - food_supply_disruption

  required:
    - emergency_roles
    - authority_limits
    - communication_tree
    - incident_log
    - resident_notification
    - external_authority_contacts
    - spending_thresholds
    - sunset_clause
    - after_action_review

  sunset:
    default: 72_hours
    extension_requires:
      - coordination_circle_review
      - member_notification
      - documented_reason
      - next_review_date

  prohibited:
    - indefinite_emergency_rule
    - unrelated_policy_changes_during_emergency
    - using_emergency_to_bypass_asset_lock
    - using_emergency_to_remove_opponents
```

### Emergency Principle

```text
Emergency authority should move fast, end quickly, and leave an audit trail.
```

---

## 19. Data Governance and Privacy

The app will hold sensitive operational and personal data.

```yaml
data_governance:
  public_to_members:
    - budgets
    - maintenance_backlog
    - asset_registry_except_sensitive_security_details
    - meeting_minutes
    - role_assignments
    - policy_decisions
    - aggregate_labor_burden
    - gate_status

  role_limited:
    - high_need_resident_support_registry
    - conflict_case_details
    - personnel_or_paid_role_reviews
    - security_access_logs
    - sensitive_vendor_credentials
    - legal_matters

  private:
    - health_details
    - personal_financial_hardship_details
    - personal conflict disclosures
    - protected identity or safety information
    - private unit access data unless emergency/safety requires

  required:
    - data_minimization
    - role_based_access
    - exportability
    - audit_log
    - retention_policy
    - resident_record_access
    - no_surveillance_by_default
```

### Data Principle

```text
Transparency belongs to common power. Privacy belongs to vulnerable people.
```

---

## 20. Labor and Governance Burden

Governance should not consume the life it is meant to return.

```yaml
governance_labor_model:
  labor_categories:
    - member_meetings
    - circle_meetings
    - role_work
    - recordkeeping
    - conflict_processes
    - budget_review
    - onboarding
    - training
    - audits
    - emergency_reviews
    - external_coordination

  required_metrics:
    total_governance_hours_per_month: number
    governance_hours_per_resident_per_month: number
    meeting_hours_per_resident_per_month: number
    role_hours_per_resident_per_month: number
    conflict_hours_per_month: number
    admin_hours: number
    volunteer_hours: number
    paid_admin_hours: number
    participation_distribution_score: number
    governance_burnout_risk: low_medium_high
```

### Labor Targets

```yaml
labor_targets:
  governance_hours_per_resident:
    target: 1-3_hours_per_month
    warning_above: 5_hours_per_month
    fail_above: 8_hours_per_month_unless_resident_opt_in_or_paid_role

  meeting_hours:
    target: 1-2_hours_per_resident_per_month
    warning_above: 4_hours
    fail_above: 6_hours_unless_crisis

  participation:
    warn_if:
      - same_small_group_makes_most_decisions
      - many_residents_disengaged
      - high_need_residents_excluded
      - paid_staff_make_unreviewed_policy
```

### Governance Burden Principle

```text
A commons has failed if residents escape wage bureaucracy only to live inside meeting bureaucracy.
```

---

## 21. Automation-Favoring Requirements

Automation should make governance visible, auditable, and lighter.

```yaml
automation_requirements:
  governance_dashboard:
    required: true
    purpose:
      - show_roles
      - show_open_decisions
      - show_policy_review_dates
      - show_budget_status
      - show_gate_status
      - show_meeting_schedule
      - show_action_items

  decision_log:
    required: true
    purpose:
      - record_decisions
      - record_method
      - record_domain
      - record_authority
      - record_review_date
      - record_vote_or_consent_status

  policy_registry:
    required: true
    purpose:
      - version_policies
      - show_owner_circle
      - show_review_cycle
      - prevent_unwritten_rules

  role_registry:
    required: true
    purpose:
      - show_role_authority
      - show_term
      - show_backup
      - show_conflicts_of_interest
      - show_training

  budget_transparency:
    required: true
    purpose:
      - budget_status
      - reserves
      - debt
      - assessments
      - major_spending
      - affordability_drift

  conflict_case_tracker:
    required: true
    privacy: role_limited
    purpose:
      - process_stage
      - due_dates
      - safety_flags
      - followup
      - external_referral

  anti_capture_monitor:
    required: true
    purpose:
      - detect_role_concentration
      - detect_budget_opacity
      - detect_vendor_lock_in
      - detect_debt_risk
      - detect_reserve_misuse
      - detect_emergency_power_extension
      - detect_survival_system_control_risk

  avoid:
    - AI_deciding_membership_termination
    - AI_scoring_resident_worth
    - opaque_recommendations_about_conflict
    - surveillance_based_governance
    - voting_without_deliberation_for_high_stakes_decisions
    - automation_that_obscures_authority
```

### Automation Principle

```text
Automate records, reminders, transparency, and capture warnings. Do not automate sovereignty over people.
```

---

## 22. Governance Roles

```yaml
governance_roles:
  membership_steward:
    purpose: onboarding, membership records, entry/exit process
    required_backup: true

  records_steward:
    purpose: minutes, decision log, policy registry, archive
    required_backup: true

  coordination_circle_facilitator:
    purpose: cross-circle coordination and agenda flow
    required_backup: true

  finance_steward:
    purpose: budget, reserves, assessments, financial transparency
    required_backup: true

  asset_lock_steward:
    purpose: monitor protected assets, transfer restrictions, legal review triggers
    required_backup: true

  anti_capture_steward:
    purpose: monitor role concentration, conflicts of interest, emergency-power drift
    required_backup: true

  conflict_resolution_steward:
    purpose: conflict ladder, mediation, restorative processes, external referrals
    required_backup: true

  safeguarding_steward:
    purpose: abuse, harassment, retaliation, privacy, high-risk situations
    required_backup: true

  emergency_governance_steward:
    purpose: emergency authorities, incident logs, sunset reviews
    required_backup: true

  legal_professional_review_liaison:
    purpose: attorneys, accountants, insurance, public authorities, professionals
    required_backup: true
```

### Role Rule

```text
No one who controls records, money, land, or conflict process should be unreviewable.
```

---

## 23. Scenario Simulations

The governance module must support stress simulations.

```yaml
governance_anticapture_scenarios:
  normal_year:
    tests:
      - role_rotation
      - meeting_load
      - budget_transparency
      - policy_review
      - conflict_volume
      - resident_participation
      - governance_burnout

  founder_exit:
    tests:
      - documentation_transfer
      - succession
      - role_backup
      - asset_control
      - cultural_dependency

  founder_capture_attempt:
    tests:
      - veto_detection
      - role_concentration
      - budget_control
      - resident_rights
      - constitutional_safeguards

  investor_or_debt_pressure:
    tests:
      - asset_lock
      - debt_thresholds
      - reserve_protection
      - member_approval
      - affordability_drift

  land_sale_pressure:
    tests:
      - supermajority_requirement
      - legal_review
      - resident_notice
      - dissolution_or_transfer_rules
      - anti_displacement_plan

  faction_conflict:
    tests:
      - minority_rights
      - mediation
      - formal_review
      - due_process
      - external_mediation
      - governance_continuity

  administrator_capture:
    tests:
      - access_control
      - record_transparency
      - audit_log
      - budget_review
      - role_replacement

  emergency_power_drift:
    tests:
      - sunset_clause
      - after_action_review
      - unrelated_policy_block
      - member_notification
      - power_return_to_normal_roles

  high_need_resident_exclusion:
    tests:
      - access_functional_needs_representation
      - care_privacy
      - reasonable_accommodation
      - decision_access
      - conflict_safeguards

  member_expulsion_case:
    tests:
      - notice
      - evidence
      - response
      - impartial_review
      - appeal
      - legal_review
      - housing_continuity_or_transition_support
```

---

## 24. Governance & Anti-Capture Gates

The app should fail or warn based on governance viability.

```yaml
governance_anticapture_gates:
  asset_lock_gate:
    fail_if:
      - land_or_survival_assets_can_be_privately_sold_without_member_review
      - founder_or_investor_has_permanent_control
      - no_legal_review_for_asset_structure
      - no_dissolution_or_transfer_rule
      - no_reserve_protection

    warn_if:
      - asset_lock_unimplemented
      - resale_or_exit_formula_missing
      - debt_can_encumber_core_assets_above_threshold

  membership_rights_gate:
    fail_if:
      - no_written_membership_rights
      - no_exit_rights
      - no_due_process_for_loss_of_access
      - no_anti_discrimination_policy
      - no_privacy_rules

  decision_domain_gate:
    fail_if:
      - no_distinction_between_operational_policy_budget_constitutional_and_emergency_decisions
      - high_stakes_decisions_can_be_made_by_single_role
      - emergency_authority_has_no_sunset

  role_capture_gate:
    fail_if:
      - critical_role_has_no_backup
      - one_person_controls_money_records_and_conflict_process
      - survival_system_roles_are_permanent
      - role_authority_undefined

    warn_if:
      - same_small_group_holds_many_critical_roles
      - role_reviews_overdue
      - paid_staff_make_unreviewed_policy

  finance_gate:
    fail_if:
      - no_budget_transparency
      - no_maintenance_or_replacement_reserve
      - no_debt_threshold_policy
      - insider_transactions_unreviewed

    warn_if:
      - affordability_drift
      - reserves_declining_without_plan
      - member_assessments_increasing_faster_than_baseline

  conflict_gate:
    fail_if:
      - no_conflict_resolution_process
      - no_safeguarding_process
      - expulsion_possible_without_due_process
      - serious_harm_handled_only_internally
      - retaliation_protections_absent

  data_privacy_gate:
    fail_if:
      - health_or_conflict_data_public_by_default
      - no_role_based_access
      - no_data_retention_policy
      - no_export_or_audit_log_for_governance_records

  governance_burden_gate:
    fail_if:
      - governance_hours_per_resident_above_8_per_month_by_default
      - consensus_required_for_routine_operational_decisions
      - meeting_load_blocks_normal_life

    warn_if:
      - governance_hours_per_resident_above_5_per_month
      - participation_concentrated
      - high_need_residents_underrepresented

  legitimacy_gate:
    fail_if:
      - residents_have_no_meaningful_vote_on_constitutional_matters
      - operational_rules_are_unwritten
      - decisions_have_no_record
      - external_law_or_professional_review_ignored_where_required
```

---

## 25. App Modeling Boundary

The app should model governance at the level of **rights, roles, domains, decision processes, asset protection, transparency, labor burden, conflict ladders, capture risk, and review triggers**, not final legal drafting.

### The App Should Model

```text
membership rights
entry and exit rules
decision domains
role authority
circle structure
asset lock requirements
budget transparency
reserve rules
conflict process
due process
privacy rules
emergency powers
capture risks
governance labor burden
external review requirements
scenario failures
```

### The App Should Not Claim to Solve by Default

```text
final legal entity selection
tax law
securities law
housing law
eviction law
employment law
nonprofit law
cooperative incorporation
CLT legal drafting
ground lease drafting
anti-discrimination compliance
privacy law compliance
criminal matters
abuse investigation
clinical or safeguarding authority
```

### Principle

```text
The app should identify what must be true for governance legitimacy and anti-capture resilience.
Qualified legal, financial, safety, care, and community-governance professionals must validate implementation.
```

---

## 26. Required Data Model

```yaml
GovernanceAntiCaptureCommons:
  id: string
  population_served: integer

  legal_asset_layer:
    land_stewardship_model: CLT_like | cooperative | nonprofit | leasehold | unknown
    legal_review_status: unknown | required | in_progress | reviewed | failed
    asset_lock_defined: boolean
    dissolution_rule_defined: boolean
    resale_or_exit_formula_defined: boolean
    core_assets_protected_percent: number
    debt_threshold_policy: boolean

  membership:
    resident_members_total: integer
    written_rights: boolean
    entry_process: boolean
    exit_process: boolean
    anti_discrimination_policy: boolean
    due_process_policy: boolean
    member_vote_on_constitutional_matters: boolean

  decision_domains:
    operational_domain_defined: boolean
    policy_domain_defined: boolean
    budget_domain_defined: boolean
    constitutional_domain_defined: boolean
    emergency_domain_defined: boolean
    supermajority_rules_defined: boolean
    emergency_sunset_defined: boolean

  circles:
    operational_circles_total: integer
    coordination_circle: boolean
    double_linking: boolean
    circle_minutes_public_to_members: boolean
    circle_review_cycles_defined: boolean

  roles:
    critical_roles_total: integer
    critical_roles_with_backup_percent: number
    roles_with_term_or_review_percent: number
    conflict_of_interest_policy: boolean
    role_concentration_score: number

  finance:
    budget_public_to_members: boolean
    reserve_status_public: boolean
    debt_report_public: boolean
    affordability_report: boolean
    insider_transaction_policy: boolean
    external_audit_or_review_threshold: boolean

  conflict_safeguarding:
    conflict_ladder: boolean
    mediation_available: boolean
    restorative_process_available: boolean
    formal_review_available: boolean
    external_authority_escalation: boolean
    anti_retaliation_policy: boolean
    safeguarding_policy: boolean

  data_governance:
    role_based_access: boolean
    audit_log: boolean
    data_retention_policy: boolean
    sensitive_data_rules: boolean
    no_public_health_status_dashboard: boolean
    records_exportable: boolean

  labor:
    total_governance_hours_per_month: number
    governance_hours_per_resident_per_month: number
    meeting_hours_per_resident_per_month: number
    participation_distribution_score: number
    governance_burnout_risk: low | medium | high

  automation:
    governance_dashboard: boolean
    decision_log: boolean
    policy_registry: boolean
    role_registry: boolean
    budget_transparency_dashboard: boolean
    conflict_case_tracker: boolean
    anti_capture_monitor: boolean

  outputs:
    governance_legitimacy_status: pass | warn | fail
    asset_capture_status: pass | warn | fail
    role_capture_status: pass | warn | fail
    finance_transparency_status: pass | warn | fail
    conflict_readiness_status: pass | warn | fail
    privacy_status: pass | warn | fail
    governance_burden_score: number
    anti_capture_score: number
    life_burden_reduction_score: number
    complexity_score: number
```

---

## 27. Required App Outputs

```yaml
required_outputs:
  - governance_system_summary
  - asset_lock_report
  - membership_rights_report
  - decision_domain_report
  - circle_structure_report
  - role_authority_and_backup_report
  - finance_transparency_report
  - reserve_and_debt_risk_report
  - conflict_resolution_report
  - due_process_report
  - data_privacy_report
  - emergency_governance_report
  - anti_capture_risk_report
  - governance_labor_burden_report
  - legal_professional_review_requirements
  - scenario_failure_report
  - visualization_bundle_metadata
```

---

## 28. Visualization Requirements

The governance module should export enough data for a dashboard or virtual world to show how authority, risk, and decisions flow without exposing sensitive personal information.

```yaml
visualization_requirements:
  graph_objects:
    - membership_body
    - operational_circles
    - coordination_circle
    - roles
    - core_assets
    - protected_reserves
    - decision_domains
    - conflict_ladder
    - emergency_roles

  overlays:
    - role_concentration
    - asset_capture_risk
    - finance_transparency_status
    - policy_review_due
    - emergency_power_status
    - open_decisions
    - governance_labor_burden
    - unresolved_conflict_stage
    - legal_review_required

  scenario_playback:
    - founder_exit
    - founder_capture_attempt
    - investor_or_debt_pressure
    - land_sale_pressure
    - faction_conflict
    - administrator_capture
    - emergency_power_drift
    - high_need_resident_exclusion
    - member_expulsion_case

  privacy_rule:
    - never_visualize_private_conflict_details
    - never_visualize_health_status
    - never_visualize_personal_financial_hardship
```

---

## 29. Best Default Requirements Summary

```yaml
MinimumViableGovernanceAntiCaptureCommons:
  population:
    first_serious_model: 80
    valid_range: 50-150

  philosophy:
    protect_the_floor: true
    govern_the_commons_not_the_soul: true
    founder_sovereignty: false
    landlord_benevolence: false
    meeting_bureaucracy: false
    transparency_for_power: true
    privacy_for_vulnerability: true

  asset_layer:
    commons_asset_lock: required
    legal_review: required
    core_assets_protected: required
    debt_thresholds: required
    dissolution_or_transfer_rules: required
    resale_or_exit_formula: preferred_or_required_depending_structure

  membership:
    written_rights: required
    resident_vote_on_constitutional_matters: required
    exit_rights: required
    due_process: required
    anti_discrimination_policy: required

  operations:
    delegated_circles: required
    coordination_circle: required
    role_registry: required
    backup_roles: required
    policy_registry: required
    decision_log: required

  protection:
    conflict_resolution_ladder: required
    safeguarding_process: required
    finance_transparency: required
    emergency_power_sunset: required
    anti_capture_monitor: required
    external_review_triggers: required

  automation:
    governance_dashboard: required
    decision_log: required
    policy_registry: required
    role_registry: required
    budget_transparency: required
    conflict_case_tracker: required_privacy_limited
    anti_capture_monitor: required

  gates:
    asset_lock_gate: required
    membership_rights_gate: required
    decision_domain_gate: required
    role_capture_gate: required
    finance_gate: required
    conflict_gate: required
    data_privacy_gate: required
    governance_burden_gate: required
    legitimacy_gate: required
```

---

## 30. Design Maxims

```text
Do not make a founder the constitution.

Do not let land become the new landlord.

Do not let investors control the floor.

Do not let friendship replace due process.

Do not let consensus eat daily life.

Do not let emergency powers linger.

Do not make conflict resolution a substitute for protection.

Do not treat transparency and privacy as opposites.

Do not let one person control money, records, and conflict process.

Do not let professional experts become unreviewable rulers.

Do not hide debt.

Do not hide reserves.

Do not hide maintenance backlog.

Do not hide role concentration.

Govern the commons, not the soul.

Attach power to roles, not personalities.

Make dangerous decisions slow.

Make ordinary decisions light.

Make emergency decisions fast and temporary.

Protect assets from capture.

Protect people from coercion.

Keep the floor outside the wealth game.
```

---

## 31. Open Questions for Iteration

```text
1. Should the default legal model be CLT-like land ownership plus limited-equity cooperative occupancy, or should the app support multiple selectable legal profiles from the start?
2. What supermajority threshold should apply to constitutional decisions: 67%, 75%, or higher?
3. Should resident membership be one adult resident one vote, one household one vote, or weighted by another principle?
4. How should children, elders, disabled residents, and non-voting dependents be represented in governance?
5. Should nonresident supporters have any formal rights, or only advisory roles?
6. What maximum governance burden per resident is acceptable?
7. Should operational circles use consent decision-making by default, or simpler delegated authority with review?
8. What decisions must always trigger external legal review?
9. Should the app treat debt above a threshold as an automatic warning or failure?
10. How should expulsion or loss of occupancy be handled without reproducing punitive housing insecurity?
11. What conflict cases are appropriate for restorative processes, and what cases must bypass them for safety?
12. How should the system prevent informal popularity, charisma, or social dominance from becoming shadow governance?
13. Should paid roles be allowed, and if so, how are they prevented from becoming a managerial class?
14. What governance failure would make the entire CIaC model morally invalid?
```

---

## 32. Source Notes

The research basis for this draft includes:

- Elinor Ostrom's design principles for enduring commons governance.
- Community land trust stewardship, ground lease, and resale-formula precedents.
- Cooperative governance principles, especially member ownership and democratic control.
- Sociocracy and consent-based circle governance patterns.
- Nonprofit/public-benefit asset-lock and dissolution concepts.
- Restorative justice and circle-process approaches to conflict and harm repair.
- FEMA whole-community resilience and emergency-management principles.
- Housing cooperative, land-trust, and community-governance practices that separate ownership, use rights, stewardship, and resident participation.
