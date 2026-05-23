import tempfile
import unittest
from pathlib import Path

from ciac.cli import main
from ciac.compiler import load_patterns
from ciac.complexity import generate_complexity_report
from ciac.food_labor import generate_food_labor_report
from ciac.io import load_data
from ciac.node_scaling import generate_node_scaling_report
from ciac.topology_optimizer import generate_topology_recommendation
from ciac.validation import validate_data


ROOT = Path(__file__).resolve().parents[1]
GENERATED = ROOT / "examples" / "generated"


class TopologyOptimizerTests(unittest.TestCase):
    def setUp(self) -> None:
        registry = load_data(ROOT / "module_registries" / "micro_commons_default_v0.yaml")
        scale_profile = load_data(ROOT / "scale_profiles" / "micro_commons_scale_targets_v0.yaml")
        patterns = load_patterns(ROOT / "patterns")
        self.node_scaling = generate_node_scaling_report(registry, scale_profile, [978])
        self.food_labor = generate_food_labor_report(registry, patterns, "food_production", [978])
        self.complexity = generate_complexity_report(registry, patterns)

    def test_topology_recommendation_preplans_second_cell_at_150_people(self) -> None:
        report = generate_topology_recommendation(self.node_scaling, 150, self.food_labor, self.complexity)

        self.assertEqual(report["kind"], "TopologyRecommendationReport")
        self.assertEqual(report["status"], "action_recommended")
        self.assertEqual(report["selected_action"]["id"], "replicate_village_node_pools")
        self.assertIn("food_production", report["selected_action"]["affected_slots"])
        self.assertEqual(report["node_summary"]["replicated_slot_count"], 3)
        self.assertTrue(validate_data(report, "topology-recommendation").ok)

    def test_topology_recommendation_scales_up_at_1500_people(self) -> None:
        report = generate_topology_recommendation(self.node_scaling, 1500, self.food_labor, self.complexity)

        self.assertEqual(report["selected_action"]["id"], "replicate_village_node_pools")
        self.assertEqual(report["node_summary"]["replicated_slot_count"], 14)
        action_ids = {action["id"] for action in report["candidate_actions"]}
        self.assertIn("add_town_city_capability_layer", action_ids)
        self.assertIn("federate_cross_node_control_plane", action_ids)

    def test_topology_recommendation_scales_up_at_operator_selected_population(self) -> None:
        report = generate_topology_recommendation(self.node_scaling, 978, self.food_labor, self.complexity)

        self.assertEqual(report["population"], 978)
        self.assertEqual(report["selected_action"]["id"], "replicate_village_node_pools")
        self.assertEqual(report["node_summary"]["total_desired_nodes"], 110)
        action_ids = {action["id"] for action in report["candidate_actions"]}
        self.assertIn("add_town_city_capability_layer", action_ids)
        self.assertIn("federate_cross_node_control_plane", action_ids)
        self.assertTrue(validate_data(report, "topology-recommendation").ok)

    def test_cli_topology_recommend_writes_report(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "topology_recommendation.json"
            code = main(
                [
                    "topology-recommend",
                    str(GENERATED / "micro_commons_node_scaling.json"),
                    "--population",
                    "150",
                    "--food-labor",
                    str(GENERATED / "micro_commons_food_labor_report.json"),
                    "--complexity",
                    str(GENERATED / "micro_commons_complexity_report.json"),
                    "--output",
                    str(output),
                ]
            )

            self.assertEqual(code, 0)
            report = load_data(output)
            self.assertEqual(report["kind"], "TopologyRecommendationReport")
            self.assertEqual(report["population"], 150)


if __name__ == "__main__":
    unittest.main()
