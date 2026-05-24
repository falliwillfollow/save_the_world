from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from ciac.cli import main
from ciac.discovery import build_discovery_loop
from ciac.io import load_data
from ciac.validation import validate_data


ROOT = Path(__file__).resolve().parents[1]
WORLD = ROOT / "examples" / "world_manifests" / "civic_floor_80_v0.world.json"
RUNTIME = ROOT / "examples" / "generated" / "micro_commons_runtime_bundle.json"


class DiscoveryLoopTests(unittest.TestCase):
    def setUp(self) -> None:
        self.world = load_data(WORLD)
        self.runtime = load_data(RUNTIME)

    def test_discovery_loop_builds_valid_report_and_candidates(self) -> None:
        report = build_discovery_loop(self.world, self.runtime, focus="all")

        self.assertEqual(report["kind"], "DiscoveryLoopReport")
        self.assertEqual(report["status"], "ready_for_generation")
        self.assertGreaterEqual(len(report["findings"]), 4)
        self.assertGreaterEqual(len(report["seed_candidates"]), 6)
        self.assertTrue(validate_data(report, "discovery-loop").ok)
        for candidate in report["seed_candidates"]:
            self.assertTrue(validate_data(candidate, candidate["id"]).ok)

    def test_discovery_loop_focuses_on_care_health(self) -> None:
        report = build_discovery_loop(self.world, self.runtime, focus="care_health")

        self.assertEqual([finding["domain"] for finding in report["findings"]], ["care_health"])
        titles = {candidate["title"] for candidate in report["seed_candidates"]}
        self.assertIn("Resident-controlled medication continuity kit", titles)
        self.assertIn("Critical-load medication cold-chain cabinet", titles)

    def test_cli_discovery_loop_writes_report(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "discovery.json"
            code = main(
                [
                    "discovery-loop",
                    str(WORLD),
                    "--runtime",
                    str(RUNTIME),
                    "--focus",
                    "care_health",
                    "--output",
                    str(output),
                ]
            )

            self.assertEqual(code, 0)
            report = load_data(output)
            self.assertEqual(report["kind"], "DiscoveryLoopReport")
            self.assertEqual(report["focus"], "care_health")


if __name__ == "__main__":
    unittest.main()
