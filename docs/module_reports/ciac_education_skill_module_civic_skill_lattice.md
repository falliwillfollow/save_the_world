# CIaC Education & Skill Module: Civic Skill Lattice

**Module ID:** `education_skill.civic_skill_lattice.v0_1`  
**Status:** Draft requirement module  
**Purpose:** Define the default education, training, onboarding, competency, knowledge-transfer, apprenticeship, and skill-resilience system for a scalable Minimum Viable Dignified Infrastructure complex.  
**Primary design question:** What learning system best gives residents enough practical competence to participate safely and meaningfully, prevents single-expert dependency, supports lifelong learning and passion, and avoids turning the community into a credential bureaucracy or unsafe amateur workshop?

---

## 1. Core Thesis

The CIaC education baseline should **not** be a school bolted onto a village.

It should be a living **Civic Skill Lattice**:

```text
role-based microlearning
+ safety-first training gates
+ apprenticeships and mentorship
+ task / knowledge / skill mapping
+ resident onboarding
+ backup-role development
+ learning by doing
+ practice logs
+ external credential paths
+ public knowledge base
+ teach-back culture
+ intergenerational learning
+ skill gap dashboards
+ professional boundary rules
+ passion learning protected from obligation
```

The goal is not to make every resident a generalist.

The goal is to make the community competent enough to operate, maintain, repair, govern, and improve the civic floor without depending on a few overburdened experts.

---

## 2. Guiding Sentence

> Teach enough for shared competence, gate enough for safety, credential only where necessary, and protect learning as a form of human flourishing.

---

## 3. Strategic Decision

The best default model is:

# A role-based skill lattice with safety gates, apprenticeships, and knowledge capture.

```yaml
education_skill_strategy:
  default_pattern:
    - role_based_micro_curricula
    - task_knowledge_skill_mapping
    - short_training_modules
    - practice_logs
    - apprentice_shadow_lead model
    - backup_role_training
    - teach_back_sessions
    - safety_gates
    - external_certification_where_required
    - resident_learning_paths
    - open_knowledge_base

  avoid_as_default:
    - everyone_must_learn_everything
    - credentialism_for_basic_participation
    - unsafe_amateurism
    - expert_capture
    - knowledge_hoarding
    - endless_training_before_useful_action
    - mandatory_ideological_education
    - hidden_training_burden
    - unpaid_apprenticeship_as_exploitation
    - AI_as_unreviewed_teacher_for_safety_critical_tasks
```

### Rationale

Every CIaC module depends on competence:

```text
Food needs food safety, inventory, cooking, gardening, and preservation competence.
Water needs testing, monitoring, maintenance, and contamination-response competence.
Sanitation needs hygiene, cleaning, waste sorting, PPE, and public-health boundary competence.
Energy needs critical-load literacy, outage procedures, and system-safety competence.
Care needs first aid, privacy, transport, illness protocol, and boundary competence.
Maintenance needs asset knowledge, tool safety, professional handoff, and documentation competence.
Governance needs facilitation, records, conflict process, finance literacy, and anti-capture competence.
```

If learning is weak, the commons decays into dependence, superstition, or burnout.

---

## 4. Research Anchors

This module is grounded in the following research and precedent categories.

### 4.1 Lifelong learning

UNESCO frames lifelong learning as continuous education, skills development, and personal growth across all stages of life.

**Design implication:** CIaC should treat learning as a lifelong civic infrastructure function, not a one-time onboarding event.

### 4.2 Inclusive learning ecosystems

UNESCO's lifelong learning work emphasizes learning ecosystems across life, in every setting, for everyone.

**Design implication:** The learning system should include residents of different ages, abilities, experience levels, schedules, and learning styles.

### 4.3 Apprenticeship

The U.S. Department of Labor describes Registered Apprenticeship as a career pathway combining paid work experience, mentorship, progressive wage increases, classroom instruction, and portable credentials.

**Design implication:** CIaC should use apprenticeship logic for internal learning: shadowing, mentored practice, structured instruction, progressive responsibility, and recognition of competence.

### 4.4 OSHA training principle

OSHA states that employers are responsible for providing required safety and health training in a manner workers can understand.

**Design implication:** CIaC training should be understandable, task-specific, documented, and matched to actual hazards. If residents are effectively workers or volunteers, legal review is required.

### 4.5 Task / Knowledge / Skill frameworks

NIST's NICE Framework provides a common language for tasks, knowledge, and skills, primarily for cybersecurity workforce planning, but the structure is transferable.

**Design implication:** CIaC should define each civic role by tasks, knowledge, skills, training, boundaries, and evidence of competence.

### 4.6 Safety training

OSHA training resources emphasize that training is tied to standards, hazards, and worker protection.

**Design implication:** Safety-critical roles should require training gates and not be assigned by enthusiasm alone.

### 4.7 Community health worker and peer-support models

Community health worker models show how trained non-clinical people can connect others to services and reduce barriers without replacing professionals.

**Design implication:** Residents can play liaison and support roles when boundaries are clear.

### 4.8 Extension, vocational, and maker education

Agricultural extension, cooperative extension, trade education, maker education, and community workshop models show the value of practical learning connected to local needs.

**Design implication:** The skill system should combine hands-on practice, local expert partnerships, and documented patterns.

---

## 5. Recommended Scale

The education and skill module should support the same first serious population as the other CIaC modules.

```yaml
population:
  minimum_meaningful_scale: 50
  ideal_first_model: 80
  upper_bound_before_replication: 150
```

### Scale Logic

```text
Below 50:
  skill coverage is fragile. One expert leaving can collapse a domain.

Around 80:
  it becomes realistic to maintain role backups, learning cohorts, peer teachers, and external training relationships.

Above 150:
  training may need formal staffing, credential partnerships, record systems, and more professionalized learning administration.
```

### Scaling Method

Use a village-block learning cell and federate specialized training across multiple blocks.

```yaml
scaling:
  50-100_residents:
    learning_node: 1
    core_skill_paths: 8-12
    backups_required_for_critical_roles: true

  100-150_residents:
    learning_node: 1_plus_specialized_tracks
    train_the_trainer_program: preferred
    external_training_partnerships: required

  above_150_residents:
    recommendation: federated_learning_network
    purpose:
      - shared_instructors
      - regional apprenticeships
      - mobile training labs
      - credential partnerships
```

---

## 6. Default Prototype

```yaml
default_prototype:
  name: civic_skill_lattice_80
  residents: 80

  facilities:
    - learning_room
    - workshop_training_area
    - tool_safety_zone
    - kitchen_training_area
    - garden_training_area
    - care_telehealth_training_room
    - digital_knowledge_base
    - documentation_station
    - skill_dashboard
    - quiet_study_space

  core_programs:
    - resident_onboarding
    - safety_orientation
    - module_role_training
    - apprentice_shadow_lead_progression
    - backup_role_training
    - first_aid_CPR_AED_path
    - food_safety_path
    - tool_safety_path
    - water_testing_path
    - sanitation_PPE_path
    - energy_outage_path
    - governance_facilitation_path
    - conflict_process_path
    - maintenance_asset_registry_path
    - teach_back_sessions
    - passion_learning_protection

  targets:
    every_resident_basic_orientation: required
    every_critical_role_has_primary_and_backup: required
    every_safety_critical_task_has_training_gate: required
    every_module_has_learning_path: required
    knowledge_base_current: required
```

---

## 7. Learning Service Levels

The app should model education as service levels.

```yaml
learning_service_levels:
  orientation_floor:
    includes:
      - rights_and_responsibilities
      - safety_basics
      - emergency_procedures
      - how_to_get_help
      - privacy_and_consent
      - common_space_use
      - reporting_problems
    dignity_status: required_for_all_residents

  participation_competence:
    includes:
      - basic_food_shift
      - cleaning_and_sanitation_basics
      - simple_maintenance_reporting
      - waste_sorting
      - water_status_awareness
      - energy_outage_behavior
      - care_request_and_support_boundary
      - governance_basics
    dignity_status: default_minimum

  role_competence:
    includes:
      - module_specific_tasks
      - checklists
      - practice
      - supervised performance
      - safety gate
      - backup role
      - documentation
    dignity_status: required_for_steward_roles

  advanced_competence:
    includes:
      - leadership
      - troubleshooting
      - training others
      - professional coordination
      - scenario response
      - improvement design
    dignity_status: preferred

  professional_or_credentialed_competence:
    includes:
      - licensed trades
      - healthcare
      - electrical
      - plumbing
      - wastewater
      - food service certification
      - OSHA or equivalent safety training
      - legal/finance/accounting
    dignity_status: external_or_formally_credentialed_domain
```

### Principle

```text
Everyone should understand the floor. Not everyone should be responsible for repairing it.
```

---

## 8. Skill Lattice Architecture

The skill lattice should be modular, role-based, and testable.

```yaml
skill_lattice:
  skill_node_fields:
    - skill_id
    - name
    - module
    - role_supported
    - task_list
    - required_knowledge
    - required_skills
    - safety_level
    - prerequisite_skills
    - training_format
    - practice_requirement
    - assessment_method
    - evidence_required
    - refresh_interval
    - professional_boundary
    - backup_role_requirement
    - documentation_link

  safety_levels:
    level_0_awareness:
      examples:
        - know_warning_signs
        - know_who_to_call
        - know_emergency_behavior
      supervision: none

    level_1_basic_participation:
      examples:
        - clean_common_space
        - sort_waste
        - help_common_meal
        - use_hand_tools
      supervision: initial_orientation

    level_2_trained_steward:
      examples:
        - pantry_inventory
        - water_sample_collection
        - tool_checkout
        - care_meal_coordination
        - basic_asset_inspection
      supervision: periodic_review

    level_3_advanced_steward:
      examples:
        - coordinate_outage_mode
        - train_others
        - manage_maintenance_backlog
        - run_food_safety_logs
        - coordinate_emergency_response
      supervision: peer_review_and_external_support

    level_4_professional_required:
      examples:
        - electrical_panel_work
        - structural_design
        - septic_repair
        - clinical_care
        - legal_documents
        - tax_filing
      supervision: licensed_or_qualified_professional
```

### Lattice Principle

```text
Skill should be represented as a network of capabilities, not a hierarchy of status.
```

---

## 9. Onboarding

Every resident should receive a simple, humane orientation.

```yaml
resident_onboarding:
  required_modules:
    - what_the_commons_is
    - rights_and_exit_rights
    - privacy_and_consent
    - emergency_procedures
    - how_to_report_a_problem
    - common_space_basics
    - food_commons_basics
    - water_and_energy_status_basics
    - sanitation_and_waste_basics
    - care_and_health_boundary_basics
    - role_contribution_options
    - conflict_process
    - safety_stop_work_authority

  format:
    - plain_language_guide
    - walk_through_tour
    - emergency_card
    - digital_reference
    - mentor_or_buddy_first_30_days
    - check_in_after_30_60_90_days

  fail_if:
    - resident_does_not_know_how_to_get_help
    - resident_does_not_understand_basic_rights
    - resident_does_not_understand_safety_reporting
    - resident_is_assigned_work_before_orientation
```

### Onboarding Principle

```text
Nobody should have to decode the commons by social osmosis.
```

---

## 10. Role-Based Curricula

Every operational role should have a curriculum.

```yaml
role_curriculum:
  required_fields:
    - role_id
    - role_purpose
    - required_tasks
    - required_knowledge
    - required_skills
    - safety_boundaries
    - tools_used
    - documentation_used
    - training_modules
    - shadowing_requirement
    - supervised_practice
    - assessment
    - refresh_interval
    - backup_training
    - professional_handoff_threshold

  example_food_safety_steward:
    tasks:
      - temperature_logs
      - allergen_matrix
      - date_marking
      - cleaning_schedule
      - illness_exclusion
    knowledge:
      - time_temperature_control
      - allergen_risk
      - cleaning_sanitizing_basics
      - local_review_boundaries
    skills:
      - read_thermometer
      - complete_logs
      - correct_labeling
      - escalate_issue
    safety_level: level_3_advanced_steward
    professional_boundary: local_health_department_or_certified_food_safety_review

  example_water_testing_steward:
    tasks:
      - sample_collection
      - test_schedule
      - lab_coordination
      - results_tracking
      - contamination_alert_escalation
    knowledge:
      - source_hierarchy
      - annual_test_requirements
      - event_based_testing
      - what_not_to_interpret_without_professional_review
    skills:
      - collect_sample
      - log_results
      - trigger_alert
      - communicate_status
    safety_level: level_2_or_3
    professional_boundary: lab_and_public_health_review

  example_tool_library_steward:
    tasks:
      - checkout
      - inspection
      - broken_tool_quarantine
      - PPE_inventory
      - training_records
    knowledge:
      - tool_classes
      - safety_boundaries
      - maintenance_schedule
    skills:
      - inspect_tools
      - enforce_access_rules
      - document_incidents
    safety_level: level_2_or_3
```

### Curriculum Principle

```text
A role without a curriculum is a burden waiting to fall on the person who already knows how.
```

---

## 11. Apprenticeship and Mentorship

Learning should happen through supported practice.

```yaml
apprenticeship_model:
  progression:
    observe:
      description: learner watches task and receives explanation

    assist:
      description: learner helps under supervision

    perform_supervised:
      description: learner completes task while mentor observes

    perform_independently:
      description: learner completes task within documented boundaries

    teach_back:
      description: learner explains and demonstrates the task to another person

    steward:
      description: learner can own the role and train backup

  requirements:
    - mentor_assigned
    - practice_log
    - safety_gate
    - documented_feedback
    - backup_coverage
    - no_apprentice_left_as_sole_operator
    - no_unpaid_apprenticeship_for_labor_that_should_be_paid

  paid_training:
    required_if:
      - training_produces_core_operational_labor
      - training_hours_are_high
      - task_has_high_responsibility
      - resident_is_low_income_and_training_replaces_work_time
```

### Apprenticeship Principle

```text
Learning by doing works when the doing is supported, safe, documented, and not exploitative.
```

---

## 12. Safety Training Gates

Safety-critical tasks require gates.

```yaml
safety_training_gates:
  required_for:
    - power_tools
    - ladders
    - roof_or_height_access
    - sanitation_PPE
    - hazardous_waste
    - food_safety_lead_roles
    - water_testing_roles
    - energy_outage_roles
    - battery_or_generator_area_access
    - first_aid_AED_response
    - emergency_transport
    - vehicle_or_cart_operation
    - care_support_roles
    - conflict_safeguarding_roles

  gate_components:
    - hazard_briefing
    - demonstration
    - supervised_practice
    - checklist
    - stop_work_authority
    - PPE
    - incident_reporting
    - refresh_interval
    - professional_boundary

  fail_if:
    - safety_task_assigned_without_training
    - resident_pressure_to_do_task_above_competence
    - no_PPE
    - no_stop_work_authority
    - no_incident_log
```

### Safety Principle

```text
Enthusiasm is not a safety qualification.
```

---

## 13. Knowledge Base

The knowledge base is the community's memory.

```yaml
knowledge_base:
  required_sections:
    - resident_orientation
    - emergency_procedures
    - module_guides
    - role_guides
    - checklists
    - asset_manuals
    - professional_contacts
    - safety_boundaries
    - policy_registry
    - decision_log
    - lessons_learned
    - failure_reviews
    - training_records
    - FAQs
    - plain_language_explainers

  required_features:
    - searchable
    - versioned
    - offline_copy
    - plain_language
    - role_limited_private_sections
    - exportable
    - backed_up
    - linked_to_asset_registry
    - linked_to_training_modules
    - reviewed_on_schedule

  avoid:
    - knowledge_only_in_chat_history
    - knowledge_only_in_one_persons_head
    - undocumented_verbal_rules
    - AI_generated_guidance_without_review_for_safety_critical_tasks
```

### Knowledge Principle

```text
The settlement should survive turnover, forgetfulness, conflict, and the founder leaving.
```

---

## 14. Teach-Back Culture

Residents should periodically teach what they know.

```yaml
teach_back:
  required:
    - monthly_or_quarterly_skill_shares
    - role_exit_notes
    - incident_lessons_learned
    - apprentice_demonstrations
    - simple_public_explainers_for_core_systems
    - rotating_facilitators

  allowed_topics:
    - food_preservation
    - garden_basics
    - tool_safety
    - water_status
    - energy_outage_mode
    - care_boundaries
    - governance_process
    - finance_basics
    - repair_basics
    - art_music_craft_passion_skills

  boundaries:
    - no_unreviewed_medical_instruction
    - no_unreviewed_electrical_or_structural_instruction
    - no_safety_critical_teaching_without_qualified_review
```

### Teach-Back Principle

```text
A person has learned well enough for the commons when they can explain the boundary of what they do not know.
```

---

## 15. Credential and Professional Boundary

Credentials should be used where they protect people, not where they create needless hierarchy.

```yaml
credential_policy:
  required_or_preferred_credentials:
    food:
      - food_handler_training_for_regular_shared_food_roles
      - manager_level_food_safety_for_leads_where_required_or_useful

    care:
      - first_aid_CPR_AED
      - mental_health_first_aid_or_crisis_training_where_useful
      - professional_healthcare_only_for_clinical_care

    safety:
      - OSHA_or_equivalent_training_for_relevant_construction_or_work_roles
      - tool_specific_training
      - lockout_tagout_awareness_where_relevant

    maintenance:
      - licensed_professionals_for_electrical_plumbing_HVAC_structural_wastewater
      - qualified_technicians_for_battery_generator_solar_service

    governance:
      - mediation_training
      - facilitation_training
      - bookkeeping_or_finance_training
      - legal_professional_review

  avoid:
    - credential_requirements_for_ordinary_belonging
    - credentialism_as_status
    - uncredentialed_people_doing_licensed_work
    - credentialed_people_becoming_unaccountable
```

### Credential Principle

```text
Credentials should mark responsibility and safety, not human worth.
```

---

## 16. Skill Coverage and Redundancy

The app must model skill gaps.

```yaml
skill_coverage:
  required_metrics:
    - critical_roles_total
    - critical_roles_with_primary_trained
    - critical_roles_with_backup_trained
    - critical_roles_with_second_backup_where_needed
    - single_point_of_skill_failure_count
    - external_professional_dependency_count
    - training_overdue_count
    - expired_certifications
    - resident_interest_pool
    - apprentice_pipeline

  coverage_targets:
    all_class_A_roles:
      primary: required
      backup: required
      second_backup: preferred

    safety_critical_roles:
      certification_or_training_current: required
      refresh_interval_defined: required

    operational_roles:
      backup_coverage: required

  fail_if:
    - critical_role_has_no_backup
    - safety_critical_training_expired
    - only_one_person_knows_core_system
    - documentation_missing_for_role
```

### Redundancy Principle

```text
Skill redundancy is care for the future.
```

---

## 17. Learning Labor and Time Burden

Education itself must not become a hidden burden.

```yaml
learning_labor_model:
  labor_categories:
    - onboarding_time
    - safety_training_time
    - role_training_time
    - apprenticeship_time
    - teach_back_time
    - documentation_time
    - refresher_training_time
    - external_class_time
    - certification_time
    - mentoring_time

  required_metrics:
    learning_hours_per_resident_per_month: number
    required_learning_hours: number
    optional_learning_hours: number
    safety_training_hours: number
    unpaid_training_labor: number
    mentor_hours: number
    training_burnout_risk: low_medium_high

  targets:
    required_learning_hours:
      target: 1-3_hours_per_resident_per_month_after_onboarding
      warning_above: 5_hours
      fail_above: 8_hours_unless_formal_program_or_paid_role

    onboarding:
      target: meaningful_but_not_overwhelming
      preferred_duration: staged_over_first_30_90_days
```

### Learning Burden Principle

```text
Training exists to lighten the system, not become another institution residents must survive.
```

---

## 18. Passion Learning and Human Flourishing

The education module should not only train residents to maintain infrastructure.

It should also protect learning for its own sake.

```yaml
passion_learning:
  purpose:
    - art
    - music
    - craft
    - science
    - literature
    - philosophy
    - ecology
    - language
    - history
    - technology
    - entrepreneurship
    - physical practice
    - meditation_or_contemplative_practice
    - local culture

  required_support:
    - quiet_learning_space
    - workshop_or_studio_access_where_possible
    - peer_skill_shares
    - library_or_digital_knowledge_access
    - optional_classes
    - intergenerational_learning
    - no_requirement_to_monetize_learning

  protected_rule:
    - passion_learning_must_not_be_reclassified_as_required_commons_labor_without_consent
```

### Flourishing Principle

```text
A society that only teaches people to maintain itself has not yet returned life to them.
```

---

## 19. Child, Youth, Elder, and Intergenerational Learning

The module should support age-diverse learning without replacing formal schooling.

```yaml
intergenerational_learning:
  children_youth:
    app_boundary:
      - does_not_replace_schooling_or_legal_education_requirements
    supports:
      - garden_learning
      - tool_safety_by_age
      - cooking_basics
      - ecology
      - arts
      - civic_participation
      - elder_story_exchange
      - supervised_maker_projects

  elders:
    supports:
      - teaching_lived_skills
      - oral_history
      - mentorship
      - low_physical_burden_roles
      - learning_new_skills_without_shame
      - digital_support

  adult_residents:
    supports:
      - role_training
      - career_transition
      - practical skills
      - creative growth
      - peer education
      - formal credential pathways

  safeguarding:
    required:
      - child_safety_policy
      - background_check_or_supervision_review_where_required
      - consent
      - boundaries
      - external_legal_review_for_childcare_or_schooling
```

### Intergenerational Principle

```text
Learning should let generations meet without making children, elders, or caregivers into unprotected infrastructure.
```

---

## 20. External Partnerships

The community should connect to outside learning systems.

```yaml
external_partnerships:
  preferred:
    - community_colleges
    - trade_schools
    - cooperative_extension
    - local_libraries
    - maker_spaces
    - health_departments
    - fire_departments
    - EMS
    - food_safety_training_providers
    - OSHA_authorized_training_providers_where_relevant
    - apprenticeship_programs
    - universities
    - local_farms
    - local_tradespeople
    - nonprofits
    - online_courses_with_review

  partnership_outputs:
    - training_calendar
    - credential_pathways
    - visiting_instructor_schedule
    - apprenticeship_opportunities
    - professional_boundary_clarity
    - cost
    - access_and_equity_plan

  avoid:
    - expensive_training_that_does_not_reduce_life_burden
    - vendor_training_that_locks_system_to_vendor
    - partnerships_that_extract_labor_without_compensation
```

### Partnership Principle

```text
The commons should learn from the world, not pretend to contain all knowledge.
```

---

## 21. AI Tutor Boundary

AI can help teach, but should not be the authority for safety-critical knowledge.

```yaml
AI_tutor_boundary:
  allowed:
    - plain_language_explanations
    - quiz_generation
    - role_practice_scenarios
    - checklist_drafts
    - study_plans
    - translation_or_accessibility_support
    - summarizing_approved_docs
    - generating_questions_for_professionals

  review_required:
    - food_safety_training
    - water_safety
    - sanitation
    - electrical
    - structural
    - healthcare
    - legal
    - financial
    - emergency_response
    - tool_safety

  prohibited:
    - AI_certifying_competence
    - AI_authorizing_safety_critical_work
    - AI_replacing_licensed_instruction
    - AI_diagnosing_health_or_mental_health
    - AI_giving_final_legal_or_financial_advice
    - AI_hiding_uncertainty
```

### AI Principle

```text
AI may tutor the learner, but it may not become the credentialing authority for danger.
```

---

## 22. Interfaces With Other Modules

### 22.1 Housing Interface

```yaml
housing_education_interface:
  required:
    - resident_onboarding_to_space
    - common_space_use_training
    - privacy_norms
    - noise_and_courtyard_norms
    - accessibility_awareness
```

```text
Housing works better when residents understand how the space is meant to be used without being policed by ideology.
```

### 22.2 Food Interface

```yaml
food_education_interface:
  required:
    - food_safety_training
    - common_meal_roles
    - pantry_inventory
    - garden_training
    - preservation_safety
    - allergen_awareness
```

```text
Food abundance depends on skill, safety, and shared memory.
```

### 22.3 Water Interface

```yaml
water_education_interface:
  required:
    - water_status_basics
    - testing_steward_training
    - contamination_alert_protocol
    - drought_behavior
    - what_not_to_touch
```

```text
Residents should understand water status without becoming amateur water engineers.
```

### 22.4 Sanitation Interface

```yaml
sanitation_education_interface:
  required:
    - hygiene_basics
    - waste_sorting
    - compost_basics
    - PPE
    - hazardous_waste
    - illness_wave_cleaning
```

```text
Sanitation education protects dignity because it prevents dirty work from becoming invisible or unsafe.
```

### 22.5 Energy Interface

```yaml
energy_education_interface:
  required:
    - critical_load_awareness
    - outage_mode
    - load_shedding_behavior
    - battery_generator_boundaries
    - safe_room procedures
```

```text
Energy literacy should make outages calmer.
```

### 22.6 Care Interface

```yaml
care_education_interface:
  required:
    - first_aid_CPR_AED_path
    - privacy_and_consent
    - care_meal_protocol
    - medication_continuity_awareness
    - mental_health_crisis_boundaries
    - transport_to_care
```

```text
Care training should teach support and boundaries together.
```

### 22.7 Maintenance Interface

```yaml
maintenance_education_interface:
  required:
    - asset_registry_use
    - work_order_submission
    - tool_safety
    - professional_handoff
    - stop_work_authority
    - basic_inspection
```

```text
Maintenance education should help residents notice problems early without asking them to exceed competence.
```

### 22.8 Governance Interface

```yaml
governance_education_interface:
  required:
    - rights_and_responsibilities
    - decision_domains
    - facilitation
    - records
    - conflict_process
    - anti_capture_awareness
```

```text
Governance education should make power legible.
```

### 22.9 Labor & Time Interface

```yaml
labor_time_education_interface:
  required:
    - learning_labor_tracking
    - required_vs_optional_training
    - apprentice_hours
    - mentor_hours
    - protected_passion_learning
```

```text
Learning is a blessing until it becomes uncounted obligation.
```

### 22.10 Legal Land & Finance Interface

```yaml
legal_finance_education_interface:
  required:
    - plain_language_legal_structure
    - resident_cost_basics
    - reserves
    - debt
    - rights_and_exit_formula
    - financial_privacy
```

```text
Residents should not need to be lawyers to understand the deal they live inside.
```

### 22.11 Materials & Fabrication Interface

```yaml
materials_education_interface:
  required:
    - build_system_basics
    - material_substitution_rules
    - tool_training
    - assembly_safety
    - what_requires_professional_review
```

```text
The build system becomes safer when residents know both how it works and where their authority ends.
```

### 22.12 Mobility Interface

```yaml
mobility_education_interface:
  required:
    - accessible_route_awareness
    - shared_vehicle_rules
    - cargo_bike_cart_safety
    - emergency_evacuation
    - non-driver support norms
```

```text
Mobility education prevents access from becoming informal favoritism.
```

---

## 23. Automation-Favoring Requirements

Automation should make learning accessible, track coverage, and prevent single-person dependency.

```yaml
automation_requirements:
  skill_graph:
    required: true
    purpose:
      - map_roles_to_tasks_knowledge_skills
      - show_prerequisites
      - show_coverage
      - show_skill_gaps

  learning_management_lite:
    required: true
    purpose:
      - orientation
      - modules
      - quizzes
      - refreshers
      - records
      - role_paths

  practice_log:
    required: true
    purpose:
      - supervised_practice
      - apprentice_progress
      - teach_back
      - evidence_of_competence

  training_gate_engine:
    required: true
    purpose:
      - block_unsafe_task_assignment
      - require_refreshers
      - flag_expired_training
      - connect_to_professional_boundaries

  knowledge_base:
    required: true
    purpose:
      - documentation
      - checklists
      - lessons_learned
      - manuals
      - plain_language_guides

  backup_role_tracker:
    required: true
    purpose:
      - critical_role_redundancy
      - expert_exit_resilience
      - apprenticeship_pipeline

  learning_burden_dashboard:
    required: true
    purpose:
      - required_training_hours
      - mentor_hours
      - apprentice_hours
      - training_burnout
      - unpaid_learning_burden

  passion_learning_calendar:
    preferred: true
    purpose:
      - optional_skill_shares
      - art_music_craft_science
      - learning_for_fulfillment

  avoid:
    - AI_certifying_competence
    - surveillance_learning_scores
    - gamified_status_hierarchy
    - required_training_bloat
    - hidden_training_labor
    - non-exportable_learning_records
```

### Automation Principle

```text
Automate skill visibility, refreshers, backup coverage, and learning access. Do not automate status hierarchy.
```

---

## 24. Education & Skill Roles

```yaml
education_skill_roles:
  learning_steward:
    purpose: overall learning system coordination
    required_backup: true

  skill_graph_steward:
    purpose: role-task-knowledge-skill mapping and gap reports
    required_backup: true

  onboarding_steward:
    purpose: resident orientation and first 90-day support
    required_backup: true

  safety_training_steward:
    purpose: tool/PPE/emergency/safety gates and refreshers
    required_backup: true

  apprenticeship_steward:
    purpose: mentor matching, practice logs, progression
    required_backup: true

  knowledge_base_steward:
    purpose: docs, checklists, versioning, offline copy
    required_backup: true

  credential_partnership_steward:
    purpose: external trainings, certificates, community college/trade partnerships
    required_backup: true

  passion_learning_steward:
    purpose: optional learning, arts, culture, science, craft, curiosity
    required_backup: true

  accessibility_learning_steward:
    purpose: multiple learning formats, language access, disability support
    required_backup: true
```

### Role Rule

```text
No one should become indispensable because they are the only person who knows how something works.
```

---

## 25. Scenario Simulations

The education and skill module must support stress simulations.

```yaml
education_skill_scenarios:
  normal_year:
    tests:
      - onboarding_completion
      - skill_coverage
      - training_burden
      - backups
      - teach_back
      - knowledge_base_updates

  expert_exit:
    tests:
      - role_backup
      - documentation_quality
      - apprentice_pipeline
      - professional_handoff
      - service_continuity

  new_resident_wave:
    tests:
      - onboarding_capacity
      - mentor_burden
      - training_schedule
      - social_integration
      - safety_orientation

  safety_incident:
    tests:
      - training_gap
      - incident_review
      - refresher_update
      - stop_work_authority
      - professional_boundary

  role_burnout:
    tests:
      - overtrained_or_overassigned_person
      - apprentice_support
      - task_redistribution
      - paid_role_threshold

  skill_gap_under_stress:
    tests:
      - outage_role_coverage
      - water_contamination_response
      - illness_wave_protocol
      - maintenance_emergency
      - care_meal_surge

  credential_expiry:
    tests:
      - food_safety
      - first_aid
      - tool_safety
      - external_certifications
      - role_assignment_blocking

  AI_training_error:
    tests:
      - review_controls
      - safety_boundary
      - human_approval
      - documentation_correction
```

---

## 26. Education & Skill Gates

The app should fail or warn based on learning-system viability.

```yaml
education_skill_gates:
  orientation_gate:
    fail_if:
      - no_resident_orientation
      - residents_do_not_know_emergency_procedures
      - residents_do_not_know_rights_and_exit_process
      - residents_are_assigned_work_before_orientation

  safety_training_gate:
    fail_if:
      - safety_critical_tasks_assigned_without_training
      - no_stop_work_authority_training
      - no_PPE_training_where_required
      - no_incident_reporting_training

  critical_skill_coverage_gate:
    fail_if:
      - critical_role_without_primary_trained_person
      - critical_role_without_backup
      - only_one_person_knows_core_system
      - training_records_missing

    warn_if:
      - second_backup_missing_for_class_A_systems
      - apprentice_pipeline_empty
      - external_professional_relationship_missing

  knowledge_capture_gate:
    fail_if:
      - no_knowledge_base
      - role_docs_missing_for_critical_roles
      - asset_manuals_not_linked
      - lessons_learned_not_recorded

    warn_if:
      - knowledge_base_outdated
      - documentation_too_technical_for_residents
      - docs_only_available_online_with_no_offline_copy

  credential_boundary_gate:
    fail_if:
      - unlicensed_people_do_licensed_work
      - app_or_AI_certifies_safety_critical_competence
      - credential_expired_for_required_role
      - professional_boundary_undefined

  learning_burden_gate:
    fail_if:
      - required_learning_hours_above_8_per_month_by_default
      - apprenticeship_used_as_unpaid_labor
      - mentors_overloaded
      - training_required_but_time_not_counted

    warn_if:
      - required_learning_hours_above_5_per_month
      - onboarding_too_dense
      - optional_learning_becoming_social_requirement

  accessibility_gate:
    fail_if:
      - training_not_understandable_to_residents
      - no_accommodation_for_disability_or_language_needs
      - only_one_learning_format_available_for_required_training

  expert_capture_gate:
    fail_if:
      - expert_controls_system_without_documentation
      - expert_can_block_access_to_knowledge
      - no_backup_for_expert_role
      - credentials_used_to_override_governance_without review

  passion_learning_gate:
    warn_if:
      - no_optional_learning_space
      - all_learning_is_operational
      - creative_learning_absorbed_into_required_labor
```

---

## 27. App Modeling Boundary

The app should model education and skill at the level of **roles, tasks, knowledge, skills, safety gates, onboarding, coverage, training burden, apprenticeships, documentation, and professional boundaries**, not final curriculum accreditation.

### The App Should Model

```text
role curricula
task/knowledge/skill statements
training modules
skill coverage
backup roles
practice logs
safety gates
refresh intervals
external credential needs
knowledge base status
onboarding
learning labor
expert dependency
apprenticeship pipeline
passion learning support
scenario failures
```

### The App Should Not Claim to Solve by Default

```text
state-approved education
schooling compliance
child education law
professional licensing
trade licensing
OSHA compliance certification
food safety certification
medical training certification
legal training
financial certification
clinical competence
employment credentialing
```

### Principle

```text
The app should identify what people must know, how they learn it, when they are ready, and where professional authority is required.
```

---

## 28. Required Data Model

```yaml
EducationSkillCommons:
  id: string
  population_served: integer

  learning_system:
    orientation_program: boolean
    knowledge_base: boolean
    skill_graph: boolean
    learning_management_lite: boolean
    practice_log: boolean
    training_gate_engine: boolean
    backup_role_tracker: boolean
    learning_burden_dashboard: boolean

  skill_coverage:
    critical_roles_total: integer
    critical_roles_primary_trained_percent: number
    critical_roles_backup_trained_percent: number
    class_A_roles_second_backup_percent: number
    single_point_skill_failures: integer
    training_overdue_count: integer
    expired_required_credentials: integer
    apprentice_pipeline_count: integer

  onboarding:
    residents_oriented_percent: number
    new_residents_in_first_90_days: integer
    mentor_capacity_status: pass | warn | fail
    rights_training_complete_percent: number
    emergency_training_complete_percent: number
    safety_orientation_complete_percent: number

  training_burden:
    required_learning_hours_per_resident_per_month: number
    optional_learning_hours_per_resident_per_month: number
    mentor_hours_per_month: number
    apprentice_hours_per_month: number
    unpaid_training_labor_hours: number
    training_burnout_risk: low | medium | high

  safety:
    safety_critical_tasks_total: integer
    safety_critical_tasks_with_gate_percent: number
    PPE_training_current_percent: number
    stop_work_authority_training_percent: number
    incident_review_training: boolean

  documentation:
    role_docs_complete_percent: number
    asset_docs_linked_percent: number
    lessons_learned_logged: boolean
    offline_copy_available: boolean
    docs_plain_language_score: number
    docs_review_overdue_count: integer

  external_partnerships:
    community_college_partner: boolean
    trade_partner: boolean
    cooperative_extension_partner: boolean
    food_safety_training_partner: boolean
    first_aid_CPR_AED_partner: boolean
    OSHA_or_safety_partner: boolean
    local_professional_mentor_pool: boolean

  passion_learning:
    optional_skill_shares_per_month: number
    quiet_learning_space: boolean
    workshop_studio_access: boolean
    intergenerational_learning_events: number
    passion_learning_protected: boolean

  outputs:
    education_readiness_status: pass | warn | fail
    critical_skill_coverage_status: pass | warn | fail
    safety_training_status: pass | warn | fail
    knowledge_capture_status: pass | warn | fail
    learning_burden_status: pass | warn | fail
    expert_dependency_score: number
    life_burden_reduction_score: number
    flourishing_score: number
    complexity_score: number
```

---

## 29. Required App Outputs

```yaml
required_outputs:
  - education_skill_summary
  - skill_graph_report
  - onboarding_report
  - critical_skill_coverage_report
  - safety_training_gate_report
  - role_curriculum_report
  - apprenticeship_pipeline_report
  - backup_role_report
  - knowledge_base_status_report
  - documentation_gap_report
  - external_credential_partnership_report
  - learning_labor_burden_report
  - expert_dependency_report
  - passion_learning_report
  - scenario_failure_report
  - professional_review_requirements
  - visualization_bundle_metadata
```

---

## 30. Visualization Requirements

The education and skill module should export enough data for a dashboard or virtual learning map.

```yaml
visualization_requirements:
  graph_objects:
    - roles
    - tasks
    - knowledge_nodes
    - skill_nodes
    - prerequisites
    - residents_or_role_slots
    - mentors
    - apprentices
    - external_credentials
    - professional_boundaries

  overlays:
    - critical_skill_coverage
    - missing_backups
    - training_overdue
    - expired_credentials
    - expert_dependency
    - learning_burden
    - safety_gate_status
    - knowledge_base_gaps
    - passion_learning_opportunities

  scenario_playback:
    - expert_exit
    - new_resident_wave
    - safety_incident
    - role_burnout
    - skill_gap_under_stress
    - credential_expiry
    - AI_training_error
```

---

## 31. Best Default Requirements Summary

```yaml
MinimumViableEducationSkillCommons:
  population:
    first_serious_model: 80
    valid_range: 50-150

  philosophy:
    lifelong_learning: true
    role_based_skill_lattice: true
    safety_gates_required: true
    credential_only_where_needed: true
    expert_capture_prevented: true
    passion_learning_protected: true
    AI_tutor_not_certifier: true

  systems:
    orientation_program: required
    skill_graph: required
    learning_management_lite: required
    practice_log: required
    training_gate_engine: required
    knowledge_base: required
    backup_role_tracker: required
    learning_burden_dashboard: required
    passion_learning_calendar: preferred

  required_learning_paths:
    resident_orientation: required
    safety_orientation: required
    food_safety: required_for_food_roles
    water_testing: required_for_water_roles
    sanitation_PPE: required_for_sanitation_roles
    energy_outage: required_for_energy_roles
    first_aid_CPR_AED: preferred_or_required_by_role
    tool_safety: required_for_tool_roles
    governance_facilitation: required_for_governance_roles
    maintenance_asset_registry: required_for_maintenance_roles
    care_privacy_boundaries: required_for_care_roles

  targets:
    critical_roles_primary_trained: 100_percent
    critical_roles_backup_trained: 100_percent
    class_A_second_backup: preferred
    residents_oriented: 100_percent
    required_learning_hours_after_onboarding: 1-3_per_month_target
    warning_above: 5_per_month
    fail_above: 8_per_month_unless_formal_or_paid

  gates:
    orientation_gate: required
    safety_training_gate: required
    critical_skill_coverage_gate: required
    knowledge_capture_gate: required
    credential_boundary_gate: required
    learning_burden_gate: required
    accessibility_gate: required
    expert_capture_gate: required
    passion_learning_gate: required
```

---

## 32. Design Maxims

```text
Do not make everyone learn everything.

Do not make one person know everything.

Do not confuse confidence with competence.

Do not confuse credentials with wisdom.

Do not assign dangerous tasks by enthusiasm.

Do not let learning become hidden labor.

Do not let apprenticeship become exploitation.

Do not let experts become rulers.

Do not let AI certify danger.

Do not make residents decode the system socially.

Teach the floor.

Gate the dangerous.

Document the tacit.

Back up every critical role.

Refresh what expires.

Use mentors.

Use teach-back.

Use external professionals.

Protect curiosity beyond utility.

Make learning return life, not consume it.
```

---

## 33. Open Questions for Iteration

```text
1. What are the first 10 required learning paths for v0?
2. Should every adult resident complete basic first aid, or only a target percentage?
3. What required learning burden is acceptable after onboarding?
4. Should the system include paid apprenticeships for high-burden internal roles?
5. Should children and youth learning be included in v0 or deferred to a separate childcare/education module?
6. Should the skill lattice map residents by name, role slot, or anonymized coverage to protect privacy?
7. What external credentials should be mandatory versus preferred?
8. Should AI tutoring be built into the app or kept outside until the knowledge base is mature?
9. How should residents challenge a denied training gate?
10. What skill failure would make the entire CIaC model morally invalid?
```

---

## 34. Source Notes

The research basis for this draft includes:

- UNESCO lifelong learning resources and Education 2030 / SDG 4.
- U.S. Department of Labor Registered Apprenticeship model.
- OSHA worker training responsibilities and safety training resources.
- NIST NICE Framework structure for tasks, knowledge, and skills.
- Community health worker boundary models.
- Cooperative extension and practical/vocational education precedents.
- Maker education, peer learning, and apprenticeship-based learning practices.
