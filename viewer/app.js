const DEFAULT_BUNDLE_PATH = "../examples/generated/micro_commons_runtime_bundle.json";
const DEFAULT_FOUNDATION_GATE_PATH = "../examples/generated/micro_commons_foundation_gate.json";

const zonePositions = {
  access_lane: { x: 10, y: 48 },
  residential_edge: { x: 31, y: 23 },
  commons_core: { x: 50, y: 43 },
  water_yard: { x: 73, y: 37 },
  sanitation_service: { x: 86, y: 66 },
  energy_workshop_yard: { x: 27, y: 72 },
  food_garden: { x: 68, y: 74 },
};

const state = {
  bundle: null,
  foundationGate: null,
  day: 1,
  selectedSystem: "",
  selectedScenarioIndex: 0,
  playing: false,
  playTimer: null,
};

const elements = {
  bundleMeta: document.querySelector("#bundleMeta"),
  loadDefault: document.querySelector("#loadDefault"),
  bundleFile: document.querySelector("#bundleFile"),
  gateFile: document.querySelector("#gateFile"),
  foundationStatus: document.querySelector("#foundationStatus"),
  foundationSummary: document.querySelector("#foundationSummary"),
  layoutStatus: document.querySelector("#layoutStatus"),
  mapStage: document.querySelector("#mapStage"),
  routeLayer: document.querySelector("#routeLayer"),
  zoneLayer: document.querySelector("#zoneLayer"),
  dayOutput: document.querySelector("#dayOutput"),
  daySlider: document.querySelector("#daySlider"),
  prevDay: document.querySelector("#prevDay"),
  playDays: document.querySelector("#playDays"),
  nextDay: document.querySelector("#nextDay"),
  systemDetails: document.querySelector("#systemDetails"),
  failureReasons: document.querySelector("#failureReasons"),
  resourceList: document.querySelector("#resourceList"),
  storageList: document.querySelector("#storageList"),
  maintenanceSummary: document.querySelector("#maintenanceSummary"),
  failureList: document.querySelector("#failureList"),
  scenarioSelect: document.querySelector("#scenarioSelect"),
  scenarioSummary: document.querySelector("#scenarioSummary"),
  warningList: document.querySelector("#warningList"),
};

elements.loadDefault.addEventListener("click", () => loadDefaultBundle());
elements.bundleFile.addEventListener("change", event => loadFile(event.target.files[0]));
elements.gateFile.addEventListener("change", event => loadGateFile(event.target.files[0]));
elements.daySlider.addEventListener("input", event => {
  state.day = Number(event.target.value);
  renderDay();
});
elements.prevDay.addEventListener("click", () => setDay(state.day - 1));
elements.playDays.addEventListener("click", togglePlayback);
elements.nextDay.addEventListener("click", () => setDay(state.day + 1));
elements.scenarioSelect.addEventListener("change", event => {
  state.selectedScenarioIndex = Number(event.target.value || 0);
  renderLayout();
  renderScenario();
  renderSystemDetails();
});

loadDefaultBundle();

async function loadDefaultBundle() {
  try {
    const bundleResponse = await fetch(noStorePath(DEFAULT_BUNDLE_PATH), { cache: "no-store" });
    if (!bundleResponse.ok) throw new Error(`HTTP ${bundleResponse.status}`);
    setBundle(await bundleResponse.json());
  } catch (error) {
    elements.bundleMeta.textContent = `Open a RuntimeBundle JSON file`;
  }
  loadDefaultFoundationGate();
}

async function loadDefaultFoundationGate() {
  try {
    const gateResponse = await fetch(noStorePath(DEFAULT_FOUNDATION_GATE_PATH), { cache: "no-store" });
    if (!gateResponse.ok) throw new Error(`HTTP ${gateResponse.status}`);
    setFoundationGate(await gateResponse.json());
  } catch (error) {
    renderFoundationLoadError(error);
  }
}

function loadFile(file) {
  if (!file) return;
  const reader = new FileReader();
  reader.onload = () => {
    try {
      setBundle(JSON.parse(reader.result));
    } catch (error) {
      elements.bundleMeta.textContent = "Invalid JSON";
    }
  };
  reader.readAsText(file);
}

function loadGateFile(file) {
  if (!file) return;
  const reader = new FileReader();
  reader.onload = () => {
    try {
      setFoundationGate(JSON.parse(reader.result));
    } catch (error) {
      elements.foundationStatus.textContent = "invalid";
      elements.foundationStatus.className = "status-chip status-fail";
    }
  };
  reader.readAsText(file);
}

function setBundle(bundle) {
  state.bundle = bundle;
  state.day = 1;
  state.selectedSystem = "";
  state.selectedScenarioIndex = 0;
  stopPlayback();
  const days = bundle.timeline?.days || bundle.timeline?.daily_states?.length || 1;
  elements.daySlider.max = String(days);
  elements.daySlider.value = "1";
  elements.bundleMeta.textContent = `${bundle.id} | ${bundle.manifest.status.simulation}`;
  elements.layoutStatus.textContent = bundle.site.provisional ? "provisional" : "ready";
  renderAll();
}

function setFoundationGate(report) {
  state.foundationGate = report;
  renderFoundation();
}

function renderAll() {
  renderFoundation();
  renderLayout();
  renderDay();
  renderScenarios();
  renderWarnings();
  renderFailureReasons();
}

function renderFoundation() {
  const report = state.foundationGate;
  if (!report) {
    elements.foundationStatus.textContent = "not loaded";
    elements.foundationStatus.className = "status-chip status-provisional";
    elements.foundationSummary.innerHTML = `
      <div class="event-row small">Load a FoundationGateReport to see visual-buildout readiness.</div>
    `;
    return;
  }
  const statusClass = foundationStatusClass(report.status);
  elements.foundationStatus.textContent = label(report.status);
  elements.foundationStatus.className = `status-chip status-${statusClass}`;
  const checks = report.checks || [];
  const summary = report.artifact_summary || {};
  elements.foundationSummary.innerHTML = `
    <div class="event-row">
      <div class="event-title">
        <span>${report.ready_for_visual_buildout ? "visual buildout gate" : "hold visual buildout"}</span>
        <span class="status-chip status-${statusClass}">${label(report.status)}</span>
      </div>
      <div class="small">baseline ${summary.baseline_days || 0} days | matrix ${label(summary.replay_matrix_status)} | scenarios ${summary.runtime_scenario_count || 0}</div>
    </div>
    ${checks.map(check => `
      <div class="event-row foundation-check status-border-${check.status}">
        <div class="event-title">
          <span>${label(check.id)}</span>
          <span class="status-chip status-${check.status}">${check.status}</span>
        </div>
        <div class="small">${check.evidence}</div>
      </div>
    `).join("")}
    <div class="event-row small">This gate is not safety, permit, public-health, engineering, or consent approval.</div>
  `;
}

function renderFoundationLoadError(error) {
  elements.foundationStatus.textContent = "not loaded";
  elements.foundationStatus.className = "status-chip status-provisional";
  elements.foundationSummary.innerHTML = `
    <div class="event-row small">Default FoundationGateReport did not load: ${String(error.message || error)}.</div>
    <div class="event-row small">Use the Gate control to open examples/generated/micro_commons_foundation_gate.json.</div>
  `;
}

function setDay(day) {
  if (!state.bundle) return;
  const max = state.bundle.timeline.daily_states.length;
  state.day = Math.max(1, Math.min(max, day));
  elements.daySlider.value = String(state.day);
  renderDay();
}

function togglePlayback() {
  if (state.playing) {
    stopPlayback();
    return;
  }
  state.playing = true;
  elements.playDays.textContent = "Pause";
  state.playTimer = window.setInterval(() => {
    const max = state.bundle?.timeline?.daily_states?.length || 1;
    setDay(state.day >= max ? 1 : state.day + 1);
  }, 450);
}

function stopPlayback() {
  if (state.playTimer) window.clearInterval(state.playTimer);
  state.playTimer = null;
  state.playing = false;
  elements.playDays.textContent = "Play";
}

function renderLayout() {
  const bundle = state.bundle;
  if (!bundle) return;
  const layoutGraph = bundle.site.layout_graph || {};
  const zones = bundle.site.zones || layoutGraph.zones || [];
  const systemsByZone = groupBy(bundle.systems || [], system => system.zone_id || "unknown");

  elements.zoneLayer.innerHTML = zones.map(zone => {
    const pos = zonePositions[zone.id] || { x: 50, y: 50 };
    const systems = systemsByZone.get(zone.id) || [];
    const zoneState = zoneClass(zone, systems);
    return `
      <section class="zone ${zoneState}" style="left:${pos.x}%;top:${pos.y}%">
        <h3>${label(zone.id)}</h3>
        ${systems.map(system => systemButton(system)).join("")}
      </section>
    `;
  }).join("");

  elements.zoneLayer.querySelectorAll(".system-chip").forEach(button => {
    button.addEventListener("click", () => {
      state.selectedSystem = button.dataset.patternId;
      renderLayout();
      renderDay();
    });
  });

  renderRoutes(zones);
}

function systemButton(system) {
  const status = effectiveSystemStatus(system);
  const selected = state.selectedSystem === system.pattern_id ? " is-selected" : "";
  const warning = systemWarnings(system.pattern_id).length ? " has-warning" : "";
  return `
    <button class="system-chip status-${status}${selected}${warning}" data-pattern-id="${system.pattern_id}" type="button">
      ${label(system.pattern_id)}
    </button>
  `;
}

function effectiveSystemStatus(system) {
  const scenarioFailures = selectedScenarioFailures().filter(failure => failure.pattern_id === system.pattern_id);
  if (scenarioFailures.some(failure => failure.severity === "catastrophic")) return "failure";
  if (scenarioFailures.length) return "risk";
  if (systemWarnings(system.pattern_id).length) return "warn";
  return system.viewer_status || "provisional";
}

function zoneClass(zone, systems) {
  if (systems.some(system => effectiveSystemStatus(system) === "failure")) return "zone-failure";
  if (systems.some(system => ["risk", "warn"].includes(effectiveSystemStatus(system)))) return "zone-warn";
  if ((zone.hazards || []).length) return "zone-hazard";
  return "";
}

function renderRoutes(zones) {
  const bundle = state.bundle;
  const routeLayer = elements.routeLayer;
  const zoneIds = new Set(zones.map(zone => zone.id));
  const routes = (bundle.site.routes || []).filter(route => zoneIds.has(route.from_zone) && zoneIds.has(route.to_zone));
  routeLayer.innerHTML = routes.map(route => {
    const from = zonePositions[route.from_zone];
    const to = zonePositions[route.to_zone];
    if (!from || !to) return "";
    return `<line class="route-line" x1="${from.x}%" y1="${from.y}%" x2="${to.x}%" y2="${to.y}%"></line>`;
  }).join("");
}

function renderDay() {
  const bundle = state.bundle;
  if (!bundle) return;
  const day = bundle.timeline.daily_states[state.day - 1];
  if (!day) return;

  elements.dayOutput.textContent = `${day.day} / ${bundle.timeline.days}`;
  renderResources(day);
  renderStorage(day);
  renderMaintenance(day);
  renderFailures(day);
  renderSystemDetails();
  renderFailureReasons();
}

function renderResources(day) {
  const resources = Object.entries(day.resources || {});
  elements.resourceList.innerHTML = resources.map(([name, summary]) => {
    const magnitude = Math.min(100, Math.abs(Number(summary.net || 0)));
    return `
      <div class="resource-row status-${summary.status}">
        <div class="resource-title">
          <span>${label(name)}</span>
          <span class="status-chip status-${summary.status}">${summary.status}</span>
        </div>
        <div class="meter"><span style="width:${Math.max(4, magnitude)}%"></span></div>
        <div class="small">net ${formatNumber(summary.net)} | balance ${formatNumber(summary.ending_balance)} | unmet ${formatNumber(summary.unmet_demand)}</div>
      </div>
    `;
  }).join("");
}

function renderStorage(day) {
  const storage = Object.entries(day.storage || {});
  const recoveryTasks = day.storage_recovery_tasks || [];
  if (!storage.length) {
    elements.storageList.innerHTML = `<div class="event-row small">No explicit storage modeled for this day.</div>`;
    return;
  }
  elements.storageList.innerHTML = storage.map(([name, summary]) => {
    const capacity = Number(summary.capacity || 0);
    const ending = Number(summary.ending_total || 0);
    const percent = capacity ? Math.max(4, Math.min(100, (ending / capacity) * 100)) : 4;
    return `
      <div class="resource-row status-${summary.status}">
        <div class="resource-title">
          <span>${label(name)}</span>
          <span class="status-chip status-${summary.status}">${summary.status}</span>
        </div>
        <div class="meter"><span style="width:${percent}%"></span></div>
        <div class="small">stored ${formatNumber(summary.ending_total)} / ${formatNumber(summary.capacity)} | floor ${formatNumber(summary.reserve_floor)} | quality ${summary.quality_status || "pass"}</div>
      </div>
    `;
  }).join("") + recoveryTasks.map(task => `
    <div class="event-row">
      <div class="event-title"><span>${label(task.resource)} recovery</span><span>${label(task.status)}</span></div>
      <div class="small">${formatNumber(task.remaining_hours)} h left | ${task.action} | ${task.review_dependency}: ${task.review_state?.status || "unknown"}</div>
    </div>
  `).join("");
}

function renderMaintenance(day) {
  const maintenance = day.maintenance || {};
  elements.maintenanceSummary.innerHTML = [
    metric("required", maintenance.required_hours),
    metric("deferred", maintenance.deferred_count),
    metric("backlog", maintenance.backlog_count),
    metric("status", maintenance.status),
  ].join("");
}

function renderFailures(day) {
  const failures = [...(day.active_failures || []), ...selectedScenarioFailures()];
  const scenarioEvents = day.scenario_events || [];
  const selected = state.selectedSystem;
  const visible = selected ? failures.filter(failure => failure.pattern_id === selected) : failures;
  if (!visible.length && !scenarioEvents.length) {
    elements.failureList.innerHTML = `<div class="event-row small">No active runtime failures on this day.</div>`;
    return;
  }
  elements.failureList.innerHTML = scenarioEvents.map(event => `
    <div class="event-row">
      <div class="event-title">
        <span>${label(event.type)}: ${label(event.id)}</span>
        <span class="status-chip status-warning">${event.status || "active"}</span>
      </div>
      <div class="small">${event.description}</div>
    </div>
  `).join("") + visible.map(failure => `
    <div class="event-row">
      <div class="event-title">
        <span>${label(failure.mode)}</span>
        <span class="status-chip status-${failure.severity === "catastrophic" ? "error" : "warning"}">${failure.severity}</span>
      </div>
      <div class="small">${label(failure.pattern_id)}</div>
    </div>
  `).join("");
}

function renderSystemDetails() {
  const system = selectedSystem();
  if (!system) {
    elements.systemDetails.innerHTML = `<div class="event-row small">Select a system on the map.</div>`;
    return;
  }
  const warnings = systemWarnings(system.pattern_id);
  const scenarioFailures = selectedScenarioFailures().filter(failure => failure.pattern_id === system.pattern_id);
  elements.systemDetails.innerHTML = `
    <div class="event-row">
      <div class="event-title">
        <span>${label(system.pattern_id)}</span>
        <span class="status-chip status-${effectiveSystemStatus(system)}">${effectiveSystemStatus(system)}</span>
      </div>
      <div class="small">zone ${label(system.zone_id)} | footprint ${formatNumber(system.footprint_m2)} m2</div>
    </div>
    ${detailRow("critical", (system.critical_resources || []).join(", ") || "none")}
    ${detailRow("hazards", (system.hazard_flags || []).join(", ") || "none")}
    ${detailRow("access", (system.access_needs || []).join(", ") || "none")}
    ${scenarioFailures.map(failure => detailRow(`failure ${label(failure.mode)}`, failure.unresolved_review_dependency)).join("")}
    ${warnings.slice(0, 4).map(warning => detailRow("warning", warning)).join("")}
  `;
}

function renderScenarios() {
  const scenarios = state.bundle?.scenarios || [];
  elements.scenarioSelect.innerHTML = scenarios.map((scenario, index) => (
    `<option value="${index}">${label(scenario.scenario)} | ${scenario.status}</option>`
  )).join("");
  renderScenario();
}

function renderScenario() {
  const scenarios = state.bundle?.scenarios || [];
  const scenario = scenarios[Number(elements.scenarioSelect.value || 0)];
  if (!scenario) {
    elements.scenarioSummary.innerHTML = `<div class="event-row small">No scenario runs bundled.</div>`;
    return;
  }
  const failures = scenario.runtime_failures || [];
  const reviewEvents = scenario.review_context?.events || [];
  elements.scenarioSummary.innerHTML = `
    <div class="event-row">
      <div class="event-title">
        <span>${label(scenario.scenario)}</span>
        <span class="status-chip status-${scenario.status}">${scenario.status}</span>
      </div>
      <div class="small">${scenario.days} days | ${scenario.affected_resources.join(", ")}</div>
    </div>
    ${failures.slice(0, 5).map(failure => `
      <div class="event-row">
        <div class="event-title"><span>${label(failure.mode)}</span><span>${label(failure.pattern_id)}</span></div>
        <div class="small">${failure.unresolved_review_dependency}</div>
      </div>
    `).join("")}
    ${reviewEvents.slice(0, 4).map(event => `
      <div class="event-row">
        <div class="event-title"><span>${label(event.domain)}</span><span>${label(event.effect)}</span></div>
        <div class="small">${label(event.status)} | ${event.notes}</div>
      </div>
    `).join("")}
  `;
}

function renderFailureReasons() {
  const bundle = state.bundle;
  if (!bundle) return;
  const reasons = [];
  for (const [resource, summary] of Object.entries(bundle.timeline.resource_balance || {})) {
    if (summary.status !== "pass") {
      reasons.push(`${label(resource)} ${summary.status}: net ${formatNumber(summary.net_per_day)} per day`);
    }
  }
  reasons.push(...(bundle.manifest?.warnings || []).slice(0, 8));
  const scenario = selectedScenario();
  if (scenario) {
    reasons.push(...(scenario.survival_critical_gate_failures || []).map(gate => `${label(scenario.scenario)} gate: ${label(gate)}`));
  }
  elements.failureReasons.innerHTML = reasons.slice(0, 10).map(reason => `
    <div class="event-row small">${reason}</div>
  `).join("");
}

function renderWarnings() {
  const warnings = state.bundle?.manifest?.warnings || [];
  const gateWarnings = (state.foundationGate?.checks || [])
    .filter(check => check.status !== "pass")
    .map(check => `${label(check.id)}: ${check.remediation}`);
  elements.warningList.innerHTML = [...gateWarnings, ...warnings].slice(0, 14).map(warning => `
    <div class="event-row small">${warning}</div>
  `).join("");
}

function metric(name, value) {
  return `
    <div class="metric">
      <div class="event-title"><span>${label(name)}</span><span>${formatNumber(value)}</span></div>
    </div>
  `;
}

function detailRow(name, value) {
  return `
    <div class="event-row">
      <div class="event-title"><span>${label(name)}</span></div>
      <div class="small">${value}</div>
    </div>
  `;
}

function selectedSystem() {
  if (!state.bundle || !state.selectedSystem) return null;
  return (state.bundle.systems || []).find(system => system.pattern_id === state.selectedSystem) || null;
}

function selectedScenario() {
  return (state.bundle?.scenarios || [])[state.selectedScenarioIndex] || null;
}

function selectedScenarioFailures() {
  return selectedScenario()?.runtime_failures || [];
}

function systemWarnings(patternId) {
  const warnings = state.bundle?.manifest?.warnings || [];
  const tokens = [patternId, label(patternId)];
  return warnings.filter(warning => tokens.some(token => warning.includes(token)));
}

function groupBy(items, keyFn) {
  const groups = new Map();
  for (const item of items) {
    const key = keyFn(item);
    if (!groups.has(key)) groups.set(key, []);
    groups.get(key).push(item);
  }
  return groups;
}

function label(value) {
  return String(value || "").replaceAll("_", " ");
}

function formatNumber(value) {
  if (typeof value === "string") return value;
  const number = Number(value || 0);
  return Number.isInteger(number) ? String(number) : number.toFixed(2);
}

function noStorePath(path) {
  const delimiter = path.includes("?") ? "&" : "?";
  return `${path}${delimiter}v=${Date.now()}`;
}

function foundationStatusClass(status) {
  if (status === "ready") return "pass";
  if (status === "ready_with_warnings") return "warn";
  return "fail";
}
