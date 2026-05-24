export function systemsForManifest(manifest) {
  return Object.entries(manifest.overlays || {}).map(([id, overlay]) => ({
    id,
    ...overlay,
  }));
}

export function systemModeSummary(manifest, selectedSystem) {
  const systems = systemsForManifest(manifest);
  const active = systems.find(system => system.id === selectedSystem) || systems[0];
  const messages = active?.messages?.length ? active.messages : [fallbackReason(active)];
  const fields = Object.entries(active?.fields || {})
    .filter(([, value]) => value !== undefined && value !== null)
    .map(([key, value]) => ({
      key,
      value,
    }));
  return {
    title: "Systems Mode",
    summary: active ? active.summary : "No system overlay selected.",
    active,
    systems,
    messages,
    fields,
  };
}

function fallbackReason(system) {
  if (!system) return "No system status is available.";
  if (system.status === "pass" || system.status === "normal") return "No blocking messages are reported for this system.";
  if (system.status === "provisional") return "This system has not reported a capability status yet.";
  return "Status is derived from resource telemetry or capability gate output.";
}
