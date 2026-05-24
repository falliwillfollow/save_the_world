from __future__ import annotations

import copy
import unittest
from pathlib import Path

from ciac.io import load_data
from ciac.validation import validate_data


ROOT = Path(__file__).resolve().parents[1]
SAMPLE = ROOT / "examples" / "world_manifests" / "civic_floor_80_v0.world.json"


class WorldManifestSchemaTests(unittest.TestCase):
    def setUp(self) -> None:
        self.manifest = load_data(SAMPLE)

    def test_sample_manifest_validates(self) -> None:
        report = validate_data(self.manifest, str(SAMPLE))

        self.assertTrue(report.ok, [issue.message for issue in report.issues])

    def test_missing_top_level_kind_fails(self) -> None:
        manifest = copy.deepcopy(self.manifest)
        manifest.pop("kind")

        self.assertFalse(validate_data(manifest, "missing-kind").ok)

    def test_missing_structures_fails(self) -> None:
        manifest = copy.deepcopy(self.manifest)
        manifest.pop("structures")

        self.assertFalse(validate_data(manifest, "missing-structures").ok)

    def test_missing_resource_telemetry_fails(self) -> None:
        manifest = copy.deepcopy(self.manifest)
        manifest.pop("resource_telemetry")

        self.assertFalse(validate_data(manifest, "missing-resource-telemetry").ok)

    def test_invalid_scale_class_fails(self) -> None:
        manifest = copy.deepcopy(self.manifest)
        manifest["scale"]["scale_class"] = "castle"

        self.assertFalse(validate_data(manifest, "bad-scale").ok)


if __name__ == "__main__":
    unittest.main()
