from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from ciac.cli import main
from ciac.compiler import compile_plan, load_patterns
from ciac.io import load_data
from ciac.matrix_redesign import generate_matrix_redesign
from ciac.validation import validate_data


ROOT = Path(__file__).resolve().parents[1]


class MatrixRedesignTests(unittest.TestCase):
    def setUp(self) -> None:
        patterns = load_patterns(ROOT / "patterns")
        site = load_data(ROOT / "examples" / "site_profiles" / "micro_commons_5_households.yaml")
        self.plan = compile_plan(site, patterns)
        self.matrix = load_data(ROOT / "examples" / "generated" / "micro_commons_replay_matrix.json")

    def test_matrix_redesign_validates(self) -> None:
        report = generate_matrix_redesign(self.plan, self.matrix)

        self.assertEqual(report["kind"], "MatrixRedesignReport")
        self.assertEqual(report["status"], "ready_for_iteration")
        self.assertTrue(validate_data(report, "matrix-redesign").ok)

    def test_matrix_redesign_prioritizes_current_top_stressor(self) -> None:
        report = generate_matrix_redesign(self.plan, self.matrix)

        self.assertEqual(report["priority_order"][0], "food_model_closure_and_recovery_clock")
        self.assertNotIn("water_response_buffer_and_isolation_floor", report["priority_order"])
        self.assertNotIn("scenario_labor_surge_buffer", report["priority_order"])
        first = report["redesign_candidates"][0]
        self.assertIn("crop_failure", first["target_scenarios"])
        self.assertTrue(first["minimum_viable_change"])

    def test_matrix_redesign_includes_energy_and_review_candidates(self) -> None:
        report = generate_matrix_redesign(self.plan, self.matrix)
        candidate_ids = set(report["priority_order"])

        self.assertIn("energy_outage_short_window_load_shed", candidate_ids)
        self.assertIn("review_evidence_minimum_register", candidate_ids)

    def test_cli_redesign_matrix_writes_report(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "matrix_redesign.json"
            code = main(
                [
                    "redesign-matrix",
                    str(ROOT / "examples" / "generated" / "micro_commons_plan.json"),
                    str(ROOT / "examples" / "generated" / "micro_commons_replay_matrix.json"),
                    "--output",
                    str(output),
                ]
            )

            self.assertEqual(code, 0)
            report = load_data(output)
            self.assertEqual(report["kind"], "MatrixRedesignReport")

    def test_matrix_redesign_shape_is_stable(self) -> None:
        report = generate_matrix_redesign(self.plan, self.matrix)

        self.assertEqual(
            list(report.keys()),
            [
                "kind",
                "id",
                "compiled_plan",
                "replay_matrix",
                "generated_by",
                "provisional",
                "status",
                "top_stressor",
                "redesign_candidates",
                "priority_order",
                "next_actions",
                "unknowns",
            ],
        )


if __name__ == "__main__":
    unittest.main()
