from __future__ import annotations

import unittest

from ciac.io import load_data
from ciac.life_manifest import PROVISIONALITY_STATEMENT, build_life_manifest
from ciac.validation import validate_data


class LifeManifestTests(unittest.TestCase):
    def setUp(self) -> None:
        self.runtime = load_data("examples/generated/micro_commons_runtime_bundle.json")
        self.world = load_data("examples/world_manifests/civic_floor_80_v0.world.json")

    def test_life_manifest_schema_validates(self) -> None:
        manifest = build_life_manifest(self.runtime, self.world, population=80)

        self.assertTrue(validate_data(manifest, "life-manifest").ok)

    def test_generated_life_manifest_has_required_contract(self) -> None:
        manifest = build_life_manifest(self.runtime, self.world, population=80)

        self.assertEqual(manifest["kind"], "LifeManifest")
        self.assertIn("resident_archetypes", manifest)
        self.assertIn("baseline_model", manifest)
        self.assertIn("civic_floor_model", manifest)
        self.assertIn("promotion_blockers", manifest)
        self.assertEqual(manifest["provisionality"]["statement"], PROVISIONALITY_STATEMENT)

    def test_resident_archetypes_have_baseline_civic_and_computed_return(self) -> None:
        manifest = build_life_manifest(self.runtime, self.world, population=80)

        self.assertGreaterEqual(len(manifest["resident_archetypes"]), 3)
        for archetype in manifest["resident_archetypes"]:
            self.assertIn("weekly_hours", archetype["baseline_life"])
            self.assertIn("weekly_hours", archetype["civic_floor_life"])
            self.assertIn("hours_per_week", archetype["life_returned"])

        self.assertGreater(manifest["metrics"]["life_returned_hours_per_week"], 0)
        self.assertEqual(manifest["metrics"]["hidden_labor_status"], "pass")


if __name__ == "__main__":
    unittest.main()
