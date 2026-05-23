from __future__ import annotations

import unittest

from ciac.capabilities import apply_capability_effects, default_capability_state, evaluate_capability_gate
from ciac.validation import validate_data


class CapabilityTests(unittest.TestCase):
    def test_apply_simple_capability_effects_records_ledger(self) -> None:
        state = default_capability_state(population=12)
        updated = apply_capability_effects(
            state,
            pattern_id="life_burden_ledger",
            effects={
                "labor_time": {
                    "hidden_labor_tracking_supported": True,
                    "hidden_labor_risk_delta": -2,
                }
            },
        )

        labor = updated["domains"]["labor_time"]
        self.assertTrue(labor["hidden_labor_tracking_supported"])
        self.assertEqual(labor["hidden_labor_risk_score"], 3)
        self.assertTrue(any(entry["field"] == "hidden_labor_risk_score" for entry in updated["ledger"]))
        self.assertTrue(validate_data(updated, "capability-state").ok)

    def test_coverage_and_risk_scores_are_clamped(self) -> None:
        state = default_capability_state()
        updated = apply_capability_effects(
            state,
            pattern_id="test_pattern",
            effects={
                "governance_anticapture": {
                    "role_backup_coverage_delta": 2,
                    "capture_risk_delta": -20,
                }
            },
        )

        governance = updated["domains"]["governance_anticapture"]
        self.assertEqual(governance["role_backup_coverage"], 1)
        self.assertEqual(governance["capture_risk_score"], 0)

    def test_capability_gate_warns_or_fails_by_active_pattern(self) -> None:
        state = default_capability_state()

        inactive_report = evaluate_capability_gate(state, active_patterns=[])
        active_report = evaluate_capability_gate(state, active_patterns=["commons_stewardship_protocol"])

        self.assertEqual(inactive_report["status"], "warn")
        self.assertEqual(active_report["status"], "fail")
        self.assertTrue(validate_data(active_report, "capability-gate").ok)


if __name__ == "__main__":
    unittest.main()
