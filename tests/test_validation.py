from __future__ import annotations

import copy
import unittest
from pathlib import Path

from ciac.io import load_data
from ciac.validation import validate_data, validate_pattern_library


ROOT = Path(__file__).resolve().parents[1]


class ValidationTests(unittest.TestCase):
    def test_seed_pattern_is_valid(self) -> None:
        pattern = load_data(ROOT / "patterns" / "starter_dwelling.yaml")
        report = validate_data(pattern, "starter_dwelling")
        self.assertTrue(report.ok, [issue.message for issue in report.issues])

    def test_dignified_village_block_pattern_is_valid(self) -> None:
        pattern = load_data(ROOT / "patterns" / "dignified_village_block.yaml")
        report = validate_data(pattern, "dignified_village_block")

        self.assertTrue(report.ok, [issue.message for issue in report.issues])
        self.assertIn("privacy", pattern["mdl_categories"])
        self.assertIn("community_kitchen", [dependency["id"] for dependency in pattern["dependencies"]])

    def test_hybrid_food_commons_pattern_is_valid(self) -> None:
        pattern = load_data(ROOT / "patterns" / "hybrid_food_commons.yaml")
        report = validate_data(pattern, "hybrid_food_commons")

        self.assertTrue(report.ok, [issue.message for issue in report.issues])
        self.assertIn("food", pattern["mdl_categories"])
        self.assertIn("regional_food_procurement_plan", [dependency["id"] for dependency in pattern["dependencies"]])

    def test_resilient_water_commons_pattern_is_valid(self) -> None:
        pattern = load_data(ROOT / "patterns" / "resilient_water_commons.yaml")
        report = validate_data(pattern, "resilient_water_commons")

        self.assertTrue(report.ok, [issue.message for issue in report.issues])
        self.assertIn("water", pattern["mdl_categories"])
        self.assertIn("water_public_health_review", [dependency["id"] for dependency in pattern["dependencies"]])
        self.assertEqual(pattern["simulation"]["storage"][0]["quality"]["review_dependency"], "water_public_health")

    def test_hygienic_circular_commons_pattern_is_valid(self) -> None:
        pattern = load_data(ROOT / "patterns" / "hygienic_circular_commons.yaml")
        report = validate_data(pattern, "hygienic_circular_commons")

        self.assertTrue(report.ok, [issue.message for issue in report.issues])
        self.assertIn("sanitation", pattern["mdl_categories"])
        self.assertIn("wastewater_professional_review", [dependency["id"] for dependency in pattern["dependencies"]])
        self.assertIn("hazardous_waste_dropoff_plan", [dependency["id"] for dependency in pattern["dependencies"]])

    def test_critical_load_energy_commons_pattern_is_valid(self) -> None:
        pattern = load_data(ROOT / "patterns" / "critical_load_energy_commons.yaml")
        report = validate_data(pattern, "critical_load_energy_commons")

        self.assertTrue(report.ok, [issue.message for issue in report.issues])
        self.assertIn("energy", pattern["mdl_categories"])
        self.assertIn("battery_fire_safety_review", [dependency["id"] for dependency in pattern["dependencies"]])
        self.assertEqual(pattern["simulation"]["storage"][0]["resource"], "energy_kwh")

    def test_maintainable_commons_spine_pattern_is_valid(self) -> None:
        pattern = load_data(ROOT / "patterns" / "maintainable_commons_spine.yaml")
        report = validate_data(pattern, "maintainable_commons_spine")

        self.assertTrue(report.ok, [issue.message for issue in report.issues])
        self.assertIn("commons", pattern["mdl_categories"])
        self.assertIn("professional_service_matrix", [dependency["id"] for dependency in pattern["dependencies"]])
        self.assertEqual(pattern["governance"]["stewardship_role"], "maintenance_steward")

    def test_commons_stewardship_protocol_pattern_is_valid(self) -> None:
        pattern = load_data(ROOT / "patterns" / "commons_stewardship_protocol.yaml")
        report = validate_data(pattern, "commons_stewardship_protocol")

        self.assertTrue(report.ok, [issue.message for issue in report.issues])
        self.assertIn("commons", pattern["mdl_categories"])
        self.assertIn("legal_governance_review", [dependency["id"] for dependency in pattern["dependencies"]])
        self.assertIn("conflict_safeguarding_review", [dependency["id"] for dependency in pattern["dependencies"]])

    def test_life_burden_ledger_pattern_is_valid(self) -> None:
        pattern = load_data(ROOT / "patterns" / "life_burden_ledger.yaml")
        report = validate_data(pattern, "life_burden_ledger")

        self.assertTrue(report.ok, [issue.message for issue in report.issues])
        self.assertIn("rest", pattern["mdl_categories"])
        self.assertIn("resident_time_use_baseline", [dependency["id"] for dependency in pattern["dependencies"]])
        self.assertEqual(pattern["governance"]["stewardship_role"], "labor_time_steward")

    def test_anti_speculative_civic_floor_pattern_is_valid(self) -> None:
        pattern = load_data(ROOT / "patterns" / "anti_speculative_civic_floor.yaml")
        report = validate_data(pattern, "anti_speculative_civic_floor")

        self.assertTrue(report.ok, [issue.message for issue in report.issues])
        self.assertIn("shelter", pattern["mdl_categories"])
        self.assertIn("land_tenure_legal_review", [dependency["id"] for dependency in pattern["dependencies"]])
        self.assertIn("finance_affordability_review", [dependency["id"] for dependency in pattern["dependencies"]])
        self.assertEqual(pattern["governance"]["stewardship_role"], "finance_steward")

    def test_standardized_low_burden_build_system_pattern_is_valid(self) -> None:
        pattern = load_data(ROOT / "patterns" / "standardized_low_burden_build_system.yaml")
        report = validate_data(pattern, "standardized_low_burden_build_system")

        self.assertTrue(report.ok, [issue.message for issue in report.issues])
        self.assertIn("shelter", pattern["mdl_categories"])
        self.assertIn("structural_engineering_review", [dependency["id"] for dependency in pattern["dependencies"]])
        self.assertIn("fabrication_vendor_review", [dependency["id"] for dependency in pattern["dependencies"]])
        self.assertEqual(pattern["governance"]["stewardship_role"], "materials_steward")

    def test_pedestrian_first_access_commons_pattern_is_valid(self) -> None:
        pattern = load_data(ROOT / "patterns" / "pedestrian_first_access_commons.yaml")
        report = validate_data(pattern, "pedestrian_first_access_commons")

        self.assertTrue(report.ok, [issue.message for issue in report.issues])
        self.assertIn("health", pattern["mdl_categories"])
        self.assertIn("accessibility_mobility_review", [dependency["id"] for dependency in pattern["dependencies"]])
        self.assertIn("emergency_access_fire_review", [dependency["id"] for dependency in pattern["dependencies"]])
        self.assertEqual(pattern["governance"]["stewardship_role"], "mobility_steward")

    def test_civic_skill_lattice_pattern_is_valid(self) -> None:
        pattern = load_data(ROOT / "patterns" / "civic_skill_lattice.yaml")
        report = validate_data(pattern, "civic_skill_lattice")

        self.assertTrue(report.ok, [issue.message for issue in report.issues])
        self.assertIn("contribution", pattern["mdl_categories"])
        self.assertIn("safety_training_review", [dependency["id"] for dependency in pattern["dependencies"]])
        self.assertIn("credential_boundary_review", [dependency["id"] for dependency in pattern["dependencies"]])
        self.assertEqual(pattern["governance"]["stewardship_role"], "learning_steward")

    def test_belonging_without_coercion_commons_pattern_is_valid(self) -> None:
        pattern = load_data(ROOT / "patterns" / "belonging_without_coercion_commons.yaml")
        report = validate_data(pattern, "belonging_without_coercion_commons")

        self.assertTrue(report.ok, [issue.message for issue in report.issues])
        self.assertIn("privacy", pattern["mdl_categories"])
        self.assertIn("social_privacy_review", [dependency["id"] for dependency in pattern["dependencies"]])
        self.assertIn("cultural_pluralism_review", [dependency["id"] for dependency in pattern["dependencies"]])
        self.assertEqual(pattern["governance"]["stewardship_role"], "commons_host")

    def test_graceful_degradation_engine_pattern_is_valid(self) -> None:
        pattern = load_data(ROOT / "patterns" / "graceful_degradation_engine.yaml")
        report = validate_data(pattern, "graceful_degradation_engine")

        self.assertTrue(report.ok, [issue.message for issue in report.issues])
        self.assertIn("energy", pattern["mdl_categories"])
        self.assertIn("emergency_management_review", [dependency["id"] for dependency in pattern["dependencies"]])
        self.assertIn("high_need_resident_resilience_review", [dependency["id"] for dependency in pattern["dependencies"]])
        self.assertEqual(pattern["governance"]["stewardship_role"], "resilience_steward")

    def test_seed_seasonal_profile_is_valid(self) -> None:
        profile = load_data(ROOT / "seasonal_profiles" / "humid_temperate_provisional.yaml")
        report = validate_data(profile, "humid_temperate_provisional")
        self.assertTrue(report.ok, [issue.message for issue in report.issues])

    def test_seed_household_profile_is_valid(self) -> None:
        profile = load_data(ROOT / "household_profiles" / "micro_commons_households_v0.yaml")
        report = validate_data(profile, "micro_commons_households_v0")
        self.assertTrue(report.ok, [issue.message for issue in report.issues])

    def test_seed_spatial_profile_is_valid(self) -> None:
        profile = load_data(ROOT / "spatial_profiles" / "micro_commons_spatial_v0.yaml")
        report = validate_data(profile, "micro_commons_spatial_v0")
        self.assertTrue(report.ok, [issue.message for issue in report.issues])

    def test_missing_lifecycle_fails(self) -> None:
        pattern = load_data(ROOT / "patterns" / "starter_dwelling.yaml")
        broken = copy.deepcopy(pattern)
        broken.pop("lifecycle")
        report = validate_data(broken, "broken")
        self.assertFalse(report.ok)
        self.assertTrue(any("lifecycle" in issue.message or "lifecycle" in issue.path for issue in report.issues))

    def test_missing_governance_field_fails_for_commons_pattern(self) -> None:
        pattern = load_data(ROOT / "patterns" / "well_house.yaml")
        broken = copy.deepcopy(pattern)
        broken["governance"]["backup_role"] = ""
        report = validate_data(broken, "broken")
        self.assertFalse(report.ok)
        self.assertTrue(any("backup_role" in issue.message or "backup_role" in issue.path for issue in report.issues))

    def test_broken_pattern_dependency_fails_library_validation(self) -> None:
        pattern = load_data(ROOT / "patterns" / "starter_dwelling.yaml")
        broken = copy.deepcopy(pattern)
        broken["dependencies"][0]["id"] = "missing_sanitation_stack"
        issues = validate_pattern_library([broken])
        self.assertTrue(any("unknown pattern dependency" in issue.message for issue in issues))


if __name__ == "__main__":
    unittest.main()
