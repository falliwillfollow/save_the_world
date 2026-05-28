from __future__ import annotations

from collections import defaultdict
import hashlib
from pathlib import Path
import re
from typing import Any
from urllib.parse import urlparse

import yaml

from .io import write_json
from .validation import validate_data


def build_research_registry(
    capability_policy: dict[str, Any],
    *,
    source_path: str | None = None,
    extra_research_inputs: list[str] | None = None,
    scan_paths: list[str] | None = None,
) -> dict[str, Any]:
    sources = {source["id"]: source for source in capability_policy.get("source_registry", [])}
    domains_by_source: dict[str, set[str]] = defaultdict(set)
    fields_by_source: dict[str, set[str]] = defaultdict(set)
    gates_by_source: dict[str, set[str]] = defaultdict(set)
    claims_by_source: dict[str, set[str]] = defaultdict(set)
    used_by_by_source: dict[str, set[str]] = defaultdict(set)

    if source_path:
        for source_id in sources:
            used_by_by_source[source_id].add(source_path)

    for domain, policy in capability_policy.get("domains", {}).items():
        for gate in policy.get("gates", []):
            for source_id in gate.get("source_ids", []):
                domains_by_source[source_id].add(domain)
                fields_by_source[source_id].add(str(gate.get("capability_field", "")))
                gates_by_source[source_id].add(str(gate.get("gate_id", "")))
                claims_by_source[source_id].add(str(gate.get("message", "")))
                used_by_by_source[source_id].add(f"capability_policy_gate:{gate.get('gate_id', '')}")

    scanned_documents = sorted(
        {
            *(capability_policy.get("research_inputs", []) or []),
            *(extra_research_inputs or []),
            *(scan_paths or []),
        }
    )
    for document_path in _iter_research_documents(scanned_documents):
        for source in extract_sources_from_document(document_path):
            source_id = source["id"]
            existing = sources.get(source_id)
            if existing:
                sources[source_id] = _merge_source(existing, source)
            else:
                sources[source_id] = source
            used_by_by_source[source_id].update(source.get("used_by", []))
            for domain in source.get("domains", []):
                domains_by_source[source_id].add(domain)

    entries = []
    for source_id, source in sorted(sources.items()):
        entries.append(
            {
                "id": source_id,
                "source_type": _source_type(source),
                "title": source.get("title"),
                "organization": source.get("organization"),
                "url": source.get("url"),
                "evidence_quality": source.get("evidence_quality", "mixed"),
                "supports": sorted(set(source.get("supports", []))),
                "domains": _clean_domains([*source.get("domains", []), *domains_by_source[source_id]]),
                "claims_supported": sorted(item for item in claims_by_source[source_id] if item),
                "model_fields": sorted(item for item in fields_by_source[source_id] if item),
                "used_by": sorted(item for item in used_by_by_source[source_id] if item),
                "notes": _source_notes(source, domains_by_source[source_id]),
            }
        )

    return {
        "kind": "ResearchRegistry",
        "version": "v0",
        "registry_id": "ciac_research_registry_v0",
        "status": "provisional",
        "source_documents": [str(path) for path in _iter_research_documents(scanned_documents)],
        "entries": entries,
        "warnings": [
            "This registry tracks CIaC model provenance. It does not independently verify legal, engineering, clinical, public-health, accessibility, or resident-consent sufficiency.",
            "Sources are attached to model claims and gates; they are not approvals to build or operate real infrastructure.",
        ],
    }


def extract_sources_from_document(path: str | Path) -> list[dict[str, Any]]:
    document = Path(path)
    text = document.read_text(encoding="utf-8")
    structured = _extract_structured_sources(text, document)
    by_url = {source.get("url"): source for source in structured if source.get("url")}
    fallback = []
    for line_number, line in enumerate(text.splitlines(), start=1):
        for url in _urls_in_line(line):
            if url in by_url:
                continue
            fallback.append(_fallback_source(url, line, document, line_number))
    by_id: dict[str, dict[str, Any]] = {}
    for source in [*structured, *fallback]:
        source_id = source["id"]
        by_id[source_id] = _merge_source(by_id[source_id], source) if source_id in by_id else source
    return sorted(by_id.values(), key=lambda source: source["id"])


def write_research_registry(registry: dict[str, Any], path: str | Path) -> None:
    report = validate_data(registry, str(path))
    if not report.ok:
        details = "; ".join(f"{issue.path}: {issue.message}" for issue in report.issues)
        raise ValueError(f"Invalid research registry: {details}")
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.suffix.lower() in {".yaml", ".yml"}:
        target.write_text(yaml.safe_dump(registry, sort_keys=False, allow_unicode=False), encoding="utf-8")
    else:
        write_json(target, registry)


def _source_type(source: dict[str, Any]) -> str:
    org = str(source.get("organization", "")).lower()
    title = str(source.get("title", "")).lower()
    if "survey" in title or "dataset" in title or "bureau of labor statistics" in org:
        return "dataset"
    if "cornell" in org or "irs" in org or "hud" in org:
        return "legal_or_policy_reference"
    if "who" in org or "ukri" in org or "oecd" in org:
        return "research_summary"
    if "cdc" in org or "fema" in org or "nist" in org or "osha" in org or "access board" in org:
        return "official_guidance"
    return "reference"


def _iter_research_documents(paths: list[str]) -> list[Path]:
    documents: list[Path] = []
    for value in paths:
        if not value:
            continue
        path = Path(value)
        if path.is_dir():
            documents.extend(sorted(child for child in path.rglob("*") if child.suffix.lower() in {".md", ".yaml", ".yml"}))
        elif path.exists() and path.suffix.lower() in {".md", ".yaml", ".yml"}:
            documents.append(path)
    return sorted(dict.fromkeys(documents))


def _extract_structured_sources(text: str, document: Path) -> list[dict[str, Any]]:
    sources: list[dict[str, Any]] = []
    current: dict[str, Any] | None = None
    current_key: str | None = None
    current_start = 0
    in_source_registry = False
    for line_number, line in enumerate(text.splitlines(), start=1):
        if line.strip().startswith("```") and in_source_registry:
            if current:
                sources.append(_finalize_structured_source(current, document, current_start))
            current = None
            current_key = None
            in_source_registry = False
            continue
        if re.match(r"^\s*source_registry:\s*$", line):
            in_source_registry = True
            continue
        if in_source_registry and current and re.match(r"^[A-Za-z_][A-Za-z0-9_-]*:\s*.*$", line):
            sources.append(_finalize_structured_source(current, document, current_start))
            current = None
            current_key = None
            in_source_registry = False
            continue
        start_match = re.match(r"^\s*-\s+id:\s*['\"]?([^'\"\s]+)['\"]?\s*$", line)
        if start_match and in_source_registry:
            if current:
                sources.append(_finalize_structured_source(current, document, current_start))
            current = {"id": start_match.group(1), "supports": [], "domains": _domains_for_document(document)}
            current_key = None
            current_start = line_number
            in_source_registry = True
            continue
        if not in_source_registry or current is None:
            continue
        key_match = re.match(r"^\s{2,}([A-Za-z_][A-Za-z0-9_]*):\s*(.*?)\s*$", line)
        if key_match:
            key, raw_value = key_match.groups()
            current_key = key
            if raw_value:
                current[key] = _strip_yaml_scalar(raw_value)
            elif key not in current:
                current[key] = []
            continue
        list_match = re.match(r"^\s{4,}-\s*(.*?)\s*$", line)
        if list_match and current_key:
            current.setdefault(current_key, [])
            if isinstance(current[current_key], list):
                current[current_key].append(_strip_yaml_scalar(list_match.group(1)))
    if current:
        sources.append(_finalize_structured_source(current, document, current_start))
    return sources


def _finalize_structured_source(source: dict[str, Any], document: Path, line_number: int) -> dict[str, Any]:
    url = str(source.get("url", ""))
    organization = source.get("organization") or _organization_from_url(url)
    domains = _domains_for_source(source, document)
    return {
        "id": str(source["id"]),
        "title": str(source.get("title") or source["id"]).strip(),
        "organization": str(organization or "unknown"),
        "url": url,
        "evidence_quality": _evidence_quality(source.get("evidence_quality")),
        "supports": sorted(set(str(item) for item in source.get("supports", []) if item)),
        "domains": domains,
        "used_by": [f"{document.as_posix()}:{line_number}"],
    }


def _fallback_source(url: str, line: str, document: Path, line_number: int) -> dict[str, Any]:
    title = _title_from_markdown_link(line, url) or _organization_from_url(url) or url
    source = {"title": title, "url": url, "supports": []}
    return {
        "id": _source_id_from_url(url),
        "title": title,
        "organization": _organization_from_url(url) or "unknown",
        "url": url,
        "evidence_quality": "mixed",
        "supports": [],
        "domains": _domains_for_source(source, document),
        "used_by": [f"{document.as_posix()}:{line_number}"],
    }


def _merge_source(existing: dict[str, Any], incoming: dict[str, Any]) -> dict[str, Any]:
    merged = dict(existing)
    for key in ("title", "organization", "url", "evidence_quality"):
        if not merged.get(key) and incoming.get(key):
            merged[key] = incoming[key]
    for key in ("supports", "domains", "used_by"):
        merged[key] = sorted(set([*merged.get(key, []), *incoming.get(key, [])]))
        if key == "domains" and "unmapped" in merged[key] and len(merged[key]) > 1:
            merged[key] = [domain for domain in merged[key] if domain != "unmapped"]
    return merged


def _clean_domains(domains: list[str]) -> list[str]:
    values = sorted(set(str(domain) for domain in domains if domain))
    if "unmapped" in values and len(values) > 1:
        values = [domain for domain in values if domain != "unmapped"]
    return values


def _urls_in_line(line: str) -> list[str]:
    return [url.rstrip(").,;]\"'") for url in re.findall(r"https?://[^\s<>\"]+", line)]


def _strip_yaml_scalar(value: str) -> str:
    return value.strip().strip("'\"")


def _evidence_quality(value: Any) -> str:
    raw = str(value or "mixed").lower().strip()
    return raw if raw in {"high", "moderate", "low", "mixed"} else "mixed"


def _source_id_from_url(url: str) -> str:
    parsed = urlparse(url)
    host = re.sub(r"[^A-Za-z0-9]+", "_", parsed.netloc.replace("www.", "")).strip("_").upper()
    digest = hashlib.sha1(url.encode("utf-8")).hexdigest()[:8].upper()
    return f"DOCSOURCE_{host}_{digest}" if host else f"DOCSOURCE_{digest}"


def _organization_from_url(url: str) -> str:
    host = urlparse(url).netloc.replace("www.", "")
    if not host:
        return "unknown"
    known = {
        "cdc.gov": "CDC",
        "who.int": "WHO",
        "fema.gov": "FEMA",
        "nist.gov": "NIST",
        "osha.gov": "OSHA",
        "epa.gov": "EPA",
        "fda.gov": "FDA",
        "access-board.gov": "U.S. Access Board",
        "bls.gov": "Bureau of Labor Statistics",
        "huduser.gov": "HUD User",
        "irs.gov": "IRS",
        "law.cornell.edu": "Cornell Legal Information Institute",
        "ncbi.nlm.nih.gov": "NCBI",
        "pmc.ncbi.nlm.nih.gov": "PubMed Central",
        "pubmed.ncbi.nlm.nih.gov": "PubMed",
    }
    for suffix, organization in known.items():
        if host.endswith(suffix):
            return organization
    return host


def _title_from_markdown_link(line: str, url: str) -> str | None:
    escaped = re.escape(url)
    match = re.search(rf"\[([^\]]+)\]\({escaped}\)", line)
    if match:
        return match.group(1).strip()
    title_match = re.search(r"title:\s*(.+)$", line)
    if title_match:
        return title_match.group(1).strip().strip("'\"")
    return None


def _domains_for_document(path: Path) -> list[str]:
    text = path.as_posix().lower()
    return _domains_for_text(text) or ["unmapped"]


def _domains_for_source(source: dict[str, Any], path: Path) -> list[str]:
    text = " ".join(
        [
            path.as_posix(),
            str(source.get("id", "")),
            str(source.get("title", "")),
            str(source.get("url", "")),
            " ".join(str(item) for item in source.get("supports", [])),
        ]
    ).lower()
    domains = set(_domains_for_text(text))
    domains.update(str(domain) for domain in source.get("domains", []) if domain)
    if not domains:
        domains.update(_domains_for_document(path))
    return sorted(domains or {"unmapped"})


def _domains_for_text(text: str) -> list[str]:
    mapping = {
        "water": "water",
        "wash": "water",
        "drinking": "water",
        "well": "water",
        "sanitation": "sanitation",
        "waste": "sanitation",
        "sewage": "sanitation",
        "food": "food",
        "nutrition": "food",
        "kitchen": "food",
        "meal": "food",
        "energy": "energy",
        "battery": "energy",
        "electrical": "energy",
        "housing": "housing",
        "cohousing": "housing",
        "residential": "housing",
        "care": "care_health",
        "health": "care_health",
        "medication": "care_health",
        "clinical": "care_health",
        "mobility": "mobility_access",
        "route": "mobility_access",
        "transport": "mobility_access",
        "accessibility": "mobility_access",
        "ada": "mobility_access",
        "governance": "governance_anticapture",
        "jury": "governance_anticapture",
        "sociocracy": "governance_anticapture",
        "participation": "governance_anticapture",
        "labor": "labor_time",
        "work": "labor_time",
        "time use": "labor_time",
        "risk": "risk_resilience",
        "resilience": "risk_resilience",
        "scaling": "scaling",
        "education": "education_skill",
        "skill": "education_skill",
        "apprenticeship": "education_skill",
        "social": "social_cultural",
        "belonging": "social_cultural",
        "loneliness": "social_cultural",
    }
    domains = [domain for token, domain in mapping.items() if token in text]
    return sorted(set(domains))


def _source_notes(source: dict[str, Any], domains: set[str]) -> str:
    source_domains = set(source.get("domains", []))
    supports = ", ".join(sorted(set(source.get("supports", [])))[:4])
    domain_text = ", ".join(sorted(set([*domains, *source_domains]))) if domains or source_domains else "not yet mapped to a capability domain"
    if supports:
        return f"Supports {supports}; currently mapped to {domain_text}."
    return f"Currently mapped to {domain_text}."
