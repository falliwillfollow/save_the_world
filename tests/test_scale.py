from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from ciac.cli import main
from ciac.compiler import load_patterns
from ciac.io import load_data
from ciac.scale import generate_tradeoff_scale_report
from ciac.validation import validate_data


ROOT = Path(__file__).resolve().parents[1]
GENERATED = ROOT / "examples" / "generated"


class TradeoffScaleTests(unittest.TestCase):
    def setUp(self) -> None:
        self.plan = load_data(GENERATED / "micro_commons_plan.json")
        self.matrix = load_data(GENERATED / "micro_commons_candidate_matrix.json")
        self.patterns = load_patterns(ROOT / "patterns")
        self.scale_profile = load_data(ROOT / "scale_profiles" / "micro_commons_scale_targets_v0.yaml")

    def test_scale_profile_validates(self) -> None:
        self.assertTrue(validate_data(self.scale_profile, "scale-profile").ok)

    def test_tradeoff_scale_report_explains_candidates_and_targets(self) -> None:
        report = generate_tradeoff_scale_report(self.plan, self.matrix, self.patterns, self.scale_profile)

        self.assertEqual(report["kind"], "TradeoffScaleReport")
        self.assertEqual(report["status"], "ready_with_warnings")
        self.assertEqual([target["households"] for target in report["scale_targets"]], [5, 10, 25, 50])
        self.assertTrue(report["objective_leaders"])
        self.assertEqual(report["metric_updates"]["faithful_pattern_optimization_engine"], "80%")
        self.assertTrue(validate_data(report, "tradeoff-scale").ok)

    def test_tradeoff_scale_report_scales_shared_capacity(self) -> None:
        report = generate_tradeoff_scale_report(self.plan, self.matrix, self.patterns, self.scale_profile)
        current = next(candidate for candidate in report["candidate_scale_results"] if candidate["candidate"] == "current_plan")
        water_capacity = next(item for item in current["scale_parameters"] if item["parameter_id"] == "potable_capacity")

        self.assertEqual(water_capacity["values"][0]["scaled_value"], 60000)
        self.assertEqual(water_capacity["values"][-1]["scaled_value"], 600000)

    def test_cli_tradeoff_scale_writes_report(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "tradeoff_scale.json"
            code = main(
                [
                    "tradeoff-scale",
                    str(GENERATED / "micro_commons_plan.json"),
                    str(GENERATED / "micro_commons_candidate_matrix.json"),
                    str(ROOT / "patterns"),
                    str(ROOT / "scale_profiles" / "micro_commons_scale_targets_v0.yaml"),
                    "--output",
                    str(output),
                ]
            )

            self.assertEqual(code, 0)
            report = load_data(output)
            self.assertEqual(report["kind"], "TradeoffScaleReport")


if __name__ == "__main__":
    unittest.main()
