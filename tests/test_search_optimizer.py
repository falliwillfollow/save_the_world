from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from ciac.cli import main
from ciac.compiler import load_patterns
from ciac.io import load_data
from ciac.search_optimizer import optimize_search
from ciac.validation import validate_data


ROOT = Path(__file__).resolve().parents[1]
GENERATED = ROOT / "examples" / "generated"


class SearchOptimizerTests(unittest.TestCase):
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

    def test_search_optimizer_generates_family_level_candidate_space(self) -> None:
        report = optimize_search(self.plan, self.patterns, self.profile, self.scenarios, self.review_status, baseline_days=30)

        self.assertEqual(report["kind"], "SearchOptimizerReport")
        self.assertEqual(report["status"], "ready_with_warnings")
        self.assertEqual(report["search_space"]["family_count"], 3)
        self.assertEqual(report["candidate_count"], 64)
        self.assertGreater(report["viable_candidate_count"], 3)
        self.assertTrue(report["selected_candidate"])
        self.assertTrue(validate_data(report, "search-optimizer").ok)

    def test_search_optimizer_reports_binding_constraints_and_locked_assumptions(self) -> None:
        report = optimize_search(self.plan, self.patterns, self.profile, self.scenarios, self.review_status, baseline_days=30)

        constraints = {constraint["constraint"]: constraint for constraint in report["binding_constraints"]}
        self.assertIn("no_unmet_survival_demand", constraints)
        self.assertIn("minimum_repeatable_patterns", constraints)
        self.assertGreaterEqual(len(report["locked_assumptions"]), 3)
        self.assertEqual(report["metric_updates"]["faithful_pattern_optimization_engine"], "98%")

    def test_search_optimizer_top_candidate_has_parameter_deltas(self) -> None:
        report = optimize_search(self.plan, self.patterns, self.profile, self.scenarios, self.review_status, baseline_days=30)
        selected = report["top_candidates"][0]

        self.assertEqual(selected["id"], report["selected_candidate"])
        self.assertIn("family_levels", selected)
        self.assertTrue(selected["parameter_deltas"])
        self.assertTrue(any(delta["delta"] != 0 for delta in selected["parameter_deltas"]))

    def test_cli_optimize_search_writes_report(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "search_optimizer.json"
            code = main(
                [
                    "optimize-search",
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
            self.assertEqual(report["kind"], "SearchOptimizerReport")


if __name__ == "__main__":
    unittest.main()
