# Life Manifest And Abundance Mode

## Purpose

The Life Manifest is the human-facing translation layer for CIaC. It takes the runtime bundle and world manifest and asks what the modeled infrastructure returns to residents: less compulsory burden, more protected recovery, more meaningful time, and clearer review boundaries.

The Automation Manifest is the machine-facing twin. It lists the routine work that software, AI, or robotics may help coordinate, and the decisions automation must never own.

## Relationship To Existing Artifacts

- `RuntimeBundle` carries simulation, resources, capability state, warnings, and stress results.
- `CivicFloorWorldManifest` carries the 3D world, structures, modules, telemetry, overlays, and evidence cards.
- `LifeManifest` carries baseline versus civic-floor life budgets, resident archetypes, Life Returned metrics, story beats, and provisionality.
- `AutomationManifest` carries allowed automation domains, blocked domains, review-gated tasks, and sovereignty boundaries.

The world manifest links to the sample life and automation manifests under `linked_manifests`.

## Abundance Mode UI

Abundance Mode in the 3D viewer shows:

- average Life Returned hours per week
- selected resident archetype
- baseline versus civic-floor weekly time budget
- compulsory burden reduction
- automation-assist tasks and review gates
- blocked automation domains
- promotion blockers and provisionality

The mode highlights infrastructure that can be supported by automation, but it does not imply automation controls residents.

## Life Returned Metric

The v0 metric is intentionally simple:

```text
baseline_compulsory =
  wage_hours + commute_hours + errands_admin + domestic_survival + required_care

civic_compulsory =
  wage_hours + commons_labor + commute_hours + errands_admin + domestic_survival + required_care

life_returned_hours =
  baseline_compulsory - civic_compulsory
```

The result is provisional. It is a review signal, not proof of wellbeing.

## Baseline Assumptions

The default baseline profile is a conventional renter/creator schedule with wage work, commuting, errands, private domestic survival work, and a small amount of protected recovery and passion time. It should be replaced with local survey data before any planning use.

## Human Sovereignty Boundaries

Automation may support scheduling, monitoring, inventory, route planning, inspection, reminders, scenario testing, hidden burden detection, logistics, and maintenance queueing.

Automation may not decide or infer:

- resident consent
- expulsion or loss of access
- clinical diagnosis
- legal judgment
- punishment
- emotional coercion
- private life status
- governance legitimacy
- human worth

## Generate Manifests

```powershell
py -3.10 -m ciac export-life-manifest --runtime examples/generated/micro_commons_runtime_bundle.json --world examples/world_manifests/civic_floor_80_v0.world.json --output examples/life_manifests/life_manifest_80_v0.json --population 80

py -3.10 -m ciac export-automation-manifest --runtime examples/generated/micro_commons_runtime_bundle.json --world examples/world_manifests/civic_floor_80_v0.world.json --output examples/life_manifests/automation_manifest_80_v0.json
```

## Run Viewer

```powershell
py -3.10 -m ciac viewer-server --host 127.0.0.1 --port 8765 --repo-root D:\Projects\CIaC

Set-Location D:\Projects\CIaC\viewer\world3d
npm run dev -- --host 127.0.0.1 --port 5173
```

Open the 3D viewer and choose `Abundance`.

## What This Does Not Prove

This layer does not certify real-world abundance, safety, legality, affordability, health outcomes, resident consent, buildability, labor compliance, accessibility, or governance legitimacy. It makes the assumptions legible enough to review.

## Future Workflow Hooks

Future n8n workflows can regenerate life manifests after simulation runs, render Abundance Mode snapshots, and create review tasks for missing gates. Future robotics interfaces should consume only the `AutomationManifest` task registry and must preserve the blocked-domain rules.
