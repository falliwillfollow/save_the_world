from __future__ import annotations

import unittest
from pathlib import Path

from ciac.capability_policy import get_required_scenarios, iter_gates, load_capability_policy
from ciac.io import load_data
from ciac.validation import validate_data


ROOT = Path(__file__).resolve().parents[1]
POLICY_PATH = ROOT / "capability_policies" / "ciac_capability_policy_v0.yaml"


class CapabilityPolicyTests(unittest.TestCase):
    def setUp(self) -> None:
        self.policy = load_capability_policy(POLICY_PATH)

    def test_policy_file_validates(self) -> None:
        report = validate_data(load_data(POLICY_PATH), str(POLICY_PATH))

        self.assertTrue(report.ok, [issue.message for issue in report.issues])

    def test_gate_source_ids_resolve(self) -> None:
        source_ids = {source["id"] for source in self.policy["source_registry"]}

        for gate in iter_gates(self.policy):
            self.assertTrue(set(gate["source_ids"]).issubset(source_ids), gate["gate_id"])

    def test_policy_covers_core_capability_domains(self) -> None:
        self.assertEqual(
            set(self.policy["domains"]),
            {
                "care_health",
                "sanitation",
                "governance_anticapture",
                "mobility_access",
                "legal_land_finance",
                "risk_resilience",
                "labor_time",
            },
        )
        for domain in self.policy["domains"]:
            self.assertTrue(list(iter_gates(self.policy, domain)), domain)

    def test_scenario_requirements_include_all_domains(self) -> None:
        scenarios = get_required_scenarios(self.policy)

        self.assertIn("illness_wave", scenarios)
        self.assertIn("route_blockage", scenarios)
        self.assertIn("scale_80_300_730_1500", scenarios)


if __name__ == "__main__":
    unittest.main()
