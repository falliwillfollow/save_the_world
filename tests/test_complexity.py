import tempfile
import unittest
from pathlib import Path

from ciac.cli import main
from ciac.compiler import load_patterns
from ciac.complexity import generate_complexity_report
from ciac.io import load_data
from ciac.validation import validate_data


ROOT = Path(__file__).resolve().parents[1]


class ComplexityReportTests(unittest.TestCase):
    def setUp(self) -> None:
        self.registry = load_data(ROOT / "module_registries" / "micro_commons_default_v0.yaml")
        self.patterns = load_patterns(ROOT / "patterns")

    def test_registry_declares_reusable_interface_bundles_and_tiers(self) -> None:
        report = validate_data(self.registry, "module-registry")

        self.assertTrue(report.ok, [issue.message for issue in report.issues])
        self.assertIn("labor_visibility", self.registry["interface_bundles"])
        self.assertIn("scenario_resilience", self.registry["interface_bundles"])
        self.assertIn("risk_resilience", self.registry["module_tiers"]["meta_systems"])
        risk = next(slot for slot in self.registry["slots"] if slot["id"] == "risk_resilience")
        self.assertIn("scenario_resilience", risk["required_interface_bundles"])

    def test_complexity_report_surfaces_registry_and_pattern_hotspots(self) -> None:
        report = generate_complexity_report(self.registry, self.patterns)

        self.assertEqual(report["kind"], "ComplexityReport")
        self.assertEqual(report["status"], "needs_simplification")
        self.assertEqual(report["registry_summary"]["slot_count"], 14)
        self.assertGreater(report["registry_summary"]["direct_required_interface_entries"], 600)
        self.assertEqual(report["registry_summary"]["bundle_count"], 7)
        self.assertIn("floor_systems", report["registry_summary"]["tiers"])
        slot_results = {slot["slot"]: slot for slot in report["slot_results"]}
        self.assertEqual(slot_results["risk_resilience"]["tier"], "meta_systems")
        self.assertGreater(slot_results["materials_fabrication"]["direct_required_interfaces"], 70)
        self.assertTrue(any(hotspot["subject"] == "materials_fabrication" for hotspot in report["hotspots"]))
        self.assertTrue(validate_data(report, "complexity-report").ok)

    def test_cli_complexity_report_writes_report(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "complexity_report.json"
            code = main(
                [
                    "complexity-report",
                    str(ROOT / "module_registries" / "micro_commons_default_v0.yaml"),
                    str(ROOT / "patterns"),
                    "--output",
                    str(output),
                ]
            )

            self.assertEqual(code, 0)
            report = load_data(output)
            self.assertEqual(report["kind"], "ComplexityReport")
            self.assertEqual(report["module_registry"], "micro_commons_default_v0")


if __name__ == "__main__":
    unittest.main()
