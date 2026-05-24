import { label } from "../world/layout.js";

const RESOURCE_OBJECT_TYPES = {
  water: ["water"],
  food: ["food_commons", "protein_commons"],
  energy: ["energy"],
};

export function insightModeSummary(manifest, selectedScenarioId) {
  const resourceDiagnostics = resourceBottlenecks(manifest);
  const labor = laborDiagnostic(manifest);
  const scenario = scenarioDiagnostic(manifest, selectedScenarioId);
  const capabilityDiagnostics = capabilityWarnings(manifest);
  const diagnostics = [
    ...resourceDiagnostics,
    labor,
    scenario,
    ...capabilityDiagnostics,
  ].filter(Boolean).sort((a, b) => severityRank(b.severity) - severityRank(a.severity));

  const first = diagnostics[0];
  return {
    title: "Insight Mode",
    summary: first ? first.summary : "No diagnostics available for this committed population.",
    diagnostics,
  };
}

function resourceBottlenecks(manifest) {
  return (manifest.resource_telemetry?.resources || []).map(resource => {
    const capacity = Number(resource.capacity || 0);
    const current = Number(resource.current || 0);
    const reserveFloor = Number(resource.reserve_floor || 0);
    const netPerDay = Number(resource.net_per_day || 0);
    const margin = Math.max(0, current - reserveFloor);
    const daysToFloor = netPerDay < 0 ? margin / Math.abs(netPerDay) : null;
    const minimumRatio = Number(resource.minimum_ratio || 0);
    const drawdownRatio = capacity ? Number(resource.drawdown || 0) / capacity : 0;
    const severity = daysToFloor !== null && daysToFloor < 180
      ? "critical"
      : daysToFloor !== null && daysToFloor < 365
        ? "warning"
        : minimumRatio < 0.3 || drawdownRatio > 0.5
          ? "watch"
          : "stable";
    const objectIds = objectsForResource(manifest, resource.id);
    return {
      id: `resource_${resource.id}`,
      type: "resource",
      system: resource.id,
      severity,
      title: `${resource.label} capacity`,
      summary: daysToFloor === null
        ? `${resource.label} is capacity-positive at ${signed(netPerDay)} ${resource.unit}/day; stress attention should focus on scenario isolation and reserve behavior.`
        : `${resource.label} draws down at ${signed(netPerDay)} ${resource.unit}/day; modeled reserve floor is reached in about ${formatDays(daysToFloor)} if no additional refill or substitution occurs.`,
      metric: daysToFloor === null ? `${signed(netPerDay)}/day` : `${formatDays(daysToFloor)} to floor`,
      object_ids: objectIds,
      module_refs: modulesForObjects(manifest, objectIds),
      evidence_card_id: evidenceForObjects(manifest, objectIds),
    };
  });
}

function laborDiagnostic(manifest) {
  const labor = manifest.resource_telemetry?.labor || {};
  const utilization = Number(labor.utilization || 0);
  const maintenance = Number(labor.maintenance_hours_per_week || 0);
  const severity = utilization > 0.8 ? "critical" : utilization > 0.55 ? "warning" : utilization > 0.25 ? "watch" : "stable";
  const objectIds = objectsBySuffix(manifest, ["structure_maintenance_shop", "node_risk_governance"]);
  return {
    id: "labor_burden",
    type: "labor",
    system: "maintenance",
    severity,
    title: "Commons labor burden",
    summary: `Modeled required commons labor is ${formatAmount(labor.required_minutes_per_resident_per_day)} min/resident/day, with ${formatAmount(maintenance)} maintenance hours/week at this scale.`,
    metric: `${Math.round(utilization * 100)}% use`,
    object_ids: objectIds,
    module_refs: modulesForObjects(manifest, objectIds),
    evidence_card_id: evidenceForObjects(manifest, objectIds),
  };
}

function scenarioDiagnostic(manifest, selectedScenarioId) {
  const scenarios = manifest.scenario_states || [];
  const active = scenarios.find(scenario => scenario.id === selectedScenarioId) || scenarios[0];
  if (!active) return null;
  const affected = Array.from(new Set((active.timeline || []).flatMap(step => step.affected_objects || [])));
  const warnings = (active.timeline || []).flatMap(step => step.warnings || []);
  const severity = warnings.length ? "warning" : affected.length ? "watch" : "stable";
  return {
    id: `scenario_${active.id}`,
    type: "scenario",
    system: "risk",
    severity,
    title: `${active.label} trace`,
    summary: affected.length
      ? `${active.label} touches ${affected.length} world object(s); inspect the highlighted dependency path before treating this scenario as resilient.`
      : `${active.label} has no survival-critical object impact in the current manifest.`,
    metric: warnings.length ? `${warnings.length} warning(s)` : `${affected.length} objects`,
    object_ids: affected,
    module_refs: modulesForObjects(manifest, affected),
    evidence_card_id: evidenceForObjects(manifest, affected),
  };
}

function capabilityWarnings(manifest) {
  return Object.entries(manifest.overlays || {})
    .filter(([, overlay]) => ["warn", "warning", "failed", "fail"].includes(overlay.status))
    .slice(0, 4)
    .map(([id, overlay]) => {
      const objectIds = objectsForCapability(manifest, id);
      return {
        id: `capability_${id}`,
        type: "capability",
        system: id,
        severity: ["failed", "fail"].includes(overlay.status) ? "critical" : "warning",
        title: `${label(id)} capability`,
        summary: overlay.summary || `${label(id)} requires review before promotion.`,
        metric: label(overlay.status),
        object_ids: objectIds,
        module_refs: modulesForObjects(manifest, objectIds),
        evidence_card_id: evidenceForObjects(manifest, objectIds),
      };
    });
}

function objectsForResource(manifest, resourceId) {
  return objectsByType(manifest, RESOURCE_OBJECT_TYPES[resourceId] || [resourceId]);
}

function objectsForCapability(manifest, capabilityId) {
  if (capabilityId.includes("labor")) return objectsBySuffix(manifest, ["structure_maintenance_shop", "structure_quiet_studio"]);
  if (capabilityId.includes("governance")) return objectsBySuffix(manifest, ["node_risk_governance", "structure_common_house"]);
  if (capabilityId.includes("care")) return objectsBySuffix(manifest, ["structure_care_room", "structure_common_house"]);
  if (capabilityId.includes("mobility")) return objectsBySuffix(manifest, ["path_primary_ring", "path_daily_spine"]);
  return objectsByType(manifest, [capabilityId]);
}

function objectsByType(manifest, types) {
  return allObjects(manifest)
    .filter(object => types.includes(object.type) || (object.systems || []).some(system => types.includes(system)))
    .map(object => object.id);
}

function objectsBySuffix(manifest, suffixes) {
  return allObjects(manifest)
    .filter(object => suffixes.some(suffix => object.id === suffix || object.id.endsWith(`__${suffix}`)))
    .map(object => object.id);
}

function modulesForObjects(manifest, objectIds) {
  const ids = new Set(objectIds);
  return Array.from(new Set(allObjects(manifest).filter(object => ids.has(object.id)).flatMap(object => object.module_refs || [])));
}

function evidenceForObjects(manifest, objectIds) {
  const ids = new Set(objectIds);
  return allObjects(manifest).find(object => ids.has(object.id) && object.evidence_card_id)?.evidence_card_id;
}

function allObjects(manifest) {
  return [
    ...(manifest.structures || []),
    ...(manifest.infrastructure_nodes || []),
    ...(manifest.zones || []),
    ...(manifest.paths || []),
  ];
}

function severityRank(severity) {
  return { stable: 1, watch: 2, warning: 3, critical: 4 }[severity] || 0;
}

function signed(value) {
  const numeric = Number(value || 0);
  return `${numeric > 0 ? "+" : ""}${formatAmount(numeric)}`;
}

function formatDays(value) {
  if (!Number.isFinite(value)) return "unknown";
  if (value >= 365) return `${formatAmount(value / 365)} years`;
  return `${formatAmount(value)} days`;
}

function formatAmount(value) {
  return new Intl.NumberFormat("en-US", { maximumFractionDigits: 1 }).format(Number(value || 0));
}
