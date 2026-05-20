from __future__ import annotations

import copy
import unittest

from ciac.review import evaluate_review_status
from ciac.validation import validate_data


class ReviewTests(unittest.TestCase):
    def setUp(self) -> None:
        self.dossier = {
            "kind": "PilotDossier",
            "id": "dossier",
            "readiness_status": "review_package_needed",
            "required_professional_reviews": [
                {"id": "water_public_health", "required": True},
                {"id": "electrical", "required": True},
            ],
            "go_no_go_checklist": [
                {"item": "Professional reviews are complete.", "status": "fail", "evidence": "none"},
            ],
        }
        self.register = {
            "kind": "ReviewRegister",
            "id": "register",
            "reviews": [
                {
                    "domain": "water_public_health",
                    "reviewer_name": "",
                    "reviewer_org": "",
                    "credential_type": "",
                    "artifact_reference": "",
                    "status": "submitted",
                    "expiration_date": "",
                    "notes": "",
                    "unresolved_issues": ["lab report missing"],
                },
                {
                    "domain": "electrical",
                    "reviewer_name": "",
                    "reviewer_org": "",
                    "credential_type": "",
                    "artifact_reference": "",
                    "status": "missing",
                    "expiration_date": "",
                    "notes": "",
                    "unresolved_issues": [],
                },
            ],
        }

    def test_review_status_validates_with_missing_evidence(self) -> None:
        report = evaluate_review_status(self.dossier, self.register)
        self.assertEqual(report["kind"], "ReviewStatusReport")
        self.assertEqual(report["status"], "in_progress")
        self.assertIn("water_public_health", report["required_reviews_covered"])
        self.assertIn("electrical", report["required_reviews_missing"])
        self.assertTrue(validate_data(report, "review").ok)

    def test_rejected_evidence_blocks_status(self) -> None:
        register = copy.deepcopy(self.register)
        register["reviews"][0]["status"] = "rejected"
        report = evaluate_review_status(self.dossier, register)
        self.assertEqual(report["status"], "missing_evidence")
        self.assertIn("water_public_health:rejected", report["expired_or_rejected_evidence"])

    def test_all_reviews_covered_can_update_readiness(self) -> None:
        register = copy.deepcopy(self.register)
        for review in register["reviews"]:
            review["status"] = "accepted"
        report = evaluate_review_status(self.dossier, register)
        self.assertEqual(report["status"], "ready_for_review_update")
        self.assertEqual(report["readiness_delta"]["after"], "candidate_for_external_review")

    def test_review_output_shape_is_stable_for_downstream_consumers(self) -> None:
        report = evaluate_review_status(self.dossier, self.register)
        self.assertEqual(
            list(report.keys()),
            [
                "kind",
                "id",
                "dossier",
                "review_register",
                "generated_by",
                "provisional",
                "status",
                "required_reviews_covered",
                "required_reviews_missing",
                "review_status_by_domain",
                "expired_or_rejected_evidence",
                "unresolved_issues_by_domain",
                "go_no_go_updates",
                "readiness_delta",
                "unknowns",
            ],
        )


if __name__ == "__main__":
    unittest.main()

