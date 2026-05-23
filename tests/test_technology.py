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

    def test_module_registry_tracks_housing_slot(self) -> None:
        housing = next(slot for slot in self.registry["slots"] if slot["id"] == "housing")

        self.assertEqual(housing["domain"], "shelter")
        self.assertIn("privacy_score", housing["required_interfaces"])
        self.assertEqual(load_data(ROOT / "patterns" / "dignified_village_block.yaml")["id"], "dignified_village_block")

    def test_module_registry_tracks_hybrid_food_interfaces(self) -> None:
        food = next(slot for slot in self.registry["slots"] if slot["id"] == "food_production")

        self.assertIn("private_food_autonomy", food["required_interfaces"])
        self.assertIn("shelf_stable_buffer_days", food["required_interfaces"])
        self.assertIn("reserve_drawdown_reduction", food["required_interfaces"])
        self.assertIn("seasonal_menu_bridge", food["required_interfaces"])
        self.assertIn("preservation", food["accepted_module_domains"])
        self.assertEqual(load_data(ROOT / "patterns" / "hybrid_food_commons.yaml")["id"], "hybrid_food_commons")
        self.assertEqual(
            load_data(ROOT / "patterns" / "seasonal_food_smoothing_commons.yaml")["id"],
            "seasonal_food_smoothing_commons",
        )

    def test_module_registry_tracks_resilient_water_interfaces(self) -> None:
        water = next(slot for slot in self.registry["slots"] if slot["id"] == "potable_water_source")

        self.assertIn("emergency_buffer_days", water["required_interfaces"])
        self.assertIn("cross_connection_prevention", water["required_interfaces"])
        self.assertIn("leak_detection", water["required_interfaces"])
        self.assertIn("public_health", water["accepted_module_domains"])
        self.assertEqual(load_data(ROOT / "patterns" / "resilient_water_commons.yaml")["id"], "resilient_water_commons")

    def test_module_registry_tracks_hygienic_circular_sanitation_interfaces(self) -> None:
        sanitation = next(slot for slot in self.registry["slots"] if slot["id"] == "sanitation")

        self.assertIn("blackwater_solution_type", sanitation["required_interfaces"])
        self.assertIn("hazardous_waste_storage", sanitation["required_interfaces"])
        self.assertIn("cleaning_labor_hours_per_week", sanitation["required_interfaces"])
        self.assertIn("hazardous_waste", sanitation["accepted_module_domains"])
        self.assertEqual(load_data(ROOT / "patterns" / "hygienic_circular_commons.yaml")["id"], "hygienic_circular_commons")

    def test_module_registry_tracks_critical_load_energy_interfaces(self) -> None:
        energy = next(slot for slot in self.registry["slots"] if slot["id"] == "critical_energy")

        self.assertIn("critical_load_runtime_hours_no_sun", energy["required_interfaces"])
        self.assertIn("battery_fire_review", energy["required_interfaces"])
        self.assertIn("safe_room_powered", energy["required_interfaces"])
        self.assertIn("thermal_resilience", energy["accepted_module_domains"])
        self.assertEqual(load_data(ROOT / "patterns" / "critical_load_energy_commons.yaml")["id"], "critical_load_energy_commons")

    def test_module_registry_tracks_maintainable_commons_interfaces(self) -> None:
        maintenance = next(slot for slot in self.registry["slots"] if slot["id"] == "maintenance_repair")

        self.assertIn("asset_registry_system", maintenance["required_interfaces"])
        self.assertIn("professional_handoff_engine", maintenance["required_interfaces"])
        self.assertIn("emergency_repair_reserve", maintenance["required_interfaces"])
        self.assertIn("asset_management", maintenance["accepted_module_domains"])
        self.assertEqual(load_data(ROOT / "patterns" / "maintainable_commons_spine.yaml")["id"], "maintainable_commons_spine")

    def test_module_registry_tracks_commons_stewardship_interfaces(self) -> None:
        governance = next(slot for slot in self.registry["slots"] if slot["id"] == "governance_anticapture")

        self.assertIn("asset_lock_defined", governance["required_interfaces"])
        self.assertIn("member_vote_on_constitutional_matters", governance["required_interfaces"])
        self.assertIn("anti_capture_monitor", governance["required_interfaces"])
        self.assertIn("land_trust", governance["accepted_module_domains"])
        self.assertEqual(load_data(ROOT / "patterns" / "commons_stewardship_protocol.yaml")["id"], "commons_stewardship_protocol")

    def test_module_registry_tracks_life_burden_interfaces(self) -> None:
        labor = next(slot for slot in self.registry["slots"] if slot["id"] == "labor_time")

        self.assertIn("time_ledger", labor["required_interfaces"])
        self.assertIn("wage_dependency_reduction_percent", labor["required_interfaces"])
        self.assertIn("bad_week_simulator", labor["required_interfaces"])
        self.assertIn("time_use", labor["accepted_module_domains"])
        self.assertEqual(load_data(ROOT / "patterns" / "life_burden_ledger.yaml")["id"], "life_burden_ledger")

    def test_module_registry_tracks_legal_land_finance_interfaces(self) -> None:
        legal_finance = next(slot for slot in self.registry["slots"] if slot["id"] == "legal_land_finance")

        self.assertIn("land_control_type", legal_finance["required_interfaces"])
        self.assertIn("affordability_formula_defined", legal_finance["required_interfaces"])
        self.assertIn("replacement_reserve", legal_finance["required_interfaces"])
        self.assertIn("debt_risk_simulator", legal_finance["required_interfaces"])
        self.assertIn("anti_speculation", legal_finance["accepted_module_domains"])
        self.assertEqual(load_data(ROOT / "patterns" / "anti_speculative_civic_floor.yaml")["id"], "anti_speculative_civic_floor")

    def test_module_registry_tracks_materials_fabrication_interfaces(self) -> None:
        materials = next(slot for slot in self.registry["slots"] if slot["id"] == "materials_fabrication")

        self.assertIn("panelization_ratio_percent", materials["required_interfaces"])
        self.assertIn("BOM_generator", materials["required_interfaces"])
        self.assertIn("embodied_carbon_estimator", materials["required_interfaces"])
        self.assertIn("BIM_IFC_export", materials["required_interfaces"])
        self.assertIn("embodied_carbon", materials["accepted_module_domains"])
        self.assertEqual(
            load_data(ROOT / "patterns" / "standardized_low_burden_build_system.yaml")["id"],
            "standardized_low_burden_build_system",
        )

    def test_module_registry_tracks_mobility_access_interfaces(self) -> None:
        mobility = next(slot for slot in self.registry["slots"] if slot["id"] == "mobility_access")

        self.assertIn("accessible_route_coverage_percent", mobility["required_interfaces"])
        self.assertIn("emergency_access_dashboard", mobility["required_interfaces"])
        self.assertIn("monthly_transport_cost_per_resident", mobility["required_interfaces"])
        self.assertIn("grocery_pharmacy_clinic_access_report", mobility["required_interfaces"])
        self.assertIn("shared_vehicle", mobility["accepted_module_domains"])
        self.assertEqual(
            load_data(ROOT / "patterns" / "pedestrian_first_access_commons.yaml")["id"],
            "pedestrian_first_access_commons",
        )

    def test_module_registry_tracks_education_skill_interfaces(self) -> None:
        education = next(slot for slot in self.registry["slots"] if slot["id"] == "education_skill")

        self.assertIn("skill_graph", education["required_interfaces"])
        self.assertIn("training_gate_engine", education["required_interfaces"])
        self.assertIn("critical_roles_backup_trained_percent", education["required_interfaces"])
        self.assertIn("required_learning_hours_per_resident_per_month", education["required_interfaces"])
        self.assertIn("apprenticeship", education["accepted_module_domains"])
        self.assertEqual(load_data(ROOT / "patterns" / "civic_skill_lattice.yaml")["id"], "civic_skill_lattice")

    def test_module_registry_tracks_social_cultural_interfaces(self) -> None:
        social = next(slot for slot in self.registry["slots"] if slot["id"] == "social_cultural_commons")

        self.assertIn("opt_out_protected", social["required_interfaces"])
        self.assertIn("common_space_scheduler", social["required_interfaces"])
        self.assertIn("social_cultural_labor_hours_per_month", social["required_interfaces"])
        self.assertIn("loneliness_support_aggregate_report", social["required_interfaces"])
        self.assertIn("third_place", social["accepted_module_domains"])
        self.assertEqual(
            load_data(ROOT / "patterns" / "belonging_without_coercion_commons.yaml")["id"],
            "belonging_without_coercion_commons",
        )

    def test_module_registry_tracks_risk_resilience_interfaces(self) -> None:
        resilience = next(slot for slot in self.registry["slots"] if slot["id"] == "risk_resilience")

        self.assertIn("hazards_total", resilience["required_interfaces"])
        self.assertIn("dependency_graph_engine", resilience["required_interfaces"])
        self.assertIn("emergency_authority_sunset", resilience["required_interfaces"])
        self.assertIn("anti_capture_under_stress_report", resilience["required_interfaces"])
        self.assertIn("emergency_management", resilience["accepted_module_domains"])
        self.assertEqual(
            load_data(ROOT / "patterns" / "graceful_degradation_engine.yaml")["id"],
            "graceful_degradation_engine",
        )

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

    def test_module_implementation_allows_capability_only_module(self) -> None:
        module = _implementation_ready_governance_module()
        report = implement_technology_module(self.plan, module, None, days=14)

        self.assertEqual(report["kind"], "ModuleImplementationReport")
        self.assertEqual(report["status"], "implemented")
        self.assertEqual(report["scalability_gate"]["status"], "pass")
        self.assertEqual(report["applied_capability_effects"]["governance_anticapture"]["due_process_defined"], True)
        module_pattern_id = f"module_{module['id']}"
        self.assertIn(module_pattern_id, report["implemented_plan"]["selected_patterns"])
        self.assertIn(module_pattern_id, report["implemented_plan"]["simulation_inputs"]["capability_effects_by_pattern"])
        self.assertTrue(report["implemented_simulation"]["capability_state"]["ledger"])
        self.assertTrue(validate_data(report, "module-implementation").ok)

    def test_module_implementation_still_blocks_negative_resource_effects(self) -> None:
        module = _implementation_ready_governance_module()
        module["modeled_impacts"]["direct_resource_effects"]["water_liters_per_day"] = -10

        report = implement_technology_module(self.plan, module, None, days=14)

        self.assertIn(report["status"], {"blocked_by_scalability_gate", "blocked_by_effects"})
        self.assertIsNone(report["implemented_plan"])
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
                "private_food_autonomy": True,
                "common_meals_per_week": 3,
                "shelf_stable_buffer_days": 30,
                "reserve_drawdown_reduction": 0,
                "preservation_servings_per_year": 0,
                "seasonal_labor_hours": 0,
                "seasonal_menu_bridge": "not_applicable",
                "supplier_count": 2,
                "food_safety.review_dependency": "food_safety",
                "crop_failure_sensitivity": "bounded",
            },
            "provisional": True,
        },
        "integration_requirements": [],
        "unknowns": [],
    }


def _implementation_ready_governance_module() -> dict[str, object]:
    return {
        "kind": "TechnologyModule",
        "id": "explicit_governance_capability_module_v0",
        "name": "Explicit Governance Capability Module",
        "domain": ["governance", "anti_capture"],
        "status": "candidate",
        "provisional": True,
        "source_evidence": [
            {
                "id": "source_1",
                "citation": "Synthetic governance test evidence record",
                "url": "https://example.org/governance-evidence",
                "context": "Unit-test fixture for a capability-only CIaC module.",
                "provisional": True,
            }
        ],
        "performance_statistics": [
            {
                "id": "stat_1",
                "source_id": "source_1",
                "metric": "role_backup_coverage_delta",
                "value": 0.2,
                "unit": "ratio_delta",
                "evidence_status": "test_fixture",
                "provisional": True,
            }
        ],
        "applicability": {
            "target_slots": ["governance_anticapture"],
            "target_patterns": ["commons_stewardship_protocol"],
            "excludes": [],
            "provisional": True,
        },
        "modeled_impacts": {
            "dignity_floor_policy": "additive_only",
            "direct_resource_effects": {
                "food_servings_per_day": 0,
                "water_liters_per_day": 0,
                "energy_kwh_per_day": 0,
            },
            "candidate_modifiers": {
                "labor_hours_per_week": 0,
            },
            "capability_effects": {
                "governance_anticapture": {
                    "due_process_defined": True,
                    "emergency_power_sunset_defined": True,
                    "capture_risk_delta": -1,
                    "role_backup_coverage_delta": 0.2,
                }
            },
            "provisional": True,
        },
        "integration_requirements": [],
        "unknowns": [],
    }


if __name__ == "__main__":
    unittest.main()
