export default function BaselineComparisonPanel({ selectedArchetype }) {
  const returned = selectedArchetype?.life_returned || {};
  const civicLife = selectedArchetype?.civic_floor_life || {};
  const allocation = civicLife.reclaimed_time_allocation || {};
  const baseline = Number(returned.compulsory_burden_baseline_hours || 0);
  const civic = Number(returned.compulsory_burden_civic_hours || 0);
  const max = Math.max(1, baseline, civic);

  return (
    <section className="abundance-section baseline-comparison">
      <h2>Scarcity Burden Delta</h2>
      <div className="comparison-bars">
        <div>
          <span>Scarcity reference</span>
          <i style={{ "--comparison-width": `${(baseline / max) * 100}%` }} />
          <strong>{baseline.toFixed(1)} h/wk</strong>
        </div>
        <div>
          <span>Civic floor</span>
          <b style={{ "--comparison-width": `${(civic / max) * 100}%` }} />
          <strong>{civic.toFixed(1)} h/wk</strong>
        </div>
      </div>
      <p>{Number(returned.hours_per_week || 0).toFixed(1)} hours per week are modeled as removed from scarcity burden for this archetype.</p>
      <p className="assumption-note">
        The scarcity reference is outside the model world. Civic-floor residents have no required external job, no rent payment pressure, no required commute, and no routine consumer errands.
      </p>
      {allocation.hours_per_week ? (
        <p className="assumption-note">
          Reclaimed time is allocated back into life: {(Number(allocation.recovery_share || 0) * 100).toFixed(0)}% recovery and {(Number(allocation.passion_share || 0) * 100).toFixed(0)}% passion/self-directed work.
        </p>
      ) : null}
      {civicLife.automation_handled_burdens?.length ? (
        <div className="assumption-chip-list">
          {civicLife.automation_handled_burdens.map(item => <span key={item}>{item}</span>)}
        </div>
      ) : null}
    </section>
  );
}
