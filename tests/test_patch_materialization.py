from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from ciac.cli import main
from ciac.io import load_data, write_json
from ciac.patch_materialization import materialize_patch_proposal
from ciac.research_loop import build_patch_proposal
from ciac.validation import validate_data


ROOT = Path(__file__).resolve().parents[1]
DISCOVERY = ROOT / "examples" / "discovery" / "civic_floor_80_discovery_loop_v0.discovery.json"


class PatchMaterializationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.candidate = load_data(DISCOVERY)["seed_candidates"][0]
        self.patch = build_patch_proposal(self.candidate)

    def test_materializes_patch_as_valid_civic_pattern(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            report = materialize_patch_proposal(self.patch, self.candidate, repo_root=tmp)

            self.assertEqual(report["kind"], "PatchMaterializationReport")
            self.assertEqual(report["status"], "materialized_draft")
            self.assertTrue(validate_data(report, "materialization").ok)
            pattern_path = Path(tmp) / report["materialized_artifact_path"]
            self.assertTrue(pattern_path.exists())
            pattern = load_data(pattern_path)
            self.assertEqual(pattern["kind"], "CivicPattern")
            self.assertEqual(pattern["id"], self.candidate["id"])
            self.assertTrue(pattern["capability_effects"]["care_health"]["medication_continuity_supported"])
            self.assertTrue(validate_data(pattern, str(pattern_path)).ok)

    def test_cli_materialize_patch_writes_report(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            patch_path = root / "patch.json"
            candidate_path = root / "candidate.json"
            report_path = root / "materialization.json"
            write_json(patch_path, self.patch)
            write_json(candidate_path, self.candidate)

            code = main(
                [
                    "materialize-patch",
                    str(patch_path),
                    "--candidate",
                    str(candidate_path),
                    "--repo-root",
                    str(root),
                    "--output",
                    str(report_path),
                ]
            )

            self.assertEqual(code, 0)
            report = load_data(report_path)
            self.assertEqual(report["status"], "materialized_draft")
            self.assertTrue((root / report["materialized_artifact_path"]).exists())

    def test_water_public_health_protocol_materializes_to_water_node(self) -> None:
        candidate = {
            "kind": "DiscoveryCandidateIntervention",
            "version": "v0",
            "id": "water_public_health_fallback_supply_protocol_test",
            "source_loop_id": "test_water_loop",
            "focus_domain": "water_public_health",
            "title": "Water fallback supply protocol",
            "hypothesis": "Fallback supply protocol keeps isolated reserve labor and public-health review visible during water disruption.",
            "intervention_type": "operating_protocol",
            "target_objects": ["node_water_reserve"],
            "module_refs": ["water.resilient_water_commons.v0_1"],
            "assumptions": [
                {
                    "id": "assumption_supply_chain",
                    "statement": "Fallback water supply paths require local verification.",
                    "confidence": "low",
                    "needs_evidence": True,
                }
            ],
            "expected_effects": [
                {
                    "metric": "water_public_health.recovery_labor_visibility_supported",
                    "direction": "increase",
                    "rationale": "Makes water recovery labor visible.",
                }
            ],
            "risk_tradeoffs": [
                {
                    "risk": "Fallback supply work increases tracked labor.",
                    "severity": "medium",
                    "mitigation": "Track the work explicitly and require labor-burden review.",
                }
            ],
            "simulation_hooks": {
                "metrics_to_compare": ["capabilities.domain_statuses"],
                "scenarios_to_run": ["water_contamination_response_v2"],
                "acceptance_tests": ["No hidden resident labor."],
            },
            "rag_context": {
                "queries": ["water fallback reserve labor public health"],
                "required_sources": ["patterns/"],
                "source_ids": ["test_source"],
            },
            "status": "generated",
            "provisional": True,
        }
        patch = build_patch_proposal(candidate)
        with tempfile.TemporaryDirectory() as tmp:
            report = materialize_patch_proposal(patch, candidate, repo_root=tmp)

            self.assertEqual(report["status"], "materialized_draft")
            self.assertEqual(report["placement_target"]["object_id"], "node_water_reserve")
            pattern = load_data(Path(tmp) / report["materialized_artifact_path"])
            self.assertTrue(pattern["capability_effects"]["water_public_health"]["reserve_sanitation_protocol_supported"])
            self.assertTrue(pattern["capability_effects"]["labor_time"]["water_recovery_labor_visibility_supported"])
            self.assertEqual(pattern["governance"]["stewardship_role"], "water_steward")
            self.assertEqual(pattern["simulation"]["critical_resources"], ["maintenance", "water"])

    def test_mobility_access_protocol_materializes_to_route_network(self) -> None:
        candidate = {
            "kind": "DiscoveryCandidateIntervention",
            "version": "v0",
            "id": "mobility_access_accessible_route_gap_survey_map_test",
            "source_loop_id": "test_mobility_loop",
            "focus_domain": "mobility_access",
            "title": "Accessible route coverage map gap survey",
            "hypothesis": "Every daily task route should declare grade, surface, rest points, lighting, and emergency access status.",
            "intervention_type": "pattern_patch",
            "target_objects": ["zone_mobility_loop"],
            "module_refs": ["mobility_access.pedestrian_first_access_commons.v0_1"],
            "assumptions": [
                {
                    "id": "assumption_route_survey",
                    "statement": "Route survey findings require local verification.",
                    "confidence": "low",
                    "needs_evidence": True,
                }
            ],
            "expected_effects": [
                {
                    "metric": "accessible_route_coverage",
                    "direction": "increase",
                    "rationale": "Makes route gaps visible and improves modeled coverage.",
                }
            ],
            "risk_tradeoffs": [
                {
                    "risk": "Proxy geometry may imply false compliance.",
                    "severity": "high",
                    "mitigation": "Keep coverage provisional until surveyed.",
                }
            ],
            "simulation_hooks": {
                "metrics_to_compare": ["capabilities.domain_statuses"],
                "scenarios_to_run": ["scenario_illness_wave"],
                "acceptance_tests": ["No hidden resident labor."],
            },
            "rag_context": {
                "queries": ["mobility access route survey"],
                "required_sources": ["patterns/"],
                "source_ids": ["test_source"],
            },
            "status": "generated",
            "provisional": True,
        }
        patch = build_patch_proposal(candidate)
        with tempfile.TemporaryDirectory() as tmp:
            report = materialize_patch_proposal(patch, candidate, repo_root=tmp)

            self.assertEqual(report["status"], "materialized_draft")
            self.assertEqual(report["placement_target"]["object_id"], "zone_mobility_loop")
            pattern_path = Path(tmp) / report["materialized_artifact_path"]
            pattern = load_data(pattern_path)
            self.assertTrue(pattern["capability_effects"]["mobility_access"]["route_gap_survey_supported"])
            self.assertEqual(pattern["capability_effects"]["mobility_access"]["accessible_route_coverage_delta"], 0.25)
            self.assertTrue(pattern["capability_effects"]["labor_time"]["mobility_labor_visibility_supported"])
            self.assertEqual(pattern["governance"]["stewardship_role"], "mobility_steward")
            self.assertEqual(pattern["simulation"]["critical_resources"], ["maintenance"])
            self.assertNotIn("medication", pattern_path.read_text(encoding="utf-8").lower())


if __name__ == "__main__":
    unittest.main()
