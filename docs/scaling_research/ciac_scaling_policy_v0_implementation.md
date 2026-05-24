# CIaC Scaling Policy v0 Implementation

**Status:** implemented as provisional topology logic  
**Policy file:** `scale_policies/ciac_scaling_policy_v0.yaml`  
**Schema:** `schemas/scaling_policy.schema.json`  
**Research inputs:**
- `docs/scaling_research/ciac_deep_research_scaling_thresholds_part_1_v0_2.md`
- `docs/scaling_research/ciac_deep_research_scaling_thresholds_part_2_v0_2.md`
- `docs/scaling_research/ciac_deep_research_scaling_thresholds_part_3_v0_1.md`
- `docs/scaling_research/ciac_deep_research_scaling_thresholds_part_4_v0_1.md`

## Purpose

The population commit workflow no longer treats scale as whole-footprint duplication. It now uses a mixed topology model:

- **Duplicate** human-sensitive local nodes before they become institutional.
- **Resize** only where added size does not erase privacy, access, or legibility.
- **Federate** district/town functions above village-block scale.
- **Keep emergency minimums separate** from dignified normal operating thresholds.

## Implemented Viewer Behavior

`viewer/world3d/src/world/scaleManifest.js` now computes:

- village block count from the 150-person village-block ceiling
- residential pods from the 20-person preferred pod size
- common houses from the 100-person neighborhood common-house ceiling
- food commons, protein commons, care rooms, quiet rooms, tool caches, water reserves, sanitation cells, and governance/federation nodes independently
- policy rows for shared kitchens, food-service radius, water testing/reserves, blackwater review, medication continuity, high-need support, governance circles, deliberative panels, essential access, training groups, reserve topology, fallback systems, and emergency governance

For example, a 731-person commit becomes:

```yaml
village_blocks: 5
residential_pods: 37
common_houses: 8
district_venues: 2
scaling_mode: mixed_topology
```

The 3D world should therefore read less like repeated city-builder tiles and more like a scaled civic topology: many residential pods, neighborhood commons, distributed food/care/service access, and visible federation layers.

## Inspection UI

Objects created by the scaler include a `scaling_policy` block. When a user clicks a structure or infrastructure node, the Info Card shows:

- residents served
- preferred capacity
- soft threshold
- hard threshold
- scale action
- human-factor driver
- threshold warning when overloaded

## Current Limits

This is still a visualization and model-topology layer. It is not:

- an architectural plan
- a public-health approval
- a building-code review
- a water-system permit
- a legal determination
- a mental-health or clinical standard

The next useful step is to let the optimizer consume the same `ScalingPolicy` file directly, so recommendations and world geometry are driven by one source of scaling truth.
