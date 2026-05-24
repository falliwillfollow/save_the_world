import { Activity, BadgeCheck, Beaker, FileJson, FilePlus2, Play, ShieldAlert } from "lucide-react";

const FOCUS_OPTIONS = [
  { id: "care_health", label: "Care" },
  { id: "water_public_health", label: "Water" },
  { id: "labor_time", label: "Labor" },
  { id: "governance_anticapture", label: "Governance" },
  { id: "mobility_access", label: "Mobility" },
  { id: "risk_resilience", label: "Risk" },
  { id: "all", label: "All" },
];

export default function ResearchLoopPanel({
  focus,
  onFocusChange,
  response,
  loading,
  error,
  onRun,
  onMaterializePatch,
  onAnalyzePatch,
  onPromotePatch,
  materializingPatchId,
  analyzingPatchId,
  promotingPatchId,
  materializationReports = {},
  impactReports = {},
  promotionReports = {},
}) {
  const run = response?.research_loop;
  const patches = response?.patch_proposals || [];
  const candidates = response?.candidates || [];
  const source = run?.candidate_source?.replaceAll("_", " ") || "none";
  const resultFocus = run?.source?.focus?.replaceAll("_", " ");
  const n8nState = run?.n8n?.called ? (run.n8n.ok ? "n8n ok" : "n8n fallback") : "n8n off";
  const traceMarker = run?.n8n?.trace_marker;
  const sourceCount = run?.n8n?.context_source_ids?.length || 0;
  const brief = run?.n8n?.discovery_brief?.summary || run?.n8n?.discovery_brief?.note;

  return (
    <aside className="research-panel">
      <div className="research-panel-head">
        <span><Beaker size={16} aria-hidden="true" /> Research Lab</span>
        <button type="button" onClick={onRun} disabled={loading} title="Run CIaC research loop">
          <Play size={15} aria-hidden="true" />
          <span>{loading ? "Running" : "Run"}</span>
        </button>
      </div>

      <div className="research-focus" role="tablist" aria-label="Research focus">
        {FOCUS_OPTIONS.map(option => (
          <button
            key={option.id}
            type="button"
            className={focus === option.id ? "is-active" : ""}
            onClick={() => onFocusChange(option.id)}
            role="tab"
            aria-selected={focus === option.id}
          >
            {option.label}
          </button>
        ))}
      </div>

      {error ? (
        <div className="research-message is-error">
          <ShieldAlert size={15} aria-hidden="true" />
          <span>{error}</span>
        </div>
      ) : null}

      {run ? (
        <>
          <div className="research-summary">
            <strong>{run.status.replaceAll("_", " ")}</strong>
            <span>{resultFocus ? `${resultFocus} | ` : ""}{candidates.length} candidates | {patches.length} patch proposals | {source} | {n8nState}</span>
            {traceMarker ? <small>trace {traceMarker} | {sourceCount} source(s)</small> : null}
            {brief ? <em>{brief}</em> : null}
          </div>
          <div className="research-artifact">
            <FileJson size={14} aria-hidden="true" />
            <span>{response.research_loop_path}</span>
          </div>
          <div className="research-list">
            {patches.slice(0, 4).map(patch => (
              <div className={`research-item status-${patch.status}`} key={patch.id}>
                {(() => {
                  const materialization = materializationReports[patch.id];
                  const impact = impactReports[patch.id];
                  const promotion = promotionReports[patch.id];
                  return (
                    <>
                <div className="research-item-head">
                  <strong>{patch.title}</strong>
                  <div className="research-item-actions">
                    <button
                      type="button"
                      onClick={() => onMaterializePatch?.(patch)}
                      disabled={!onMaterializePatch || materializingPatchId === patch.id}
                      title="Materialize draft pattern"
                    >
                      <FilePlus2 size={14} aria-hidden="true" />
                      <span>{materializingPatchId === patch.id ? "Writing" : "Draft"}</span>
                    </button>
                    <button
                      type="button"
                      onClick={() => onAnalyzePatch?.(patch)}
                      disabled={!materialization || !onAnalyzePatch || analyzingPatchId === patch.id}
                      title="Analyze modeled impact"
                    >
                      <Activity size={14} aria-hidden="true" />
                      <span>{analyzingPatchId === patch.id ? "Testing" : "Test"}</span>
                    </button>
                    <button
                      type="button"
                      onClick={() => onPromotePatch?.(patch)}
                      disabled={!impact?.acceptance?.can_promote || !onPromotePatch || promotingPatchId === patch.id || promotion?.status === "promoted"}
                      title="Promote into active model"
                    >
                      <BadgeCheck size={14} aria-hidden="true" />
                      <span>{promotingPatchId === patch.id ? "Promoting" : "Promote"}</span>
                    </button>
                  </div>
                </div>
                <span>{patch.status.replaceAll("_", " ")} | {patch.target?.change_type?.replaceAll("_", " ")}</span>
                <small>{patch.validation?.warnings?.[0] || patch.target?.artifact}</small>
                {materialization ? (
                  <em className={`materialization-status status-${materialization.status}`}>
                    {materialization.status.replaceAll("_", " ")} | {materialization.materialized_artifact_path}
                  </em>
                ) : null}
                {materialization?.placement_target?.label ? (
                  <small>Will attach to {materialization.placement_target.label}</small>
                ) : null}
                {impact ? (
                  <div className={`impact-status status-${impact.status}`}>
                    <strong>{impact.status.replaceAll("_", " ")}</strong>
                    <span>{impact.acceptance?.improvements?.length || 0} improvements | {impact.acceptance?.regressions?.length || 0} regressions</span>
                    {impact.placement_target?.label ? <small>Target: {impact.placement_target.label}</small> : null}
                    <small>{impact.acceptance?.improvements?.[0] || impact.summary?.[0]}</small>
                    {impact.acceptance?.warnings?.[0] ? <small>{impact.acceptance.warnings[0]}</small> : null}
                  </div>
                ) : null}
                {promotion ? (
                  <em className={`materialization-status status-${promotion.status}`}>
                    {promotion.status.replaceAll("_", " ")} | {promotion.updated_artifacts?.world_manifest || promotion.summary?.[0]}
                  </em>
                ) : null}
                    </>
                  );
                })()}
              </div>
            ))}
          </div>
        </>
      ) : (
        <p>Run a focused loop from the current committed world state. CIaC will write candidates and patch proposals for review.</p>
      )}
    </aside>
  );
}
