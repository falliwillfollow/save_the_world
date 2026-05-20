const DEFAULT_BUNDLE_PATH = "../examples/generated/micro_commons_runtime_bundle.json";
const DEFAULT_FOUNDATION_GATE_PATH = "../examples/generated/micro_commons_foundation_gate.json";
const DEFAULT_SEARCH_OPTIMIZER_PATH = "../examples/generated/micro_commons_search_optimizer_report.json";
const DEFAULT_OBJECTIVE_CALIBRATION_PATH = "../examples/generated/micro_commons_objective_calibration.json";
const DEFAULT_WEIGHT_GOVERNANCE_PATH = "../examples/generated/micro_commons_weight_governance.json";
const DEFAULT_CYCLE_ITERATION_PATH = "../examples/generated/micro_commons_cycle_iteration.json";

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
  searchOptimizer: null,
  objectiveCalibration: null,
  weightGovernance: null,
  cycleReport: null,
  day: 1,
  selectedSystem: "",
  selectedScenarioIndex: 0,
  playing: false,
  playTimer: null,
  cycle: {
    number: 1,
    running: false,
    completed: false,
    reviewOpen: false,
    submitted: false,
    appliedCandidate: "",
    startMs: 0,
    durationMs: 20000,
  },
};

const elements = {
  bundleMeta: document.querySelector("#bundleMeta"),
  loadDefault: document.querySelector("#loadDefault"),
  bundleFile: document.querySelector("#bundleFile"),
  gateFile: document.querySelector("#gateFile"),
  searchFile: document.querySelector("#searchFile"),
  calibrationFile: document.querySelector("#calibrationFile"),
  weightFile: document.querySelector("#weightFile"),
  cycleFile: document.querySelector("#cycleFile"),
  foundationStatus: document.querySelector("#foundationStatus"),
  foundationSummary: document.querySelector("#foundationSummary"),
  optimizationStatus: document.querySelector("#optimizationStatus"),
  optimizationSummary: document.querySelector("#optimizationSummary"),
  cycleStatus: document.querySelector("#cycleStatus"),
  cycleSummary: document.querySelector("#cycleSummary"),
  cycleProgress: document.querySelector("#cycleProgress"),
  runCycle: document.querySelector("#runCycle"),
  reviewChange: document.querySelector("#reviewChange"),
  submitChange: document.querySelector("#submitChange"),
  nextCycle: document.querySelector("#nextCycle"),
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
elements.searchFile.addEventListener("change", event => loadOptimizationFile(event.target.files[0], "search"));
elements.calibrationFile.addEventListener("change", event => loadOptimizationFile(event.target.files[0], "calibration"));
elements.weightFile.addEventListener("change", event => loadOptimizationFile(event.target.files[0], "weight"));
elements.cycleFile.addEventListener("change", event => loadCycleFile(event.target.files[0]));
elements.daySlider.addEventListener("input", event => {
  state.day = Number(event.target.value);
  renderDay();
});
elements.prevDay.addEventListener("click", () => setDay(state.day - 1));
elements.playDays.addEventListener("click", togglePlayback);
elements.nextDay.addEventListener("click", () => setDay(state.day + 1));
elements.runCycle.addEventListener("click", runYearCycle);
elements.reviewChange.addEventListener("click", reviewCycleChange);
elements.submitChange.addEventListener("click", submitCycleChange);
elements.nextCycle.addEventListener("click", runNextCycle);
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
  loadDefaultOptimizationReports();
  loadDefaultCycleIteration();
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

async function loadDefaultOptimizationReports() {
  const paths = [
    [DEFAULT_SEARCH_OPTIMIZER_PATH, "search"],
    [DEFAULT_OBJECTIVE_CALIBRATION_PATH, "calibration"],
    [DEFAULT_WEIGHT_GOVERNANCE_PATH, "weight"],
  ];
  for (const [path, kind] of paths) {
    try {
      const response = await fetch(noStorePath(path), { cache: "no-store" });
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      setOptimizationReport(await response.json(), kind);
    } catch (error) {
      renderOptimizationLoadError(error);
    }
  }
  renderOptimization();
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

function loadOptimizationFile(file, kind) {
  if (!file) return;
  const reader = new FileReader();
  reader.onload = () => {
    try {
      setOptimizationReport(JSON.parse(reader.result), kind);
    } catch (error) {
      elements.optimizationStatus.textContent = "invalid";
      elements.optimizationStatus.className = "status-chip status-fail";
    }
  };
  reader.readAsText(file);
}

async function loadDefaultCycleIteration() {
  try {
    const response = await fetch(noStorePath(DEFAULT_CYCLE_ITERATION_PATH), { cache: "no-store" });
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    setCycleReport(await response.json());
  } catch (error) {
    state.cycleReport = null;
    renderCycle();
  }
}

function loadCycleFile(file) {
  if (!file) return;
  const reader = new FileReader();
  reader.onload = () => {
    try {
      setCycleReport(JSON.parse(reader.result));
    } catch (error) {
      elements.cycleStatus.textContent = "invalid";
      elements.cycleStatus.className = "status-chip status-fail";
    }
  };
  reader.readAsText(file);
}

function setCycleReport(report) {
  state.cycleReport = report;
  renderCycle();
}

function setOptimizationReport(report, kind) {
  if (kind === "search") state.searchOptimizer = report;
  if (kind === "calibration") state.objectiveCalibration = report;
  if (kind === "weight") state.weightGovernance = report;
  renderOptimization();
  renderCycle();
}

function setBundle(bundle) {
  state.bundle = bundle;
  state.day = 1;
  state.selectedSystem = "";
  state.selectedScenarioIndex = 0;
  stopPlayback();
  resetCycleState();
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
  renderOptimization();
  renderCycle();
  renderLayout();
  renderDay();
  renderScenarios();
  renderWarnings();
  renderFailureReasons();
}

function resetCycleState() {
  state.cycle.number = 1;
  state.cycle.running = false;
  state.cycle.completed = false;
  state.cycle.reviewOpen = false;
  state.cycle.submitted = false;
  state.cycle.appliedCandidate = "";
  state.cycle.startMs = 0;
}

function runYearCycle() {
  if (!state.bundle) return;
  stopPlayback();
  const max = state.bundle.timeline?.daily_states?.length || 1;
  const intervalMs = Math.max(20, Math.floor(state.cycle.durationMs / max));
  state.cycle.running = true;
  state.cycle.completed = false;
  state.cycle.reviewOpen = false;
  state.cycle.submitted = false;
  state.cycle.startMs = Date.now();
  setDay(1);
  state.playing = true;
  elements.playDays.textContent = "Pause";
  elements.reviewChange.disabled = true;
  elements.submitChange.disabled = true;
  elements.nextCycle.disabled = true;
  state.playTimer = window.setInterval(() => {
    const elapsedMs = Date.now() - state.cycle.startMs;
    const progress = Math.min(1, elapsedMs / state.cycle.durationMs);
    const day = Math.max(1, Math.ceil(progress * max));
    setDay(day);
    if (progress >= 1 || day >= max) completeCycle();
  }, intervalMs);
  renderCycle();
}

function completeCycle() {
  if (!state.bundle) return;
  const max = state.bundle.timeline?.daily_states?.length || 1;
  state.cycle.running = false;
  state.cycle.completed = true;
  state.cycle.reviewOpen = false;
  state.cycle.submitted = false;
  setDay(max);
  stopPlayback();
  renderCycle();
}

function reviewCycleChange() {
  if (!state.cycle.completed) return;
  state.cycle.reviewOpen = true;
  state.cycle.submitted = false;
  renderCycle();
}

function submitCycleChange() {
  if (!state.cycle.completed) return;
  if (!operatorSubmitAllowed()) return;
  const selected = selectedSearchCandidate();
  state.cycle.reviewOpen = true;
  state.cycle.submitted = true;
  state.cycle.appliedCandidate = selected?.id || "";
  renderCycle();
}

function runNextCycle() {
  if (!state.cycle.submitted) return;
  const nextCycle = state.cycle.number + 1;
  const report = state.cycleReport;
  if (report?.runtime_bundle && report.selected_candidate === state.cycle.appliedCandidate) {
    setBundle(report.runtime_bundle);
    if (report.next_search_optimizer_report) state.searchOptimizer = report.next_search_optimizer_report;
    state.cycle.number = nextCycle;
    renderOptimization();
  } else {
    state.cycle.number = nextCycle;
  }
  runYearCycle();
}

function renderCycle() {
  if (!state.bundle) {
    elements.cycleStatus.textContent = "not loaded";
    elements.cycleStatus.className = "status-chip status-provisional";
    elements.cycleSummary.innerHTML = `<div class="event-row small">Load a runtime bundle to run a simulation cycle.</div>`;
    elements.cycleProgress.style.width = "0%";
    return;
  }
  const max = state.bundle.timeline?.daily_states?.length || 1;
  const progress = state.cycle.completed || state.cycle.submitted ? 100 : Math.round((state.day / max) * 100);
  const status = cycleStatus();
  const statusClass = cycleStatusClass(status);
  const selected = selectedSearchCandidate();
  elements.cycleStatus.textContent = label(status);
  elements.cycleStatus.className = `status-chip status-${statusClass}`;
  elements.cycleProgress.style.width = `${Math.max(0, Math.min(100, progress))}%`;
  elements.reviewChange.disabled = !state.cycle.completed;
  elements.submitChange.disabled = !state.cycle.completed || !state.cycle.reviewOpen || !operatorSubmitAllowed();
  elements.nextCycle.disabled = !state.cycle.submitted;
  elements.runCycle.disabled = state.cycle.running;
  elements.cycleSummary.innerHTML = cycleSummaryMarkup(selected, max);
}

function cycleStatus() {
  if (state.cycle.running) return "running";
  if (state.cycle.submitted) return "change_staged";
  if (state.cycle.reviewOpen) return "reviewing";
  if (state.cycle.completed) return "recommendation_ready";
  return "ready";
}

function cycleSummaryMarkup(selected, max) {
  const cycleLabel = `cycle ${state.cycle.number}`;
  if (state.cycle.running) {
    return `
      <div class="event-row status-border-warn">
        <div class="event-title"><span>${cycleLabel}</span><span>${state.day} / ${max}</span></div>
        <div class="small">Accelerated playback target: one simulated year in about ${Math.round(state.cycle.durationMs / 1000)} seconds.</div>
      </div>
    `;
  }
  if (state.cycle.submitted) {
    const hasAppliedRuntime = state.cycleReport?.runtime_bundle && state.cycleReport.selected_candidate === state.cycle.appliedCandidate;
    const hasNextSearch = Boolean(state.cycleReport?.next_search_optimizer_report);
    return `
      <div class="event-row status-border-pass">
        <div class="event-title"><span>change staged</span><span>${label(state.cycle.appliedCandidate || "candidate")}</span></div>
        <div class="small">${hasAppliedRuntime ? "A generated cycle report is loaded; Next Cycle will switch to its applied runtime bundle." : "The viewer has staged this optimization, but no matching generated cycle report is loaded yet."}</div>
        <div class="small">${hasNextSearch ? "A next search report is available, so the following cycle can recommend from the applied plan." : "No next search report is loaded; recommendations will not compound yet."}</div>
      </div>
      ${cycleAuthoritySummary()}
      ${selected ? cycleChangeReview(selected) : ""}
    `;
  }
  if (state.cycle.reviewOpen) {
    return selected ? `${cycleAcceptanceSummary()}${cycleChangeReview(selected)}` : `
      <div class="event-row small">No optimizer recommendation is loaded for review.</div>
    `;
  }
  if (state.cycle.completed) {
    const hasCycleReport = state.cycleReport?.runtime_bundle && state.cycleReport.selected_candidate === selected?.id;
    const hasNextSearch = Boolean(state.cycleReport?.next_search_optimizer_report);
    const acceptance = state.cycleReport?.operator_acceptance;
    return `
      <div class="event-row status-border-warn">
        <div class="event-title"><span>recommended change</span><span>${label(selected?.id || "none")}</span></div>
        <div class="small">${selected?.selection_rationale || "The cycle completed, but no selected optimizer candidate is loaded."}</div>
      </div>
      <div class="event-row small">${hasCycleReport ? "Generated applied runtime is ready for this candidate." : "Generate or load a matching CycleIterationReport before expecting Next Cycle to change the underlying runtime."}</div>
      <div class="event-row small">${hasNextSearch ? "Next-cycle optimizer search is ready from the applied plan." : "Next-cycle optimizer search is not loaded yet."}</div>
      <div class="event-row small">${acceptance ? `operator acceptance: ${label(acceptance.status)} | submit allowed: ${String(acceptance.simulation_submit_allowed)}` : "Operator acceptance is not loaded yet."}</div>
      <div class="event-row small">Review the particulars before submitting the change into the next cycle.</div>
    `;
  }
  return `
    <div class="event-row">
      <div class="event-title"><span>${cycleLabel}</span><span>${max} days</span></div>
      <div class="small">Run a one-year cycle, inspect one recommended infrastructure change, submit it, then run the next cycle.</div>
    </div>
  `;
}

function cycleChangeReview(candidate) {
  const changed = (candidate.parameter_deltas || []).filter(delta => Number(delta.delta || 0) !== 0);
  return `
    <div class="event-row status-border-warn">
      <div class="event-title">
        <span>${label(candidate.id)}</span>
        <span>${formatNumber(candidate.aggregate_score)}</span>
      </div>
      <div class="small">${candidate.selection_rationale || "Selected by current optimizer report."}</div>
    </div>
    ${optimizationFamilyLevels(candidate)}
    <div class="event-row">
      <div class="event-title"><span>parameter changes</span><span>${changed.length}</span></div>
      ${changed.slice(0, 8).map(delta => `
        <div class="small">${label(delta.pattern_id)} ${label(delta.parameter_id)}: ${formatNumber(delta.from_value)} -> ${formatNumber(delta.to_value)} ${delta.unit}</div>
      `).join("") || `<div class="small">No parameter changes are present in the selected candidate.</div>`}
    </div>
    ${cycleAppliedScenarioRows()}
    ${governanceSummary(state.weightGovernance || {})}
    ${bindingConstraintRows(state.searchOptimizer || {})}
  `;
}

function operatorSubmitAllowed() {
  const selected = selectedSearchCandidate();
  if (!selected) return false;
  const report = state.cycleReport;
  if (!report || report.selected_candidate !== selected.id) return false;
  const acceptance = report.operator_acceptance;
  if (!acceptance) return true;
  return Boolean(acceptance.simulation_submit_allowed);
}

function cycleAcceptanceSummary() {
  const acceptance = state.cycleReport?.operator_acceptance;
  if (!acceptance) return "";
  const statusClass = acceptance.status === "improved" || acceptance.status === "converged" ? "pass" : "fail";
  return `
    <div class="event-row status-border-${statusClass}">
      <div class="event-title">
        <span>operator acceptance</span>
        <span class="status-chip status-${statusClass}">${label(acceptance.status)}</span>
      </div>
      <div class="small">${acceptance.rationale}</div>
      ${(acceptance.objective_regressions || []).slice(0, 5).map(item => `<div class="small">regression: ${item}</div>`).join("")}
      ${(acceptance.objective_improvements || []).slice(0, 5).map(item => `<div class="small">improvement: ${item}</div>`).join("")}
    </div>
  `;
}

function cycleAuthoritySummary() {
  const authority = state.cycleReport?.authority;
  if (!authority) return "";
  return `
    <div class="event-row status-border-warn">
      <div class="event-title">
        <span>${label(authority.mode)}</span>
        <span>${authority.simulation_submit_allowed ? "simulation ok" : "blocked"}</span>
      </div>
      <div class="small">${authority.oversight_policy}</div>
      <div class="small">real-world promotion allowed: ${String(authority.promotion_allowed)}</div>
    </div>
  `;
}

function cycleAppliedScenarioRows() {
  const scenarios = state.cycleReport?.applied_scenarios || [];
  if (!scenarios.length) return "";
  return `
    <div class="event-row">
      <div class="event-title"><span>applied scenario checks</span><span>${scenarios.length}</span></div>
      ${scenarios.slice(0, 4).map(scenario => `
        <div class="small">${label(scenario.scenario)}: ${label(scenario.status)}${scenario.survival_critical_gate_failures?.length ? ` | gates ${scenario.survival_critical_gate_failures.join(", ")}` : ""}</div>
      `).join("")}
    </div>
  `;
}

function renderOptimization() {
  const search = state.searchOptimizer;
  if (!search) {
    elements.optimizationStatus.textContent = "not loaded";
    elements.optimizationStatus.className = "status-chip status-provisional";
    elements.optimizationSummary.innerHTML = `
      <div class="event-row small">Load a SearchOptimizerReport to see the selected infrastructure optimization.</div>
    `;
    return;
  }
  const selected = selectedSearchCandidate();
  const current = currentSearchCandidate();
  const governance = state.weightGovernance;
  const calibration = state.objectiveCalibration;
  const status = governance?.status || search.status || "provisional";
  const statusClass = optimizationStatusClass(status);
  elements.optimizationStatus.textContent = label(status);
  elements.optimizationStatus.className = `status-chip status-${statusClass}`;
  elements.optimizationSummary.innerHTML = `
    <div class="event-row status-border-${statusClass}">
      <div class="event-title">
        <span>${label(search.selected_candidate || "no selection")}</span>
        <span class="status-chip status-${statusClass}">${label(status)}</span>
      </div>
      <div class="small">${selected?.selection_rationale || "No selected candidate available."}</div>
    </div>
    <div class="metric-grid">
      ${metric("searched", search.candidate_count)}
      ${metric("viable", search.viable_candidate_count)}
      ${metric("rejected", search.rejected_candidate_count)}
      ${metric("score", selected?.aggregate_score)}
    </div>
    ${selected ? optimizationFamilyLevels(selected) : ""}
    ${current ? optimizationComparison(selected, current) : ""}
    ${calibration ? calibrationSummary(calibration) : detailRow("calibration", "Objective calibration report not loaded.")}
    ${governance ? governanceSummary(governance) : detailRow("governance", "Weight governance report not loaded.")}
    ${bindingConstraintRows(search)}
  `;
}

function renderOptimizationLoadError(error) {
  if (!state.searchOptimizer) {
    elements.optimizationStatus.textContent = "not loaded";
    elements.optimizationStatus.className = "status-chip status-provisional";
    elements.optimizationSummary.innerHTML = `
      <div class="event-row small">Default optimization report did not load: ${String(error.message || error)}.</div>
      <div class="event-row small">Use the Search, Calib, and Weights controls to load generated optimizer reports.</div>
    `;
  }
}

function selectedSearchCandidate() {
  const search = state.searchOptimizer;
  if (!search) return null;
  return (search.top_candidates || []).find(candidate => candidate.id === search.selected_candidate) || search.top_candidates?.[0] || null;
}

function currentSearchCandidate() {
  const candidates = state.searchOptimizer?.top_candidates || [];
  return candidates.find(candidate => {
    const levels = Object.values(candidate.family_levels || {});
    return levels.length && levels.every(level => level === "current");
  }) || null;
}

function optimizationFamilyLevels(candidate) {
  return `
    <div class="event-row">
      <div class="event-title"><span>Selected family levels</span></div>
      <div class="family-grid">
        ${Object.entries(candidate.family_levels || {}).map(([family, level]) => `
          <div><strong>${label(family)}</strong><span>${label(level)}</span></div>
        `).join("")}
      </div>
    </div>
  `;
}

function optimizationComparison(selected, current) {
  if (!selected || !current) return "";
  const scoreDelta = Number(selected.aggregate_score || 0) - Number(current.aggregate_score || 0);
  const changed = (selected.parameter_deltas || []).filter(delta => Number(delta.delta || 0) !== 0);
  return `
    <div class="event-row">
      <div class="event-title">
        <span>Compared with all-current plan</span>
        <span>${scoreDelta >= 0 ? "+" : ""}${scoreDelta.toFixed(3)}</span>
      </div>
      ${changed.slice(0, 6).map(delta => `
        <div class="small">${label(delta.pattern_id)} ${label(delta.parameter_id)}: ${formatNumber(delta.from_value)} -> ${formatNumber(delta.to_value)} ${delta.unit}</div>
      `).join("") || `<div class="small">No parameter changes from current search levels.</div>`}
    </div>
  `;
}

function calibrationSummary(report) {
  return `
    <div class="event-row">
      <div class="event-title">
        <span>Objective calibration</span>
        <span class="status-chip status-${optimizationStatusClass(report.status)}">${label(report.status)}</span>
      </div>
      <div class="small">${report.uncalibrated_score_count || 0} uncalibrated selected score(s)</div>
      ${(report.calibrated_objectives || []).slice(0, 4).map(item => `
        <div class="small">${label(item.metric)}: ${label(item.formula_id)} | ${label(item.evidence_status)}</div>
      `).join("")}
    </div>
  `;
}

function governanceSummary(report) {
  const summary = report.governance_summary || {};
  return `
    <div class="event-row">
      <div class="event-title">
        <span>Weight governance</span>
        <span class="status-chip status-${optimizationStatusClass(report.status)}">${label(report.status)}</span>
      </div>
      <div class="small">promotion allowed: ${String(report.promotion_allowed)}</div>
      <div class="small">resident consent: ${label(summary.resident_consent_status)} | professional review: ${label(summary.professional_review_status)}</div>
    </div>
  `;
}

function bindingConstraintRows(search) {
  return (search.binding_constraints || []).slice(0, 3).map(constraint => `
    <div class="event-row">
      <div class="event-title">
        <span>${label(constraint.constraint)}</span>
        <span class="status-chip status-${constraint.severity === "hard" ? "fail" : "warn"}">${constraint.candidate_count}</span>
      </div>
      <div class="small">${constraint.description}</div>
    </div>
  `).join("");
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
  if (state.cycle.running) state.cycle.running = false;
  elements.playDays.textContent = "Play";
  renderCycle();
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
  const scenarioFailures = selectedScenarioFailuresForDay(state.day).filter(failure => failure.pattern_id === system.pattern_id);
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
  renderCycle();
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
  const failures = day.active_failures || [];
  const scenarioFailures = selectedScenarioFailuresForDay(day.day);
  const scenarioEvents = day.scenario_events || [];
  const selected = state.selectedSystem;
  const visible = selected ? failures.filter(failure => failure.pattern_id === selected) : failures;
  const visibleScenario = selected ? scenarioFailures.filter(failure => failure.pattern_id === selected) : scenarioFailures;
  if (!visible.length && !visibleScenario.length && !scenarioEvents.length) {
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
  `).join("") + visibleScenario.map(failure => `
    <div class="event-row">
      <div class="event-title">
        <span>scenario replay: ${label(failure.mode)}</span>
        <span class="status-chip status-${failure.severity === "catastrophic" ? "error" : "warning"}">${failure.severity}</span>
      </div>
      <div class="small">${label(failure.pattern_id)} | day ${failure.start_day} to ${scenarioFailureEndDay(failure)}</div>
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
  const scenarioFailures = selectedScenarioFailuresForDay(state.day).filter(failure => failure.pattern_id === system.pattern_id);
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
    ${scenarioFailures.map(failure => detailRow(`scenario replay ${label(failure.mode)}`, `${failure.unresolved_review_dependency || "no review dependency"} | day ${failure.start_day} to ${scenarioFailureEndDay(failure)}`)).join("")}
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

function selectedScenarioFailuresForDay(day) {
  return selectedScenarioFailures().filter(failure => scenarioFailureActiveOnDay(failure, day));
}

function scenarioFailureActiveOnDay(failure, day) {
  const start = Number(failure.start_day || 1);
  const duration = Math.max(1, Number(failure.duration_days || 1));
  const current = Number(day || 1);
  return current >= start && current <= start + duration - 1;
}

function scenarioFailureEndDay(failure) {
  return Number(failure.start_day || 1) + Math.max(1, Number(failure.duration_days || 1)) - 1;
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

function optimizationStatusClass(status) {
  if (["ratified", "calibrated", "ready"].includes(status)) return "pass";
  if (["not_ratified", "missing_calibration", "not_ready", "rejected"].includes(status)) return "fail";
  return "warn";
}

function cycleStatusClass(status) {
  if (status === "change_staged") return "pass";
  if (["recommendation_ready", "reviewing", "running"].includes(status)) return "warn";
  return "provisional";
}
