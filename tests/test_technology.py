from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from ciac.cli import main
from ciac.io import load_data
from ciac.technology import evaluate_module_compatibility, pressure_test_technology_module
from ciac.validation import validate_data


ROOT = Path(__file__).resolve().parents[1]
GENERATED = ROOT / "examples" / "generated"


class TechnologyModuleTests(unittest.TestCase):
    def setUp(self) -> None:
        self.plan = load_data(GENERATED / "micro_commons_plan.json")
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


if __name__ == "__main__":
    unittest.main()
