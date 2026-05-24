from __future__ import annotations

import unittest
from pathlib import Path

from ciac.io import load_data
from ciac.validation import validate_data


ROOT = Path(__file__).resolve().parents[1]


class ScalingPolicyTests(unittest.TestCase):
    def setUp(self) -> None:
        self.policy = load_data(ROOT / "scale_policies" / "ciac_scaling_policy_v0.yaml")

    def test_scaling_policy_validates(self) -> None:
        report = validate_data(self.policy, "scaling-policy")

        self.assertTrue(report.ok, [issue.message for issue in report.issues])

    def test_policy_encodes_human_scale_thresholds(self) -> None:
        policies = {item["id"]: item for item in self.policy["node_policies"]}

        self.assertEqual(policies["residential_pod"]["maximum"], 24)
        self.assertEqual(policies["common_house"]["maximum"], 100)
        self.assertEqual(policies["shared_kitchen"]["hard_max"], 100)
        self.assertEqual(policies["potable_water"]["regulatory_strength"], "binding")
        self.assertEqual(policies["operational_circle"]["maximum"], 12)
        self.assertEqual(policies["hands_on_skill_group"]["maximum"], 8)
        self.assertEqual(self.policy["global_layers"]["village_block"]["comfortable_max"], 150)
        self.assertIn("docs/scaling_research/ciac_deep_research_scaling_thresholds_part_2_v0_2.md", self.policy["research_inputs"])
        self.assertIn("docs/scaling_research/ciac_deep_research_scaling_thresholds_part_3_v0_1.md", self.policy["research_inputs"])
        self.assertIn("docs/scaling_research/ciac_deep_research_scaling_thresholds_part_4_v0_1.md", self.policy["research_inputs"])


if __name__ == "__main__":
    unittest.main()
