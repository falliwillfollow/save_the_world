from __future__ import annotations

import unittest
from pathlib import Path

from ciac.capability_policy import iter_gates, load_capability_policy
from ciac.io import load_data
from ciac.validation import validate_data


ROOT = Path(__file__).resolve().parents[1]
SCENARIO_DIR = ROOT / "scenarios" / "capability"


class CapabilityScenarioTests(unittest.TestCase):
    def setUp(self) -> None:
        self.policy = load_capability_policy(ROOT / "capability_policies" / "ciac_capability_policy_v0.yaml")
        self.policy_fields = {
            field
            for domain in self.policy["domains"].values()
            for field in domain["capability_fields"]
        }
        self.gate_ids = {gate["gate_id"] for gate in iter_gates(self.policy)}

    def test_required_scenario_files_exist_and_validate(self) -> None:
        for domain, domain_policy in self.policy["domains"].items():
            for scenario_id in domain_policy.get("scenarios", []):
                scenario_path = SCENARIO_DIR / f"{scenario_id}.yaml"
                self.assertTrue(scenario_path.exists(), f"{domain}:{scenario_id}")
                scenario = load_data(scenario_path)
                self.assertTrue(validate_data(scenario, str(scenario_path)).ok)

    def test_scenario_capability_fields_and_gates_resolve(self) -> None:
        for scenario_path in SCENARIO_DIR.glob("*.yaml"):
            scenario = load_data(scenario_path)
            for field in scenario["required_capability_fields"]:
                self.assertIn(field, self.policy_fields, f"{scenario_path.name}:{field}")
            for gate_id in scenario["expected_gates"]:
                self.assertIn(gate_id, self.gate_ids, f"{scenario_path.name}:{gate_id}")


if __name__ == "__main__":
    unittest.main()
