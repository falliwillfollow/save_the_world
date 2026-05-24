from __future__ import annotations

import unittest
from pathlib import Path

from ciac.io import load_data
from ciac.validation import validate_data
from ciac.world_manifest import build_world_manifest, infer_scale


ROOT = Path(__file__).resolve().parents[1]


class WorldManifestExportTests(unittest.TestCase):
    def setUp(self) -> None:
        self.runtime = load_data(ROOT / "examples" / "generated" / "micro_commons_runtime_bundle.json")
        self.manifest = build_world_manifest(self.runtime, population=80, runtime_bundle_path="runtime.json", world_id="test_world")

    def test_build_world_manifest_returns_required_top_level_keys(self) -> None:
        self.assertEqual(
            list(self.manifest.keys()),
            [
                "kind",
                "version",
                "world_id",
                "generated_at",
                "source",
                "population",
                "scale",
                "modules",
                "zones",
                "structures",
                "paths",
                "infrastructure_nodes",
                "residents",
                "daily_events",
                "scenario_states",
                "overlays",
                "resource_telemetry",
                "evidence_cards",
                "warnings",
                "failures",
                "unknowns",
            ],
        )
        self.assertTrue(validate_data(self.manifest, "world").ok)

    def test_population_80_gives_village_block(self) -> None:
        self.assertEqual(infer_scale(80)["scale_class"], "village_block")
        self.assertEqual(self.manifest["scale"]["scale_class"], "village_block")

    def test_manifest_includes_core_world_objects(self) -> None:
        structure_ids = {item["id"] for item in self.manifest["structures"]}
        node_ids = {item["id"] for item in self.manifest["infrastructure_nodes"]}

        self.assertIn("structure_common_house", structure_ids)
        self.assertIn("structure_residential_pod_1", structure_ids)
        self.assertIn("structure_protein_commons", structure_ids)
        self.assertIn("node_solar_battery", node_ids)
        self.assertIn("node_water_reserve", node_ids)

    def test_manifest_includes_evidence_residents_and_overlays(self) -> None:
        self.assertGreaterEqual(len(self.manifest["residents"]), 12)
        self.assertTrue(self.manifest["daily_events"])
        self.assertTrue(self.manifest["evidence_cards"])
        self.assertIn("water", self.manifest["overlays"])
        self.assertIn("labor_time", self.manifest["overlays"])

    def test_manifest_includes_resource_telemetry(self) -> None:
        telemetry = self.manifest["resource_telemetry"]
        resource_ids = {item["id"] for item in telemetry["resources"]}

        self.assertEqual({"water", "food", "energy"}, resource_ids)
        self.assertGreater(telemetry["labor"]["required_minutes_per_resident_per_day"], 0)
        for resource in telemetry["resources"]:
            self.assertGreaterEqual(resource["current_ratio"], 0)
            self.assertLessEqual(resource["current_ratio"], 1)
            self.assertIn("drawdown", resource)


if __name__ == "__main__":
    unittest.main()
