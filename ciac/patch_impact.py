from __future__ import annotations

import copy
from pathlib import Path
from typing import Any

from .io import load_data, write_json
from .runtime_export import build_runtime_bundle
from .scenarios import run_scenario
from .simulation import simulate
from .simulation_compare import compare_simulations
from .validation import validate_data
from .viewer_cycle_pipeline import _materialize_active_patterns
from .world_manifest import build_world_manifest


GENERATED_DIR = Path("examples/generated")
WORLD_MANIFEST_PATH = Path("examples/world_manifests/civic_floor_80_v0.world.json")
DEFAULT_COMPILED_PLAN_PATH = GENERATED_DIR / "micro_commons_plan.json"
DEFAULT_SIMULATION_PATH = GENERATED_DIR / "micro_commons_simulation.json"
DEFAULT_RUNTIME_BUNDLE_PATH = GENERATED_DIR / "micro_commons_runtime_bundle.json"
DEFAULT_SCENARIO_PATHS = [
    Path("scenarios/water_contamination_response_v2.yaml"),
    Path("scenarios/crop_failure.yaml"),
    Path("scenarios/energy_outage_reserve_v2.yaml"),
]


def analyze_materialized_patch(
    materialization: dict[str, Any],
    *,
    repo_root: str | Path = ".",
    compiled_plan_path: str | Path = DEFAULT_COMPILED_PLAN_PATH,
    days: int = 365,
    scenario_paths: list[str | Path] | None = None,
    report_output: str | Path | None = None,
) -> dict[str, Any]:
    root = Path(repo_root).resolve()
    mat_validation = validate_data(materialization, materialization.get("id", "<materialization>"))
    if not mat_validation.ok or materialization.get("status") != "materialized_draft":
        return _blocked_impact(materialization, _validation_messages(mat_validation) or ["Materialization is not a materialized draft."])

    pattern_path = _resolve(root, materialization["materialized_artifact_path"])
    pattern = load_data(pattern_path)
    pattern_validation = validate_data(pattern, str(pattern_path))
    if not pattern_validation.ok:
        return _blocked_impact(materialization, _validation_messages(pattern_validation))

    plan_path = _resolve(root, compiled_plan_path)
    baseline_plan = load_data(plan_path)
    candidate_plan = apply_pattern_to_compiled_plan(baseline_plan, pattern)
    review_status = _optional_load(root / GENERATED_DIR / "micro_commons_review_status.json")

    baseline_sim = simulate(baseline_plan, days=int(days), review_status=review_status)
    candidate_sim = simulate(candidate_plan, days=int(days), review_status=review_status)
    normal_comparison = compare_simulations(baseline_sim, candidate_sim)

    scenario_results = []
    for scenario_path in _scenario_paths(root, scenario_paths):
        scenario = load_data(scenario_path)
        baseline_scenario = simulate(baseline_plan, days=int(scenario["days"]), review_status=review_status, scenario=scenario)
        candidate_scenario = simulate(candidate_plan, days=int(scenario["days"]), review_status=review_status, scenario=scenario)
        comparison = compare_simulations(baseline_scenario, candidate_scenario)
        scenario_results.append(
            {
                "scenario": scenario["id"],
                "status": comparison["status"],
                "summary": comparison["summary"],
                "bottlenecks": comparison["bottlenecks"],
                "labor_delta": comparison["labor_delta"],
                "unmet_need_deltas": comparison["unmet_need_deltas"],
                "resource_deltas": comparison["resource_deltas"],
                "provisional": True,
            }
        )

    capability_deltas = _capability_deltas(baseline_sim, candidate_sim)
    acceptance = _acceptance(pattern, materialization, normal_comparison, scenario_results, capability_deltas)
    status = "promotion_recommended" if acceptance["can_promote"] else "blocked" if acceptance["regressions"] else "needs_review"
    report = {
        "kind": "PatchImpactReport",
        "version": "v0",
        "id": f"impact_{materialization['id']}",
        "status": status,
        "source_materialization_id": materialization["id"],
        "pattern_id": pattern["id"],
        "pattern_path": _display_path(pattern_path, root),
        "placement_target": materialization.get("placement_target") or _placement_target_for_pattern(pattern["id"]),
        "baseline_plan_id": baseline_plan["id"],
        "candidate_plan_id": candidate_plan["id"],
        "summary": _summary(status, pattern, acceptance, capability_deltas, normal_comparison),
        "capability_deltas": capability_deltas,
        "normal_year_comparison": {
            "status": normal_comparison["status"],
            "summary": normal_comparison["summary"],
            "resource_deltas": normal_comparison["resource_deltas"],
            "labor_delta": normal_comparison["labor_delta"],
            "unmet_need_deltas": normal_comparison["unmet_need_deltas"],
            "bottlenecks": normal_comparison["bottlenecks"],
            "provisional": True,
        },
        "scenario_results": scenario_results,
        "acceptance": acceptance,
        "provisional": True,
    }
    _require_valid(report, report["id"])
    if report_output:
        write_json(report_output, report)
    return report


def promote_materialized_patch(
    materialization: dict[str, Any],
    *,
    repo_root: str | Path = ".",
    compiled_plan_path: str | Path = DEFAULT_COMPILED_PLAN_PATH,
    days: int = 365,
    report_output: str | Path | None = None,
) -> dict[str, Any]:
    root = Path(repo_root).resolve()
    impact = analyze_materialized_patch(
        materialization,
        repo_root=root,
        compiled_plan_path=compiled_plan_path,
        days=days,
    )
    if not impact.get("acceptance", {}).get("can_promote"):
        report = _blocked_promotion(impact)
        if report_output:
            write_json(report_output, report)
        return report

    pattern = load_data(_resolve(root, impact["pattern_path"]))
    plan_path = _resolve(root, compiled_plan_path)
    baseline_plan = load_data(plan_path)
    promoted_plan = apply_pattern_to_compiled_plan(baseline_plan, pattern)
    review_status = _optional_load(root / GENERATED_DIR / "micro_commons_review_status.json")
    simulation = simulate(promoted_plan, days=int(days), review_status=review_status)
    scenario_runs = [
        run_scenario(promoted_plan, load_data(path))
        for path in _scenario_paths(root, None)
    ]
    runtime_bundle = build_runtime_bundle(
        promoted_plan,
        simulation,
        scenario_runs,
        {
            "compiled_plan": str(DEFAULT_COMPILED_PLAN_PATH),
            "simulation": str(DEFAULT_SIMULATION_PATH),
            "scenarios": [str(GENERATED_DIR / f"{run['scenario']}_scenario.json") for run in scenario_runs],
        },
    )
    population = _world_population(root) or int(promoted_plan.get("site_summary", {}).get("population_target", 80))
    world_manifest = build_world_manifest(
        runtime_bundle,
        population=population,
        runtime_bundle_path=str(DEFAULT_RUNTIME_BUNDLE_PATH),
        world_id=f"civic_floor_{population}_v0",
    )

    write_json(root / DEFAULT_COMPILED_PLAN_PATH, promoted_plan)
    write_json(root / DEFAULT_SIMULATION_PATH, simulation)
    for run in scenario_runs:
        write_json(root / GENERATED_DIR / f"{run['scenario']}_scenario.json", run)
    write_json(root / DEFAULT_RUNTIME_BUNDLE_PATH, runtime_bundle)
    write_json(root / WORLD_MANIFEST_PATH, world_manifest)

    report = {
        "kind": "PatchPromotionReport",
        "version": "v0",
        "id": f"promotion_{impact['id']}",
        "status": "promoted",
        "source_impact_report_id": impact["id"],
        "pattern_id": pattern["id"],
        "updated_artifacts": {
            "compiled_plan": str(DEFAULT_COMPILED_PLAN_PATH),
            "simulation": str(DEFAULT_SIMULATION_PATH),
            "runtime_bundle": str(DEFAULT_RUNTIME_BUNDLE_PATH),
            "world_manifest": str(WORLD_MANIFEST_PATH),
        },
        "summary": [
            f"Promoted {pattern['id']} into the active generated model.",
            "Regenerated compiled plan, normal-year simulation, runtime bundle, scenario runs, and world manifest.",
        ],
        "next_actions": [
            "Reload the viewer to pick up the regenerated world manifest.",
            "Keep external health, privacy, consent, and professional-boundary review visible before treating this as validated.",
        ],
        "provisional": True,
    }
    _require_valid(report, report["id"])
    if report_output:
        write_json(report_output, report)
    return report


def apply_pattern_to_compiled_plan(compiled_plan: dict[str, Any], pattern: dict[str, Any]) -> dict[str, Any]:
    plan = copy.deepcopy(compiled_plan)
    pattern_id = pattern["id"]
    _remove_pattern_from_compiled_plan(plan, pattern_id)
    _materialize_active_patterns(plan, [pattern_id], {pattern_id: pattern})
    _refresh_role_burden(plan)
    plan.setdefault("metadata", {})["patch_impact"] = {
        "source": "materialized_patch",
        "pattern_id": pattern_id,
        "provisional": True,
    }
    return plan


def _remove_pattern_from_compiled_plan(plan: dict[str, Any], pattern_id: str) -> None:
    plan["selected_patterns"] = [item for item in plan.get("selected_patterns", []) if item != pattern_id]
    plan["dependency_order"] = [item for item in plan.get("dependency_order", []) if item != pattern_id]
    for phase in plan.get("phases", []):
        phase["patterns"] = [item for item in phase.get("patterns", []) if item.get("pattern_id") != pattern_id]
    plan["maintenance_calendar"] = [item for item in plan.get("maintenance_calendar", []) if item.get("pattern_id") != pattern_id]
    plan["risk_register"] = [item for item in plan.get("risk_register", []) if item.get("pattern_id") != pattern_id]
    inputs = plan.setdefault("simulation_inputs", {})
    for key in [
        "resource_effects_by_pattern",
        "critical_resources_by_pattern",
        "storage_by_pattern",
        "capability_effects_by_pattern",
    ]:
        inputs.setdefault(key, {}).pop(pattern_id, None)
    _refresh_role_burden(plan)


def _refresh_role_burden(plan: dict[str, Any]) -> None:
    role_hours: dict[str, float] = {}
    for task in plan.get("maintenance_calendar", []):
        role = str(task.get("role") or "unassigned")
        role_hours[role] = role_hours.get(role, 0.0) + float(task.get("estimated_hours", 0.0))
    burden = plan.setdefault("role_burden", {})
    burden["weekly_hours_by_role"] = dict(sorted((role, round(hours, 6)) for role, hours in role_hours.items()))
    total_hours = round(sum(role_hours.values()), 6)
    burden["total_recurring_hours_per_week"] = total_hours
    population = max(1, int(plan.get("site_summary", {}).get("population_target", 1)))
    burden["recurring_hours_per_resident_per_week"] = round(total_hours / population, 3)


def _acceptance(
    pattern: dict[str, Any],
    materialization: dict[str, Any],
    normal_comparison: dict[str, Any],
    scenario_results: list[dict[str, Any]],
    capability_deltas: list[dict[str, Any]],
) -> dict[str, Any]:
    survival_resources = {"water_liters", "energy_kwh", "food_servings"}
    improvements = [
        f"{delta['domain']}.{delta['field']}: {delta['before']} -> {delta['after']}"
        for delta in capability_deltas
        if delta.get("improved")
    ]
    regressions = []
    warnings = []
    for item in normal_comparison["unmet_need_deltas"]:
        if item.get("resource") in survival_resources and float(item.get("delta", 0)) > 0:
            regressions.append(f"Normal year {item['resource']} unmet demand increases by {item['delta']}.")
    labor_delta = float(normal_comparison["labor_delta"].get("estimated_hours_per_resident_per_week_delta", 0))
    if labor_delta > 0.5:
        regressions.append(f"Visible labor burden increases by {labor_delta} hours per resident per week.")
    elif labor_delta > 0:
        warnings.append(f"Visible labor burden increases by {labor_delta} hours per resident per week.")
    for scenario in scenario_results:
        for item in scenario["unmet_need_deltas"]:
            if item.get("resource") in survival_resources and float(item.get("delta", 0)) > 0:
                regressions.append(f"{scenario['scenario']} {item['resource']} unmet demand increases by {item['delta']}.")
        if scenario["status"] != "stable":
            warnings.append(f"{scenario['scenario']} comparison is {scenario['status']}.")
    required_external = list(materialization.get("suggested_plan_change", {}).get("resolved_external_dependencies", []))
    if required_external:
        warnings.append(f"External review dependencies remain explicit: {', '.join(required_external)}.")
    if not improvements:
        regressions.append("No modeled capability improvement was detected.")
    return {
        "can_promote": bool(improvements) and not regressions,
        "improvements": improvements,
        "regressions": regressions,
        "warnings": warnings,
        "required_external_dependencies": required_external,
    }


def _capability_deltas(baseline_sim: dict[str, Any], candidate_sim: dict[str, Any]) -> list[dict[str, Any]]:
    before_domains = baseline_sim.get("capability_state", {}).get("domains", {})
    after_domains = candidate_sim.get("capability_state", {}).get("domains", {})
    deltas = []
    for domain in sorted(set(before_domains) | set(after_domains)):
        before = before_domains.get(domain, {})
        after = after_domains.get(domain, {})
        for field in sorted(set(before) | set(after)):
            before_value = before.get(field)
            after_value = after.get(field)
            if before_value == after_value:
                continue
            deltas.append(
                {
                    "domain": domain,
                    "field": field,
                    "before": before_value,
                    "after": after_value,
                    "improved": _is_improvement(field, before_value, after_value),
                    "provisional": True,
                }
            )
    return deltas


def _is_improvement(field: str, before: Any, after: Any) -> bool:
    if isinstance(before, bool) or isinstance(after, bool):
        return after is True and before in {False, None, "unknown", "missing"}
    if isinstance(before, (int, float)) and isinstance(after, (int, float)):
        if field.endswith("_risk_score"):
            return float(after) < float(before)
        return float(after) > float(before)
    return before != after and after not in {None, "unknown", False}


def _summary(
    status: str,
    pattern: dict[str, Any],
    acceptance: dict[str, Any],
    capability_deltas: list[dict[str, Any]],
    normal_comparison: dict[str, Any],
) -> list[str]:
    labor_delta = normal_comparison["labor_delta"].get("estimated_hours_per_resident_per_week_delta", 0)
    return [
        f"Impact status is {status}.",
        f"Pattern {pattern['id']} changes {len(capability_deltas)} capability field(s).",
        f"Promotion improvements: {len(acceptance['improvements'])}. Regressions: {len(acceptance['regressions'])}.",
        f"Normal-year labor delta is {labor_delta} hours per resident per week.",
    ]


def _blocked_impact(materialization: dict[str, Any], reasons: list[str]) -> dict[str, Any]:
    return {
        "kind": "PatchImpactReport",
        "version": "v0",
        "id": f"impact_{materialization.get('id', 'unknown_materialization')}",
        "status": "blocked",
        "source_materialization_id": str(materialization.get("id", "unknown_materialization")),
        "pattern_id": str(materialization.get("source_candidate_id", "unknown_pattern")),
        "pattern_path": str(materialization.get("materialized_artifact_path", "")),
        "placement_target": materialization.get("placement_target") or _placement_target_for_pattern(str(materialization.get("source_candidate_id", ""))),
        "baseline_plan_id": "unknown",
        "candidate_plan_id": "unknown",
        "summary": reasons,
        "capability_deltas": [],
        "normal_year_comparison": {},
        "scenario_results": [],
        "acceptance": {
            "can_promote": False,
            "improvements": [],
            "regressions": reasons,
            "warnings": [],
            "required_external_dependencies": [],
        },
        "provisional": True,
    }


def _blocked_promotion(impact: dict[str, Any]) -> dict[str, Any]:
    return {
        "kind": "PatchPromotionReport",
        "version": "v0",
        "id": f"promotion_{impact.get('id', 'unknown_impact')}",
        "status": "blocked",
        "source_impact_report_id": str(impact.get("id", "unknown_impact")),
        "pattern_id": str(impact.get("pattern_id", "unknown_pattern")),
        "updated_artifacts": {},
        "summary": impact.get("acceptance", {}).get("regressions", ["Impact report does not recommend promotion."]),
        "next_actions": ["Resolve regressions or rerun analysis before promotion."],
        "provisional": True,
    }


def _scenario_paths(root: Path, scenario_paths: list[str | Path] | None) -> list[Path]:
    paths = scenario_paths or DEFAULT_SCENARIO_PATHS
    return [path for path in (_resolve(root, item) for item in paths) if path.exists()]


def _resolve(root: Path, path: str | Path) -> Path:
    target = Path(path)
    if not target.is_absolute():
        target = root / target
    target = target.resolve()
    if not target.is_relative_to(root):
        raise ValueError(f"Path escapes repo root: {path}")
    return target


def _display_path(path: Path, root: Path) -> str:
    try:
        return str(path.resolve().relative_to(root))
    except ValueError:
        return str(path)


def _optional_load(path: Path) -> dict[str, Any] | None:
    return load_data(path) if path.exists() else None


def _world_population(root: Path) -> int | None:
    path = root / WORLD_MANIFEST_PATH
    if not path.exists():
        return None
    world = load_data(path)
    return int(world.get("population", {}).get("residents", 0)) or None


def _validation_messages(report: Any) -> list[str]:
    return [f"{issue.path}: {issue.message}" for issue in getattr(report, "issues", [])]


def _require_valid(data: dict[str, Any], path: str) -> None:
    report = validate_data(data, path)
    if not report.ok:
        raise ValueError("; ".join(f"{issue.path}: {issue.message}" for issue in report.issues))


def _placement_target_for_pattern(pattern_id: str) -> dict[str, str]:
    if pattern_id.startswith("care_health_") or "medication" in pattern_id:
        return {
            "object_id": "structure_care_room",
            "label": "Care Room",
            "relationship": "contained_module",
        }
    if pattern_id.startswith("water_") or "water" in pattern_id:
        return {
            "object_id": "node_water_reserve",
            "label": "Water Source + Reserve",
            "relationship": "attached_operating_protocol",
        }
    if pattern_id.startswith("mobility_access_") or "accessible_route" in pattern_id:
        return {
            "object_id": "zone_mobility_loop",
            "label": "Mobility Loop / Daily Route Network",
            "relationship": "attached_operating_protocol",
        }
    return {
        "object_id": "",
        "label": "Unplaced Model Layer",
        "relationship": "model_layer",
    }
