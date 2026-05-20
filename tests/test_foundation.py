from __future__ import annotations

import tempfile
import unittest
from copy import deepcopy
from pathlib import Path

from ciac.cli import main
from ciac.foundation import evaluate_foundation_gate
from ciac.io import load_data
from ciac.validation import validate_data


ROOT = Path(__file__).resolve().parents[1]
GENERATED = ROOT / "examples" / "generated"


class FoundationGateTests(unittest.TestCase):
    def setUp(self) -> None:
        self.plan = load_data(GENERATED / "micro_commons_plan.json")
        self.baseline = load_data(GENERATED / "micro_commons_simulation.json")
        self.bundle = load_data(GENERATED / "micro_commons_runtime_bundle.json")
        self.matrix = load_data(GENERATED / "micro_commons_replay_matrix.json")
        self.review = load_data(GENERATED / "micro_commons_review_status.json")
        self.comparisons = [
            load_data(GENERATED / "water_contamination_response_v2_replay_comparison.json"),
            load_data(GENERATED / "crop_failure_replay_comparison.json"),
            load_data(GENERATED / "energy_outage_reserve_v2_replay_comparison.json"),
        ]

    def test_foundation_gate_is_ready_with_visible_warnings(self) -> None:
        report = evaluate_foundation_gate(self.plan, self.baseline, self.bundle, self.matrix, self.review, self.comparisons)

        self.assertEqual(report["kind"], "FoundationGateReport")
        self.assertEqual(report["status"], "ready_with_warnings")
        self.assertTrue(report["ready_for_visual_buildout"])
        self.assertTrue(any(check["id"] == "review_blocker_visibility" and check["status"] == "warn" for check in report["checks"]))
        self.assertTrue(validate_data(report, "foundation-gate").ok)

    def test_foundation_gate_fails_when_stress_unmet_demand_remains(self) -> None:
        matrix = deepcopy(self.matrix)
        matrix["status"] = "stress_failed"
        matrix["rankings"][0]["status"] = "stress_failed"
        matrix["rankings"][0]["total_unmet_delta"] = 2

        report = evaluate_foundation_gate(self.plan, self.baseline, self.bundle, matrix, self.review, self.comparisons)

        self.assertEqual(report["status"], "not_ready")
        self.assertFalse(report["ready_for_visual_buildout"])
        self.assertTrue(any(check["id"] == "stress_unmet_survival_demand" and check["status"] == "fail" for check in report["checks"]))

    def test_cli_foundation_gate_writes_report(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "foundation_gate.json"
            code = main(
                [
                    "foundation-gate",
                    str(GENERATED / "micro_commons_plan.json"),
                    str(GENERATED / "micro_commons_simulation.json"),
                    str(GENERATED / "micro_commons_runtime_bundle.json"),
                    str(GENERATED / "micro_commons_replay_matrix.json"),
                    "--review-status",
                    str(GENERATED / "micro_commons_review_status.json"),
                    "--comparison",
                    str(GENERATED / "water_contamination_response_v2_replay_comparison.json"),
                    "--comparison",
                    str(GENERATED / "crop_failure_replay_comparison.json"),
                    "--comparison",
                    str(GENERATED / "energy_outage_reserve_v2_replay_comparison.json"),
                    "--output",
                    str(output),
                ]
            )

            self.assertEqual(code, 0)
            report = load_data(output)
            self.assertEqual(report["kind"], "FoundationGateReport")


if __name__ == "__main__":
    unittest.main()

