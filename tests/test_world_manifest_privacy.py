from __future__ import annotations

import unittest
from pathlib import Path

from ciac.io import load_data
from ciac.world_manifest import build_world_manifest


ROOT = Path(__file__).resolve().parents[1]


class WorldManifestPrivacyTests(unittest.TestCase):
    def setUp(self) -> None:
        runtime = load_data(ROOT / "examples" / "generated" / "micro_commons_runtime_bundle.json")
        self.manifest = build_world_manifest(runtime, population=80)

    def test_residents_are_archetype_only(self) -> None:
        self.assertTrue(self.manifest["residents"])
        self.assertTrue(all(resident["privacy"] == "archetype_only" for resident in self.manifest["residents"]))

    def test_no_real_names_required(self) -> None:
        for resident in self.manifest["residents"]:
            self.assertNotIn("name", resident)
            self.assertIn("archetype", resident)

    def test_no_health_or_private_finance_fields_are_exposed(self) -> None:
        forbidden = {"health_status", "diagnosis", "disability_status", "income", "debt", "payment_status"}
        for resident in self.manifest["residents"]:
            self.assertFalse(forbidden.intersection(resident))


if __name__ == "__main__":
    unittest.main()
