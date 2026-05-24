export function stressModeSummary(manifest, selectedScenarioId) {
  const scenarios = manifest.scenario_states || [];
  const active = scenarios.find(scenario => scenario.id === selectedScenarioId) || scenarios[0];
  const warnings = (active?.timeline || []).flatMap(step => step.warnings || []);
  const affected = new Set((active?.timeline || []).flatMap(step => step.affected_objects || []));
  return {
    title: "Stress Mode",
    summary: active ? `${active.label} affects ${affected.size} object(s).` : "No scenario selected.",
    active,
    warnings,
    affected,
    scenarios,
  };
}
