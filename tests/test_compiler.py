from __future__ import annotations

import copy
import unittest
from pathlib import Path

from ciac.compiler import CompileError, compile_plan, load_patterns
from ciac.io import load_data
from ciac.validation import validate_data


ROOT = Path(__file__).resolve().parents[1]


class CompilerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.patterns = load_patterns(ROOT / "patterns")
        self.site = load_data(ROOT / "examples" / "site_profiles" / "micro_commons_5_households.yaml")
        self.seasonal_profile = load_data(ROOT / "seasonal_profiles" / "humid_temperate_provisional.yaml")
        self.household_profile = load_data(ROOT / "household_profiles" / "micro_commons_households_v0.yaml")
        self.spatial_profile = load_data(ROOT / "spatial_profiles" / "micro_commons_spatial_v0.yaml")

    def test_happy_path_compiles_5_household_plan(self) -> None:
        plan = compile_plan(self.site, self.patterns)
        self.assertEqual(plan["kind"], "CompiledPlan")
        self.assertEqual(plan["source_site_profile"], "micro_commons_5_households")
        self.assertEqual(plan["missing_dependencies"], [])
        self.assertIn("well_house", plan["dependency_order"])
        self.assertLess(plan["dependency_order"].index("well_house"), plan["dependency_order"].index("shared_bathhouse"))
        self.assertTrue(validate_data(plan, "compiled").ok)

    def test_compile_refuses_missing_water_and_sanitation_dependencies(self) -> None:
        site = copy.deepcopy(self.site)
        site["selected_patterns"] = ["solar_shed", "starter_dwelling", "community_kitchen"]
        with self.assertRaises(CompileError) as raised:
            compile_plan(site, self.patterns)
        self.assertIsNotNone(raised.exception.plan)
        missing_ids = {dep["dependency_id"] for dep in raised.exception.plan["missing_dependencies"]}
        self.assertIn("shared_bathhouse", missing_ids)
        self.assertIn("well_house", missing_ids)

    def test_compiled_json_shape_is_stable_for_downstream_consumers(self) -> None:
        plan = compile_plan(self.site, self.patterns)
        self.assertEqual(
            list(plan.keys()),
            [
                "kind",
                "id",
                "source_site_profile",
                "generated_by",
                "provisional",
                "site_summary",
                "selected_patterns",
                "dependency_order",
                "missing_dependencies",
                "phases",
                "maintenance_calendar",
                "role_burden",
                "layout_graph",
                "risk_register",
                "simulation_inputs",
                "promotion_status",
            ],
        )

    def test_compiled_plan_exports_simulation_inputs(self) -> None:
        plan = compile_plan(self.site, self.patterns)
        simulation_inputs = plan["simulation_inputs"]
        self.assertTrue(simulation_inputs["provisional"])
        self.assertIn("well_house", simulation_inputs["resource_effects_by_pattern"])
        self.assertIn("water_liters_per_day", simulation_inputs["resource_effects_by_pattern"]["well_house"])
        self.assertIn("emergency_water_reserve", simulation_inputs["storage_by_pattern"])
        self.assertEqual(simulation_inputs["storage_by_pattern"]["emergency_water_reserve"][0]["resource"], "water_liters")

    def test_compile_can_embed_matching_seasonal_profile(self) -> None:
        plan = compile_plan(self.site, self.patterns, self.seasonal_profile)
        self.assertEqual(plan["site_summary"]["seasonal_profile_id"], "humid_temperate_provisional")
        self.assertEqual(plan["simulation_inputs"]["seasonal_profile"]["kind"], "SeasonalProfile")
        self.assertTrue(validate_data(plan, "compiled").ok)

    def test_compile_rejects_wrong_seasonal_profile_reference(self) -> None:
        site = copy.deepcopy(self.site)
        site["seasonal_profile_id"] = "different_profile"
        with self.assertRaises(CompileError):
            compile_plan(site, self.patterns, self.seasonal_profile)

    def test_compile_can_embed_matching_household_profile(self) -> None:
        plan = compile_plan(self.site, self.patterns, self.seasonal_profile, self.household_profile)
        self.assertEqual(plan["site_summary"]["household_profile_id"], "micro_commons_households_v0")
        self.assertEqual(plan["simulation_inputs"]["household_profile"]["kind"], "HouseholdProfile")
        self.assertTrue(validate_data(plan, "compiled").ok)

    def test_compile_rejects_household_population_mismatch(self) -> None:
        household_profile = copy.deepcopy(self.household_profile)
        household_profile["households"][0]["adults"] = 3
        with self.assertRaises(CompileError):
            compile_plan(self.site, self.patterns, self.seasonal_profile, household_profile)

    def test_compile_can_emit_layout_graph_from_spatial_profile(self) -> None:
        plan = compile_plan(self.site, self.patterns, self.seasonal_profile, self.household_profile, self.spatial_profile)
        layout = plan["layout_graph"]
        self.assertEqual(layout["source_spatial_profile"], "micro_commons_spatial_v0")
        self.assertEqual(len(layout["nodes"]), len(self.site["selected_patterns"]))
        self.assertTrue(any(edge["relationship"] == "adjacency" for edge in layout["edges"]))
        self.assertTrue(any(edge["relationship"] == "separation" for edge in layout["edges"]))
        self.assertIn("survey", " ".join(layout["unresolved_spatial_issues"]))
        self.assertTrue(validate_data(plan, "compiled").ok)

    def test_can_compile_dignified_village_block_housing_pattern(self) -> None:
        site = copy.deepcopy(self.site)
        site["selected_patterns"] = [
            pattern_id
            for pattern_id in site["selected_patterns"]
            if pattern_id != "starter_dwelling"
        ]
        site["selected_patterns"].append("dignified_village_block")
        site["resolved_external_dependencies"].extend(
            [
                "residential_building_code_review",
                "accessibility_review",
                "fire_life_safety_review",
            ]
        )

        plan = compile_plan(site, self.patterns)

        self.assertIn("dignified_village_block", plan["selected_patterns"])
        self.assertNotIn("starter_dwelling", plan["selected_patterns"])
        self.assertEqual(plan["missing_dependencies"], [])
        self.assertEqual(
            plan["simulation_inputs"]["resource_effects_by_pattern"]["dignified_village_block"]["energy_kwh_per_day"],
            -90,
        )
        self.assertTrue(validate_data(plan, "compiled").ok)

    def test_can_compile_hybrid_food_commons_pattern(self) -> None:
        site = copy.deepcopy(self.site)
        site["selected_patterns"].append("hybrid_food_commons")
        site["resolved_external_dependencies"].extend(
            [
                "regional_food_procurement_plan",
                "nutrition_review",
            ]
        )

        plan = compile_plan(site, self.patterns)

        self.assertIn("hybrid_food_commons", plan["selected_patterns"])
        self.assertEqual(plan["missing_dependencies"], [])
        self.assertEqual(
            plan["simulation_inputs"]["resource_effects_by_pattern"]["hybrid_food_commons"]["food_servings_per_day"],
            60,
        )
        self.assertEqual(
            plan["simulation_inputs"]["storage_by_pattern"]["hybrid_food_commons"][0]["reserve_floor"],
            7200,
        )
        self.assertTrue(validate_data(plan, "compiled").ok)

    def test_can_compile_protein_commons_supplement_pattern(self) -> None:
        site = copy.deepcopy(self.site)
        site["selected_patterns"].extend(
            [
                "hybrid_food_commons",
                "protein_commons_supplement",
            ]
        )
        site["resolved_external_dependencies"].extend(
            [
                "regional_food_procurement_plan",
                "nutrition_review",
                "resident_acceptance_review",
            ]
        )

        plan = compile_plan(site, self.patterns)

        self.assertIn("protein_commons_supplement", plan["selected_patterns"])
        self.assertEqual(plan["missing_dependencies"], [])
        self.assertEqual(
            plan["simulation_inputs"]["resource_effects_by_pattern"]["protein_commons_supplement"]["food_servings_per_day"],
            80,
        )
        self.assertEqual(
            plan["simulation_inputs"]["storage_by_pattern"]["protein_commons_supplement"][0]["reserve_floor"],
            2400,
        )
        self.assertTrue(validate_data(plan, "compiled").ok)

    def test_can_compile_resilient_water_commons_pattern(self) -> None:
        site = copy.deepcopy(self.site)
        site["selected_patterns"].append("resilient_water_commons")
        site["resolved_external_dependencies"].extend(
            [
                "water_public_health_review",
                "plumbing_code_review",
                "delivered_water_fallback_plan",
                "onsite_reuse_review",
            ]
        )

        plan = compile_plan(site, self.patterns)

        self.assertIn("resilient_water_commons", plan["selected_patterns"])
        self.assertEqual(plan["missing_dependencies"], [])
        self.assertEqual(
            plan["simulation_inputs"]["storage_by_pattern"]["resilient_water_commons"][0]["capacity"],
            9085,
        )
        self.assertEqual(
            plan["simulation_inputs"]["resource_effects_by_pattern"]["resilient_water_commons"]["energy_kwh_per_day"],
            -8,
        )
        self.assertTrue(validate_data(plan, "compiled").ok)

    def test_can_compile_hygienic_circular_commons_pattern(self) -> None:
        site = copy.deepcopy(self.site)
        site["selected_patterns"].append("hygienic_circular_commons")
        site["resolved_external_dependencies"].extend(
            [
                "wastewater_professional_review",
                "hazardous_waste_dropoff_plan",
                "worker_safety_training",
                "greywater_reuse_review",
            ]
        )

        plan = compile_plan(site, self.patterns)

        self.assertIn("hygienic_circular_commons", plan["selected_patterns"])
        self.assertEqual(plan["missing_dependencies"], [])
        self.assertEqual(
            plan["simulation_inputs"]["resource_effects_by_pattern"]["hygienic_circular_commons"]["water_liters_per_day"],
            -1200,
        )
        self.assertIn(
            "sanitation",
            plan["simulation_inputs"]["critical_resources_by_pattern"]["hygienic_circular_commons"],
        )
        self.assertTrue(validate_data(plan, "compiled").ok)

    def test_can_compile_critical_load_energy_commons_pattern(self) -> None:
        site = copy.deepcopy(self.site)
        site["selected_patterns"].append("critical_load_energy_commons")
        site["resolved_external_dependencies"].extend(
            [
                "battery_fire_safety_review",
                "utility_interconnection_review",
                "thermal_resilience_review",
                "generator_fuel_plan",
            ]
        )

        plan = compile_plan(site, self.patterns)

        self.assertIn("critical_load_energy_commons", plan["selected_patterns"])
        self.assertEqual(plan["missing_dependencies"], [])
        self.assertEqual(
            plan["simulation_inputs"]["resource_effects_by_pattern"]["critical_load_energy_commons"]["energy_kwh_per_day"],
            180,
        )
        self.assertEqual(
            plan["simulation_inputs"]["storage_by_pattern"]["critical_load_energy_commons"][0]["reserve_floor"],
            60,
        )
        self.assertTrue(validate_data(plan, "compiled").ok)

    def test_can_compile_maintainable_commons_spine_pattern(self) -> None:
        site = copy.deepcopy(self.site)
        site["selected_patterns"].append("maintainable_commons_spine")
        site["resolved_external_dependencies"].extend(
            [
                "professional_service_matrix",
                "maintenance_budget_reserve_plan",
            ]
        )

        plan = compile_plan(site, self.patterns)

        self.assertIn("maintainable_commons_spine", plan["selected_patterns"])
        self.assertEqual(plan["missing_dependencies"], [])
        self.assertEqual(
            plan["simulation_inputs"]["resource_effects_by_pattern"]["maintainable_commons_spine"]["energy_kwh_per_day"],
            -4,
        )
        self.assertIn(
            "maintenance",
            plan["simulation_inputs"]["critical_resources_by_pattern"]["maintainable_commons_spine"],
        )
        self.assertTrue(validate_data(plan, "compiled").ok)

    def test_can_compile_commons_stewardship_protocol_pattern(self) -> None:
        site = copy.deepcopy(self.site)
        site["selected_patterns"].extend(
            [
                "maintainable_commons_spine",
                "commons_stewardship_protocol",
            ]
        )
        site["resolved_external_dependencies"].extend(
            [
                "professional_service_matrix",
                "maintenance_budget_reserve_plan",
                "legal_governance_review",
                "resident_membership_charter",
                "finance_transparency_review",
                "conflict_safeguarding_review",
                "data_privacy_review",
            ]
        )

        plan = compile_plan(site, self.patterns)

        self.assertIn("commons_stewardship_protocol", plan["selected_patterns"])
        self.assertEqual(plan["missing_dependencies"], [])
        self.assertEqual(
            plan["simulation_inputs"]["resource_effects_by_pattern"]["commons_stewardship_protocol"]["energy_kwh_per_day"],
            -1,
        )
        self.assertIn(
            "maintenance",
            plan["simulation_inputs"]["critical_resources_by_pattern"]["commons_stewardship_protocol"],
        )
        self.assertTrue(validate_data(plan, "compiled").ok)

    def test_can_compile_life_burden_ledger_pattern(self) -> None:
        site = copy.deepcopy(self.site)
        site["selected_patterns"].extend(
            [
                "maintainable_commons_spine",
                "commons_stewardship_protocol",
                "life_burden_ledger",
            ]
        )
        site["resolved_external_dependencies"].extend(
            [
                "professional_service_matrix",
                "maintenance_budget_reserve_plan",
                "legal_governance_review",
                "resident_membership_charter",
                "finance_transparency_review",
                "conflict_safeguarding_review",
                "data_privacy_review",
                "resident_time_use_baseline",
                "labor_privacy_review",
                "accommodation_policy_review",
                "labor_fairness_review",
            ]
        )

        plan = compile_plan(site, self.patterns)

        self.assertIn("life_burden_ledger", plan["selected_patterns"])
        self.assertEqual(plan["missing_dependencies"], [])
        self.assertEqual(
            plan["simulation_inputs"]["resource_effects_by_pattern"]["life_burden_ledger"]["energy_kwh_per_day"],
            -1,
        )
        self.assertIn(
            "maintenance",
            plan["simulation_inputs"]["critical_resources_by_pattern"]["life_burden_ledger"],
        )
        self.assertTrue(validate_data(plan, "compiled").ok)

    def test_can_compile_anti_speculative_civic_floor_pattern(self) -> None:
        site = copy.deepcopy(self.site)
        site["selected_patterns"].extend(
            [
                "maintainable_commons_spine",
                "commons_stewardship_protocol",
                "anti_speculative_civic_floor",
            ]
        )
        site["resolved_external_dependencies"].extend(
            [
                "professional_service_matrix",
                "maintenance_budget_reserve_plan",
                "legal_governance_review",
                "resident_membership_charter",
                "finance_transparency_review",
                "conflict_safeguarding_review",
                "data_privacy_review",
                "land_tenure_legal_review",
                "finance_affordability_review",
                "tax_accounting_review",
                "insurance_liability_review",
                "securities_fundraising_review",
            ]
        )

        plan = compile_plan(site, self.patterns)

        self.assertIn("anti_speculative_civic_floor", plan["selected_patterns"])
        self.assertEqual(plan["missing_dependencies"], [])
        self.assertEqual(
            plan["simulation_inputs"]["resource_effects_by_pattern"]["anti_speculative_civic_floor"]["energy_kwh_per_day"],
            -1,
        )
        self.assertIn(
            "maintenance",
            plan["simulation_inputs"]["critical_resources_by_pattern"]["anti_speculative_civic_floor"],
        )
        self.assertTrue(validate_data(plan, "compiled").ok)

    def test_can_compile_standardized_low_burden_build_system_pattern(self) -> None:
        site = copy.deepcopy(self.site)
        site["selected_patterns"].extend(
            [
                "maintainable_commons_spine",
                "commons_stewardship_protocol",
                "anti_speculative_civic_floor",
                "standardized_low_burden_build_system",
            ]
        )
        site["resolved_external_dependencies"].extend(
            [
                "professional_service_matrix",
                "maintenance_budget_reserve_plan",
                "legal_governance_review",
                "resident_membership_charter",
                "finance_transparency_review",
                "conflict_safeguarding_review",
                "data_privacy_review",
                "land_tenure_legal_review",
                "finance_affordability_review",
                "tax_accounting_review",
                "insurance_liability_review",
                "securities_fundraising_review",
                "structural_engineering_review",
                "building_code_fire_review",
                "envelope_moisture_review",
                "fabrication_vendor_review",
                "material_health_review",
                "embodied_carbon_review",
            ]
        )

        plan = compile_plan(site, self.patterns)

        self.assertIn("standardized_low_burden_build_system", plan["selected_patterns"])
        self.assertEqual(plan["missing_dependencies"], [])
        self.assertEqual(
            plan["simulation_inputs"]["resource_effects_by_pattern"]["standardized_low_burden_build_system"]["energy_kwh_per_day"],
            -15,
        )
        self.assertIn(
            "energy",
            plan["simulation_inputs"]["critical_resources_by_pattern"]["standardized_low_burden_build_system"],
        )
        self.assertTrue(validate_data(plan, "compiled").ok)

    def test_can_compile_pedestrian_first_access_commons_pattern(self) -> None:
        site = copy.deepcopy(self.site)
        site["selected_patterns"].extend(
            [
                "maintainable_commons_spine",
                "commons_stewardship_protocol",
                "anti_speculative_civic_floor",
                "life_burden_ledger",
                "pedestrian_first_access_commons",
            ]
        )
        site["resolved_external_dependencies"].extend(
            [
                "professional_service_matrix",
                "maintenance_budget_reserve_plan",
                "legal_governance_review",
                "resident_membership_charter",
                "finance_transparency_review",
                "conflict_safeguarding_review",
                "data_privacy_review",
                "land_tenure_legal_review",
                "finance_affordability_review",
                "tax_accounting_review",
                "insurance_liability_review",
                "securities_fundraising_review",
                "resident_time_use_baseline",
                "labor_privacy_review",
                "accommodation_policy_review",
                "labor_fairness_review",
                "accessibility_mobility_review",
                "emergency_access_fire_review",
                "civil_site_access_review",
                "shared_vehicle_insurance_review",
                "external_access_transport_plan",
                "mobility_privacy_review",
            ]
        )

        plan = compile_plan(site, self.patterns)

        self.assertIn("pedestrian_first_access_commons", plan["selected_patterns"])
        self.assertEqual(plan["missing_dependencies"], [])
        self.assertEqual(
            plan["simulation_inputs"]["resource_effects_by_pattern"]["pedestrian_first_access_commons"]["energy_kwh_per_day"],
            -4,
        )
        self.assertIn(
            "maintenance",
            plan["simulation_inputs"]["critical_resources_by_pattern"]["pedestrian_first_access_commons"],
        )
        self.assertTrue(validate_data(plan, "compiled").ok)

    def test_can_compile_civic_skill_lattice_pattern(self) -> None:
        site = copy.deepcopy(self.site)
        site["selected_patterns"].extend(
            [
                "maintainable_commons_spine",
                "commons_stewardship_protocol",
                "life_burden_ledger",
                "civic_skill_lattice",
            ]
        )
        site["resolved_external_dependencies"].extend(
            [
                "professional_service_matrix",
                "maintenance_budget_reserve_plan",
                "legal_governance_review",
                "resident_membership_charter",
                "finance_transparency_review",
                "conflict_safeguarding_review",
                "data_privacy_review",
                "resident_time_use_baseline",
                "labor_privacy_review",
                "accommodation_policy_review",
                "labor_fairness_review",
                "safety_training_review",
                "credential_boundary_review",
                "learning_privacy_review",
                "accessibility_learning_review",
                "youth_education_legal_review",
            ]
        )

        plan = compile_plan(site, self.patterns)

        self.assertIn("civic_skill_lattice", plan["selected_patterns"])
        self.assertEqual(plan["missing_dependencies"], [])
        self.assertEqual(
            plan["simulation_inputs"]["resource_effects_by_pattern"]["civic_skill_lattice"]["energy_kwh_per_day"],
            -1,
        )
        self.assertIn(
            "maintenance",
            plan["simulation_inputs"]["critical_resources_by_pattern"]["civic_skill_lattice"],
        )
        self.assertTrue(validate_data(plan, "compiled").ok)

    def test_can_compile_belonging_without_coercion_commons_pattern(self) -> None:
        site = copy.deepcopy(self.site)
        site["selected_patterns"].extend(
            [
                "maintainable_commons_spine",
                "commons_stewardship_protocol",
                "life_burden_ledger",
                "civic_skill_lattice",
                "belonging_without_coercion_commons",
            ]
        )
        site["resolved_external_dependencies"].extend(
            [
                "professional_service_matrix",
                "maintenance_budget_reserve_plan",
                "legal_governance_review",
                "resident_membership_charter",
                "finance_transparency_review",
                "conflict_safeguarding_review",
                "data_privacy_review",
                "resident_time_use_baseline",
                "labor_privacy_review",
                "accommodation_policy_review",
                "labor_fairness_review",
                "safety_training_review",
                "credential_boundary_review",
                "learning_privacy_review",
                "accessibility_learning_review",
                "youth_education_legal_review",
                "social_privacy_review",
                "accessibility_inclusion_review",
                "cultural_pluralism_review",
                "hospitality_safeguarding_review",
            ]
        )

        plan = compile_plan(site, self.patterns)

        self.assertIn("belonging_without_coercion_commons", plan["selected_patterns"])
        self.assertEqual(plan["missing_dependencies"], [])
        self.assertEqual(
            plan["simulation_inputs"]["resource_effects_by_pattern"]["belonging_without_coercion_commons"]["energy_kwh_per_day"],
            -1,
        )
        self.assertIn(
            "maintenance",
            plan["simulation_inputs"]["critical_resources_by_pattern"]["belonging_without_coercion_commons"],
        )
        self.assertTrue(validate_data(plan, "compiled").ok)

    def test_can_compile_graceful_degradation_engine_pattern(self) -> None:
        site = copy.deepcopy(self.site)
        site["selected_patterns"].extend(
            [
                "hybrid_food_commons",
                "resilient_water_commons",
                "hygienic_circular_commons",
                "critical_load_energy_commons",
                "maintainable_commons_spine",
                "commons_stewardship_protocol",
                "anti_speculative_civic_floor",
                "life_burden_ledger",
                "pedestrian_first_access_commons",
                "civic_skill_lattice",
                "belonging_without_coercion_commons",
                "graceful_degradation_engine",
            ]
        )
        site["resolved_external_dependencies"].extend(
            [
                "regional_food_procurement_plan",
                "nutrition_review",
                "water_public_health_review",
                "plumbing_code_review",
                "delivered_water_fallback_plan",
                "onsite_reuse_review",
                "wastewater_professional_review",
                "hazardous_waste_dropoff_plan",
                "worker_safety_training",
                "greywater_reuse_review",
                "battery_fire_safety_review",
                "utility_interconnection_review",
                "thermal_resilience_review",
                "generator_fuel_plan",
                "professional_service_matrix",
                "maintenance_budget_reserve_plan",
                "legal_governance_review",
                "resident_membership_charter",
                "finance_transparency_review",
                "conflict_safeguarding_review",
                "data_privacy_review",
                "land_tenure_legal_review",
                "finance_affordability_review",
                "tax_accounting_review",
                "insurance_liability_review",
                "securities_fundraising_review",
                "resident_time_use_baseline",
                "labor_privacy_review",
                "accommodation_policy_review",
                "labor_fairness_review",
                "accessibility_mobility_review",
                "emergency_access_fire_review",
                "civil_site_access_review",
                "shared_vehicle_insurance_review",
                "external_access_transport_plan",
                "mobility_privacy_review",
                "safety_training_review",
                "credential_boundary_review",
                "learning_privacy_review",
                "accessibility_learning_review",
                "youth_education_legal_review",
                "social_privacy_review",
                "accessibility_inclusion_review",
                "cultural_pluralism_review",
                "hospitality_safeguarding_review",
                "emergency_management_review",
                "local_hazard_climate_review",
                "high_need_resident_resilience_review",
                "mutual_aid_external_support_plan",
            ]
        )

        plan = compile_plan(site, self.patterns)

        self.assertIn("graceful_degradation_engine", plan["selected_patterns"])
        self.assertEqual(plan["missing_dependencies"], [])
        self.assertEqual(
            plan["simulation_inputs"]["resource_effects_by_pattern"]["graceful_degradation_engine"]["energy_kwh_per_day"],
            -1,
        )
        self.assertIn(
            "water",
            plan["simulation_inputs"]["critical_resources_by_pattern"]["graceful_degradation_engine"],
        )
        self.assertTrue(validate_data(plan, "compiled").ok)

    def test_compile_rejects_spatial_profile_missing_selected_placement(self) -> None:
        spatial_profile = copy.deepcopy(self.spatial_profile)
        spatial_profile["placements"] = [
            placement for placement in spatial_profile["placements"] if placement["pattern_id"] != "greenhouse"
        ]
        with self.assertRaises(CompileError):
            compile_plan(self.site, self.patterns, self.seasonal_profile, self.household_profile, spatial_profile)


if __name__ == "__main__":
    unittest.main()
