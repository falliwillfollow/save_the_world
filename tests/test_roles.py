from __future__ import annotations

import copy
import unittest
from pathlib import Path

from ciac.compiler import compile_plan, load_patterns
from ciac.io import load_data
from ciac.roles import evaluate_roles
from ciac.validation import validate_data


ROOT = Path(__file__).resolve().parents[1]


class RoleTests(unittest.TestCase):
    def setUp(self) -> None:
        patterns = load_patterns(ROOT / "patterns")
        site = load_data(ROOT / "examples" / "site_profiles" / "micro_commons_5_households.yaml")
        self.plan = compile_plan(site, patterns)
        self.role_plan = load_data(ROOT / "role_plans" / "micro_commons_basic.yaml")

    def test_basic_role_plan_validates_and_fails_energy_backup(self) -> None:
        report = evaluate_roles(self.plan, self.role_plan)
        self.assertEqual(report["kind"], "RoleReport")
        self.assertEqual(report["status"], "fail")
        self.assertTrue(validate_data(report, "roles").ok)
        self.assertIn("energy_steward", report["single_point_of_failure_roles"])
        self.assertIn("energy_steward", report["backup_coverage"]["roles_missing_backup"])

    def test_training_second_energy_steward_improves_backup(self) -> None:
        role_plan = copy.deepcopy(self.role_plan)
        role_plan["participants"][0]["skills"].extend(["energy_ops", "electrical_awareness"])
        role_plan["participants"][0]["eligible_roles"].append("energy_steward")
        report = evaluate_roles(self.plan, role_plan)
        self.assertNotIn("energy_steward", report["backup_coverage"]["roles_missing_backup"])

    def test_unfilled_role_is_reported(self) -> None:
        role_plan = copy.deepcopy(self.role_plan)
        for participant in role_plan["participants"]:
            participant["eligible_roles"] = [role for role in participant["eligible_roles"] if role != "water_steward"]
        report = evaluate_roles(self.plan, role_plan)
        self.assertIn("water_steward", report["unfilled_roles"])
        self.assertEqual(report["status"], "fail")

    def test_overloaded_resident_is_reported(self) -> None:
        role_plan = copy.deepcopy(self.role_plan)
        for participant in role_plan["participants"]:
            participant["availability_hours_per_week"] = 0.1
        report = evaluate_roles(self.plan, role_plan)
        self.assertTrue(report["overloaded_residents"])

    def test_role_output_shape_is_stable_for_downstream_consumers(self) -> None:
        report = evaluate_roles(self.plan, self.role_plan)
        self.assertEqual(
            list(report.keys()),
            [
                "kind",
                "id",
                "compiled_plan",
                "role_plan",
                "generated_by",
                "weeks",
                "provisional",
                "status",
                "assigned_role_schedule",
                "unfilled_roles",
                "overloaded_residents",
                "single_point_of_failure_roles",
                "backup_coverage",
                "care_work_accounting",
                "fairness",
                "burnout_warnings",
                "redesign_recommendations",
                "unknowns",
            ],
        )


if __name__ == "__main__":
    unittest.main()

