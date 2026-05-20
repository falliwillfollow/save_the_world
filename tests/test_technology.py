from __future__ import annotations

import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from ciac.ai_research import OpenAIConfigurationError, draft_technology_module
from ciac.cli import main
from ciac.io import load_data
from ciac.research import evaluate_scalability_gate, generate_research_needs
from ciac.technology import evaluate_module_compatibility, pressure_test_technology_module
from ciac.validation import validate_data


ROOT = Path(__file__).resolve().parents[1]
GENERATED = ROOT / "examples" / "generated"


class TechnologyModuleTests(unittest.TestCase):
    def setUp(self) -> None:
        self.plan = load_data(GENERATED / "micro_commons_plan.json")
        self.simulation = load_data(GENERATED / "micro_commons_simulation.json")
        self.module = load_data(ROOT / "tech_modules" / "agrivoltaic_shade_pasture_water_efficiency.yaml")
        self.registry = load_data(ROOT / "module_registries" / "micro_commons_default_v0.yaml")

    def test_technology_module_validates(self) -> None:
        self.assertTrue(validate_data(self.module, "technology-module").ok)
        self.assertTrue(validate_data(self.registry, "module-registry").ok)

    def test_pressure_test_preserves_dignity_floors_and_flags_modeling_gap(self) -> None:
        report = pressure_test_technology_module(self.plan, self.module)

        self.assertEqual(report["kind"], "TechnologyPressureTestReport")
        self.assertEqual(report["status"], "needs_modeling")
        self.assertTrue(report["dignity_floor_effect"]["safe_for_operator_iteration"])
        self.assertFalse(report["dignity_floor_effect"]["regressions"])
        self.assertTrue(any("survival-resource effect" in gap for gap in report["integration_gaps"]))
        self.assertTrue(validate_data(report, "technology-pressure-test").ok)

    def test_cli_technology_pressure_test_writes_report(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "technology_pressure.json"
            code = main(
                [
                    "technology-pressure-test",
                    str(GENERATED / "micro_commons_plan.json"),
                    str(ROOT / "tech_modules" / "agrivoltaic_shade_pasture_water_efficiency.yaml"),
                    "--output",
                    str(output),
                ]
            )

            self.assertEqual(code, 0)
            report = load_data(output)
            self.assertEqual(report["kind"], "TechnologyPressureTestReport")

    def test_module_compatibility_tracks_default_slots_and_research_backlog(self) -> None:
        report = evaluate_module_compatibility(self.plan, self.registry, [self.module])

        self.assertEqual(report["kind"], "ModuleCompatibilityReport")
        self.assertEqual(report["status"], "needs_research")
        slots = {slot["slot"]: slot for slot in report["slot_results"]}
        self.assertTrue(slots["food_production"]["default_posture_ready"])
        self.assertEqual(len(report["adapter_required"]), 1)
        self.assertEqual(report["adapter_required"][0]["module"], self.module["id"])
        self.assertTrue(report["research_backlog"])
        self.assertTrue(validate_data(report, "module-compatibility").ok)

    def test_cli_module_compatibility_writes_report(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "module_compatibility.json"
            code = main(
                [
                    "module-compatibility",
                    str(GENERATED / "micro_commons_plan.json"),
                    str(ROOT / "module_registries" / "micro_commons_default_v0.yaml"),
                    "--technology-module",
                    str(ROOT / "tech_modules" / "agrivoltaic_shade_pasture_water_efficiency.yaml"),
                    "--output",
                    str(output),
                ]
            )

            self.assertEqual(code, 0)
            report = load_data(output)
            self.assertEqual(report["kind"], "ModuleCompatibilityReport")

    def test_research_needs_emit_food_production_gap(self) -> None:
        report = generate_research_needs(self.plan, self.simulation, self.registry)

        self.assertEqual(report["kind"], "ResearchNeedReport")
        self.assertEqual(report["status"], "blocked_by_model_gap")
        self.assertEqual(report["needs"][0]["id"], "food_local_production_gap_v0")
        self.assertEqual(report["needs"][0]["module_slot"], "food_production")
        self.assertGreater(report["needs"][0]["target"]["required_delta_per_day"], 20)
        self.assertIn("controlled environment agriculture", " ".join(report["needs"][0]["search_queries"]))
        self.assertTrue(validate_data(report, "research-needs").ok)

    def test_cli_research_needs_writes_report(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "research_needs.json"
            code = main(
                [
                    "research-needs",
                    str(GENERATED / "micro_commons_plan.json"),
                    str(GENERATED / "micro_commons_simulation.json"),
                    "--module-registry",
                    str(ROOT / "module_registries" / "micro_commons_default_v0.yaml"),
                    "--output",
                    str(output),
                ]
            )

            self.assertEqual(code, 0)
            report = load_data(output)
            self.assertEqual(report["kind"], "ResearchNeedReport")

    def test_scalability_gate_blocks_module_without_edible_labor_interfaces(self) -> None:
        report = evaluate_scalability_gate(self.plan, self.module, self.registry)

        self.assertEqual(report["kind"], "ScalabilityGateReport")
        self.assertEqual(report["status"], "fail")
        self.assertFalse(report["passes_scalability_gate"])
        gates = {gate["id"]: gate for gate in report["gate_results"]}
        self.assertEqual(gates["dignity_floor_protection"]["status"], "pass")
        self.assertEqual(gates["evidence_traceability"]["status"], "pass")
        self.assertEqual(gates["scalable_interface"]["status"], "fail")
        self.assertEqual(gates["labor_visibility"]["status"], "fail")
        self.assertTrue(validate_data(report, "scalability-gate").ok)

    def test_cli_scalability_gate_writes_report_and_returns_fail_status(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "scalability_gate.json"
            code = main(
                [
                    "scalability-gate",
                    str(GENERATED / "micro_commons_plan.json"),
                    str(ROOT / "tech_modules" / "agrivoltaic_shade_pasture_water_efficiency.yaml"),
                    "--module-registry",
                    str(ROOT / "module_registries" / "micro_commons_default_v0.yaml"),
                    "--output",
                    str(output),
                ]
            )

            self.assertEqual(code, 1)
            report = load_data(output)
            self.assertEqual(report["kind"], "ScalabilityGateReport")

    def test_openai_draft_uses_api_key_and_web_search_tool(self) -> None:
        report = generate_research_needs(self.plan, self.simulation, self.registry)

        def fake_post(url: str, headers: dict[str, str], payload: dict[str, object], timeout_seconds: int) -> dict[str, object]:
            self.assertEqual(url, "https://api.openai.com/v1/responses")
            self.assertEqual(headers["Authorization"], "Bearer sk-test")
            self.assertEqual(payload["model"], "gpt-5.5")
            self.assertEqual(payload["tools"], [{"type": "web_search"}])
            self.assertIn("research_need", str(payload["input"]))
            self.assertEqual(timeout_seconds, 90)
            return {"output_text": json.dumps(_valid_drafted_module())}

        module = draft_technology_module(report, api_key="sk-test", post_json=fake_post)

        self.assertEqual(module["kind"], "TechnologyModule")
        self.assertEqual(module["status"], "draft")
        self.assertTrue(validate_data(module, "drafted-technology-module").ok)

    def test_openai_draft_requires_api_key(self) -> None:
        report = generate_research_needs(self.plan, self.simulation, self.registry)
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaises(OpenAIConfigurationError):
                draft_technology_module(report, include_web_search=False)

    def test_cli_draft_research_module_writes_valid_module(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            need_path = Path(tmp) / "research_needs.json"
            output = Path(tmp) / "drafted_module.json"
            need_path.write_text(json.dumps(generate_research_needs(self.plan, self.simulation, self.registry)), encoding="utf-8")

            def fake_post(url: str, headers: dict[str, str], payload: dict[str, object], timeout_seconds: int) -> dict[str, object]:
                self.assertEqual(headers["Authorization"], "Bearer sk-test")
                self.assertNotIn("tools", payload)
                return {"output": [{"content": [{"type": "output_text", "text": json.dumps(_valid_drafted_module())}]}]}

            with patch.dict(os.environ, {"OPENAI_API_KEY": "sk-test"}), patch("ciac.ai_research._post_json", side_effect=fake_post):
                code = main(["draft-research-module", str(need_path), "--no-web-search", "--output", str(output)])

            self.assertEqual(code, 0)
            module = load_data(output)
            self.assertEqual(module["kind"], "TechnologyModule")
            self.assertTrue(validate_data(module, "drafted-technology-module").ok)


def _valid_drafted_module() -> dict[str, object]:
    return {
        "kind": "TechnologyModule",
        "id": "draft_low_labor_food_production_v0",
        "name": "Draft Low-Labor Food Production Module",
        "domain": "food",
        "status": "draft",
        "provisional": True,
        "source_evidence": [
            {
                "id": "source_1",
                "citation": "Placeholder cited paper",
                "url": "https://example.org/paper",
                "notes": "Test fixture only.",
            }
        ],
        "performance_statistics": [
            {
                "id": "stat_1",
                "source_id": "source_1",
                "metric": "edible_servings_per_day",
                "value": "unknown",
                "uncertainty": "Not enough extracted evidence in test fixture.",
            }
        ],
        "applicability": ["Suitable for the food production slot after evidence review."],
        "modeled_impacts": ["No modeled numeric effect is accepted from this draft yet."],
        "integration_requirements": {
            "adapter": [
                "Extract edible-serving, water, energy, labor, land, skill, preservation, and failure-mode interfaces before optimization use."
            ]
        },
        "unknowns": {
            "review": [
                "This is an AI-assisted draft and must be reviewed against source evidence before it can affect CIaC optimization."
            ]
        },
    }


if __name__ == "__main__":
    unittest.main()
