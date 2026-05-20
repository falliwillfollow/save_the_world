from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from ciac.cli import main
from ciac.compiler import compile_plan, load_patterns
from ciac.io import load_data
from ciac.replay_matrix import build_replay_matrix
from ciac.simulation import simulate
from ciac.simulation_compare import compare_simulations
from ciac.validation import validate_data


ROOT = Path(__file__).resolve().parents[1]


class ReplayMatrixTests(unittest.TestCase):
    def setUp(self) -> None:
        patterns = load_patterns(ROOT / "patterns")
        site = load_data(ROOT / "examples" / "site_profiles" / "micro_commons_5_households.yaml")
        self.plan = compile_plan(site, patterns)

    def test_replay_matrix_ranks_stressors(self) -> None:
        contamination = _comparison(self.plan, "water_contamination_response_v2.yaml")
        energy = _comparison(self.plan, "energy_outage_reserve_v2.yaml")

        matrix = build_replay_matrix([energy, contamination])

        self.assertEqual(matrix["kind"], "ReplayMatrixReport")
        self.assertEqual(matrix["status"], "stress_warn")
        self.assertEqual(matrix["comparison_count"], 2)
        self.assertEqual(matrix["rankings"][0]["scenario"], "water_contamination_response_v2")
        self.assertGreaterEqual(matrix["rankings"][0]["stress_score"], matrix["rankings"][1]["stress_score"])
        self.assertGreater(matrix["rankings"][0]["stress_score_per_day"], 0)
        self.assertEqual(matrix["rankings"][0]["replay_days"], 14)
        self.assertTrue(validate_data(matrix, "replay-matrix").ok)

    def test_replay_matrix_can_be_stable(self) -> None:
        baseline = simulate(self.plan, days=7)
        comparison = compare_simulations(baseline, baseline)

        matrix = build_replay_matrix([comparison])

        self.assertEqual(matrix["status"], "stable")
        self.assertEqual(matrix["top_stressor"]["stress_score"], 0)

    def test_replay_matrix_requires_comparisons(self) -> None:
        with self.assertRaises(ValueError):
            build_replay_matrix([])

    def test_cli_replay_matrix_writes_report(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "matrix.json"
            code = main(
                [
                    "replay-matrix",
                    str(ROOT / "examples" / "generated" / "water_contamination_response_v2_replay_comparison.json"),
                    "--output",
                    str(output),
                ]
            )

            self.assertEqual(code, 0)
            matrix = load_data(output)
            self.assertEqual(matrix["kind"], "ReplayMatrixReport")


def _comparison(plan: dict, scenario_name: str) -> dict:
    scenario = load_data(ROOT / "scenarios" / scenario_name)
    days = int(scenario["days"])
    baseline = simulate(plan, days=days)
    replay = simulate(plan, days=days, scenario=scenario)
    return compare_simulations(baseline, replay)


if __name__ == "__main__":
    unittest.main()
