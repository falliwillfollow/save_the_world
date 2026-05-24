# Civic Floor Scenario Snapshot Pipeline

n8n is the orchestration layer, not the renderer. It coordinates CIaC scenario artifacts and human-readable snapshots.

## Inputs

```yaml
population: 80
scenario: energy_outage_reserve_v2
runtime_bundle_path: examples/generated/micro_commons_runtime_bundle.json
world_manifest_path: examples/world_manifests/civic_floor_80_v0.world.json
snapshot_output_path:
```

## Workflow

```text
Manual Trigger
  -> Select population
  -> Select scenario
  -> Run scenario export
  -> Generate world manifest scenario state
  -> Capture key states
  -> Generate markdown summary
  -> Create shareable scenario card
```

## Outputs

```yaml
scenario_state_id:
affected_objects:
warnings:
failures:
markdown_summary_path:
shareable_card_path:
```

## Human Gates

- Confirm scenario language is not presented as a prediction.
- Confirm personal health, finance, or resident identity data is absent.
