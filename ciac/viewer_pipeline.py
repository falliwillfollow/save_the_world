from __future__ import annotations

from pathlib import Path
from typing import Any

from .artifact_cohesion import evaluate_artifact_cohesion
from .compiler import load_patterns
from .complexity import generate_complexity_report
from .food_autonomy import generate_food_autonomy_report
from .food_labor import generate_food_labor_report
from .io import load_data, write_json
from .node_scaling import generate_node_scaling_report
from .topology_optimizer import generate_topology_recommendation
from .viewer_cycle_pipeline import regenerate_viewer_cycle_reports


GENERATED_DIR = Path("examples/generated")
MODULE_REGISTRY_PATH = Path("module_registries/micro_commons_default_v0.yaml")
SCALE_PROFILE_PATH = Path("scale_profiles/micro_commons_scale_targets_v0.yaml")
FOOD_LABOR_REPORT_PATH = GENERATED_DIR / "micro_commons_food_labor_report.json"
COMPLEXITY_REPORT_PATH = GENERATED_DIR / "micro_commons_complexity_report.json"
NODE_SCALING_REPORT_PATH = GENERATED_DIR / "micro_commons_node_scaling.json"
TOPOLOGY_RECOMMENDATION_PATH = GENERATED_DIR / "micro_commons_topology_recommendation.json"
ARTIFACT_COHESION_PATH = GENERATED_DIR / "micro_commons_artifact_cohesion.json"
FOOD_AUTONOMY_REPORT_PATH = GENERATED_DIR / "micro_commons_food_autonomy_report.json"
DEFAULT_SCENARIO_PATHS = [
    Path("scenarios/water_contamination_response_v2.yaml"),
    Path("scenarios/crop_failure.yaml"),
    Path("scenarios/energy_outage_reserve_v2.yaml"),
]


def regenerate_viewer_population_reports(
    repo_root: str | Path,
    population: int,
    cycle_event: dict[str, Any] | None = None,
) -> dict[str, Any]:
    root = Path(repo_root)
    generated_dir = root / GENERATED_DIR
    registry = load_data(root / MODULE_REGISTRY_PATH)
    scale_profile = load_data(root / SCALE_PROFILE_PATH)
    patterns = load_patterns(root / "patterns")

    food_labor = generate_food_labor_report(registry, patterns, "food_production", [int(population)])
    write_json(generated_dir / FOOD_LABOR_REPORT_PATH.name, food_labor)

    complexity = generate_complexity_report(registry, patterns)
    write_json(generated_dir / COMPLEXITY_REPORT_PATH.name, complexity)

    node_report = generate_node_scaling_report(registry, scale_profile, [int(population)])
    write_json(generated_dir / NODE_SCALING_REPORT_PATH.name, node_report)

    topology_report = generate_topology_recommendation(node_report, int(population), food_labor, complexity)
    write_json(generated_dir / TOPOLOGY_RECOMMENDATION_PATH.name, topology_report)

    cycle_payload = regenerate_viewer_cycle_reports(
        root,
        int(population),
        days=int((cycle_event or {}).get("days", 365)),
        cycle_index=int((cycle_event or {}).get("cycle_number", 1)),
        candidate_id=str((cycle_event or {}).get("selected_candidate") or "") or None,
        node_scaling_report=node_report,
    )
    scenarios = [load_data(root / path) for path in DEFAULT_SCENARIO_PATHS if (root / path).exists()]
    food_autonomy = generate_food_autonomy_report(cycle_payload["cycle_iteration"], scenarios)
    write_json(generated_dir / FOOD_AUTONOMY_REPORT_PATH.name, food_autonomy)

    cohesion_report = evaluate_artifact_cohesion(generated_dir)
    write_json(generated_dir / ARTIFACT_COHESION_PATH.name, cohesion_report)

    return {
        "status": "regenerated",
        "population": int(population),
        "artifacts": {
            "food_labor": str(GENERATED_DIR / FOOD_LABOR_REPORT_PATH.name),
            "complexity": str(GENERATED_DIR / COMPLEXITY_REPORT_PATH.name),
            "node_scaling": str(GENERATED_DIR / NODE_SCALING_REPORT_PATH.name),
            "topology_recommendation": str(GENERATED_DIR / TOPOLOGY_RECOMMENDATION_PATH.name),
            "artifact_cohesion": str(GENERATED_DIR / ARTIFACT_COHESION_PATH.name),
            "food_autonomy": str(GENERATED_DIR / FOOD_AUTONOMY_REPORT_PATH.name),
            **cycle_payload["artifacts"],
        },
        "food_labor": food_labor,
        "complexity": complexity,
        "node_scaling": node_report,
        "topology_recommendation": topology_report,
        "artifact_cohesion": cohesion_report,
        "food_autonomy": food_autonomy,
        "cycle_iteration": cycle_payload["cycle_iteration"],
        "runtime_bundle": cycle_payload["runtime_bundle"],
        "search_optimizer": cycle_payload["search_optimizer"],
    }
