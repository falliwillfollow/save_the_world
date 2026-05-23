# CIaC Runtime Viewer

Viewer for `RuntimeBundle` JSON artifacts.

Run from the repository root with the CIaC viewer server if you want completed webapp years to be written to `examples/generated/micro_commons_viewer_session_report.json`:

```powershell
py -3.10 -m ciac viewer-server --port 8765
```

Then open:

```text
http://localhost:8765/viewer/
```

The viewer loads `examples/generated/micro_commons_runtime_bundle.json`, `examples/generated/micro_commons_foundation_gate.json`, optimizer reports, cycle reports, `examples/generated/micro_commons_node_scaling.json`, `examples/generated/micro_commons_topology_recommendation.json`, and `examples/generated/micro_commons_viewer_session_report.json` by default when served over HTTP. It also accepts local report files through the header controls.

A plain `py -3.10 -m http.server 8765` can still inspect reports, but browser runs will only be held in local storage because that server cannot accept the viewer run log POST.

With `ciac viewer-server`, every completed webapp year writes the viewer run report, runs the simulator from the webapp population context, materializes the selected search candidate into a cycle report, and regenerates the population-specific food labor, complexity, node-scaling, topology recommendation, and artifact-cohesion reports.

Use `py -3.10 -m ciac artifact-cohesion examples/generated --output examples/generated/micro_commons_artifact_cohesion.json` after regenerating reports to confirm the default viewer artifacts are not stale or disconnected.

Current inspection features:

- day scrubber and playback
- persisted webapp year-run log when served with `ciac viewer-server`
- layout zones and access routes
- system selection and details
- scenario failure overlays
- resource, maintenance, and unmet-need panels
- population slider for infrastructure node-pool scaling
- abundance-first topology summary across micro, village, town, and city scopes
- compact failure-reason and warning panels
- foundation gate status and check evidence

This is an inspection surface only. It must not be used as evidence of legal permission, engineering safety, public-health safety, resident consent, accessibility compliance, or construction readiness.
