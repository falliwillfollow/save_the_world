from __future__ import annotations

import copy
import tempfile
import unittest
from pathlib import Path

from ciac.cli import main
from ciac.io import load_data
from ciac.validation import validate_data
from ciac.weight_governance import evaluate_weight_governance


ROOT = Path(__file__).resolve().parents[1]
GENERATED = ROOT / "examples" / "generated"


class WeightGovernanceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.optimization_profile = load_data(ROOT / "optimization_profiles" / "minimum_dignity_v0.yaml")
        self.calibration_report = load_data(GENERATED / "micro_commons_objective_calibration.json")
        self.governance_profile = load_data(ROOT / "governance_profiles" / "minimum_dignity_weights_draft_v0.yaml")

    def test_weight_governance_profile_validates(self) -> None:
        self.assertTrue(validate_data(self.governance_profile, "weight-governance-profile").ok)

    def test_draft_weights_block_promotion_but_complete_engine_contract(self) -> None:
        report = evaluate_weight_governance(self.optimization_profile, self.calibration_report, self.governance_profile)

        self.assertEqual(report["kind"], "WeightGovernanceReport")
        self.assertEqual(report["status"], "not_ratified")
        self.assertFalse(report["promotion_allowed"])
        self.assertEqual(report["metric_updates"]["faithful_pattern_optimization_engine"], "100%")
        self.assertTrue(all(check["matches_profile"] for check in report["weight_checks"]))
        self.assertTrue(validate_data(report, "weight-governance-report").ok)

    def test_ratified_weights_can_promote_only_with_calibrated_objectives(self) -> None:
        profile = copy.deepcopy(self.governance_profile)
        profile["authority"]["resident_consent_status"] = "ratified"
        profile["authority"]["professional_review_status"] = "accepted"
        for weight in profile["objective_weights"]:
            weight["status"] = "ratified"
        calibration = copy.deepcopy(self.calibration_report)
        calibration["status"] = "calibrated"

        report = evaluate_weight_governance(self.optimization_profile, calibration, profile)

        self.assertEqual(report["status"], "ratified")
        self.assertTrue(report["promotion_allowed"])

    def test_cli_weight_governance_writes_report_and_blocks_draft(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "weight_governance.json"
            code = main(
                [
                    "weight-governance",
                    str(ROOT / "optimization_profiles" / "minimum_dignity_v0.yaml"),
                    str(GENERATED / "micro_commons_objective_calibration.json"),
                    str(ROOT / "governance_profiles" / "minimum_dignity_weights_draft_v0.yaml"),
                    "--output",
                    str(output),
                ]
            )

            self.assertEqual(code, 1)
            report = load_data(output)
            self.assertEqual(report["kind"], "WeightGovernanceReport")
            self.assertEqual(report["status"], "not_ratified")


if __name__ == "__main__":
    unittest.main()
