from __future__ import annotations

import unittest
from pathlib import Path

from ciac.io import load_data
from ciac.validation import validate_data


ROOT = Path(__file__).resolve().parents[1]


def assert_no_failures_and_only_allowed_warnings(test_case: unittest.TestCase, report: dict) -> None:
    test_case.assertEqual(report["summary"]["fail_count"], 0)
    warnings = [
        check
        for check in [*report.get("artifact_checks", []), *report.get("relationship_checks", [])]
        if check.get("status") == "warn"
    ]
    test_case.assertEqual({warning["id"] for warning in warnings}, {"viewer_run_nodes_match_node_scaling"} if warnings else set())


class ViewerTests(unittest.TestCase):
    def test_static_viewer_files_exist_and_reference_runtime_bundle(self) -> None:
        index = (ROOT / "viewer" / "index.html").read_text(encoding="utf-8")
        app = (ROOT / "viewer" / "app.js").read_text(encoding="utf-8")
        styles = (ROOT / "viewer" / "styles.css").read_text(encoding="utf-8")

        self.assertIn("CIaC Runtime Viewer", index)
        self.assertIn("Selected System", index)
        self.assertIn("Diagnostics and Raw Reports", index)
        self.assertIn("Foundation", index)
        self.assertIn("Optimization", index)
        self.assertIn("Cycle", index)
        self.assertIn("Scalability", index)
        self.assertIn("View Mode", index)
        self.assertIn("Baseline | normal year", app)
        self.assertIn("Why Failing", index)
        self.assertIn("Storage", index)
        self.assertIn("Involuntary Labor", index)
        self.assertNotIn("playDays", index)
        self.assertIn("runCycle", index)
        self.assertIn("reviewChange", index)
        self.assertIn("submitChange", index)
        self.assertIn("nextCycle", index)
        self.assertIn("cycleProgress", index)
        self.assertIn("runtimeKpis", index)
        self.assertIn("snapshotSummary", index)
        self.assertIn("cycleFile", index)
        self.assertIn("food autonomy", app)
        self.assertIn("nodeFile", index)
        self.assertIn("topologyFile", index)
        self.assertIn("populationSlider", index)
        self.assertIn("nodeScalingSummary", index)
        self.assertIn("searchFile", index)
        self.assertIn("calibrationFile", index)
        self.assertIn("weightFile", index)
        self.assertIn("../examples/generated/micro_commons_runtime_bundle.json", app)
        self.assertIn("../examples/generated/micro_commons_foundation_gate.json", app)
        self.assertIn("../examples/generated/micro_commons_search_optimizer_report.json", app)
        self.assertIn("../examples/generated/micro_commons_objective_calibration.json", app)
        self.assertIn("../examples/generated/micro_commons_weight_governance.json", app)
        self.assertIn("../examples/generated/micro_commons_cycle_iteration.json", app)
        self.assertIn("../examples/generated/micro_commons_food_autonomy_report.json", app)
        self.assertIn("../examples/generated/micro_commons_node_scaling.json", app)
        self.assertIn("../examples/generated/micro_commons_topology_recommendation.json", app)
        self.assertIn("../examples/generated/micro_commons_viewer_session_report.json", app)
        self.assertIn("/api/viewer-session-report", app)
        self.assertIn("renderFoundation", app)
        self.assertIn("loadDefaultFoundationGate", app)
        self.assertIn("loadDefaultOptimizationReports", app)
        self.assertIn("renderOptimization", app)
        self.assertIn("optimizationComparison", app)
        self.assertIn("governanceSummary", app)
        self.assertIn("runYearCycle", app)
        self.assertIn("completeCycle", app)
        self.assertIn("pauseCycle", app)
        self.assertIn("resumeCycle", app)
        self.assertIn("stopCycleTimer", app)
        self.assertIn("reviewCycleChange", app)
        self.assertIn("submitCycleChange", app)
        self.assertIn("runNextCycle", app)
        self.assertIn("renderCycle", app)
        self.assertIn("recordCompletedYear", app)
        self.assertIn("persistViewerRunEvent", app)
        self.assertIn("applyViewerRunPipelineResponse", app)
        self.assertIn("foodAutonomySummary", app)
        self.assertIn("ran the simulator and regenerated food labor, food autonomy, complexity, node-scaling, topology, cycle, and cohesion", app)
        self.assertIn("viewerRunLogSummary", app)
        self.assertIn("ViewerRunReport", app)
        self.assertIn("renderNodeScaling", app)
        self.assertIn("renderTopologyLayout", app)
        self.assertIn("topologyRecommendationMarkup", app)
        self.assertIn("liveTopologyRecommendation", app)
        self.assertIn("defaultPopulationFromTargets", app)
        self.assertIn("populationTouched", app)
        self.assertIn("syncPopulation: false", app)
        self.assertIn("Loaded recommendation file is for", app)
        self.assertIn("topologyCell", app)
        self.assertIn("capabilityLayerRows", app)
        self.assertIn("scaledNodeRow", app)
        self.assertIn("node_policy_catalog", app)
        self.assertIn("loadDefaultCycleIteration", app)
        self.assertIn("loadDefaultNodeScaling", app)
        self.assertIn("loadDefaultTopologyRecommendation", app)
        self.assertIn("setCycleReport", app)
        self.assertIn("cycleAuthoritySummary", app)
        self.assertIn("cycleAppliedScenarioRows", app)
        self.assertIn("cycleAcceptanceSummary", app)
        self.assertIn("operatorSubmitAllowed", app)
        self.assertIn("operator_acceptance", app)
        self.assertIn("next_search_optimizer_report", app)
        self.assertIn("20000", app)
        self.assertIn("renderFoundationLoadError", app)
        self.assertIn("noStorePath", app)
        self.assertIn("foundationStatusClass", app)
        self.assertIn("optimizationStatusClass", app)
        self.assertIn("cycleStatusClass", app)
        self.assertIn("layout_graph", app)
        self.assertIn("runtime_failures", app)
        self.assertIn("selectedScenarioFailures", app)
        self.assertIn("selectedScenarioFailuresForDay", app)
        self.assertIn("scenarioFailureActiveOnDay", app)
        self.assertIn("baseline normal year", app)
        self.assertIn("scenario replay", app)
        self.assertIn("renderFailureReasons", app)
        self.assertIn("renderRuntimeKpis", app)
        self.assertIn("renderSnapshot", app)
        self.assertIn("renderStorage", app)
        self.assertIn("renderPursuit", app)
        self.assertIn("modeled_involuntary_labor_minutes_per_resident_per_day", app)
        self.assertIn("modeled_personal_pursuit_hours_per_resident_per_day", app)
        self.assertIn("Mandatory upkeep only", app)
        self.assertIn("storage_recovery_tasks", app)
        self.assertIn("review_context", app)
        self.assertIn("scenario_events", app)
        self.assertIn(".map-stage", styles)
        self.assertIn(".zone-failure", styles)
        self.assertIn(".system-chip.has-warning", styles)
        self.assertIn(".topology-board", styles)
        self.assertIn(".topology-cell", styles)
        self.assertIn(".capability-layers", styles)
        self.assertIn(".foundation-check", styles)
        self.assertIn(".family-grid", styles)
        self.assertIn(".cycle-actions", styles)
        self.assertIn(".progress-track", styles)
        self.assertIn(".kpi-strip", styles)
        self.assertIn(".slider-row", styles)
        self.assertIn(".diagnostics", styles)
        self.assertIn(".primary-card", styles)

    def test_generated_bundle_has_viewer_ready_sections(self) -> None:
        bundle = load_data(ROOT / "examples" / "generated" / "micro_commons_runtime_bundle.json")

        self.assertEqual(bundle["kind"], "RuntimeBundle")
        self.assertIn("layout_graph", bundle["site"])
        self.assertTrue(bundle["systems"])
        self.assertTrue(bundle["timeline"]["daily_states"])
        self.assertIn("storage", bundle["timeline"]["daily_states"][0])
        self.assertIn("labor", bundle["timeline"])
        self.assertIn("modeled_involuntary_labor_minutes_per_resident_per_day", bundle["timeline"]["labor"])
        self.assertIn("modeled_personal_pursuit_hours_per_resident_per_day", bundle["timeline"]["labor"])
        self.assertIn("do_not_visualize_as_proof", bundle["viewer_hints"])

    def test_generated_foundation_gate_is_viewer_ready(self) -> None:
        gate = load_data(ROOT / "examples" / "generated" / "micro_commons_foundation_gate.json")

        self.assertEqual(gate["kind"], "FoundationGateReport")
        self.assertEqual(gate["status"], "ready_with_warnings")
        self.assertTrue(gate["checks"])
        self.assertTrue(any(check["status"] == "warn" for check in gate["checks"]))

    def test_generated_optimizer_artifacts_are_viewer_ready(self) -> None:
        search = load_data(ROOT / "examples" / "generated" / "micro_commons_search_optimizer_report.json")
        calibration = load_data(ROOT / "examples" / "generated" / "micro_commons_objective_calibration.json")
        governance = load_data(ROOT / "examples" / "generated" / "micro_commons_weight_governance.json")
        cycle = load_data(ROOT / "examples" / "generated" / "micro_commons_cycle_iteration.json")

        self.assertEqual(search["kind"], "SearchOptimizerReport")
        self.assertEqual(search["selected_candidate"], "search_001")
        self.assertTrue(search["top_candidates"])
        self.assertEqual(calibration["kind"], "ObjectiveCalibrationReport")
        self.assertEqual(calibration["status"], "provisional_calibrated")
        self.assertEqual(governance["kind"], "WeightGovernanceReport")
        self.assertEqual(governance["status"], "not_ratified")
        self.assertFalse(governance["promotion_allowed"])
        self.assertEqual(cycle["kind"], "CycleIterationReport")
        self.assertEqual(cycle["selected_candidate"], search["selected_candidate"])
        self.assertEqual(cycle["viewer_population_context"]["population"], cycle["applied_simulation"]["population"]["population"])
        self.assertIn("resilient_water_commons", cycle["viewer_population_context"]["active_node_patterns"])
        self.assertEqual(cycle["runtime_bundle"]["kind"], "RuntimeBundle")
        self.assertEqual(cycle["authority"]["mode"], "operator_directed")
        self.assertEqual(cycle["operator_acceptance"]["status"], "converged")
        self.assertTrue(cycle["operator_acceptance"]["simulation_submit_allowed"])
        self.assertEqual(cycle["next_search_optimizer_report"]["kind"], "SearchOptimizerReport")

    def test_generated_food_autonomy_report_is_viewer_ready(self) -> None:
        report = load_data(ROOT / "examples" / "generated" / "micro_commons_food_autonomy_report.json")
        viewer = load_data(ROOT / "examples" / "generated" / "micro_commons_viewer_session_report.json")

        self.assertEqual(report["kind"], "FoodAutonomyReport")
        self.assertEqual(report["population"], viewer["active_population"])
        self.assertIn(report["status"], {"pass", "warn"})
        self.assertTrue(report["seasonal_smoothing"]["resources"])
        self.assertTrue(validate_data(report, "food-autonomy").ok)

    def test_generated_artifact_cohesion_report_is_viewer_ready(self) -> None:
        report = load_data(ROOT / "examples" / "generated" / "micro_commons_artifact_cohesion.json")
        viewer = load_data(ROOT / "examples" / "generated" / "micro_commons_viewer_session_report.json")

        self.assertEqual(report["kind"], "ArtifactCohesionReport")
        self.assertIn(report["status"], {"coherent", "ready_with_warnings"})
        self.assertEqual(report["active_population"], viewer["active_population"])
        assert_no_failures_and_only_allowed_warnings(self, report)

    def test_generated_viewer_run_report_is_viewer_ready(self) -> None:
        report = load_data(ROOT / "examples" / "generated" / "micro_commons_viewer_session_report.json")

        self.assertEqual(report["kind"], "ViewerRunReport")
        self.assertEqual(report["status"], "runs_recorded")
        self.assertGreater(report["active_population"], 0)
        self.assertGreaterEqual(report["run_count"], 2)
        self.assertEqual(report["runs"][-1]["population"], report["active_population"])

    def test_generated_node_scaling_report_is_viewer_ready(self) -> None:
        report = load_data(ROOT / "examples" / "generated" / "micro_commons_node_scaling.json")

        self.assertEqual(report["kind"], "InfrastructureNodeReport")
        self.assertTrue(report["node_policy_catalog"])
        self.assertIn("flourishing_frame", report["orchestration_model"])
        food = next(policy for policy in report["node_policy_catalog"] if policy["slot"] == "food_production")
        self.assertEqual(food["maximum_population_per_node"], 80)
        self.assertIn("hybrid_food_commons", food["accepted_patterns"])

    def test_generated_topology_recommendation_is_viewer_ready(self) -> None:
        report = load_data(ROOT / "examples" / "generated" / "micro_commons_topology_recommendation.json")
        viewer = load_data(ROOT / "examples" / "generated" / "micro_commons_viewer_session_report.json")

        self.assertEqual(report["kind"], "TopologyRecommendationReport")
        self.assertEqual(report["population"], viewer["active_population"])
        self.assertEqual(report["selected_action"]["id"], "replicate_village_node_pools")
        self.assertTrue(report["candidate_actions"])

    def test_generated_food_labor_report_matches_viewer_population(self) -> None:
        report = load_data(ROOT / "examples" / "generated" / "micro_commons_food_labor_report.json")
        viewer = load_data(ROOT / "examples" / "generated" / "micro_commons_viewer_session_report.json")

        self.assertEqual(report["kind"], "FoodLaborReport")
        self.assertIn(viewer["active_population"], {row["target_population"] for row in report["scaling_results"]})


if __name__ == "__main__":
    unittest.main()
