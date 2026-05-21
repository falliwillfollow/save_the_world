import json
import tempfile
import unittest
from pathlib import Path

from ciac.cli import main
from ciac.io import load_data
from ciac.module_implementation import implement_technology_module
from ciac.research import evaluate_scalability_gate, generate_research_needs
from ciac.technology import evaluate_module_compatibility, pressure_test_technology_module
from ciac.validation import validate_data


ROOT = Path(__file__).resolve().parents[1]
GENERATED = ROOT / "examples" / "generated"


class TechnologyModuleTests(unittest.TestCase):
    def setUp(self) -> None:
        self.plan = load_data(GENERATED / "micro_commons_plan.json")
        self.simulation = load_data(GENERATED / "micro_commons_simulation.json")
        self.module = load_data(ROOT / "tech_modules" / "agrivoltaic_shade_pasture_water_efficiency.yaml")
        self.registry = load_data(ROOT / "module_registries" / "micro_commons_default_v0.yaml")

    def test_technology_module_validates(self) -> None:
        self.assertTrue(validate_data(self.module, "technology-module").ok)
        self.assertTrue(validate_data(self.registry, "module-registry").ok)

    def test_pressure_test_preserves_dignity_floors_and_flags_modeling_gap(self) -> None:
        report = pressure_test_technology_module(self.plan, self.module)

        self.assertEqual(report["kind"], "TechnologyPressureTestReport")
        self.assertEqual(report["status"], "needs_modeling")
        self.assertTrue(report["dignity_floor_effect"]["safe_for_operator_iteration"])
        self.assertFalse(report["dignity_floor_effect"]["regressions"])
        self.assertTrue(any("survival-resource effect" in gap for gap in report["integration_gaps"]))
        self.assertTrue(validate_data(report, "technology-pressure-test").ok)

    def test_cli_technology_pressure_test_writes_report(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "technology_pressure.json"
            code = main(
                [
                    "technology-pressure-test",
                    str(GENERATED / "micro_commons_plan.json"),
                    str(ROOT / "tech_modules" / "agrivoltaic_shade_pasture_water_efficiency.yaml"),
                    "--output",
                    str(output),
                ]
            )

            self.assertEqual(code, 0)
            report = load_data(output)
            self.assertEqual(report["kind"], "TechnologyPressureTestReport")

    def test_module_compatibility_tracks_default_slots_and_research_backlog(self) -> None:
        report = evaluate_module_compatibility(self.plan, self.registry, [self.module])

        self.assertEqual(report["kind"], "ModuleCompatibilityReport")
        self.assertEqual(report["status"], "needs_research")
        slots = {slot["slot"]: slot for slot in report["slot_results"]}
        self.assertTrue(slots["food_production"]["default_posture_ready"])
        self.assertEqual(len(report["adapter_required"]), 1)
        self.assertEqual(report["adapter_required"][0]["module"], self.module["id"])
        self.assertTrue(report["research_backlog"])
        self.assertTrue(validate_data(report, "module-compatibility").ok)

    def test_cli_module_compatibility_writes_report(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "module_compatibility.json"
            code = main(
                [
                    "module-compatibility",
                    str(GENERATED / "micro_commons_plan.json"),
                    str(ROOT / "module_registries" / "micro_commons_default_v0.yaml"),
                    "--technology-module",
                    str(ROOT / "tech_modules" / "agrivoltaic_shade_pasture_water_efficiency.yaml"),
                    "--output",
                    str(output),
                ]
            )

            self.assertEqual(code, 0)
            report = load_data(output)
            self.assertEqual(report["kind"], "ModuleCompatibilityReport")

    def test_research_needs_emit_food_production_gap(self) -> None:
        report = generate_research_needs(self.plan, self.simulation, self.registry)

        self.assertEqual(report["kind"], "ResearchNeedReport")
        self.assertEqual(report["status"], "blocked_by_model_gap")
        self.assertEqual(report["needs"][0]["id"], "food_local_production_gap_v0")
        self.assertEqual(report["needs"][0]["module_slot"], "food_production")
        self.assertGreater(report["needs"][0]["target"]["required_delta_per_day"], 20)
        self.assertIn("controlled environment agriculture", " ".join(report["needs"][0]["search_queries"]))
        self.assertTrue(validate_data(report, "research-needs").ok)

    def test_cli_research_needs_writes_report(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "research_needs.json"
            code = main(
                [
                    "research-needs",
                    str(GENERATED / "micro_commons_plan.json"),
                    str(GENERATED / "micro_commons_simulation.json"),
                    "--module-registry",
                    str(ROOT / "module_registries" / "micro_commons_default_v0.yaml"),
                    "--output",
                    str(output),
                ]
            )

            self.assertEqual(code, 0)
            report = load_data(output)
            self.assertEqual(report["kind"], "ResearchNeedReport")

    def test_scalability_gate_blocks_module_without_edible_labor_interfaces(self) -> None:
        report = evaluate_scalability_gate(self.plan, self.module, self.registry)

        self.assertEqual(report["kind"], "ScalabilityGateReport")
        self.assertEqual(report["status"], "fail")
        self.assertFalse(report["passes_scalability_gate"])
        gates = {gate["id"]: gate for gate in report["gate_results"]}
        self.assertEqual(gates["dignity_floor_protection"]["status"], "pass")
        self.assertEqual(gates["evidence_traceability"]["status"], "pass")
        self.assertEqual(gates["scalable_interface"]["status"], "fail")
        self.assertEqual(gates["labor_visibility"]["status"], "fail")
        self.assertTrue(validate_data(report, "scalability-gate").ok)

    def test_cli_scalability_gate_writes_report_and_returns_fail_status(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "scalability_gate.json"
            code = main(
                [
                    "scalability-gate",
                    str(GENERATED / "micro_commons_plan.json"),
                    str(ROOT / "tech_modules" / "agrivoltaic_shade_pasture_water_efficiency.yaml"),
                    "--module-registry",
                    str(ROOT / "module_registries" / "micro_commons_default_v0.yaml"),
                    "--output",
                    str(output),
                ]
            )

            self.assertEqual(code, 1)
            report = load_data(output)
            self.assertEqual(report["kind"], "ScalabilityGateReport")

    def test_module_implementation_blocks_unscalable_module(self) -> None:
        report = implement_technology_module(self.plan, self.module, self.registry, days=14)

        self.assertEqual(report["kind"], "ModuleImplementationReport")
        self.assertEqual(report["status"], "blocked_by_scalability_gate")
        self.assertIsNone(report["implemented_plan"])
        self.assertEqual(report["scalability_gate"]["status"], "fail")
        self.assertTrue(validate_data(report, "module-implementation").ok)

    def test_module_implementation_materializes_explicit_candidate(self) -> None:
        module = _implementation_ready_food_module()
        report = implement_technology_module(self.plan, module, self.registry, days=14)

        self.assertEqual(report["kind"], "ModuleImplementationReport")
        self.assertEqual(report["status"], "implemented")
        self.assertEqual(report["scalability_gate"]["status"], "pass")
        self.assertIn(f"module_{module['id']}", report["implemented_plan"]["selected_patterns"])
        self.assertEqual(report["implemented_plan"]["simulation_inputs"]["resource_effects_by_pattern"][f"module_{module['id']}"]["food_servings_per_day"], 30.0)
        food_delta = next(item for item in report["comparison_report"]["resource_deltas"] if item["resource"] == "food_servings")
        self.assertGreater(food_delta["net_per_day_delta"], 10)
        self.assertTrue(validate_data(report, "module-implementation").ok)

    def test_cli_implement_module_writes_report(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            module_path = Path(tmp) / "ready_food_module.json"
            output = Path(tmp) / "implementation.json"
            module_path.write_text(json.dumps(_implementation_ready_food_module()), encoding="utf-8")

            code = main(
                [
                    "implement-module",
                    str(GENERATED / "micro_commons_plan.json"),
                    str(module_path),
                    "--module-registry",
                    str(ROOT / "module_registries" / "micro_commons_default_v0.yaml"),
                    "--days",
                    "14",
                    "--output",
                    str(output),
                ]
            )

            self.assertEqual(code, 0)
            report = load_data(output)
            self.assertEqual(report["kind"], "ModuleImplementationReport")
            self.assertEqual(report["status"], "implemented")


def _implementation_ready_food_module() -> dict[str, object]:
    return {
        "kind": "TechnologyModule",
        "id": "explicit_low_labor_food_module_v0",
        "name": "Explicit Low-Labor Food Module",
        "domain": ["food", "controlled_environment_agriculture"],
        "status": "candidate",
        "provisional": True,
        "source_evidence": [
            {
                "id": "source_1",
                "citation": "Synthetic test evidence record",
                "url": "https://example.org/evidence",
                "context": "Unit-test fixture for a fully adapted CIaC module.",
                "provisional": True,
            }
        ],
        "performance_statistics": [
            {
                "id": "stat_1",
                "source_id": "source_1",
                "metric": "edible_servings_per_day",
                "value": 30,
                "unit": "servings_per_day",
                "evidence_status": "test_fixture",
                "provisional": True,
            }
        ],
        "applicability": {
            "target_slots": ["food_production"],
            "target_patterns": ["greenhouse"],
            "excludes": [],
            "provisional": True,
        },
        "modeled_impacts": {
            "dignity_floor_policy": "additive_only",
            "direct_resource_effects": {
                "food_servings_per_day": 30,
                "water_liters_per_day": 0,
                "energy_kwh_per_day": 0,
            },
            "candidate_modifiers": {
                "edible_servings_per_day": 30,
                "water_liters_per_serving": 0,
                "labor_hours_per_week": 0,
                "crop_failure_sensitivity": "bounded",
            },
            "provisional": True,
        },
        "integration_requirements": [],
        "unknowns": [],
    }


if __name__ == "__main__":
    unittest.main()
