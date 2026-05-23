import shutil
import tempfile
import unittest
from pathlib import Path

from ciac.artifact_cohesion import evaluate_artifact_cohesion
from ciac.compiler import load_patterns
from ciac.io import load_data
from ciac.node_scaling import generate_node_scaling_report
from ciac.viewer_cycle_pipeline import adapt_compiled_plan_for_population
from ciac.viewer_pipeline import regenerate_viewer_population_reports
from ciac.viewer_session import append_viewer_run_event, append_viewer_run_event_to_path, empty_viewer_run_report
from ciac.validation import validate_data


ROOT = Path(__file__).resolve().parents[1]
GENERATED = ROOT / "examples" / "generated"


class ViewerSessionTests(unittest.TestCase):
    def test_append_viewer_run_event_records_population_and_topology(self) -> None:
        report = append_viewer_run_event(
            empty_viewer_run_report(),
            {
                "completed_at": "2026-05-21T21:00:00.000Z",
                "cycle_number": 1,
                "population": 553,
                "days": 365,
                "bundle_id": "bundle",
                "selected_candidate": "search_001",
                "topology_action": "replicate_village_node_pools",
                "topology_status": "action_recommended",
                "total_nodes": 56,
                "replicated_slots": 14,
                "scaled_down_slots": 0,
                "near_capacity_slots": 0,
                "tier_node_counts": {
                    "floor_systems": 20,
                    "operating_systems": 16,
                    "capacity_systems": 16,
                    "meta_systems": 4,
                },
            },
        )

        self.assertEqual(report["kind"], "ViewerRunReport")
        self.assertEqual(report["status"], "runs_recorded")
        self.assertEqual(report["active_population"], 553)
        self.assertEqual(report["run_count"], 1)
        self.assertEqual(report["runs"][0]["total_nodes"], 56)
        self.assertTrue(validate_data(report, "viewer-run").ok)

    def test_append_viewer_run_event_to_path_persists_runs(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "viewer_run.json"

            first = append_viewer_run_event_to_path(output, {"population": 553, "total_nodes": 56, "days": 365})
            second = append_viewer_run_event_to_path(output, {"population": 553, "total_nodes": 56, "days": 365})

            self.assertEqual(first["run_count"], 1)
            self.assertEqual(second["run_count"], 2)
            self.assertEqual(load_data(output)["runs"][1]["run_index"], 2)

    def test_artifact_cohesion_warns_when_latest_webapp_run_is_not_canonical(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            for filename in [
                "micro_commons_runtime_bundle.json",
                "micro_commons_foundation_gate.json",
                "micro_commons_search_optimizer_report.json",
                "micro_commons_objective_calibration.json",
                "micro_commons_weight_governance.json",
                "micro_commons_cycle_iteration.json",
                "micro_commons_food_autonomy_report.json",
                "micro_commons_food_labor_report.json",
                "micro_commons_complexity_report.json",
                "micro_commons_node_scaling.json",
                "micro_commons_topology_recommendation.json",
                "micro_commons_viewer_session_report.json",
            ]:
                shutil.copy(GENERATED / filename, target / filename)
            append_viewer_run_event_to_path(
                target / "micro_commons_viewer_session_report.json",
                {"population": 553, "total_nodes": 56, "replicated_slots": 14, "days": 365},
            )

            report = evaluate_artifact_cohesion(target)

            self.assertEqual(report["active_population"], 553)
            self.assertEqual(report["status"], "ready_with_warnings")
            warning_ids = {check["id"] for check in report["relationship_checks"] if check["status"] == "warn"}
            self.assertIn("viewer_run_population_matches_topology", warning_ids)
            self.assertIn("viewer_run_population_has_node_target", warning_ids)

    def test_viewer_pipeline_regenerates_population_reports(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            shutil.copytree(ROOT / "module_registries", root / "module_registries")
            shutil.copytree(ROOT / "scale_profiles", root / "scale_profiles")
            shutil.copytree(ROOT / "patterns", root / "patterns")
            shutil.copytree(ROOT / "optimization_profiles", root / "optimization_profiles")
            shutil.copytree(ROOT / "scenarios", root / "scenarios")
            shutil.copytree(GENERATED, root / "examples" / "generated")
            append_viewer_run_event_to_path(
                root / "examples" / "generated" / "micro_commons_viewer_session_report.json",
                {"population": 594, "total_nodes": 60, "replicated_slots": 14, "days": 365},
            )

            payload = regenerate_viewer_population_reports(root, 594)

            self.assertEqual(payload["status"], "regenerated")
            self.assertIn(594, {row["target_population"] for row in payload["food_labor"]["scaling_results"]})
            self.assertEqual(payload["complexity"]["kind"], "ComplexityReport")
            self.assertEqual(payload["node_scaling"]["target_results"][2]["people"], 594)
            self.assertEqual(payload["topology_recommendation"]["population"], 594)
            self.assertEqual(payload["topology_recommendation"]["source_reports"]["food_labor"], payload["food_labor"]["id"])
            self.assertEqual(payload["topology_recommendation"]["source_reports"]["complexity"], payload["complexity"]["id"])
            self.assertEqual(payload["topology_recommendation"]["node_summary"]["total_desired_nodes"], 60)
            self.assertEqual(payload["food_autonomy"]["kind"], "FoodAutonomyReport")
            self.assertEqual(payload["food_autonomy"]["population"], 594)
            self.assertEqual(payload["artifact_cohesion"]["status"], "coherent")
            self.assertEqual(payload["artifact_cohesion"]["active_population"], 594)

    def test_viewer_pipeline_can_materialize_cycle_from_webapp_population(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            shutil.copytree(ROOT / "module_registries", root / "module_registries")
            shutil.copytree(ROOT / "scale_profiles", root / "scale_profiles")
            shutil.copytree(ROOT / "patterns", root / "patterns")
            shutil.copytree(ROOT / "optimization_profiles", root / "optimization_profiles")
            shutil.copytree(ROOT / "scenarios", root / "scenarios")
            shutil.copytree(GENERATED, root / "examples" / "generated")
            event = {
                "population": 756,
                "total_nodes": 88,
                "replicated_slots": 14,
                "days": 7,
                "cycle_number": 3,
                "selected_candidate": "search_001",
            }
            append_viewer_run_event_to_path(
                root / "examples" / "generated" / "micro_commons_viewer_session_report.json",
                event,
            )

            payload = regenerate_viewer_population_reports(root, 756, event)

            self.assertEqual(payload["cycle_iteration"]["kind"], "CycleIterationReport")
            self.assertEqual(payload["cycle_iteration"]["cycle"]["simulated_days"], 7)
            self.assertEqual(payload["cycle_iteration"]["viewer_population_context"]["population"], 756)
            self.assertIn("resilient_water_commons", payload["cycle_iteration"]["viewer_population_context"]["active_node_patterns"])
            self.assertEqual(payload["cycle_iteration"]["applied_simulation"]["population"]["population"], 756)
            self.assertIn("resilient_water_commons", payload["cycle_iteration"]["applied_plan"]["selected_patterns"])
            self.assertIn("protein_commons_supplement", payload["cycle_iteration"]["applied_plan"]["selected_patterns"])
            self.assertNotIn("food model is partial: greenhouse output is not a complete nutrition plan", payload["cycle_iteration"]["applied_simulation"]["bottlenecks"])
            self.assertEqual(payload["runtime_bundle"]["kind"], "RuntimeBundle")
            self.assertEqual(payload["food_autonomy"]["population"], 756)
            self.assertIn("food_autonomy", payload["artifacts"])
            self.assertIn("cycle_iteration", payload["artifacts"])
            self.assertEqual(payload["artifact_cohesion"]["status"], "coherent")

    def test_population_adaptation_does_not_mutate_pattern_catalog(self) -> None:
        registry = load_data(ROOT / "module_registries" / "micro_commons_default_v0.yaml")
        scale_profile = load_data(ROOT / "scale_profiles" / "micro_commons_scale_targets_v0.yaml")
        patterns = load_patterns(ROOT / "patterns")
        base_plan = load_data(GENERATED / "micro_commons_plan.json")
        node_report = generate_node_scaling_report(registry, scale_profile, [573, 877])

        adapt_compiled_plan_for_population(base_plan, 573, node_report, registry, patterns)
        adapted = adapt_compiled_plan_for_population(base_plan, 877, node_report, registry, patterns)

        self.assertEqual(patterns["resilient_water_commons"]["simulation"]["resource_effects"]["water_liters_per_day"], 2200)
        self.assertEqual(patterns["resilient_water_commons"]["simulation"]["storage"][0]["capacity"], 9085)
        self.assertEqual(adapted["simulation_inputs"]["storage_by_pattern"]["resilient_water_commons"][0]["capacity"], 54510)


if __name__ == "__main__":
    unittest.main()
