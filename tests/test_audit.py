from __future__ import annotations

import copy
import unittest
from pathlib import Path

from ciac.audit import evaluate_audit
from ciac.compiler import compile_plan, load_patterns
from ciac.energy import evaluate_energy
from ciac.gates import evaluate_gates
from ciac.io import load_data
from ciac.nutrition import evaluate_nutrition
from ciac.roles import evaluate_roles
from ciac.scenarios import run_scenario
from ciac.simulation import simulate
from ciac.validation import validate_data
from ciac.water import evaluate_water


ROOT = Path(__file__).resolve().parents[1]


class AuditTests(unittest.TestCase):
    def setUp(self) -> None:
        patterns = load_patterns(ROOT / "patterns")
        site = load_data(ROOT / "examples" / "site_profiles" / "micro_commons_5_households.yaml")
        self.plan = compile_plan(site, patterns)
        self.reports = {
            "gates": evaluate_gates(self.plan),
            "simulation": simulate(self.plan, days=365),
            "nutrition": evaluate_nutrition(self.plan, load_data(ROOT / "food_plans" / "micro_commons_basic.yaml")),
            "water": evaluate_water(self.plan, load_data(ROOT / "water_plans" / "micro_commons_basic.yaml")),
            "energy": evaluate_energy(self.plan, load_data(ROOT / "energy_plans" / "micro_commons_basic.yaml")),
            "roles": evaluate_roles(self.plan, load_data(ROOT / "role_plans" / "micro_commons_basic.yaml")),
        }
        self.scenarios = [
            run_scenario(self.plan, load_data(ROOT / "scenarios" / "drought.yaml")),
            run_scenario(self.plan, load_data(ROOT / "scenarios" / "water_contamination.yaml")),
        ]

    def test_current_micro_commons_audit_does_not_promote(self) -> None:
        report = evaluate_audit(self.plan, self.reports, self.scenarios)
        self.assertEqual(report["kind"], "AuditReport")
        self.assertEqual(report["overall_status"], "fail")
        self.assertEqual(report["promotion_decision"], "do_not_promote")
        self.assertTrue(validate_data(report, "audit").ok)
        self.assertTrue(any("water" in item for item in report["survival_critical_blockers"]))
        self.assertTrue(any("energy" in item for item in report["survival_critical_blockers"]))
        self.assertTrue(any("roles" in item for item in report["survival_critical_blockers"]))

    def test_warning_only_audit_requires_revision_before_pilot(self) -> None:
        reports = {
            "gates": {"kind": "GateReport", "id": "gates", "promotion_allowed": True, "results": []},
            "nutrition": {"kind": "NutritionReport", "id": "nutrition", "status": "warn", "bottlenecks": ["local share low"]},
        }
        report = evaluate_audit(self.plan, reports, [])
        self.assertEqual(report["overall_status"], "warn")
        self.assertEqual(report["promotion_decision"], "revise_before_pilot")

    def test_pass_audit_is_candidate_for_review_not_approval(self) -> None:
        reports = {
            "gates": {"kind": "GateReport", "id": "gates", "promotion_allowed": True, "results": []},
            "water": {"kind": "WaterReport", "id": "water", "status": "pass"},
            "energy": {"kind": "EnergyReport", "id": "energy", "status": "pass"},
            "roles": {"kind": "RoleReport", "id": "roles", "status": "pass"},
        }
        report = evaluate_audit(self.plan, reports, [])
        self.assertEqual(report["overall_status"], "pass")
        self.assertEqual(report["promotion_decision"], "candidate_for_review")
        self.assertIn("not approval", " ".join(report["unknowns"]))

    def test_failed_scenario_is_survival_critical_blocker(self) -> None:
        scenario = copy.deepcopy(self.scenarios[0])
        scenario["status"] = "fail"
        report = evaluate_audit(self.plan, {"gates": self.reports["gates"]}, [scenario])
        self.assertTrue(any("scenario:drought failed" in item for item in report["survival_critical_blockers"]))

    def test_audit_output_shape_is_stable_for_downstream_consumers(self) -> None:
        report = evaluate_audit(self.plan, self.reports, self.scenarios)
        self.assertEqual(
            list(report.keys()),
            [
                "kind",
                "id",
                "compiled_plan",
                "generated_by",
                "provisional",
                "overall_status",
                "promotion_decision",
                "confidence",
                "subsystem_statuses",
                "survival_critical_blockers",
                "noncritical_warnings",
                "required_redesigns",
                "top_risks",
                "next_sprint_recommendations",
                "inputs",
                "unknowns",
            ],
        )


if __name__ == "__main__":
    unittest.main()

