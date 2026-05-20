from __future__ import annotations

import copy
import unittest
from pathlib import Path

from ciac.compiler import compile_plan, load_patterns
from ciac.io import load_data
from ciac.validation import validate_data
from ciac.water import evaluate_water


ROOT = Path(__file__).resolve().parents[1]


class WaterTests(unittest.TestCase):
    def setUp(self) -> None:
        patterns = load_patterns(ROOT / "patterns")
        site = load_data(ROOT / "examples" / "site_profiles" / "micro_commons_5_households.yaml")
        self.plan = compile_plan(site, patterns)
        self.water_plan = load_data(ROOT / "water_plans" / "micro_commons_basic.yaml")

    def test_basic_water_plan_validates_and_fails_drought(self) -> None:
        report = evaluate_water(self.plan, self.water_plan)
        self.assertEqual(report["kind"], "WaterReport")
        self.assertEqual(report["status"], "fail")
        self.assertTrue(validate_data(report, "water").ok)
        self.assertEqual(report["normal_balance"]["status"], "pass")
        self.assertEqual(report["drought_balance"]["status"], "fail")
        self.assertIn("drought water balance is insufficient", report["bottlenecks"])

    def test_more_storage_improves_contamination_fallback_window(self) -> None:
        water_plan = copy.deepcopy(self.water_plan)
        water_plan["storage"]["potable_liters"] = 12000
        report = evaluate_water(self.plan, water_plan)
        self.assertGreaterEqual(report["contamination_response"]["potable_storage_fallback_days"], 7)

    def test_missing_rainwater_pattern_warns(self) -> None:
        plan = copy.deepcopy(self.plan)
        plan["selected_patterns"] = [pattern for pattern in plan["selected_patterns"] if pattern != "rainwater_capture"]
        report = evaluate_water(plan, self.water_plan)
        self.assertIn(
            "Compiled plan does not include rainwater_capture; backup water assumptions may be unsupported.",
            report["water_safety_warnings"],
        )

    def test_unverified_testing_warns(self) -> None:
        water_plan = copy.deepcopy(self.water_plan)
        water_plan["testing"]["requires_lab_confirmation"] = False
        report = evaluate_water(self.plan, water_plan)
        self.assertEqual(report["testing"]["status"], "warn")
        self.assertTrue(any("testing" in item.lower() for item in report["bottlenecks"]))

    def test_water_output_shape_is_stable_for_downstream_consumers(self) -> None:
        report = evaluate_water(self.plan, self.water_plan)
        self.assertEqual(
            list(report.keys()),
            [
                "kind",
                "id",
                "compiled_plan",
                "water_plan",
                "generated_by",
                "days",
                "population",
                "provisional",
                "status",
                "storage",
                "normal_balance",
                "drought_balance",
                "contamination_response",
                "testing",
                "demand_reduction_needed",
                "water_safety_warnings",
                "redesign_recommendations",
                "bottlenecks",
                "unknowns",
            ],
        )


if __name__ == "__main__":
    unittest.main()

