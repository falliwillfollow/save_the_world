from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from ciac.cli import main
from ciac.io import load_data
from ciac.validation import validate_data
from ciac.visualization_bundle import build_visualization_bundle


ROOT = Path(__file__).resolve().parents[1]
GENERATED = ROOT / "examples" / "generated"


class VisualizationBundleTests(unittest.TestCase):
    def setUp(self) -> None:
        self.runtime = load_data(GENERATED / "micro_commons_runtime_bundle.json")
        self.foundation = load_data(GENERATED / "micro_commons_foundation_gate.json")
        self.matrix = load_data(GENERATED / "micro_commons_candidate_matrix.json")
        self.scale = load_data(GENERATED / "micro_commons_tradeoff_scale.json")
        self.optimizer = load_data(GENERATED / "micro_commons_optimizer_report.json")

    def test_visualization_bundle_shape_is_stable(self) -> None:
        bundle = build_visualization_bundle(self.runtime, self.foundation, self.matrix, self.scale, self.optimizer)

        self.assertEqual(
            list(bundle.keys()),
            [
                "kind",
                "id",
                "schema_version",
                "generated_by",
                "provisional",
                "status",
                "selected_candidate",
                "manifest",
                "site",
                "runtime",
                "optimization",
                "viewer_contract",
                "metric_updates",
                "next_actions",
                "unknowns",
            ],
        )
        self.assertEqual(bundle["kind"], "VisualizationBundle")
        self.assertEqual(bundle["schema_version"], "visualization_bundle.v0")
        self.assertTrue(validate_data(bundle, "visualization-bundle").ok)

    def test_visualization_bundle_freezes_runtime_and_optimizer_entrypoints(self) -> None:
        bundle = build_visualization_bundle(self.runtime, self.foundation, self.matrix, self.scale, self.optimizer)

        self.assertEqual(bundle["selected_candidate"], "current_plan")
        self.assertEqual(bundle["status"], "ready_with_warnings")
        self.assertEqual(bundle["runtime"]["summary"]["days"], 365)
        self.assertEqual(bundle["optimization"]["candidate_summaries"][0]["candidate"], "current_plan")
        self.assertTrue(bundle["optimization"]["candidate_summaries"][0]["selected"])
        self.assertIn("$.runtime.bundle.timeline.daily_states", bundle["viewer_contract"]["stable_entrypoints"])
        self.assertIn("$.optimization.sensitivity_checks", bundle["viewer_contract"]["stable_entrypoints"])

    def test_visualization_bundle_tracks_metric_completion(self) -> None:
        bundle = build_visualization_bundle(self.runtime, self.foundation, self.matrix, self.scale, self.optimizer)

        self.assertEqual(bundle["metric_updates"]["inspectable_simulation_proof_of_concept"], "100%")
        self.assertEqual(bundle["metric_updates"]["mature_commune_virtualization_data_contract"], "100%")
        self.assertEqual(bundle["metric_updates"]["faithful_pattern_optimization_engine"], "95%")
        self.assertIn("not engineering", bundle["viewer_contract"]["non_proof_notice"])

    def test_cli_export_visualization_writes_bundle(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "visualization_bundle.json"
            code = main(
                [
                    "export-visualization",
                    str(GENERATED / "micro_commons_runtime_bundle.json"),
                    str(GENERATED / "micro_commons_foundation_gate.json"),
                    str(GENERATED / "micro_commons_candidate_matrix.json"),
                    str(GENERATED / "micro_commons_tradeoff_scale.json"),
                    str(GENERATED / "micro_commons_optimizer_report.json"),
                    "--output",
                    str(output),
                ]
            )

            self.assertEqual(code, 0)
            bundle = load_data(output)
            self.assertEqual(bundle["kind"], "VisualizationBundle")


if __name__ == "__main__":
    unittest.main()
