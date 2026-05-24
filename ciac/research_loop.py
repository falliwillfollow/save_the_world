from __future__ import annotations

import json
import re
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

from .discovery import build_discovery_loop
from .io import write_json
from .validation import validate_data


def run_research_loop(
    world_manifest: dict[str, Any],
    runtime_bundle: dict[str, Any] | None,
    *,
    focus: str,
    source_paths: dict[str, str | None],
    discovery_report_path: str | Path,
    candidate_output_dir: str | Path,
    patch_output_dir: str | Path,
    n8n_webhook: str | None = None,
    allow_seed_fallback: bool = True,
) -> dict[str, Any]:
    discovery_report = build_discovery_loop(
        world_manifest,
        runtime_bundle=runtime_bundle,
        focus=focus,
        source_paths=source_paths,
    )
    _require_valid(discovery_report, str(discovery_report_path))
    write_json(discovery_report_path, discovery_report)

    n8n_result: dict[str, Any] | None = None
    n8n_error: str | None = None
    if n8n_webhook:
        try:
            n8n_result = _post_json(
                n8n_webhook,
                {
                    "kind": "CIaCResearchLoopRequest",
                    "version": "v0",
                    "discovery_report_path": str(discovery_report_path),
                    "discovery_report": discovery_report,
                },
            )
        except (OSError, ValueError, urllib.error.URLError) as exc:
            n8n_error = str(exc)
            if not allow_seed_fallback:
                return _blocked_run(
                    discovery_report,
                    source_paths,
                    focus,
                    str(discovery_report_path),
                    n8n_webhook,
                    n8n_error,
                )

    webhook_candidates = _extract_candidates(n8n_result) if n8n_result else []
    candidates = webhook_candidates or discovery_report.get("seed_candidates", [])
    candidate_source = "n8n_webhook" if webhook_candidates else "seed_candidates"

    candidate_records = []
    patch_records = []
    for raw_candidate in candidates:
        candidate = _normalized_candidate(raw_candidate)
        candidate_id = _safe_id(candidate.get("id", "candidate"))
        candidate_validation = validate_data(candidate, candidate_id)
        candidate_path = Path(candidate_output_dir) / f"{candidate_id}.json"
        write_json(candidate_path, candidate)
        candidate_records.append(
            {
                "id": candidate_id,
                "path": str(candidate_path),
                "status": "valid" if candidate_validation.ok else "invalid",
            }
        )

        patch = build_patch_proposal(candidate, candidate_validation.ok)
        patch_validation = validate_data(patch, patch["id"])
        if not patch_validation.ok:
            messages = [f"{issue.path}: {issue.message}" for issue in patch_validation.issues]
            patch["status"] = "blocked"
            patch["validation"]["blocking_reasons"].extend(messages)
        patch_path = Path(patch_output_dir) / f"{patch['id']}.json"
        write_json(patch_path, patch)
        patch_records.append({"id": patch["id"], "path": str(patch_path), "status": patch["status"]})

    status = "ready_for_review" if candidates else "blocked"
    run = {
        "kind": "ResearchLoopRun",
        "version": "v0",
        "id": f"research_{discovery_report['id']}",
        "status": status,
        "source": {
            "world_manifest_path": source_paths.get("world_manifest"),
            "runtime_bundle_path": source_paths.get("runtime_bundle"),
            "focus": focus,
        },
        "discovery_report_path": str(discovery_report_path),
        "candidate_source": candidate_source,
        "candidates_written": candidate_records,
        "patch_proposals_written": patch_records,
        "n8n": {
            "webhook_url": n8n_webhook,
            "called": n8n_webhook is not None,
            "ok": n8n_result is not None,
            "error": n8n_error,
            **_n8n_metadata(n8n_result, len(webhook_candidates)),
        },
        "next_actions": [
            "Review generated PatchProposal artifacts before applying any model change.",
            "Run scenario checks listed in each patch proposal.",
            "Promote only proposals that reduce the triggering warning without adding hidden labor or survival-critical unmet demand.",
        ],
        "provisional": True,
    }
    _require_valid(run, run["id"])
    return run


def build_patch_proposal(candidate: dict[str, Any], schema_valid: bool = True) -> dict[str, Any]:
    candidate = _normalized_candidate(candidate)
    candidate_id = _safe_id(candidate.get("id", "candidate"))
    focus_domain = candidate.get("focus_domain", "unknown")
    simulation_hooks = candidate.get("simulation_hooks", {})
    warnings = _patch_warnings(candidate)
    blocking_reasons = [] if schema_valid else ["Source candidate does not satisfy DiscoveryCandidateIntervention schema."]
    status = "blocked" if blocking_reasons else "needs_evidence" if warnings else "simulation_ready"
    change_type = _change_type(candidate.get("intervention_type"))
    return {
        "kind": "PatchProposal",
        "version": "v0",
        "id": f"patch_{candidate_id}",
        "source_candidate_id": candidate_id,
        "source_loop_id": candidate.get("source_loop_id", "unknown_loop"),
        "focus_domain": focus_domain,
        "title": candidate.get("title", candidate_id),
        "status": status,
        "target": {
            "artifact": _target_artifact(focus_domain, candidate_id, change_type),
            "change_type": change_type,
        },
        "model_changes": _model_changes(candidate),
        "simulation_checks": list(simulation_hooks.get("scenarios_to_run", []))
        + list(simulation_hooks.get("metrics_to_compare", [])),
        "acceptance_tests": list(simulation_hooks.get("acceptance_tests", [])),
        "validation": {
            "schema_valid": schema_valid,
            "blocking_reasons": blocking_reasons,
            "warnings": warnings,
        },
        "implementation_notes": [
            "Patch proposal is an implementation intent artifact, not an automatic mutation.",
            "Model changes should be applied through a dedicated promotion command after simulation comparison.",
            candidate.get("hypothesis", "No candidate hypothesis was provided."),
        ],
        "provisional": True,
    }


def _post_json(url: str, payload: dict[str, Any]) -> dict[str, Any]:
    body = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(url, data=body, headers={"Content-Type": "application/json"}, method="POST")
    with urllib.request.urlopen(request, timeout=240) as response:
        text = response.read().decode("utf-8")
    data = json.loads(text) if text else {}
    if not isinstance(data, dict):
        raise ValueError("n8n webhook response must be a JSON object")
    return data


def _extract_candidates(data: dict[str, Any] | None) -> list[dict[str, Any]]:
    if not data:
        return []
    candidates = data.get("candidate_interventions") or data.get("candidates")
    if isinstance(candidates, list):
        return [item for item in candidates if isinstance(item, dict)]
    report = data.get("report")
    if isinstance(report, dict) and isinstance(report.get("seed_candidates"), list):
        return [item for item in report["seed_candidates"] if isinstance(item, dict)]
    if isinstance(data.get("json"), dict):
        return _extract_candidates(data["json"])
    if isinstance(data.get("body"), dict):
        return _extract_candidates(data["body"])
    return []


def _model_changes(candidate: dict[str, Any]) -> list[dict[str, Any]]:
    candidate_id = _safe_id(candidate.get("id", "candidate"))
    focus_domain = candidate.get("focus_domain", "unknown")
    changes = [
        {
            "path": f"capabilities.{focus_domain}.tracked_interventions.{candidate_id}",
            "from": False,
            "to": True,
            "rationale": "Make the candidate intervention explicit in the capability layer before promotion.",
            "provisional": True,
        }
    ]
    for effect in candidate.get("expected_effects", []):
        metric = _safe_id(effect.get("metric", "metric"))
        changes.append(
            {
                "path": f"candidate_effects.{candidate_id}.{metric}",
                "from": None,
                "to": effect.get("direction", "unknown"),
                "rationale": effect.get("rationale", "Expected effect declared by candidate."),
                "provisional": True,
            }
        )
    return changes


def _normalized_candidate(candidate: dict[str, Any]) -> dict[str, Any]:
    normalized = dict(candidate)
    effects = []
    for effect in candidate.get("expected_effects", []):
        item = dict(effect)
        item["direction"] = _normalized_effect_direction(item.get("direction"))
        effects.append(item)
    if effects:
        normalized["expected_effects"] = effects
    return normalized


def _normalized_effect_direction(value: Any) -> str:
    direction = str(value or "unknown").strip().lower()
    if direction in {"increase", "decrease", "neutral", "unknown"}:
        return direction
    if direction in {"pass", "passed", "improve", "improved", "improvement", "resolve", "resolved"}:
        return "increase"
    if direction in {"fail", "failed", "worsen", "worse", "regress", "regressed"}:
        return "decrease"
    if direction in {"stable", "same", "unchanged", "maintain", "maintained"}:
        return "neutral"
    return "unknown"


def _patch_warnings(candidate: dict[str, Any]) -> list[str]:
    warnings = []
    rag_context = candidate.get("rag_context", {})
    if not rag_context.get("source_ids"):
        warnings.append("Candidate has no retrieved source_ids yet.")
    for assumption in candidate.get("assumptions", []):
        if assumption.get("needs_evidence"):
            warnings.append(f"Assumption requires evidence: {assumption.get('id', '<unknown>')}")
    if not candidate.get("simulation_hooks", {}).get("scenarios_to_run"):
        warnings.append("Candidate does not declare scenario checks.")
    return warnings


def _change_type(intervention_type: str | None) -> str:
    return {
        "pattern_patch": "update_pattern",
        "module_candidate": "add_module",
        "operating_protocol": "add_operating_protocol",
        "scenario_playbook": "add_scenario_playbook",
        "governance_rule": "add_governance_rule",
        "research_task": "add_research_task",
    }.get(intervention_type or "", "add_pattern")


def _target_artifact(focus_domain: str, candidate_id: str, change_type: str) -> str:
    if change_type in {"add_operating_protocol", "add_governance_rule"}:
        return f"patterns/{focus_domain}/{candidate_id}.yaml"
    if change_type == "add_scenario_playbook":
        return f"scenarios/{candidate_id}.yaml"
    if change_type == "add_module":
        return f"tech_modules/{candidate_id}.yaml"
    if change_type == "add_research_task":
        return f"docs/research/{candidate_id}.md"
    return f"patterns/{focus_domain}/{candidate_id}.yaml"


def _blocked_run(
    discovery_report: dict[str, Any],
    source_paths: dict[str, str | None],
    focus: str,
    discovery_report_path: str,
    n8n_webhook: str,
    error: str,
) -> dict[str, Any]:
    return {
        "kind": "ResearchLoopRun",
        "version": "v0",
        "id": f"research_{discovery_report['id']}",
        "status": "blocked",
        "source": {
            "world_manifest_path": source_paths.get("world_manifest"),
            "runtime_bundle_path": source_paths.get("runtime_bundle"),
            "focus": focus,
        },
        "discovery_report_path": discovery_report_path,
        "candidate_source": "seed_candidates",
        "candidates_written": [],
        "patch_proposals_written": [],
        "n8n": {
            "webhook_url": n8n_webhook,
            "called": True,
            "ok": False,
            "error": error,
            "workflow_name": None,
            "trace_marker": None,
            "discovery_brief": None,
            "candidate_count": 0,
            "context_source_ids": [],
        },
        "next_actions": ["Fix the n8n webhook or rerun with seed fallback enabled."],
        "provisional": True,
    }


def _require_valid(data: dict[str, Any], path: str) -> None:
    report = validate_data(data, path)
    if not report.ok:
        details = "; ".join(f"{issue.path}: {issue.message}" for issue in report.issues)
        raise ValueError(f"Invalid {data.get('kind', 'artifact')}: {details}")


def _safe_id(value: Any) -> str:
    return re.sub(r"[^a-z0-9_]+", "_", str(value).lower()).strip("_") or "artifact"


def _n8n_metadata(data: dict[str, Any] | None, candidate_count: int) -> dict[str, Any]:
    if not data:
        return {
            "workflow_name": None,
            "trace_marker": None,
            "discovery_brief": None,
            "candidate_count": 0,
            "context_source_ids": [],
        }
    brief = data.get("discovery_brief") if isinstance(data.get("discovery_brief"), dict) else None
    return {
        "workflow_name": data.get("workflow_name") or data.get("source"),
        "trace_marker": data.get("trace_marker"),
        "discovery_brief": brief,
        "candidate_count": int(data.get("candidate_count", candidate_count) or candidate_count),
        "context_source_ids": [str(item) for item in data.get("context_source_ids", []) if isinstance(item, str)],
    }
