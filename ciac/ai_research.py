from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from typing import Any, Callable


DEFAULT_OPENAI_MODEL = "gpt-5.5"
OPENAI_RESPONSES_URL = "https://api.openai.com/v1/responses"

PostJson = Callable[[str, dict[str, str], dict[str, Any], int], dict[str, Any]]


class OpenAIConfigurationError(RuntimeError):
    pass


class OpenAIResponseError(RuntimeError):
    pass


def draft_technology_module(
    research_need_report: dict[str, Any],
    need_id: str | None = None,
    model: str | None = None,
    include_web_search: bool = True,
    api_key: str | None = None,
    timeout_seconds: int = 90,
    post_json: PostJson | None = None,
) -> dict[str, Any]:
    need = _select_need(research_need_report, need_id)
    key = api_key or os.environ.get("OPENAI_API_KEY")
    if not key:
        raise OpenAIConfigurationError("OPENAI_API_KEY is not set.")

    payload = {
        "model": model or os.environ.get("CIAC_OPENAI_MODEL") or DEFAULT_OPENAI_MODEL,
        "instructions": _draft_instructions(),
        "input": _research_need_prompt(need),
        "max_output_tokens": 5000,
    }
    if include_web_search:
        payload["tools"] = [{"type": "web_search"}]
        payload["tool_choice"] = "auto"
        payload["include"] = ["web_search_call.action.sources"]

    response = (post_json or _post_json)(
        OPENAI_RESPONSES_URL,
        {
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
        },
        payload,
        timeout_seconds,
    )
    return _normalize_technology_module(_parse_technology_module(_extract_response_text(response)), need)


def _select_need(report: dict[str, Any], need_id: str | None) -> dict[str, Any]:
    needs = report.get("needs", [])
    if not needs:
        raise OpenAIConfigurationError("ResearchNeedReport has no needs to draft from.")
    if need_id is None:
        return needs[0]
    for need in needs:
        if need.get("id") == need_id:
            return need
    raise OpenAIConfigurationError(f"ResearchNeedReport does not contain need: {need_id}")


def _draft_instructions() -> str:
    return (
        "You draft provisional CIaC TechnologyModule JSON from evidence search briefs. "
        "Search for credible published evidence when web search is available. Preserve citations, study context, "
        "performance statistics, limitations, and uncertainty. Do not invent numbers. If evidence is weak, keep "
        "status as draft and explain uncertainty in unknowns. Return only one JSON object matching this shape: "
        "kind, id, name, domain, status, provisional, source_evidence, performance_statistics, applicability, "
        "modeled_impacts, integration_requirements, unknowns. The domain field must be an array of strings, even "
        "when there is only one domain. integration_requirements must be a flat array of strings, not an object."
        " unknowns must be a flat array of strings. applicability and modeled_impacts must be objects. Put prose "
        "limitations in object notes fields."
    )


def _research_need_prompt(need: dict[str, Any]) -> str:
    return json.dumps(
        {
            "task": "Draft one provisional CIaC TechnologyModule for this research need.",
            "technology_module_rules": {
                "kind": "TechnologyModule",
                "status_values": ["draft", "evidence_seed", "candidate", "validated"],
                "required_policy": "The module must not reduce food, water, or critical energy dignity floors.",
                "citation_rule": "Every performance statistic should point to a source_evidence id.",
                "optimization_rule": "Leave modeled impacts conservative unless the evidence directly supports them.",
            },
            "research_need": need,
        },
        indent=2,
        sort_keys=True,
    )


def _post_json(url: str, headers: dict[str, str], payload: dict[str, Any], timeout_seconds: int) -> dict[str, Any]:
    request = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers=headers,
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout_seconds) as response:
            body = response.read().decode("utf-8")
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise OpenAIResponseError(f"OpenAI API request failed with HTTP {exc.code}: {_redact_secret_text(detail)}") from exc
    except urllib.error.URLError as exc:
        raise OpenAIResponseError(f"OpenAI API request failed: {exc.reason}") from exc

    try:
        data = json.loads(body)
    except json.JSONDecodeError as exc:
        raise OpenAIResponseError("OpenAI API returned non-JSON response.") from exc
    if not isinstance(data, dict):
        raise OpenAIResponseError("OpenAI API returned an unexpected response shape.")
    return data


def _extract_response_text(response: dict[str, Any]) -> str:
    output_text = response.get("output_text")
    if isinstance(output_text, str) and output_text.strip():
        return output_text

    fragments: list[str] = []
    for item in response.get("output", []):
        if not isinstance(item, dict):
            continue
        for content in item.get("content", []):
            if isinstance(content, dict) and content.get("type") in {"output_text", "text"}:
                text = content.get("text")
                if isinstance(text, str):
                    fragments.append(text)
    if fragments:
        return "\n".join(fragments)
    raise OpenAIResponseError("OpenAI response did not contain output text.")


def _parse_technology_module(text: str) -> dict[str, Any]:
    source = text.strip()
    if source.startswith("```"):
        source = source.strip("`")
        if source.lower().startswith("json"):
            source = source[4:].strip()
    if not source.startswith("{"):
        start = source.find("{")
        end = source.rfind("}")
        if start >= 0 and end > start:
            source = source[start : end + 1]
    try:
        module = json.loads(source)
    except json.JSONDecodeError as exc:
        raise OpenAIResponseError("OpenAI response did not contain a parseable JSON object.") from exc
    if not isinstance(module, dict):
        raise OpenAIResponseError("OpenAI response JSON was not an object.")
    return module


def _normalize_technology_module(module: dict[str, Any], need: dict[str, Any]) -> dict[str, Any]:
    if isinstance(module.get("domain"), str):
        module = dict(module)
        module["domain"] = [module["domain"]]
    if isinstance(module.get("integration_requirements"), dict):
        module = dict(module)
        module["integration_requirements"] = _flatten_requirement_map(module["integration_requirements"])
    if isinstance(module.get("applicability"), list):
        module = dict(module)
        module["applicability"] = {
            "target_slots": [need.get("module_slot", "unknown")],
            "target_patterns": [],
            "excludes": [],
            "notes": module["applicability"],
        }
    if isinstance(module.get("modeled_impacts"), list):
        module = dict(module)
        module["modeled_impacts"] = {
            "dignity_floor_policy": "additive_only",
            "direct_resource_effects": {},
            "candidate_modifiers": {},
            "notes": module["modeled_impacts"],
        }
    if isinstance(module.get("unknowns"), dict):
        module = dict(module)
        module["unknowns"] = _flatten_requirement_map(module["unknowns"])
    return module


def _flatten_requirement_map(requirements: dict[str, Any]) -> list[str]:
    flattened: list[str] = []
    for category, value in requirements.items():
        if isinstance(value, list):
            flattened.extend(f"{category}: {item}" for item in value)
        else:
            flattened.append(f"{category}: {value}")
    return flattened


def _redact_secret_text(text: str) -> str:
    return text.replace(os.environ.get("OPENAI_API_KEY", ""), "[redacted]") if os.environ.get("OPENAI_API_KEY") else text
