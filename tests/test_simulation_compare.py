from __future__ import annotations

import unittest
import tempfile
from pathlib import Path

from ciac.cli import main
from ciac.compiler import compile_plan, load_patterns
from ciac.io import load_data
from ciac.simulation import simulate
from ciac.simulation_compare import compare_simulations
from ciac.validation import validate_data


ROOT = Path(__file__).resolve().parents[1]


class SimulationCompareTests(unittest.TestCase):
    def setUp(self) -> None:
        patterns = load_patterns(ROOT / "patterns")
        site = load_data(ROOT / "examples" / "site_profiles" / "micro_commons_5_households.yaml")
        self.plan = compile_plan(site, patterns)

    def test_simulation_comparison_reports_stress_warning(self) -> None:
        baseline = simulate(self.plan, days=14)
        replay = simulate(self.plan, days=14, scenario=load_data(ROOT / "scenarios" / "water_contamination_response_v2.yaml"))

        report = compare_simulations(baseline, replay)

        self.assertEqual(report["kind"], "SimulationComparisonReport")
        self.assertEqual(report["status"], "stress_warn")
        self.assertEqual(report["scenario_context"]["id"], "water_contamination_response_v2")
        self.assertTrue(any(item["resource"] == "labor_hours" and item["delta"] == 0 for item in report["unmet_need_deltas"]))
        self.assertTrue(any(item["resource"] == "water_liters" and item["delta"] == 0 for item in report["unmet_need_deltas"]))
        self.assertGreater(report["labor_delta"]["scenario_emergency_hours"], 0)
        self.assertIn("water_public_health", report["review_delta"]["new_blocked_domains"])
        self.assertTrue(validate_data(report, "simulation-comparison").ok)

    def test_stable_comparison_when_runs_match(self) -> None:
        baseline = simulate(self.plan, days=7)
        replay = simulate(self.plan, days=7)

        report = compare_simulations(baseline, replay)

        self.assertEqual(report["status"], "stable")
        self.assertFalse(report["review_delta"]["new_blocked_domains"])
        self.assertTrue(all(item["delta"] == 0 for item in report["unmet_need_deltas"]))

    def test_cli_compare_simulations_writes_report(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "simulation_comparison.json"
            code = main(
                [
                    "compare-simulations",
                    str(ROOT / "examples" / "generated" / "micro_commons_simulation.json"),
                    str(ROOT / "examples" / "generated" / "water_contamination_response_v2_replay_simulation.json"),
                    "--output",
                    str(output),
                ]
            )

            self.assertEqual(code, 0)
            report = load_data(output)
            self.assertEqual(report["kind"], "SimulationComparisonReport")

    def test_simulation_comparison_shape_is_stable(self) -> None:
        report = compare_simulations(simulate(self.plan, days=1), simulate(self.plan, days=1))

        self.assertEqual(
            list(report.keys()),
            [
                "kind",
                "id",
                "baseline_simulation",
                "replay_simulation",
                "generated_by",
                "provisional",
                "status",
                "scenario_context",
                "status_delta",
                "duration",
                "resource_deltas",
                "storage_deltas",
                "labor_delta",
                "unmet_need_deltas",
                "failure_day_delta",
                "recovery_delta",
                "review_delta",
                "bottlenecks",
                "summary",
                "unknowns",
            ],
        )


if __name__ == "__main__":
    unittest.main()
