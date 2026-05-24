from __future__ import annotations

import tempfile
import unittest
from functools import partial
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Thread
import json

from ciac.cli import main
from ciac.io import load_data
from ciac.research_loop import build_patch_proposal, run_research_loop
from ciac.validation import validate_data


ROOT = Path(__file__).resolve().parents[1]
WORLD = ROOT / "examples" / "world_manifests" / "civic_floor_80_v0.world.json"
RUNTIME = ROOT / "examples" / "generated" / "micro_commons_runtime_bundle.json"


class ResearchLoopTests(unittest.TestCase):
    def setUp(self) -> None:
        self.world = load_data(WORLD)
        self.runtime = load_data(RUNTIME)

    def test_patch_proposal_from_candidate_is_valid(self) -> None:
        candidate = load_data(ROOT / "examples" / "discovery" / "civic_floor_80_discovery_loop_v0.discovery.json")[
            "seed_candidates"
        ][0]

        proposal = build_patch_proposal(candidate)

        self.assertEqual(proposal["kind"], "PatchProposal")
        self.assertEqual(proposal["source_candidate_id"], candidate["id"])
        self.assertEqual(proposal["status"], "needs_evidence")
        self.assertTrue(validate_data(proposal, proposal["id"]).ok)

    def test_research_loop_writes_candidates_and_patch_proposals(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            report = run_research_loop(
                self.world,
                self.runtime,
                focus="care_health",
                source_paths={"world_manifest": str(WORLD), "runtime_bundle": str(RUNTIME)},
                discovery_report_path=root / "discovery.json",
                candidate_output_dir=root / "candidates",
                patch_output_dir=root / "patches",
            )

            self.assertEqual(report["kind"], "ResearchLoopRun")
            self.assertEqual(report["status"], "ready_for_review")
            self.assertEqual(report["candidate_source"], "seed_candidates")
            self.assertEqual(len(report["candidates_written"]), 3)
            self.assertEqual(len(report["patch_proposals_written"]), 3)
            self.assertTrue(validate_data(report, "research-loop").ok)
            for record in report["candidates_written"]:
                self.assertTrue(Path(record["path"]).exists())
                self.assertTrue(validate_data(load_data(record["path"]), record["path"]).ok)
            for record in report["patch_proposals_written"]:
                self.assertTrue(Path(record["path"]).exists())
                self.assertTrue(validate_data(load_data(record["path"]), record["path"]).ok)

    def test_research_loop_uses_webhook_candidates_when_available(self) -> None:
        candidate = load_data(ROOT / "examples" / "discovery" / "civic_floor_80_discovery_loop_v0.discovery.json")[
            "seed_candidates"
        ][0]
        server = ThreadingHTTPServer(
            ("127.0.0.1", 0),
            partial(_ResearchWebhookHandler, response_candidates=[{**candidate, "status": "generated"}]),
        )
        thread = Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            with tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                report = run_research_loop(
                    self.world,
                    self.runtime,
                    focus="care_health",
                    source_paths={"world_manifest": str(WORLD), "runtime_bundle": str(RUNTIME)},
                    discovery_report_path=root / "discovery.json",
                    candidate_output_dir=root / "candidates",
                    patch_output_dir=root / "patches",
                    n8n_webhook=f"http://127.0.0.1:{server.server_address[1]}/webhook/ciac-research-loop",
                )
        finally:
            server.shutdown()
            server.server_close()

        self.assertEqual(report["candidate_source"], "n8n_webhook")
        self.assertTrue(report["n8n"]["called"])
        self.assertTrue(report["n8n"]["ok"])
        self.assertEqual(len(report["candidates_written"]), 1)

    def test_cli_research_loop_writes_report(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            output = root / "research.json"
            code = main(
                [
                    "research-loop",
                    str(WORLD),
                    "--runtime",
                    str(RUNTIME),
                    "--focus",
                    "care_health",
                    "--discovery-output",
                    str(root / "discovery.json"),
                    "--candidate-output-dir",
                    str(root / "candidates"),
                    "--patch-output-dir",
                    str(root / "patches"),
                    "--output",
                    str(output),
                ]
            )

            self.assertEqual(code, 0)
            report = load_data(output)
            self.assertEqual(report["kind"], "ResearchLoopRun")
            self.assertEqual(len(report["patch_proposals_written"]), 3)


class _ResearchWebhookHandler(BaseHTTPRequestHandler):
    def __init__(self, *args, response_candidates: list[dict], **kwargs) -> None:
        self.response_candidates = response_candidates
        super().__init__(*args, **kwargs)

    def do_POST(self) -> None:  # noqa: N802
        length = int(self.headers.get("Content-Length", "0"))
        payload = json.loads(self.rfile.read(length).decode("utf-8")) if length else {}
        body = json.dumps(
            {
                "kind": "CIaCResearchLoopResponse",
                "version": "v0",
                "received_report_id": payload.get("discovery_report", {}).get("id"),
                "candidate_interventions": self.response_candidates,
            }
        ).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


if __name__ == "__main__":
    unittest.main()
