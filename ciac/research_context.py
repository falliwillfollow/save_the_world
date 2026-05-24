from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from .validation import schema_dir


SEARCH_ROOTS = [
    "patterns",
    "docs/module_reports",
    "docs",
    "examples/generated",
    "examples/world_manifests",
    "scenarios",
    "schemas",
]


def build_research_context(repo_root: str | Path, discovery_report: dict[str, Any]) -> dict[str, Any]:
    root = Path(repo_root).resolve()
    focus = discovery_report.get("focus", "all")
    findings = discovery_report.get("findings", [])
    queries = [item.get("query", "") for item in discovery_report.get("retrieval_plan", []) if item.get("query")]
    if not queries:
        queries = [f"CIaC {focus} interventions expected effects risk simulation"]
    snippets = _retrieve_snippets(root, queries, findings)
    candidate_schema = json.loads((schema_dir() / "discovery_candidate_intervention.schema.json").read_text(encoding="utf-8"))
    prompt = _candidate_prompt(discovery_report, snippets, candidate_schema)
    return {
        "kind": "CIaCResearchContext",
        "version": "v0",
        "focus": focus,
        "discovery_report_id": discovery_report.get("id"),
        "context_source_ids": [snippet["source_id"] for snippet in snippets],
        "context_snippets": snippets,
        "candidate_schema": candidate_schema,
        "seed_candidates": discovery_report.get("seed_candidates", []),
        "prompt": prompt,
    }


def _retrieve_snippets(root: Path, queries: list[str], findings: list[dict[str, Any]]) -> list[dict[str, str]]:
    terms = _terms(queries, findings)
    scored = []
    for search_root in SEARCH_ROOTS:
        directory = root / search_root
        if not directory.exists():
            continue
        for path in directory.rglob("*"):
            if path.suffix.lower() not in {".md", ".json", ".yaml", ".yml"} or not path.is_file():
                continue
            try:
                text = path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue
            score = _score(text, path, terms)
            if score <= 0:
                continue
            scored.append((score, path, text))
    snippets = []
    for score, path, text in sorted(scored, key=lambda item: item[0], reverse=True)[:8]:
        rel = path.relative_to(root).as_posix()
        snippets.append(
            {
                "source_id": rel,
                "score": str(score),
                "excerpt": _excerpt(text, terms),
            }
        )
    return snippets


def _candidate_prompt(discovery_report: dict[str, Any], snippets: list[dict[str, str]], candidate_schema: dict[str, Any]) -> str:
    payload = {
        "discovery_report": {
            "id": discovery_report.get("id"),
            "focus": discovery_report.get("focus"),
            "findings": discovery_report.get("findings", []),
            "evaluation_contract": discovery_report.get("evaluation_contract", {}),
            "seed_candidates": discovery_report.get("seed_candidates", []),
        },
        "retrieved_context": snippets,
        "candidate_schema": candidate_schema,
    }
    return (
        "You are the CIaC local research loop. Use only the provided DiscoveryLoopReport and retrieved context. "
        "Return exactly one JSON object with keys: workflow_name, trace_marker, discovery_brief, candidate_interventions. "
        "candidate_interventions must be an array of 2 or 3 valid DiscoveryCandidateIntervention objects. "
        "Use the seed candidates only as templates; enrich or revise them using retrieved context. "
        "Every returned candidate must include rag_context.source_ids copied from retrieved_context source_id values, "
        "status='generated', provisional=true, explicit assumptions, expected_effects, risk_tradeoffs, and simulation_hooks. "
        "Do not claim safety, legality, medical validity, public-health approval, engineering validity, or resident consent. "
        "No markdown. JSON only.\n\n"
        + json.dumps(payload, separators=(",", ":"))
    )


def _terms(queries: list[str], findings: list[dict[str, Any]]) -> set[str]:
    text = " ".join(queries)
    for finding in findings:
        text += " " + str(finding.get("domain", ""))
        text += " " + str(finding.get("summary", ""))
        text += " " + " ".join(finding.get("evidence", []))
        text += " " + " ".join(finding.get("module_refs", []))
    words = re.findall(r"[a-zA-Z][a-zA-Z0-9_]{2,}", text.lower())
    stop = {"the", "and", "for", "with", "this", "that", "from", "into", "ciac", "v0", "v1"}
    return {word for word in words if word not in stop}


def _score(text: str, path: Path, terms: set[str]) -> int:
    lowered = text.lower()
    haystack = lowered + " " + path.as_posix().lower()
    return sum(haystack.count(term) for term in terms)


def _excerpt(text: str, terms: set[str]) -> str:
    clean = re.sub(r"\s+", " ", text).strip()
    if not clean:
        return ""
    lowered = clean.lower()
    first_index = min((lowered.find(term) for term in terms if lowered.find(term) >= 0), default=0)
    start = max(0, first_index - 220)
    end = min(len(clean), first_index + 620)
    excerpt = clean[start:end]
    if start:
        excerpt = "..." + excerpt
    if end < len(clean):
        excerpt += "..."
    return excerpt
