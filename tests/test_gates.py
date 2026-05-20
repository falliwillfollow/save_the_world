from __future__ import annotations

import copy
import unittest
from pathlib import Path

from ciac.compiler import CompileError, compile_plan, load_patterns
from ciac.gates import evaluate_gates
from ciac.io import load_data
from ciac.validation import validate_data


ROOT = Path(__file__).resolve().parents[1]


class GateTests(unittest.TestCase):
    def setUp(self) -> None:
        self.patterns = load_patterns(ROOT / "patterns")
        self.site = load_data(ROOT / "examples" / "site_profiles" / "micro_commons_5_households.yaml")

    def test_happy_plan_has_no_survival_critical_failures(self) -> None:
        report = evaluate_gates(compile_plan(self.site, self.patterns))
        self.assertTrue(report["promotion_allowed"])
        self.assertTrue(validate_data(report, "gates").ok)
        self.assertFalse(
            [
                result
                for result in report["results"]
                if result["survival_critical"] and result["status"] == "fail"
            ]
        )

    def test_food_gate_warns_until_nutrition_simulation_exists(self) -> None:
        report = evaluate_gates(compile_plan(self.site, self.patterns))
        food_gate = next(result for result in report["results"] if result["gate"] == "food_gate")
        self.assertEqual(food_gate["status"], "warn")
        self.assertTrue(food_gate["remediation"])

    def test_bad_plan_fails_gates_with_remediation(self) -> None:
        site = copy.deepcopy(self.site)
        site["selected_patterns"] = ["starter_dwelling", "solar_shed"]
        with self.assertRaises(CompileError) as raised:
            compile_plan(site, self.patterns)
        report = evaluate_gates(raised.exception.plan)
        self.assertFalse(report["promotion_allowed"])
        failures = [result for result in report["results"] if result["status"] == "fail"]
        self.assertTrue(failures)
        self.assertTrue(all(result["remediation"] for result in failures))


if __name__ == "__main__":
    unittest.main()

