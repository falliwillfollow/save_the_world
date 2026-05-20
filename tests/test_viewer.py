from __future__ import annotations

import unittest
from pathlib import Path

from ciac.io import load_data


ROOT = Path(__file__).resolve().parents[1]


class ViewerTests(unittest.TestCase):
    def test_static_viewer_files_exist_and_reference_runtime_bundle(self) -> None:
        index = (ROOT / "viewer" / "index.html").read_text(encoding="utf-8")
        app = (ROOT / "viewer" / "app.js").read_text(encoding="utf-8")
        styles = (ROOT / "viewer" / "styles.css").read_text(encoding="utf-8")

        self.assertIn("CIaC Runtime Viewer", index)
        self.assertIn("Selected System", index)
        self.assertIn("Foundation", index)
        self.assertIn("Why Failing", index)
        self.assertIn("Storage", index)
        self.assertIn("playDays", index)
        self.assertIn("../examples/generated/micro_commons_runtime_bundle.json", app)
        self.assertIn("../examples/generated/micro_commons_foundation_gate.json", app)
        self.assertIn("renderFoundation", app)
        self.assertIn("loadDefaultFoundationGate", app)
        self.assertIn("renderFoundationLoadError", app)
        self.assertIn("noStorePath", app)
        self.assertIn("foundationStatusClass", app)
        self.assertIn("layout_graph", app)
        self.assertIn("runtime_failures", app)
        self.assertIn("selectedScenarioFailures", app)
        self.assertIn("renderFailureReasons", app)
        self.assertIn("renderStorage", app)
        self.assertIn("storage_recovery_tasks", app)
        self.assertIn("review_context", app)
        self.assertIn("scenario_events", app)
        self.assertIn(".map-stage", styles)
        self.assertIn(".zone-failure", styles)
        self.assertIn(".system-chip.has-warning", styles)
        self.assertIn(".foundation-check", styles)

    def test_generated_bundle_has_viewer_ready_sections(self) -> None:
        bundle = load_data(ROOT / "examples" / "generated" / "micro_commons_runtime_bundle.json")

        self.assertEqual(bundle["kind"], "RuntimeBundle")
        self.assertIn("layout_graph", bundle["site"])
        self.assertTrue(bundle["systems"])
        self.assertTrue(bundle["timeline"]["daily_states"])
        self.assertIn("storage", bundle["timeline"]["daily_states"][0])
        self.assertIn("do_not_visualize_as_proof", bundle["viewer_hints"])

    def test_generated_foundation_gate_is_viewer_ready(self) -> None:
        gate = load_data(ROOT / "examples" / "generated" / "micro_commons_foundation_gate.json")

        self.assertEqual(gate["kind"], "FoundationGateReport")
        self.assertEqual(gate["status"], "ready_with_warnings")
        self.assertTrue(gate["checks"])
        self.assertTrue(any(check["status"] == "warn" for check in gate["checks"]))


if __name__ == "__main__":
    unittest.main()
