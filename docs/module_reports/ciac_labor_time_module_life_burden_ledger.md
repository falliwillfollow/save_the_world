# CIaC Labor & Time Module: Life Burden Ledger

**Module ID:** `labor_time.life_burden_ledger.v0_1`  
**Status:** Draft requirement module  
**Purpose:** Define the labor, time, fairness, and life-burden accounting system for a scalable Minimum Viable Dignified Infrastructure complex.  
**Primary design question:** Does the CIaC system actually return life to people, or does it merely replace wage labor, rent extraction, and institutional bureaucracy with commons labor, meetings, invisible care work, and maintenance anxiety?

---

## 1. Core Thesis

The CIaC labor baseline should **not** be “everyone contributes vaguely.”

Vague contribution models hide labor, reward charismatic avoidance, overburden conscientious residents, reproduce gendered care work, and make the civic floor dependent on guilt.

The recommended baseline is a **Life Burden Ledger**:

```text
total life burden accounting
+ required labor budgets
+ paid work / commons work distinction
+ care labor visibility
+ maintenance labor visibility
+ governance burden limits
+ role rotation
+ role backup
+ skill tracking
+ burnout detection
+ opt-in contribution pathways
+ substitution and accommodation rules
+ free-time protection
+ passion-time measurement
+ fairness audits
+ life-burden reduction scoring
```

The goal is not to make everyone do the same amount of work.

The goal is to make the required work visible, finite, fair, dignified, and genuinely lower than the burden of conventional survival.

---

## 2. Guiding Sentence

> The system succeeds only if it returns time, reduces coercion, and makes necessary work feel meaningful, bounded, and fairly shared.

---

## 3. Strategic Decision

The best default model is:

# A total-life-burden accounting system, not a simple chores chart.

```yaml
labor_time_strategy:
  measure:
    - required_wage_labor
    - commons_labor
    - care_labor
    - household_labor
    - maintenance_labor
    - governance_labor
    - commute_and_transport_labor
    - survival_admin
    - emotional_recovery_time
    - free_time
    - passion_time
    - rest_time
    - social_time
    - nature_time

  optimize_for:
    - lower_required_cashflow
    - lower_required_wage_hours
    - lower_total_compulsory_labor
    - lower_invisible_labor
    - lower_meeting_burden
    - lower_burnout_risk
    - higher_free_time
    - higher_unstructured_time
    - higher_passion_time
    - higher_dignity
    - higher_resilience_under_bad_weeks

  avoid_as_default:
    - equal_hours_as_false_fairness
    - unpaid_care_labor_invisibility
    - volunteerism_as_infrastructure
    - guilt_based_contribution
    - meetings_as_default_governance
    - work_credits_that_become_social_credit
    - punishing_disability_or_illness
    - requiring_all_residents_to_be_generalists
    - hiding_labor_inside_automation
```

### Rationale

CIaC exists because modern life extracts time through rent, debt, commuting, fragmented errands, duplicated domestic infrastructure, administrative complexity, status competition, and wage dependency.

A successful alternative must prove that the burden has been removed, not merely relocated.

---

## 4. Research Anchors

This module is grounded in the following research and precedent categories.

### 4.1 Time-use measurement

The U.S. Bureau of Labor Statistics American Time Use Survey measures how people spend time working, doing household activities, providing care, and engaging in leisure and sports. It is the correct type of empirical baseline for comparing conventional life against CIaC life.

**Design implication:** The app should use time-use categories, not only money, to evaluate whether the system improves life.

### 4.2 Work-life balance

OECD work-life balance indicators emphasize that long working hours reduce time available for leisure, personal care, social relationships, and wellbeing.

**Design implication:** CIaC should track leisure, personal care, and social time as serious infrastructure outcomes, not leftovers.

### 4.3 Long working hours and health

WHO and ILO estimate that long working hours, defined as 55 or more hours per week, are associated with major disease burdens from stroke and ischemic heart disease.

**Design implication:** The app should treat high required labor as a health and dignity risk, not a badge of honor.

### 4.4 Shorter working week trials

Large four-day-week pilots have reported reductions in stress and burnout while many participating employers continued the policy.

**Design implication:** The project should not assume that reduced work time necessarily means lower functioning. It should test whether redesigned systems can preserve output while returning time.

### 4.5 Unpaid care and domestic labor

Time-use surveys consistently show care and household work are real labor, often distributed unequally.

**Design implication:** Care, cleaning, food, domestic work, emotional labor, and coordination must be counted or the model will reproduce the burden it claims to remove.

### 4.6 Burnout and psychosocial risk

Occupational health frameworks treat excessive demands, low control, poor support, and long working hours as stressors.

**Design implication:** The app should measure time burden, control, predictability, support, recovery, and fairness, not just total hours.

---

## 5. Recommended Scale

The labor and time module should support the same first serious population as the physical and governance modules.

```yaml
population:
  minimum_meaningful_scale: 50
  ideal_first_model: 80
  upper_bound_before_replication: 150
```

### Scale Logic

```text
Below 50:
  labor is too personal. A few motivated people can carry the system invisibly.

Around 80:
  role rotation, skill coverage, paid/volunteer distinction, care backup, and fair scheduling become realistic.

Above 150:
  labor accounting may require formal staffing, payroll, stronger HR-like policies, privacy controls, and federation-level coordination.
```

### Scaling Method

Labor should scale by village block cells, not by endlessly growing shared obligations.

```yaml
scaling:
  50-100_residents:
    labor_ledger: required
    contribution_paths: 3-5
    role_backup: required
    burnout_monitoring: required

  100-150_residents:
    labor_ledger: required
    paid_part_time_operations_roles: preferred
    role_specialization: higher
    fairness_audit: required

  above_150_residents:
    recommendation: replicate_village_block_or_formalize_workforce_system
```

---

## 6. Default Prototype

```yaml
default_prototype:
  name: life_burden_ledger_80
  residents: 80

  baseline_comparisons:
    - conventional_renter_life
    - conventional_homeowner_life
    - CIaC_resident_life
    - bad_week_CIaC_life
    - illness_or_care_week_CIaC_life

  tracked_labor_domains:
    - wage_labor
    - commons_operations
    - food
    - water
    - sanitation_waste
    - energy
    - maintenance_repair
    - care_health
    - governance
    - household_private_labor
    - transportation
    - survival_admin
    - emergency_response

  protected_time_domains:
    - sleep
    - personal_care
    - unstructured_free_time
    - passion_time
    - social_time
    - nature_time
    - learning_time
    - rest_recovery_time
    - family_or_intimate_time

  targets:
    required_wage_hours_reduction: 25-50_percent_vs_conventional_baseline
    total_compulsory_labor_target: lower_than_conventional_baseline
    commons_labor_target: 4-10_hours_per_resident_per_week
    governance_labor_target: 1-3_hours_per_resident_per_month
    maintenance_labor_target: 1-3_hours_per_resident_per_month
    free_time_increase: required
    burnout_risk: low_or_managed
```

---

## 7. Labor Categories

The app should distinguish labor types rather than collapsing them into “work.”

```yaml
labor_categories:
  required_wage_labor:
    definition: paid external work needed to cover cash obligations
    examples:
      - employment
      - contracting
      - business_income_generation
    design_goal: reduce_required_hours_not_eliminate_optional_ambition

  commons_labor:
    definition: work required to keep shared survival and dignity infrastructure operating
    examples:
      - food_commons
      - water_checks
      - cleaning
      - maintenance
      - care_support
      - governance
    design_goal: finite_visible_fair

  private_household_labor:
    definition: personal or household work not collectivized
    examples:
      - private_meals
      - personal_cleaning
      - laundry_if_private
      - personal_admin
    design_goal: reduce_duplication_without_destroying_autonomy

  care_labor:
    definition: support for children, elders, disabled residents, sick residents, injured residents, grieving residents, or overwhelmed residents
    examples:
      - care_meals
      - check_ins
      - transport_to_care
      - hygiene_support
      - emotional_support
    design_goal: count_it_protect_it_distribute_it

  coordination_labor:
    definition: planning, scheduling, recordkeeping, meetings, conflict work, communication
    examples:
      - governance_meetings
      - role_scheduling
      - budget_review
      - conflict_process
      - documentation
    design_goal: minimize_and_automate_where_safe

  emergency_labor:
    definition: surge labor during outages, illness waves, disasters, failures, or conflict
    examples:
      - water_distribution
      - emergency_food
      - storm_cleanup
      - outage_response
      - care_surge
    design_goal: rare_planned_and_recovered_from

  passion_labor:
    definition: freely chosen creative, craft, intellectual, entrepreneurial, artistic, exploratory, or service work
    examples:
      - art
      - music
      - gardening_for_joy
      - research
      - teaching
      - small_business
      - craft
    design_goal: increase_without_turning_into_obligation
```

### Labor Principle

```text
Not all work is the enemy. Coerced, hidden, meaningless, or extractive work is the enemy.
```

---

## 8. The Life Burden Equation

The app should calculate a total life-burden score.

```yaml
LifeBurdenScore:
  positive_burdens:
    required_wage_hours: high_weight
    commute_hours: medium_high_weight
    commons_required_labor_hours: medium_weight
    care_labor_hours: context_sensitive_weight
    household_labor_hours: medium_weight
    governance_hours: medium_high_weight
    survival_admin_hours: medium_weight
    emergency_labor_hours: high_weight
    cognitive_overhead: high_weight
    unpredictability: high_weight
    burnout_risk: high_weight
    cashflow_fragility: high_weight
    debt_pressure: high_weight
    role_unfairness: high_weight
    lack_of_recovery_time: high_weight

  relief_factors:
    free_time: high_weight
    passion_time: high_weight
    sleep_and_recovery: high_weight
    nature_time: medium_weight
    social_belonging_time: medium_weight
    autonomy: high_weight
    predictability: high_weight
    role_choice: medium_high_weight
    care_availability: high_weight
    low_recurring_costs: high_weight
    resilience_buffer: high_weight

  output:
    lower_is_better: true
    compare_against:
      - conventional_life_baseline
      - CIaC_normal_week
      - CIaC_bad_week
      - CIaC_growth_scenario
```

### Equation Principle

```text
A system that lowers costs by increasing invisible labor has not lowered life burden.
```

---

## 9. The Week Model

The core unit of proof should be the week.

```yaml
week_model:
  time_budget_hours: 168

  required_categories:
    sleep:
      target_range: 49-63_hours_per_week
      note: 7-9_hours_per_day_reference_range

    personal_care:
      includes:
        - hygiene
        - eating
        - medical_needs
        - recovery

    required_wage_labor:
      includes:
        - paid_work
        - unpaid_required_work_for_income
        - job_search_if_needed

    commute_transport:
      includes:
        - commute
        - care_trips
        - food_errands
        - administrative_trips

    commons_labor:
      includes:
        - food
        - cleaning
        - maintenance
        - care
        - governance
        - emergency_preparedness

    household_private_labor:
      includes:
        - private_cleaning
        - private_food
        - private_laundry
        - personal_admin

    care_labor:
      includes:
        - care_for_others
        - care_coordination
        - emotional_support
        - transport_to_care

    governance:
      includes:
        - meetings
        - circle_work
        - records
        - conflict_process

    free_time:
      includes:
        - leisure
        - unstructured_rest
        - social_time
        - nature_time

    passion_time:
      includes:
        - art
        - music
        - craft
        - study
        - exploration
        - voluntary_enterprise

  required_outputs:
    - weekly_time_budget
    - compulsory_hours_total
    - optional_hours_total
    - free_time_total
    - passion_time_total
    - recovery_time_total
    - unpredictability_score
    - burden_distribution
    - comparison_to_baseline
```

### Week Principle

```text
If the system cannot improve a normal week and protect a bad week, it has not proven the vision.
```

---

## 10. Required vs Optional Contribution

The app should clearly separate required contribution from voluntary work.

```yaml
contribution_types:
  required_floor_contribution:
    definition: minimum contribution needed to keep commons operating
    examples:
      - routine cleaning
      - basic food shift
      - maintenance inspection
      - governance minimum
      - emergency drill
    constraints:
      - bounded
      - scheduled
      - fair
      - substitutable
      - accommodated_for_disability_or_illness
      - never_open_ended

  elective_commons_contribution:
    definition: useful but not required contribution
    examples:
      - extra garden work
      - teaching
      - art events
      - workshop projects
      - optional care support
    constraints:
      - voluntary
      - credited_or_appreciated
      - not_allowed_to_mask_understaffing

  paid_internal_work:
    definition: work paid by the commons because it exceeds fair resident contribution
    examples:
      - facilities coordination
      - food operations
      - bookkeeping
      - specialized maintenance
      - care coordination
    constraints:
      - transparent
      - accountable
      - no_managerial_capture
      - fair_compensation

  external_wage_work:
    definition: work residents choose or need outside the commons
    examples:
      - jobs
      - contracting
      - businesses
    constraints:
      - not_required_to_access_survival_floor_beyond_agreed_costs
```

### Contribution Principle

```text
The commons must know the difference between contribution, calling, and exploitation.
```

---

## 11. Fairness Model

Fairness does not mean identical work for every resident.

```yaml
fairness_model:
  fairness_dimensions:
    time:
      question: are_required_hours_reasonably_distributed

    intensity:
      question: are_dirty_difficult_or_emotional_tasks_fairly_distributed_or_compensated

    flexibility:
      question: can_people_choose_roles_that_fit_ability_schedule_and_dignity

    capacity:
      question: are_disability_illness_age_childcare_and_caregiving_realities_accounted_for

    skill:
      question: are_specialized_skills_recognized_without_creating_power_capture

    benefit:
      question: do_people_who_benefit_more_contribute_fairly_without_punitive_means_testing

    choice:
      question: are_there_multiple_valid_contribution_paths

  avoid:
    - strict_equal_hours_that_punish_disability
    - invisible_care_work
    - charismatic_free_riding
    - technical_expert_capture
    - gendered_default_roles
    - seniority_as_unaccountable_power
```

### Fairness Principle

```text
Equal hours can be unfair. Invisible labor is always unfair.
```

---

## 12. Contribution Pathways

Residents should have multiple ways to contribute.

```yaml
contribution_pathways:
  operations_path:
    examples:
      - food_shift
      - cleaning
      - pantry
      - water_check
      - waste_sorting
      - maintenance_inspection
    suited_for:
      - predictable_task_preference
      - hands_on_work

  care_path:
    examples:
      - care_meals
      - check_ins
      - transport_to_care
      - elder_support
      - childcare_support_if_module_exists
    suited_for:
      - relational_work
      - flexible_availability
    safeguards:
      - labor_counted
      - consent_required
      - burnout_monitoring

  technical_path:
    examples:
      - energy_dashboard
      - water_testing_schedule
      - asset_registry
      - tool_maintenance
      - data_exports
    safeguards:
      - no_single_person_dependency
      - plain_language_docs
      - backup_role

  governance_path:
    examples:
      - facilitation
      - records
      - budget_review
      - policy_review
      - conflict_support
    safeguards:
      - meeting_burden_limits
      - role_rotation
      - authority_limits

  creative_cultural_path:
    examples:
      - art
      - events
      - education
      - music
      - public_space_care
    safeguards:
      - not_substitute_for_survival_labor_unless_agreed
      - voluntary
      - no_status_hierarchy

  financial_path:
    examples:
      - higher_assessment
      - funding_support
      - paying_for_internal_services
    safeguards:
      - cannot_buy_governance_control
      - cannot_replace_minimum_social_obligation_entirely_without_policy
```

### Pathway Principle

```text
A dignified system should let people contribute from strength without abandoning shared responsibility.
```

---

## 13. Role Rotation and Backup

Role rotation prevents capture and burnout, but rotation must not destroy competence.

```yaml
role_rotation:
  required:
    - role_term
    - backup_role
    - onboarding_docs
    - shadow_period
    - exit_notes
    - review_date
    - burnout_check
    - skill_requirements
    - professional_boundary

  rotation_types:
    short_cycle:
      use_for:
        - cleaning
        - meal_cleanup
        - routine shifts
      term: weekly_or_monthly

    medium_cycle:
      use_for:
        - pantry_steward
        - garden_steward
        - tool_library
        - records
      term: 3-12_months

    long_cycle:
      use_for:
        - finance
        - maintenance
        - care_coordination
        - energy
        - water
      term: 6-24_months_with_review

    professional_or_paid_role:
      use_for:
        - high_skill_or_high_liability_work
      term: contract_or_employment_period_with_accountability

  avoid:
    - rotating_too_fast_for_critical_competence
    - permanent_unreviewed_roles
    - no_backup
    - role_identity_fusion
```

### Rotation Principle

```text
Rotate power faster than competence, but not so fast that safety collapses.
```

---

## 14. Burnout and Overload Detection

Burnout is a system signal, not a personal failure.

```yaml
burnout_detection:
  risk_indicators:
    - repeated_overassignment
    - same_people_covering_emergencies
    - high_unfilled_tasks
    - rising_conflict
    - missed_maintenance
    - care_labor_concentration
    - declining_participation
    - increased_meeting_length
    - reduced_free_time
    - frequent_last_minute_requests
    - resident_feedback_of_exhaustion

  required_outputs:
    - burnout_risk_by_domain
    - labor_concentration_report
    - emergency_labor_report
    - unfilled_work_report
    - recommendations:
        - reduce_scope
        - hire_or_pay_internal_role
        - simplify_system
        - pause_optional_projects
        - redistribute_roles
        - adjust expectations
        - activate_respite
```

### Burnout Principle

```text
When a system burns out its best people, the design is failing.
```

---

## 15. Labor Credits and Cautions

Labor credits may help fairness, but they can become coercive social currency.

```yaml
labor_credit_system:
  default_status: optional_cautious

  allowed_uses:
    - track_contribution_balance
    - identify_overload
    - compensate_extra_work
    - support_role_rotation
    - make_hidden_work_visible

  prohibited_uses:
    - ranking_resident_worth
    - denying_core_survival_access_without_due_process
    - public_shaming
    - punishing_disability
    - forcing_health_disclosure
    - creating_black_market_power
    - replacing_human_judgment

  alternatives:
    - contribution_bands
    - role_commitments
    - time_budgets
    - paid_internal_roles
    - hardship_accommodation
    - periodic_fairness_review
```

### Credit Principle

```text
Track labor to protect people, not to score them.
```

---

## 16. Substitution, Accommodation, and Hardship

A humane system must handle unequal capacity.

```yaml
substitution_accommodation:
  required:
    - illness_pause
    - disability_accommodation
    - elder_adjustment
    - temporary_caregiving_adjustment
    - grief_or_crisis_adjustment
    - role_substitution
    - paid_substitution_option_where_allowed
    - makeup_not_required_for_all_hardship
    - confidential_request_process
    - review_without_shame

  examples:
    - resident_with_mobility_limit_does_records_instead_of_cleaning
    - sick_resident_receives_care_meals_and_is_not_penalized
    - high_income_low_time_resident_pays_into_paid_ops_role_with_member_policy
    - skilled_electrician_resident_advises_but_licensed_work_still_professionally_controlled
    - elder_resident_contributes_to_history_education_child_support_or_culture_not_heavy_labor
```

### Accommodation Principle

```text
The commons must not become survival of the most able-bodied and available.
```

---

## 17. Time Sovereignty and Protected Time

The purpose of the project is not only fewer hours. It is more sovereignty over time.

```yaml
protected_time:
  required_categories:
    sleep:
      protection: high

    recovery:
      protection: high

    unstructured_free_time:
      protection: high

    passion_time:
      protection: high

    social_belonging:
      protection: medium_high

    nature_time:
      protection: medium_high

    learning_time:
      protection: medium

  protected_time_rules:
    - no_recurring_required_meetings_above_target_without_review
    - emergency_after_action_recovery_time_required
    - optional_projects_must_not_consume_floor_labor
    - passion_time_cannot_be_reclassified_as_commons_obligation_without_consent
    - quiet_hours_protected
    - resident_off_time_respected

  app_outputs:
    - protected_time_report
    - passion_time_report
    - free_time_trend
    - recovery_deficit_warning
```

### Time Sovereignty Principle

```text
Free time is not empty time. It is where a life becomes one's own.
```

---

## 18. Wage Dependency Reduction

The module must show whether CIaC reduces required cashflow and therefore required wage hours.

```yaml
wage_dependency_model:
  inputs:
    - monthly_housing_cost
    - food_cost
    - utilities
    - transportation
    - healthcare_out_of_pocket
    - debt
    - insurance
    - taxes_or_assessments
    - commons_fees
    - savings_reserve
    - personal_discretionary_needs

  outputs:
    - monthly_cash_required
    - required_wage_hours_at_income_levels
    - required_wage_hours_at_local_wages
    - hours_reduced_vs_conventional_baseline
    - wage_dependency_score
    - cashflow_fragility_score

  comparisons:
    - conventional_rent_path
    - conventional_homeownership_path
    - CIaC_resident_path
    - CIaC_bad_year_path
```

### Wage Dependency Principle

```text
The system returns life partly by reducing how much money a person must earn just to remain safe.
```

---

## 19. Bad Week / Bad Year Modeling

The system must protect time and dignity under stress.

```yaml
bad_week_model:
  scenarios:
    - resident_illness
    - injury
    - care_responsibility_surge
    - power_outage
    - crop_failure
    - water_shortage
    - conflict_case
    - job_loss
    - maintenance_emergency
    - family_crisis

  required_outputs:
    - extra_labor_hours
    - who_absorbs_extra_labor
    - free_time_loss
    - sleep_loss
    - cashflow_impact
    - care_support_activated
    - role_backup_status
    - recovery_period
    - dignity_status

  pass_condition:
    - bad_week_does_not_destroy_floor
    - labor_surge_is_distributed_or_paid
    - affected_resident_not_punished_for_vulnerability
    - recovery_time_is_scheduled
```

### Bad Week Principle

```text
The alternative is real only if a bad week does not throw a person back into the extraction machine.
```

---

## 20. Interfaces With Other Modules

### 20.1 Housing Interface

```yaml
housing_labor_interface:
  required:
    - private_unit_maintenance_burden
    - common_space_cleaning
    - noise_conflict_time_cost
    - commute_reduction
    - shared_space_scheduling
    - move_in_move_out_labor
```

```text
Housing design should reduce daily friction and duplicated private labor.
```

### 20.2 Food Interface

```yaml
food_labor_interface:
  required:
    - cooking_labor
    - cleanup_labor
    - garden_labor
    - procurement_labor
    - preservation_labor
    - care_meal_labor
    - food_safety_logging
```

```text
Food savings are false if they come from hidden unpaid kitchen and garden labor.
```

### 20.3 Water Interface

```yaml
water_labor_interface:
  required:
    - testing_labor
    - maintenance_labor
    - drought_response_labor
    - emergency_distribution_labor
    - monitoring_labor
```

```text
Water resilience must not require residents to constantly worry about water.
```

### 20.4 Sanitation Interface

```yaml
sanitation_labor_interface:
  required:
    - cleaning_labor
    - waste_sorting_labor
    - organics_labor
    - hazardous_waste_labor
    - emergency_sanitation_labor
```

```text
Sanitation labor must be visible because it is easy to hide and hard to dignify.
```

### 20.5 Energy Interface

```yaml
energy_labor_interface:
  required:
    - monitoring_labor
    - maintenance_labor
    - outage_response_labor
    - generator_fuel_labor_if_present
    - seasonal_preparation
```

```text
Energy automation should reduce anxiety, not create dashboards residents must babysit.
```

### 20.6 Care Interface

```yaml
care_labor_interface:
  required:
    - check_ins
    - care_meals
    - transport_to_care
    - medication_pickup
    - illness_support
    - caregiver_respite
    - emotional_support
```

```text
Care is labor even when it is loving.
```

### 20.7 Maintenance Interface

```yaml
maintenance_labor_interface:
  required:
    - routine_maintenance
    - corrective_repairs
    - emergency_repairs
    - tool_library
    - spare_parts
    - contractor_coordination
```

```text
Maintenance is where hidden labor becomes system decay.
```

### 20.8 Governance Interface

```yaml
governance_labor_interface:
  required:
    - meetings
    - facilitation
    - records
    - conflict_process
    - budget_review
    - onboarding
    - policy_review
```

```text
Governance is necessary, but meeting burden must never become the new rent.
```

---

## 21. Automation-Favoring Requirements

Automation should make time visible, reduce scheduling burden, and prevent hidden labor.

```yaml
automation_requirements:
  time_ledger:
    required: true
    purpose:
      - track_required_labor
      - track_free_time
      - compare_baselines
      - expose_hidden_labor

  role_scheduler:
    required: true
    purpose:
      - distribute_tasks
      - avoid_overassignment
      - respect_availability
      - support_accommodations
      - track_backup_roles

  labor_fairness_dashboard:
    required: true
    purpose:
      - identify_concentration
      - detect_gender_or_role_imbalance
      - show_unfilled_tasks
      - flag_burnout_risk

  protected_time_dashboard:
    required: true
    purpose:
      - show_free_time
      - show_recovery_deficits
      - show_passion_time
      - compare_to_baseline

  wage_dependency_calculator:
    required: true
    purpose:
      - calculate_required_cashflow
      - calculate_required_wage_hours
      - compare_conventional_and_CIaC_life

  bad_week_simulator:
    required: true
    purpose:
      - simulate_labor_surges
      - show_who_absorbs_burden
      - detect_floor_failure

  meeting_limiter:
    required: true
    purpose:
      - track_governance_hours
      - warn_when_meeting_burden_exceeds_targets
      - force_review_of_process_bloat

  avoid:
    - social_credit_system
    - public_shaming_dashboard
    - productivity_surveillance
    - mandatory_wearables
    - AI_assigning_labor_without_appeal
    - health_or_disability_inference
    - optimizing_for_hours_without_dignity
```

### Automation Principle

```text
Automate memory, fairness detection, scheduling, and comparison. Do not automate coercion.
```

---

## 22. Labor & Time Roles

```yaml
labor_time_roles:
  labor_time_steward:
    purpose: maintain labor ledger and time-burden reports
    required_backup: true

  fairness_steward:
    purpose: detect imbalance, hidden labor, concentration, and accommodations
    required_backup: true

  scheduling_steward:
    purpose: coordinate recurring required tasks and role backups
    required_backup: true

  burnout_steward:
    purpose: monitor overload, recovery deficits, and repeated emergency burden
    required_backup: true

  accommodation_steward:
    purpose: confidentially support illness, disability, caregiving, and hardship adjustments
    required_backup: true
    privacy_limited: true

  wage_dependency_steward:
    purpose: compare cashflow and required wage hours against baseline
    required_backup: true

  protected_time_steward:
    purpose: defend free time, passion time, quiet hours, and meeting limits
    required_backup: true
```

### Role Rule

```text
No one should have to personally argue that their exhaustion is real. The ledger should make overload visible.
```

---

## 23. Scenario Simulations

The labor and time module must support stress simulations.

```yaml
labor_time_scenarios:
  normal_week:
    tests:
      - required_wage_hours
      - commons_labor
      - private_labor
      - free_time
      - passion_time
      - sleep_and_recovery
      - fairness_distribution

  conventional_baseline_week:
    tests:
      - rent_or_mortgage_cashflow
      - commute
      - errands
      - household_duplication
      - required_wage_hours
      - free_time
      - recovery_deficit

  CIaC_normal_week:
    tests:
      - lower_cashflow
      - commons_labor
      - shared_food_labor
      - governance_burden
      - maintenance_burden
      - free_time_gain

  illness_week:
    tests:
      - affected_resident_work_reduction
      - care_meals
      - role_backup
      - care_labor_distribution
      - recovery_time

  job_loss_month:
    tests:
      - cashflow_buffer
      - required_wage_dependency
      - food_housing_security
      - community_support
      - role_adjustment

  bad_infrastructure_week:
    tests:
      - maintenance_emergency
      - emergency_labor_distribution
      - sleep_loss
      - free_time_loss
      - professional_support

  governance_conflict_month:
    tests:
      - meeting_burden
      - conflict_labor
      - emotional_labor
      - core_operations_continuity

  growth_scenario:
    tests:
      - labor_scaling
      - role_count
      - meeting_burden
      - care_load
      - maintenance_load
      - need_for_paid_roles

  founder_or_expert_exit:
    tests:
      - knowledge_loss
      - backup_roles
      - labor_surge
      - free_time_impact
      - system_continuity
```

---

## 24. Labor & Time Gates

The app should fail or warn based on life-burden performance.

```yaml
labor_time_gates:
  life_return_gate:
    fail_if:
      - CIaC_total_compulsory_labor_exceeds_conventional_baseline_without_resilience_gain
      - free_time_not_increased
      - passion_time_not_increased_or_protected
      - required_wage_hours_not_reduced

    warn_if:
      - gains_depend_on_unverified_cost_assumptions
      - free_time_increase_erased_in_bad_week
      - only_high_income_residents_benefit

  hidden_labor_gate:
    fail_if:
      - care_labor_untracked
      - cleaning_labor_untracked
      - governance_labor_untracked
      - maintenance_labor_untracked
      - food_labor_untracked

    warn_if:
      - emotional_labor_untracked
      - scheduling_labor_untracked
      - conflict_labor_untracked

  burnout_gate:
    fail_if:
      - same_small_group_handles_most_critical_labor
      - burnout_risk_high_without_intervention
      - emergency_labor_repeatedly_unrecovered
      - protected_time_deficit_persists

    warn_if:
      - labor_concentration_score_rising
      - unfilled_tasks_growing
      - role_backups_missing

  fairness_gate:
    fail_if:
      - contribution_model_punishes_disability_or_illness
      - no_accommodation_process
      - labor_credits_control_survival_access_without_due_process
      - unpaid_care_labor_concentrated_by_gender_or_status

    warn_if:
      - equal_hours_policy_ignores_capacity
      - specialized_skills_create_power_capture
      - charismatic_free_riding_detected

  governance_burden_gate:
    fail_if:
      - governance_hours_per_resident_above_8_per_month_by_default
      - routine_decisions_require_full_group_meetings
      - conflict_process_consumes_core_operations

    warn_if:
      - governance_hours_above_5_per_month
      - meeting_hours_above_target
      - policy_review_backlog_growing

  commons_labor_gate:
    fail_if:
      - required_commons_labor_above_12_hours_per_resident_per_week_by_default
      - no_paid_or_specialized_role_for_high_burden_operations
      - emergency_labor_plan_missing

    warn_if:
      - required_commons_labor_above_10_hours_per_week
      - common_meals_or_gardens_require_hidden_work

  wage_dependency_gate:
    fail_if:
      - monthly_cash_required_not_lower_than_conventional_baseline
      - housing_food_energy_savings_unproven
      - reserve_or_assessment_burden_recreates_rent_pressure

    warn_if:
      - savings_depend_on_unpaid_labor
      - bad_year_assessment_spike_likely
      - health_or_transport_costs_unmodeled

  protected_time_gate:
    fail_if:
      - sleep_recovery_regularly_below_safe_target
      - no_unstructured_free_time
      - passion_time_absorbed_by_required_commons_work
      - quiet_hours_not_protected

    warn_if:
      - protected_time_declines_for_3_consecutive_periods
      - optional_projects_consuming_required_labor_capacity
```

---

## 25. App Modeling Boundary

The app should model labor and time at the level of **required work, cashflow, fairness, protected time, role distribution, and stress scenarios**, not personal productivity optimization.

### The App Should Model

```text
weekly time budgets
monthly required cashflow
required wage hours
commons labor
private household labor
care labor
maintenance labor
governance labor
emergency labor
free time
passion time
role distribution
burnout risk
fairness
accommodations
bad week scenarios
life-burden comparison
```

### The App Should Not Claim to Solve by Default

```text
individual therapy
employment law
wage and hour compliance
tax treatment of internal labor
clinical burnout diagnosis
personal productivity coaching
surveillance of residents
disability determination
caregiver qualification
HR compliance
labor union law
benefits administration
```

### Principle

```text
The app should identify whether the system returns life, hides labor, creates overload, or shifts burden onto vulnerable people.
```

---

## 26. Required Data Model

```yaml
LaborTimeCommons:
  id: string
  population_served: integer

  weekly_time_budget:
    time_budget_hours: 168
    sleep_hours: number
    personal_care_hours: number
    required_wage_labor_hours: number
    commute_transport_hours: number
    commons_labor_hours: number
    private_household_labor_hours: number
    care_labor_hours: number
    governance_hours: number
    survival_admin_hours: number
    free_time_hours: number
    passion_time_hours: number
    recovery_time_hours: number

  cashflow:
    monthly_cash_required: number
    required_wage_hours_at_local_wage: number
    required_wage_hours_at_resident_income: number
    conventional_baseline_cash_required: number
    conventional_baseline_required_wage_hours: number
    wage_dependency_reduction_percent: number

  labor_distribution:
    residents_active_in_labor_pool: integer
    required_commons_hours_total: number
    required_commons_hours_per_resident: number
    labor_concentration_score: number
    care_labor_concentration_score: number
    dirty_or_unpleasant_labor_distribution_score: number
    gender_or_role_imbalance_flag: boolean
    unfilled_required_hours: number

  roles:
    critical_roles_total: integer
    critical_roles_with_backup_percent: number
    roles_overdue_for_rotation: integer
    paid_internal_roles_total: integer
    volunteer_roles_total: integer
    accommodation_requests_active: integer

  protected_time:
    free_time_increase_vs_baseline: number
    passion_time_increase_vs_baseline: number
    recovery_deficit_hours: number
    quiet_hours_protected: boolean
    meeting_burden_status: pass | warn | fail

  burnout:
    burnout_risk: low | medium | high
    overloaded_resident_count: integer
    repeated_emergency_labor_count: integer
    same_group_labor_dependency_score: number

  automation:
    time_ledger: boolean
    role_scheduler: boolean
    labor_fairness_dashboard: boolean
    protected_time_dashboard: boolean
    wage_dependency_calculator: boolean
    bad_week_simulator: boolean
    meeting_limiter: boolean

  outputs:
    life_burden_status: pass | warn | fail
    life_burden_score: number
    life_burden_reduction_score: number
    fairness_status: pass | warn | fail
    burnout_status: pass | warn | fail
    hidden_labor_status: pass | warn | fail
    protected_time_status: pass | warn | fail
    complexity_score: number
```

---

## 27. Required App Outputs

```yaml
required_outputs:
  - life_burden_summary
  - conventional_baseline_comparison
  - weekly_time_budget_report
  - required_wage_hours_report
  - commons_labor_report
  - hidden_labor_report
  - care_labor_report
  - governance_burden_report
  - maintenance_labor_report
  - protected_time_report
  - passion_time_report
  - fairness_distribution_report
  - burnout_risk_report
  - role_rotation_and_backup_report
  - accommodation_report_privacy_limited
  - bad_week_scenario_report
  - growth_labor_scaling_report
  - life_burden_reduction_score
  - visualization_bundle_metadata
```

---

## 28. Visualization Requirements

The labor and time module should export enough data for a dashboard or virtual world to show where life is being returned or extracted.

```yaml
visualization_requirements:
  chart_objects:
    - weekly_time_budget
    - conventional_vs_CIaC_comparison
    - labor_by_domain
    - free_time_trend
    - passion_time_trend
    - hidden_labor_heatmap
    - role_concentration_graph
    - burnout_risk_by_domain
    - bad_week_labor_surge
    - required_wage_hours_by_cost_scenario

  overlays:
    - labor_burden_by_module
    - role_unfilled_status
    - emergency_labor_surge
    - protected_time_loss
    - meeting_burden
    - care_labor_concentration
    - maintenance_backlog_time_cost
    - commons_labor_distribution

  scenario_playback:
    - normal_week
    - conventional_baseline_week
    - CIaC_normal_week
    - illness_week
    - job_loss_month
    - infrastructure_failure_week
    - governance_conflict_month
    - growth_scenario
```

---

## 29. Best Default Requirements Summary

```yaml
MinimumViableLaborTimeCommons:
  population:
    first_serious_model: 80
    valid_range: 50-150

  philosophy:
    return_life: true
    hidden_labor_forbidden: true
    care_labor_counted: true
    governance_burden_limited: true
    equal_hours_not_assumed_fair: true
    protected_time_required: true
    passion_time_is_real_metric: true

  targets:
    required_wage_hours_reduction: 25-50_percent_vs_conventional_baseline
    commons_labor_target: 4-10_hours_per_resident_per_week
    commons_labor_warning_above: 10_hours_per_week
    commons_labor_fail_above: 12_hours_per_week_by_default
    governance_labor_target: 1-3_hours_per_resident_per_month
    maintenance_labor_target: 1-3_hours_per_resident_per_month
    free_time_increase: required
    passion_time_increase_or_protection: required
    burnout_risk: low_or_managed

  systems:
    time_ledger: required
    role_scheduler: required
    labor_fairness_dashboard: required
    protected_time_dashboard: required
    wage_dependency_calculator: required
    bad_week_simulator: required
    meeting_limiter: required

  gates:
    life_return_gate: required
    hidden_labor_gate: required
    burnout_gate: required
    fairness_gate: required
    governance_burden_gate: required
    commons_labor_gate: required
    wage_dependency_gate: required
    protected_time_gate: required
```

---

## 30. Design Maxims

```text
Do not replace wage labor with invisible commons labor.

Do not count savings without counting the work that creates them.

Do not treat care as personality.

Do not treat maintenance as hobby.

Do not treat governance as free.

Do not treat passion time as a luxury.

Do not let the most conscientious people become the infrastructure.

Do not punish illness, disability, age, grief, or crisis.

Do not make equality of hours the only definition of fairness.

Do not use labor credits as social credit.

Do not optimize for productivity when the goal is life.

Count the whole week.

Compare against the broken world honestly.

Protect sleep.

Protect free time.

Protect passion time.

Make bad weeks survivable.

Make required work visible, finite, and meaningful.

Let optional ambition remain optional.

Return life or reject the design.
```

---

## 31. Open Questions for Iteration

```text
1. What required-wage-hour reduction is enough to prove the vision: 25%, 40%, or 50%?
2. What commons labor target is morally acceptable: 4, 6, 8, or 10 hours per resident per week?
3. Should passion time be modeled separately from leisure/free time?
4. Should internal labor be compensated, credited, rotated, or handled through contribution bands?
5. How should the app model residents with high income but low available time?
6. How should the app model residents with low cash but high available time?
7. Should the system allow financial substitution for required labor, and if so, how does it prevent class hierarchy?
8. What is the correct threshold for hiring paid internal roles?
9. How should disability and illness accommodations work without forcing disclosure?
10. Should child care and elder care be separate modules or labor categories within Care & Health?
11. Should governance burden be capped hard, or only warned?
12. What life-burden failure would make the entire CIaC design invalid?
```

---

## 32. Source Notes

The research basis for this draft includes:

- U.S. Bureau of Labor Statistics, American Time Use Survey.
- OECD work-life balance and wellbeing indicators.
- WHO / ILO research on long working hours and health burden.
- Four-day-week trial reports on reduced stress and burnout.
- Time-use and unpaid care labor research.
- Occupational health frameworks on burnout, psychosocial risk, workload, control, and recovery.
