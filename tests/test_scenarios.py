from __future__ import annotations

import unittest
from pathlib import Path

from ciac.compiler import compile_plan, load_patterns
from ciac.io import load_data
from ciac.scenarios import run_scenario
from ciac.validation import validate_data


ROOT = Path(__file__).resolve().parents[1]


class ScenarioTests(unittest.TestCase):
    def setUp(self) -> None:
        self.patterns = load_patterns(ROOT / "patterns")
        self.site = load_data(ROOT / "examples" / "site_profiles" / "micro_commons_5_households.yaml")
        self.plan = compile_plan(self.site, self.patterns)

    def test_drought_scenario_validates_and_preserves_water_gate_after_reserve(self) -> None:
        scenario = load_data(ROOT / "scenarios" / "drought.yaml")
        run = run_scenario(self.plan, scenario)
        self.assertEqual(run["kind"], "ScenarioRun")
        self.assertEqual(run["scenario"], "drought")
        self.assertTrue(validate_data(run, "scenario-run").ok)
        self.assertEqual(run["resource_balance"]["water_liters"]["status"], "pass")
        self.assertNotIn("water_gate", run["survival_critical_gate_failures"])
        self.assertEqual(run["status"], "warn")

    def test_water_contamination_triggers_expected_risk_modes(self) -> None:
        scenario = load_data(ROOT / "scenarios" / "water_contamination.yaml")
        run = run_scenario(self.plan, scenario)
        modes = {risk["mode"] for risk in run["triggered_risks"]}
        self.assertIn("contaminated_source", modes)
        self.assertIn("pathogen_exposure", modes)
        runtime_modes = {failure["mode"] for failure in run["runtime_failures"]}
        self.assertIn("contaminated_source", runtime_modes)
        self.assertIn("stored_water_contamination", runtime_modes)
        self.assertTrue(run["failure_timeline"])

    def test_scenario_review_context_overrides_are_reported(self) -> None:
        scenario = load_data(ROOT / "scenarios" / "water_contamination_response_v2.yaml")
        run = run_scenario(self.plan, scenario)

        self.assertEqual(run["review_context"]["status"], "impacted")
        self.assertIn("water_public_health", run["review_context"]["blocked_domains"])
        self.assertTrue(any(event["event"] == "review_context:water_public_health" for event in run["failure_timeline"]))
        self.assertIn("review fallback", " ".join(run["recommended_redesigns"]))

    def test_energy_outage_runtime_failure_adds_response_labor(self) -> None:
        scenario = load_data(ROOT / "scenarios" / "energy_outage_reserve_v2.yaml")
        run = run_scenario(self.plan, scenario)
        modes = {failure["mode"] for failure in run["runtime_failures"]}
        self.assertIn("battery_fault", modes)
        self.assertGreater(run["emergency_labor"]["runtime_failure_response_hours"], 0)
        self.assertTrue(any(event["event"] == "runtime_failure:battery_fault" for event in run["failure_timeline"]))

    def test_resident_exit_models_labor_capacity_loss(self) -> None:
        scenario = load_data(ROOT / "scenarios" / "resident_exit_labor_loss.yaml")
        run = run_scenario(self.plan, scenario)
        self.assertEqual(run["emergency_labor"]["labor_capacity_multiplier"], 0.8)
        self.assertGreater(run["emergency_labor"]["hours_per_resident_per_week"], 0)

    def test_resident_exit_uses_labor_support_and_bounded_tool_response(self) -> None:
        scenario = load_data(ROOT / "scenarios" / "resident_exit_labor_loss.yaml")
        run = run_scenario(self.plan, scenario)
        failures = {failure["mode"]: failure for failure in run["runtime_failures"]}

        self.assertEqual(failures["tool_capture"]["duration_days"], 21)
        self.assertEqual(failures["tool_capture"]["response_hours_per_day"], 0.5)
        self.assertTrue(scenario["labor_support"])
        self.assertTrue(validate_data(run, "scenario-run").ok)

    def test_crop_failure_scenario_uses_bounded_runtime_failure_overrides(self) -> None:
        scenario = load_data(ROOT / "scenarios" / "crop_failure.yaml")
        run = run_scenario(self.plan, scenario)
        durations = {failure["mode"]: failure["duration_days"] for failure in run["runtime_failures"]}

        self.assertEqual(durations["crop_failure"], 30)
        self.assertEqual(durations["foodborne_illness"], 7)
        self.assertTrue(validate_data(run, "scenario-run").ok)

    def test_water_response_scenario_bounds_acute_labor_without_removing_review_block(self) -> None:
        scenario = load_data(ROOT / "scenarios" / "water_contamination_response_v2.yaml")
        run = run_scenario(self.plan, scenario)
        failures = {failure["mode"]: failure for failure in run["runtime_failures"]}

        self.assertEqual(failures["contaminated_source"]["duration_days"], 14)
        self.assertEqual(failures["pathogen_exposure"]["duration_days"], 5)
        self.assertEqual(failures["stored_water_contamination"]["duration_days"], 3)
        self.assertLess(run["emergency_labor"]["runtime_failure_response_hours"], 45)
        self.assertIn("water_public_health", run["review_context"]["blocked_domains"])

    def test_scenario_output_shape_is_stable_for_downstream_consumers(self) -> None:
        scenario = load_data(ROOT / "scenarios" / "energy_outage.yaml")
        run = run_scenario(self.plan, scenario)
        self.assertEqual(
            list(run.keys()),
            [
                "kind",
                "id",
                "compiled_plan",
                "scenario",
                "generated_by",
                "days",
                "provisional",
                "status",
                "baseline_status",
                "runtime_failures",
                "failure_timeline",
                "affected_resources",
                "resource_balance",
                "emergency_labor",
                "review_context",
                "triggered_risks",
                "bottlenecks",
                "survival_critical_gate_failures",
                "recommended_redesigns",
                "unknowns",
            ],
        )


if __name__ == "__main__":
    unittest.main()
