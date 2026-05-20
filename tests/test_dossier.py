from __future__ import annotations

import unittest
from pathlib import Path

from ciac.compiler import compile_plan, load_patterns
from ciac.dossier import generate_dossier
from ciac.io import load_data
from ciac.validation import validate_data


ROOT = Path(__file__).resolve().parents[1]


class DossierTests(unittest.TestCase):
    def setUp(self) -> None:
        patterns = load_patterns(ROOT / "patterns")
        site = load_data(ROOT / "examples" / "site_profiles" / "micro_commons_5_households.yaml")
        self.plan = compile_plan(site, patterns)
        self.audit = {
            "kind": "AuditReport",
            "id": "audit_v5",
            "promotion_decision": "revise_before_pilot",
            "confidence": "low",
            "survival_critical_blockers": [],
            "noncritical_warnings": [
                "water:contamination fallback window is insufficient",
                "energy:solar reduction scenario is not resilient",
                "roles:Role load distribution is uneven enough to create fairness or burnout risk.",
            ],
        }

    def test_dossier_validates_and_requires_review_package(self) -> None:
        dossier = generate_dossier(self.audit, self.plan)
        self.assertEqual(dossier["kind"], "PilotDossier")
        self.assertEqual(dossier["readiness_status"], "review_package_needed")
        self.assertTrue(validate_data(dossier, "dossier").ok)

    def test_required_reviews_include_core_safety_domains(self) -> None:
        dossier = generate_dossier(self.audit, self.plan)
        review_ids = {review["id"] for review in dossier["required_professional_reviews"]}
        self.assertIn("water_public_health", review_ids)
        self.assertIn("electrical", review_ids)
        self.assertIn("structural_building", review_ids)
        self.assertIn("sanitation", review_ids)
        self.assertIn("governance_legal", review_ids)

    def test_do_not_promote_audit_is_not_ready(self) -> None:
        audit = dict(self.audit)
        audit["promotion_decision"] = "do_not_promote"
        audit["survival_critical_blockers"] = ["water failed"]
        dossier = generate_dossier(audit, self.plan)
        self.assertEqual(dossier["readiness_status"], "not_ready")
        first_check = dossier["go_no_go_checklist"][0]
        self.assertEqual(first_check["status"], "fail")

    def test_must_never_be_inferred_is_explicit(self) -> None:
        dossier = generate_dossier(self.audit, self.plan)
        text = " ".join(dossier["must_never_be_inferred"])
        self.assertIn("legally permitted", text)
        self.assertIn("residents consent", text)
        self.assertIn("approved for construction", text)

    def test_dossier_output_shape_is_stable_for_downstream_consumers(self) -> None:
        dossier = generate_dossier(self.audit, self.plan)
        self.assertEqual(
            list(dossier.keys()),
            [
                "kind",
                "id",
                "compiled_plan",
                "audit_report",
                "generated_by",
                "provisional",
                "current_promotion_decision",
                "readiness_status",
                "unresolved_warnings_by_subsystem",
                "required_professional_reviews",
                "legal_jurisdictional_unknowns",
                "evidence_gaps",
                "resident_governance_questions",
                "documents_needed_before_pilot",
                "go_no_go_checklist",
                "must_never_be_inferred",
                "unknowns",
            ],
        )


if __name__ == "__main__":
    unittest.main()

