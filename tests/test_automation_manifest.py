from __future__ import annotations

import unittest

from ciac.automation_manifest import BLOCKED_AUTOMATION_DOMAINS, build_automation_manifest, validate_no_blocked_automation_tasks
from ciac.io import load_data
from ciac.validation import validate_data


class AutomationManifestTests(unittest.TestCase):
    def setUp(self) -> None:
        self.runtime = load_data("examples/generated/micro_commons_runtime_bundle.json")
        self.world = load_data("examples/world_manifests/civic_floor_80_v0.world.json")

    def test_automation_manifest_schema_validates(self) -> None:
        manifest = build_automation_manifest(self.runtime, self.world)

        self.assertTrue(validate_data(manifest, "automation-manifest").ok)

    def test_allowed_blocked_domains_and_task_contract(self) -> None:
        manifest = build_automation_manifest(self.runtime, self.world)

        for domain in ("expulsion_or_loss_of_access", "clinical_diagnosis", "legal_judgment", "resident_consent", "determining_human_worth"):
            self.assertIn(domain, manifest["blocked_automation_domains"])
        self.assertEqual(set(BLOCKED_AUTOMATION_DOMAINS), set(manifest["blocked_automation_domains"]))
        for task in manifest["tasks"]:
            self.assertTrue(task["human_review_required"])
            self.assertTrue(task["actor"])
            self.assertTrue(task["trigger"])
            self.assertTrue(task["output"])
            self.assertTrue(task["review_gate"])
            self.assertTrue(task["privacy_level"])

    def test_no_task_matches_blocked_domain(self) -> None:
        manifest = build_automation_manifest(self.runtime, self.world)

        self.assertEqual(validate_no_blocked_automation_tasks(manifest["tasks"]), [])


if __name__ == "__main__":
    unittest.main()
