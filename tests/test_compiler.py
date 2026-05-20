from __future__ import annotations

import copy
import unittest
from pathlib import Path

from ciac.compiler import CompileError, compile_plan, load_patterns
from ciac.io import load_data
from ciac.validation import validate_data


ROOT = Path(__file__).resolve().parents[1]


class CompilerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.patterns = load_patterns(ROOT / "patterns")
        self.site = load_data(ROOT / "examples" / "site_profiles" / "micro_commons_5_households.yaml")
        self.seasonal_profile = load_data(ROOT / "seasonal_profiles" / "humid_temperate_provisional.yaml")
        self.household_profile = load_data(ROOT / "household_profiles" / "micro_commons_households_v0.yaml")
        self.spatial_profile = load_data(ROOT / "spatial_profiles" / "micro_commons_spatial_v0.yaml")

    def test_happy_path_compiles_5_household_plan(self) -> None:
        plan = compile_plan(self.site, self.patterns)
        self.assertEqual(plan["kind"], "CompiledPlan")
        self.assertEqual(plan["source_site_profile"], "micro_commons_5_households")
        self.assertEqual(plan["missing_dependencies"], [])
        self.assertIn("well_house", plan["dependency_order"])
        self.assertLess(plan["dependency_order"].index("well_house"), plan["dependency_order"].index("shared_bathhouse"))
        self.assertTrue(validate_data(plan, "compiled").ok)

    def test_compile_refuses_missing_water_and_sanitation_dependencies(self) -> None:
        site = copy.deepcopy(self.site)
        site["selected_patterns"] = ["solar_shed", "starter_dwelling", "community_kitchen"]
        with self.assertRaises(CompileError) as raised:
            compile_plan(site, self.patterns)
        self.assertIsNotNone(raised.exception.plan)
        missing_ids = {dep["dependency_id"] for dep in raised.exception.plan["missing_dependencies"]}
        self.assertIn("shared_bathhouse", missing_ids)
        self.assertIn("well_house", missing_ids)

    def test_compiled_json_shape_is_stable_for_downstream_consumers(self) -> None:
        plan = compile_plan(self.site, self.patterns)
        self.assertEqual(
            list(plan.keys()),
            [
                "kind",
                "id",
                "source_site_profile",
                "generated_by",
                "provisional",
                "site_summary",
                "selected_patterns",
                "dependency_order",
                "missing_dependencies",
                "phases",
                "maintenance_calendar",
                "role_burden",
                "layout_graph",
                "risk_register",
                "simulation_inputs",
                "promotion_status",
            ],
        )

    def test_compiled_plan_exports_simulation_inputs(self) -> None:
        plan = compile_plan(self.site, self.patterns)
        simulation_inputs = plan["simulation_inputs"]
        self.assertTrue(simulation_inputs["provisional"])
        self.assertIn("well_house", simulation_inputs["resource_effects_by_pattern"])
        self.assertIn("water_liters_per_day", simulation_inputs["resource_effects_by_pattern"]["well_house"])
        self.assertIn("emergency_water_reserve", simulation_inputs["storage_by_pattern"])
        self.assertEqual(simulation_inputs["storage_by_pattern"]["emergency_water_reserve"][0]["resource"], "water_liters")

    def test_compile_can_embed_matching_seasonal_profile(self) -> None:
        plan = compile_plan(self.site, self.patterns, self.seasonal_profile)
        self.assertEqual(plan["site_summary"]["seasonal_profile_id"], "humid_temperate_provisional")
        self.assertEqual(plan["simulation_inputs"]["seasonal_profile"]["kind"], "SeasonalProfile")
        self.assertTrue(validate_data(plan, "compiled").ok)

    def test_compile_rejects_wrong_seasonal_profile_reference(self) -> None:
        site = copy.deepcopy(self.site)
        site["seasonal_profile_id"] = "different_profile"
        with self.assertRaises(CompileError):
            compile_plan(site, self.patterns, self.seasonal_profile)

    def test_compile_can_embed_matching_household_profile(self) -> None:
        plan = compile_plan(self.site, self.patterns, self.seasonal_profile, self.household_profile)
        self.assertEqual(plan["site_summary"]["household_profile_id"], "micro_commons_households_v0")
        self.assertEqual(plan["simulation_inputs"]["household_profile"]["kind"], "HouseholdProfile")
        self.assertTrue(validate_data(plan, "compiled").ok)

    def test_compile_rejects_household_population_mismatch(self) -> None:
        household_profile = copy.deepcopy(self.household_profile)
        household_profile["households"][0]["adults"] = 3
        with self.assertRaises(CompileError):
            compile_plan(self.site, self.patterns, self.seasonal_profile, household_profile)

    def test_compile_can_emit_layout_graph_from_spatial_profile(self) -> None:
        plan = compile_plan(self.site, self.patterns, self.seasonal_profile, self.household_profile, self.spatial_profile)
        layout = plan["layout_graph"]
        self.assertEqual(layout["source_spatial_profile"], "micro_commons_spatial_v0")
        self.assertEqual(len(layout["nodes"]), len(self.site["selected_patterns"]))
        self.assertTrue(any(edge["relationship"] == "adjacency" for edge in layout["edges"]))
        self.assertTrue(any(edge["relationship"] == "separation" for edge in layout["edges"]))
        self.assertIn("survey", " ".join(layout["unresolved_spatial_issues"]))
        self.assertTrue(validate_data(plan, "compiled").ok)

    def test_compile_rejects_spatial_profile_missing_selected_placement(self) -> None:
        spatial_profile = copy.deepcopy(self.spatial_profile)
        spatial_profile["placements"] = [
            placement for placement in spatial_profile["placements"] if placement["pattern_id"] != "greenhouse"
        ]
        with self.assertRaises(CompileError):
            compile_plan(self.site, self.patterns, self.seasonal_profile, self.household_profile, spatial_profile)


if __name__ == "__main__":
    unittest.main()
