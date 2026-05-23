from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from ciac.cli import main
from ciac.compiler import compile_plan, load_patterns
from ciac.io import load_data
from ciac.runtime_export import build_runtime_bundle
from ciac.scenarios import run_scenario
from ciac.simulation import simulate
from ciac.validation import validate_data


ROOT = Path(__file__).resolve().parents[1]


class RuntimeExportTests(unittest.TestCase):
    def setUp(self) -> None:
        patterns = load_patterns(ROOT / "patterns")
        site = load_data(ROOT / "examples" / "site_profiles" / "micro_commons_5_households.yaml")
        seasonal = load_data(ROOT / "seasonal_profiles" / "humid_temperate_provisional.yaml")
        household = load_data(ROOT / "household_profiles" / "micro_commons_households_v0.yaml")
        spatial = load_data(ROOT / "spatial_profiles" / "micro_commons_spatial_v0.yaml")
        self.plan = compile_plan(site, patterns, seasonal, household, spatial)
        self.simulation = simulate(self.plan, days=14)
        self.scenario = run_scenario(self.plan, load_data(ROOT / "scenarios" / "water_contamination_response_v2.yaml"))

    def test_runtime_bundle_shape_is_stable(self) -> None:
        bundle = build_runtime_bundle(self.plan, self.simulation, [self.scenario])

        self.assertEqual(
            list(bundle.keys()),
            [
                "kind",
                "id",
                "generated_by",
                "provisional",
                "manifest",
                "site",
                "systems",
                "timeline",
                "capabilities",
                "scenarios",
                "viewer_hints",
                "unknowns",
            ],
        )
        self.assertEqual(bundle["kind"], "RuntimeBundle")
        self.assertEqual(bundle["capabilities"]["state"]["kind"], "CapabilityState")
        self.assertTrue(validate_data(bundle, "runtime-bundle").ok)

    def test_runtime_bundle_includes_layout_systems_and_spatial_warnings(self) -> None:
        bundle = build_runtime_bundle(self.plan, self.simulation, [self.scenario])
        systems = {system["pattern_id"]: system for system in bundle["systems"]}

        self.assertEqual(systems["well_house"]["zone_id"], "water_yard")
        self.assertIn("water_safety", systems["well_house"]["hazard_flags"])
        self.assertIn("survey", " ".join(bundle["site"]["unresolved_spatial_issues"]))

    def test_runtime_bundle_compresses_daily_timeline_for_viewers(self) -> None:
        bundle = build_runtime_bundle(self.plan, self.simulation, [self.scenario])
        first_day = bundle["timeline"]["daily_states"][0]

        self.assertEqual(first_day["day"], 1)
        self.assertIn("water_liters", first_day["resources"])
        self.assertIn("production", first_day["resources"]["water_liters"])
        self.assertIn("consumption", first_day["resources"]["water_liters"])
        self.assertIn("storage_release", first_day["resources"]["water_liters"])
        self.assertIn("curtailment", first_day["resources"]["water_liters"])
        self.assertIn("opening_total", first_day["storage"]["water_liters"])
        self.assertIn("percent_full", first_day["storage"]["water_liters"])
        self.assertIn("deferred_count", first_day["maintenance"])
        self.assertIn("labor", bundle["timeline"])
        self.assertIn("modeled_involuntary_labor_minutes_per_resident_per_day", bundle["timeline"]["labor"])
        self.assertIn("modeled_personal_pursuit_hours_per_resident_per_day", bundle["timeline"]["labor"])
        self.assertIn("hours_per_resident", first_day["labor"])
        self.assertIn("scenario_events", first_day)
        self.assertNotIn("maintenance_events", first_day)

    def test_runtime_bundle_includes_scenario_failures(self) -> None:
        bundle = build_runtime_bundle(self.plan, self.simulation, [self.scenario])
        scenario = bundle["scenarios"][0]
        modes = {failure["mode"] for failure in scenario["runtime_failures"]}

        self.assertEqual(scenario["scenario"], "water_contamination_response_v2")
        self.assertIn("contaminated_source", modes)
        self.assertNotIn("water_gate", scenario["survival_critical_gate_failures"])

    def test_cli_export_runtime_writes_bundle(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "runtime" / "bundle.json"
            code = main(
                [
                    "export-runtime",
                    str(ROOT / "examples" / "generated" / "micro_commons_plan.json"),
                    str(ROOT / "examples" / "generated" / "micro_commons_simulation.json"),
                    "--scenario",
                    str(ROOT / "examples" / "generated" / "water_contamination_response_v2_scenario.json"),
                    "--output",
                    str(output),
                ]
            )

            self.assertEqual(code, 0)
            bundle = load_data(output)
            self.assertEqual(bundle["kind"], "RuntimeBundle")


if __name__ == "__main__":
    unittest.main()
