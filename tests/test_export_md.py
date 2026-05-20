from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from ciac.cli import main
from ciac.export_md import render_review_packet, write_review_packet


class ExportMarkdownTests(unittest.TestCase):
    def setUp(self) -> None:
        self.compiled_plan = {
            "kind": "CompiledPlan",
            "id": "micro_commons_plan",
        }
        self.audit = {
            "kind": "AuditReport",
            "id": "audit",
            "overall_status": "warn",
            "promotion_decision": "revise_before_pilot",
            "survival_critical_blockers": [],
            "noncritical_warnings": ["water:contamination fallback window is insufficient"],
            "subsystem_statuses": {
                "water": {"status": "warn"},
                "roles": {"status": "pass"},
            },
            "inputs": {"scenarios": ["drought", "contamination"]},
        }
        self.dossier = {
            "kind": "PilotDossier",
            "id": "dossier",
            "readiness_status": "review_package_needed",
            "current_promotion_decision": "revise_before_pilot",
            "required_professional_reviews": [
                {
                    "id": "water_public_health",
                    "title": "Water / public health review",
                    "reviewer": "licensed water/public-health professional",
                    "reason": "Required for water safety.",
                }
            ],
            "unresolved_warnings_by_subsystem": {
                "water": ["Contamination fallback is incomplete."],
            },
            "go_no_go_checklist": [
                {"item": "Professional reviews are complete.", "status": "fail", "evidence": "none"},
            ],
            "must_never_be_inferred": [
                "Do not infer that a generated plan is legally permitted.",
            ],
        }
        self.review = {
            "kind": "ReviewStatusReport",
            "id": "review",
            "status": "missing_evidence",
            "required_reviews_covered": ["sanitation"],
            "required_reviews_missing": ["water_public_health"],
            "expired_or_rejected_evidence": ["insurance_liability:rejected"],
            "unresolved_issues_by_domain": {
                "water_public_health": ["lab water quality results are missing"],
            },
            "go_no_go_updates": [
                {
                    "item": "Professional reviews are complete.",
                    "original_status": "fail",
                    "updated_status": "fail",
                    "evidence": "1 review(s) covered; 1 missing; 1 expired/rejected.",
                }
            ],
        }

    def test_review_packet_contains_expected_sections_and_statuses(self) -> None:
        markdown = render_review_packet(self.compiled_plan, self.audit, self.dossier, self.review)

        for heading in [
            "# CIaC Review Packet",
            "## Executive Summary",
            "## Current Status",
            "## Required Professional Reviews",
            "## Missing Or Rejected Review Evidence",
            "## Go/No-Go Checklist",
            "## Must Never Be Inferred",
            "## Next Actions",
        ]:
            self.assertIn(heading, markdown)
        self.assertIn("`revise_before_pilot`", markdown)
        self.assertIn("`review_package_needed`", markdown)
        self.assertIn("`missing_evidence`", markdown)

    def test_review_packet_does_not_invent_iteration_claims(self) -> None:
        markdown = render_review_packet(self.compiled_plan, self.audit, self.dossier, self.review)

        self.assertIn("Compare reports remain the source of truth", markdown)
        self.assertNotIn("moved from failing to warning", markdown)

    def test_write_review_packet_creates_parent_directory(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "reports" / "packet.md"
            write_review_packet(target, "hello\n")

            self.assertEqual(target.read_text(encoding="utf-8"), "hello\n")

    def test_cli_export_md_writes_markdown_packet(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            compiled = root / "compiled.json"
            audit = root / "audit.json"
            dossier = root / "dossier.json"
            review = root / "review.json"
            output = root / "reports" / "packet.md"
            compiled.write_text(json.dumps(self.compiled_plan), encoding="utf-8")
            audit.write_text(json.dumps(self.audit), encoding="utf-8")
            dossier.write_text(json.dumps(self.dossier), encoding="utf-8")
            review.write_text(json.dumps(self.review), encoding="utf-8")

            code = main(
                [
                    "export-md",
                    str(compiled),
                    "--audit",
                    str(audit),
                    "--dossier",
                    str(dossier),
                    "--review",
                    str(review),
                    "--output",
                    str(output),
                ]
            )

            self.assertEqual(code, 0)
            self.assertIn("# CIaC Review Packet", output.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
