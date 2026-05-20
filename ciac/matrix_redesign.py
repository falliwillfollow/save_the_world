from __future__ import annotations

from typing import Any


def generate_matrix_redesign(compiled_plan: dict[str, Any], replay_matrix: dict[str, Any]) -> dict[str, Any]:
    entries = replay_matrix.get("rankings", replay_matrix.get("entries", []))
    candidates = _candidates(entries)
    priority_order = [candidate["id"] for candidate in candidates]
    return {
        "kind": "MatrixRedesignReport",
        "id": f"{compiled_plan['id']}_matrix_redesign",
        "compiled_plan": compiled_plan["id"],
        "replay_matrix": replay_matrix["id"],
        "generated_by": "ciac.matrix_redesign.v0",
        "provisional": True,
        "status": "ready_for_iteration" if candidates else "draft",
        "top_stressor": replay_matrix.get("top_stressor", {}),
        "redesign_candidates": candidates,
        "priority_order": priority_order,
        "next_actions": _next_actions(priority_order),
        "unknowns": [
            "Matrix redesign candidates are planning prompts, not engineering, public-health, legal, or governance approval.",
            "Candidates are based on generated replay comparison artifacts and inherit all provisional scenario assumptions.",
            "Recommended changes must be edited into source YAML and verified by rerunning compile, simulation replays, comparisons, and matrix ranking.",
        ],
    }


def _candidates(entries: list[dict[str, Any]]) -> list[dict[str, Any]]:
    candidates: list[dict[str, Any]] = []
    scenarios = {entry["scenario"]: entry for entry in entries}
    top_total = entries[0] if entries else {}
    top_per_day = max(entries, key=lambda item: float(item.get("stress_score_per_day", 0.0)), default={})
    if _food_reserve_still_bottleneck(entries):
        candidates.append(_food_reserve_candidate(scenarios.get("crop_failure", top_total)))
    elif _food_model_still_partial(entries):
        candidates.append(_food_model_closure_candidate(scenarios.get("crop_failure", top_total)))
    if _water_still_bottleneck(entries):
        candidates.append(_water_response_candidate(entries))
    if top_per_day.get("scenario") == "energy_outage_reserve_v2" or "energy_outage_reserve_v2" in scenarios:
        candidates.append(_energy_intensity_candidate(scenarios.get("energy_outage_reserve_v2", top_per_day)))
    if _labor_still_bottleneck(entries):
        candidates.append(_labor_surge_candidate(entries))
    if any(int(entry.get("blocked_review_domain_count", 0)) > 0 for entry in entries):
        candidates.append(_review_evidence_candidate(entries))
    return _renumber(_dedupe(candidates))


def _food_reserve_candidate(entry: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": "food_staple_reserve_and_procurement_floor",
        "subsystem": "food",
        "priority": 10,
        "target_scenarios": ["crop_failure"],
        "target_metric": "Reduce long-duration food and labor stress from crop failure replay.",
        "proposal": "Add a plain staple reserve and procurement floor for crop-failure mode before expanding local production complexity.",
        "minimum_viable_change": [
            "Model shelf-stable staple days as inventory, not daily production.",
            "Add a conservative procurement fallback task with lead time and role owner.",
            "Keep greenhouse failure active but reduce unmet food/labor pressure through reserve drawdown.",
        ],
        "expected_effect": [
            "Reduces crop_failure total stress score.",
            "Reduces food or labor unmet-demand deltas during long replays.",
            "Preserves minimum dignified existence without overdesigning agriculture.",
        ],
        "tradeoffs": [
            "External staples reduce autonomy.",
            "Stored food requires rotation, pest control, cultural acceptability, and food-safety review.",
        ],
        "files_to_edit": [
            "patterns/staple_food_reserve.yaml",
            "food_plans/micro_commons_basic.yaml",
            "scenarios/crop_failure.yaml",
        ],
        "acceptance_criteria": [
            "crop_failure replay comparison remains non-fail or materially lowers total_unmet_delta.",
            "micro_commons_replay_matrix no longer ranks crop_failure as the top total stressor, or its score drops by at least 25%.",
            "No new labor or review blocker is introduced.",
        ],
        "evidence": _entry_evidence(entry),
    }


def _food_model_closure_candidate(entry: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": "food_model_closure_and_recovery_clock",
        "subsystem": "food",
        "priority": 10,
        "target_scenarios": ["crop_failure"],
        "target_metric": "Replace the partial food-model warning with explicit nutrition coverage, reserve rotation, and crop-recovery timing.",
        "proposal": "Close the minimum viable food model before adding more agricultural complexity.",
        "minimum_viable_change": [
            "Declare which food servings are staples, fresh produce, emergency reserve, or external procurement.",
            "Add a simple recovery clock for crop failure: reserve drawdown, procurement bridge, replanting window, and return-to-normal criteria.",
            "Keep all nutrition, food safety, and procurement assumptions provisional until reviewed.",
        ],
        "expected_effect": [
            "Turns the current food-model warning into measurable food coverage states.",
            "Reduces ambiguous active failure-day pressure in crop_failure replay.",
            "Improves simulation readiness without requiring detailed crop science or visual buildout.",
        ],
        "tradeoffs": [
            "A simple food model will still be less autonomous than a complete production model.",
            "External procurement remains a dependency and must stay visible.",
        ],
        "files_to_edit": [
            "nutrition_plans/micro_commons_basic.yaml",
            "food_plans/micro_commons_basic.yaml",
            "scenarios/crop_failure.yaml",
            "ciac/simulation.py",
        ],
        "acceptance_criteria": [
            "crop_failure replay keeps total_unmet_delta at 0.",
            "The generic partial-food-model bottleneck is replaced by explicit food coverage and recovery-state evidence.",
            "The crop_failure active_failure_day_delta drops or is explained by an explicit recovery clock.",
        ],
        "evidence": _entry_evidence(entry),
    }


def _water_response_candidate(entries: list[dict[str, Any]]) -> dict[str, Any]:
    target_entries = [
        entry
        for entry in entries
        if entry["scenario"] in {"water_contamination_response_v2", "drought_reserve_v2", "sanitation_failure"}
    ]
    return {
        "id": "water_response_buffer_and_isolation_floor",
        "subsystem": "water",
        "priority": 20,
        "target_scenarios": [entry["scenario"] for entry in target_entries],
        "target_metric": "Reduce water unmet demand and failure-day pressure during contamination, drought, and sanitation stress.",
        "proposal": "Add a minimum response buffer: isolate unsafe sources, preserve a small protected potable reserve, and define rationing thresholds.",
        "minimum_viable_change": [
            "Separate protected potable emergency reserve from ordinary water drawdown.",
            "Add daily rationing threshold and mutual-aid/haul trigger for contamination and drought scenarios.",
            "Make retest failure keep recovery blocked while still preserving minimum drinking/cooking/hygiene allocations.",
        ],
        "expected_effect": [
            "Reduces water_contamination_response_v2 unmet water delta.",
            "Reduces drought_reserve_v2 water negative-balance bottleneck.",
            "Keeps sanitation response from consuming the same protected potable reserve.",
        ],
        "tradeoffs": [
            "May increase storage footprint and inspection burden.",
            "Mutual-aid or hauled water adds external dependency.",
        ],
        "files_to_edit": [
            "patterns/emergency_water_reserve.yaml",
            "water_plans/micro_commons_water_reserve_v2.yaml",
            "scenarios/water_contamination_response_v2.yaml",
            "scenarios/drought_reserve_v2.yaml",
            "scenarios/sanitation_failure.yaml",
        ],
        "acceptance_criteria": [
            "water_contamination_response_v2 total_unmet_delta drops below current value.",
            "drought_reserve_v2 no longer reports water_liters negative daily balance, or the matrix score drops by at least 25%.",
            "Recovery remains blocked when review fails; only minimum reserve allocation improves.",
        ],
        "evidence": [_entry_evidence(entry) for entry in target_entries],
    }


def _energy_intensity_candidate(entry: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": "energy_outage_short_window_load_shed",
        "subsystem": "energy",
        "priority": 30,
        "target_scenarios": ["energy_outage_reserve_v2"],
        "target_metric": "Reduce highest per-day stress from short energy outage replay.",
        "proposal": "Tighten emergency load shedding and backup charging for the first outage week before adding larger energy infrastructure.",
        "minimum_viable_change": [
            "Move noncritical energy use to explicit outage-off state.",
            "Add manual fallback for one or two low-risk loads where labor impact is acceptable.",
            "Model a small constrained backup charging/import path for critical devices only.",
        ],
        "expected_effect": [
            "Reduces energy_outage_reserve_v2 per-day stress score.",
            "Reduces labor_hours unmet demand caused by response overload.",
            "Avoids premature large-system redesign.",
        ],
        "tradeoffs": [
            "Manual fallback can shift burden to residents.",
            "Backup charging may create fuel, transport, noise, or safety dependencies.",
        ],
        "files_to_edit": [
            "energy_plans/micro_commons_energy_reserve_v2.yaml",
            "scenarios/energy_outage_reserve_v2.yaml",
            "role_plans/micro_commons_roles_v2.yaml",
        ],
        "acceptance_criteria": [
            "energy_outage_reserve_v2 stress_score_per_day drops by at least 25%.",
            "Labor status does not regress under outage replay.",
            "Electrical review dependency remains explicit.",
        ],
        "evidence": _entry_evidence(entry),
    }


def _labor_surge_candidate(entries: list[dict[str, Any]]) -> dict[str, Any]:
    worst = max(entries, key=lambda item: float(item.get("scenario_emergency_hours", 0.0)), default={})
    return {
        "id": "scenario_labor_surge_buffer",
        "subsystem": "labor",
        "priority": 15,
        "target_scenarios": [entry["scenario"] for entry in entries if float(entry.get("scenario_emergency_hours", 0.0)) > 0],
        "target_metric": "Reduce emergency labor spikes and labor_hours unmet demand across replays.",
        "proposal": "Create a small mutual-aid and pause-noncritical-work buffer for scenario response days.",
        "minimum_viable_change": [
            "Declare which maintenance tasks can pause during emergency response.",
            "Add a mutual-aid role or outside support placeholder for high-hour response days.",
            "Cap per-day emergency work to avoid silently exceeding available commons labor.",
        ],
        "expected_effect": [
            "Reduces labor_hours unmet-demand deltas.",
            "Makes emergency response burden visible before visual buildout.",
            "Protects care-loaded residents from being treated as hidden spare capacity.",
        ],
        "tradeoffs": [
            "Deferred maintenance can increase degradation if pauses last too long.",
            "Mutual aid is an external dependency and needs governance agreement.",
        ],
        "files_to_edit": [
            "role_plans/micro_commons_roles_v2.yaml",
            "scenarios/*.yaml",
            "patterns/*reserve*.yaml",
        ],
        "acceptance_criteria": [
            "No replay comparison reports labor_hours total_unmet_delta above the current matrix baseline.",
            "resident_exit_labor_loss score drops or no longer stress-fails solely from labor capacity.",
            "Care and protected labor assumptions remain visible in role report.",
        ],
        "evidence": _entry_evidence(worst),
    }


def _review_evidence_candidate(entries: list[dict[str, Any]]) -> dict[str, Any]:
    affected = [entry["scenario"] for entry in entries if int(entry.get("blocked_review_domain_count", 0)) > 0]
    return {
        "id": "review_evidence_minimum_register",
        "subsystem": "review",
        "priority": 50,
        "target_scenarios": affected,
        "target_metric": "Reduce unresolved review context that keeps recovery non-promotable.",
        "proposal": "Fill the review register with current evidence status for survival-critical domains, while preserving failed-retest blocks.",
        "minimum_viable_change": [
            "Separate globally missing review evidence from scenario-specific failed retests.",
            "Add placeholder status for who must review water, sanitation, electrical, structural, food safety, accessibility, governance/legal, and insurance/liability.",
            "Keep accepted evidence from implying legal approval or professional certification.",
        ],
        "expected_effect": [
            "Makes blocked domains specific instead of broad.",
            "Improves recovery-state interpretation in replay comparisons.",
            "Prevents false confidence by keeping failed scenario review events active.",
        ],
        "tradeoffs": [
            "Requires disciplined evidence tracking.",
            "May reveal more external dependencies before pilot readiness.",
        ],
        "files_to_edit": [
            "review_registers/micro_commons_placeholder.yaml",
            "reports/micro_commons_review_packet.md",
        ],
        "acceptance_criteria": [
            "Review status distinguishes missing evidence from rejected, expired, or scenario-blocked evidence.",
            "Replay matrix blocked_review_domain_count decreases for non-scenario domains.",
            "water_contamination_response_v2 still blocks water_public_health when failed_retest is active.",
        ],
        "evidence": [
            _entry_evidence(entry)
            for entry in entries
            if int(entry.get("blocked_review_domain_count", 0)) > 0
        ],
    }


def _entry_evidence(entry: dict[str, Any]) -> dict[str, Any]:
    return {
        "scenario": entry.get("scenario", ""),
        "status": entry.get("status", ""),
        "stress_score": entry.get("stress_score", 0),
        "stress_score_per_day": entry.get("stress_score_per_day", 0),
        "total_unmet_delta": entry.get("total_unmet_delta", 0),
        "scenario_emergency_hours": entry.get("scenario_emergency_hours", 0),
        "active_failure_day_delta": entry.get("active_failure_day_delta", 0),
        "blocked_review_domain_count": entry.get("blocked_review_domain_count", 0),
        "top_bottlenecks": entry.get("top_bottlenecks", []),
    }


def _all_bottlenecks(entries: list[dict[str, Any]]) -> str:
    return " ".join(
        bottleneck
        for entry in entries
        for bottleneck in entry.get("top_bottlenecks", [])
    ).lower()


def _food_reserve_still_bottleneck(entries: list[dict[str, Any]]) -> bool:
    bottlenecks = _all_bottlenecks(entries)
    return "food_servings unmet demand" in bottlenecks


def _food_model_still_partial(entries: list[dict[str, Any]]) -> bool:
    if not entries:
        return False
    top = entries[0]
    return top.get("scenario") == "crop_failure" or "food model is partial" in _all_bottlenecks(entries)


def _water_still_bottleneck(entries: list[dict[str, Any]]) -> bool:
    water_scenarios = {"water_contamination_response_v2", "drought_reserve_v2", "sanitation_failure"}
    for entry in entries:
        if entry["scenario"] not in water_scenarios:
            continue
        if any("water_liters" in bottleneck for bottleneck in entry.get("top_bottlenecks", [])):
            return True
    return False


def _labor_still_bottleneck(entries: list[dict[str, Any]]) -> bool:
    for entry in entries:
        bottlenecks = " ".join(entry.get("top_bottlenecks", [])).lower()
        if "labor_hours unmet demand" in bottlenecks:
            return True
    return False


def _dedupe(candidates: list[dict[str, Any]]) -> list[dict[str, Any]]:
    seen: set[str] = set()
    unique: list[dict[str, Any]] = []
    for candidate in candidates:
        if candidate["id"] in seen:
            continue
        seen.add(candidate["id"])
        unique.append(candidate)
    return unique


def _renumber(candidates: list[dict[str, Any]]) -> list[dict[str, Any]]:
    ordered = sorted(candidates, key=lambda item: item["priority"])
    for index, candidate in enumerate(ordered, start=1):
        candidate["priority"] = index
    return ordered


def _next_actions(priority_order: list[str]) -> list[str]:
    if not priority_order:
        return ["No matrix redesign candidates were generated; add replay comparisons first."]
    return [
        f"Implement candidate {priority_order[0]} first as a YAML/data change.",
        "Regenerate affected scenario replays, simulation comparisons, and the replay matrix.",
        "Accept a candidate only if it reduces stress without hiding review, labor, or governance blockers.",
    ]
