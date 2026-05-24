import { SCALING_POLICY, countForPopulation, policyForType } from "./scalingPolicy.js";

const BLOCK_SPACING_X = 154;
const BLOCK_SPACING_Z = 132;
const HUMAN_VISIBLE_AGENT_COUNT = 12;

export function inferScale(population) {
  const people = clampPopulation(population);
  const villageBlocks = Math.max(1, Math.ceil(people / SCALING_POLICY.villageBlock.maximum));
  const topology = topologyCounts(people, villageBlocks);
  if (people <= 20) return scale("micro_commons", 12, 1, "seed", ["micro_commons"], topology);
  if (people <= SCALING_POLICY.villageBlock.maximum) return scale("village_block", SCALING_POLICY.villageBlock.preferred, 1, "single_node", ["village_block"], topology);
  if (people <= 750) return scale("multi_block_district", SCALING_POLICY.villageBlock.preferred, villageBlocks, "mixed_topology", ["village_block", "district_capability"], topology);
  if (people <= 1500) return scale("town_city_layer", SCALING_POLICY.villageBlock.preferred, villageBlocks, "federated_layers", ["village_block", "district_capability", "town_city_capability"], topology);
  return scale("regional_membrane", SCALING_POLICY.villageBlock.preferred, villageBlocks, "federated_layers", ["village_block", "district_capability", "town_city_capability", "regional_membrane"], topology);
}

export function scaleWorldManifest(baseManifest, population) {
  const people = clampPopulation(population);
  const scaleState = inferScale(people);
  const baseClone = structuredClone(baseManifest);
  const populationRatio = people / Math.max(1, Number(baseManifest.population?.residents || 80));
  const topology = buildMixedTopology(baseManifest, people, scaleState);

  return {
    ...baseClone,
    world_id: `${baseManifest.world_id}_pop_${people}`,
    population: populationState(baseManifest, people),
    scale: scaleState,
    zones: topology.zones,
    structures: topology.structures,
    paths: topology.paths,
    infrastructure_nodes: topology.infrastructure_nodes,
    residents: topology.residents,
    daily_events: topology.daily_events,
    scenario_states: remapScenarios(baseManifest.scenario_states || [], topology.objectGroups),
    resource_telemetry: scaleTelemetry(baseManifest.resource_telemetry, populationRatio),
    unknowns: [
      ...(baseManifest.unknowns || []),
      "Population commits use ciac_scaling_policy_v0 research thresholds. This is topology logic, not site design, permitting, or professional certification.",
    ],
  };
}

export function worldBounds(manifest) {
  const points = [
    ...(manifest.zones || []).flatMap(zone => corners(zone)),
    ...(manifest.structures || []).map(item => item.position),
    ...(manifest.infrastructure_nodes || []).map(item => item.position),
    ...(manifest.paths || []).flatMap(path => path.points || []),
  ].filter(Boolean);
  if (!points.length) return { center: [0, 0, 0], size: [92, 0, 76], radius: 60 };
  const xs = points.map(point => Number(point.x || 0));
  const zs = points.map(point => Number(point.z || 0));
  const minX = Math.min(...xs);
  const maxX = Math.max(...xs);
  const minZ = Math.min(...zs);
  const maxZ = Math.max(...zs);
  const width = Math.max(92, maxX - minX + 34);
  const depth = Math.max(76, maxZ - minZ + 34);
  return {
    center: [(minX + maxX) / 2, 0, (minZ + maxZ) / 2],
    size: [width, 0, depth],
    radius: Math.max(width, depth),
  };
}

function buildMixedTopology(baseManifest, people, scaleState) {
  const prototypes = prototypesFor(baseManifest);
  const blockCount = scaleState.implied_village_blocks;
  const blockCenters = blockOffsets(blockCount);
  const counts = scaleState.topology_counts;
  const blockPopulations = distributePeople(people, blockCount);
  const objectGroups = {};

  const zones = buildScaledZones(prototypes, people, blockCount, blockCenters);
  const structures = [
    ...buildResidentialPods(prototypes, people, blockCenters, counts.residential_pods, objectGroups),
    ...buildCellHostStructures(prototypes, "structure_common_house", "common_house", "Common House", counts.common_houses, blockPopulations, blockCenters, objectGroups, {
      moduleRefs: ["social_cultural_commons.belonging_without_coercion.v0_1", "labor_time.life_burden_ledger.v0_1"],
    }),
    ...buildDistrictVenues(prototypes, people, blockCenters, objectGroups),
    ...buildCellHostStructures(prototypes, "structure_food_commons", "food_commons", "Food Access", counts.food_commons, blockPopulations, blockCenters, objectGroups, {
      moduleRefs: ["food.protein_commons_supplement.v0_1"],
    }),
    ...buildCellHostStructures(prototypes, "structure_care_room", "care_room", "Care Access", counts.care_rooms, blockPopulations, blockCenters, objectGroups),
    ...buildMaintenanceStructures(prototypes, people, blockCenters, objectGroups),
  ];
  const infrastructure_nodes = buildInfrastructureNodes(prototypes, people, blockCenters, objectGroups);
  const paths = buildScaledPaths(prototypes, blockCenters, structures, infrastructure_nodes);
  const residents = remapResidents(baseManifest.residents || [], structures);
  const daily_events = remapDailyEvents(baseManifest.daily_events || [], residents, structures, infrastructure_nodes);

  return { zones, structures, paths, infrastructure_nodes, residents, daily_events, objectGroups };
}

function buildScaledZones(prototypes, people, blockCount, blockCenters) {
  const bounds = boundsForCenters(blockCenters);
  const residential = cloneZone(prototypes.zone("zone_residential_ring"), {
    id: "zone_residential_cells",
    label: `${blockCount} Residential Cell${blockCount === 1 ? "" : "s"}`,
    position: v(bounds.centerX, -0.04, bounds.centerZ),
    size: v(Math.max(62, bounds.width + 44), 0.05, Math.max(42, bounds.depth + 34)),
  });
  const common = cloneZone(prototypes.zone("zone_common_core"), {
    id: "zone_common_network",
    label: people > 150 ? "Commons Network" : "Common Core",
    position: v(0, -0.03, 0),
    size: v(people > 150 ? 48 : 32, 0.05, people > 150 ? 30 : 22),
  });
  const food = cloneZone(prototypes.zone("zone_food_garden"), {
    id: "zone_food_garden_network",
    label: people > 150 ? "Food + Garden Network" : "Food Garden",
    position: v(0, -0.05, bounds.maxZ + 20),
    size: v(Math.max(42, bounds.width * 0.7), 0.05, 22),
  });
  const service = cloneZone(prototypes.zone("zone_service_edge"), {
    id: "zone_service_edge_network",
    label: people > 150 ? "Federated Service Edge" : "Service Edge",
    position: v(bounds.maxX + 22, -0.06, bounds.centerZ),
    size: v(22, 0.05, Math.max(32, bounds.depth + 28)),
  });
  const mobility = cloneZone(prototypes.zone("zone_mobility_loop"), {
    id: "zone_access_network",
    label: "Accessible Daily Need Network",
    position: v(bounds.centerX, -0.07, bounds.centerZ),
    size: v(Math.max(72, bounds.width + 62), 0.04, Math.max(58, bounds.depth + 56)),
  });
  return [common, residential, food, service, mobility];
}

function buildResidentialPods(prototypes, people, blockCenters, count, objectGroups) {
  const policy = policyForType("residential_pod");
  const prototype = prototypes.structure("structure_residential_pod_1");
  const residentsPerPod = distributePeople(people, count);
  const pods = Array.from({ length: count }, (_, index) => {
    const block = blockCenters[index % blockCenters.length];
    const localIndex = Math.floor(index / blockCenters.length);
    const offset = podOffset(localIndex, count, blockCenters.length);
    const served = residentsPerPod[index];
    const id = `structure_residential_pod_${index + 1}`;
    return cloneStructure(prototype, {
      id,
      label: `Residential Pod ${index + 1}`,
      position: translate(block, offset),
      size: scaledSize(prototype.size, Math.min(1.18, Math.max(0.86, Math.sqrt(served / policy.preferred)))),
      occupancy: served,
      policy,
      status: served > policy.maximum ? "warning" : "normal",
      display: {
        cell_id: `cell_${index % blockCenters.length + 1}`,
        label_priority: 4,
      },
    });
  });
  objectGroups.structure_residential_pod_1 = pods.map(item => item.id);
  objectGroups.residential_pod = pods.map(item => item.id);
  return pods;
}

function buildCellHostStructures(prototypes, prototypeId, policyId, label, totalUnits, blockPopulations, blockCenters, objectGroups, options = {}) {
  const policy = policyForType(policyId);
  const prototype = prototypes.structure(prototypeId);
  const unitsByCell = distributeNodeUnits(totalUnits, blockCenters.length);
  const structures = blockCenters.map((block, index) => {
    const unitCount = unitsByCell[index];
    const served = blockPopulations[index];
    const id = `${prototypeId}_cell_${index + 1}`;
    const adjustedPolicy = scaledPolicyCapacity(policy, unitCount);
    const factor = Math.min(1.65, Math.max(0.92, Math.sqrt(served / Math.max(1, adjustedPolicy.preferred))));
    return cloneStructure(prototype, {
      id,
      label: unitCount > 1 ? `${label} ${index + 1} (${unitCount} modules)` : `${label} ${index + 1}`,
      type: prototype.type,
      position: translate(block, serviceOffset(policyId, 0)),
      size: scaledSize(prototype.size, factor),
      occupancy: served,
      policy: adjustedPolicy,
      status: served > adjustedPolicy.maximum ? "warning" : "normal",
      moduleRefs: options.moduleRefs || [],
      display: {
        cell_id: `cell_${index + 1}`,
        label_priority: labelPriorityFor(policyId, 0),
        represented_units: unitCount,
      },
    });
  });
  objectGroups[prototypeId] = [...(objectGroups[prototypeId] || []), ...structures.map(item => item.id)];
  objectGroups[policyId] = [...(objectGroups[policyId] || []), ...structures.map(item => item.id)];
  return structures;
}

function buildDistributedStructures(prototypes, prototypeId, policyId, label, count, people, blockCenters, objectGroups, options = {}) {
  const policy = policyForType(policyId);
  const prototype = prototypes.structure(prototypeId);
  const peoplePerNode = distributePeople(people, count);
  const structures = Array.from({ length: count }, (_, index) => {
    const blockIndex = index % blockCenters.length;
    const block = blockCenters[blockIndex];
    const localIndex = Math.floor(index / blockCenters.length);
    const offset = serviceOffset(policyId, localIndex);
    const served = peoplePerNode[index];
    const id = `${prototypeId}_${index + 1}`;
    const factor = sizeFactorFor(policy, served, options.sizeBase);
    return cloneStructure(prototype, {
      id,
      label: count === 1 ? label : `${label} ${index + 1}`,
      type: options.typeOverride || prototype.type,
      position: translate(block, offset),
      size: scaledSize(prototype.size, factor),
      occupancy: served,
      policy,
      status: served > policy.maximum ? "warning" : "normal",
      display: {
        cell_id: `cell_${blockIndex + 1}`,
        label_priority: labelPriorityFor(policyId, localIndex),
      },
    });
  });
  objectGroups[prototypeId] = [...(objectGroups[prototypeId] || []), ...structures.map(item => item.id)];
  objectGroups[policyId] = [...(objectGroups[policyId] || []), ...structures.map(item => item.id)];
  return structures;
}

function buildDistrictVenues(prototypes, people, blockCenters, objectGroups) {
  if (people < SCALING_POLICY.district.minimum) return [];
  const prototype = prototypes.structure("structure_common_house");
  const policy = policyForType("common_house");
  const count = Math.max(1, Math.ceil(people / SCALING_POLICY.district.maximum));
  const spacing = 34;
  const baseZ = districtBandZ(blockCenters, 92);
  const venues = Array.from({ length: count }, (_, index) => {
    const x = (index - (count - 1) / 2) * spacing;
    return cloneStructure(prototype, {
      id: `structure_district_venue_${index + 1}`,
      label: count === 1 ? "District Commons" : `District Commons ${index + 1}`,
      type: "district_venue",
      position: v(x, 0, baseZ),
      size: scaledSize(prototype.size, 1.45),
      occupancy: Math.round(people / count),
      policy: { ...policy, scale_action: "federate" },
      status: "normal",
      display: {
        cell_id: "district",
        label_priority: 1,
      },
    });
  });
  objectGroups.structure_common_house = [...(objectGroups.structure_common_house || []), ...venues.map(item => item.id)];
  objectGroups.district_venue = venues.map(item => item.id);
  return venues;
}

function buildMaintenanceStructures(prototypes, people, blockCenters, objectGroups) {
  if (people < 150) {
    return buildCellHostStructures(prototypes, "structure_maintenance_shop", "maintenance_tool_cache", "Tool Cache", 1, [people], [blockCenters[0]], objectGroups, {
      moduleRefs: ["education_skill.civic_skill_lattice.v0_1"],
    });
  }
  const prototype = prototypes.structure("structure_maintenance_shop");
  const policy = policyForType("maintenance_tool_cache");
  const workshop = cloneStructure(prototype, {
    id: "structure_district_workshop_1",
    label: "District Workshop",
    type: "maintenance_shop",
    position: v(0, 0, districtBandZ(blockCenters, 120)),
    size: scaledSize(prototype.size, people >= 500 ? 1.45 : 1.22),
    occupancy: people,
    policy: { ...policy, scale_action: "federate" },
    status: "normal",
    moduleRefs: ["education_skill.civic_skill_lattice.v0_1"],
    display: {
      cell_id: "district",
      label_priority: 1,
    },
  });
  objectGroups.structure_maintenance_shop = [...(objectGroups.structure_maintenance_shop || []), workshop.id];
  return [workshop];
}

function buildInfrastructureNodes(prototypes, people, blockCenters, objectGroups) {
  const waterPolicy = policyForType("potable_water");
  const sanitationPolicy = policyForType("sanitation_access");
  const energyPolicy = policyForType("risk_resilience_cell");
  const blockCount = blockCenters.length;
  const water = Array.from({ length: blockCount }, (_, index) => cloneNode(prototypes.node("node_water_reserve"), {
    id: `node_water_reserve_${index + 1}`,
    label: blockCount === 1 ? "Water Source + Reserve" : `Water Reserve ${index + 1}`,
    position: translate(blockCenters[index], { x: -22, y: 0, z: 28 }),
    residentsServed: Math.ceil(people / blockCount),
    policy: waterPolicy,
    status: people >= waterPolicy.minimum ? "warning" : "normal",
    display: {
      cell_id: `cell_${index + 1}`,
      label_priority: 3,
    },
  }));
  const energy = Array.from({ length: blockCount }, (_, index) => cloneNode(prototypes.node("node_solar_battery"), {
    id: `node_solar_battery_${index + 1}`,
    label: blockCount === 1 ? "Solar + Critical Battery" : `Critical Energy ${index + 1}`,
    position: translate(blockCenters[index], { x: 0, y: 0, z: -40 }),
    residentsServed: Math.ceil(people / blockCount),
    policy: energyPolicy,
    status: "normal",
    display: {
      cell_id: `cell_${index + 1}`,
      label_priority: 3,
    },
  }));
  const sanitation = Array.from({ length: blockCount }, (_, index) => cloneNode(prototypes.node("node_sanitation_waste"), {
    id: `node_sanitation_waste_${index + 1}`,
    label: blockCount === 1 ? "Sanitation + Waste" : `Sanitation Access ${index + 1}`,
    position: translate(blockCenters[index], { x: 42, y: 0, z: -12 }),
    residentsServed: Math.ceil(people / blockCount),
    policy: sanitationPolicy,
    status: "normal",
    display: {
      cell_id: `cell_${index + 1}`,
      label_priority: 3,
    },
  }));
  const governancePolicy = policyForType("governance_circle");
  const governance = [cloneNode(prototypes.node("node_risk_governance"), {
    id: "node_governance_federation",
    label: people > 150 ? "Federated Governance Board" : "Risk + Governance Board",
    position: v(-34, 0, people > 150 ? districtBandZ(blockCenters, 120) : -8),
    residentsServed: people,
    policy: governancePolicy,
    status: people > governancePolicy.maximum ? "warning" : "normal",
    display: {
      cell_id: "district",
      label_priority: 1,
    },
  })];
  const reviewedWater = people >= waterPolicy.minimum ? [cloneNode(prototypes.node("node_water_reserve"), {
    id: "node_reviewed_water_oversight",
    label: "Reviewed Water Oversight",
    position: v(34, 0, districtBandZ(blockCenters, 120)),
    residentsServed: people,
    policy: { ...waterPolicy, scale_action: "federate" },
    status: "warning",
    display: {
      cell_id: "district",
      label_priority: 1,
    },
  })] : [];
  objectGroups.node_water_reserve = water.map(item => item.id);
  objectGroups.water = [...water.map(item => item.id), ...reviewedWater.map(item => item.id)];
  objectGroups.node_solar_battery = energy.map(item => item.id);
  objectGroups.node_sanitation_waste = sanitation.map(item => item.id);
  objectGroups.node_risk_governance = governance.map(item => item.id);
  return [...water, ...reviewedWater, ...energy, ...sanitation, ...governance];
}

function buildScaledPaths(prototypes, blockCenters, structures, nodes) {
  const pathPrototype = prototypes.path("path_daily_spine");
  const paths = [];
  blockCenters.forEach((center, index) => {
    const cellId = `cell_${index + 1}`;
    const cellStructures = structures.filter(item => item.display?.cell_id === cellId);
    const cellNodes = nodes.filter(item => item.display?.cell_id === cellId);
    const pods = nearestPoints(cellStructures.filter(item => item.type === "residential_pod").map(item => item.position), center, 8);
    const common = nearestPoint(cellStructures.filter(item => item.type === "common_house").map(item => item.position), center);
    const food = nearestPoint(cellStructures.filter(item => item.type === "food_commons").map(item => item.position), center);
    const care = nearestPoint(cellStructures.filter(item => item.type === "care_room").map(item => item.position), center);
    const quiet = nearestPoint(cellStructures.filter(item => item.type === "quiet_room").map(item => item.position), center);
    const water = nearestPoint(cellNodes.filter(item => item.type === "water").map(item => item.position), center);
    const energy = nearestPoint(cellNodes.filter(item => item.type === "energy").map(item => item.position), center);
    const sanitation = nearestPoint(cellNodes.filter(item => item.type === "sanitation").map(item => item.position), center);
    paths.push(clonePath(pathPrototype, `path_${cellId}_pod_loop`, `Cell ${index + 1} Pod Loop`, loopPoints(pods)));
    paths.push(clonePath(pathPrototype, `path_${cellId}_daily_access`, `Cell ${index + 1} Daily Access`, compactPoints([common, food, care, quiet])));
    paths.push(clonePath(pathPrototype, `path_${cellId}_service_access`, `Cell ${index + 1} Service Access`, compactPoints([water, center, energy, sanitation])));
  });
  const districtTargets = compactPoints([
    ...structures.filter(item => item.type === "district_venue" || item.type === "maintenance_shop").map(item => item.position),
    ...nodes.filter(item => item.id === "node_governance_federation" || item.id === "node_reviewed_water_oversight").map(item => item.position),
  ]);
  if (districtTargets.length >= 2) {
    paths.push(clonePath(pathPrototype, "path_district_federation", "District Federation Spine", orderedPoints(districtTargets)));
  }
  return paths;
}

function remapResidents(baseResidents, structures) {
  const pods = structures.filter(item => item.type === "residential_pod");
  const count = Math.min(HUMAN_VISIBLE_AGENT_COUNT, Math.max(1, baseResidents.length));
  return Array.from({ length: count }, (_, index) => {
    const source = baseResidents[index % baseResidents.length] || {};
    const home = pods[index % Math.max(1, pods.length)];
    const offset = miniOffset(index);
    return {
      ...source,
      id: `resident_${source.archetype || "resident"}_${index + 1}`,
      label: source.label || `Resident ${index + 1}`,
      home_structure_id: home?.id || source.home_structure_id,
      position: home ? translate(home.position, offset) : source.position,
    };
  });
}

function remapDailyEvents(baseEvents, residents, structures, nodes) {
  const objects = [...structures, ...nodes];
  const byType = groupIdsByType(objects);
  return baseEvents.map((event, index) => {
    const resident = residents[index % Math.max(1, residents.length)];
    const targetType = targetTypeFor(event.location_id);
    const locationId = (byType[targetType] || byType.common_house || byType.residential_pod || [event.location_id])[index % Math.max(1, (byType[targetType] || []).length || 1)];
    return {
      ...event,
      id: `event_${index + 1}_${event.type || "daily"}`,
      resident_id: resident?.id || event.resident_id,
      location_id: locationId,
    };
  });
}

function remapScenarios(scenarios, objectGroups) {
  return scenarios.map(scenario => ({
    ...scenario,
    timeline: (scenario.timeline || []).map(step => ({
      ...step,
      affected_objects: unique((step.affected_objects || []).flatMap(id => objectGroups[id] || objectGroups[targetTypeFor(id)] || [id])),
    })),
  }));
}

function topologyCounts(people, villageBlocks) {
  return {
    village_blocks: villageBlocks,
    residential_pods: countForPopulation(people, "residential_pod"),
    common_houses: countForPopulation(people, "common_house", { capacity: policyForType("common_house").maximum }),
    food_commons: countForPopulation(people, "food_commons", { capacity: policyForType("food_commons").maximum }),
    protein_commons: countForPopulation(people, "protein_commons", { capacity: policyForType("protein_commons").maximum }),
    care_rooms: countForPopulation(people, "care_room", { capacity: policyForType("care_room").maximum }),
    quiet_rooms: Math.max(villageBlocks, countForPopulation(people, "quiet_room", { capacity: policyForType("quiet_room").maximum })),
    social_commons: countForPopulation(people, "common_house", { capacity: policyForType("common_house").maximum }),
    water_reserves: villageBlocks,
    sanitation_cells: villageBlocks,
    local_tool_caches: villageBlocks,
  };
}

function scale(scaleClass, recommendedUnitSize, impliedVillageBlocks, scalingMode, activeLayers, topologyCountsValue) {
  return {
    scale_class: scaleClass,
    recommended_unit_size: recommendedUnitSize,
    implied_village_blocks: impliedVillageBlocks,
    scaling_mode: scalingMode,
    active_layers: activeLayers,
    topology_policy_id: SCALING_POLICY.id,
    topology_counts: topologyCountsValue,
  };
}

function populationState(baseManifest, population) {
  return {
    ...(baseManifest.population || {}),
    residents: population,
    households: Math.max(1, Math.ceil(population / 2)),
    active_scale_slider_value: population,
  };
}

function scaleTelemetry(telemetry = {}, populationRatio) {
  return {
    ...telemetry,
    resources: (telemetry.resources || []).map(resource => ({
      ...resource,
      capacity: round(Number(resource.capacity || 0) * populationRatio),
      current: round(Number(resource.current || 0) * populationRatio),
      minimum: round(Number(resource.minimum || 0) * populationRatio),
      reserve_floor: round(Number(resource.reserve_floor || 0) * populationRatio),
      net_per_day: round(Number(resource.net_per_day || 0) * populationRatio),
      drawdown: round(Number(resource.drawdown || 0) * populationRatio),
      total_released: round(Number(resource.total_released || 0) * populationRatio),
      total_refilled: round(Number(resource.total_refilled || 0) * populationRatio),
      total_curtailed: round(Number(resource.total_curtailed || 0) * populationRatio),
    })),
    labor: {
      ...(telemetry.labor || {}),
      maintenance_hours_per_week: round(Number(telemetry.labor?.maintenance_hours_per_week || 0) * populationRatio),
      care_hours_per_week: round(Number(telemetry.labor?.care_hours_per_week || 0) * populationRatio),
    },
  };
}

function prototypesFor(manifest) {
  return {
    structure: id => (manifest.structures || []).find(item => item.id === id) || (manifest.structures || [])[0] || {},
    node: id => (manifest.infrastructure_nodes || []).find(item => item.id === id) || (manifest.infrastructure_nodes || [])[0] || {},
    zone: id => (manifest.zones || []).find(item => item.id === id) || (manifest.zones || [])[0] || {},
    path: id => (manifest.paths || []).find(item => item.id === id) || (manifest.paths || [])[0] || {},
  };
}

function cloneStructure(prototype, updates) {
  const moduleRefs = [...(prototype.module_refs || []), ...(updates.moduleRefs || [])];
  const state = {
    ...(prototype.state || {}),
    status: updates.status || prototype.state?.status || "normal",
    occupancy: updates.occupancy,
    residents_served: updates.occupancy,
  };
  return {
    ...prototype,
    id: updates.id,
    label: updates.label,
    type: updates.type || prototype.type,
    position: updates.position,
    rotation: prototype.rotation || v(0, 0, 0),
    size: updates.size || prototype.size,
    module_refs: unique(moduleRefs),
    state,
    display: {
      ...(prototype.display || {}),
      ...(updates.display || {}),
    },
    scaling_policy: objectPolicy(updates.policy, updates.occupancy),
  };
}

function cloneNode(prototype, updates) {
  return {
    ...prototype,
    id: updates.id,
    label: updates.label,
    position: updates.position,
    metrics: {
      ...(prototype.metrics || {}),
      status: updates.status || prototype.metrics?.status || "normal",
      residents_served: updates.residentsServed,
    },
    display: {
      ...(prototype.display || {}),
      ...(updates.display || {}),
    },
    scaling_policy: objectPolicy(updates.policy, updates.residentsServed),
  };
}

function cloneZone(prototype, updates) {
  return {
    ...prototype,
    ...updates,
  };
}

function clonePath(prototype, id, labelValue, points) {
  const safePoints = orderedPoints(points).slice(0, 60);
  return {
    ...prototype,
    id,
    label: labelValue,
    points: safePoints.length >= 2 ? safePoints : [v(-1, 0, 0), v(1, 0, 0)],
  };
}

function objectPolicy(policy, residentsServed) {
  if (!policy) return null;
  const served = Number(residentsServed || 0);
  return {
    policy_id: policy.policy_id || policy.id,
    source_policy_id: SCALING_POLICY.id,
    scale_action: policy.scale_action,
    residents_served: served,
    preferred_capacity: policy.preferred,
    soft_threshold: policy.maximum,
    hard_threshold: policy.hard_max,
    human_factor_driver: policy.human_factor_driver,
    ui_warning: served > Number(policy.maximum || Infinity) ? policy.ui_warning : "",
  };
}

function blockOffsets(count) {
  const columns = Math.ceil(Math.sqrt(count));
  const rows = Math.ceil(count / columns);
  const centerX = ((columns - 1) * BLOCK_SPACING_X) / 2;
  const centerZ = ((rows - 1) * BLOCK_SPACING_Z) / 2;
  return Array.from({ length: count }, (_, index) => ({
    x: (index % columns) * BLOCK_SPACING_X - centerX,
    y: 0,
    z: Math.floor(index / columns) * BLOCK_SPACING_Z - centerZ,
  }));
}

function distributeNodeUnits(totalUnits, count) {
  const total = Math.max(count, Number(totalUnits || count));
  const base = Math.floor(total / count);
  const remainder = total % count;
  return Array.from({ length: count }, (_, index) => base + (index < remainder ? 1 : 0));
}

function scaledPolicyCapacity(policy, unitCount) {
  const units = Math.max(1, Number(unitCount || 1));
  return {
    ...policy,
    preferred: Number(policy.preferred || 0) * units,
    maximum: Number(policy.maximum || 0) * units,
    hard_max: Number(policy.hard_max || 0) ? Number(policy.hard_max) * units : policy.hard_max,
  };
}

function distributePeople(people, count) {
  const base = Math.floor(people / count);
  const remainder = people % count;
  return Array.from({ length: count }, (_, index) => base + (index < remainder ? 1 : 0));
}

function podOffset(index, totalCount, blockCount) {
  const perCell = Math.ceil(totalCount / Math.max(1, blockCount));
  const slots = Math.max(6, Math.min(10, perCell));
  const ring = Math.floor(index / slots);
  const angle = ((index % slots) / slots) * Math.PI * 2 + (ring % 2 ? Math.PI / slots : 0);
  const radius = 56 + ring * 14;
  return { x: Math.cos(angle) * radius, y: 0, z: Math.sin(angle) * radius };
}

function serviceOffset(policyId, index) {
  const offsets = {
    common_house: [{ x: 0, y: 0, z: 0 }],
    food_commons: [{ x: 0, y: 0, z: 26 }],
    protein_commons: [{ x: 0, y: 0, z: 26 }],
    care_room: [{ x: -32, y: 0, z: 0 }],
    quiet_room: [{ x: 26, y: 0, z: 0 }],
    maintenance_tool_cache: [{ x: 34, y: 0, z: -28 }],
  };
  const choices = offsets[policyId] || [{ x: 14, y: 0, z: 0 }];
  const local = choices[index % choices.length];
  const spread = Math.floor(index / choices.length) * 5;
  return { x: local.x + spread, y: 0, z: local.z + spread };
}

function labelPriorityFor(policyId, localIndex) {
  if (localIndex > 0) return 5;
  if (policyId === "common_house") return 2;
  if (policyId === "food_commons" || policyId === "care_room") return 3;
  if (policyId === "quiet_room" || policyId === "protein_commons") return 5;
  if (policyId === "maintenance_tool_cache") return 5;
  return 4;
}

function compactPoints(points) {
  return (points || []).filter(Boolean);
}

function loopPoints(points) {
  const ordered = radialOrder(points);
  if (ordered.length > 2) return [...ordered, ordered[0]];
  return ordered;
}

function nearestPoint(points, origin) {
  return nearestPoints(points, origin, 1)[0];
}

function nearestPoints(points, origin, limit) {
  return compactPoints(points)
    .sort((a, b) => distance(a, origin) - distance(b, origin))
    .slice(0, limit);
}

function radialOrder(points) {
  if (!points?.length) return [];
  const center = {
    x: points.reduce((sum, point) => sum + Number(point.x || 0), 0) / points.length,
    z: points.reduce((sum, point) => sum + Number(point.z || 0), 0) / points.length,
  };
  return [...points].sort((a, b) => Math.atan2(a.z - center.z, a.x - center.x) - Math.atan2(b.z - center.z, b.x - center.x));
}

function distance(a, b) {
  const dx = Number(a?.x || 0) - Number(b?.x || 0);
  const dz = Number(a?.z || 0) - Number(b?.z || 0);
  return Math.sqrt(dx * dx + dz * dz);
}

function miniOffset(index) {
  const angle = (index / HUMAN_VISIBLE_AGENT_COUNT) * Math.PI * 2;
  return { x: Math.cos(angle) * 2.6, y: 0, z: Math.sin(angle) * 2.2 };
}

function sizeFactorFor(policy, served, sizeBase = 1) {
  if (!policy) return sizeBase;
  return sizeBase * Math.min(1.35, Math.max(0.78, Math.sqrt(served / Math.max(1, policy.preferred))));
}

function scaledSize(size, factor) {
  return {
    x: round(Number(size?.x || 6) * factor),
    y: round(Number(size?.y || 3) * Math.min(1.12, Math.max(0.92, factor))),
    z: round(Number(size?.z || 5) * factor),
  };
}

function boundsForCenters(centers) {
  const xs = centers.map(point => point.x);
  const zs = centers.map(point => point.z);
  const minX = Math.min(...xs);
  const maxX = Math.max(...xs);
  const minZ = Math.min(...zs);
  const maxZ = Math.max(...zs);
  return {
    minX,
    maxX,
    minZ,
    maxZ,
    centerX: (minX + maxX) / 2,
    centerZ: (minZ + maxZ) / 2,
    width: maxX - minX,
    depth: maxZ - minZ,
  };
}

function districtBandZ(centers, offset) {
  return Math.min(...centers.map(point => Number(point.z || 0))) - Number(offset || 90);
}

function groupIdsByType(objects) {
  return objects.reduce((groups, object) => {
    groups[object.type] = [...(groups[object.type] || []), object.id];
    return groups;
  }, {});
}

function targetTypeFor(id) {
  const value = String(id || "");
  if (value.includes("water")) return "water";
  if (value.includes("solar") || value.includes("energy")) return "energy";
  if (value.includes("sanitation")) return "sanitation";
  if (value.includes("food")) return "food_commons";
  if (value.includes("protein")) return "protein_commons";
  if (value.includes("care")) return "care_room";
  if (value.includes("quiet")) return "quiet_room";
  if (value.includes("maintenance")) return "maintenance_shop";
  if (value.includes("social")) return "social_cultural";
  if (value.includes("common")) return "common_house";
  if (value.includes("residential") || value.includes("pod")) return "residential_pod";
  if (value.includes("risk") || value.includes("governance")) return "risk";
  return value;
}

function orderedPoints(points) {
  return [...(points || [])].filter(Boolean).sort((a, b) => (a.z - b.z) || (a.x - b.x));
}

function translate(vector, offset) {
  return {
    x: Number(vector?.x || 0) + Number(offset?.x || 0),
    y: Number(vector?.y || 0) + Number(offset?.y || 0),
    z: Number(vector?.z || 0) + Number(offset?.z || 0),
  };
}

function v(x, y, z) {
  return { x: Number(x), y: Number(y), z: Number(z) };
}

function corners(zone) {
  const x = Number(zone.position?.x || 0);
  const z = Number(zone.position?.z || 0);
  const halfX = Number(zone.size?.x || 0) / 2;
  const halfZ = Number(zone.size?.z || 0) / 2;
  return [
    { x: x - halfX, z: z - halfZ },
    { x: x + halfX, z: z + halfZ },
  ];
}

function unique(items) {
  return Array.from(new Set(items));
}

function clampPopulation(value) {
  return Math.max(12, Math.min(1500, Math.round(Number(value || SCALING_POLICY.villageBlock.preferred))));
}

function round(value) {
  return Math.round(Number(value || 0) * 1000) / 1000;
}
