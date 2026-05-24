# Civic Floor World Build Pipeline

n8n is the orchestration layer, not the renderer. It coordinates validated CIaC artifacts, human approvals, asset gaps, publishing, and scenario snapshots.

## Trigger

Manual Trigger or GitHub Push.

## Inputs

```yaml
population: 80
scenario: normal
runtime_bundle_path: examples/generated/micro_commons_runtime_bundle.json
world_manifest_path: examples/world_manifests/civic_floor_80_v0.world.json
publish_target: local|github_pages|netlify|vercel|s3
```

## Workflow

```text
Manual Trigger or GitHub Push
  -> Run CIaC validation
  -> Run CIaC simulation / export runtime
  -> Export world manifest
  -> Validate world manifest schema
  -> Build viewer/world3d
  -> Publish preview artifact or static site
  -> Create GitHub issue on failure
  -> Notify user
```

## Outputs

```yaml
world_manifest_path:
viewer_build_path:
preview_url:
validation_status:
warnings:
failures:
```

## Human Gates

- Review generated warnings before publishing.
- Confirm provisionality language remains visible.
- Approve any asset replacement beyond proxy geometry.
