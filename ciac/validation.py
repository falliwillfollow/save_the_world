from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from jsonschema import Draft7Validator

from .io import iter_data_files, load_data
from .models import ValidationIssue, ValidationReport


SCHEMA_BY_KIND = {
    "CivicPattern": "civic_pattern.schema.json",
    "SiteProfile": "site_profile.schema.json",
    "CompiledPlan": "compiled_plan.schema.json",
    "GateReport": "gate_report.schema.json",
    "SimulationRun": "simulation_run.schema.json",
    "Scenario": "scenario.schema.json",
    "ScenarioRun": "scenario_run.schema.json",
    "FoodPlan": "food_plan.schema.json",
    "NutritionReport": "nutrition_report.schema.json",
    "WaterPlan": "water_plan.schema.json",
    "WaterReport": "water_report.schema.json",
    "EnergyPlan": "energy_plan.schema.json",
    "EnergyReport": "energy_report.schema.json",
    "RolePlan": "role_plan.schema.json",
    "RoleReport": "role_report.schema.json",
    "AuditReport": "audit_report.schema.json",
    "RedesignReport": "redesign_report.schema.json",
    "ComparisonReport": "comparison_report.schema.json",
    "SimulationComparisonReport": "simulation_comparison_report.schema.json",
    "ReplayMatrixReport": "replay_matrix_report.schema.json",
    "MatrixRedesignReport": "matrix_redesign_report.schema.json",
    "PilotDossier": "pilot_dossier.schema.json",
    "ReviewRegister": "review_register.schema.json",
    "ReviewStatusReport": "review_status_report.schema.json",
    "SeasonalProfile": "seasonal_profile.schema.json",
    "HouseholdProfile": "household_profile.schema.json",
    "SpatialProfile": "spatial_profile.schema.json",
    "RuntimeBundle": "runtime_bundle.schema.json",
    "FoundationGateReport": "foundation_gate_report.schema.json",
    "OptimizationProfile": "optimization_profile.schema.json",
    "OptimizationReadinessReport": "optimization_readiness_report.schema.json",
    "CandidatePlanMatrixReport": "candidate_plan_matrix_report.schema.json",
    "ScaleProfile": "scale_profile.schema.json",
    "TradeoffScaleReport": "tradeoff_scale_report.schema.json",
    "OptimizerReport": "optimizer_report.schema.json",
    "VisualizationBundle": "visualization_bundle.schema.json",
    "SearchOptimizerReport": "search_optimizer_report.schema.json",
    "ObjectiveCalibrationProfile": "objective_calibration_profile.schema.json",
    "ObjectiveCalibrationReport": "objective_calibration_report.schema.json",
    "WeightGovernanceProfile": "weight_governance_profile.schema.json",
    "WeightGovernanceReport": "weight_governance_report.schema.json",
    "CycleIterationReport": "cycle_iteration_report.schema.json",
    "TechnologyModule": "technology_module.schema.json",
    "TechnologyPressureTestReport": "technology_pressure_test_report.schema.json",
    "ModuleRegistry": "module_registry.schema.json",
    "ModuleCompatibilityReport": "module_compatibility_report.schema.json",
}


def schema_dir() -> Path:
    return Path(__file__).resolve().parent.parent / "schemas"


def load_schema(kind: str) -> dict[str, Any]:
    filename = SCHEMA_BY_KIND.get(kind)
    if filename is None:
        raise ValueError(f"Unsupported kind: {kind}")
    return json.loads((schema_dir() / filename).read_text(encoding="utf-8"))


def validate_data(data: dict[str, Any], path: str = "<memory>") -> ValidationReport:
    kind = data.get("kind")
    report = ValidationReport(path=path)
    if not isinstance(kind, str):
        report.issues.append(ValidationIssue("error", "Missing string field: kind"))
        return report
    if kind not in SCHEMA_BY_KIND:
        report.issues.append(ValidationIssue("error", f"Unsupported kind: {kind}", "$.kind"))
        return report

    validator = Draft7Validator(load_schema(kind))
    for error in sorted(validator.iter_errors(data), key=lambda e: list(e.path)):
        json_path = "$" + "".join(f"[{part!r}]" if isinstance(part, int) else f".{part}" for part in error.path)
        report.issues.append(ValidationIssue("error", error.message, json_path))

    if kind == "CivicPattern":
        report.issues.extend(_validate_pattern_semantics(data))

    return report


def validate_path(path: str | Path) -> list[ValidationReport]:
    reports: list[ValidationReport] = []
    for data_file in iter_data_files(path):
        try:
            reports.append(validate_data(load_data(data_file), str(data_file)))
        except Exception as exc:  # Keep CLI validation useful across many files.
            reports.append(ValidationReport(str(data_file), [ValidationIssue("error", str(exc))]))
    return reports


def validate_pattern_library(patterns: list[dict[str, Any]]) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    ids = [pattern.get("id") for pattern in patterns]
    duplicate_ids = sorted({pattern_id for pattern_id in ids if ids.count(pattern_id) > 1})
    for pattern_id in duplicate_ids:
        issues.append(ValidationIssue("error", f"Duplicate pattern id: {pattern_id}", "$.id"))

    known_ids = {pattern.get("id") for pattern in patterns}
    for pattern in patterns:
        pattern_id = pattern.get("id", "<unknown>")
        for index, dep in enumerate(pattern.get("dependencies", [])):
            if dep.get("kind") == "pattern" and dep.get("id") not in known_ids:
                issues.append(
                    ValidationIssue(
                        "error",
                        f"Pattern {pattern_id} references unknown pattern dependency: {dep.get('id')}",
                        f"$.dependencies[{index}]",
                    )
                )
    return issues


def _validate_pattern_semantics(pattern: dict[str, Any]) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    metrics = pattern.get("metrics", {})
    governance = pattern.get("governance", {})
    lifecycle = pattern.get("lifecycle", {})

    if not pattern.get("failure_modes"):
        issues.append(ValidationIssue("error", "Civic patterns must declare failure modes", "$.failure_modes"))
    if not lifecycle.get("maintenance"):
        issues.append(ValidationIssue("error", "Civic patterns must declare maintenance tasks", "$.lifecycle.maintenance"))
    if not lifecycle.get("inspection_points"):
        issues.append(ValidationIssue("error", "Civic patterns must declare inspection points", "$.lifecycle.inspection_points"))

    if governance.get("owner") == "commons":
        for field_name in ("stewardship_role", "backup_role", "audit_frequency", "capture_risk"):
            if not governance.get(field_name):
                issues.append(
                    ValidationIssue(
                        "error",
                        f"Commons-owned patterns must declare governance.{field_name}",
                        f"$.governance.{field_name}",
                    )
                )

    for field_name in ("build_labor_hours", "recurring_labor_hours_per_week", "maintenance_burden"):
        value = metrics.get(field_name)
        if not isinstance(value, (int, float)):
            issues.append(ValidationIssue("error", f"metrics.{field_name} must be numeric", f"$.metrics.{field_name}"))

    sensitive_tags = {"engineering", "legal", "health", "water", "sanitation", "structural", "electrical"}
    tags = set(pattern.get("provisional_for", []))
    if pattern.get("provisional") is not True or not sensitive_tags.intersection(tags):
        issues.append(
            ValidationIssue(
                "warning",
                "Seed patterns should be marked provisional for any unsourced safety/legal/engineering assumptions",
                "$.provisional_for",
            )
        )

    return issues
