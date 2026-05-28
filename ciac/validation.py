from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from jsonschema import Draft7Validator

from .io import iter_data_files, load_data
from .models import ValidationIssue, ValidationReport


SCHEMA_BY_KIND = {
    "CivicPattern": "civic_pattern.schema.json",
    "CapabilityState": "capability_state.schema.json",
    "CapabilityGateReport": "capability_gate_report.schema.json",
    "SiteProfile": "site_profile.schema.json",
    "CompiledPlan": "compiled_plan.schema.json",
    "GateReport": "gate_report.schema.json",
    "SimulationRun": "simulation_run.schema.json",
    "Scenario": "scenario.schema.json",
    "ScenarioRun": "scenario_run.schema.json",
    "FoodPlan": "food_plan.schema.json",
    "FoodLaborReport": "food_labor_report.schema.json",
    "FoodAutonomyReport": "food_autonomy_report.schema.json",
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
    "InfrastructureNodeReport": "infrastructure_node_report.schema.json",
    "SpatialProfile": "spatial_profile.schema.json",
    "RuntimeBundle": "runtime_bundle.schema.json",
    "CivicFloorWorldManifest": "world_manifest.schema.json",
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
    "ResearchNeedReport": "research_need_report.schema.json",
    "ScalabilityGateReport": "scalability_gate_report.schema.json",
    "ModuleImplementationReport": "module_implementation_report.schema.json",
    "ComplexityReport": "complexity_report.schema.json",
    "TopologyRecommendationReport": "topology_recommendation_report.schema.json",
    "ArtifactCohesionReport": "artifact_cohesion_report.schema.json",
    "ViewerRunReport": "viewer_run_report.schema.json",
    "DiscoveryCandidateIntervention": "discovery_candidate_intervention.schema.json",
    "DiscoveryLoopReport": "discovery_loop_report.schema.json",
    "PatchProposal": "patch_proposal.schema.json",
    "PatchMaterializationReport": "patch_materialization_report.schema.json",
    "PatchImpactReport": "patch_impact_report.schema.json",
    "PatchPromotionReport": "patch_promotion_report.schema.json",
    "ResearchLoopRun": "research_loop_run.schema.json",
    "ScalingPolicy": "scaling_policy.schema.json",
    "CapabilityPolicy": "capability_policy.schema.json",
    "CapabilityPolicyGateReport": "capability_policy_gate_report.schema.json",
    "CapabilityScenario": "capability_scenario.schema.json",
    "ResearchRegistry": "research_registry.schema.json",
    "LifeManifest": "life_manifest.schema.json",
    "AutomationManifest": "automation_manifest.schema.json",
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
    if kind == "ModuleRegistry":
        report.issues.extend(_validate_module_registry_semantics(data))
    if kind == "CapabilityPolicy":
        report.issues.extend(_validate_capability_policy_semantics(data))

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


def _validate_module_registry_semantics(registry: dict[str, Any]) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    bundles = registry.get("interface_bundles", {})
    bundle_ids = set(bundles)
    slots = registry.get("slots", [])
    slot_ids = [slot.get("id") for slot in slots]
    duplicate_slot_ids = sorted({slot_id for slot_id in slot_ids if slot_ids.count(slot_id) > 1})
    for slot_id in duplicate_slot_ids:
        issues.append(ValidationIssue("error", f"Duplicate module slot id: {slot_id}", "$.slots"))

    tier_slots = set()
    for tier_id, tier_slot_ids in registry.get("module_tiers", {}).items():
        if not isinstance(tier_slot_ids, list):
            continue
        for slot_id in tier_slot_ids:
            if slot_id not in slot_ids:
                issues.append(
                    ValidationIssue(
                        "error",
                        f"Module tier {tier_id} references unknown slot: {slot_id}",
                        "$.module_tiers",
                    )
                )
            tier_slots.add(slot_id)

    for index, slot in enumerate(slots):
        for bundle_id in slot.get("required_interface_bundles", []):
            if bundle_id not in bundle_ids:
                issues.append(
                    ValidationIssue(
                        "error",
                        f"Slot {slot.get('id', '<unknown>')} references unknown interface bundle: {bundle_id}",
                        f"$.slots[{index}].required_interface_bundles",
                    )
                )
        node_policy = slot.get("node_policy")
        if isinstance(node_policy, dict):
            minimum = node_policy.get("minimum_population_per_node")
            preferred = node_policy.get("preferred_population_per_node")
            maximum = node_policy.get("maximum_population_per_node")
            if all(isinstance(value, int) for value in (minimum, preferred, maximum)):
                if not minimum <= preferred <= maximum:
                    issues.append(
                        ValidationIssue(
                            "error",
                            f"Slot {slot.get('id', '<unknown>')} node_policy must satisfy minimum <= preferred <= maximum",
                            f"$.slots[{index}].node_policy",
                        )
                    )
    unclassified = sorted(slot_id for slot_id in slot_ids if slot_id not in tier_slots)
    if unclassified:
        issues.append(
            ValidationIssue(
                "warning",
                f"Module slots are not assigned to a tier: {', '.join(unclassified)}",
                "$.module_tiers",
            )
        )

    return issues


def _validate_capability_policy_semantics(policy: dict[str, Any]) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    source_ids = [source.get("id") for source in policy.get("source_registry", [])]
    duplicate_sources = sorted({source_id for source_id in source_ids if source_ids.count(source_id) > 1})
    for source_id in duplicate_sources:
        issues.append(ValidationIssue("error", f"Duplicate source id: {source_id}", "$.source_registry"))
    source_id_set = set(source_ids)
    gate_ids: list[str] = []
    for domain, domain_policy in policy.get("domains", {}).items():
        for gate_index, gate in enumerate(domain_policy.get("gates", [])):
            gate_id = gate.get("gate_id")
            gate_ids.append(gate_id)
            for source_id in gate.get("source_ids", []):
                if source_id not in source_id_set:
                    issues.append(
                        ValidationIssue(
                            "error",
                            f"Gate {gate_id} references unknown source id: {source_id}",
                            f"$.domains.{domain}.gates[{gate_index}].source_ids",
                        )
                    )
    duplicate_gates = sorted({gate_id for gate_id in gate_ids if gate_ids.count(gate_id) > 1})
    for gate_id in duplicate_gates:
        issues.append(ValidationIssue("error", f"Duplicate gate id: {gate_id}", "$.domains"))
    return issues
