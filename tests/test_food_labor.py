import tempfile
import unittest
from pathlib import Path

from ciac.cli import main
from ciac.compiler import load_patterns
from ciac.food_labor import generate_food_labor_report
from ciac.io import load_data
from ciac.validation import validate_data


ROOT = Path(__file__).resolve().parents[1]


class FoodLaborReportTests(unittest.TestCase):
    def setUp(self) -> None:
        self.registry = load_data(ROOT / "module_registries" / "micro_commons_default_v0.yaml")
        self.patterns = load_patterns(ROOT / "patterns")

    def test_hybrid_food_commons_declares_category_labor_model(self) -> None:
        pattern = self.patterns["hybrid_food_commons"]
        report = validate_data(pattern, "hybrid-food-commons")

        self.assertTrue(report.ok, [issue.message for issue in report.issues])
        self.assertEqual(pattern["labor_model"]["target_population"], 80)
        category_hours = sum(category["hours_per_week"] for category in pattern["labor_model"]["categories"])
        self.assertEqual(category_hours, pattern["metrics"]["recurring_labor_hours_per_week"])
        self.assertIn("replicate food commons nodes", pattern["labor_model"]["replication"]["above_max_strategy"])

    def test_food_labor_report_flags_total_labor_but_accepts_replicated_scale(self) -> None:
        report = generate_food_labor_report(self.registry, self.patterns, extra_people=[756])

        self.assertEqual(report["kind"], "FoodLaborReport")
        self.assertEqual(report["status"], "warn")
        self.assertEqual(report["primary_pattern"], "hybrid_food_commons")
        self.assertIn("protein_commons_supplement", report["modeled_patterns"])
        self.assertIn("seasonal_food_smoothing_commons", report["modeled_patterns"])
        self.assertEqual(report["summary"]["base_hours_per_week"], 97.5)
        self.assertLessEqual(report["summary"]["hours_per_resident_per_week"], 1.5)
        self.assertTrue(any(hotspot["kind"] == "total_food_labor_surface" for hotspot in report["hotspots"]))
        scale = {row["target_population"]: row for row in report["scaling_results"]}
        self.assertEqual(scale[1500]["nodes"], 19)
        self.assertEqual(scale[756]["nodes"], 10)
        self.assertLessEqual(scale[1500]["hours_per_resident_per_week"], 1.5)
        self.assertLessEqual(scale[756]["max_category_hours_per_node"], 20)
        self.assertEqual(scale[12]["status"], "warn")
        self.assertTrue(validate_data(report, "food-labor").ok)

    def test_cli_food_labor_writes_report(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "food_labor.json"
            code = main(
                [
                    "food-labor",
                    str(ROOT / "module_registries" / "micro_commons_default_v0.yaml"),
                    str(ROOT / "patterns"),
                    "--people",
                    "756",
                    "--output",
                    str(output),
                ]
            )

            self.assertEqual(code, 0)
            report = load_data(output)
            self.assertEqual(report["kind"], "FoodLaborReport")
            self.assertEqual(report["slot"], "food_production")
            self.assertIn(756, {row["target_population"] for row in report["scaling_results"]})


if __name__ == "__main__":
    unittest.main()
