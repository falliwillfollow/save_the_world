# CIaC Runtime Viewer

Static viewer for `RuntimeBundle` JSON artifacts.

Run from the repository root:

```powershell
py -3.10 -m http.server 8765
```

Then open:

```text
http://localhost:8765/viewer/
```

The viewer loads `examples/generated/micro_commons_runtime_bundle.json` and `examples/generated/micro_commons_foundation_gate.json` by default when served over HTTP. It also accepts local bundle and foundation gate files through the header controls.

Current inspection features:

- day scrubber and playback
- layout zones and access routes
- system selection and details
- scenario failure overlays
- resource, maintenance, and unmet-need panels
- compact failure-reason and warning panels
- foundation gate status and check evidence

This is an inspection surface only. It must not be used as evidence of legal permission, engineering safety, public-health safety, resident consent, accessibility compliance, or construction readiness.
