from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from ciac.cli import main
from ciac.compiler import load_patterns
from ciac.io import load_data
from ciac.optimization import evaluate_optimization_readiness
from ciac.validation import validate_data


ROOT = Path(__file__).resolve().parents[1]


class OptimizationReadinessTests(unittest.TestCase):
    def setUp(self) -> None:
        self.patterns = load_patterns(ROOT / "patterns")
        self.profile = load_data(ROOT / "optimization_profiles" / "minimum_dignity_v0.yaml")

    def test_optimization_profile_validates(self) -> None:
        self.assertTrue(validate_data(self.profile, "optimization-profile").ok)

    def test_readiness_report_tracks_chunk_a_metrics(self) -> None:
        report = evaluate_optimization_readiness(self.patterns, self.profile)

        self.assertEqual(report["kind"], "OptimizationReadinessReport")
        self.assertEqual(report["status"], "ready_with_warnings")
        self.assertEqual(report["metric_updates"]["inspectable_simulation_proof_of_concept"], "80%")
        self.assertEqual(report["metric_updates"]["mature_commune_virtualization_data_contract"], "68%")
        self.assertEqual(report["metric_updates"]["faithful_pattern_optimization_engine"], "50%")
        self.assertTrue(validate_data(report, "optimization-readiness").ok)

    def test_readiness_requires_reserve_pattern_tunables(self) -> None:
        patterns = dict(self.patterns)
        broken = dict(patterns["emergency_water_reserve"])
        broken["optimization"] = {**broken["optimization"], "tunable_parameters": []}
        patterns["emergency_water_reserve"] = broken

        report = evaluate_optimization_readiness(patterns, self.profile)

        self.assertEqual(report["status"], "not_ready")
        self.assertTrue(any("emergency_water_reserve" in gap for gap in report["readiness_gaps"]))

    def test_cli_optimization_readiness_writes_report(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "optimization_readiness.json"
            code = main(
                [
                    "optimization-readiness",
                    str(ROOT / "patterns"),
                    str(ROOT / "optimization_profiles" / "minimum_dignity_v0.yaml"),
                    "--output",
                    str(output),
                ]
            )

            self.assertEqual(code, 0)
            report = load_data(output)
            self.assertEqual(report["kind"], "OptimizationReadinessReport")


if __name__ == "__main__":
    unittest.main()
