import unittest
from pathlib import Path

from ciac.food_autonomy import generate_food_autonomy_report
from ciac.io import load_data
from ciac.validation import validate_data


ROOT = Path(__file__).resolve().parents[1]
GENERATED = ROOT / "examples" / "generated"


class FoodAutonomyTests(unittest.TestCase):
    def setUp(self) -> None:
        self.cycle = load_data(GENERATED / "micro_commons_cycle_iteration.json")
        self.scenarios = [
            load_data(ROOT / "scenarios" / "water_contamination_response_v2.yaml"),
            load_data(ROOT / "scenarios" / "crop_failure.yaml"),
            load_data(ROOT / "scenarios" / "energy_outage_reserve_v2.yaml"),
        ]

    def test_food_autonomy_report_tracks_drawdown_smoothing_and_risk_coverage(self) -> None:
        report = generate_food_autonomy_report(self.cycle, self.scenarios)

        self.assertEqual(report["kind"], "FoodAutonomyReport")
        self.assertEqual(report["population"], self.cycle["viewer_population_context"]["population"])
        self.assertEqual(report["status"], "warn")
        self.assertGreater(report["food_autonomy"]["reserve_release_ratio"], 0.1)
        hotspots = {(hotspot["kind"], hotspot["severity"], hotspot["subject"]) for hotspot in report["hotspots"]}
        self.assertIn(("food_procurement_dependency", "warn", "food_servings"), hotspots)
        self.assertIn(("multi_season_deficit", "warn", "food_servings"), hotspots)
        self.assertTrue(report["seasonal_smoothing"]["resources"])
        self.assertIn("battery_fire_or_fault", report["risk_scenario_coverage"]["uncovered_risk_modes"])
        self.assertTrue(validate_data(report, "food-autonomy").ok)


if __name__ == "__main__":
    unittest.main()
