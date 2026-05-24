from __future__ import annotations

import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any

from .discovery import build_discovery_loop
from .io import load_data, write_json
from .research_context import build_research_context
from .validation import validate_data


def serve_discovery_bridge(host: str, port: int, repo_root: str) -> None:
    root = Path(repo_root).resolve()

    class Handler(BaseHTTPRequestHandler):
        def do_GET(self) -> None:  # noqa: N802
            if self.path == "/health":
                self._json(200, {"ok": True, "service": "ciac-discovery-bridge", "repo_root": str(root)})
                return
            self._json(404, {"ok": False, "error": "not_found"})

        def do_POST(self) -> None:  # noqa: N802
            if self.path == "/research-context":
                self._research_context()
                return
            if self.path != "/discovery-loop":
                self._json(404, {"ok": False, "error": "not_found"})
                return
            try:
                payload = self._read_json()
                world_path = _resolve_inside(root, payload["world_manifest_path"])
                runtime_path = _resolve_inside(root, payload["runtime_bundle_path"]) if payload.get("runtime_bundle_path") else None
                output_path = _resolve_inside(root, payload["output_path"]) if payload.get("output_path") else None
                world = load_data(world_path)
                runtime = load_data(runtime_path) if runtime_path else None
                report = build_discovery_loop(
                    world,
                    runtime_bundle=runtime,
                    focus=payload.get("focus", "all"),
                    source_paths={
                        "world_manifest": str(world_path.relative_to(root)),
                        "runtime_bundle": str(runtime_path.relative_to(root)) if runtime_path else None,
                    },
                )
                validation = validate_data(report, str(output_path or "<discovery-loop>"))
                if not validation.ok:
                    self._json(422, {"ok": False, "issues": [issue.__dict__ for issue in validation.issues]})
                    return
                if output_path:
                    write_json(output_path, report)
                self._json(200, {"ok": True, "output_path": str(output_path.relative_to(root)) if output_path else None, "report": report})
            except Exception as exc:  # Keep the local bridge debuggable from n8n.
                self._json(500, {"ok": False, "error": str(exc)})

        def _research_context(self) -> None:
            try:
                payload = self._read_json()
                report = payload.get("discovery_report")
                if not isinstance(report, dict):
                    raise ValueError("research-context requires discovery_report object")
                context = build_research_context(root, report)
                self._json(200, {"ok": True, **context})
            except Exception as exc:
                self._json(500, {"ok": False, "error": str(exc)})

        def log_message(self, format: str, *args: Any) -> None:
            return

        def _read_json(self) -> dict[str, Any]:
            length = int(self.headers.get("Content-Length", "0"))
            data = json.loads(self.rfile.read(length).decode("utf-8") or "{}")
            if not isinstance(data, dict):
                raise ValueError("Request body must be a JSON object")
            return data

        def _json(self, status: int, payload: dict[str, Any]) -> None:
            body = json.dumps(payload, indent=2, sort_keys=True).encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

    server = ThreadingHTTPServer((host, port), Handler)
    print(f"CIaC discovery bridge listening on http://{host}:{port}")
    print(f"Repo root: {root}")
    server.serve_forever()


def _resolve_inside(root: Path, path: str) -> Path:
    resolved = (root / path).resolve() if not Path(path).is_absolute() else Path(path).resolve()
    if root != resolved and root not in resolved.parents:
        raise ValueError(f"Path escapes repo root: {path}")
    return resolved
