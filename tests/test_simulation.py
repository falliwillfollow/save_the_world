from __future__ import annotations

import copy
import unittest
from pathlib import Path

from ciac.compiler import CompileError, compile_plan, load_patterns
from ciac.io import load_data
from ciac.simulation import simulate
from ciac.validation import validate_data


ROOT = Path(__file__).resolve().parents[1]


class SimulationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.patterns = load_patterns(ROOT / "patterns")
        self.site = load_data(ROOT / "examples" / "site_profiles" / "micro_commons_5_households.yaml")
        self.seasonal_profile = load_data(ROOT / "seasonal_profiles" / "humid_temperate_provisional.yaml")
        self.household_profile = load_data(ROOT / "household_profiles" / "micro_commons_households_v0.yaml")

    def test_normal_year_simulation_completes_and_validates(self) -> None:
        plan = compile_plan(self.site, self.patterns)
        run = simulate(plan, days=365)
        self.assertEqual(run["kind"], "SimulationRun")
        self.assertEqual(run["days"], 365)
        self.assertEqual(len(run["daily_states"]), 365)
        self.assertIn(run["status"], {"pass", "warn", "fail"})
        self.assertTrue(validate_data(run, "simulation").ok)

    def test_missing_water_plan_produces_water_bottleneck(self) -> None:
        site = copy.deepcopy(self.site)
        site["selected_patterns"] = ["starter_dwelling", "solar_shed"]
        with self.assertRaises(CompileError) as raised:
            compile_plan(site, self.patterns)
        run = simulate(raised.exception.plan, days=365)
        self.assertEqual(run["resource_balance"]["water_liters"]["status"], "fail")
        self.assertTrue(any("water_liters" in bottleneck for bottleneck in run["bottlenecks"]))

    def test_excessive_maintenance_burden_fails_labor(self) -> None:
        plan = compile_plan(self.site, self.patterns)
        overloaded = copy.deepcopy(plan)
        overloaded["maintenance_calendar"][0]["estimated_hours"] = 10000
        run = simulate(overloaded, days=365)
        self.assertEqual(run["labor"]["status"], "fail")
        self.assertGreater(run["maintenance"]["overdue_task_count"], 0)
        self.assertIn("Reduce recurring labor", " ".join(run["gate_recommendations"]))

    def test_maintenance_intervals_generate_expected_task_counts(self) -> None:
        plan = compile_plan(self.site, self.patterns)
        run = simulate(plan, days=365)
        task_runs = {task["task_id"]: task["runs"] for task in run["maintenance"]["scheduled_tasks"]}
        self.assertEqual(task_runs["hygiene_round"], 365)
        self.assertEqual(task_runs["energy_check"], 53)
        self.assertEqual(task_runs["tank_screen_check"], 13)
        self.assertEqual(task_runs["envelope_check"], 5)

    def test_daily_state_tracks_shared_resource_ledger(self) -> None:
        plan = compile_plan(self.site, self.patterns)
        run = simulate(plan, days=30)
        first_day = run["daily_states"][0]
        self.assertEqual(first_day["day"], 1)
        self.assertEqual(first_day["season"], "winter")
        self.assertEqual(
            sorted(first_day["resources"].keys()),
            [
                "energy_kwh",
                "food_servings",
                "labor_hours",
                "procurement_units",
                "sanitation_capacity",
                "water_liters",
            ],
        )
        self.assertEqual(run["resource_ledger"]["water_liters"]["ending_balance"], 60000)
        self.assertEqual(run["resource_balance"]["water_liters"]["ending_balance"], 60000)
        self.assertEqual(len(run["resource_ledger"]["water_liters"]["entries"]), 30)
        self.assertEqual(first_day["resources"]["water_liters"]["curtailment"], 215)
        self.assertEqual(run["storage"]["resources"]["water_liters"]["total_curtailed"], 6450)

    def test_daily_maintenance_events_are_scheduled_on_calendar_days(self) -> None:
        plan = compile_plan(self.site, self.patterns)
        run = simulate(plan, days=8)
        day_one_tasks = {task["task_id"] for task in run["daily_states"][0]["maintenance_events"]}
        day_eight_tasks = {task["task_id"] for task in run["daily_states"][7]["maintenance_events"]}
        self.assertIn("energy_check", day_one_tasks)
        self.assertIn("energy_check", day_eight_tasks)
        self.assertIn("maintenance_scheduled", " ".join(event["event"] for event in run["timeline"]))

    def test_deferred_maintenance_creates_backlog_and_degradation(self) -> None:
        plan = compile_plan(self.site, self.patterns)
        overloaded = copy.deepcopy(plan)
        for task in overloaded["maintenance_calendar"]:
            if task["task_id"] == "energy_check":
                task["estimated_hours"] = 100
        run = simulate(overloaded, days=2)

        self.assertEqual(run["daily_states"][0]["maintenance_state"]["deferred_count"], 1)
        self.assertEqual(run["daily_states"][1]["system_degradation"]["patterns"]["solar_shed"], 0.03)
        self.assertEqual(run["daily_states"][1]["resources"]["energy_kwh"]["production"], 33.95)
        self.assertIn("maintenance_deferred", " ".join(event["event"] for event in run["timeline"]))
        self.assertIn("Reduce maintenance load", " ".join(run["gate_recommendations"]))

    def test_seasonal_profile_changes_daily_resource_flows(self) -> None:
        plan = compile_plan(self.site, self.patterns, self.seasonal_profile)
        run = simulate(plan, days=160)
        day_one = run["daily_states"][0]
        summer_day = run["daily_states"][151]

        self.assertEqual(day_one["season"], "winter")
        self.assertEqual(summer_day["season"], "summer")
        self.assertEqual(day_one["resources"]["water_liters"]["raw_net"], -71.75)
        self.assertEqual(day_one["resources"]["water_liters"]["storage_release"], 71.75)
        self.assertEqual(summer_day["resources"]["water_liters"]["raw_net"], -283.25)
        self.assertEqual(summer_day["resources"]["water_liters"]["storage_release"], 283.25)
        self.assertEqual(day_one["labor"]["maintenance_labor_multiplier"], 1.1)
        self.assertEqual(summer_day["labor"]["maintenance_labor_multiplier"], 1.15)
        self.assertEqual(run["resource_balance"]["water_liters"]["status"], "pass")

    def test_simulation_output_shape_is_stable_for_unreal_consumers(self) -> None:
        plan = compile_plan(self.site, self.patterns)
        run = simulate(plan, days=365)
        self.assertEqual(
            list(run.keys()),
            [
                "kind",
                "id",
                "compiled_plan",
                "generated_by",
                "days",
                "provisional",
                "status",
                "population",
                "runtime_failures",
                "review_context",
                "scenario_context",
                "daily_states",
                "resource_ledger",
                "timeline",
                "resource_balance",
                "storage",
                "labor",
                "maintenance",
                "triggered_risks",
                "bottlenecks",
                "gate_recommendations",
                "confidence",
                "unknowns",
            ],
        )

    def test_household_profile_changes_labor_capacity_and_demands(self) -> None:
        plan = compile_plan(self.site, self.patterns, self.seasonal_profile, self.household_profile)
        run = simulate(plan, days=1)
        first_day = run["daily_states"][0]

        self.assertEqual(run["population"]["source"], "micro_commons_households_v0")
        self.assertEqual(run["population"]["available_commons_labor_hours_per_week"], 84)
        self.assertEqual(first_day["labor"]["available_commons_hours"], 12)
        self.assertEqual(first_day["resources"]["food_servings"]["consumption"], 36)
        self.assertEqual(first_day["resources"]["water_liters"]["consumption"], 1149.5)
        self.assertEqual(run["labor"]["care_hours_per_week"], 41)
        self.assertEqual(run["labor"]["modeled_available_commons_hours_per_resident_per_day"], 1)
        self.assertEqual(run["labor"]["labor_objective"], "minimize_involuntary_commons_labor_after_dignity_floors")
        self.assertGreater(run["labor"]["modeled_involuntary_labor_minutes_per_resident_per_day"], 0)
        self.assertIn("intentionally unstated", run["labor"]["involuntary_labor_basis"])
        self.assertGreater(run["labor"]["modeled_personal_pursuit_hours_per_resident_per_day"], 0)
        self.assertGreater(run["labor"]["modeled_required_commons_minutes_per_resident_per_day"], 0)
        self.assertIn("not total free time", run["labor"]["personal_pursuit_time_basis"])

    def test_scenario_failures_reduce_runtime_resource_output(self) -> None:
        plan = compile_plan(self.site, self.patterns)
        scenario = {
            "id": "battery_test",
            "triggered_risk_modes": ["battery_fault"],
        }
        run = simulate(plan, days=1, scenario=scenario)

        self.assertEqual(run["runtime_failures"][0]["mode"], "battery_fault")
        self.assertEqual(run["daily_states"][0]["active_failures"][0]["pattern_id"], "solar_shed")
        self.assertEqual(run["daily_states"][0]["resources"]["energy_kwh"]["production"], 12.25)
        self.assertEqual(run["daily_states"][0]["resources"]["energy_kwh"]["storage_release"], 16.75)
        self.assertIn("runtime_failure_active", " ".join(event["event"] for event in run["timeline"]))

    def test_scenario_replay_applies_resource_and_emergency_labor_events_daily(self) -> None:
        plan = compile_plan(self.site, self.patterns)
        scenario = load_data(ROOT / "scenarios" / "drought_reserve_v2.yaml")
        scenario["triggered_risk_modes"] = []

        baseline = simulate(plan, days=1)
        run = simulate(plan, days=3, scenario=scenario)
        first_day = run["daily_states"][0]

        self.assertEqual(run["scenario_context"]["id"], "drought_reserve_v2")
        self.assertEqual(first_day["resources"]["water_liters"]["production"], round(baseline["daily_states"][0]["resources"]["water_liters"]["production"] * 0.85, 3))
        self.assertEqual(first_day["resources"]["water_liters"]["consumption"], round(baseline["daily_states"][0]["resources"]["water_liters"]["consumption"] + 40, 3))
        self.assertEqual(first_day["labor"]["scenario_emergency_hours"], 18)
        self.assertTrue(any(event["event"] == "scenario_emergency_task:water_rationing_protocol" for event in run["timeline"]))
        self.assertTrue(validate_data(run, "simulation").ok)

    def test_scenario_runtime_failure_overrides_bound_acute_response_window(self) -> None:
        plan = compile_plan(self.site, self.patterns)
        scenario = load_data(ROOT / "scenarios" / "crop_failure.yaml")

        run = simulate(plan, days=120, scenario=scenario)
        failures = {failure["mode"]: failure for failure in run["runtime_failures"]}

        self.assertEqual(failures["crop_failure"]["duration_days"], 30)
        self.assertEqual(failures["crop_failure"]["response_hours_per_day"], 0.75)
        self.assertEqual(failures["foodborne_illness"]["duration_days"], 7)
        self.assertEqual(run["daily_states"][29]["active_failures"][0]["mode"], "crop_failure")
        self.assertFalse(run["daily_states"][30]["active_failures"])

    def test_scenario_review_override_blocks_runtime_recovery_even_with_accepted_status(self) -> None:
        plan = compile_plan(self.site, self.patterns)
        quality = plan["simulation_inputs"]["storage_by_pattern"]["emergency_water_reserve"][0]["quality"]
        quality["unsafe_after_days"] = 1
        quality["recovery_labor_hours"] = 6
        scenario = load_data(ROOT / "scenarios" / "water_contamination_response_v2.yaml")
        review_status = {
            "id": "accepted_review_status",
            "status": "in_progress",
            "review_status_by_domain": {
                "water_public_health": {
                    "status": "accepted",
                    "expiration_date": "",
                    "unresolved_issue_count": 0,
                }
            },
            "expired_or_rejected_evidence": [],
        }

        run = simulate(plan, days=4, scenario=scenario, review_status=review_status)
        task = run["storage"]["recovery"]["tasks"][0]

        self.assertEqual(run["review_context"]["status"], "impacted")
        self.assertIn("water_public_health", run["review_context"]["blocked_domains"])
        self.assertEqual(task["status"], "blocked_review")
        self.assertIn("Scenario override blocks recovery", task["review_state"]["reason"])

    def test_water_response_buffer_prevents_contamination_water_unmet_but_keeps_failed_review(self) -> None:
        plan = compile_plan(self.site, self.patterns)
        scenario = load_data(ROOT / "scenarios" / "water_contamination_response_v2.yaml")

        run = simulate(plan, days=14, scenario=scenario)
        first_day = run["daily_states"][0]

        self.assertEqual(first_day["resources"]["water_liters"]["unmet_demand"], 0)
        self.assertGreater(first_day["resources"]["water_liters"]["storage_release"], 1000)
        self.assertEqual(run["review_context"]["status"], "impacted")
        self.assertIn("water_public_health", run["review_context"]["blocked_domains"])

    def test_scenario_labor_support_adds_capacity_without_changing_population(self) -> None:
        plan = compile_plan(self.site, self.patterns)
        scenario = load_data(ROOT / "scenarios" / "resident_exit_labor_loss.yaml")

        run = simulate(plan, days=1, scenario=scenario)
        first_day = run["daily_states"][0]

        self.assertEqual(first_day["population"], 12)
        self.assertGreater(first_day["labor"]["available_commons_hours"], 20)
        self.assertTrue(any(event["type"] == "labor_support" for event in first_day["scenario_events"]))

    def test_storage_reserves_draw_down_before_unmet_demand(self) -> None:
        plan = compile_plan(self.site, self.patterns, self.seasonal_profile, self.household_profile)
        run = simulate(plan, days=365)

        self.assertEqual(run["storage"]["status"], "pass")
        self.assertGreater(run["storage"]["resources"]["water_liters"]["minimum_total"], 8000)
        self.assertGreater(run["storage"]["resources"]["food_servings"]["total_released"], 0)
        self.assertEqual(run["resource_balance"]["food_servings"]["status"], "pass")

    def test_deferred_storage_checks_create_quality_warning(self) -> None:
        plan = compile_plan(self.site, self.patterns)
        overloaded = copy.deepcopy(plan)
        for task in overloaded["maintenance_calendar"]:
            if task["task_id"] == "potable_reserve_rotation":
                task["estimated_hours"] = 100

        run = simulate(overloaded, days=9)

        water_storage = run["daily_states"][-1]["storage_state"]["resources"]["water_liters"]
        self.assertEqual(water_storage["quality_status"], "warn")
        self.assertEqual(water_storage["stores"][0]["quality"]["days_since_check"], 9)
        self.assertIn("storage_quality_or_reserve_warning", " ".join(event["event"] for event in run["timeline"]))

    def test_failed_storage_quality_creates_recovery_work(self) -> None:
        plan = compile_plan(self.site, self.patterns)
        overloaded = copy.deepcopy(plan)
        for task in overloaded["maintenance_calendar"]:
            if task["task_id"] == "potable_reserve_rotation":
                task["estimated_hours"] = 100

        run = simulate(overloaded, days=22)

        recovery_tasks = run["daily_states"][-1]["storage_state"]["recovery_tasks"]
        self.assertEqual(run["daily_states"][-1]["storage_state"]["resources"]["water_liters"]["quality_status"], "fail")
        self.assertEqual(recovery_tasks[0]["role"], "water_steward")
        self.assertEqual(recovery_tasks[0]["estimated_hours"], 6)
        self.assertEqual(recovery_tasks[0]["status"], "blocked_review")
        self.assertEqual(recovery_tasks[0]["remaining_hours"], 0)
        self.assertEqual(recovery_tasks[0]["review_dependency"], "water_public_health")
        self.assertGreater(run["labor"]["storage_recovery_hours"], 0)
        self.assertEqual(run["storage"]["recovery"]["blocked_review_count"], 1)
        self.assertIn("storage_recovery_required", " ".join(event["event"] for event in run["timeline"]))

    def test_storage_recovery_progresses_over_multiple_days(self) -> None:
        plan = compile_plan(self.site, self.patterns)
        quality = plan["simulation_inputs"]["storage_by_pattern"]["emergency_water_reserve"][0]["quality"]
        quality["unsafe_after_days"] = 1
        quality["recovery_labor_hours"] = 60

        run = simulate(plan, days=5)
        day_three_task = run["daily_states"][2]["storage_state"]["recovery_tasks"][0]
        final_task = run["storage"]["recovery"]["tasks"][0]

        self.assertEqual(day_three_task["status"], "in_progress")
        self.assertEqual(day_three_task["worked_hours_today"], 22)
        self.assertEqual(day_three_task["remaining_hours"], 38)
        self.assertEqual(final_task["status"], "blocked_review")
        self.assertEqual(final_task["worked_hours_total"], 60)
        self.assertEqual(run["storage"]["recovery"]["total_remaining_hours"], 0)

    def test_accepted_review_status_resolves_storage_recovery(self) -> None:
        plan = compile_plan(self.site, self.patterns)
        quality = plan["simulation_inputs"]["storage_by_pattern"]["emergency_water_reserve"][0]["quality"]
        quality["unsafe_after_days"] = 1
        quality["recovery_labor_hours"] = 6
        review_status = {
            "id": "accepted_review_status",
            "status": "in_progress",
            "review_status_by_domain": {
                "water_public_health": {
                    "status": "accepted",
                    "expiration_date": "",
                    "unresolved_issue_count": 0,
                }
            },
            "expired_or_rejected_evidence": [],
        }

        run = simulate(plan, days=4, review_status=review_status)
        task = run["storage"]["recovery"]["tasks"][0]

        self.assertEqual(run["review_context"]["accepted_domains"], ["water_public_health"])
        self.assertEqual(task["status"], "resolved")
        self.assertTrue(task["review_state"]["accepted"])
        self.assertEqual(run["storage"]["recovery"]["resolved_count"], 1)
        self.assertEqual(run["daily_states"][-1]["storage_state"]["resources"]["water_liters"]["quality_status"], "pass")

    def test_unresolved_review_status_keeps_storage_recovery_blocked(self) -> None:
        plan = compile_plan(self.site, self.patterns)
        quality = plan["simulation_inputs"]["storage_by_pattern"]["emergency_water_reserve"][0]["quality"]
        quality["unsafe_after_days"] = 1
        quality["recovery_labor_hours"] = 6
        review_status = {
            "id": "unresolved_review_status",
            "status": "in_progress",
            "review_status_by_domain": {
                "water_public_health": {
                    "status": "accepted",
                    "expiration_date": "",
                    "unresolved_issue_count": 1,
                }
            },
            "expired_or_rejected_evidence": [],
        }

        run = simulate(plan, days=4, review_status=review_status)
        task = run["storage"]["recovery"]["tasks"][0]

        self.assertEqual(task["status"], "blocked_review")
        self.assertFalse(task["review_state"]["accepted"])
        self.assertIn("unresolved issue", task["review_state"]["reason"])


if __name__ == "__main__":
    unittest.main()
