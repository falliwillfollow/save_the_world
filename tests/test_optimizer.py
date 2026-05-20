from __future__ import annotations

import copy
import tempfile
import unittest
from pathlib import Path

from ciac.cli import main
from ciac.io import load_data
from ciac.optimizer import optimize_candidates
from ciac.validation import validate_data


ROOT = Path(__file__).resolve().parents[1]
GENERATED = ROOT / "examples" / "generated"


class OptimizerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.matrix = load_data(GENERATED / "micro_commons_candidate_matrix.json")
        self.profile = load_data(ROOT / "optimization_profiles" / "minimum_dignity_v0.yaml")
        self.tradeoff_scale = load_data(GENERATED / "micro_commons_tradeoff_scale.json")

    def test_optimizer_selects_ranked_candidate_and_validates(self) -> None:
        report = optimize_candidates(self.matrix, self.profile, self.tradeoff_scale)

        self.assertEqual(report["kind"], "OptimizerReport")
        self.assertEqual(report["status"], "ready_with_warnings")
        self.assertEqual(report["selected_candidate"], "current_plan")
        self.assertEqual(report["rankings"][0]["candidate"], "current_plan")
        self.assertEqual(report["metric_updates"]["faithful_pattern_optimization_engine"], "90%")
        self.assertTrue(validate_data(report, "optimizer-report").ok)

    def test_optimizer_sensitivity_shows_objective_weight_flip(self) -> None:
        report = optimize_candidates(self.matrix, self.profile, self.tradeoff_scale)
        checks = {check["objective"]: check for check in report["sensitivity_checks"]}

        self.assertEqual(checks["maximize_resilience"]["leader"], "high_resilience_reserve")
        self.assertFalse(checks["maximize_resilience"]["selection_stable"])
        self.assertEqual(checks["reduce_cost"]["leader"], "current_plan")
        self.assertTrue(checks["reduce_cost"]["selection_stable"])

    def test_optimizer_reports_specific_constraint_explanations(self) -> None:
        report = optimize_candidates(self.matrix, self.profile, self.tradeoff_scale)

        self.assertTrue(report["constraint_explanations"])
        constraints = {item["constraint"] for item in report["constraint_explanations"]}
        self.assertIn("minimum_repeatable_patterns", constraints)
        self.assertTrue(all("remediation" in item for item in report["constraint_explanations"]))

    def test_optimizer_refuses_all_rejected_candidates(self) -> None:
        matrix = copy.deepcopy(self.matrix)
        for candidate in matrix["candidates"]:
            candidate["status"] = "rejected"
            candidate["hard_constraint_failures"] = 1
            candidate["constraint_results"][0]["status"] = "fail"

        report = optimize_candidates(matrix, self.profile, self.tradeoff_scale)

        self.assertEqual(report["status"], "not_ready")
        self.assertEqual(report["selected_candidate"], "")
        self.assertTrue(any(item["severity"] == "hard" for item in report["constraint_explanations"]))

    def test_cli_optimizer_writes_report(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "optimizer.json"
            code = main(
                [
                    "optimize",
                    str(GENERATED / "micro_commons_candidate_matrix.json"),
                    str(ROOT / "optimization_profiles" / "minimum_dignity_v0.yaml"),
                    "--tradeoff-scale",
                    str(GENERATED / "micro_commons_tradeoff_scale.json"),
                    "--output",
                    str(output),
                ]
            )

            self.assertEqual(code, 0)
            report = load_data(output)
            self.assertEqual(report["kind"], "OptimizerReport")


if __name__ == "__main__":
    unittest.main()
