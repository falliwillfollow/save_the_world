from __future__ import annotations

import copy
import tempfile
import unittest
from pathlib import Path

from ciac.cli import main
from ciac.io import load_data
from ciac.objective_calibration import evaluate_objective_calibration
from ciac.validation import validate_data


ROOT = Path(__file__).resolve().parents[1]
GENERATED = ROOT / "examples" / "generated"


class ObjectiveCalibrationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.search = load_data(GENERATED / "micro_commons_search_optimizer_report.json")
        self.profile = load_data(ROOT / "calibration_profiles" / "minimum_dignity_objectives_v0.yaml")

    def test_profile_validates(self) -> None:
        self.assertTrue(validate_data(self.profile, "calibration-profile").ok)

    def test_objective_calibration_report_validates(self) -> None:
        report = evaluate_objective_calibration(self.search, self.profile)

        self.assertEqual(report["kind"], "ObjectiveCalibrationReport")
        self.assertEqual(report["status"], "provisional_calibrated")
        self.assertEqual(report["selected_candidate"], self.search["selected_candidate"])
        self.assertEqual(report["missing_metrics"], [])
        self.assertEqual(report["uncalibrated_score_count"], 0)
        self.assertEqual(report["metric_updates"]["faithful_pattern_optimization_engine"], "99%")
        self.assertTrue(validate_data(report, "objective-calibration").ok)

    def test_missing_metric_blocks_calibration(self) -> None:
        profile = copy.deepcopy(self.profile)
        profile["metric_calibrations"] = [
            calibration
            for calibration in profile["metric_calibrations"]
            if calibration["metric"] != "cost"
        ]

        report = evaluate_objective_calibration(self.search, profile)

        self.assertEqual(report["status"], "missing_calibration")
        self.assertIn("cost", report["missing_metrics"])
        self.assertGreater(report["uncalibrated_score_count"], 0)

    def test_cli_objective_calibration_writes_report(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "objective_calibration.json"
            code = main(
                [
                    "objective-calibration",
                    str(GENERATED / "micro_commons_search_optimizer_report.json"),
                    str(ROOT / "calibration_profiles" / "minimum_dignity_objectives_v0.yaml"),
                    "--output",
                    str(output),
                ]
            )

            self.assertEqual(code, 0)
            report = load_data(output)
            self.assertEqual(report["kind"], "ObjectiveCalibrationReport")


if __name__ == "__main__":
    unittest.main()
