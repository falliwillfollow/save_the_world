from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

from .io import load_data, write_json
from .patch_impact import analyze_materialized_patch, promote_materialized_patch
from .patch_materialization import materialize_patch_proposal
from .research_loop import run_research_loop
from .viewer_pipeline import regenerate_viewer_population_reports
from .viewer_session import append_viewer_run_event_to_path, empty_viewer_run_report


SESSION_REPORT_PATH = Path("examples/generated/micro_commons_viewer_session_report.json")
DEFAULT_RUNTIME_BUNDLE_PATH = Path("examples/generated/micro_commons_runtime_bundle.json")
DEFAULT_LOCAL_N8N_WEBHOOK = "http://127.0.0.1:5678/webhook/ciac-research-loop"
N8N_DISABLED_VALUES = {"", "0", "false", "off", "none", "disabled"}


def serve_viewer(host: str, port: int, repo_root: str | Path) -> None:
    root = Path(repo_root).resolve()
    handler = partial(ViewerRequestHandler, directory=str(root), repo_root=root)
    server = ThreadingHTTPServer((host, port), handler)
    print(f"Serving CIaC viewer at http://{host}:{port}/viewer/")
    print("Viewer run logs POST to examples/generated/micro_commons_viewer_session_report.json")
    server.serve_forever()


class ViewerRequestHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args: Any, repo_root: Path, **kwargs: Any) -> None:
        self.repo_root = repo_root
        super().__init__(*args, **kwargs)

    def do_GET(self) -> None:  # noqa: N802
        if urlparse(self.path).path == "/api/viewer-session-report":
            self._send_json(self._load_session_report())
            return
        super().do_GET()

    def do_POST(self) -> None:  # noqa: N802
        path = urlparse(self.path).path
        if path == "/api/research-loop":
            self._handle_research_loop()
            return
        if path == "/api/materialize-patch":
            self._handle_materialize_patch()
            return
        if path == "/api/analyze-materialized-patch":
            self._handle_analyze_materialized_patch()
            return
        if path == "/api/promote-materialized-patch":
            self._handle_promote_materialized_patch()
            return
        if path != "/api/viewer-session-report":
            self.send_error(404, "Unknown API endpoint")
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
            payload = json.loads(self.rfile.read(length).decode("utf-8")) if length else {}
            event = payload.get("event", payload)
            report = append_viewer_run_event_to_path(self.repo_root / SESSION_REPORT_PATH, event)
            pipeline = regenerate_viewer_population_reports(self.repo_root, int(report.get("active_population", 0)), event)
        except Exception as exc:
            self.send_error(400, f"Could not persist viewer run: {exc}")
            return
        self._send_json(
            {
                "kind": "ViewerRunPipelineResponse",
                "viewer_run_report": report,
                "pipeline": {
                    "status": pipeline["status"],
                    "population": pipeline["population"],
                    "artifacts": pipeline["artifacts"],
                },
                "food_labor": pipeline["food_labor"],
                "complexity": pipeline["complexity"],
                "node_scaling": pipeline["node_scaling"],
                "topology_recommendation": pipeline["topology_recommendation"],
                "food_autonomy": pipeline.get("food_autonomy"),
                "cycle_iteration": pipeline.get("cycle_iteration"),
                "runtime_bundle": pipeline.get("runtime_bundle"),
                "search_optimizer": pipeline.get("search_optimizer"),
                "artifact_cohesion": pipeline["artifact_cohesion"],
            }
        )

    def _handle_research_loop(self) -> None:
        try:
            length = int(self.headers.get("Content-Length", "0"))
            payload = json.loads(self.rfile.read(length).decode("utf-8")) if length else {}
            focus = str(payload.get("focus") or "care_health")
            world_manifest = payload.get("world_manifest")
            if not isinstance(world_manifest, dict):
                world_manifest = load_data(self.repo_root / "examples/world_manifests/civic_floor_80_v0.world.json")
            runtime_bundle_path = Path(str(payload.get("runtime_bundle_path") or DEFAULT_RUNTIME_BUNDLE_PATH))
            if not runtime_bundle_path.is_absolute():
                runtime_bundle_path = self.repo_root / runtime_bundle_path
            runtime_bundle = load_data(runtime_bundle_path) if runtime_bundle_path.exists() else None
            world_id = str(world_manifest.get("world_id", "world")).replace("/", "_").replace("\\", "_")
            safe_focus = "".join(ch if ch.isalnum() or ch in {"_", "-"} else "_" for ch in focus)
            discovery_path = self.repo_root / "examples/discovery" / f"{world_id}_{safe_focus}_viewer_research.discovery.json"
            run_path = self.repo_root / "examples/discovery" / f"{world_id}_{safe_focus}_viewer_research.run.json"
            n8n_webhook = _research_webhook(payload)
            report = run_research_loop(
                world_manifest,
                runtime_bundle,
                focus=focus,
                source_paths={
                    "world_manifest": payload.get("world_manifest_path") or f"browser:{world_id}",
                    "runtime_bundle": str(runtime_bundle_path.relative_to(self.repo_root)) if runtime_bundle_path.is_relative_to(self.repo_root) else str(runtime_bundle_path),
                },
                discovery_report_path=discovery_path,
                candidate_output_dir=self.repo_root / "candidate_interventions",
                patch_output_dir=self.repo_root / "patch_proposals",
                n8n_webhook=n8n_webhook,
                allow_seed_fallback=True,
            )
            write_json(run_path, report)
        except Exception as exc:
            self.send_error(400, f"Could not run research loop: {exc}")
            return
        self._send_json(
            {
                "kind": "ViewerResearchLoopResponse",
                "research_loop": report,
                "research_loop_path": str(run_path.relative_to(self.repo_root)),
                "candidates": self._load_written_artifacts(report.get("candidates_written", [])),
                "patch_proposals": self._load_written_artifacts(report.get("patch_proposals_written", [])),
            }
        )

    def _handle_materialize_patch(self) -> None:
        try:
            length = int(self.headers.get("Content-Length", "0"))
            payload = json.loads(self.rfile.read(length).decode("utf-8")) if length else {}
            patch_proposal = payload.get("patch_proposal")
            if not isinstance(patch_proposal, dict):
                patch_path = payload.get("patch_proposal_path")
                if not patch_path:
                    raise ValueError("patch_proposal or patch_proposal_path is required")
                patch_file = Path(str(patch_path))
                if not patch_file.is_absolute():
                    patch_file = self.repo_root / patch_file
                patch_proposal = load_data(patch_file)
            candidate = payload.get("candidate")
            if candidate is not None and not isinstance(candidate, dict):
                raise ValueError("candidate must be a JSON object when provided")
            patch_id = str(patch_proposal.get("id", "patch")).replace("/", "_").replace("\\", "_")
            report_path = self.repo_root / "examples/discovery" / f"{patch_id}.materialization.json"
            report = materialize_patch_proposal(
                patch_proposal,
                candidate,
                repo_root=self.repo_root,
                overwrite=True,
                report_output=report_path,
            )
            artifact = None
            artifact_path = self.repo_root / report.get("materialized_artifact_path", "")
            if report.get("status") == "materialized_draft" and artifact_path.exists():
                artifact = load_data(artifact_path)
        except Exception as exc:
            self.send_error(400, f"Could not materialize patch: {exc}")
            return
        self._send_json(
            {
                "kind": "ViewerPatchMaterializationResponse",
                "materialization": report,
                "materialization_path": str(report_path.relative_to(self.repo_root)),
                "materialized_artifact": artifact,
            }
        )

    def _handle_analyze_materialized_patch(self) -> None:
        try:
            payload = self._read_json_body()
            materialization = payload.get("materialization")
            if not isinstance(materialization, dict):
                materialization_path = payload.get("materialization_path")
                if not materialization_path:
                    raise ValueError("materialization or materialization_path is required")
                path = Path(str(materialization_path))
                if not path.is_absolute():
                    path = self.repo_root / path
                materialization = load_data(path)
            pattern_id = str(materialization.get("source_candidate_id", "patch")).replace("/", "_").replace("\\", "_")
            report_path = self.repo_root / "examples/discovery" / f"{pattern_id}.impact.json"
            report = analyze_materialized_patch(
                materialization,
                repo_root=self.repo_root,
                report_output=report_path,
            )
        except Exception as exc:
            self.send_error(400, f"Could not analyze materialized patch: {exc}")
            return
        self._send_json(
            {
                "kind": "ViewerPatchImpactResponse",
                "impact": report,
                "impact_path": str(report_path.relative_to(self.repo_root)),
            }
        )

    def _handle_promote_materialized_patch(self) -> None:
        try:
            payload = self._read_json_body()
            materialization = payload.get("materialization")
            if not isinstance(materialization, dict):
                materialization_path = payload.get("materialization_path")
                if not materialization_path:
                    raise ValueError("materialization or materialization_path is required")
                path = Path(str(materialization_path))
                if not path.is_absolute():
                    path = self.repo_root / path
                materialization = load_data(path)
            pattern_id = str(materialization.get("source_candidate_id", "patch")).replace("/", "_").replace("\\", "_")
            report_path = self.repo_root / "examples/discovery" / f"{pattern_id}.promotion.json"
            report = promote_materialized_patch(
                materialization,
                repo_root=self.repo_root,
                report_output=report_path,
            )
            runtime_bundle = load_data(self.repo_root / DEFAULT_RUNTIME_BUNDLE_PATH) if report.get("status") == "promoted" else None
            world_manifest = load_data(self.repo_root / "examples/world_manifests/civic_floor_80_v0.world.json") if report.get("status") == "promoted" else None
        except Exception as exc:
            self.send_error(400, f"Could not promote materialized patch: {exc}")
            return
        self._send_json(
            {
                "kind": "ViewerPatchPromotionResponse",
                "promotion": report,
                "promotion_path": str(report_path.relative_to(self.repo_root)),
                "runtime_bundle": runtime_bundle,
                "world_manifest": world_manifest,
            }
        )

    def _load_written_artifacts(self, records: list[dict[str, Any]]) -> list[dict[str, Any]]:
        artifacts = []
        for record in records:
            path = Path(record.get("path", ""))
            if not path.is_absolute():
                path = self.repo_root / path
            try:
                artifacts.append(load_data(path))
            except Exception:
                artifacts.append({"kind": "UnavailableArtifact", **record})
        return artifacts

    def _load_session_report(self) -> dict[str, Any]:
        path = self.repo_root / SESSION_REPORT_PATH
        if not path.exists():
            return empty_viewer_run_report()
        return json.loads(path.read_text(encoding="utf-8"))

    def _read_json_body(self) -> dict[str, Any]:
        length = int(self.headers.get("Content-Length", "0"))
        payload = json.loads(self.rfile.read(length).decode("utf-8")) if length else {}
        if not isinstance(payload, dict):
            raise ValueError("Request body must be a JSON object")
        return payload

    def _send_json(self, data: dict[str, Any]) -> None:
        body = json.dumps(data, indent=2, sort_keys=True).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def _research_webhook(payload: dict[str, Any]) -> str | None:
    explicit = payload.get("n8n_webhook")
    if explicit is not None:
        value = str(explicit).strip()
        return None if value.lower() in N8N_DISABLED_VALUES else value
    configured = str(os.environ.get("CIAC_N8N_RESEARCH_WEBHOOK", "")).strip()
    if configured:
        return None if configured.lower() in N8N_DISABLED_VALUES else configured
    return DEFAULT_LOCAL_N8N_WEBHOOK if _local_n8n_available() else None


def _local_n8n_available() -> bool:
    try:
        with urllib.request.urlopen("http://127.0.0.1:5678", timeout=0.5):
            return True
    except (OSError, TimeoutError, urllib.error.URLError):
        return False
