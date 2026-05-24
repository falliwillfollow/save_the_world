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

    def test_care_gate_warns_when_core_care_fields_are_missing(self) -> None:
        state = default_capability_state()
        updated = apply_capability_effects(
            state,
            pattern_id="medication_continuity_only",
            effects={
                "care_health": {
                    "care_continuity_protocol_supported": True,
                    "medication_continuity_supported": True,
                }
            },
        )

        report = evaluate_capability_gate(updated, active_patterns=[])
        care = report["domain_statuses"]["care_health"]

        self.assertEqual(care["status"], "warn")
        self.assertIn("High-need support coverage is below the review threshold.", care["messages"])
        self.assertIn("Care meal protocol is not explicitly supported.", care["messages"])
        self.assertIn("Illness-wave protocol is not explicitly supported.", care["messages"])
        self.assertNotIn("Medication continuity is not yet explicitly supported.", care["messages"])

    def test_care_gate_passes_when_core_care_fields_are_supported(self) -> None:
        state = default_capability_state()
        updated = apply_capability_effects(
            state,
            pattern_id="full_care_test",
            effects={
                "care_health": {
                    "care_continuity_protocol_supported": True,
                    "medication_continuity_supported": True,
                    "care_meal_protocol_supported": True,
                    "illness_wave_protocol_supported": True,
                    "high_need_support_coverage_delta": 0.25,
                }
            },
        )

        report = evaluate_capability_gate(updated, active_patterns=[])

        self.assertEqual(report["domain_statuses"]["care_health"]["status"], "pass")


if __name__ == "__main__":
    unittest.main()
