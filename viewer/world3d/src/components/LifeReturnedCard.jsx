export default function LifeReturnedCard({ lifeManifest }) {
  const metrics = lifeManifest?.metrics || {};
  const returned = Number(metrics.life_returned_hours_per_week || 0);
  const wageReduction = Number(metrics.required_wage_hours_reduction_percent || 0);
  const commonsLabor = Number(metrics.commons_labor_hours_per_resident_per_week || 0);
  const externalWage = Number(metrics.civic_floor_external_wage_hours_per_week || 0);

  return (
    <section className="abundance-section life-returned-card">
      <div>
        <span className={`status-pill status-${metrics.capability_gate_status || "unknown"}`}>
          {metrics.capability_gate_status || "unknown"}
        </span>
        <h2>Life Returned</h2>
      </div>
      <strong>{returned.toFixed(1)} h/wk</strong>
      <p>{lifeManifest?.life_returned?.summary || "No life-returned summary is available."}</p>
      <p className="assumption-note">This is a provisional abundance hypothesis. Civic-floor residents are not modeled as having required jobs, rent payments, commutes, or routine errands.</p>
      <dl>
        <div>
          <dt>External wage burden</dt>
          <dd>{externalWage.toFixed(1)} h/wk</dd>
        </div>
        <div>
          <dt>Scarcity wage removed</dt>
          <dd>{wageReduction.toFixed(1)}%</dd>
        </div>
        <div>
          <dt>Visible commons labor</dt>
          <dd>{commonsLabor.toFixed(2)} h/wk</dd>
        </div>
        <div>
          <dt>Hidden labor</dt>
          <dd>{metrics.hidden_labor_status || "unknown"}</dd>
        </div>
      </dl>
    </section>
  );
}
