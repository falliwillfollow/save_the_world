export function vecToArray(vector) {
  return [Number(vector?.x || 0), Number(vector?.y || 0), Number(vector?.z || 0)];
}

export function sizeToArray(size, fallback = [4, 2, 4]) {
  if (!size) return fallback;
  return [Number(size.x || fallback[0]), Number(size.y || fallback[1]), Number(size.z || fallback[2])];
}

export function allWorldObjects(manifest) {
  return [
    ...(manifest.structures || []).map(item => ({ ...item, object_kind: "structure" })),
    ...(manifest.infrastructure_nodes || []).map(item => ({ ...item, object_kind: "infrastructure_node" })),
    ...(manifest.zones || []).map(item => ({ ...item, object_kind: "zone" })),
    ...(manifest.paths || []).map(item => ({ ...item, object_kind: "path" })),
  ];
}

export function objectStatusForMode(object, mode, selectedScenario) {
  if (mode === "stress" && selectedScenario) {
    const affected = new Set((selectedScenario.timeline || []).flatMap(step => step.affected_objects || []));
    if (affected.has(object.id)) return "degraded";
  }
  return object.state?.status || object.metrics?.status || "normal";
}

export function statusColor(status, fallback) {
  if (status === "failed" || status === "fail") return "#b3261e";
  if (status === "promotion_blocked") return "#6b2f90";
  if (status === "degraded" || status === "warning" || status === "warn") return "#c77700";
  if (status === "normal" || status === "pass") return fallback;
  return fallback;
}

export function label(value) {
  return String(value || "").replaceAll("_", " ");
}

export function eventTargetFor(manifest, event) {
  return allWorldObjects(manifest).find(item => item.id === event.location_id);
}
