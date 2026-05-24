import { lifeModeSummary } from "../modes/LifeMode.jsx";
import { insightModeSummary } from "../modes/InsightMode.jsx";
import { systemModeSummary } from "../modes/SystemsMode.jsx";
import { stressModeSummary } from "../modes/StressMode.jsx";
import { allWorldObjects, label } from "../world/layout.js";

export default function OverlayPanel({
  manifest,
  mode,
  timePercent,
  selectedSystem,
  selectedScenarioId,
  onScenarioChange,
  onSelectObject,
  onHighlightObjects,
}) {
  const life = lifeModeSummary(manifest, timePercent);
  const systems = systemModeSummary(manifest, selectedSystem);
  const stress = stressModeSummary(manifest, selectedScenarioId);
  const insight = insightModeSummary(manifest, selectedScenarioId);
  const current = mode === "life" ? life : mode === "systems" ? systems : mode === "stress" ? stress : insight;
  const worldObjects = allWorldObjects(manifest);

  function selectDiagnostic(diagnostic) {
    const linkedObject = worldObjects.find(object => (diagnostic.object_ids || []).includes(object.id));
    onHighlightObjects(diagnostic.object_ids || []);
    if (linkedObject) onSelectObject(linkedObject);
  }

  return (
    <aside className="overlay-panel">
      <h2>{current.title}</h2>
      <p>{current.summary}</p>
      {mode === "life" ? (
        <div className="event-list">
          {life.events.slice(0, 5).map(event => (
            <div className="event-chip" key={event.id}>
              <strong>{event.time}</strong>
              <span>{event.label}</span>
            </div>
          ))}
        </div>
      ) : null}
      {mode === "systems" ? (
        <div className="event-list">
          {(systems.systems || []).slice(0, 9).map(system => (
            <div className="event-chip" key={system.id}>
              <strong>{label(system.id)}</strong>
              <span>{label(system.status)}</span>
            </div>
          ))}
        </div>
      ) : null}
      {mode === "stress" ? (
        <>
          <label className="field-label">
            <span>Scenario</span>
            <select value={selectedScenarioId} onChange={event => onScenarioChange(event.target.value)}>
              {stress.scenarios.map(scenario => (
                <option key={scenario.id} value={scenario.id}>{scenario.label}</option>
              ))}
            </select>
          </label>
          <div className="event-list">
            {(stress.warnings.length ? stress.warnings : ["No survival-critical warning for this scenario state."]).slice(0, 5).map(item => (
              <div className="event-chip" key={item}>
                <strong>Signal</strong>
                <span>{item}</span>
              </div>
            ))}
          </div>
        </>
      ) : null}
      {mode === "insight" ? (
        <div className="diagnostic-list">
          {insight.diagnostics.slice(0, 7).map(diagnostic => (
            <button
              type="button"
              key={diagnostic.id}
              className={`diagnostic-item severity-${diagnostic.severity}`}
              onClick={() => selectDiagnostic(diagnostic)}
              onFocus={() => onHighlightObjects(diagnostic.object_ids || [])}
            >
              <span>
                <strong>{diagnostic.title}</strong>
                <small>{diagnostic.metric}</small>
              </span>
              <em>{diagnostic.summary}</em>
              <i>{(diagnostic.module_refs || []).slice(0, 2).map(label).join(" | ") || "manifest evidence"}</i>
            </button>
          ))}
        </div>
      ) : null}
    </aside>
  );
}
