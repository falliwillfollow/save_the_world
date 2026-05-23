import tempfile
import unittest
from pathlib import Path

from ciac.artifact_cohesion import evaluate_artifact_cohesion
from ciac.cli import main
from ciac.io import load_data
from ciac.validation import validate_data


ROOT = Path(__file__).resolve().parents[1]
GENERATED = ROOT / "examples" / "generated"


def assert_no_failures_and_only_allowed_warnings(test_case: unittest.TestCase, report: dict) -> None:
    test_case.assertEqual(report["summary"]["fail_count"], 0)
    warnings = [
        check
        for check in [*report.get("artifact_checks", []), *report.get("relationship_checks", [])]
        if check.get("status") == "warn"
    ]
    test_case.assertEqual({warning["id"] for warning in warnings}, {"viewer_run_nodes_match_node_scaling"} if warnings else set())


class ArtifactCohesionTests(unittest.TestCase):
    def test_default_viewer_artifacts_are_coherent(self) -> None:
        report = evaluate_artifact_cohesion(GENERATED)

        self.assertEqual(report["kind"], "ArtifactCohesionReport")
        self.assertIn(report["status"], {"coherent", "ready_with_warnings"})
        self.assertEqual(report["active_population"], load_data(GENERATED / "micro_commons_viewer_session_report.json")["active_population"])
        assert_no_failures_and_only_allowed_warnings(self, report)
        check_ids = {check["id"] for check in report["relationship_checks"]}
        self.assertIn("cycle_selected_candidate_matches_search", check_ids)
        self.assertIn("runtime_bundle_matches_cycle_runtime", check_ids)
        self.assertIn("runtime_water_flow_fields_visible", check_ids)
        self.assertIn("runtime_water_balance_has_temporal_movement", check_ids)
        self.assertIn("food_labor_has_active_population_row", check_ids)
        self.assertIn("topology_population_has_node_target", check_ids)
        self.assertIn("topology_total_nodes_match_node_scaling", check_ids)
        self.assertTrue(validate_data(report, "artifact-cohesion").ok)

    def test_generated_artifact_cohesion_report_is_valid(self) -> None:
        report = load_data(GENERATED / "micro_commons_artifact_cohesion.json")

        self.assertEqual(report["kind"], "ArtifactCohesionReport")
        self.assertIn(report["status"], {"coherent", "ready_with_warnings"})
        self.assertEqual(report["active_population"], load_data(GENERATED / "micro_commons_viewer_session_report.json")["active_population"])
        assert_no_failures_and_only_allowed_warnings(self, report)
        self.assertTrue(validate_data(report, "artifact-cohesion").ok)

    def test_cli_artifact_cohesion_writes_report(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "cohesion.json"
            code = main(["artifact-cohesion", str(GENERATED), "--output", str(output)])

            self.assertEqual(code, 0)
            report = load_data(output)
            self.assertEqual(report["kind"], "ArtifactCohesionReport")
            self.assertIn(report["status"], {"coherent", "ready_with_warnings"})
            assert_no_failures_and_only_allowed_warnings(self, report)


if __name__ == "__main__":
    unittest.main()
