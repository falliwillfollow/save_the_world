from __future__ import annotations

import json
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

from .viewer_pipeline import regenerate_viewer_population_reports
from .viewer_session import append_viewer_run_event_to_path, empty_viewer_run_report


SESSION_REPORT_PATH = Path("examples/generated/micro_commons_viewer_session_report.json")


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
        if urlparse(self.path).path != "/api/viewer-session-report":
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

    def _load_session_report(self) -> dict[str, Any]:
        path = self.repo_root / SESSION_REPORT_PATH
        if not path.exists():
            return empty_viewer_run_report()
        return json.loads(path.read_text(encoding="utf-8"))

    def _send_json(self, data: dict[str, Any]) -> None:
        body = json.dumps(data, indent=2, sort_keys=True).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)
