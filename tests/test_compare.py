from __future__ import annotations

import copy
import unittest

from ciac.compare import compare_audits
from ciac.validation import validate_data


class CompareTests(unittest.TestCase):
    def test_improved_comparison_validates(self) -> None:
        before = _audit(
            "before",
            ["water:old failed", "energy:still failed"],
            {"water": "fail", "energy": "fail", "scenario:drought": "fail"},
            "do_not_promote",
        )
        after = _audit(
            "after",
            ["energy:still failed"],
            {"water": "warn", "energy": "fail", "scenario:drought_reserve_v2": "warn"},
            "do_not_promote",
        )
        report = compare_audits(before, after)
        self.assertEqual(report["kind"], "ComparisonReport")
        self.assertEqual(report["status"], "improved")
        self.assertEqual(report["blocker_delta"], 1)
        self.assertIn("water:old failed", report["resolved_blockers"])
        self.assertTrue(validate_data(report, "comparison").ok)

    def test_regressed_comparison_detects_new_blocker(self) -> None:
        before = _audit("before", [], {"water": "pass"}, "candidate_for_review")
        after = _audit("after", ["water:new failed"], {"water": "fail"}, "do_not_promote")
        report = compare_audits(before, after)
        self.assertEqual(report["status"], "regressed")
        self.assertIn("water:new failed", report["new_blockers"])

    def test_unchanged_comparison(self) -> None:
        before = _audit("before", ["energy:failed"], {"energy": "fail"}, "do_not_promote")
        after = _audit("after", ["energy:failed"], {"energy": "fail"}, "do_not_promote")
        report = compare_audits(before, after)
        self.assertEqual(report["status"], "unchanged")
        self.assertEqual(report["blocker_delta"], 0)

    def test_water_acceptance_criteria_pass_for_v2_statuses(self) -> None:
        before = _audit("before", ["water:failed", "scenario:drought failed water_gate"], {"water": "fail", "scenario:drought": "fail"}, "do_not_promote")
        after = _audit("after", [], {"water": "warn", "scenario:drought_reserve_v2": "warn"}, "revise_before_pilot")
        report = compare_audits(before, after)
        water_criteria = [item for item in report["acceptance_criteria"] if item["candidate"] == "water_storage_and_drought_reserve"]
        self.assertTrue(all(item["passed"] for item in water_criteria))

    def test_energy_acceptance_criteria_pass_for_v3_statuses(self) -> None:
        before = _audit("before", ["energy:failed"], {"energy": "fail", "scenario:energy_outage": "fail"}, "do_not_promote")
        after = _audit("after", [], {"energy": "pass", "scenario:energy_outage_reserve_v2": "warn"}, "revise_before_pilot")
        report = compare_audits(before, after)
        energy_criteria = [item for item in report["acceptance_criteria"] if item["candidate"] == "energy_battery_and_backup"]
        self.assertTrue(all(item["passed"] for item in energy_criteria))

    def test_role_acceptance_criteria_pass_for_v4_statuses(self) -> None:
        before = _audit("before", ["roles:failed"], {"roles": "fail"}, "do_not_promote")
        after = _audit("after", [], {"roles": "warn"}, "revise_before_pilot")
        report = compare_audits(before, after)
        role_criteria = [
            item
            for item in report["acceptance_criteria"]
            if item["candidate"] in {"roles_train_second_energy_steward", "roles_rebalance_care_and_fairness"}
        ]
        self.assertTrue(all(item["passed"] for item in role_criteria))

    def test_contamination_acceptance_criteria_pass_for_v5_statuses(self) -> None:
        before = _audit(
            "before",
            ["scenario:water_contamination failed", "scenario:water_contamination failed water_gate"],
            {"scenario:water_contamination": "fail"},
            "do_not_promote",
        )
        after = _audit(
            "after",
            [],
            {"scenario:water_contamination_response_v2": "warn"},
            "revise_before_pilot",
        )
        report = compare_audits(before, after)
        contamination_criteria = [
            item for item in report["acceptance_criteria"] if item["candidate"] == "water_verified_backup_source"
        ]
        self.assertTrue(all(item["passed"] for item in contamination_criteria))

    def test_comparison_output_shape_is_stable_for_downstream_consumers(self) -> None:
        report = compare_audits(
            _audit("before", ["water:failed"], {"water": "fail"}, "do_not_promote"),
            _audit("after", [], {"water": "warn"}, "revise_before_pilot"),
        )
        self.assertEqual(
            list(report.keys()),
            [
                "kind",
                "id",
                "before_audit",
                "after_audit",
                "generated_by",
                "provisional",
                "status",
                "blocker_count_before",
                "blocker_count_after",
                "blocker_delta",
                "promotion_decision_delta",
                "status_changes_by_subsystem",
                "resolved_blockers",
                "remaining_blockers",
                "new_blockers",
                "new_warnings",
                "metric_deltas",
                "acceptance_criteria",
                "summary",
                "unknowns",
            ],
        )


def _audit(
    audit_id: str,
    blockers: list[str],
    statuses: dict[str, str],
    decision: str,
) -> dict:
    return {
        "kind": "AuditReport",
        "id": audit_id,
        "promotion_decision": decision,
        "survival_critical_blockers": copy.deepcopy(blockers),
        "noncritical_warnings": [],
        "subsystem_statuses": {
            key: {"kind": "MockReport", "status": value, "survival_critical": True}
            for key, value in statuses.items()
        },
    }


if __name__ == "__main__":
    unittest.main()
