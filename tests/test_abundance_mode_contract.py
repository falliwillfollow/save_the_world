from __future__ import annotations

import unittest
from pathlib import Path

from ciac.io import load_data
from ciac.validation import validate_data


class AbundanceModeContractTests(unittest.TestCase):
    def test_viewer_can_load_manifest_fixtures(self) -> None:
        life = load_data("examples/life_manifests/life_manifest_80_v0.json")
        automation = load_data("examples/life_manifests/automation_manifest_80_v0.json")

        self.assertTrue(validate_data(life, "life-fixture").ok)
        self.assertTrue(validate_data(automation, "automation-fixture").ok)
        self.assertGreater(life["metrics"]["life_returned_hours_per_week"], 0)
        self.assertGreater(len(automation["tasks"]), 0)

    def test_abundance_mode_available(self) -> None:
        switcher = Path("viewer/world3d/src/components/ModeSwitcher.jsx").read_text(encoding="utf-8")
        app = Path("viewer/world3d/src/App.jsx").read_text(encoding="utf-8")

        self.assertIn("abundance", switcher)
        self.assertIn("AbundanceMode", app)

    def test_abundance_components_receive_contract_fields(self) -> None:
        life_card = Path("viewer/world3d/src/components/LifeReturnedCard.jsx").read_text(encoding="utf-8")
        automation_panel = Path("viewer/world3d/src/components/AutomationSubstratePanel.jsx").read_text(encoding="utf-8")
        sovereignty_panel = Path("viewer/world3d/src/components/HumanSovereigntyPanel.jsx").read_text(encoding="utf-8")

        self.assertIn("life_returned_hours_per_week", life_card)
        self.assertIn("tasks", automation_panel)
        self.assertIn("blocked_automation_domains", sovereignty_panel)


if __name__ == "__main__":
    unittest.main()
