from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .artifact_cohesion import evaluate_artifact_cohesion
from .audit import evaluate_audit
from .automation_manifest import build_automation_manifest, write_automation_manifest
from .candidates import generate_candidate_matrix
from .compare import compare_audits
from .compiler import CompileError, compile_plan, load_patterns
from .complexity import generate_complexity_report
from .cycle import materialize_search_candidate
from .dossier import generate_dossier
from .discovery import build_discovery_loop
from .discovery_bridge import serve_discovery_bridge
from .energy import evaluate_energy
from .export_md import render_review_packet, write_review_packet
from .food_labor import generate_food_labor_report
from .foundation import evaluate_foundation_gate
from .gates import evaluate_gates
from .io import dump_json, load_data, write_json
from .life_manifest import build_life_manifest, write_life_manifest
from .matrix_redesign import generate_matrix_redesign
from .module_implementation import implement_technology_module
from .nutrition import evaluate_nutrition
from .node_scaling import generate_node_scaling_report
from .objective_calibration import evaluate_objective_calibration
from .optimization import evaluate_optimization_readiness
from .patch_materialization import materialize_patch_proposal
from .optimizer import optimize_candidates
from .redesign import generate_redesign
from .research import evaluate_scalability_gate, generate_research_needs
from .research_registry import build_research_registry, write_research_registry
from .research_loop import run_research_loop
from .replay_matrix import build_replay_matrix
from .review import evaluate_review_status
from .roles import evaluate_roles
from .runtime_export import build_runtime_bundle
from .scale import generate_tradeoff_scale_report
from .scenarios import run_scenario
from .search_optimizer import optimize_search
from .simulation import simulate
from .simulation_compare import compare_simulations
from .technology import evaluate_module_compatibility, pressure_test_technology_module
from .topology_optimizer import generate_topology_recommendation
from .validation import validate_data, validate_path
from .viewer_server import serve_viewer
from .visualization_bundle import build_visualization_bundle
from .water import evaluate_water
from .weight_governance import evaluate_weight_governance
from .world_manifest import build_world_manifest


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="ciac", description="Civic Infrastructure as Code CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    validate_parser = subparsers.add_parser("validate", help="Validate YAML/JSON civic data")
    validate_parser.add_argument("path")

    compile_parser = subparsers.add_parser("compile", help="Compile a site profile and pattern directory into a plan")
    compile_parser.add_argument("site_profile")
    compile_parser.add_argument("pattern_dir")
    compile_parser.add_argument("--seasonal-profile")
    compile_parser.add_argument("--household-profile")
    compile_parser.add_argument("--spatial-profile")
    compile_parser.add_argument("--output", "-o")

    gates_parser = subparsers.add_parser("gates", help="Evaluate validity gates for a compiled plan")
    gates_parser.add_argument("compiled_plan")
    gates_parser.add_argument("--output", "-o")

    simulate_parser = subparsers.add_parser("simulate", help="Run a provisional normal-year simulation")
    simulate_parser.add_argument("compiled_plan")
    simulate_parser.add_argument("--days", type=int, default=365)
    simulate_parser.add_argument("--scenario")
    simulate_parser.add_argument("--review-status")
    simulate_parser.add_argument("--output", "-o")

    scenario_parser = subparsers.add_parser("scenario", help="Run a provisional stress scenario")
    scenario_parser.add_argument("compiled_plan")
    scenario_parser.add_argument("scenario")
    scenario_parser.add_argument("--output", "-o")

    nutrition_parser = subparsers.add_parser("nutrition", help="Evaluate a provisional food and nutrition plan")
    nutrition_parser.add_argument("compiled_plan")
    nutrition_parser.add_argument("food_plan")
    nutrition_parser.add_argument("--output", "-o")

    food_labor_parser = subparsers.add_parser("food-labor", help="Evaluate food commons labor burden and scale fit")
    food_labor_parser.add_argument("module_registry")
    food_labor_parser.add_argument("pattern_dir")
    food_labor_parser.add_argument("--slot", default="food_production")
    food_labor_parser.add_argument("--people", type=int, action="append", default=[], help="Add an ad hoc population row to scaling_results")
    food_labor_parser.add_argument("--output", "-o")

    water_parser = subparsers.add_parser("water", help="Evaluate a provisional water resilience plan")
    water_parser.add_argument("compiled_plan")
    water_parser.add_argument("water_plan")
    water_parser.add_argument("--output", "-o")

    energy_parser = subparsers.add_parser("energy", help="Evaluate a provisional energy resilience plan")
    energy_parser.add_argument("compiled_plan")
    energy_parser.add_argument("energy_plan")
    energy_parser.add_argument("--output", "-o")

    roles_parser = subparsers.add_parser("roles", help="Evaluate provisional role rotation and labor fairness")
    roles_parser.add_argument("compiled_plan")
    roles_parser.add_argument("role_plan")
    roles_parser.add_argument("--output", "-o")

    audit_parser = subparsers.add_parser("audit", help="Aggregate subsystem reports into a provisional readiness audit")
    audit_parser.add_argument("compiled_plan")
    audit_parser.add_argument("--gates")
    audit_parser.add_argument("--simulation")
    audit_parser.add_argument("--nutrition")
    audit_parser.add_argument("--water")
    audit_parser.add_argument("--energy")
    audit_parser.add_argument("--roles")
    audit_parser.add_argument("--scenario", action="append", default=[])
    audit_parser.add_argument("--output", "-o")

    redesign_parser = subparsers.add_parser("redesign", help="Generate provisional redesign candidates from an audit")
    redesign_parser.add_argument("audit_report")
    redesign_parser.add_argument("compiled_plan")
    redesign_parser.add_argument("--output", "-o")

    compare_parser = subparsers.add_parser("compare", help="Compare two provisional audit reports")
    compare_parser.add_argument("before_audit")
    compare_parser.add_argument("after_audit")
    compare_parser.add_argument("--output", "-o")

    sim_compare_parser = subparsers.add_parser("compare-simulations", help="Compare a baseline simulation with a scenario replay")
    sim_compare_parser.add_argument("baseline_simulation")
    sim_compare_parser.add_argument("replay_simulation")
    sim_compare_parser.add_argument("--output", "-o")

    replay_matrix_parser = subparsers.add_parser("replay-matrix", help="Rank scenario replay comparison reports")
    replay_matrix_parser.add_argument("comparison", nargs="+")
    replay_matrix_parser.add_argument("--output", "-o")

    matrix_redesign_parser = subparsers.add_parser("redesign-matrix", help="Generate redesign candidates from a replay matrix")
    matrix_redesign_parser.add_argument("compiled_plan")
    matrix_redesign_parser.add_argument("replay_matrix")
    matrix_redesign_parser.add_argument("--output", "-o")

    dossier_parser = subparsers.add_parser("dossier", help="Generate a provisional pilot review dossier")
    dossier_parser.add_argument("audit_report")
    dossier_parser.add_argument("compiled_plan")
    dossier_parser.add_argument("--output", "-o")

    review_parser = subparsers.add_parser("review", help="Evaluate review evidence against a pilot dossier")
    review_parser.add_argument("dossier")
    review_parser.add_argument("review_register")
    review_parser.add_argument("--output", "-o")

    export_parser = subparsers.add_parser("export-md", help="Export a human-readable Markdown review packet")
    export_parser.add_argument("compiled_plan")
    export_parser.add_argument("--audit", required=True)
    export_parser.add_argument("--dossier", required=True)
    export_parser.add_argument("--review", required=True)
    export_parser.add_argument("--output", "-o", required=True)

    runtime_parser = subparsers.add_parser("export-runtime", help="Export a viewer-oriented runtime JSON bundle")
    runtime_parser.add_argument("compiled_plan")
    runtime_parser.add_argument("simulation")
    runtime_parser.add_argument("--scenario", action="append", default=[])
    runtime_parser.add_argument("--output", "-o", required=True)

    foundation_parser = subparsers.add_parser("foundation-gate", help="Evaluate simulation foundation readiness for visual buildout")
    foundation_parser.add_argument("compiled_plan")
    foundation_parser.add_argument("baseline_simulation")
    foundation_parser.add_argument("runtime_bundle")
    foundation_parser.add_argument("replay_matrix")
    foundation_parser.add_argument("--review-status")
    foundation_parser.add_argument("--comparison", action="append", default=[])
    foundation_parser.add_argument("--output", "-o")

    opt_ready_parser = subparsers.add_parser("optimization-readiness", help="Evaluate whether patterns expose enough metadata for optimization")
    opt_ready_parser.add_argument("pattern_dir")
    opt_ready_parser.add_argument("optimization_profile")
    opt_ready_parser.add_argument("--output", "-o")

    candidate_parser = subparsers.add_parser("candidate-matrix", help="Generate and compare provisional candidate plans from pattern tunables")
    candidate_parser.add_argument("compiled_plan")
    candidate_parser.add_argument("pattern_dir")
    candidate_parser.add_argument("optimization_profile")
    candidate_parser.add_argument("--scenario", action="append", default=[])
    candidate_parser.add_argument("--review-status")
    candidate_parser.add_argument("--days", type=int, default=365)
    candidate_parser.add_argument("--output", "-o")

    scale_parser = subparsers.add_parser("tradeoff-scale", help="Explain candidate tradeoffs and scale implications")
    scale_parser.add_argument("compiled_plan")
    scale_parser.add_argument("candidate_matrix")
    scale_parser.add_argument("pattern_dir")
    scale_parser.add_argument("scale_profile")
    scale_parser.add_argument("--output", "-o")

    node_scaling_parser = subparsers.add_parser("node-scaling", help="Plan infrastructure node-pool scale up/down across population targets")
    node_scaling_parser.add_argument("module_registry")
    node_scaling_parser.add_argument("--scale-profile")
    node_scaling_parser.add_argument("--people", type=int, action="append", default=[], help="Add an ad hoc population target to the node-scaling report")
    node_scaling_parser.add_argument("--output", "-o")

    topology_parser = subparsers.add_parser("topology-recommend", help="Recommend the next node-aware civic topology action")
    topology_parser.add_argument("node_scaling_report")
    topology_parser.add_argument("--population", type=int, default=150)
    topology_parser.add_argument("--food-labor")
    topology_parser.add_argument("--complexity")
    topology_parser.add_argument("--output", "-o")

    optimize_parser = subparsers.add_parser("optimize", help="Rank candidate configurations and run objective sensitivity checks")
    optimize_parser.add_argument("candidate_matrix")
    optimize_parser.add_argument("optimization_profile")
    optimize_parser.add_argument("--tradeoff-scale")
    optimize_parser.add_argument("--output", "-o")

    viz_parser = subparsers.add_parser("export-visualization", help="Export a versioned visualization handoff bundle")
    viz_parser.add_argument("runtime_bundle")
    viz_parser.add_argument("foundation_gate")
    viz_parser.add_argument("candidate_matrix")
    viz_parser.add_argument("tradeoff_scale")
    viz_parser.add_argument("optimizer_report")
    viz_parser.add_argument("--output", "-o", required=True)

    world_parser = subparsers.add_parser("export-world", help="Export a manifest-driven 3D civic floor world")
    world_parser.add_argument("--runtime", required=True)
    world_parser.add_argument("--output", "-o", required=True)
    world_parser.add_argument("--population", type=int)
    world_parser.add_argument("--world-id")
    world_parser.add_argument("--research-registry")

    life_parser = subparsers.add_parser("export-life-manifest", help="Export a human-facing Life Manifest for Abundance Mode")
    life_parser.add_argument("--runtime", required=True)
    life_parser.add_argument("--world")
    life_parser.add_argument("--output", "-o", required=True)
    life_parser.add_argument("--population", type=int)
    life_parser.add_argument("--baseline-profile", default="default_renter_creator")

    automation_parser = subparsers.add_parser("export-automation-manifest", help="Export an automation substrate manifest with human review gates")
    automation_parser.add_argument("--runtime", required=True)
    automation_parser.add_argument("--world")
    automation_parser.add_argument("--output", "-o", required=True)

    validate_world_parser = subparsers.add_parser("validate-world", help="Validate a CivicFloorWorldManifest JSON file")
    validate_world_parser.add_argument("manifest")

    discovery_parser = subparsers.add_parser("discovery-loop", help="Build an AI/RAG discovery-loop handoff report from a world manifest")
    discovery_parser.add_argument("world_manifest")
    discovery_parser.add_argument("--runtime")
    discovery_parser.add_argument("--focus", default="all")
    discovery_parser.add_argument("--output", "-o")

    discovery_bridge_parser = subparsers.add_parser("discovery-bridge", help="Serve a local HTTP bridge for n8n discovery-loop calls")
    discovery_bridge_parser.add_argument("--host", default="127.0.0.1")
    discovery_bridge_parser.add_argument("--port", type=int, default=8791)
    discovery_bridge_parser.add_argument("--repo-root", default=".")

    research_loop_parser = subparsers.add_parser("research-loop", help="Run a discovery-to-patch-proposal research loop")
    research_loop_parser.add_argument("world_manifest")
    research_loop_parser.add_argument("--runtime")
    research_loop_parser.add_argument("--focus", default="all")
    research_loop_parser.add_argument("--n8n-webhook")
    research_loop_parser.add_argument("--no-seed-fallback", action="store_true")
    research_loop_parser.add_argument("--discovery-output", default="examples/discovery/research_loop.discovery.json")
    research_loop_parser.add_argument("--candidate-output-dir", default="candidate_interventions")
    research_loop_parser.add_argument("--patch-output-dir", default="patch_proposals")
    research_loop_parser.add_argument("--output", "-o")

    materialize_patch_parser = subparsers.add_parser("materialize-patch", help="Materialize a PatchProposal into a provisional model artifact")
    materialize_patch_parser.add_argument("patch_proposal")
    materialize_patch_parser.add_argument("--candidate")
    materialize_patch_parser.add_argument("--repo-root", default=".")
    materialize_patch_parser.add_argument("--overwrite", action="store_true")
    materialize_patch_parser.add_argument("--output", "-o")

    search_parser = subparsers.add_parser("optimize-search", help="Run bounded family-level optimization search")
    search_parser.add_argument("compiled_plan")
    search_parser.add_argument("pattern_dir")
    search_parser.add_argument("optimization_profile")
    search_parser.add_argument("--scenario", action="append", default=[])
    search_parser.add_argument("--review-status")
    search_parser.add_argument("--days", type=int, default=365)
    search_parser.add_argument("--top", type=int, default=10)
    search_parser.add_argument("--output", "-o")

    calibration_parser = subparsers.add_parser("objective-calibration", help="Evaluate optimizer objective score calibration")
    calibration_parser.add_argument("search_optimizer_report")
    calibration_parser.add_argument("calibration_profile")
    calibration_parser.add_argument("--output", "-o")

    weight_parser = subparsers.add_parser("weight-governance", help="Evaluate governance status for optimization objective weights")
    weight_parser.add_argument("optimization_profile")
    weight_parser.add_argument("objective_calibration_report")
    weight_parser.add_argument("weight_governance_profile")
    weight_parser.add_argument("--output", "-o")

    apply_search_parser = subparsers.add_parser("apply-search-candidate", help="Materialize a search optimizer candidate into a next-cycle runtime bundle")
    apply_search_parser.add_argument("compiled_plan")
    apply_search_parser.add_argument("search_optimizer_report")
    apply_search_parser.add_argument("--candidate")
    apply_search_parser.add_argument("--scenario", action="append", default=[])
    apply_search_parser.add_argument("--review-status")
    apply_search_parser.add_argument("--days", type=int, default=365)
    apply_search_parser.add_argument("--cycle-index", type=int, default=1)
    apply_search_parser.add_argument("--playback-seconds", type=int, default=20)
    apply_search_parser.add_argument("--authority-mode", choices=["operator_directed", "review_directed"], default="operator_directed")
    apply_search_parser.add_argument("--pattern-dir")
    apply_search_parser.add_argument("--optimization-profile")
    apply_search_parser.add_argument("--top", type=int, default=10)
    apply_search_parser.add_argument("--output", "-o")

    tech_parser = subparsers.add_parser("technology-pressure-test", help="Pressure-test an evidence-backed sustainability technology module")
    tech_parser.add_argument("compiled_plan")
    tech_parser.add_argument("technology_module")
    tech_parser.add_argument("--output", "-o")

    module_parser = subparsers.add_parser("module-compatibility", help="Evaluate modular swap readiness against a module registry")
    module_parser.add_argument("compiled_plan")
    module_parser.add_argument("module_registry")
    module_parser.add_argument("--technology-module", action="append", default=[])
    module_parser.add_argument("--output", "-o")

    research_parser = subparsers.add_parser("research-needs", help="Emit research briefs for bottlenecks that need evidence-backed modules")
    research_parser.add_argument("compiled_plan")
    research_parser.add_argument("simulation")
    research_parser.add_argument("--module-registry")
    research_parser.add_argument("--output", "-o")

    research_registry_parser = subparsers.add_parser("export-research-registry", help="Export the project-wide research source registry")
    research_registry_parser.add_argument("--capability-policy", default="capability_policies/ciac_capability_policy_v0.yaml")
    research_registry_parser.add_argument("--research-input", action="append", default=[])
    research_registry_parser.add_argument("--scan-path", action="append", default=[])
    research_registry_parser.add_argument("--output", "-o", required=True)

    scalability_parser = subparsers.add_parser("scalability-gate", help="Evaluate whether a technology module is ready to scale in simulation")
    scalability_parser.add_argument("compiled_plan")
    scalability_parser.add_argument("technology_module")
    scalability_parser.add_argument("--module-registry")
    scalability_parser.add_argument("--output", "-o")

    implement_module_parser = subparsers.add_parser("implement-module", help="Gate and materialize a preauthored TechnologyModule into an adjusted simulation plan")
    implement_module_parser.add_argument("compiled_plan")
    implement_module_parser.add_argument("technology_module")
    implement_module_parser.add_argument("--module-registry")
    implement_module_parser.add_argument("--review-status")
    implement_module_parser.add_argument("--days", type=int, default=365)
    implement_module_parser.add_argument("--output", "-o")

    complexity_parser = subparsers.add_parser("complexity-report", help="Evaluate registry and pattern complexity for scalability")
    complexity_parser.add_argument("module_registry")
    complexity_parser.add_argument("pattern_dir")
    complexity_parser.add_argument("--output", "-o")

    cohesion_parser = subparsers.add_parser("artifact-cohesion", help="Check generated viewer artifacts for stale or disconnected report flow")
    cohesion_parser.add_argument("generated_dir")
    cohesion_parser.add_argument("--output", "-o")

    viewer_server_parser = subparsers.add_parser("viewer-server", help="Serve the viewer with an API that persists browser run logs")
    viewer_server_parser.add_argument("--host", default="127.0.0.1")
    viewer_server_parser.add_argument("--port", type=int, default=8765)
    viewer_server_parser.add_argument("--repo-root", default=".")

    args = parser.parse_args(argv)
    if args.command == "validate":
        return _validate(args.path)
    if args.command == "compile":
        return _compile(args.site_profile, args.pattern_dir, args.seasonal_profile, args.household_profile, args.spatial_profile, args.output)
    if args.command == "gates":
        return _gates(args.compiled_plan, args.output)
    if args.command == "simulate":
        return _simulate(args.compiled_plan, args.days, args.scenario, args.review_status, args.output)
    if args.command == "scenario":
        return _scenario(args.compiled_plan, args.scenario, args.output)
    if args.command == "nutrition":
        return _nutrition(args.compiled_plan, args.food_plan, args.output)
    if args.command == "food-labor":
        return _food_labor(args.module_registry, args.pattern_dir, args.slot, args.people, args.output)
    if args.command == "water":
        return _water(args.compiled_plan, args.water_plan, args.output)
    if args.command == "energy":
        return _energy(args.compiled_plan, args.energy_plan, args.output)
    if args.command == "roles":
        return _roles(args.compiled_plan, args.role_plan, args.output)
    if args.command == "audit":
        return _audit(args)
    if args.command == "redesign":
        return _redesign(args.audit_report, args.compiled_plan, args.output)
    if args.command == "compare":
        return _compare(args.before_audit, args.after_audit, args.output)
    if args.command == "compare-simulations":
        return _compare_simulations(args.baseline_simulation, args.replay_simulation, args.output)
    if args.command == "replay-matrix":
        return _replay_matrix(args.comparison, args.output)
    if args.command == "redesign-matrix":
        return _redesign_matrix(args.compiled_plan, args.replay_matrix, args.output)
    if args.command == "dossier":
        return _dossier(args.audit_report, args.compiled_plan, args.output)
    if args.command == "review":
        return _review(args.dossier, args.review_register, args.output)
    if args.command == "export-md":
        return _export_md(args)
    if args.command == "export-runtime":
        return _export_runtime(args)
    if args.command == "foundation-gate":
        return _foundation_gate(args)
    if args.command == "optimization-readiness":
        return _optimization_readiness(args.pattern_dir, args.optimization_profile, args.output)
    if args.command == "candidate-matrix":
        return _candidate_matrix(args)
    if args.command == "tradeoff-scale":
        return _tradeoff_scale(args)
    if args.command == "node-scaling":
        return _node_scaling(args.module_registry, args.scale_profile, args.people, args.output)
    if args.command == "topology-recommend":
        return _topology_recommend(args)
    if args.command == "optimize":
        return _optimize(args)
    if args.command == "export-visualization":
        return _export_visualization(args)
    if args.command == "export-world":
        return _export_world(args)
    if args.command == "export-life-manifest":
        return _export_life_manifest(args)
    if args.command == "export-automation-manifest":
        return _export_automation_manifest(args)
    if args.command == "validate-world":
        return _validate_world(args.manifest)
    if args.command == "discovery-loop":
        return _discovery_loop(args)
    if args.command == "discovery-bridge":
        return _discovery_bridge(args.host, args.port, args.repo_root)
    if args.command == "research-loop":
        return _research_loop(args)
    if args.command == "materialize-patch":
        return _materialize_patch(args)
    if args.command == "optimize-search":
        return _optimize_search(args)
    if args.command == "objective-calibration":
        return _objective_calibration(args.search_optimizer_report, args.calibration_profile, args.output)
    if args.command == "weight-governance":
        return _weight_governance(args.optimization_profile, args.objective_calibration_report, args.weight_governance_profile, args.output)
    if args.command == "apply-search-candidate":
        return _apply_search_candidate(args)
    if args.command == "technology-pressure-test":
        return _technology_pressure_test(args.compiled_plan, args.technology_module, args.output)
    if args.command == "module-compatibility":
        return _module_compatibility(args.compiled_plan, args.module_registry, args.technology_module, args.output)
    if args.command == "research-needs":
        return _research_needs(args.compiled_plan, args.simulation, args.module_registry, args.output)
    if args.command == "export-research-registry":
        return _export_research_registry(args)
    if args.command == "scalability-gate":
        return _scalability_gate(args.compiled_plan, args.technology_module, args.module_registry, args.output)
    if args.command == "implement-module":
        return _implement_module(args)
    if args.command == "complexity-report":
        return _complexity_report(args.module_registry, args.pattern_dir, args.output)
    if args.command == "artifact-cohesion":
        return _artifact_cohesion(args.generated_dir, args.output)
    if args.command == "viewer-server":
        return _viewer_server(args.host, args.port, args.repo_root)
    return 2


def _validate(path: str) -> int:
    reports = validate_path(path)
    had_errors = False
    for report in reports:
        if report.ok:
            print(f"OK {report.path}")
        else:
            had_errors = True
            print(f"ERROR {report.path}")
        for issue in report.issues:
            print(f"  {issue.severity.upper()} {issue.path}: {issue.message}")
    return 1 if had_errors else 0


def _compile(
    site_profile_path: str,
    pattern_dir: str,
    seasonal_profile_path: str | None,
    household_profile_path: str | None,
    spatial_profile_path: str | None,
    output: str | None,
) -> int:
    try:
        site_profile = load_data(site_profile_path)
        seasonal_profile = load_data(seasonal_profile_path) if seasonal_profile_path else None
        household_profile = load_data(household_profile_path) if household_profile_path else None
        spatial_profile = load_data(spatial_profile_path) if spatial_profile_path else None
        plan = compile_plan(site_profile, load_patterns(pattern_dir), seasonal_profile, household_profile, spatial_profile)
    except CompileError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        if exc.plan is not None:
            serialized = dump_json(exc.plan)
            if output:
                write_json(output, exc.plan)
            else:
                print(serialized)
        return 2

    if output:
        write_json(output, plan)
        print(f"Wrote {Path(output)}")
    else:
        print(dump_json(plan), end="")
    return 0


def _gates(compiled_plan_path: str, output: str | None) -> int:
    report = evaluate_gates(load_data(compiled_plan_path))
    if output:
        write_json(output, report)
        print(f"Wrote {Path(output)}")
    else:
        print(dump_json(report), end="")
    return 1 if not report["promotion_allowed"] else 0


def _simulate(
    compiled_plan_path: str,
    days: int,
    scenario_path: str | None,
    review_status_path: str | None,
    output: str | None,
) -> int:
    try:
        report = simulate(
            load_data(compiled_plan_path),
            days=days,
            scenario=load_data(scenario_path) if scenario_path else None,
            review_status=load_data(review_status_path) if review_status_path else None,
        )
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    if output:
        write_json(output, report)
        print(f"Wrote {Path(output)}")
    else:
        print(dump_json(report), end="")
    return 1 if report["status"] == "fail" else 0


def _scenario(compiled_plan_path: str, scenario_path: str, output: str | None) -> int:
    report = run_scenario(load_data(compiled_plan_path), load_data(scenario_path))
    if output:
        write_json(output, report)
        print(f"Wrote {Path(output)}")
    else:
        print(dump_json(report), end="")
    return 1 if report["status"] == "fail" else 0


def _nutrition(compiled_plan_path: str, food_plan_path: str, output: str | None) -> int:
    report = evaluate_nutrition(load_data(compiled_plan_path), load_data(food_plan_path))
    if output:
        write_json(output, report)
        print(f"Wrote {Path(output)}")
    else:
        print(dump_json(report), end="")
    return 1 if report["status"] == "fail" else 0


def _food_labor(module_registry_path: str, pattern_dir: str, slot: str, people: list[int], output: str | None) -> int:
    registry = load_data(module_registry_path)
    registry_report = validate_data(registry, module_registry_path)
    if not registry_report.ok:
        details = "; ".join(f"{issue.path}: {issue.message}" for issue in registry_report.issues)
        print(f"ERROR: Invalid module registry: {details}", file=sys.stderr)
        return 2
    try:
        report = generate_food_labor_report(registry, load_patterns(pattern_dir), slot, people)
    except CompileError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    if output:
        write_json(output, report)
        print(f"Wrote {Path(output)}")
    else:
        print(dump_json(report), end="")
    return 1 if report["status"] == "fail" else 0


def _water(compiled_plan_path: str, water_plan_path: str, output: str | None) -> int:
    report = evaluate_water(load_data(compiled_plan_path), load_data(water_plan_path))
    if output:
        write_json(output, report)
        print(f"Wrote {Path(output)}")
    else:
        print(dump_json(report), end="")
    return 1 if report["status"] == "fail" else 0


def _energy(compiled_plan_path: str, energy_plan_path: str, output: str | None) -> int:
    report = evaluate_energy(load_data(compiled_plan_path), load_data(energy_plan_path))
    if output:
        write_json(output, report)
        print(f"Wrote {Path(output)}")
    else:
        print(dump_json(report), end="")
    return 1 if report["status"] == "fail" else 0


def _roles(compiled_plan_path: str, role_plan_path: str, output: str | None) -> int:
    report = evaluate_roles(load_data(compiled_plan_path), load_data(role_plan_path))
    if output:
        write_json(output, report)
        print(f"Wrote {Path(output)}")
    else:
        print(dump_json(report), end="")
    return 1 if report["status"] == "fail" else 0


def _audit(args: argparse.Namespace) -> int:
    reports = {
        "gates": load_data(args.gates) if args.gates else None,
        "simulation": load_data(args.simulation) if args.simulation else None,
        "nutrition": load_data(args.nutrition) if args.nutrition else None,
        "water": load_data(args.water) if args.water else None,
        "energy": load_data(args.energy) if args.energy else None,
        "roles": load_data(args.roles) if args.roles else None,
    }
    scenarios = [load_data(path) for path in args.scenario]
    report = evaluate_audit(load_data(args.compiled_plan), reports, scenarios)
    if args.output:
        write_json(args.output, report)
        print(f"Wrote {Path(args.output)}")
    else:
        print(dump_json(report), end="")
    return 1 if report["overall_status"] == "fail" else 0


def _redesign(audit_report_path: str, compiled_plan_path: str, output: str | None) -> int:
    report = generate_redesign(load_data(audit_report_path), load_data(compiled_plan_path))
    if output:
        write_json(output, report)
        print(f"Wrote {Path(output)}")
    else:
        print(dump_json(report), end="")
    return 0


def _compare(before_audit_path: str, after_audit_path: str, output: str | None) -> int:
    report = compare_audits(load_data(before_audit_path), load_data(after_audit_path))
    if output:
        write_json(output, report)
        print(f"Wrote {Path(output)}")
    else:
        print(dump_json(report), end="")
    return 1 if report["status"] == "regressed" else 0


def _compare_simulations(baseline_path: str, replay_path: str, output: str | None) -> int:
    report = compare_simulations(load_data(baseline_path), load_data(replay_path))
    if output:
        write_json(output, report)
        print(f"Wrote {Path(output)}")
    else:
        print(dump_json(report), end="")
    return 1 if report["status"] == "stress_failed" else 0


def _replay_matrix(comparison_paths: list[str], output: str | None) -> int:
    try:
        report = build_replay_matrix([load_data(path) for path in comparison_paths])
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    if output:
        write_json(output, report)
        print(f"Wrote {Path(output)}")
    else:
        print(dump_json(report), end="")
    return 1 if report["status"] == "stress_failed" else 0


def _redesign_matrix(compiled_plan_path: str, replay_matrix_path: str, output: str | None) -> int:
    report = generate_matrix_redesign(load_data(compiled_plan_path), load_data(replay_matrix_path))
    if output:
        write_json(output, report)
        print(f"Wrote {Path(output)}")
    else:
        print(dump_json(report), end="")
    return 0


def _dossier(audit_report_path: str, compiled_plan_path: str, output: str | None) -> int:
    report = generate_dossier(load_data(audit_report_path), load_data(compiled_plan_path))
    if output:
        write_json(output, report)
        print(f"Wrote {Path(output)}")
    else:
        print(dump_json(report), end="")
    return 1 if report["readiness_status"] == "not_ready" else 0


def _review(dossier_path: str, review_register_path: str, output: str | None) -> int:
    report = evaluate_review_status(load_data(dossier_path), load_data(review_register_path))
    if output:
        write_json(output, report)
        print(f"Wrote {Path(output)}")
    else:
        print(dump_json(report), end="")
    return 1 if report["status"] == "missing_evidence" else 0


def _export_md(args: argparse.Namespace) -> int:
    content = render_review_packet(
        load_data(args.compiled_plan),
        load_data(args.audit),
        load_data(args.dossier),
        load_data(args.review),
        {
            "compiled_plan": args.compiled_plan,
            "audit": args.audit,
            "dossier": args.dossier,
            "review": args.review,
        },
    )
    write_review_packet(args.output, content)
    print(f"Wrote {Path(args.output)}")
    return 0


def _export_runtime(args: argparse.Namespace) -> int:
    scenarios = [load_data(path) for path in args.scenario]
    bundle = build_runtime_bundle(
        load_data(args.compiled_plan),
        load_data(args.simulation),
        scenarios,
        {
            "compiled_plan": args.compiled_plan,
            "simulation": args.simulation,
            "scenarios": args.scenario,
        },
    )
    write_json(args.output, bundle)
    print(f"Wrote {Path(args.output)}")
    return 0


def _foundation_gate(args: argparse.Namespace) -> int:
    report = evaluate_foundation_gate(
        load_data(args.compiled_plan),
        load_data(args.baseline_simulation),
        load_data(args.runtime_bundle),
        load_data(args.replay_matrix),
        load_data(args.review_status) if args.review_status else None,
        [load_data(path) for path in args.comparison],
    )
    if args.output:
        write_json(args.output, report)
        print(f"Wrote {Path(args.output)}")
    else:
        print(dump_json(report), end="")
    return 1 if report["status"] == "not_ready" else 0


def _optimization_readiness(pattern_dir: str, optimization_profile_path: str, output: str | None) -> int:
    try:
        optimization_profile = load_data(optimization_profile_path)
        profile_report = validate_data(optimization_profile, optimization_profile_path)
        if not profile_report.ok:
            details = "; ".join(f"{issue.path}: {issue.message}" for issue in profile_report.issues)
            print(f"ERROR: Invalid optimization profile: {details}", file=sys.stderr)
            return 2
        report = evaluate_optimization_readiness(load_patterns(pattern_dir), optimization_profile)
    except CompileError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    if output:
        write_json(output, report)
        print(f"Wrote {Path(output)}")
    else:
        print(dump_json(report), end="")
    return 1 if report["status"] == "not_ready" else 0


def _candidate_matrix(args: argparse.Namespace) -> int:
    optimization_profile = load_data(args.optimization_profile)
    profile_report = validate_data(optimization_profile, args.optimization_profile)
    if not profile_report.ok:
        details = "; ".join(f"{issue.path}: {issue.message}" for issue in profile_report.issues)
        print(f"ERROR: Invalid optimization profile: {details}", file=sys.stderr)
        return 2
    try:
        report = generate_candidate_matrix(
            load_data(args.compiled_plan),
            load_patterns(args.pattern_dir),
            optimization_profile,
            [load_data(path) for path in args.scenario],
            load_data(args.review_status) if args.review_status else None,
            args.days,
        )
    except (CompileError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    if args.output:
        write_json(args.output, report)
        print(f"Wrote {Path(args.output)}")
    else:
        print(dump_json(report), end="")
    return 1 if report["status"] == "not_ready" else 0


def _tradeoff_scale(args: argparse.Namespace) -> int:
    scale_profile = load_data(args.scale_profile)
    scale_report = validate_data(scale_profile, args.scale_profile)
    if not scale_report.ok:
        details = "; ".join(f"{issue.path}: {issue.message}" for issue in scale_report.issues)
        print(f"ERROR: Invalid scale profile: {details}", file=sys.stderr)
        return 2
    try:
        report = generate_tradeoff_scale_report(
            load_data(args.compiled_plan),
            load_data(args.candidate_matrix),
            load_patterns(args.pattern_dir),
            scale_profile,
        )
    except (CompileError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    if args.output:
        write_json(args.output, report)
        print(f"Wrote {Path(args.output)}")
    else:
        print(dump_json(report), end="")
    return 1 if report["status"] == "not_ready" else 0


def _node_scaling(module_registry_path: str, scale_profile_path: str | None, people: list[int], output: str | None) -> int:
    registry = load_data(module_registry_path)
    registry_report = validate_data(registry, module_registry_path)
    if not registry_report.ok:
        details = "; ".join(f"{issue.path}: {issue.message}" for issue in registry_report.issues)
        print(f"ERROR: Invalid module registry: {details}", file=sys.stderr)
        return 2
    scale_profile = load_data(scale_profile_path) if scale_profile_path else None
    if scale_profile is not None:
        scale_report = validate_data(scale_profile, scale_profile_path or "<scale-profile>")
        if not scale_report.ok:
            details = "; ".join(f"{issue.path}: {issue.message}" for issue in scale_report.issues)
            print(f"ERROR: Invalid scale profile: {details}", file=sys.stderr)
            return 2
    report = generate_node_scaling_report(registry, scale_profile, people)
    if output:
        write_json(output, report)
        print(f"Wrote {Path(output)}")
    else:
        print(dump_json(report), end="")
    return 1 if report["status"] == "not_ready" else 0


def _topology_recommend(args: argparse.Namespace) -> int:
    node_report = load_data(args.node_scaling_report)
    node_validation = validate_data(node_report, args.node_scaling_report)
    if not node_validation.ok:
        details = "; ".join(f"{issue.path}: {issue.message}" for issue in node_validation.issues)
        print(f"ERROR: Invalid node scaling report: {details}", file=sys.stderr)
        return 2
    food_labor = load_data(args.food_labor) if args.food_labor else None
    if food_labor is not None:
        food_validation = validate_data(food_labor, args.food_labor)
        if not food_validation.ok:
            details = "; ".join(f"{issue.path}: {issue.message}" for issue in food_validation.issues)
            print(f"ERROR: Invalid food labor report: {details}", file=sys.stderr)
            return 2
    complexity = load_data(args.complexity) if args.complexity else None
    if complexity is not None:
        complexity_validation = validate_data(complexity, args.complexity)
        if not complexity_validation.ok:
            details = "; ".join(f"{issue.path}: {issue.message}" for issue in complexity_validation.issues)
            print(f"ERROR: Invalid complexity report: {details}", file=sys.stderr)
            return 2
    report = generate_topology_recommendation(node_report, args.population, food_labor, complexity)
    if args.output:
        write_json(args.output, report)
        print(f"Wrote {Path(args.output)}")
    else:
        print(dump_json(report), end="")
    return 1 if report["status"] == "not_ready" else 0


def _optimize(args: argparse.Namespace) -> int:
    optimization_profile = load_data(args.optimization_profile)
    profile_report = validate_data(optimization_profile, args.optimization_profile)
    if not profile_report.ok:
        details = "; ".join(f"{issue.path}: {issue.message}" for issue in profile_report.issues)
        print(f"ERROR: Invalid optimization profile: {details}", file=sys.stderr)
        return 2
    report = optimize_candidates(
        load_data(args.candidate_matrix),
        optimization_profile,
        load_data(args.tradeoff_scale) if args.tradeoff_scale else None,
    )
    if args.output:
        write_json(args.output, report)
        print(f"Wrote {Path(args.output)}")
    else:
        print(dump_json(report), end="")
    return 1 if report["status"] == "not_ready" else 0


def _export_visualization(args: argparse.Namespace) -> int:
    report = build_visualization_bundle(
        load_data(args.runtime_bundle),
        load_data(args.foundation_gate),
        load_data(args.candidate_matrix),
        load_data(args.tradeoff_scale),
        load_data(args.optimizer_report),
        {
            "runtime_bundle": args.runtime_bundle,
            "foundation_gate": args.foundation_gate,
            "candidate_matrix": args.candidate_matrix,
            "tradeoff_scale": args.tradeoff_scale,
            "optimizer_report": args.optimizer_report,
        },
    )
    write_json(args.output, report)
    print(f"Wrote {Path(args.output)}")
    return 1 if report["status"] == "not_ready" else 0


def _optimize_search(args: argparse.Namespace) -> int:
    optimization_profile = load_data(args.optimization_profile)
    profile_report = validate_data(optimization_profile, args.optimization_profile)
    if not profile_report.ok:
        details = "; ".join(f"{issue.path}: {issue.message}" for issue in profile_report.issues)
        print(f"ERROR: Invalid optimization profile: {details}", file=sys.stderr)
        return 2
    try:
        report = optimize_search(
            load_data(args.compiled_plan),
            load_patterns(args.pattern_dir),
            optimization_profile,
            [load_data(path) for path in args.scenario],
            load_data(args.review_status) if args.review_status else None,
            args.days,
            args.top,
        )
    except (CompileError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    if args.output:
        write_json(args.output, report)
        print(f"Wrote {Path(args.output)}")
    else:
        print(dump_json(report), end="")
    return 1 if report["status"] == "not_ready" else 0


def _objective_calibration(search_optimizer_report_path: str, calibration_profile_path: str, output: str | None) -> int:
    calibration_profile = load_data(calibration_profile_path)
    profile_report = validate_data(calibration_profile, calibration_profile_path)
    if not profile_report.ok:
        details = "; ".join(f"{issue.path}: {issue.message}" for issue in profile_report.issues)
        print(f"ERROR: Invalid objective calibration profile: {details}", file=sys.stderr)
        return 2
    report = evaluate_objective_calibration(load_data(search_optimizer_report_path), calibration_profile)
    if output:
        write_json(output, report)
        print(f"Wrote {Path(output)}")
    else:
        print(dump_json(report), end="")
    return 1 if report["status"] == "missing_calibration" else 0


def _weight_governance(
    optimization_profile_path: str,
    objective_calibration_report_path: str,
    weight_governance_profile_path: str,
    output: str | None,
) -> int:
    optimization_profile = load_data(optimization_profile_path)
    profile_report = validate_data(optimization_profile, optimization_profile_path)
    if not profile_report.ok:
        details = "; ".join(f"{issue.path}: {issue.message}" for issue in profile_report.issues)
        print(f"ERROR: Invalid optimization profile: {details}", file=sys.stderr)
        return 2
    governance_profile = load_data(weight_governance_profile_path)
    governance_report = validate_data(governance_profile, weight_governance_profile_path)
    if not governance_report.ok:
        details = "; ".join(f"{issue.path}: {issue.message}" for issue in governance_report.issues)
        print(f"ERROR: Invalid weight governance profile: {details}", file=sys.stderr)
        return 2
    report = evaluate_weight_governance(
        optimization_profile,
        load_data(objective_calibration_report_path),
        governance_profile,
    )
    if output:
        write_json(output, report)
        print(f"Wrote {Path(output)}")
    else:
        print(dump_json(report), end="")
    return 1 if report["status"] == "not_ratified" else 0


def _apply_search_candidate(args: argparse.Namespace) -> int:
    try:
        report = materialize_search_candidate(
            load_data(args.compiled_plan),
            load_data(args.search_optimizer_report),
            args.candidate,
            load_data(args.review_status) if args.review_status else None,
            [load_data(path) for path in args.scenario],
            args.days,
            args.cycle_index,
            args.playback_seconds,
            args.authority_mode,
            load_patterns(args.pattern_dir) if args.pattern_dir else None,
            load_data(args.optimization_profile) if args.optimization_profile else None,
            args.top,
        )
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    if args.output:
        write_json(args.output, report)
        print(f"Wrote {Path(args.output)}")
    else:
        print(dump_json(report), end="")
    return 1 if report["status"] == "blocked" else 0


def _technology_pressure_test(compiled_plan_path: str, technology_module_path: str, output: str | None) -> int:
    module = load_data(technology_module_path)
    module_report = validate_data(module, technology_module_path)
    if not module_report.ok:
        details = "; ".join(f"{issue.path}: {issue.message}" for issue in module_report.issues)
        print(f"ERROR: Invalid technology module: {details}", file=sys.stderr)
        return 2
    report = pressure_test_technology_module(load_data(compiled_plan_path), module)
    if output:
        write_json(output, report)
        print(f"Wrote {Path(output)}")
    else:
        print(dump_json(report), end="")
    return 1 if report["status"] == "blocked" else 0


def _module_compatibility(
    compiled_plan_path: str,
    module_registry_path: str,
    technology_module_paths: list[str],
    output: str | None,
) -> int:
    registry = load_data(module_registry_path)
    registry_report = validate_data(registry, module_registry_path)
    if not registry_report.ok:
        details = "; ".join(f"{issue.path}: {issue.message}" for issue in registry_report.issues)
        print(f"ERROR: Invalid module registry: {details}", file=sys.stderr)
        return 2
    modules = []
    for path in technology_module_paths:
        module = load_data(path)
        module_report = validate_data(module, path)
        if not module_report.ok:
            details = "; ".join(f"{issue.path}: {issue.message}" for issue in module_report.issues)
            print(f"ERROR: Invalid technology module: {details}", file=sys.stderr)
            return 2
        modules.append(module)
    report = evaluate_module_compatibility(load_data(compiled_plan_path), registry, modules)
    if output:
        write_json(output, report)
        print(f"Wrote {Path(output)}")
    else:
        print(dump_json(report), end="")
    return 0


def _export_world(args: argparse.Namespace) -> int:
    runtime_bundle = load_data(args.runtime)
    research_registry = load_data(args.research_registry) if args.research_registry else None
    if research_registry is not None:
        registry_report = validate_data(research_registry, args.research_registry or "<research-registry>")
        if not registry_report.ok:
            details = "; ".join(f"{issue.path}: {issue.message}" for issue in registry_report.issues)
            print(f"ERROR: Invalid research registry: {details}", file=sys.stderr)
            return 2
    manifest = build_world_manifest(
        runtime_bundle,
        population=args.population,
        runtime_bundle_path=args.runtime,
        world_id=args.world_id,
        research_registry=research_registry,
    )
    report = validate_data(manifest, args.output)
    if not report.ok:
        details = "; ".join(f"{issue.path}: {issue.message}" for issue in report.issues)
        print(f"ERROR: Invalid world manifest: {details}", file=sys.stderr)
        return 2
    write_json(args.output, manifest)
    print(f"Wrote {Path(args.output)}")
    return 0


def _export_life_manifest(args: argparse.Namespace) -> int:
    runtime_bundle = load_data(args.runtime)
    world_manifest = load_data(args.world) if args.world else None
    manifest = build_life_manifest(
        runtime_bundle,
        world_manifest,
        population=args.population,
        baseline_profile=args.baseline_profile,
        runtime_bundle_path=args.runtime,
        world_manifest_path=args.world,
    )
    try:
        write_life_manifest(manifest, args.output)
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    print(f"Wrote {Path(args.output)}")
    return 0


def _export_automation_manifest(args: argparse.Namespace) -> int:
    runtime_bundle = load_data(args.runtime)
    world_manifest = load_data(args.world) if args.world else None
    manifest = build_automation_manifest(
        runtime_bundle,
        world_manifest,
        runtime_bundle_path=args.runtime,
        world_manifest_path=args.world,
    )
    try:
        write_automation_manifest(manifest, args.output)
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    print(f"Wrote {Path(args.output)}")
    return 0


def _validate_world(manifest_path: str) -> int:
    manifest = load_data(manifest_path)
    report = validate_data(manifest, manifest_path)
    if report.ok:
        print(f"OK {manifest_path}")
        return 0
    print(f"ERROR {manifest_path}")
    for issue in report.issues:
        print(f"  {issue.severity.upper()} {issue.path}: {issue.message}")
    return 1


def _discovery_loop(args: argparse.Namespace) -> int:
    world_manifest = load_data(args.world_manifest)
    world_report = validate_data(world_manifest, args.world_manifest)
    if not world_report.ok:
        details = "; ".join(f"{issue.path}: {issue.message}" for issue in world_report.issues)
        print(f"ERROR: Invalid world manifest: {details}", file=sys.stderr)
        return 2
    runtime_bundle = load_data(args.runtime) if args.runtime else None
    if runtime_bundle is not None:
        runtime_report = validate_data(runtime_bundle, args.runtime or "<runtime>")
        if not runtime_report.ok:
            details = "; ".join(f"{issue.path}: {issue.message}" for issue in runtime_report.issues)
            print(f"ERROR: Invalid runtime bundle: {details}", file=sys.stderr)
            return 2
    report = build_discovery_loop(
        world_manifest,
        runtime_bundle=runtime_bundle,
        focus=args.focus,
        source_paths={
            "world_manifest": args.world_manifest,
            "runtime_bundle": args.runtime,
        },
    )
    validation = validate_data(report, args.output or "<discovery-loop>")
    if not validation.ok:
        details = "; ".join(f"{issue.path}: {issue.message}" for issue in validation.issues)
        print(f"ERROR: Invalid discovery loop report: {details}", file=sys.stderr)
        return 2
    for candidate in report.get("seed_candidates", []):
        candidate_validation = validate_data(candidate, candidate.get("id", "<candidate>"))
        if not candidate_validation.ok:
            details = "; ".join(f"{issue.path}: {issue.message}" for issue in candidate_validation.issues)
            print(f"ERROR: Invalid seed candidate: {details}", file=sys.stderr)
            return 2
    if args.output:
        write_json(args.output, report)
        print(f"Wrote {Path(args.output)}")
    else:
        print(dump_json(report), end="")
    return 0 if report["status"] != "blocked" else 1


def _discovery_bridge(host: str, port: int, repo_root: str) -> int:
    try:
        serve_discovery_bridge(host, port, repo_root)
    except KeyboardInterrupt:
        return 0
    return 0


def _research_loop(args: argparse.Namespace) -> int:
    world_manifest = load_data(args.world_manifest)
    world_report = validate_data(world_manifest, args.world_manifest)
    if not world_report.ok:
        details = "; ".join(f"{issue.path}: {issue.message}" for issue in world_report.issues)
        print(f"ERROR: Invalid world manifest: {details}", file=sys.stderr)
        return 2
    runtime_bundle = load_data(args.runtime) if args.runtime else None
    if runtime_bundle is not None:
        runtime_report = validate_data(runtime_bundle, args.runtime or "<runtime>")
        if not runtime_report.ok:
            details = "; ".join(f"{issue.path}: {issue.message}" for issue in runtime_report.issues)
            print(f"ERROR: Invalid runtime bundle: {details}", file=sys.stderr)
            return 2
    try:
        report = run_research_loop(
            world_manifest,
            runtime_bundle,
            focus=args.focus,
            source_paths={
                "world_manifest": args.world_manifest,
                "runtime_bundle": args.runtime,
            },
            discovery_report_path=args.discovery_output,
            candidate_output_dir=args.candidate_output_dir,
            patch_output_dir=args.patch_output_dir,
            n8n_webhook=args.n8n_webhook,
            allow_seed_fallback=not args.no_seed_fallback,
        )
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    validation = validate_data(report, args.output or "<research-loop>")
    if not validation.ok:
        details = "; ".join(f"{issue.path}: {issue.message}" for issue in validation.issues)
        print(f"ERROR: Invalid research loop report: {details}", file=sys.stderr)
        return 2
    if args.output:
        write_json(args.output, report)
        print(f"Wrote {Path(args.output)}")
    else:
        print(dump_json(report), end="")
    return 0 if report["status"] != "blocked" else 1


def _materialize_patch(args: argparse.Namespace) -> int:
    patch_proposal = load_data(args.patch_proposal)
    patch_report = validate_data(patch_proposal, args.patch_proposal)
    if not patch_report.ok:
        details = "; ".join(f"{issue.path}: {issue.message}" for issue in patch_report.issues)
        print(f"ERROR: Invalid patch proposal: {details}", file=sys.stderr)
        return 2
    candidate = load_data(args.candidate) if args.candidate else None
    if candidate is not None:
        candidate_report = validate_data(candidate, args.candidate or "<candidate>")
        if not candidate_report.ok:
            details = "; ".join(f"{issue.path}: {issue.message}" for issue in candidate_report.issues)
            print(f"ERROR: Invalid discovery candidate: {details}", file=sys.stderr)
            return 2
    try:
        report = materialize_patch_proposal(
            patch_proposal,
            candidate,
            repo_root=args.repo_root,
            overwrite=args.overwrite,
            report_output=args.output,
        )
    except (FileNotFoundError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    if args.output:
        print(f"Wrote {Path(args.output)}")
    else:
        print(dump_json(report), end="")
    return 1 if report["status"] == "blocked" else 0


def _research_needs(
    compiled_plan_path: str,
    simulation_path: str,
    module_registry_path: str | None,
    output: str | None,
) -> int:
    registry = load_data(module_registry_path) if module_registry_path else None
    if registry is not None:
        registry_report = validate_data(registry, module_registry_path or "<module-registry>")
        if not registry_report.ok:
            details = "; ".join(f"{issue.path}: {issue.message}" for issue in registry_report.issues)
            print(f"ERROR: Invalid module registry: {details}", file=sys.stderr)
            return 2
    report = generate_research_needs(load_data(compiled_plan_path), load_data(simulation_path), registry)
    if output:
        write_json(output, report)
        print(f"Wrote {Path(output)}")
    else:
        print(dump_json(report), end="")
    return 0


def _export_research_registry(args: argparse.Namespace) -> int:
    capability_policy = load_data(args.capability_policy)
    report = validate_data(capability_policy, args.capability_policy)
    if not report.ok:
        details = "; ".join(f"{issue.path}: {issue.message}" for issue in report.issues)
        print(f"ERROR: Invalid capability policy: {details}", file=sys.stderr)
        return 2
    registry = build_research_registry(
        capability_policy,
        source_path=args.capability_policy,
        extra_research_inputs=args.research_input,
        scan_paths=args.scan_path,
    )
    try:
        write_research_registry(registry, args.output)
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    print(f"Wrote {Path(args.output)}")
    return 0


def _scalability_gate(
    compiled_plan_path: str,
    technology_module_path: str,
    module_registry_path: str | None,
    output: str | None,
) -> int:
    module = load_data(technology_module_path)
    module_report = validate_data(module, technology_module_path)
    if not module_report.ok:
        details = "; ".join(f"{issue.path}: {issue.message}" for issue in module_report.issues)
        print(f"ERROR: Invalid technology module: {details}", file=sys.stderr)
        return 2
    registry = load_data(module_registry_path) if module_registry_path else None
    if registry is not None:
        registry_report = validate_data(registry, module_registry_path or "<module-registry>")
        if not registry_report.ok:
            details = "; ".join(f"{issue.path}: {issue.message}" for issue in registry_report.issues)
            print(f"ERROR: Invalid module registry: {details}", file=sys.stderr)
            return 2
    report = evaluate_scalability_gate(load_data(compiled_plan_path), module, registry)
    if output:
        write_json(output, report)
        print(f"Wrote {Path(output)}")
    else:
        print(dump_json(report), end="")
    return 1 if report["status"] == "fail" else 0


def _implement_module(args: argparse.Namespace) -> int:
    module = load_data(args.technology_module)
    module_report = validate_data(module, args.technology_module)
    if not module_report.ok:
        details = "; ".join(f"{issue.path}: {issue.message}" for issue in module_report.issues)
        print(f"ERROR: Invalid technology module: {details}", file=sys.stderr)
        return 2
    registry = load_data(args.module_registry) if args.module_registry else None
    if registry is not None:
        registry_report = validate_data(registry, args.module_registry or "<module-registry>")
        if not registry_report.ok:
            details = "; ".join(f"{issue.path}: {issue.message}" for issue in registry_report.issues)
            print(f"ERROR: Invalid module registry: {details}", file=sys.stderr)
            return 2
    report = implement_technology_module(
        load_data(args.compiled_plan),
        module,
        registry,
        days=args.days,
        review_status=load_data(args.review_status) if args.review_status else None,
    )
    if args.output:
        write_json(args.output, report)
        print(f"Wrote {Path(args.output)}")
    else:
        print(dump_json(report), end="")
    return 1 if report["status"].startswith("blocked") or report["status"] == "implemented_with_regression" else 0


def _complexity_report(module_registry_path: str, pattern_dir: str, output: str | None) -> int:
    registry = load_data(module_registry_path)
    registry_report = validate_data(registry, module_registry_path)
    if not registry_report.ok:
        details = "; ".join(f"{issue.path}: {issue.message}" for issue in registry_report.issues)
        print(f"ERROR: Invalid module registry: {details}", file=sys.stderr)
        return 2
    try:
        report = generate_complexity_report(registry, load_patterns(pattern_dir))
    except CompileError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    if output:
        write_json(output, report)
        print(f"Wrote {Path(output)}")
    else:
        print(dump_json(report), end="")
    return 1 if report["status"] == "blocked" else 0


def _artifact_cohesion(generated_dir: str, output: str | None) -> int:
    report = evaluate_artifact_cohesion(generated_dir)
    if output:
        write_json(output, report)
        print(f"Wrote {Path(output)}")
    else:
        print(dump_json(report), end="")
    return 1 if report["status"] == "not_ready" else 0


def _viewer_server(host: str, port: int, repo_root: str) -> int:
    try:
        serve_viewer(host, port, repo_root)
    except KeyboardInterrupt:
        return 0
    return 0
