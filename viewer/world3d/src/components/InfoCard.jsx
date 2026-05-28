import { label } from "../world/layout.js";

export default function InfoCard({ object, evidenceCard, manifest, mode, scenario }) {
  if (!object) {
    return (
      <aside className="info-card">
        <h2>Civic Floor World</h2>
        <p>Select a structure, node, path, or zone.</p>
      </aside>
    );
  }
  const card = evidenceCard || {};
  const modules = modulesForObject(manifest, object, card);
  const reviewItems = reviewItemsForModules(modules, card);
  const operatingNotes = operatingNotesForObject(object, card, modules);
  const sources = sourcesForCard(card);
  const status = displayStatus(object, card);
  const scalingPolicy = object.scaling_policy || null;
  return (
    <aside className="info-card">
      <div className="info-card-title">
        <h2>{object.label || card.title || label(object.id)}</h2>
        <span>{label(object.type || object.object_kind)}</span>
      </div>
      <p>{card.summary || "Model object generated from the world manifest."}</p>
      {mode === "stress" && scenario ? (
        <div className="info-highlight">
          <strong>{scenario.label}</strong>
          <span>{scenario.status}</span>
        </div>
      ) : null}
      <dl>
        <dt>Status</dt>
        <dd>{status}</dd>
        {object.state?.occupancy ? (
          <>
            <dt>Occupancy</dt>
            <dd>{object.state.occupancy}</dd>
          </>
        ) : null}
        {object.metrics?.residents_served ? (
          <>
            <dt>Serves</dt>
            <dd>{formatNumber(object.metrics.residents_served)} residents</dd>
          </>
        ) : null}
        {scalingPolicy?.residents_served ? (
          <>
            <dt>Scale Fit</dt>
            <dd>{scaleFitLabel(scalingPolicy)}</dd>
          </>
        ) : null}
        {object.metrics?.daily_net !== undefined ? (
          <>
            <dt>Daily Net</dt>
            <dd>{formatNumber(object.metrics.daily_net)}</dd>
          </>
        ) : null}
        {object.metrics?.stored !== undefined ? (
          <>
            <dt>Stored</dt>
            <dd>{formatNumber(object.metrics.stored)}</dd>
          </>
        ) : null}
      </dl>
      <section>
        <h3>Contained Modules</h3>
        <div className="contained-modules">
          {modules.length ? modules.map(module => (
            <article className={`contained-module status-${module.status}`} key={module.module_id || module.pattern_id}>
              <strong>{module.label || label(module.pattern_id || module.module_id)}</strong>
              <span>{label(module.domain || module.tier)} | {label(module.status || "modeled")}</span>
              <p>{module.summary || "Attached model module."}</p>
              {module.critical_resources?.length ? <small>Critical resources: {module.critical_resources.map(label).join(", ")}</small> : null}
              {module.failure_modes?.length ? <small>Failure modes: {module.failure_modes.map(mode => label(mode.mode)).join(", ")}</small> : null}
            </article>
          )) : <p>No modules are attached to this object yet.</p>}
        </div>
      </section>
      <section>
        <h3>Operating Notes</h3>
        <ul>
          {operatingNotes.map(item => <li key={item}>{item}</li>)}
        </ul>
      </section>
      {reviewItems.length ? (
        <section>
          <h3>Review Queue</h3>
          <ul>
            {reviewItems.map(item => <li key={item}>{item}</li>)}
          </ul>
        </section>
      ) : null}
      {sources.length ? (
        <section>
          <h3>Research Sources</h3>
          <div className="source-list">
            {sources.map(source => (
              <article className="source-item" key={source.id}>
                <strong>{source.title || source.id}</strong>
                <span>{source.organization || "unknown"} | {label(source.evidence_quality || "mixed")}</span>
                {source.supports?.length ? <small>Supports: {source.supports.map(label).slice(0, 4).join(", ")}</small> : null}
                {source.url ? <a href={source.url} target="_blank" rel="noreferrer">Open source</a> : null}
              </article>
            ))}
          </div>
          {card.source_note ? <p>{card.source_note}</p> : null}
        </section>
      ) : null}
      {scalingPolicy ? (
        <section>
          <h3>Scaling Policy</h3>
          <ul>
            <li>{label(scalingPolicy.scale_action)} from {scalingPolicy.source_policy_id}</li>
            <li>{formatNumber(scalingPolicy.residents_served)} served; preferred {formatNumber(scalingPolicy.preferred_capacity)}, soft {formatNumber(scalingPolicy.soft_threshold)}</li>
            {scalingPolicy.human_factor_driver ? <li>{scalingPolicy.human_factor_driver}</li> : null}
            {scalingPolicy.ui_warning ? <li>{scalingPolicy.ui_warning}</li> : null}
          </ul>
        </section>
      ) : null}
    </aside>
  );
}

function sourcesForCard(card = {}) {
  if (Array.isArray(card.sources) && card.sources.length) {
    return card.sources;
  }
  return (card.source_ids || []).map(sourceId => ({
    id: sourceId,
    title: sourceId,
    organization: "source registry",
    evidence_quality: "mixed",
  }));
}

function modulesForObject(manifest = {}, object = {}, card = {}) {
  const refs = new Set([...(object.module_refs || []), ...(card.module_refs || [])]);
  const modules = manifest.modules || [];
  const resolved = modules.filter(module => refs.has(module.module_id) || refs.has(module.pattern_id));
  const unresolved = Array.from(refs)
    .filter(ref => !resolved.some(module => module.module_id === ref || module.pattern_id === ref))
    .map(ref => ({
      module_id: ref,
      pattern_id: ref,
      label: label(ref),
      domain: domainFromRef(ref),
      status: "contract_defined",
      summary: "Referenced model layer.",
    }));
  return [...resolved, ...unresolved].sort((a, b) => String(a.label || a.module_id).localeCompare(String(b.label || b.module_id)));
}

function reviewItemsForModules(modules, card) {
  const items = new Set(card.review_required || []);
  modules.forEach(module => {
    if (module.review_status === "review_required") {
      items.add(`${label(module.label || module.pattern_id)} review`);
    }
    (module.failure_modes || []).forEach(mode => {
      if (mode.mitigation) items.add(`${label(mode.mode)} response path`);
    });
  });
  return Array.from(items).filter(Boolean);
}

function operatingNotesForObject(object, card, modules) {
  const notes = new Set((card.assumptions || []).filter(item => !isBoilerplate(item)));
  if (object.systems?.length) notes.add(`Systems: ${object.systems.map(label).join(", ")}`);
  if (modules.some(module => module.domain === "care_health")) {
    notes.add("Care modules are attached here as aggregate operating capacity; personal health data is not represented.");
  }
  if (modules.some(module => module.status === "simulation_connected")) {
    notes.add("At least one contained module is connected to the active simulation.");
  }
  return Array.from(notes).slice(0, 6);
}

function displayStatus(object, card) {
  const raw = object.state?.status || object.metrics?.status || card.status || "modeled";
  if (raw === "provisional") return "Modeled";
  return label(raw);
}

function isBoilerplate(item) {
  const text = String(item).toLowerCase();
  return text.includes("provisional civic simulation") || text.includes("does not certify") || text.includes("proxy geometry");
}

function domainFromRef(ref) {
  const value = String(ref);
  if (value.includes(".")) return value.split(".")[0];
  if (value.startsWith("care_health_")) return "care_health";
  if (value.startsWith("water_")) return "water";
  if (value.startsWith("energy_")) return "energy";
  if (value.startsWith("food_")) return "food";
  return "model";
}

function formatNumber(value) {
  const number = Number(value);
  if (!Number.isFinite(number)) return String(value);
  return number.toLocaleString(undefined, { maximumFractionDigits: 2 });
}

function scaleFitLabel(policy) {
  const served = Number(policy.residents_served || 0);
  const soft = Number(policy.soft_threshold || 0);
  const preferred = Number(policy.preferred_capacity || 0);
  if (soft && served > soft) return "Over soft threshold";
  if (preferred && served > preferred) return "Above preferred";
  return "Within preferred";
}
