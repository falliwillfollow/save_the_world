# Proxy Assets

The Sprint 54 world viewer uses procedural proxy geometry only:

- boxes for structures
- cylinders or blocks for infrastructure nodes
- transparent planes for zones
- lines for paths
- simple archetype figures for residents

Future glTF, Blender, or Unreal assets should preserve the same `asset_key` values declared in the world manifest and `AssetRegistry.js`.
