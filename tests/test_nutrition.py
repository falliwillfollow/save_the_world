from __future__ import annotations

import copy
import unittest
from pathlib import Path

from ciac.compiler import compile_plan, load_patterns
from ciac.io import load_data
from ciac.nutrition import evaluate_nutrition
from ciac.validation import validate_data


ROOT = Path(__file__).resolve().parents[1]


class NutritionTests(unittest.TestCase):
    def setUp(self) -> None:
        patterns = load_patterns(ROOT / "patterns")
        site = load_data(ROOT / "examples" / "site_profiles" / "micro_commons_5_households.yaml")
        self.plan = compile_plan(site, patterns)
        self.food_plan = load_data(ROOT / "food_plans" / "micro_commons_basic.yaml")

    def test_basic_food_plan_validates_and_warns(self) -> None:
        report = evaluate_nutrition(self.plan, self.food_plan)
        self.assertEqual(report["kind"], "NutritionReport")
        self.assertEqual(report["status"], "warn")
        self.assertTrue(validate_data(report, "nutrition").ok)
        self.assertGreaterEqual(
            report["nutrition"]["calories_per_person_per_day"],
            self.food_plan["targets"]["calories_per_person_per_day"],
        )

    def test_calorie_shortage_fails(self) -> None:
        food_plan = copy.deepcopy(self.food_plan)
        for food in food_plan["foods"]:
            food["calories_per_day"] = 100
        report = evaluate_nutrition(self.plan, food_plan)
        self.assertEqual(report["status"], "fail")
        self.assertIn("daily calories are below target", report["bottlenecks"])
        self.assertTrue(any(event["event"] == "calorie_shortage" for event in report["shortage_timeline"]))

    def test_storage_shortfall_warns_with_procurement_need(self) -> None:
        food_plan = copy.deepcopy(self.food_plan)
        food_plan["targets"]["storage_days_target"] = 120
        report = evaluate_nutrition(self.plan, food_plan)
        self.assertIn("stored calorie buffer is below target", report["bottlenecks"])
        self.assertTrue(any("stored staples" in need for need in report["fallback_procurement_needs"]))

    def test_missing_greenhouse_warns_about_local_fresh_food(self) -> None:
        plan = copy.deepcopy(self.plan)
        plan["selected_patterns"] = [pattern for pattern in plan["selected_patterns"] if pattern != "greenhouse"]
        report = evaluate_nutrition(plan, self.food_plan)
        self.assertIn(
            "Compiled plan does not include greenhouse; local fresh-food assumptions may be unsupported.",
            report["dietary_risk_warnings"],
        )

    def test_nutrition_output_shape_is_stable_for_downstream_consumers(self) -> None:
        report = evaluate_nutrition(self.plan, self.food_plan)
        self.assertEqual(
            list(report.keys()),
            [
                "kind",
                "id",
                "compiled_plan",
                "food_plan",
                "generated_by",
                "days",
                "population",
                "provisional",
                "status",
                "nutrition",
                "local_food",
                "storage",
                "shortage_timeline",
                "fallback_procurement_needs",
                "dietary_risk_warnings",
                "bottlenecks",
                "unknowns",
            ],
        )


if __name__ == "__main__":
    unittest.main()

