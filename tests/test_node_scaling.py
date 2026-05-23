import tempfile
import unittest
from pathlib import Path

from ciac.cli import main
from ciac.io import load_data
from ciac.node_scaling import generate_node_scaling_report
from ciac.validation import validate_data


ROOT = Path(__file__).resolve().parents[1]


class NodeScalingTests(unittest.TestCase):
    def setUp(self) -> None:
        self.registry = load_data(ROOT / "module_registries" / "micro_commons_default_v0.yaml")
        self.scale_profile = load_data(ROOT / "scale_profiles" / "micro_commons_scale_targets_v0.yaml")

    def test_registry_slots_declare_node_policies(self) -> None:
        report = validate_data(self.registry, "module-registry")

        self.assertTrue(report.ok, [issue.message for issue in report.issues])
        self.assertIn("Abundance", self.registry["flourishing_posture"]["frame"])
        self.assertIn("city", self.registry["flourishing_posture"]["scope_rule"])
        for slot in self.registry["slots"]:
            self.assertIn("node_policy", slot)
            policy = slot["node_policy"]
            self.assertLessEqual(policy["minimum_population_per_node"], policy["preferred_population_per_node"])
            self.assertLessEqual(policy["preferred_population_per_node"], policy["maximum_population_per_node"])

    def test_node_scaling_report_represents_civic_node_pools(self) -> None:
        report = generate_node_scaling_report(self.registry, self.scale_profile)

        self.assertEqual(report["kind"], "InfrastructureNodeReport")
        self.assertEqual(report["status"], "ready_with_warnings")
        self.assertIn("Abundance", report["orchestration_model"]["flourishing_frame"])
        self.assertIn("city", report["orchestration_model"]["scope_rule"])
        self.assertEqual(len(report["node_policy_catalog"]), 14)
        food_policy = next(policy for policy in report["node_policy_catalog"] if policy["slot"] == "food_production")
        self.assertEqual(food_policy["maximum_population_per_node"], 80)
        self.assertIn("hybrid_food_commons", food_policy["accepted_patterns"])
        targets = {target["people"]: target for target in report["target_results"]}
        self.assertEqual(targets[12]["scaled_down_slot_count"], 10)
        food_12 = next(slot for slot in targets[12]["slot_results"] if slot["slot"] == "food_production")
        self.assertEqual(food_12["mode"], "seed_or_minimal")
        food_150 = next(slot for slot in targets[150]["slot_results"] if slot["slot"] == "food_production")
        self.assertEqual(food_150["mode"], "replicated_nodes")
        self.assertEqual(food_150["desired_nodes"], 2)
        food_1500 = next(slot for slot in targets[1500]["slot_results"] if slot["slot"] == "food_production")
        self.assertEqual(food_1500["mode"], "replicated_nodes")
        self.assertEqual(food_1500["desired_nodes"], 19)
        water_1500 = next(slot for slot in targets[1500]["slot_results"] if slot["slot"] == "potable_water_source")
        energy_1500 = next(slot for slot in targets[1500]["slot_results"] if slot["slot"] == "critical_energy")
        self.assertEqual(water_1500["desired_nodes"], 15)
        self.assertEqual(energy_1500["desired_nodes"], 15)
        self.assertEqual(targets[1500]["tier_node_counts"]["floor_systems"], 69)
        self.assertTrue(validate_data(report, "node-scaling").ok)

    def test_node_scaling_report_accepts_ad_hoc_people_target(self) -> None:
        report = generate_node_scaling_report(self.registry, self.scale_profile, [978])
        targets = {target["people"]: target for target in report["target_results"]}

        self.assertIn(978, targets)
        self.assertEqual(targets[978]["replicated_slot_count"], 14)
        self.assertEqual(targets[978]["total_desired_nodes"], 110)
        food_978 = next(slot for slot in targets[978]["slot_results"] if slot["slot"] == "food_production")
        self.assertEqual(food_978["desired_nodes"], 13)
        self.assertEqual(food_978["action"], "scale_up")
        self.assertTrue(validate_data(report, "node-scaling").ok)

    def test_cli_node_scaling_writes_report(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "node_scaling.json"
            code = main(
                [
                    "node-scaling",
                    str(ROOT / "module_registries" / "micro_commons_default_v0.yaml"),
                    "--scale-profile",
                    str(ROOT / "scale_profiles" / "micro_commons_scale_targets_v0.yaml"),
                    "--people",
                    "978",
                    "--output",
                    str(output),
                ]
            )

            self.assertEqual(code, 0)
            report = load_data(output)
            self.assertEqual(report["kind"], "InfrastructureNodeReport")
            self.assertEqual(report["scale_profile"], "micro_commons_scale_targets_v0")
            self.assertIn(978, {target["people"] for target in report["target_results"]})


if __name__ == "__main__":
    unittest.main()
