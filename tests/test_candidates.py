from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from ciac.candidates import generate_candidate_matrix
from ciac.compiler import load_patterns
from ciac.io import load_data
from ciac.validation import validate_data
from ciac.cli import main


ROOT = Path(__file__).resolve().parents[1]
GENERATED = ROOT / "examples" / "generated"


class CandidateMatrixTests(unittest.TestCase):
    def setUp(self) -> None:
        self.plan = load_data(GENERATED / "micro_commons_plan.json")
        self.patterns = load_patterns(ROOT / "patterns")
        self.profile = load_data(ROOT / "optimization_profiles" / "minimum_dignity_v0.yaml")
        self.review_status = load_data(GENERATED / "micro_commons_review_status.json")
        self.scenarios = [
            load_data(ROOT / "scenarios" / "water_contamination_response_v2.yaml"),
            load_data(ROOT / "scenarios" / "crop_failure.yaml"),
            load_data(ROOT / "scenarios" / "energy_outage_reserve_v2.yaml"),
        ]

    def test_candidate_matrix_generates_three_viable_configurations(self) -> None:
        report = generate_candidate_matrix(self.plan, self.patterns, self.profile, self.scenarios, self.review_status, baseline_days=30)

        self.assertEqual(report["kind"], "CandidatePlanMatrixReport")
        self.assertEqual(report["status"], "ready_with_warnings")
        self.assertEqual(report["candidate_count"], 3)
        self.assertEqual(report["viable_candidate_count"], 3)
        self.assertEqual(report["metric_updates"]["faithful_pattern_optimization_engine"], "65%")
        self.assertTrue(validate_data(report, "candidate-matrix").ok)

    def test_candidate_matrix_rejects_unmet_survival_demand(self) -> None:
        plan = dict(self.plan)
        plan["simulation_inputs"] = dict(self.plan["simulation_inputs"])
        plan["simulation_inputs"]["storage_by_pattern"] = {
            key: [dict(item) for item in value]
            for key, value in self.plan["simulation_inputs"]["storage_by_pattern"].items()
        }
        plan["simulation_inputs"]["storage_by_pattern"]["emergency_water_reserve"][0]["capacity"] = 1
        plan["simulation_inputs"]["storage_by_pattern"]["emergency_water_reserve"][0]["initial"] = 1
        plan["simulation_inputs"]["storage_by_pattern"]["emergency_water_reserve"][0]["max_release_per_day"] = 1

        report = generate_candidate_matrix(plan, self.patterns, self.profile, self.scenarios[:1], self.review_status, baseline_days=30)

        self.assertEqual(report["status"], "not_ready")
        self.assertLess(report["viable_candidate_count"], 3)

    def test_cli_candidate_matrix_writes_report(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "candidate_matrix.json"
            code = main(
                [
                    "candidate-matrix",
                    str(GENERATED / "micro_commons_plan.json"),
                    str(ROOT / "patterns"),
                    str(ROOT / "optimization_profiles" / "minimum_dignity_v0.yaml"),
                    "--scenario",
                    str(ROOT / "scenarios" / "water_contamination_response_v2.yaml"),
                    "--scenario",
                    str(ROOT / "scenarios" / "crop_failure.yaml"),
                    "--scenario",
                    str(ROOT / "scenarios" / "energy_outage_reserve_v2.yaml"),
                    "--review-status",
                    str(GENERATED / "micro_commons_review_status.json"),
                    "--days",
                    "30",
                    "--output",
                    str(output),
                ]
            )

            self.assertEqual(code, 0)
            report = load_data(output)
            self.assertEqual(report["kind"], "CandidatePlanMatrixReport")


if __name__ == "__main__":
    unittest.main()
