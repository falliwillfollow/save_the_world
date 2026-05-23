from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from ciac.cli import main
from ciac.compiler import load_patterns
from ciac.cycle import materialize_search_candidate
from ciac.io import load_data
from ciac.validation import validate_data


ROOT = Path(__file__).resolve().parents[1]
GENERATED = ROOT / "examples" / "generated"


class CycleIterationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.plan = load_data(GENERATED / "micro_commons_plan.json")
        self.search = load_data(GENERATED / "micro_commons_search_optimizer_report.json")
        self.review_status = load_data(GENERATED / "micro_commons_review_status.json")
        self.patterns = load_patterns(ROOT / "patterns")
        self.profile = load_data(ROOT / "optimization_profiles" / "minimum_dignity_v0.yaml")
        self.scenarios = [
            load_data(ROOT / "scenarios" / "water_contamination_response_v2.yaml"),
            load_data(ROOT / "scenarios" / "crop_failure.yaml"),
            load_data(ROOT / "scenarios" / "energy_outage_reserve_v2.yaml"),
        ]

    def test_materializes_selected_search_candidate_into_runtime_bundle(self) -> None:
        report = materialize_search_candidate(
            self.plan,
            self.search,
            review_status=self.review_status,
            scenarios=self.scenarios,
            days=365,
            patterns_by_id=self.patterns,
            optimization_profile=self.profile,
        )

        self.assertEqual(report["kind"], "CycleIterationReport")
        self.assertEqual(report["status"], "materialized")
        self.assertEqual(report["selected_candidate"], self.search["selected_candidate"])
        self.assertEqual(report["authority"]["mode"], "operator_directed")
        self.assertEqual(report["viewer_population_context"]["population"], self.plan["site_summary"]["population_target"])
        self.assertIn(report["operator_acceptance"]["status"], {"improved", "converged"})
        self.assertTrue(report["operator_acceptance"]["simulation_submit_allowed"])
        self.assertTrue(report["authority"]["simulation_submit_allowed"])
        self.assertFalse(report["operator_acceptance"]["objective_regressions"])
        self.assertEqual(len(report["applied_scenarios"]), 3)
        self.assertEqual(report["runtime_bundle"]["kind"], "RuntimeBundle")
        self.assertEqual(report["next_search_optimizer_report"]["kind"], "SearchOptimizerReport")
        self.assertTrue(validate_data(report, "cycle-iteration").ok)

    def test_materialized_plan_applies_candidate_parameter_values(self) -> None:
        report = materialize_search_candidate(self.plan, self.search, review_status=self.review_status, days=30)
        for parameter in selected_candidate(self.search)["parameter_values"]:
            pattern_id = parameter["pattern_id"]
            applied_storage = report["applied_plan"]["simulation_inputs"]["storage_by_pattern"][pattern_id]
            applied_values = [float(value) for storage in applied_storage for value in storage.values() if isinstance(value, (int, float))]
            self.assertIn(float(parameter["value"]), applied_values)
        self.assertNotEqual(report["applied_plan"]["id"], self.plan["id"])
        self.assertEqual(report["artifacts"]["runtime_bundle_id"], report["runtime_bundle"]["id"])

    def test_cli_apply_search_candidate_writes_cycle_report(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "cycle.json"
            code = main(
                [
                    "apply-search-candidate",
                    str(GENERATED / "micro_commons_plan.json"),
                    str(GENERATED / "micro_commons_search_optimizer_report.json"),
                    "--review-status",
                    str(GENERATED / "micro_commons_review_status.json"),
                    "--scenario",
                    str(ROOT / "scenarios" / "water_contamination_response_v2.yaml"),
                    "--pattern-dir",
                    str(ROOT / "patterns"),
                    "--optimization-profile",
                    str(ROOT / "optimization_profiles" / "minimum_dignity_v0.yaml"),
                    "--days",
                    "30",
                    "--output",
                    str(output),
                ]
            )

            self.assertEqual(code, 0)
            report = load_data(output)
            self.assertEqual(report["kind"], "CycleIterationReport")
            self.assertEqual(report["runtime_bundle"]["kind"], "RuntimeBundle")
            self.assertEqual(report["next_search_optimizer_report"]["kind"], "SearchOptimizerReport")
            self.assertIn(report["operator_acceptance"]["status"], {"improved", "regressed", "converged", "blocked"})


if __name__ == "__main__":
    unittest.main()


def selected_candidate(search: dict) -> dict:
    return next(candidate for candidate in search["top_candidates"] if candidate["id"] == search["selected_candidate"])
