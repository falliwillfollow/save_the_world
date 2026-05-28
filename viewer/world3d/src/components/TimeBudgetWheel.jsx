const ORDER = [
  ["wage_hours", "Required job"],
  ["commons_labor", "Civic ops"],
  ["commute_hours", "Required commute"],
  ["errands_admin", "Manual errands"],
  ["domestic_survival", "Domestic"],
  ["required_care", "Care"],
  ["recovery", "Recovery"],
  ["passion_time", "Passion"],
];

export default function TimeBudgetWheel({ baseline, civic }) {
  const baselineHours = baseline?.weekly_hours || {};
  const civicHours = civic?.weekly_hours || {};
  const max = Math.max(
    1,
    ...ORDER.map(([key]) => Number(baselineHours[key] || 0)),
    ...ORDER.map(([key]) => Number(civicHours[key] || 0))
  );

  return (
    <section className="abundance-section time-budget">
      <h2>Weekly Time Budget</h2>
      <p className="assumption-note">Brown bars are the outside scarcity reference. Blue bars are the civic-floor hypothesis where required jobs, rent, commutes, and routine errands are absent.</p>
      <div className="time-budget-grid">
        {ORDER.map(([key, label]) => (
          <div className="time-budget-row" key={key}>
            <span>{label}</span>
            <i style={{ "--budget-width": `${(Number(baselineHours[key] || 0) / max) * 100}%` }} />
            <b style={{ "--budget-width": `${(Number(civicHours[key] || 0) / max) * 100}%` }} />
            <small>{Number(baselineHours[key] || 0).toFixed(1)} / {Number(civicHours[key] || 0).toFixed(1)}</small>
          </div>
        ))}
      </div>
    </section>
  );
}
