from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .audit import evaluate_audit
from .candidates import generate_candidate_matrix
from .compare import compare_audits
from .compiler import CompileError, compile_plan, load_patterns
from .cycle import materialize_search_candidate
from .dossier import generate_dossier
from .energy import evaluate_energy
from .export_md import render_review_packet, write_review_packet
from .foundation import evaluate_foundation_gate
from .gates import evaluate_gates
from .io import dump_json, load_data, write_json
from .matrix_redesign import generate_matrix_redesign
from .module_implementation import implement_technology_module
from .nutrition import evaluate_nutrition
from .objective_calibration import evaluate_objective_calibration
from .optimization import evaluate_optimization_readiness
from .optimizer import optimize_candidates
from .redesign import generate_redesign
from .research import evaluate_scalability_gate, generate_research_needs
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
from .validation import validate_data, validate_path
from .visualization_bundle import build_visualization_bundle
from .water import evaluate_water
from .weight_governance import evaluate_weight_governance


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
    if args.command == "optimize":
        return _optimize(args)
    if args.command == "export-visualization":
        return _export_visualization(args)
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
    if args.command == "scalability-gate":
        return _scalability_gate(args.compiled_plan, args.technology_module, args.module_registry, args.output)
    if args.command == "implement-module":
        return _implement_module(args)
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
