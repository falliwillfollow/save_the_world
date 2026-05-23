# CIaC Legal Land & Finance Module: Anti-Speculative Civic Floor

**Module ID:** `legal_land_finance.anti_speculative_civic_floor.v0_1`  
**Status:** Draft requirement module  
**Purpose:** Define the default legal, land-control, finance, affordability, reserve, insurance, and risk structure for a scalable Minimum Viable Dignified Infrastructure complex.  
**Primary design question:** What legal and financial architecture best removes the civic floor from speculative extraction, keeps monthly cash requirements low, funds maintenance honestly, protects residents from bank-pressure cascades, and remains legally reviewable without pretending the app can practice law or finance?

---

## 1. Core Thesis

The CIaC legal and finance baseline should **not** be private real-estate speculation with nicer language.

If land, housing, energy, water, food, care, or maintenance systems can be captured by investors, founders, lenders, landlords, or appreciation games, the project will eventually reproduce the system it was meant to escape.

The recommended baseline is an **Anti-Speculative Civic Floor**:

```text
land held by a mission-locked steward
+ resident use or occupancy rights
+ limited-equity or shared-equity ownership logic
+ commons asset lock
+ transparent operating budget
+ replacement reserves
+ emergency reserves
+ affordability covenants or resale formulas
+ debt limits
+ insurance and liability planning
+ professional legal / tax / finance review
+ anti-displacement rules
+ exit rights
+ no investor control of survival infrastructure
```

The goal is not to eliminate all money.

The goal is to prevent money from becoming sovereign over the floor.

---

## 2. Guiding Sentence

> Land should be stewarded, housing should remain affordable, debt should be bounded, reserves should be real, and no one should be able to turn the civic floor into an extraction machine.

---

## 3. Strategic Decision

The best default model is:

# A CLT-like land stewardship layer combined with limited-equity cooperative or shared-equity resident rights, plus a separate operating commons for shared infrastructure.

```yaml
legal_land_finance_strategy:
  default_pattern:
    land_layer:
      recommended: CLT_like_or_mission_locked_land_steward
      purpose:
        - remove_land_from_speculation
        - preserve_long_term_affordability
        - hold_common_land_and_ecological_assets
        - enforce_resale_or_transfer_limits
        - protect_community_purpose

    housing_use_layer:
      recommended:
        - limited_equity_cooperative
        - shared_equity_occupancy_rights
        - long_term_leasehold_or_ground_lease
        - deed_restricted_or_resale_formula_model_where_appropriate
      purpose:
        - give_residents secure use rights
        - allow modest equity or exit value where appropriate
        - prevent private windfall capture
        - prevent landlord-like unilateral control

    operating_commons_layer:
      recommended:
        - resident_controlled_operating_cooperative_or_association
        - service_cooperative
        - nonprofit_or_public_benefit_entity_where_reviewed
      purpose:
        - operate food, water, energy, maintenance, care, and common spaces
        - collect operating assessments
        - hold reserves
        - contract with professionals
        - maintain transparent budgets

    finance_layer:
      recommended:
        - low_interest_mission_aligned_debt
        - public_subsidy_where_available
        - grants_or_philanthropic_capital
        - patient_capital_without_control_rights
        - member_capital_capped_and_protected
        - reserves_funded_from_day_one
      avoid:
        - speculative_investor_equity
        - uncapped_appreciation
        - high_interest_debt
        - short_maturity_balloon_risk_without_plan
        - founder_personal_guarantee_as_permanent_structure
        - underfunded_maintenance_reserves

  app_boundary:
    required: true
    statement: The app can model legal and financial requirements, risks, and options, but cannot choose or draft the final legal structure without qualified professionals.
```

### Rationale

The civic floor needs a legal and financial immune system.

Without it, land appreciation, debt service, insurance shocks, taxes, deferred maintenance, succession conflicts, or investor claims can slowly pull the project back into the wealth game.

---

## 4. Research Anchors

This module is grounded in the following research and precedent categories.

### 4.1 Community land trusts

Community land trusts are nonprofit organizations that can hold land and steward long-term affordability. CLT models typically separate ownership of land from ownership or use of buildings, using ground leases and resale limits to preserve affordability across generations.

**Design implication:** CIaC should use CLT-like logic to remove land from speculation and protect long-term affordability.

### 4.2 Limited-equity cooperatives

Limited-equity cooperatives allow residents to purchase shares in a cooperative that owns the property, while restricting resale prices by formula to preserve affordability.

**Design implication:** CIaC can use limited-equity logic to give residents secure participation and modest equity without allowing housing to become speculative.

### 4.3 Cooperative principles

Cooperatives are member-owned and democratically controlled, with members contributing to and controlling capital. Primary cooperatives generally use one-member-one-vote democratic control.

**Design implication:** Resident control should not scale with financial contribution.

### 4.4 Shared-equity housing

Shared-equity models divide property rights between the resident and a community steward, preserving affordability while allowing resident stability and some wealth-building.

**Design implication:** CIaC should distinguish resident security from speculative upside.

### 4.5 Nonprofit asset dedication

U.S. nonprofit charitable structures can require that assets remain dedicated to exempt or public purposes upon dissolution, depending on legal form and documents.

**Design implication:** The app should model asset-lock and dissolution requirements as legal-review triggers.

### 4.6 Replacement reserves

Affordable, cooperative, and multifamily housing systems often require replacement reserves to fund major repairs and capital replacements over time.

**Design implication:** Low monthly cost without reserves is false affordability.

### 4.7 Securities and investment-risk boundaries

Pooling money with expectations of profit from others' efforts can raise securities-law issues depending on structure, offering, jurisdiction, and facts.

**Design implication:** CIaC should avoid crowdfunding or investor-return structures without legal review.

### 4.8 Zoning, land use, and permitting

Housing form, density, shared facilities, wells, septic, agriculture, food service, accessory structures, and occupancy rules are locally governed.

**Design implication:** The app should treat jurisdictional feasibility as a first-class constraint.

---

## 5. Recommended Scale

The legal and finance module should support the same first serious village-block population as the physical modules.

```yaml
population:
  minimum_meaningful_scale: 50
  ideal_first_model: 80
  upper_bound_before_replication: 150
```

### Scale Logic

```text
Below 50:
  legal and finance overhead can become too heavy per resident unless piggybacking on an existing entity or landowner.

Around 80:
  land stewardship, cooperative governance, reserves, shared operating costs, and professional services become more economically plausible.

Above 150:
  legal, insurance, employment, tax, public-health, utility, and housing-law complexity increases and may require more formalized administration.
```

### Scaling Method

Do not grow one legal organism indefinitely. Replicate village blocks and federate shared services.

```yaml
scaling:
  50-100_residents:
    land_entity: 1
    housing_use_entity: 1
    operating_commons: 1
    professional_review: required

  100-150_residents:
    land_entity: 1
    housing_use_entity: 1_or_multiple_pods
    operating_commons: 1_with_subaccounts
    formal_admin_capacity: preferred

  above_150_residents:
    recommendation: replicate_block_or_federate
    reason: preserve_human_scale_and_reduce_legal_bureaucracy
```

---

## 6. Default Prototype

```yaml
default_prototype:
  name: anti_speculative_civic_floor_80
  residents: 80

  legal_structure_profile:
    status: model_only_requires_attorney
    candidate_stack:
      land_steward:
        type: CLT_like_nonprofit_or_mission_locked_land_entity
        purpose:
          - own_land
          - hold_ground_leases_or_use_restrictions
          - enforce_affordability
          - protect_ecological_and_common_assets

      resident_housing_body:
        type: limited_equity_cooperative_or_shared_equity_association
        purpose:
          - resident_membership
          - occupancy_or_use_rights
          - resident_governance
          - capped_equity_or_exit_formula

      operating_commons:
        type: service_cooperative_or_common_benefit_operating_entity
        purpose:
          - food_energy_water_maintenance_care_common_space_operations
          - assessments
          - reserves
          - contracts
          - insurance

      finance_vehicle:
        type: project_specific_debt_and_capital_stack
        purpose:
          - acquisition
          - construction
          - infrastructure
          - reserves
          - startup_operations

  finance_targets:
    monthly_core_cost_per_resident: materially_below_conventional_baseline
    debt_service_coverage: required_if_debt
    operating_reserve: 3-6_months_target
    emergency_reserve: required
    replacement_reserve: required_from_day_one
    affordability_drift_monitor: required

  prohibited_by_default:
    - uncapped_private_appreciation_of_core_housing
    - investor_control_of_land_or_survival_assets
    - debt_without_refinance_or_maturity_plan
    - deferred_maintenance_as_affordability_strategy
    - informal_occupancy_without_written_rights
```

---

## 7. Legal Layer Model

The app should model legal layers separately.

```yaml
legal_layers:
  land_ownership_layer:
    questions:
      - who_owns_land
      - can_land_be_sold
      - who_approves_sale
      - what_happens_on_dissolution
      - are_ecological_assets_protected
      - can_land_be_encumbered_by_debt
      - who_has_reversionary_or_enforcement_rights

  housing_use_layer:
    questions:
      - what_right_does_resident_have
      - lease_share_membership_or_ownership
      - can_resident_be_removed
      - what_due_process_applies
      - what_exit_value_exists
      - how_is_resale_or_transfer_controlled
      - what_happens_if_resident_cannot_pay

  operating_layer:
    questions:
      - who_operates_common_systems
      - who_collects_assessments
      - who_holds_reserves
      - who_contracts_with_professionals
      - who_carries_insurance
      - who_pays_taxes_and_utilities
      - who_has_emergency_authority

  finance_layer:
    questions:
      - who_borrows
      - who_guarantees
      - what_assets_are_collateral
      - what_is_the_debt_maturity
      - what_are_the_interest_rate_risks
      - are_capital_sources_control_free
      - what_happens_on_default

  regulatory_layer:
    questions:
      - zoning_allowed
      - building_permits_required
      - subdivision_or_condo_rules
      - occupancy_limits
      - health_department_review
      - utility_regulation
      - food_service_rules
      - employment_labor_rules
      - tax_status
      - securities_law_review
```

### Legal Layer Principle

```text
Do not let one entity quietly hold incompatible powers over land, housing, money, operations, and resident rights.
```

---

## 8. Land Control Strategy

Land control is the foundation of the civic floor.

```yaml
land_control:
  preferred:
    - mission_locked_land_steward
    - CLT_like_nonprofit
    - public_or_public_benefit_land_lease
    - conservation_or_affordability_restrictions_where_appropriate
    - long_term_ground_lease
    - anti_speculation_covenants

  acceptable_with_review:
    - cooperative_owned_land
    - nonprofit_owned_land
    - public_private_partnership
    - long_term_master_lease
    - donated_land_with_restrictions
    - land_bank_transfer
    - church_or_institutional_land_partnership

  high_risk:
    - private_founder_owned_land
    - investor_owned_land
    - short_term_lease
    - land_debt_secured_by_all_core_assets
    - no_resale_or_transfer_restrictions
    - unclear_title
    - unresolved_easements_or_access

  fail_if:
    - no_secure_land_control
    - land_can_be_sold_without_commons_review
    - residents_have_no_written_use_rights
    - lender_can_eliminate_floor_without_mitigation_plan
```

### Land Principle

```text
If land remains speculative, the floor remains temporary.
```

---

## 9. Resident Rights and Tenure

Residents need secure, legible rights.

```yaml
resident_tenure:
  possible_forms:
    cooperative_share:
      benefits:
        - resident_democratic_control
        - shared_ownership_logic
        - possible_limited_equity
      risks:
        - financing_complexity
        - governance_burden
        - exit_value_disputes

    long_term_ground_or_occupancy_lease:
      benefits:
        - clearer_use_right
        - compatibility_with_CLT_logic
        - enforceable_affordability
      risks:
        - lease_complexity
        - perceived_lower_ownership

    rental_with_strong_member_rights:
      benefits:
        - lower_entry_cost
        - easier_for_transient_or_low_asset_residents
      risks:
        - landlord_like_dynamic
        - weaker_equity_participation

    deed_restricted_homeownership:
      benefits:
        - familiar_ownership
        - mortgage_compatibility
      risks:
        - less_suitable_for_integrated_commons
        - possible_fragmentation

  required_rights:
    - written_occupancy_or_use_agreement
    - due_process
    - privacy
    - access_to_common_floor
    - repair_request_process
    - participation_rights
    - exit_process
    - accommodation_process
    - dispute_process
    - anti_retaliation_protection

  prohibited:
    - informal_promises_as_tenure
    - founder_discretionary_eviction
    - survival_access_conditioned_on_social_popularity
    - unclear_exit_value
```

### Tenure Principle

```text
Dignity requires knowing why you can stay, when you can be asked to leave, and what process protects you.
```

---

## 10. Affordability Model

Affordability must be structural, not aspirational.

```yaml
affordability_model:
  core_metric:
    - monthly_core_cost_per_resident
    - monthly_core_cost_per_household
    - required_wage_hours_to_cover_core_cost
    - cost_as_percent_of_income_bands
    - comparison_to_local_rent
    - comparison_to_conventional_homeownership
    - bad_year_assessment_risk
    - reserve_contribution_included

  core_cost_components:
    - housing_use_cost
    - operating_assessment
    - utilities_or_energy_contribution
    - water_sanitation
    - food_commons_optional_or_baseline_component
    - maintenance_reserve
    - replacement_reserve
    - emergency_reserve
    - insurance
    - taxes_or_payments_in_lieu
    - administration
    - debt_service

  rules:
    - reserves_count_as_real_cost
    - deferred_maintenance_cannot_make_model_look_affordable
    - food_labor_savings_must_count_labor
    - volunteer_labor_cannot_hide_operating_costs
    - bad_year_assessment_spikes_must_be_simulated
    - affordability_measured_against_local_income_and_wage_hours
```

### Affordability Principle

```text
A low monthly cost that omits reserves, insurance, taxes, labor, or replacement cycles is not affordability. It is a delayed bill.
```

---

## 11. Resale, Exit Value, and Equity

CIaC should allow security and modest equity where appropriate, but not speculative windfall.

```yaml
resale_exit_value:
  allowed_models:
    no_equity_low_entry:
      description: residents pay low entry and low monthly cost; exit value minimal
      suited_for:
        - rental_like_models
        - very_low_income_access
      risk:
        - weaker_asset_building

    limited_equity_formula:
      description: resident share value increases by defined formula
      suited_for:
        - cooperative_models
        - shared_equity_models
      risk:
        - formula_complexity

    indexed_resale_formula:
      description: exit value tied to inflation, wage index, or limited appreciation
      suited_for:
        - CLT_or_coop_hybrid
      risk:
        - must_preserve_future_affordability

    sweat_equity_credit:
      description: certain capital-improving labor credited at capped value
      suited_for:
        - early_build_phase
      risk:
        - labor_valuation_conflicts
        - securities_or_tax_or_employment_review

  required:
    - written_exit_formula
    - affordability_test_for_next_resident
    - reserve_and_debt_adjustment_rules
    - dispute_process
    - hardship_exit_process
    - death_divorce_disability_transition_rules
    - no_private_market_sale_of_core_unit_without_restriction

  fail_if:
    - uncapped_appreciation
    - exit_value_destroying_next_resident_affordability
    - no_exit_value_rule
    - founder_or_investor_claim_before_resident_protection
```

### Equity Principle

```text
Residents should be able to leave with dignity, but not by selling the floor out from under the next resident.
```

---

## 12. Capital Stack

The app should model project funding as a stack with risk labels.

```yaml
capital_stack:
  uses:
    - land_acquisition
    - predevelopment
    - design_engineering_legal
    - permits
    - construction
    - infrastructure
    - contingency
    - startup_operations
    - replacement_reserve_seed
    - emergency_reserve_seed
    - working_capital

  preferred_sources:
    public_or_mission_sources:
      - grants
      - public_land
      - land_bank
      - housing_trust_fund
      - climate_or_resilience_funding
      - USDA_or_rural_development_where_eligible
      - CDFI_loans
      - municipal_support
      - philanthropic_program_related_investment

    community_sources:
      - member_capital_capped
      - donations_without_control
      - low_interest_community_notes_after_legal_review
      - predevelopment_fundraising_after_review

    debt_sources:
      - low_interest_mission_lender
      - construction_loan
      - permanent_mortgage
      - cooperative_share_loan_where_available
      - equipment_finance_for_noncritical_assets_with_review

  high_risk_sources:
    - high_interest_private_debt
    - short_maturity_balloon_debt
    - investor_equity_with_control_rights
    - unsecured_promissory_notes_sold_publicly_without_review
    - crowdfunding_with_profit_expectation
    - founder_personal_credit_as_core_foundation
    - crypto_or_tokenized_ownership
```

### Capital Principle

```text
Capital should be patient enough not to make the floor nervous.
```

---

## 13. Debt Policy

Debt is not forbidden, but it must be bounded.

```yaml
debt_policy:
  required:
    - debt_service_schedule
    - interest_rate_risk_model
    - maturity_or_balloon_plan
    - collateral_map
    - default_consequence_map
    - reserve_requirement
    - member_approval_threshold
    - refinance_risk_scenario
    - bad_year_revenue_scenario
    - lender_rights_review
    - covenant_tracking

  debt_limits:
    - no_debt_that_can_force_sale_without_mitigation_review
    - no_major_debt_without_member_approval
    - no_cross_collateralization_of_all_core_assets_without_review
    - no_short_term_bridge_debt_without takeout_plan
    - no_variable_rate_exposure_without_stress_test

  ratios_to_model:
    - debt_service_coverage_ratio
    - loan_to_value
    - debt_per_resident
    - monthly_debt_service_per_resident
    - reserve_months_available
    - refinance_gap
```

### Debt Principle

```text
Debt is useful only if it does not turn the bank into the hidden sovereign.
```

---

## 14. Reserves and Capital Planning

Reserves are the difference between affordability and deferred collapse.

```yaml
reserves:
  required_reserves:
    operating_reserve:
      purpose: cover normal revenue or cost disruption
      target: 3-6_months_operating_expenses
      minimum: 3_months_unless_formally_justified

    replacement_reserve:
      purpose: major repair and replacement of building and infrastructure components
      basis:
        - capital_needs_assessment
        - asset_registry
        - expected_life
        - replacement_cost
      required_from_day_one: true

    emergency_repair_reserve:
      purpose: unexpected critical failures
      target: risk_based
      required: true

    insurance_deductible_reserve:
      purpose: cover deductibles after loss event
      required: true

    hardship_or_stabilization_reserve:
      purpose: prevent temporary resident crisis from becoming displacement
      preferred: true
      restrictions:
        - transparent_policy
        - privacy
        - anti_favoritism

    predevelopment_reserve:
      purpose: legal_design_engineering_feasibility_before_build
      required_for_new_project: true

  reserve_rules:
    - reserves_are_real_monthly_cost
    - replacement_reserve_cannot_be_used_for_discretionary_projects_without_approval
    - reserve_drawdown_requires_replenishment_plan
    - reserve_status_public_to_members
    - reserve_shortfall_triggers_affordability_and_risk_review
```

### Reserve Principle

```text
Every cheap system becomes expensive when it reaches the replacement year with no money.
```

---

## 15. Insurance and Liability

Insurance is boring until it decides whether the project survives a bad event.

```yaml
insurance_liability:
  required_review:
    - property_insurance
    - general_liability
    - directors_and_officers
    - workers_compensation_if_employees_or_required
    - volunteer_accident_or_liability_coverage_where_available
    - auto_or_shared_vehicle
    - cyber_or_data_if_app_stores_sensitive_info
    - professional_liability_for services_provided_by_professionals
    - builder_risk_during_construction
    - flood_wildfire_wind_or_regional_hazard_coverage
    - food_service_liability_if_common_kitchen_or_sales
    - farm_or_agricultural_liability_if_applicable
    - care_room_liability_boundaries

  required_outputs:
    - coverage_map
    - exclusions_report
    - deductible_map
    - annual_premium_per_resident
    - insurance_unavailability_risk
    - claim_response_plan
    - risk_reduction_requirements

  fail_if:
    - no_liability_review
    - no_property_coverage_plan
    - no_D&O_or_governance_liability_review
    - no_workers_compensation_review_where_labor_roles_or_employees_exist
    - high_hazard_module_without_insurance_review
```

### Insurance Principle

```text
A community that cannot insure its risks has not finished designing them.
```

---

## 16. Taxes and Public Obligations

The app should flag tax obligations without attempting to resolve them.

```yaml
tax_public_obligations:
  possible_obligations:
    - property_tax
    - transfer_tax
    - sales_tax
    - payroll_tax
    - income_tax
    - unrelated_business_income_tax_if_nonprofit
    - cooperative_taxation
    - local_fees
    - utility_fees
    - stormwater_fees
    - permit_fees
    - special_assessments

  possible_exemptions_or_reductions:
    - nonprofit_exemption_where_eligible
    - affordable_housing_tax_treatment
    - agricultural_use_value_where_eligible
    - renewable_energy_incentives
    - historic_or_conservation_incentives
    - public_private_partnership_benefits

  required:
    - CPA_or_tax_attorney_review
    - annual_tax_calendar
    - tax_status_not_assumed
    - reserve_for_taxes_and_fees
    - no_claim_of_tax_exemption_without_approval
```

### Tax Principle

```text
Do not build a low-cost model on assumed tax treatment.
```

---

## 17. Zoning, Land Use, and Permitting

The app should treat legal feasibility as a gate.

```yaml
zoning_land_use:
  required_review_topics:
    - allowed_residential_density
    - multifamily_or_cohousing_classification
    - cooperative_or_group_living_rules
    - subdivision_or_condominium_rules
    - accessory_structures
    - common_house
    - kitchen_or_food_service
    - agriculture_or_greenhouse
    - workshops
    - wastewater_and_septic_capacity
    - wells_and_water_rights
    - parking_requirements
    - fire_access
    - stormwater
    - floodplain
    - wetlands
    - environmental_constraints
    - building_code
    - accessibility
    - occupancy_limits
    - short_term_guest_rooms_or_caregiver_rooms

  feasibility_status:
    allowed_by_right: best
    special_use_or_conditional_permit: possible
    rezoning_required: high_risk
    prohibited: fail_or_new_site_required

  app_outputs:
    - jurisdiction_profile
    - zoning_risk
    - permit_sequence
    - professional_review_list
    - blocker_report
```

### Land Use Principle

```text
A design that cannot be permitted is a concept, not an infrastructure plan.
```

---

## 18. Securities, Crowdfunding, and Investor Boundary

Raising money can accidentally become regulated investment activity.

```yaml
securities_investor_boundary:
  high_risk_patterns:
    - public_offering_of_profit_bearing_notes
    - tokenized_land_or_housing_shares
    - investor_returns_from_resident_payments
    - crowdfunding_with_expectation_of_profit
    - passive_investors_funding_project_for_return_from_others_efforts
    - revenue_share_from_common_infrastructure
    - speculative_membership_interest

  lower_risk_but_review_required:
    - donations
    - member_capital
    - low_interest_loans
    - community_notes
    - philanthropic_PRIs
    - grants
    - cooperative_share_sales
    - predevelopment fundraising

  required:
    - securities_law_review_before_public_fundraising
    - offering_documents_if_needed
    - investor_control_prohibited_over_core_assets
    - no_profit_expectation_marketing_without_review
    - cap_table_or_obligation_map
```

### Securities Principle

```text
Do not accidentally finance an anti-speculation project by selling speculation.
```

---

## 19. Resident Affordability and Hardship

The system must handle residents who temporarily cannot pay.

```yaml
resident_affordability_hardship:
  required:
    - affordability_screening_method_without_exclusionary_abuse
    - monthly_cost_transparency
    - hardship_policy
    - grace_period_policy
    - payment_plan_policy
    - emergency_stabilization_fund_where_possible
    - due_process_before_loss_of_access
    - role_adjustment_during_hardship
    - no_public_shaming
    - financial_privacy

  hardship_triggers:
    - job_loss
    - illness
    - injury
    - caregiving_burden
    - family_crisis
    - disaster
    - disability_or_access_need
    - unexpected_medical_expense

  prohibited:
    - automatic_loss_of_housing_for_short_term_crisis
    - public_debt_shaming
    - arbitrary_favoritism
    - indefinite_nonpayment_without_process
```

### Hardship Principle

```text
The floor is real only if a temporary crisis does not immediately become displacement.
```

---

## 20. Operating Budget

The operating budget should make the real cost visible.

```yaml
operating_budget:
  required_categories:
    - debt_service
    - insurance
    - taxes_and_fees
    - utilities
    - water_sanitation
    - energy_operations
    - food_commons_operations
    - maintenance_labor_or_contracts
    - replacement_reserve_contribution
    - emergency_reserve_contribution
    - administrative_costs
    - legal_accounting_professional_services
    - software_and_records
    - training
    - safety_and_PPE
    - cleaning
    - common_space_supplies
    - care_room_supplies
    - contingency

  outputs:
    - monthly_cost_per_resident
    - monthly_cost_per_household_type
    - required_income_at_affordability_threshold
    - required_wage_hours_at_local_wage
    - sensitivity_to_interest_rates
    - sensitivity_to_insurance
    - sensitivity_to_tax_changes
    - sensitivity_to_maintenance_cost
    - reserve_shortfall_risk
```

### Budget Principle

```text
The app should not let the project look affordable by hiding the boring line items.
```

---

## 21. Capital Budget and Development Feasibility

The capital budget should include soft costs, contingencies, reserves, and predevelopment.

```yaml
capital_budget:
  required_categories:
    - land
    - due_diligence
    - survey
    - environmental_review
    - geotechnical
    - legal
    - accounting
    - architecture
    - engineering
    - permits
    - utility_connections
    - water_infrastructure
    - sanitation_infrastructure
    - energy_infrastructure
    - roads_paths_access
    - stormwater
    - buildings
    - common_house
    - workshop
    - food_infrastructure
    - care_room
    - furniture_fixtures_equipment
    - construction_contingency
    - escalation_contingency
    - financing_costs
    - developer_or_project_management_fee_if_any
    - startup_operations
    - initial_reserves

  required_outputs:
    - total_development_cost
    - cost_per_resident
    - cost_per_unit_or_bedroom
    - subsidy_needed
    - financing_gap
    - contingency_percent
    - break_even_monthly_cost
    - affordability_gap
    - development_risk_score
```

### Capital Principle

```text
The first lie in housing is usually the missing soft costs.
```

---

## 22. Professional Review Matrix

The app must require professional review for legal, finance, tax, insurance, and permitting issues.

```yaml
professional_review_matrix:
  attorney_required:
    - entity_selection
    - land_purchase_or_lease
    - ground_lease
    - cooperative_documents
    - occupancy_agreements
    - resale_formula
    - asset_lock
    - securities_or_fundraising
    - debt_documents
    - eviction_or_membership_termination
    - employment_or_labor_structure
    - privacy_policy
    - zoning_land_use

  CPA_or_tax_advisor_required:
    - entity_tax_status
    - member_capital
    - cooperative_taxation
    - nonprofit_tax_status
    - payroll
    - reserve accounting
    - unrelated_business_income
    - charitable_deduction_claims
    - depreciation_or_capitalization

  lender_or_project_finance_review_required:
    - capital_stack
    - debt_service
    - refinance_risk
    - DSCR
    - reserve requirements
    - collateral
    - loan covenants

  insurance_broker_required:
    - coverage_map
    - exclusions
    - builder_risk
    - D&O
    - general_liability
    - property
    - workers_comp
    - flood_wildfire_wind
    - food_or_agriculture
    - shared_vehicle
    - cyber_or_privacy

  local_authority_required:
    - zoning
    - building
    - fire
    - health_department
    - water_well
    - septic_wastewater
    - stormwater
    - food_service
    - accessibility
```

### Review Principle

```text
The app may produce questions, warnings, and candidate structures. Professionals must produce enforceable documents and approvals.
```

---

## 23. Interfaces With Other Modules

### 23.1 Housing Interface

```yaml
housing_legal_finance_interface:
  required:
    - tenure_form
    - unit_cost
    - affordability_formula
    - capital_budget
    - insurance
    - replacement_reserve
    - permits
    - accessibility_review
```

```text
Housing is not dignified if legal tenure is fragile.
```

### 23.2 Food Interface

```yaml
food_legal_finance_interface:
  required:
    - common_kitchen_legal_status
    - food_service_review
    - CSA_or_supplier_contracts
    - food_budget
    - food_labor_compensation_or_contribution_rules
    - food_enterprise_boundary
```

```text
Food savings should not accidentally create illegal food service or unpaid labor exploitation.
```

### 23.3 Water Interface

```yaml
water_legal_finance_interface:
  required:
    - water_rights_or_service_agreement
    - well_permit
    - testing_budget
    - treatment_capital_cost
    - maintenance_reserve
    - emergency_water_contract
```

```text
Water rights and water safety are legal-financial commitments, not design preferences.
```

### 23.4 Sanitation Interface

```yaml
sanitation_legal_finance_interface:
  required:
    - sewer_or_septic_approval
    - waste_hauling_contracts
    - hazardous_waste_review
    - composting_legality
    - greywater_legality
    - system_replacement_reserve
```

```text
Sanitation finance must include the cost of doing it legally.
```

### 23.5 Energy Interface

```yaml
energy_legal_finance_interface:
  required:
    - utility_interconnection
    - incentive_eligibility
    - battery_insurance_review
    - solar_ownership_model
    - power_purchase_or_lease_terms
    - replacement_reserve
```

```text
Energy resilience becomes extraction if the financing terms are predatory.
```

### 23.6 Care Interface

```yaml
care_legal_finance_interface:
  required:
    - care_room_boundary
    - liability_review
    - privacy_review
    - external_provider_contracts
    - transport_liability
    - emergency_support_fund
```

```text
Care support must not accidentally become unlicensed healthcare.
```

### 23.7 Maintenance Interface

```yaml
maintenance_legal_finance_interface:
  required:
    - replacement_reserve
    - professional_service_contracts
    - worker_safety_review
    - volunteer_vs_employee_classification_review
    - tool_library_liability
```

```text
Maintenance is where legal, labor, insurance, and finance collide.
```

### 23.8 Governance Interface

```yaml
governance_legal_finance_interface:
  required:
    - bylaws
    - membership_agreements
    - decision_rights
    - conflict_process
    - due_process
    - asset_lock
    - financial_transparency
```

```text
Governance ideals must become enforceable documents.
```

### 23.9 Labor & Time Interface

```yaml
labor_time_legal_finance_interface:
  required:
    - monthly_cash_required
    - required_wage_hours
    - labor_substitution_rules
    - paid_internal_role_review
    - volunteer_labor_risk
    - employment_law_review
```

```text
A low-cost life that depends on unlawful or invisible labor is not an alternative.
```

---

## 24. Automation-Favoring Requirements

Automation should make costs, rights, risks, and review requirements visible.

```yaml
automation_requirements:
  entity_structure_mapper:
    required: true
    purpose:
      - show_land_housing_operating_finance_layers
      - show_who_owns_what
      - show_approval_rights
      - show_capture_risks

  capital_stack_builder:
    required: true
    purpose:
      - track_sources_and_uses
      - detect_gap
      - label_risk
      - show_control_rights
      - flag_securities_review

  pro_forma_engine:
    required: true
    purpose:
      - monthly_cost_per_resident
      - debt_service
      - reserves
      - insurance
      - taxes
      - operating_costs
      - affordability_tests

  reserve_modeler:
    required: true
    purpose:
      - replacement_reserve
      - operating_reserve
      - emergency_reserve
      - deductible_reserve
      - reserve_drawdown_scenarios

  legal_review_trigger_engine:
    required: true
    purpose:
      - entity_documents
      - fundraising
      - securities
      - zoning
      - leases
      - cooperative_docs
      - employment
      - insurance
      - tax

  affordability_drift_monitor:
    required: true
    purpose:
      - monthly_cost_trends
      - insurance_shock
      - tax_shock
      - interest_rate_shock
      - maintenance_shortfall
      - reserve_shortfall

  debt_risk_simulator:
    required: true
    purpose:
      - interest_rate_change
      - refinancing_failure
      - revenue_shortfall
      - default_consequence
      - lender_control_rights

  rights_and_obligations_generator:
    required: true
    purpose:
      - resident_plain_language_summary
      - exit_rights
      - due_process
      - payment_obligations
      - contribution_obligations
      - limitations

  avoid:
    - app_drafting_final_legal_documents
    - app_promising_tax_exemption
    - app_recommending_investment_offerings
    - app_claiming_securities_compliance
    - app_automating_eviction_or_expulsion
    - opaque_affordability_scoring
    - hiding_reserve_shortfalls
```

### Automation Principle

```text
Automate visibility, scenario testing, and review triggers. Do not automate legal judgment.
```

---

## 25. Roles

```yaml
legal_land_finance_roles:
  land_stewardship_liaison:
    purpose: land entity, title, ground lease, land use restrictions
    required_backup: true

  legal_review_liaison:
    purpose: attorneys, documents, review calendar, issue tracking
    required_backup: true

  finance_steward:
    purpose: budget, pro forma, debt, capital stack, reserves
    required_backup: true

  affordability_steward:
    purpose: monthly cost, income/wage comparisons, affordability drift, hardship policy
    required_backup: true

  reserve_steward:
    purpose: operating, replacement, emergency, deductible, hardship reserves
    required_backup: true

  insurance_risk_steward:
    purpose: coverage map, exclusions, renewals, claims, risk mitigation
    required_backup: true

  tax_accounting_liaison:
    purpose: CPA review, tax calendar, filings, accounting controls
    required_backup: true

  permitting_land_use_liaison:
    purpose: zoning, permits, local authority coordination
    required_backup: true

  fundraising_compliance_liaison:
    purpose: grants, donations, member capital, securities review triggers
    required_backup: true
```

### Role Rule

```text
No one person should control land documents, budgets, debt, and resident payment enforcement.
```

---

## 26. Scenario Simulations

The legal land and finance module must support stress simulations.

```yaml
legal_land_finance_scenarios:
  normal_year:
    tests:
      - operating_budget
      - monthly_cost
      - reserves
      - debt_service
      - insurance
      - taxes
      - affordability

  insurance_shock:
    tests:
      - premium_increase
      - deductible_exposure
      - coverage_exclusions
      - monthly_cost_impact
      - reserve_drawdown

  tax_or_fee_shock:
    tests:
      - property_tax_increase
      - stormwater_or_utility_fee_increase
      - exemption_denial
      - affordability_impact

  interest_rate_or_refinance_shock:
    tests:
      - variable_rate_increase
      - refinancing_failure
      - debt_service_spike
      - default_risk

  maintenance_capex_shock:
    tests:
      - roof_replacement
      - water_system_failure
      - septic_failure
      - battery_replacement
      - reserve_adequacy
      - special_assessment_risk

  resident_income_shock:
    tests:
      - job_loss
      - illness
      - payment_shortfall
      - hardship_reserve
      - eviction_or_loss_of_access_risk

  land_sale_pressure:
    tests:
      - asset_lock
      - supermajority
      - lender_rights
      - legal_review
      - resident_displacement_risk

  founder_or_investor_pressure:
    tests:
      - control_rights
      - debt_claims
      - asset_transfer_attempt
      - member_approval
      - legal_defense

  zoning_denial:
    tests:
      - site_failure
      - redesign_options
      - permit_delay_cost
      - predevelopment_loss
      - alternate_site_strategy

  dissolution:
    tests:
      - asset_distribution
      - resident_transition
      - debt_satisfaction
      - reserve_use
      - mission_continuity
```

---

## 27. Legal Land & Finance Gates

The app should fail or warn based on legal-financial viability.

```yaml
legal_land_finance_gates:
  land_security_gate:
    fail_if:
      - no_secure_land_control
      - title_or_access_unresolved
      - land_can_be_sold_without_commons_review
      - residents_have_no_written_use_right
      - short_term_lease_for_core_housing

    warn_if:
      - founder_owned_land
      - investor_owned_land
      - unclear_easements
      - unresolved_environmental_or_access_issue

  asset_lock_gate:
    fail_if:
      - core_assets_can_be_privately_distributed
      - no_dissolution_rule
      - no_transfer_restrictions
      - no_resale_or_exit_formula_where_equity_exists
      - no_legal_review

  affordability_gate:
    fail_if:
      - monthly_core_cost_exceeds_conventional_baseline_without_clear_resilience_justification
      - reserves_excluded_from_cost_model
      - debt_service_unmodeled
      - insurance_or_taxes_unmodeled
      - bad_year_assessment_likely_to_displace_residents

    warn_if:
      - monthly_cost_rising_faster_than_local_income
      - affordability_depends_on_unpaid_labor
      - food_or_energy_savings_unverified

  reserve_gate:
    fail_if:
      - no_operating_reserve
      - no_replacement_reserve
      - no_emergency_repair_reserve
      - no_insurance_deductible_reserve
      - reserve_drawdown_has_no_replenishment_plan

    warn_if:
      - operating_reserve_below_3_months
      - replacement_reserve_not_based_on_asset_registry
      - reserve_contributions_deferred_to_future

  debt_gate:
    fail_if:
      - no_debt_service_model
      - no_default_consequence_map
      - debt_can_force_core_asset_sale_without_mitigation
      - balloon_maturity_without_takeout_plan
      - variable_rate_risk_unmodeled

    warn_if:
      - debt_per_resident_high
      - refinance_risk_high
      - lender_covenants_unclear
      - founder_personal_guarantee_required

  legal_review_gate:
    fail_if:
      - no_attorney_review_for_entity_structure
      - no_review_for_resident_rights
      - no_review_for_fundraising_or_member_capital
      - no_zoning_review
      - no_insurance_review

  securities_gate:
    fail_if:
      - public_profit_bearing_fundraise_without_review
      - tokenized_or_speculative_ownership_without_review
      - investors_receive_control_over_survival_assets
      - marketing_promises_returns_without_review

  insurance_gate:
    fail_if:
      - no_property_or_liability_review
      - no_D&O_or_governance_liability_review
      - no_workers_comp_review_where_labor_or_staffing_requires
      - high_risk_module_uninsurable

  tenure_gate:
    fail_if:
      - residents_can_be_removed_without_due_process
      - exit_value_unclear
      - payment_hardship_process_absent
      - financial_privacy_absent

  tax_gate:
    fail_if:
      - tax_exemption_assumed_without_approval
      - tax_obligations_unmodeled
      - no_CPA_or_tax_review

  permit_gate:
    fail_if:
      - zoning_prohibits_core_plan
      - water_or_sanitation_permit_path_absent
      - building_permit_path_absent
      - occupancy_classification_unknown_for_final_plan
```

---

## 28. App Modeling Boundary

The app should model legal, land, and finance at the level of **structure, risk, affordability, reserves, debt, review requirements, and scenario failures**, not final legal or financial advice.

### The App Should Model

```text
land-control options
ownership/use-right layers
resident rights
asset lock requirements
resale/exit formulas
capital stack
operating budget
capital budget
debt service
reserve requirements
monthly cost per resident
required wage hours
insurance categories
tax and fee placeholders
zoning and permit review triggers
fundraising risk
securities review triggers
hardship policies
default consequences
dissolution scenarios
professional review requirements
```

### The App Should Not Claim to Solve by Default

```text
legal entity selection
legal drafting
tax exemption
securities compliance
investment offering design
mortgage underwriting
insurance underwriting
zoning approval
building permit approval
eviction process
employment classification
cooperative incorporation
nonprofit formation
CLT formation
ground lease drafting
loan negotiation
tax advice
financial advice
```

### Principle

```text
The app should identify what must be true for anti-speculative legal and financial resilience.
Qualified attorneys, CPAs, lenders, insurance professionals, and local authorities must validate implementation.
```

---

## 29. Required Data Model

```yaml
LegalLandFinanceCommons:
  id: string
  population_served: integer

  land:
    land_control_type: owned | ground_lease | master_lease | public_land | donated_land | unknown
    land_steward_type: CLT_like | cooperative | nonprofit | public | private | unknown
    title_review_status: unknown | required | reviewed | issue_found
    zoning_status: unknown | allowed_by_right | conditional | rezoning_required | prohibited
    asset_lock_status: absent | provisional | drafted | reviewed | enforceable
    transfer_restrictions: boolean
    dissolution_rule: boolean

  resident_rights:
    tenure_type: cooperative_share | leasehold | rental_membership | deed_restricted | unknown
    written_use_agreement: boolean
    due_process: boolean
    exit_formula: boolean
    hardship_policy: boolean
    financial_privacy: boolean
    anti_retaliation: boolean

  capital_budget:
    total_development_cost: number
    land_cost: number
    hard_costs: number
    soft_costs: number
    infrastructure_costs: number
    contingency: number
    startup_reserves: number
    financing_gap: number
    cost_per_resident: number
    cost_per_unit: number

  operating_budget:
    monthly_operating_cost: number
    monthly_cost_per_resident: number
    debt_service_monthly: number
    insurance_monthly: number
    taxes_fees_monthly: number
    utilities_monthly: number
    maintenance_monthly: number
    admin_monthly: number
    reserve_contribution_monthly: number

  reserves:
    operating_reserve_months: number
    replacement_reserve_balance: number
    replacement_reserve_annual_contribution: number
    emergency_repair_reserve: number
    insurance_deductible_reserve: number
    hardship_reserve: number
    reserve_status: pass | warn | fail

  debt:
    total_debt: number
    interest_rate: number
    fixed_or_variable: fixed | variable | mixed | unknown
    maturity_years: number
    balloon_payment: boolean
    DSCR: number
    loan_to_value: number
    debt_per_resident: number
    collateral_core_assets: boolean
    default_consequence_map: boolean

  capital_stack:
    grants: number
    donations: number
    public_subsidy: number
    member_capital: number
    mission_debt: number
    commercial_debt: number
    investor_capital: number
    securities_review_required: boolean
    control_rights_to_external_capital: boolean

  insurance_tax:
    property_insurance_review: boolean
    liability_review: boolean
    D_and_O_review: boolean
    workers_comp_review: boolean
    regional_hazard_review: boolean
    CPA_tax_review: boolean
    tax_status: unknown | taxable | exempt_applied | exempt_approved | mixed

  professional_review:
    attorney_review: boolean
    CPA_review: boolean
    lender_review: boolean
    insurance_review: boolean
    zoning_review: boolean
    authority_review: boolean

  outputs:
    land_security_status: pass | warn | fail
    affordability_status: pass | warn | fail
    reserve_status: pass | warn | fail
    debt_risk_status: pass | warn | fail
    legal_review_status: pass | warn | fail
    anti_speculation_status: pass | warn | fail
    monthly_cost_per_resident: number
    required_wage_hours_to_cover_core_cost: number
    bank_pressure_risk_score: number
    life_burden_reduction_score: number
    complexity_score: number
```

---

## 30. Required App Outputs

```yaml
required_outputs:
  - legal_land_finance_summary
  - legal_layer_map
  - land_control_report
  - resident_rights_report
  - asset_lock_report
  - capital_budget_report
  - operating_budget_report
  - monthly_cost_per_resident_report
  - required_wage_hours_report
  - capital_stack_report
  - debt_risk_report
  - reserve_adequacy_report
  - insurance_review_report
  - tax_review_report
  - zoning_permit_risk_report
  - securities_fundraising_review_report
  - hardship_policy_report
  - affordability_drift_report
  - professional_review_requirements
  - scenario_failure_report
  - visualization_bundle_metadata
```

---

## 31. Visualization Requirements

The legal and finance module should export enough data for a dashboard to show who owns what, what costs what, and where capture pressure exists.

```yaml
visualization_requirements:
  graph_objects:
    - land_steward_entity
    - resident_housing_entity
    - operating_commons_entity
    - lenders
    - funders
    - insurers
    - residents
    - core_assets
    - reserves
    - decision_rights

  overlays:
    - ownership_layer_map
    - asset_lock_status
    - debt_pressure
    - monthly_cost_per_resident
    - reserve_health
    - affordability_drift
    - land_sale_risk
    - investor_control_risk
    - legal_review_required
    - permit_blockers
    - insurance_exclusions

  scenario_playback:
    - insurance_shock
    - tax_shock
    - refinance_failure
    - maintenance_capex_shock
    - resident_income_shock
    - land_sale_pressure
    - founder_or_investor_pressure
    - zoning_denial
    - dissolution
```

---

## 32. Best Default Requirements Summary

```yaml
MinimumViableLegalLandFinanceCommons:
  population:
    first_serious_model: 80
    valid_range: 50-150

  philosophy:
    land_outside_speculation: true
    housing_affordability_preserved: true
    resident_security_required: true
    investor_control_of_floor: false
    legal_review_required: true
    reserves_count_as_cost: true
    debt_bounded: true
    hardship_protection: required

  legal_stack:
    land_stewardship: CLT_like_or_mission_locked
    housing_use_rights: limited_equity_or_shared_equity
    operating_commons: resident_controlled_service_entity
    final_structure: attorney_required

  finance:
    capital_stack: mission_aligned
    public_or_philanthropic_support: preferred
    low_interest_debt: preferred
    speculative_equity: rejected
    investor_control: rejected
    founder_personal_guarantee_as_permanent_structure: rejected

  reserves:
    operating_reserve: 3-6_months_target
    replacement_reserve: required_from_day_one
    emergency_repair_reserve: required
    insurance_deductible_reserve: required
    hardship_reserve: preferred

  protections:
    asset_lock: required
    resale_exit_formula: required_where_equity_exists
    due_process: required
    exit_rights: required
    affordability_drift_monitor: required
    debt_thresholds: required
    securities_review_triggers: required
    insurance_review: required
    zoning_review: required

  automation:
    entity_structure_mapper: required
    capital_stack_builder: required
    pro_forma_engine: required
    reserve_modeler: required
    legal_review_trigger_engine: required
    affordability_drift_monitor: required
    debt_risk_simulator: required
    rights_and_obligations_generator: required

  gates:
    land_security_gate: required
    asset_lock_gate: required
    affordability_gate: required
    reserve_gate: required
    debt_gate: required
    legal_review_gate: required
    securities_gate: required
    insurance_gate: required
    tenure_gate: required
    tax_gate: required
    permit_gate: required
```

---

## 33. Design Maxims

```text
Do not let land become the new landlord.

Do not let finance become the hidden sovereign.

Do not call it affordable if reserves are missing.

Do not treat deferred maintenance as savings.

Do not accept speculative equity for survival infrastructure.

Do not make resident security depend on founder goodwill.

Do not raise money in ways that recreate the wealth game.

Do not assume tax exemption.

Do not assume zoning.

Do not assume insurance.

Do not assume a bank will be patient.

Do not hide debt.

Do not hide soft costs.

Do not hide bad-year assessments.

Do not let exit value destroy the next resident's affordability.

Do not use legal complexity to obscure power.

Separate land, use rights, operations, and finance.

Map who owns what.

Map who can force what.

Fund the boring reserves.

Make the monthly floor cost brutally visible.

Stress-test bad financial years.

Keep the floor outside speculation.
```

---

## 34. Open Questions for Iteration

```text
1. Should the default model prioritize CLT + limited-equity cooperative, or support CLT, cooperative, rental, and deed-restricted profiles equally?
2. What monthly core cost per resident would prove the model against local Richmond-area baselines?
3. Should residents build equity at all, or should the design prioritize the lowest possible entry and monthly cost?
4. What exit formula best balances resident dignity and future affordability?
5. Should hardship reserves be required or preferred?
6. What operating reserve target should be required: 3 months, 6 months, or risk-based?
7. How should member labor be valued financially, if at all?
8. Should external capital ever receive a capped return, or only interest/debt repayment?
9. Should CIaC reject all investor equity for core assets?
10. What debt service coverage threshold should the app require?
11. How should the app model insurance unavailability or climate-risk premium shocks?
12. Should the app model property taxes by jurisdiction or only flag professional review in v0?
13. Should the first pilot assume rural land, peri-urban land, institutional land, or public land?
14. What legal-financial failure would make the entire CIaC design morally invalid?
```

---

## 35. Source Notes

The research basis for this draft includes:

- Community land trust model descriptions and shared-equity housing resources.
- Limited-equity cooperative housing resources.
- Cooperative principles from ICA / USDA-style cooperative guidance.
- IRS organizational and dissolution requirements for 501(c)(3) asset dedication.
- HUD / affordable-housing replacement reserve concepts.
- Cooperative housing development guidance on operating, replacement, and training reserves.
- Shared-equity housing guides from national housing organizations.
- Securities-law concepts such as investment contracts and expectations of profit from others' efforts.
- Affordable housing finance practices, including operating reserves, replacement reserves, capital needs, and debt-service risk.
