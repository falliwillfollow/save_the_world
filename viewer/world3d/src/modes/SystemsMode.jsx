export function systemsForManifest(manifest) {
  return Object.entries(manifest.overlays || {}).map(([id, overlay]) => ({
    id,
    ...overlay,
  }));
}

export function systemModeSummary(manifest, selectedSystem) {
  const systems = systemsForManifest(manifest);
  const active = systems.find(system => system.id === selectedSystem) || systems[0];
  return {
    title: "Systems Mode",
    summary: active ? active.summary : "No system overlay selected.",
    active,
    systems,
  };
}
