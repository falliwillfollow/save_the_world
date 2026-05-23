from __future__ import annotations

from pathlib import Path
from typing import Any

from .io import load_data
from .validation import validate_data


DEFAULT_VIEWER_ARTIFACTS = {
    "runtime_bundle": ("micro_commons_runtime_bundle.json", "RuntimeBundle"),
    "foundation_gate": ("micro_commons_foundation_gate.json", "FoundationGateReport"),
    "search_optimizer": ("micro_commons_search_optimizer_report.json", "SearchOptimizerReport"),
    "objective_calibration": ("micro_commons_objective_calibration.json", "ObjectiveCalibrationReport"),
    "weight_governance": ("micro_commons_weight_governance.json", "WeightGovernanceReport"),
    "cycle_iteration": ("micro_commons_cycle_iteration.json", "CycleIterationReport"),
    "food_autonomy": ("micro_commons_food_autonomy_report.json", "FoodAutonomyReport"),
    "food_labor": ("micro_commons_food_labor_report.json", "FoodLaborReport"),
    "complexity": ("micro_commons_complexity_report.json", "ComplexityReport"),
    "node_scaling": ("micro_commons_node_scaling.json", "InfrastructureNodeReport"),
    "topology_recommendation": ("micro_commons_topology_recommendation.json", "TopologyRecommendationReport"),
    "viewer_run": ("micro_commons_viewer_session_report.json", "ViewerRunReport"),
}


def evaluate_artifact_cohesion(generated_dir: str | Path) -> dict[str, Any]:
    root = Path(generated_dir)
    loaded: dict[str, dict[str, Any]] = {}
    artifact_checks = []
    relationship_checks = []

    for name, (filename, expected_kind) in DEFAULT_VIEWER_ARTIFACTS.items():
        path = root / filename
        if not path.exists():
            artifact_checks.append(_check(f"{name}_exists", "fail", f"Missing default viewer artifact: {filename}", [filename]))
            continue
        try:
            data = load_data(path)
        except Exception as exc:
            artifact_checks.append(_check(f"{name}_loads", "fail", f"Could not load {filename}: {exc}", [filename]))
            continue
        loaded[name] = data
        kind = data.get("kind")
        artifact_checks.append(
            _check(
                f"{name}_kind",
                "pass" if kind == expected_kind else "fail",
                f"{filename} kind is {kind}; expected {expected_kind}.",
                [filename],
            )
        )
        validation = validate_data(data, str(path))
        artifact_checks.append(
            _check(
                f"{name}_validates",
                "pass" if validation.ok else "fail",
                f"{filename} validates." if validation.ok else _validation_message(filename, validation),
                [filename],
            )
        )

    relationship_checks.extend(_optimizer_cycle_checks(loaded))
    relationship_checks.extend(_food_autonomy_checks(loaded))
    relationship_checks.extend(_node_topology_checks(loaded))
    relationship_checks.extend(_viewer_run_checks(loaded))
    relationship_checks.extend(_run_configuration_checks(loaded))
    relationship_checks.extend(_duplicate_topology_checks(root, loaded.get("topology_recommendation")))

    checks = artifact_checks + relationship_checks
    status = _status(checks)
    active_population = _active_population(loaded)
    return {
        "kind": "ArtifactCohesionReport",
        "id": f"{root.name}_viewer_artifact_cohesion",
        "generated_by": "ciac.artifact_cohesion.v0",
        "provisional": True,
        "status": status,
        "generated_dir": str(root),
        "active_population": active_population,
        "summary": {
            "artifact_count": len(DEFAULT_VIEWER_ARTIFACTS),
            "pass_count": sum(1 for check in checks if check["status"] == "pass"),
            "warn_count": sum(1 for check in checks if check["status"] == "warn"),
            "fail_count": sum(1 for check in checks if check["status"] == "fail"),
            "provisional": True,
        },
        "artifact_checks": artifact_checks,
        "relationship_checks": relationship_checks,
        "recommendations": _recommendations(checks),
        "unknowns": [
            "The viewer reads generated JSON artifacts; completed webapp years regenerate backend artifacts when served through ciac viewer-server.",
            "When served through ciac viewer-server, completed webapp years regenerate the CycleIterationReport from the UI run context.",
            "Population-specific reports should consume the latest webapp run population; non-population reports should be treated as explicit dependency context.",
        ],
    }


def _optimizer_cycle_checks(loaded: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    checks = []
    search = loaded.get("search_optimizer")
    cycle = loaded.get("cycle_iteration")
    calibration = loaded.get("objective_calibration")
    weights = loaded.get("weight_governance")
    if search:
        selected = search.get("selected_candidate")
        candidate_ids = {candidate.get("id") for candidate in search.get("top_candidates", [])}
        checks.append(
            _check(
                "search_selected_candidate_present",
                "pass" if selected in candidate_ids else "fail",
                f"Search selected candidate {selected} is present in top_candidates.",
                ["micro_commons_search_optimizer_report.json"],
            )
        )
    if search and cycle:
        checks.append(
            _check(
                "cycle_selected_candidate_matches_search",
                "pass" if cycle.get("selected_candidate") == search.get("selected_candidate") else "fail",
                f"Cycle selected candidate {cycle.get('selected_candidate')} matches search selected candidate {search.get('selected_candidate')}.",
                ["micro_commons_cycle_iteration.json", "micro_commons_search_optimizer_report.json"],
            )
        )
        checks.append(
            _check(
                "cycle_has_applied_runtime_bundle",
                "pass" if cycle.get("runtime_bundle", {}).get("kind") == "RuntimeBundle" else "fail",
                "CycleIterationReport contains the applied RuntimeBundle used by Next Cycle.",
                ["micro_commons_cycle_iteration.json"],
            )
        )
        checks.append(
            _check(
                "cycle_has_next_search_report",
                "pass" if cycle.get("next_search_optimizer_report", {}).get("kind") == "SearchOptimizerReport" else "fail",
                "CycleIterationReport contains the next SearchOptimizerReport.",
                ["micro_commons_cycle_iteration.json"],
            )
        )
    if search and calibration:
        checks.append(
            _check(
                "calibration_targets_search_report",
                "pass" if calibration.get("search_optimizer_report") == search.get("id") else "fail",
                f"Objective calibration targets search report {search.get('id')}.",
                ["micro_commons_objective_calibration.json", "micro_commons_search_optimizer_report.json"],
            )
        )
    if search and calibration and weights:
        checks.append(
            _check(
                "weight_governance_targets_calibration",
                "pass" if weights.get("objective_calibration_report") == calibration.get("id") else "fail",
                f"Weight governance targets calibration report {calibration.get('id')}.",
                ["micro_commons_weight_governance.json", "micro_commons_objective_calibration.json"],
            )
        )
        checks.append(
            _check(
                "weight_governance_targets_optimizer_profile",
                "pass" if weights.get("optimization_profile") == search.get("optimization_profile") else "fail",
                f"Weight governance profile {weights.get('optimization_profile')} matches search profile {search.get('optimization_profile')}.",
                ["micro_commons_weight_governance.json", "micro_commons_search_optimizer_report.json"],
            )
        )
    return checks


def _food_autonomy_checks(loaded: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    checks = []
    cycle = loaded.get("cycle_iteration")
    food_autonomy = loaded.get("food_autonomy")
    if not cycle or not food_autonomy:
        return checks
    checks.append(
        _check(
            "food_autonomy_sources_cycle_iteration",
            "pass" if food_autonomy.get("source_cycle_iteration") == cycle.get("id") else "fail",
            f"Food autonomy source cycle is {food_autonomy.get('source_cycle_iteration')}; expected {cycle.get('id')}.",
            ["micro_commons_food_autonomy_report.json", "micro_commons_cycle_iteration.json"],
        )
    )
    checks.append(
        _check(
            "food_autonomy_population_matches_cycle",
            "pass" if int(food_autonomy.get("population", -1)) == int(cycle.get("viewer_population_context", {}).get("population", -2)) else "fail",
            f"Food autonomy population {food_autonomy.get('population')} matches cycle population {cycle.get('viewer_population_context', {}).get('population')}.",
            ["micro_commons_food_autonomy_report.json", "micro_commons_cycle_iteration.json"],
        )
    )
    return checks


def _node_topology_checks(loaded: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    checks = []
    node = loaded.get("node_scaling")
    topology = loaded.get("topology_recommendation")
    if not node or not topology:
        return checks
    population = int(topology.get("population", 0))
    targets = {int(target.get("people", 0)): target for target in node.get("target_results", [])}
    target = targets.get(population)
    checks.append(
        _check(
            "topology_population_has_node_target",
            "pass" if target else "fail",
            f"Topology population {population} has a matching node-scaling target.",
            ["micro_commons_topology_recommendation.json", "micro_commons_node_scaling.json"],
        )
    )
    checks.append(
        _check(
            "topology_sources_node_report",
            "pass" if topology.get("source_reports", {}).get("node_scaling") == node.get("id") else "fail",
            f"Topology source node report is {topology.get('source_reports', {}).get('node_scaling')}; expected {node.get('id')}.",
            ["micro_commons_topology_recommendation.json", "micro_commons_node_scaling.json"],
        )
    )
    food_labor = loaded.get("food_labor")
    complexity = loaded.get("complexity")
    if food_labor:
        checks.append(
            _check(
                "topology_sources_food_labor_report",
                "pass" if topology.get("source_reports", {}).get("food_labor") == food_labor.get("id") else "fail",
                f"Topology source food labor report is {topology.get('source_reports', {}).get('food_labor')}; expected {food_labor.get('id')}.",
                ["micro_commons_topology_recommendation.json", "micro_commons_food_labor_report.json"],
            )
        )
    if complexity:
        checks.append(
            _check(
                "topology_sources_complexity_report",
                "pass" if topology.get("source_reports", {}).get("complexity") == complexity.get("id") else "fail",
                f"Topology source complexity report is {topology.get('source_reports', {}).get('complexity')}; expected {complexity.get('id')}.",
                ["micro_commons_topology_recommendation.json", "micro_commons_complexity_report.json"],
            )
        )
    if target:
        checks.append(
            _check(
                "topology_total_nodes_match_node_scaling",
                "pass" if int(topology.get("node_summary", {}).get("total_desired_nodes", -1)) == int(target.get("total_desired_nodes", -2)) else "fail",
                f"Topology total nodes {topology.get('node_summary', {}).get('total_desired_nodes')} match node-scaling total {target.get('total_desired_nodes')}.",
                ["micro_commons_topology_recommendation.json", "micro_commons_node_scaling.json"],
            )
        )
        checks.append(
            _check(
                "topology_replicated_slots_match_node_scaling",
                "pass" if int(topology.get("node_summary", {}).get("replicated_slot_count", -1)) == int(target.get("replicated_slot_count", -2)) else "fail",
                f"Topology replicated slots {topology.get('node_summary', {}).get('replicated_slot_count')} match node-scaling replicated slots {target.get('replicated_slot_count')}.",
                ["micro_commons_topology_recommendation.json", "micro_commons_node_scaling.json"],
            )
        )
    return checks


def _run_configuration_checks(loaded: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    checks = []
    population = _active_population(loaded)
    if population <= 0:
        return checks
    food_labor = loaded.get("food_labor")
    if food_labor:
        targets = {int(target.get("target_population", 0)) for target in food_labor.get("scaling_results", [])}
        checks.append(
            _check(
                "food_labor_has_active_population_row",
                "pass" if population in targets else "warn",
                f"Food labor scaling_results {'include' if population in targets else 'do not include'} the active webapp population {population}.",
                ["micro_commons_food_labor_report.json", "micro_commons_viewer_session_report.json"],
            )
        )
    complexity = loaded.get("complexity")
    if complexity:
        registry_ids = {
            loaded.get("node_scaling", {}).get("module_registry"),
            food_labor.get("module_registry") if food_labor else None,
            complexity.get("module_registry"),
        }
        registry_ids.discard(None)
        registry_ids.discard("")
        checks.append(
            _check(
                "complexity_uses_same_registry_context",
                "pass" if len(registry_ids) <= 1 else "fail",
                f"Complexity, node-scaling, and food-labor reports use registry context: {', '.join(sorted(registry_ids)) or 'unknown'}.",
                [
                    "micro_commons_complexity_report.json",
                    "micro_commons_node_scaling.json",
                    "micro_commons_food_labor_report.json",
                ],
            )
        )
    return checks


def _viewer_run_checks(loaded: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    checks = []
    viewer = loaded.get("viewer_run")
    if not viewer:
        return checks
    runs = viewer.get("runs", [])
    if not runs:
        checks.append(
            _check(
                "viewer_run_report_has_no_runs",
                "pass",
                "ViewerRunReport exists but no completed webapp runs have been recorded.",
                ["micro_commons_viewer_session_report.json"],
            )
        )
        return checks
    latest = runs[-1]
    population = int(latest.get("population", 0))
    node = loaded.get("node_scaling")
    topology = loaded.get("topology_recommendation")
    checks.append(
        _check(
            "viewer_run_population_matches_topology",
            "pass" if topology and int(topology.get("population", -1)) == population else "warn",
            f"Latest webapp run population is {population}; canonical topology population is {topology.get('population') if topology else 'missing'}.",
            ["micro_commons_viewer_session_report.json", "micro_commons_topology_recommendation.json"],
        )
    )
    if node:
        targets = {int(target.get("people", 0)): target for target in node.get("target_results", [])}
        target = targets.get(population)
        checks.append(
            _check(
                "viewer_run_population_has_node_target",
                "pass" if target else "warn",
                f"Latest webapp run population {population} {'has' if target else 'does not have'} a persisted node-scaling target.",
                ["micro_commons_viewer_session_report.json", "micro_commons_node_scaling.json"],
            )
        )
        if target:
            checks.append(
                _check(
                    "viewer_run_nodes_match_node_scaling",
                    "pass" if int(latest.get("total_nodes", -1)) == int(target.get("total_desired_nodes", -2)) else "warn",
                    f"Latest webapp run nodes {latest.get('total_nodes')} compare with persisted node-scaling total {target.get('total_desired_nodes')}.",
                    ["micro_commons_viewer_session_report.json", "micro_commons_node_scaling.json"],
                )
            )
    return checks


def _duplicate_topology_checks(root: Path, topology: dict[str, Any] | None) -> list[dict[str, Any]]:
    if not topology:
        return []
    extras = sorted(path.name for path in root.glob("micro_commons_topology_recommendation_*.json"))
    if not extras:
        return [_check("extra_topology_reports_absent", "pass", "No non-canonical topology recommendation artifacts are present.", [])]
    return [
        _check(
            "extra_topology_reports_absent",
            "warn",
            f"Non-canonical topology recommendation artifacts are present: {', '.join(extras)}.",
            extras,
        )
    ]


def _active_population(loaded: dict[str, dict[str, Any]]) -> int:
    viewer = loaded.get("viewer_run")
    if viewer and viewer.get("runs"):
        return int(viewer["runs"][-1].get("population", 0))
    topology = loaded.get("topology_recommendation")
    if topology and topology.get("population"):
        return int(topology["population"])
    node = loaded.get("node_scaling")
    if node:
        targets = node.get("target_results", [])
        ad_hoc = [target for target in targets if "ad hoc" in str(target.get("notes", "")).lower()]
        if ad_hoc:
            return int(ad_hoc[-1]["people"])
    return 0


def _validation_message(filename: str, validation: Any) -> str:
    details = "; ".join(f"{issue.path}: {issue.message}" for issue in validation.issues[:5])
    return f"{filename} failed schema validation: {details}"


def _check(identifier: str, status: str, message: str, artifacts: list[str]) -> dict[str, Any]:
    return {
        "id": identifier,
        "status": status,
        "message": message,
        "artifacts": artifacts,
        "provisional": True,
    }


def _status(checks: list[dict[str, Any]]) -> str:
    if any(check["status"] == "fail" for check in checks):
        return "not_ready"
    if any(check["status"] == "warn" for check in checks):
        return "ready_with_warnings"
    return "coherent"


def _recommendations(checks: list[dict[str, Any]]) -> list[str]:
    recommendations = [
        "Run artifact-cohesion after regenerating viewer-facing reports.",
        "Treat examples/generated/micro_commons_topology_recommendation.json as the canonical topology log for the active population.",
        "Use ciac viewer-server for browser runs so population-specific backend reports are regenerated from the same configured state.",
    ]
    if any(check["id"] == "extra_topology_reports_absent" and check["status"] == "warn" for check in checks):
        recommendations.append("Remove or archive non-canonical topology recommendation files once their population is promoted to the default report.")
    if any(check["id"].startswith("viewer_run_") and check["status"] == "warn" for check in checks):
        recommendations.append("Replay the latest browser run through ciac viewer-server so node-scaling, food-labor, topology, and cohesion share the same population.")
    if any(check["id"] == "food_labor_has_active_population_row" and check["status"] == "warn" for check in checks):
        recommendations.append("Regenerate food labor through the viewer pipeline before trusting topology recommendations for the active population.")
    if any(check["status"] == "fail" for check in checks):
        recommendations.append("Regenerate the failing upstream report before trusting the static viewer state.")
    return recommendations
