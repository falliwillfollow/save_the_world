const RESOURCE_ORDER = ["water", "food", "energy"];

export default function ResourceDashboard({ telemetry, timePercent, elapsedDays }) {
  const resources = RESOURCE_ORDER
    .map(id => (telemetry?.resources || []).find(resource => resource.id === id))
    .filter(Boolean);
  const labor = telemetry?.labor || {};
  const horizonDays = Number(telemetry?.horizon_days || 365);

  return (
    <aside className="resource-dashboard" aria-label="Resource telemetry">
      {resources.map(resource => {
        const live = liveResource(resource, timePercent, elapsedDays, horizonDays);
        return (
          <article className="resource-card" key={resource.id}>
            <div className="resource-card-head">
              <h2>{resource.label}</h2>
              <span className={`status-pill status-${live.status}`}>{live.status}</span>
            </div>
            <div className="resource-value">
              <strong>{formatAmount(live.current)}</strong>
              <span>/ {formatAmount(resource.capacity)} {resource.unit}</span>
            </div>
            <div className="meter" aria-hidden="true">
              <i className="meter-reserve" style={{ width: percent(resource.reserve_floor_ratio) }} />
              <i className="meter-minimum" style={{ width: percent(resource.minimum_ratio) }} />
              <i className="meter-current" style={{ width: percent(live.currentRatio) }} />
            </div>
            <dl>
              <dt>Net/day</dt>
              <dd>{signed(resource.net_per_day)}</dd>
              <dt>Today</dt>
              <dd>{signed(live.todayDelta)}</dd>
              <dt>Refill/release</dt>
              <dd>{formatAmount(live.dailyRefill)} / {formatAmount(live.dailyRelease)}</dd>
            </dl>
          </article>
        );
      })}
      <article className="resource-card labor-card">
        <div className="resource-card-head">
          <h2 title="Modeled civic operations labor, not total resident work or life burden.">Commons labor</h2>
          <span className={`status-pill status-${labor.status}`}>{labor.status || "provisional"}</span>
        </div>
        <div className="resource-value">
          <strong>{formatAmount(labor.required_minutes_per_resident_per_day)}</strong>
          <span>min/resident/day</span>
        </div>
        <div className="meter" aria-hidden="true">
          <i className="meter-current" style={{ width: percent(labor.utilization) }} />
        </div>
        <dl>
          <dt>Use</dt>
          <dd>{Math.round(Number(labor.utilization || 0) * 100)}%</dd>
          <dt>Maint/wk</dt>
          <dd>{formatAmount(labor.maintenance_hours_per_week)} h</dd>
          <dt>Care/wk</dt>
          <dd>{formatAmount(labor.care_hours_per_week)} h</dd>
        </dl>
        <p className="resource-note">Visible civic operations only.</p>
      </article>
    </aside>
  );
}

function liveResource(resource, timePercent, elapsedDays, horizonDays) {
  const capacity = Number(resource.capacity || 0);
  const floor = Number(resource.reserve_floor || 0);
  const current = Number(resource.current || 0);
  const netPerDay = Number(resource.net_per_day || 0);
  const reportedDailyRelease = Number(resource.total_released || 0) / Math.max(1, horizonDays);
  const reportedDailyRefill = Number(resource.total_refilled || 0) / Math.max(1, horizonDays);
  const operatingSwing = netPerDay >= 0 ? Math.abs(netPerDay) * 0.25 : 0;
  const dailyRelease = Math.max(reportedDailyRelease, operatingSwing);
  const dailyRefill = netPerDay >= 0 ? Math.max(reportedDailyRefill, dailyRelease) : reportedDailyRefill;
  const demandProgress = smoothProgress(timePercent, 18, 88);
  const refillProgress = smoothProgress(timePercent, 34, 82);
  const dayDrift = Number(elapsedDays || 0) * netPerDay;
  const todayDelta = dailyRefill * refillProgress - dailyRelease * demandProgress;
  const liveCurrent = clamp(current + dayDrift + todayDelta, floor, capacity || current);
  return {
    current: liveCurrent,
    currentRatio: capacity ? liveCurrent / capacity : 0,
    todayDelta,
    dailyRelease,
    dailyRefill,
    status: liveCurrent <= floor ? "warning" : resource.status,
  };
}

function smoothProgress(value, startPercent, endPercent) {
  const percentValue = Number(value || 0);
  if (percentValue <= startPercent) return 0;
  if (percentValue >= endPercent) return 1;
  const t = (percentValue - startPercent) / (endPercent - startPercent);
  return t * t * (3 - 2 * t);
}

function clamp(value, min, max) {
  return Math.max(min, Math.min(max, value));
}

function percent(value) {
  return `${Math.round(Math.max(0, Math.min(1, Number(value || 0))) * 100)}%`;
}

function signed(value) {
  const raw = Number(value || 0);
  const numeric = Math.abs(raw) < 0.05 ? 0 : raw;
  return `${numeric > 0 ? "+" : ""}${formatAmount(numeric)}`;
}

function formatAmount(value) {
  const numeric = Number(value || 0);
  if (Math.abs(numeric) >= 1000) {
    return new Intl.NumberFormat("en-US", { maximumFractionDigits: 0 }).format(numeric);
  }
  return new Intl.NumberFormat("en-US", { maximumFractionDigits: 1 }).format(numeric);
}
