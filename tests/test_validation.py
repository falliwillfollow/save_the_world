from __future__ import annotations

import copy
import unittest
from pathlib import Path

from ciac.io import load_data
from ciac.validation import validate_data, validate_pattern_library


ROOT = Path(__file__).resolve().parents[1]


class ValidationTests(unittest.TestCase):
    def test_seed_pattern_is_valid(self) -> None:
        pattern = load_data(ROOT / "patterns" / "starter_dwelling.yaml")
        report = validate_data(pattern, "starter_dwelling")
        self.assertTrue(report.ok, [issue.message for issue in report.issues])

    def test_seed_seasonal_profile_is_valid(self) -> None:
        profile = load_data(ROOT / "seasonal_profiles" / "humid_temperate_provisional.yaml")
        report = validate_data(profile, "humid_temperate_provisional")
        self.assertTrue(report.ok, [issue.message for issue in report.issues])

    def test_seed_household_profile_is_valid(self) -> None:
        profile = load_data(ROOT / "household_profiles" / "micro_commons_households_v0.yaml")
        report = validate_data(profile, "micro_commons_households_v0")
        self.assertTrue(report.ok, [issue.message for issue in report.issues])

    def test_seed_spatial_profile_is_valid(self) -> None:
        profile = load_data(ROOT / "spatial_profiles" / "micro_commons_spatial_v0.yaml")
        report = validate_data(profile, "micro_commons_spatial_v0")
        self.assertTrue(report.ok, [issue.message for issue in report.issues])

    def test_missing_lifecycle_fails(self) -> None:
        pattern = load_data(ROOT / "patterns" / "starter_dwelling.yaml")
        broken = copy.deepcopy(pattern)
        broken.pop("lifecycle")
        report = validate_data(broken, "broken")
        self.assertFalse(report.ok)
        self.assertTrue(any("lifecycle" in issue.message or "lifecycle" in issue.path for issue in report.issues))

    def test_missing_governance_field_fails_for_commons_pattern(self) -> None:
        pattern = load_data(ROOT / "patterns" / "well_house.yaml")
        broken = copy.deepcopy(pattern)
        broken["governance"]["backup_role"] = ""
        report = validate_data(broken, "broken")
        self.assertFalse(report.ok)
        self.assertTrue(any("backup_role" in issue.message or "backup_role" in issue.path for issue in report.issues))

    def test_broken_pattern_dependency_fails_library_validation(self) -> None:
        pattern = load_data(ROOT / "patterns" / "starter_dwelling.yaml")
        broken = copy.deepcopy(pattern)
        broken["dependencies"][0]["id"] = "missing_sanitation_stack"
        issues = validate_pattern_library([broken])
        self.assertTrue(any("unknown pattern dependency" in issue.message for issue in issues))


if __name__ == "__main__":
    unittest.main()
