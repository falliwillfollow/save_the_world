from __future__ import annotations

import unittest
from pathlib import Path

from ciac.capabilities import apply_capability_effects, default_capability_state
from ciac.capability_policy import evaluate_policy_gates, load_capability_policy
from ciac.validation import validate_data


ROOT = Path(__file__).resolve().parents[1]


class CapabilityPolicyGateTests(unittest.TestCase):
    def setUp(self) -> None:
        self.policy = load_capability_policy(ROOT / "capability_policies" / "ciac_capability_policy_v0.yaml")

    def test_default_state_warns_or_blocks_missing_policy_capabilities(self) -> None:
        report = evaluate_policy_gates(default_capability_state(), self.policy, mode="simulation")

        self.assertEqual(report["status"], "warn")
        self.assertEqual(report["domain_statuses"]["care_health"]["status"], "warn")
        self.assertEqual(report["domain_statuses"]["risk_resilience"]["status"], "warn")
        self.assertTrue(validate_data(report, "policy-gate").ok)

    def test_promotion_mode_blocks_missing_due_process_and_routes(self) -> None:
        report = evaluate_policy_gates(default_capability_state(), self.policy, mode="promotion")

        self.assertEqual(report["status"], "promotion_blocked")
        self.assertEqual(report["promotion_mode"], "review_blocked")
        self.assertTrue(any("due process" in item.lower() for item in report["promotion_blockers"]))
        self.assertTrue(any("accessible" in item.lower() for item in report["promotion_blockers"]))

    def test_care_policy_passes_when_core_fields_are_satisfied(self) -> None:
        state = apply_capability_effects(
            default_capability_state(),
            pattern_id="full_care_policy_test",
            effects={
                "care_health": {
                    "care_continuity_protocol_supported": True,
                    "medication_continuity_supported": True,
                    "care_meal_protocol_supported": True,
                    "illness_wave_protocol_supported": True,
                    "high_need_support_coverage_delta": 1.0,
                }
            },
        )

        report = evaluate_policy_gates(state, self.policy)

        self.assertEqual(report["domain_statuses"]["care_health"]["status"], "pass")

    def test_labor_zero_is_not_a_policy_pass(self) -> None:
        report = evaluate_policy_gates(default_capability_state(), self.policy)

        labor_messages = "\n".join(report["domain_statuses"]["labor_time"]["messages"])
        self.assertIn("unmeasured", labor_messages)

    def test_simulation_mode_never_claims_promotion_ready(self) -> None:
        state = default_capability_state()
        state["domains"].update(
            {
                "care_health": {
                    "care_continuity_protocol_supported": True,
                    "medication_continuity_supported": True,
                    "care_meal_protocol_supported": True,
                    "illness_wave_protocol_supported": True,
                    "high_need_support_coverage": 1.0,
                },
                "governance_anticapture": {
                    "due_process_defined": True,
                    "emergency_power_sunset_defined": True,
                    "role_backup_coverage": 1.0,
                },
                "sanitation": {
                    "toilet_hygiene_access_supported": True,
                    "blackwater_path_defined": True,
                    "greywater_boundary_defined": True,
                    "waste_stream_separation_supported": True,
                    "hazardous_waste_plan_supported": True,
                    "worker_safety_training_supported": True,
                    "sanitation_labor_visibility_supported": True,
                    "emergency_sanitation_fallback_supported": True,
                    "pathogen_control_protocol_supported": True,
                },
                "mobility_access": {
                    "accessible_route_coverage": 1.0,
                    "non_driver_access_supported": True,
                    "emergency_access_supported": True,
                },
                "legal_land_finance": {
                    "land_security_status": "pass",
                    "reserve_modeling_supported": True,
                    "resident_rights_defined": True,
                },
                "risk_resilience": {
                    "hazard_register_supported": True,
                    "dependency_graph_supported": True,
                    "dependency_graph_coverage": 1.0,
                    "recovery_playbook_count": 8,
                    "graceful_degradation_supported": True,
                },
                "labor_time": {
                    "commons_labor_hours_per_resident_per_week": 2,
                    "hidden_labor_tracking_supported": True,
                    "free_time_increase_supported": True,
                    "required_wage_hours_reduction_percent": 25,
                },
            }
        )

        report = evaluate_policy_gates(state, self.policy, mode="simulation")

        self.assertEqual(report["status"], "pass")
        self.assertEqual(report["promotion_mode"], "simulation_only")


if __name__ == "__main__":
    unittest.main()
