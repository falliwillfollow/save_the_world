import { Check } from "lucide-react";

export default function PopulationCommitControl({ draftPopulation, committedPopulation, scale, onDraftChange, onCommit }) {
  const dirty = Number(draftPopulation) !== Number(committedPopulation);
  return (
    <div className="population-commit">
      <label>
        <span>Population</span>
        <div className="population-input-row">
          <input
            type="number"
            min="12"
            max="1500"
            step="1"
            value={draftPopulation}
            onChange={event => onDraftChange(Number(event.target.value))}
            aria-label="Population"
          />
          <button type="button" onClick={onCommit} disabled={!dirty} title="Commit population" aria-label="Commit population">
            <Check size={15} aria-hidden="true" />
            <span>Commit</span>
          </button>
        </div>
      </label>
      <input
        type="range"
        min="12"
        max="1500"
        step="1"
        value={draftPopulation}
        onChange={event => onDraftChange(Number(event.target.value))}
        aria-label="Population slider"
      />
      <p>
        {scale.implied_village_blocks} block{scale.implied_village_blocks === 1 ? "" : "s"}
        {" | "}
        {scale.topology_counts?.residential_pods || 1} pods
        {" | "}
        {scale.topology_counts?.common_houses || 1} commons
        {" | "}
        {scale.scale_class.replaceAll("_", " ")}
      </p>
    </div>
  );
}
