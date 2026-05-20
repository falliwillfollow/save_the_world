from __future__ import annotations

import copy
import unittest
from pathlib import Path

from ciac.compiler import compile_plan, load_patterns
from ciac.energy import evaluate_energy
from ciac.io import load_data
from ciac.validation import validate_data


ROOT = Path(__file__).resolve().parents[1]


class EnergyTests(unittest.TestCase):
    def setUp(self) -> None:
        patterns = load_patterns(ROOT / "patterns")
        site = load_data(ROOT / "examples" / "site_profiles" / "micro_commons_5_households.yaml")
        self.plan = compile_plan(site, patterns)
        self.energy_plan = load_data(ROOT / "energy_plans" / "micro_commons_basic.yaml")

    def test_basic_energy_plan_validates_and_fails_outage(self) -> None:
        report = evaluate_energy(self.plan, self.energy_plan)
        self.assertEqual(report["kind"], "EnergyReport")
        self.assertEqual(report["status"], "fail")
        self.assertTrue(validate_data(report, "energy").ok)
        self.assertEqual(report["normal_balance"]["status"], "pass")
        self.assertEqual(report["outage_survival"]["status"], "fail")
        self.assertIn("battery storage does not meet outage target", report["bottlenecks"])

    def test_more_battery_improves_outage_survival(self) -> None:
        energy_plan = copy.deepcopy(self.energy_plan)
        energy_plan["storage"]["battery_usable_kwh"] = 80
        report = evaluate_energy(self.plan, energy_plan)
        self.assertEqual(report["critical_load_autonomy"]["status"], "pass")
        self.assertEqual(report["outage_survival"]["status"], "pass")

    def test_missing_solar_shed_warns(self) -> None:
        plan = copy.deepcopy(self.plan)
        plan["selected_patterns"] = [pattern for pattern in plan["selected_patterns"] if pattern != "solar_shed"]
        report = evaluate_energy(plan, self.energy_plan)
        self.assertIn(
            "Compiled plan does not include solar_shed; solar energy assumptions may be unsupported.",
            report["energy_safety_warnings"],
        )

    def test_unqualified_maintenance_warns(self) -> None:
        energy_plan = copy.deepcopy(self.energy_plan)
        energy_plan["maintenance"]["requires_qualified_review"] = False
        report = evaluate_energy(self.plan, energy_plan)
        self.assertEqual(report["maintenance"]["status"], "warn")
        self.assertIn("energy maintenance protocol is incomplete", report["bottlenecks"])

    def test_energy_output_shape_is_stable_for_downstream_consumers(self) -> None:
        report = evaluate_energy(self.plan, self.energy_plan)
        self.assertEqual(
            list(report.keys()),
            [
                "kind",
                "id",
                "compiled_plan",
                "energy_plan",
                "generated_by",
                "days",
                "provisional",
                "status",
                "normal_balance",
                "critical_load_autonomy",
                "outage_survival",
                "load_shedding_plan",
                "solar_reduction",
                "refrigeration_risk",
                "backup_energy_gap",
                "maintenance",
                "energy_safety_warnings",
                "redesign_recommendations",
                "bottlenecks",
                "unknowns",
            ],
        )


if __name__ == "__main__":
    unittest.main()
