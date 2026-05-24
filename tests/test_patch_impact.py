from __future__ import annotations

import copy
import tempfile
import unittest
from pathlib import Path

from ciac.io import load_data, write_json
from ciac.patch_impact import analyze_materialized_patch, apply_pattern_to_compiled_plan
from ciac.simulation import simulate


ROOT = Path(__file__).resolve().parents[1]
PLAN = ROOT / "examples" / "generated" / "micro_commons_plan.json"
PATTERN = ROOT / "patterns" / "care_health" / "care_health_resident_controlled_medication_continuity_kit_v1.yaml"
WATER_MATERIALIZATION = ROOT / "examples" / "discovery" / "patch_water_public_health_fallback_supply_protocol_v0.materialization.json"
MOBILITY_MATERIALIZATION = ROOT / "examples" / "discovery" / "patch_mobility_access_accessible_route_gap_survey_map_v0.materialization.json"


class PatchImpactTests(unittest.TestCase):
    def test_apply_pattern_adds_capability_effects_to_simulation(self) -> None:
        plan = load_data(PLAN)
        pattern = load_data(PATTERN)
        baseline = _without_pattern(plan, pattern["id"])

        candidate = apply_pattern_to_compiled_plan(baseline, pattern)
        simulation = simulate(candidate, days=14)

        self.assertIn(pattern["id"], candidate["selected_patterns"])
        self.assertIn(pattern["id"], candidate["simulation_inputs"]["capability_effects_by_pattern"])
        self.assertTrue(simulation["capability_state"]["domains"]["care_health"]["medication_continuity_supported"])

    def test_water_public_health_impact_detects_modeled_improvements(self) -> None:
        materialization = load_data(WATER_MATERIALIZATION)
        plan = _without_pattern(load_data(PLAN), materialization["source_candidate_id"])
        plan = _without_pattern(plan, "water_public_health_sanitation_labor_protocal_v0")
        with tempfile.TemporaryDirectory(dir=ROOT / "examples" / "generated") as tmp:
            plan_path = Path(tmp) / "plan.json"
            write_json(plan_path, plan)

            report = analyze_materialized_patch(materialization, repo_root=ROOT, compiled_plan_path=plan_path, days=30)

        self.assertEqual(report["placement_target"]["object_id"], "node_water_reserve")
        self.assertEqual(report["acceptance"]["regressions"], [])
        self.assertTrue(report["acceptance"]["can_promote"])
        improvements = "\n".join(report["acceptance"]["improvements"])
        self.assertIn("water_public_health.reserve_sanitation_protocol_supported", improvements)
        self.assertIn("labor_time.water_recovery_labor_visibility_supported", improvements)

    def test_mobility_access_impact_detects_route_visibility_improvements(self) -> None:
        materialization = load_data(MOBILITY_MATERIALIZATION)
        plan = _without_pattern(load_data(PLAN), "mobility_access_accessible_route_gap_survey_map_v0")
        with tempfile.TemporaryDirectory(dir=ROOT / "examples" / "generated") as tmp:
            plan_path = Path(tmp) / "plan.json"
            write_json(plan_path, plan)

            report = analyze_materialized_patch(materialization, repo_root=ROOT, compiled_plan_path=plan_path, days=30)

        self.assertEqual(report["placement_target"]["object_id"], "zone_mobility_loop")
        self.assertEqual(report["acceptance"]["regressions"], [])
        self.assertTrue(report["acceptance"]["can_promote"])
        improvements = "\n".join(report["acceptance"]["improvements"])
        self.assertIn("mobility_access.accessible_route_coverage", improvements)
        self.assertIn("mobility_access.route_gap_survey_supported", improvements)
        self.assertNotIn("care_continuity_protocol_supported", improvements)


def _without_pattern(plan: dict, pattern_id: str) -> dict:
    candidate = copy.deepcopy(plan)
    candidate["selected_patterns"] = [item for item in candidate.get("selected_patterns", []) if item != pattern_id]
    candidate["dependency_order"] = [item for item in candidate.get("dependency_order", []) if item != pattern_id]
    inputs = candidate.setdefault("simulation_inputs", {})
    for key in [
        "resource_effects_by_pattern",
        "critical_resources_by_pattern",
        "storage_by_pattern",
        "capability_effects_by_pattern",
    ]:
        inputs.setdefault(key, {}).pop(pattern_id, None)
    return candidate


if __name__ == "__main__":
    unittest.main()
