# Asset Gap Pipeline

n8n is the orchestration layer, not the renderer. It can compare manifest asset keys against available viewer assets and create human-reviewed work items.

## Inputs

```yaml
world_manifest_path: examples/world_manifests/civic_floor_80_v0.world.json
asset_registry_path: viewer/world3d/src/world/AssetRegistry.js
issue_target: github
```

## Workflow

```text
World manifest generated
  -> Compare asset_key values against asset registry
  -> Identify missing assets
  -> Create GitHub issues
  -> Assign labels: proxy-needed, gltf-needed, blender-needed, unreal-later
  -> Optional AI-generated asset brief
  -> Human approval
```

## Outputs

```yaml
missing_asset_keys:
proxy_coverage_status:
created_issue_urls:
approval_status:
```

## Human Gates

- Asset briefs must preserve the manifest's provisional status.
- No asset should imply real-world approval, code compliance, or buildability.
