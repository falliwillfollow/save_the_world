# Civic Floor World MVP

The Civic Floor World is an experimental web-first 3D viewer for CIaC outputs. It renders a generated `CivicFloorWorldManifest` as a stylized civic diorama with Life, Systems, Stress, and Insight modes.

It is not hand-authored art and it is not a site plan. The world is a provisional visualization of CIaC assumptions, module states, scenarios, capability warnings, and review blockers.

## Architecture

```text
RuntimeBundle
  -> ciac export-world
  -> CivicFloorWorldManifest
  -> viewer/world3d
```

The web viewer does not know Python internals. It reads the manifest contract and renders zones, structures, paths, infrastructure nodes, residents, daily events, scenario states, overlays, and evidence cards.

## Generate A Manifest

From the repository root:

```powershell
py -3.10 -m ciac export-world --runtime examples/generated/micro_commons_runtime_bundle.json --population 80 --world-id civic_floor_80_v0 --output examples/world_manifests/civic_floor_80_v0.world.json
```

Validate it:

```powershell
py -3.10 -m ciac validate-world examples/world_manifests/civic_floor_80_v0.world.json
py -3.10 -m ciac validate examples/world_manifests
```

## Run The Web Viewer

```powershell
Set-Location viewer/world3d
npm install
npm run dev
```

Then open the Vite URL shown in the terminal.

Build the static bundle:

```powershell
npm run build
```

## Viewer Modes

- Life Mode: shows archetypal residents and daily routines such as care, food work, maintenance, learning, rest, social time, and passion time.
- Systems Mode: highlights infrastructure domains such as food, water, energy, sanitation, care, governance, labor, and risk.
- Stress Mode: selects scenario states and highlights affected objects, warnings, and failures.
- Insight Mode: ranks bottlenecks and capability warnings, then links diagnostics to world objects and evidence.

The viewer also supports committed population scaling. The operator changes the draft population, commits it, and the world rerenders as a scaled symbolic layout instead of twitching in real time.

## Evidence Cards

Every visible object can link to an evidence card with:

- summary
- module references
- assumptions
- required reviews
- provisional status

Clicking the common house, protein commons, energy node, paths, zones, or residents opens the right-side card.

## Asset Registry

`viewer/world3d/src/world/AssetRegistry.js` maps object types and `asset_key` values to proxy geometry, colors, icons, and future asset hooks.

The current viewer uses boxes, planes, lines, cylinders, and simple resident figures. Future glTF, Blender, or Unreal assets should keep the same manifest keys.

## n8n Boundary

n8n is the orchestration layer, not the renderer. It should coordinate validation, artifact generation, AI/RAG discovery loops, publishing, asset-gap tracking, and scenario snapshots. The local viewer does not require n8n.

Workflow specs live in `n8n/workflow_specs/`.

The Discovery Lab implementation is documented separately in `docs/n8n_discovery_lab_implementation.md`.

## What V0 Does Not Prove

This is a provisional civic simulation. It visualizes model assumptions and stress tests. It does not certify real-world safety, legality, affordability, engineering, public health, accessibility, resident consent, or buildability.

## Future Roadmap

```text
world_manifest.json
  -> slider checkpoint manifests
  -> scenario frame exports
  -> richer daily routines
  -> asset gap workflow
  -> Blender asset maturation
  -> Unreal scene generation
  -> cinematic exports and high-fidelity review
```
