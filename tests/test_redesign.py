from __future__ import annotations

import unittest
from pathlib import Path

from ciac.audit import evaluate_audit
from ciac.compiler import compile_plan, load_patterns
from ciac.energy import evaluate_energy
from ciac.gates import evaluate_gates
from ciac.io import load_data
from ciac.nutrition import evaluate_nutrition
from ciac.redesign import generate_redesign
from ciac.roles import evaluate_roles
from ciac.scenarios import run_scenario
from ciac.simulation import simulate
from ciac.validation import validate_data
from ciac.water import evaluate_water


ROOT = Path(__file__).resolve().parents[1]


class RedesignTests(unittest.TestCase):
    def setUp(self) -> None:
        patterns = load_patterns(ROOT / "patterns")
        site = load_data(ROOT / "examples" / "site_profiles" / "micro_commons_5_households.yaml")
        self.plan = compile_plan(site, patterns)
        reports = {
            "gates": evaluate_gates(self.plan),
            "simulation": simulate(self.plan, days=365),
            "nutrition": evaluate_nutrition(self.plan, load_data(ROOT / "food_plans" / "micro_commons_basic.yaml")),
            "water": evaluate_water(self.plan, load_data(ROOT / "water_plans" / "micro_commons_basic.yaml")),
            "energy": evaluate_energy(self.plan, load_data(ROOT / "energy_plans" / "micro_commons_basic.yaml")),
            "roles": evaluate_roles(self.plan, load_data(ROOT / "role_plans" / "micro_commons_basic.yaml")),
        }
        scenarios = [
            run_scenario(self.plan, load_data(ROOT / "scenarios" / "drought.yaml")),
            run_scenario(self.plan, load_data(ROOT / "scenarios" / "water_contamination.yaml")),
        ]
        self.audit = evaluate_audit(self.plan, reports, scenarios)

    def test_redesign_report_validates(self) -> None:
        report = generate_redesign(self.audit, self.plan)
        self.assertEqual(report["kind"], "RedesignReport")
        self.assertEqual(report["status"], "ready_for_iteration")
        self.assertTrue(validate_data(report, "redesign").ok)

    def test_current_audit_generates_expected_subsystem_candidates(self) -> None:
        report = generate_redesign(self.audit, self.plan)
        subsystems = {candidate["subsystem"] for candidate in report["redesign_candidates"]}
        self.assertIn("water", subsystems)
        self.assertIn("energy", subsystems)
        self.assertIn("roles", subsystems)
        self.assertIn("nutrition", subsystems)

    def test_first_priority_is_water_reserve(self) -> None:
        report = generate_redesign(self.audit, self.plan)
        self.assertEqual(report["priority_order"][0], "water_storage_and_drought_reserve")
        first = report["redesign_candidates"][0]
        self.assertIn("water_plans/micro_commons_basic.yaml", first["files_to_edit"])
        self.assertTrue(first["acceptance_criteria"])

    def test_empty_audit_produces_draft_report(self) -> None:
        audit = {
            "kind": "AuditReport",
            "id": "empty_audit",
            "survival_critical_blockers": [],
            "noncritical_warnings": [],
            "top_risks": [],
            "required_redesigns": [],
        }
        report = generate_redesign(audit, self.plan)
        self.assertEqual(report["status"], "draft")
        self.assertEqual(report["redesign_candidates"], [])

    def test_redesign_output_shape_is_stable_for_downstream_consumers(self) -> None:
        report = generate_redesign(self.audit, self.plan)
        self.assertEqual(
            list(report.keys()),
            [
                "kind",
                "id",
                "compiled_plan",
                "audit_report",
                "generated_by",
                "provisional",
                "status",
                "blockers_by_subsystem",
                "redesign_candidates",
                "priority_order",
                "next_actions",
                "unknowns",
            ],
        )


if __name__ == "__main__":
    unittest.main()

