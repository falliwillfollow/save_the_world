const DEFAULT_BUNDLE_PATH = "../examples/generated/micro_commons_runtime_bundle.json";
const DEFAULT_FOUNDATION_GATE_PATH = "../examples/generated/micro_commons_foundation_gate.json";
const DEFAULT_SEARCH_OPTIMIZER_PATH = "../examples/generated/micro_commons_search_optimizer_report.json";
const DEFAULT_OBJECTIVE_CALIBRATION_PATH = "../examples/generated/micro_commons_objective_calibration.json";
const DEFAULT_WEIGHT_GOVERNANCE_PATH = "../examples/generated/micro_commons_weight_governance.json";
const DEFAULT_CYCLE_ITERATION_PATH = "../examples/generated/micro_commons_cycle_iteration.json";
const DEFAULT_FOOD_AUTONOMY_PATH = "../examples/generated/micro_commons_food_autonomy_report.json";
const DEFAULT_NODE_SCALING_PATH = "../examples/generated/micro_commons_node_scaling.json";
const DEFAULT_TOPOLOGY_RECOMMENDATION_PATH = "../examples/generated/micro_commons_topology_recommendation.json";
const DEFAULT_VIEWER_RUN_REPORT_PATH = "../examples/generated/micro_commons_viewer_session_report.json";
const VIEWER_RUN_REPORT_API = "/api/viewer-session-report";
const VIEWER_RUN_REPORT_STORAGE_KEY = "ciac.viewerRunReport.v0";

const zonePositions = {
  access_lane: { x: 10, y: 48 },
  residential_edge: { x: 31, y: 23 },
  commons_core: { x: 50, y: 43 },
  hygiene_core: { x: 57, y: 27 },
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
  foodAutonomyReport: null,
  foodLaborReport: null,
  complexityReport: null,
  nodeScaling: null,
  topologyRecommendation: null,
  viewerRunReport: null,
  artifactCohesion: null,
  runLogStatus: "not_loaded",
  runLogMessage: "",
  population: 150,
  populationTouched: false,
  day: 1,
  selectedSystem: "",
  selectedScenarioIndex: -1,
  cycle: {
    number: 1,
    running: false,
    paused: false,
    completed: false,
    reviewOpen: false,
    submitted: false,
    appliedCandidate: "",
    startMs: 0,
    elapsedBeforePauseMs: 0,
    durationMs: 20000,
    timer: null,
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
  nodeFile: document.querySelector("#nodeFile"),
  topologyFile: document.querySelector("#topologyFile"),
  nodeScalingStatus: document.querySelector("#nodeScalingStatus"),
  nodeScalingSummary: document.querySelector("#nodeScalingSummary"),
  populationSlider: document.querySelector("#populationSlider"),
  populationOutput: document.querySelector("#populationOutput"),
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
  runtimeKpis: document.querySelector("#runtimeKpis"),
  mapStage: document.querySelector("#mapStage"),
  routeLayer: document.querySelector("#routeLayer"),
  zoneLayer: document.querySelector("#zoneLayer"),
  dayOutput: document.querySelector("#dayOutput"),
  daySlider: document.querySelector("#daySlider"),
  prevDay: document.querySelector("#prevDay"),
  nextDay: document.querySelector("#nextDay"),
  snapshotSummary: document.querySelector("#snapshotSummary"),
  systemDetails: document.querySelector("#systemDetails"),
  failureReasons: document.querySelector("#failureReasons"),
  resourceList: document.querySelector("#resourceList"),
  storageList: document.querySelector("#storageList"),
  maintenanceSummary: document.querySelector("#maintenanceSummary"),
  pursuitSummary: document.querySelector("#pursuitSummary"),
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
elements.nodeFile.addEventListener("change", event => loadNodeScalingFile(event.target.files[0]));
elements.topologyFile.addEventListener("change", event => loadTopologyRecommendationFile(event.target.files[0]));
elements.populationSlider.addEventListener("input", event => {
  state.population = Number(event.target.value || 150);
  state.populationTouched = true;
  renderNodeScaling();
  renderLayout();
});
elements.daySlider.addEventListener("input", event => {
  state.day = Number(event.target.value);
  renderDay();
});
elements.prevDay.addEventListener("click", () => setDay(state.day - 1));
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
  loadDefaultFoodAutonomy();
  loadDefaultNodeScaling();
  loadDefaultTopologyRecommendation();
  loadDefaultViewerRunReport();
}

async function loadDefaultFoodAutonomy() {
  try {
    const response = await fetch(noStorePath(DEFAULT_FOOD_AUTONOMY_PATH), { cache: "no-store" });
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    state.foodAutonomyReport = await response.json();
    renderOptimization();
  } catch (error) {
    state.foodAutonomyReport = null;
  }
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

async function loadDefaultNodeScaling() {
  try {
    const response = await fetch(noStorePath(DEFAULT_NODE_SCALING_PATH), { cache: "no-store" });
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    setNodeScaling(await response.json());
  } catch (error) {
    state.nodeScaling = null;
    renderNodeScalingLoadError(error);
  }
}

async function loadDefaultTopologyRecommendation() {
  try {
    const response = await fetch(noStorePath(DEFAULT_TOPOLOGY_RECOMMENDATION_PATH), { cache: "no-store" });
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    setTopologyRecommendation(await response.json(), { syncPopulation: false });
  } catch (error) {
    state.topologyRecommendation = null;
    renderNodeScaling();
  }
}

async function loadDefaultViewerRunReport() {
  try {
    const response = await fetch(noStorePath(VIEWER_RUN_REPORT_API), { cache: "no-store" });
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    setViewerRunReport(await response.json(), "persisted");
    return;
  } catch (error) {
    try {
      const response = await fetch(noStorePath(DEFAULT_VIEWER_RUN_REPORT_PATH), { cache: "no-store" });
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      setViewerRunReport(await response.json(), "artifact");
      return;
    } catch (artifactError) {
      const cached = window.localStorage.getItem(VIEWER_RUN_REPORT_STORAGE_KEY);
      if (cached) {
        setViewerRunReport(JSON.parse(cached), "local_only");
      } else {
        setViewerRunReport(emptyViewerRunReport(), "not_persisted");
      }
    }
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

function loadNodeScalingFile(file) {
  if (!file) return;
  const reader = new FileReader();
  reader.onload = () => {
    try {
      setNodeScaling(JSON.parse(reader.result));
    } catch (error) {
      elements.nodeScalingStatus.textContent = "invalid";
      elements.nodeScalingStatus.className = "status-chip status-fail";
    }
  };
  reader.readAsText(file);
}

function loadTopologyRecommendationFile(file) {
  if (!file) return;
  const reader = new FileReader();
  reader.onload = () => {
    try {
      setTopologyRecommendation(JSON.parse(reader.result), { syncPopulation: true });
    } catch (error) {
      elements.nodeScalingStatus.textContent = "invalid";
      elements.nodeScalingStatus.className = "status-chip status-fail";
    }
  };
  reader.readAsText(file);
}

function setTopologyRecommendation(report, options = {}) {
  state.topologyRecommendation = report;
  if (options.syncPopulation && report.population) {
    state.population = Number(report.population);
    state.populationTouched = true;
    elements.populationSlider.value = String(state.population);
  }
  renderNodeScaling();
}

function setNodeScaling(report) {
  state.nodeScaling = report;
  const targets = report.target_results || [];
  const maxTarget = Math.max(1500, ...targets.map(target => Number(target.people || 0)));
  elements.populationSlider.max = String(maxTarget);
  if (!state.populationTouched) {
    state.population = defaultPopulationFromTargets(targets, maxTarget);
  } else if (!state.population || state.population > maxTarget) {
    state.population = Math.min(150, maxTarget);
  }
  elements.populationSlider.value = String(state.population);
  renderNodeScaling();
  renderLayout();
}

function setViewerRunReport(report, status) {
  state.viewerRunReport = report;
  state.runLogStatus = status;
  state.runLogMessage = runLogMessage(status);
  renderCycle();
}

function defaultPopulationFromTargets(targets, maxTarget) {
  const adHoc = targets
    .filter(target => String(target.notes || "").toLowerCase().includes("ad hoc"))
    .map(target => Number(target.people || 0))
    .filter(Boolean);
  if (adHoc.length) return adHoc[adHoc.length - 1];
  return Math.min(150, maxTarget);
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
  state.selectedScenarioIndex = -1;
  stopCycleTimer();
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
  renderNodeScaling();
  renderRuntimeKpis();
  renderLayout();
  renderDay();
  renderScenarios();
  renderWarnings();
  renderFailureReasons();
}

function resetCycleState() {
  stopCycleTimer();
  state.cycle.number = 1;
  state.cycle.running = false;
  state.cycle.paused = false;
  state.cycle.completed = false;
  state.cycle.reviewOpen = false;
  state.cycle.submitted = false;
  state.cycle.appliedCandidate = "";
  state.cycle.startMs = 0;
  state.cycle.elapsedBeforePauseMs = 0;
}

function runYearCycle() {
  if (!state.bundle) return;
  if (state.cycle.running) {
    pauseCycle();
    return;
  }
  const max = state.bundle.timeline?.daily_states?.length || 1;
  if (state.cycle.paused && !state.cycle.completed) {
    resumeCycle(max);
    return;
  }
  startCycle(max);
}

function startCycle(max) {
  stopCycleTimer();
  state.cycle.running = true;
  state.cycle.paused = false;
  state.cycle.completed = false;
  state.cycle.reviewOpen = false;
  state.cycle.submitted = false;
  state.cycle.startMs = Date.now();
  state.cycle.elapsedBeforePauseMs = 0;
  setDay(1);
  elements.reviewChange.disabled = true;
  elements.submitChange.disabled = true;
  elements.nextCycle.disabled = true;
  startCycleTimer(max);
  renderCycle();
}

function resumeCycle(max) {
  state.cycle.running = true;
  state.cycle.paused = false;
  state.cycle.startMs = Date.now();
  startCycleTimer(max);
  renderCycle();
}

function pauseCycle() {
  state.cycle.elapsedBeforePauseMs += Date.now() - state.cycle.startMs;
  state.cycle.running = false;
  state.cycle.paused = true;
  stopCycleTimer();
  renderCycle();
}

function startCycleTimer(max) {
  const intervalMs = Math.max(20, Math.floor(state.cycle.durationMs / max));
  state.cycle.timer = window.setInterval(() => {
    const elapsedMs = state.cycle.elapsedBeforePauseMs + Date.now() - state.cycle.startMs;
    const progress = Math.min(1, elapsedMs / state.cycle.durationMs);
    const day = Math.max(1, Math.ceil(progress * max));
    setDay(day);
    if (progress >= 1 || day >= max) completeCycle();
  }, intervalMs);
}

function completeCycle() {
  if (!state.bundle) return;
  const max = state.bundle.timeline?.daily_states?.length || 1;
  stopCycleTimer();
  state.cycle.running = false;
  state.cycle.paused = false;
  state.cycle.completed = true;
  state.cycle.reviewOpen = false;
  state.cycle.submitted = false;
  state.cycle.elapsedBeforePauseMs = 0;
  setDay(max);
  recordCompletedYear(max);
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
  elements.runCycle.disabled = false;
  elements.runCycle.textContent = state.cycle.running ? "Pause" : state.cycle.paused ? "Resume" : "Run Year";
  elements.cycleSummary.innerHTML = `${cycleSummaryMarkup(selected, max)}${viewerRunLogSummary()}`;
}

function recordCompletedYear(max) {
  const event = viewerRunEvent(max);
  appendViewerRunLocal(event, "local_pending");
  persistViewerRunEvent(event);
}

function viewerRunEvent(days) {
  const people = Math.max(1, Number(state.population || elements.populationSlider.value || 150));
  const rows = state.nodeScaling ? scaledNodeRows(state.nodeScaling.node_policy_catalog || [], people) : [];
  const tierCounts = tierNodeCounts(rows);
  const live = liveTopologyRecommendation(rows, people);
  return {
    event_type: "year_cycle_completed",
    completed_at: new Date().toISOString(),
    cycle_number: Number(state.cycle.number || 1),
    population: people,
    days,
    bundle_id: state.bundle?.id || "",
    selected_candidate: selectedSearchCandidate()?.id || "",
    topology_action: live.action.id,
    topology_status: live.status,
    total_nodes: rows.reduce((sum, row) => sum + Number(row.desired_nodes || 0), 0),
    replicated_slots: rows.filter(row => row.mode === "replicated_nodes").length,
    scaled_down_slots: rows.filter(row => row.mode === "seed_or_minimal").length,
    near_capacity_slots: rows.filter(row => row.action === "near_capacity").length,
    tier_node_counts: tierCounts,
  };
}

async function persistViewerRunEvent(event) {
  try {
    const response = await fetch(VIEWER_RUN_REPORT_API, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ event }),
    });
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    const payload = await response.json();
    applyViewerRunPipelineResponse(payload);
    state.runLogStatus = "persisted";
    state.runLogMessage = runLogMessage("persisted", payload);
    window.localStorage.setItem(VIEWER_RUN_REPORT_STORAGE_KEY, JSON.stringify(state.viewerRunReport));
  } catch (error) {
    state.runLogStatus = "local_only";
    state.runLogMessage = `Run recorded in browser only; start ciac viewer-server to write examples/generated/micro_commons_viewer_session_report.json. ${String(error.message || error)}`;
  }
  renderCycle();
}

function applyViewerRunPipelineResponse(payload) {
  const report = payload.viewer_run_report || payload;
  state.viewerRunReport = report;
  if (payload.node_scaling) {
    state.nodeScaling = payload.node_scaling;
    const targets = state.nodeScaling.target_results || [];
    const maxTarget = Math.max(1500, ...targets.map(target => Number(target.people || 0)));
    elements.populationSlider.max = String(maxTarget);
  }
  if (payload.food_labor) state.foodLaborReport = payload.food_labor;
  if (payload.food_autonomy) state.foodAutonomyReport = payload.food_autonomy;
  if (payload.complexity) state.complexityReport = payload.complexity;
  if (payload.topology_recommendation) state.topologyRecommendation = payload.topology_recommendation;
  if (payload.cycle_iteration) state.cycleReport = payload.cycle_iteration;
  if (payload.artifact_cohesion) state.artifactCohesion = payload.artifact_cohesion;
  renderNodeScaling();
  renderLayout();
}

function appendViewerRunLocal(event, status) {
  const report = state.viewerRunReport || emptyViewerRunReport();
  const runs = [...(report.runs || [])];
  const normalized = {
    run_index: runs.length + 1,
    provisional: true,
    ...event,
  };
  runs.push(normalized);
  const updated = {
    ...report,
    status: "runs_recorded",
    active_population: Number(event.population || 0),
    run_count: runs.length,
    runs,
  };
  state.viewerRunReport = updated;
  state.runLogStatus = status;
  state.runLogMessage = runLogMessage(status);
  window.localStorage.setItem(VIEWER_RUN_REPORT_STORAGE_KEY, JSON.stringify(updated));
}

function emptyViewerRunReport() {
  return {
    kind: "ViewerRunReport",
    id: "micro_commons_viewer_session_report",
    generated_by: "ciac.viewer.client.v0",
    provisional: true,
    status: "no_runs",
    active_population: 0,
    run_count: 0,
    runs: [],
    unknowns: [],
  };
}

function viewerRunLogSummary() {
  const report = state.viewerRunReport;
  if (!report) return "";
  const runs = report.runs || [];
  const latest = runs[runs.length - 1];
  const status = state.runLogStatus === "persisted" || state.runLogStatus === "artifact" ? "pass" : state.runLogStatus === "local_pending" ? "warn" : "fail";
  const summary = latest
    ? `${runs.length} completed year run(s); latest population ${latest.population}, ${latest.total_nodes} nodes, ${label(latest.topology_action)}.`
    : "No completed webapp year runs recorded yet.";
  const cohesion = state.artifactCohesion ? `cohesion: ${label(state.artifactCohesion.status)} | active ${state.artifactCohesion.active_population}` : "";
  return `
    <div class="event-row status-border-${status}">
      <div class="event-title"><span>webapp run log</span><span>${label(state.runLogStatus)}</span></div>
      <div class="small">${summary}</div>
      ${cohesion ? `<div class="small">${cohesion}</div>` : ""}
      <div class="small">${state.runLogMessage || runLogMessage(state.runLogStatus)}</div>
    </div>
  `;
}

function runLogMessage(status, payload = null) {
  if (status === "persisted") {
    const pipeline = payload?.pipeline;
    return pipeline ? `Run log persisted; ran the simulator and regenerated food labor, food autonomy, complexity, node-scaling, topology, cycle, and cohesion for ${pipeline.population} people.` : "Run log is being written through the viewer-server API.";
  }
  if (status === "artifact") return "Run log loaded from generated artifacts; new runs need viewer-server for persistence.";
  if (status === "local_pending") return "Run completed; attempting to write the generated viewer run report.";
  if (status === "local_only") return "Run is recorded in browser storage only; it is not visible to Codex as a generated artifact.";
  if (status === "not_persisted") return "No writable viewer run endpoint is active.";
  return "";
}

function cycleStatus() {
  if (state.cycle.running) return "running";
  if (state.cycle.paused) return "paused";
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
  if (state.cycle.paused) {
    return `
      <div class="event-row status-border-warn">
        <div class="event-title"><span>${cycleLabel}</span><span>${state.day} / ${max}</span></div>
        <div class="small">The simulated year is paused. Resume continues from the current day.</div>
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
  const changed = (selected?.parameter_deltas || []).filter(delta => Number(delta.delta || 0) !== 0);
  elements.optimizationSummary.innerHTML = `
    <div class="event-row status-border-${statusClass}">
      <div class="event-title">
        <span>${label(search.selected_candidate || "no selection")}</span>
        <span class="status-chip status-${statusClass}">${label(status)}</span>
      </div>
      <div class="small">${selected?.selection_rationale || "No selected candidate available."}</div>
    </div>
    <div class="metric-grid compact-metrics">
      ${metric("searched", search.candidate_count)}
      ${metric("viable", search.viable_candidate_count)}
      ${metric("score", selected?.aggregate_score)}
      ${metric("changes", changed.length)}
    </div>
    ${current ? optimizationComparison(selected, current) : ""}
    ${calibration ? detailRow("calibration", `${label(calibration.status)} | ${calibration.uncalibrated_score_count || 0} uncalibrated`) : detailRow("calibration", "not loaded")}
    ${governance ? detailRow("governance", `${label(governance.status)} | promotion ${String(governance.promotion_allowed)}`) : detailRow("governance", "not loaded")}
    ${bindingConstraintRows(search)}
    ${foodAutonomySummary()}
  `;
}

function foodAutonomySummary() {
  const report = state.foodAutonomyReport;
  if (!report) return "";
  const food = report.food_autonomy || {};
  const smoothing = report.seasonal_smoothing || {};
  const risk = report.risk_scenario_coverage || {};
  const statusClass = report.status === "pass" ? "pass" : report.status === "fail" ? "fail" : "warn";
  return `
    <div class="event-row status-border-${statusClass}">
      <div class="event-title">
        <span>food autonomy</span>
        <span class="status-chip status-${statusClass}">${label(report.status)}</span>
      </div>
      <div class="small">production ${formatNumber(Number(food.production_ratio || 0) * 100)}% | reserve release ${formatNumber(Number(food.reserve_release_ratio || 0) * 100)}% | drawdown ${formatNumber(food.reserve_drawdown_per_resident_servings)} servings/resident</div>
      <div class="small">seasonal smoothing: ${label(smoothing.status)} | uncovered risk modes: ${(risk.uncovered_risk_modes || []).length}</div>
      ${(report.recommendations || []).slice(0, 2).map(item => `<div class="small">${item}</div>`).join("")}
    </div>
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
  const priorityChecks = checks.filter(check => check.status !== "pass");
  const summary = report.artifact_summary || {};
  elements.foundationSummary.innerHTML = `
    <div class="event-row">
      <div class="event-title">
        <span>${report.ready_for_visual_buildout ? "visual buildout gate" : "hold visual buildout"}</span>
        <span class="status-chip status-${statusClass}">${label(report.status)}</span>
      </div>
      <div class="small">baseline ${summary.baseline_days || 0} days | scenarios ${summary.runtime_scenario_count || 0} | ${priorityChecks.length} warning item(s)</div>
    </div>
    ${priorityChecks.slice(0, 4).map(check => `
      <div class="event-row foundation-check status-border-${check.status}">
        <div class="event-title">
          <span>${label(check.id)}</span>
          <span class="status-chip status-${check.status}">${check.status}</span>
        </div>
        <div class="small">${check.evidence}</div>
      </div>
    `).join("") || `<div class="event-row small">No foundation warnings are active.</div>`}
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

function renderNodeScaling() {
  const report = state.nodeScaling;
  if (!report) {
    elements.nodeScalingStatus.textContent = "not loaded";
    elements.nodeScalingStatus.className = "status-chip status-provisional";
    elements.populationOutput.textContent = `${state.population || 150} people`;
    elements.nodeScalingSummary.innerHTML = `<div class="event-row small">Load an InfrastructureNodeReport to use the population slider.</div>`;
    return;
  }
  const people = Math.max(1, Number(state.population || elements.populationSlider.value || 150));
  elements.populationSlider.value = String(people);
  elements.populationOutput.textContent = `${people} people`;
  const rows = scaledNodeRows(report.node_policy_catalog || [], people);
  const tierCounts = tierNodeCounts(rows);
  const totalNodes = rows.reduce((sum, row) => sum + row.desired_nodes, 0);
  const replicated = rows.filter(row => row.mode === "replicated_nodes").length;
  const scaledDown = rows.filter(row => row.mode === "seed_or_minimal").length;
  const status = scaledDown || replicated ? "ready_with_warnings" : "ready";
  elements.nodeScalingStatus.textContent = label(status);
  elements.nodeScalingStatus.className = `status-chip status-${statusClass(status)}`;
  elements.nodeScalingSummary.innerHTML = `
    <div class="event-row status-border-${statusClass(status)}">
      <div class="event-title"><span>node topology</span><span>${totalNodes} nodes</span></div>
      <div class="small">${replicated} replicated slot(s) | ${scaledDown} seed/minimal slot(s)</div>
    </div>
    <div class="metric-grid compact-metrics">
      ${metric("floor", tierCounts.floor_systems || 0)}
      ${metric("operating", tierCounts.operating_systems || 0)}
      ${metric("capacity", tierCounts.capacity_systems || 0)}
      ${metric("meta", tierCounts.meta_systems || 0)}
    </div>
    ${topologyRecommendationMarkup(rows, people)}
    ${flourishingFrame(report)}
    ${rows
      .filter(row => row.mode !== "village_node" || row.action === "near_capacity")
      .slice(0, 8)
      .map(nodeScalingRow)
      .join("")}
    ${rows.every(row => row.mode === "village_node" && row.action !== "near_capacity") ? `<div class="event-row small">All node pools are inside preferred village-node range.</div>` : ""}
  `;
}

function topologyRecommendationMarkup(rows, people) {
  const live = liveTopologyRecommendation(rows, people);
  const report = state.topologyRecommendation;
  const sourceNote = report && Number(report.population || 0) !== Number(people)
    ? `<div class="small">Loaded recommendation file is for ${report.population} people; live action is recalculated for ${people}.</div>`
    : "";
  return `
    <div class="event-row status-border-${statusClass(live.status)}">
      <div class="event-title"><span>topology action</span><span>${label(live.action.type)}</span></div>
      <div class="small">${label(live.action.id)}: ${live.action.rationale}</div>
      <div class="small">${live.summary}</div>
      ${sourceNote}
    </div>
  `;
}

function liveTopologyRecommendation(rows, people) {
  const scaledDown = rows.filter(row => row.mode === "seed_or_minimal");
  const replicated = rows.filter(row => row.mode === "replicated_nodes");
  const nearCapacity = rows.filter(row => row.action === "near_capacity");
  const candidates = [];
  if (scaledDown.length) {
    candidates.push(topologyAction(
      "scale_down_to_seed_patterns",
      "scale_down",
      people < 50 ? 82 : 45,
      "Use seed/default patterns instead of carrying every village-scale module.",
      scaledDown,
    ));
  }
  if (replicated.length) {
    candidates.push(topologyAction(
      "replicate_village_node_pools",
      "scale_up",
      88,
      "Replicate local dignity-floor and capacity nodes rather than centralizing one oversized system.",
      replicated,
    ));
  }
  if (nearCapacity.length) {
    const floorNear = nearCapacity.filter(row => row.tier === "floor_systems");
    candidates.push(topologyAction(
      "preplan_second_village_cell",
      "prepare_scale_up",
      floorNear.length ? 76 : 62,
      "Population is above preferred node size; prepare split-node topology before adding more residents.",
      floorNear.length ? floorNear : nearCapacity,
    ));
  }
  const maxNodes = Math.max(1, ...rows.map(row => Number(row.desired_nodes || 1)));
  if (people >= 300) {
    candidates.push({
      id: "add_district_capability_layer",
      type: "add_capability_layer",
      priority: 64,
      rationale: "Add district-scale shared services while preserving local dignity-floor nodes.",
    });
  }
  if (people >= 900) {
    candidates.push({
      id: "add_town_city_capability_layer",
      type: "add_capability_layer",
      priority: 66,
      rationale: "Add town/city capability for transit, culture, markets, and utilities coordination.",
    });
  }
  if (maxNodes >= 6) {
    candidates.push({
      id: "federate_cross_node_control_plane",
      type: "federate",
      priority: 70,
      rationale: "Add a thin federation layer for aggregate dashboards, mutual aid, standards, and portability.",
    });
  }
  const action = candidates.sort((a, b) => b.priority - a.priority || a.id.localeCompare(b.id))[0] || {
    id: "monitor_current_topology",
    type: "monitor",
    priority: 20,
    rationale: `Current node topology is inside preferred range for ${people} people.`,
  };
  const status = action.type === "monitor" ? "ready" : "action_recommended";
  return {
    action,
    status,
    summary: `${rows.reduce((sum, row) => sum + Number(row.desired_nodes || 0), 0)} desired nodes | ${replicated.length} replicated slot(s) | ${nearCapacity.length} near-capacity slot(s)`,
  };
}

function topologyAction(id, type, priority, rationale, rows) {
  return {
    id,
    type,
    priority,
    rationale,
    affected_slots: rows.map(row => row.slot),
  };
}

function renderNodeScalingLoadError(error) {
  elements.nodeScalingStatus.textContent = "not loaded";
  elements.nodeScalingStatus.className = "status-chip status-provisional";
  elements.nodeScalingSummary.innerHTML = `
    <div class="event-row small">Default InfrastructureNodeReport did not load: ${String(error.message || error)}.</div>
    <div class="event-row small">Use the Nodes control to open examples/generated/micro_commons_node_scaling.json.</div>
  `;
}

function scaledNodeRows(policies, people) {
  return policies.map(policy => scaledNodeRow(policy, people));
}

function scaledNodeRow(policy, people) {
  const minimum = Number(policy.minimum_population_per_node || 1);
  const preferred = Number(policy.preferred_population_per_node || minimum);
  const maximum = Number(policy.maximum_population_per_node || preferred);
  let desiredNodes = 1;
  let mode = "village_node";
  let action = "steady";
  let activePatterns = policy.accepted_patterns?.length ? policy.accepted_patterns : policy.default_patterns || [];
  let notes = "Within preferred node range.";
  if (people < minimum) {
    mode = "seed_or_minimal";
    action = "scale_down";
    activePatterns = policy.default_patterns || [];
    notes = policy.scale_down_strategy || "Use seed/default patterns.";
  } else if (people > maximum) {
    desiredNodes = Math.ceil(people / maximum);
    mode = "replicated_nodes";
    action = "scale_up";
    notes = policy.scale_up_strategy || "Replicate node pool.";
  } else if (people > preferred) {
    action = "near_capacity";
    notes = "Above preferred population but still inside one maximum-size node.";
  }
  const populationPerNode = people / desiredNodes;
  return {
    ...policy,
    mode,
    action,
    desired_nodes: desiredNodes,
    population_per_node: populationPerNode,
    headroom_per_node: maximum - populationPerNode,
    active_patterns: activePatterns,
    notes,
  };
}

function tierNodeCounts(rows) {
  return rows.reduce((counts, row) => {
    counts[row.tier] = (counts[row.tier] || 0) + row.desired_nodes;
    return counts;
  }, {});
}

function flourishingFrame(report) {
  const model = report.orchestration_model || {};
  if (!model.flourishing_frame && !model.scope_rule) return "";
  return `
    <div class="event-row">
      <div class="event-title"><span>abundance frame</span><span>${label(report.status)}</span></div>
      <div class="small">${model.flourishing_frame || ""}</div>
      <div class="small">${model.scope_rule || ""}</div>
    </div>
  `;
}

function nodeScalingRow(row) {
  const status = row.mode === "replicated_nodes" || row.action === "near_capacity" ? "warn" : "provisional";
  return `
    <div class="event-row status-border-${status}">
      <div class="event-title"><span>${label(row.slot)}</span><span>${row.desired_nodes} node${row.desired_nodes === 1 ? "" : "s"}</span></div>
      <div class="small">${label(row.mode)} | ${formatNumber(row.population_per_node)} people/node | ${label(row.tier)}</div>
      <div class="small">${row.notes}</div>
    </div>
  `;
}

function setDay(day) {
  if (!state.bundle) return;
  const max = state.bundle.timeline.daily_states.length;
  state.day = Math.max(1, Math.min(max, day));
  elements.daySlider.value = String(state.day);
  renderDay();
}

function stopCycleTimer() {
  if (state.cycle.timer) window.clearInterval(state.cycle.timer);
  state.cycle.timer = null;
}

function renderLayout() {
  if (state.nodeScaling) {
    renderTopologyLayout();
    return;
  }
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

function renderTopologyLayout() {
  const report = state.nodeScaling;
  const people = Math.max(1, Number(state.population || elements.populationSlider.value || 150));
  const rows = scaledNodeRows(report.node_policy_catalog || [], people);
  const tierCounts = tierNodeCounts(rows);
  const cellCount = Math.max(1, ...rows.map(row => Number(row.desired_nodes || 1)));
  const replicated = rows.filter(row => row.mode === "replicated_nodes");
  const scaledDown = rows.filter(row => row.mode === "seed_or_minimal");
  const nearCapacity = rows.filter(row => row.action === "near_capacity");
  const status = scaledDown.length || nearCapacity.length || replicated.length ? "ready_with_warnings" : "ready";
  const perCell = {
    floor_systems: Math.round((tierCounts.floor_systems || 0) / cellCount),
    operating_systems: Math.round((tierCounts.operating_systems || 0) / cellCount),
    capacity_systems: Math.round((tierCounts.capacity_systems || 0) / cellCount),
    meta_systems: Math.round((tierCounts.meta_systems || 0) / cellCount),
  };
  elements.layoutStatus.textContent = label(status);
  elements.layoutStatus.className = `status-chip status-${statusClass(status)}`;
  elements.routeLayer.innerHTML = "";
  elements.zoneLayer.innerHTML = `
    <div class="topology-board">
      <div class="topology-summary">
        <div>
          <h3>${people} people</h3>
          <p>${cellCount} local cell${cellCount === 1 ? "" : "s"} | ${(tierCounts.floor_systems || 0) + (tierCounts.operating_systems || 0) + (tierCounts.capacity_systems || 0) + (tierCounts.meta_systems || 0)} infrastructure nodes</p>
        </div>
        <div class="topology-badges">
          <span>${scaledDown.length} scaled down</span>
          <span>${nearCapacity.length} near capacity</span>
          <span>${replicated.length} replicated</span>
        </div>
      </div>
      <div class="topology-grid" style="--cell-count:${Math.min(5, cellCount)}">
        ${Array.from({ length: cellCount }, (_, index) => topologyCell(index, perCell, people, cellCount)).join("")}
      </div>
      <div class="capability-layers">
        ${capabilityLayerRows(people, cellCount).map(capabilityLayer).join("")}
      </div>
      <div class="topology-footer">
        ${report.orchestration_model?.flourishing_frame || "Local dignity floors stay resilient while larger scales add shared capability."}
      </div>
    </div>
  `;
}

function topologyCell(index, perCell, people, cellCount) {
  const residents = Math.round(people / cellCount);
  return `
    <section class="topology-cell">
      <div class="topology-cell-title">
        <h3>${cellCount === 1 ? "Local cell" : `Cell ${index + 1}`}</h3>
        <span>${residents} people</span>
      </div>
      <div class="node-stack">
        ${topologyTier("floor", perCell.floor_systems, "food water shelter energy sanitation")}
        ${topologyTier("operating", perCell.operating_systems, "maintenance governance labor finance")}
        ${topologyTier("capacity", perCell.capacity_systems, "materials mobility skill culture")}
        ${topologyTier("meta", perCell.meta_systems, "risk and graceful degradation")}
      </div>
    </section>
  `;
}

function topologyTier(name, count, detail) {
  return `
    <div class="node-tier node-tier-${name}">
      <span>${label(name)}</span>
      <strong>${count}</strong>
      <small>${detail}</small>
    </div>
  `;
}

function capabilityLayerRows(people, localCells) {
  const layers = [
    {
      id: "district",
      active: people >= 300,
      count: people >= 300 ? Math.max(1, Math.ceil(people / 500)) : 0,
      label: "District capability",
      detail: "shared clinics, logistics, advanced workshops, learning partnerships",
    },
    {
      id: "town_city",
      active: people >= 900,
      count: people >= 900 ? Math.max(1, Math.ceil(people / 1500)) : 0,
      label: "Town / city layer",
      detail: "transit spine, cultural venues, markets, utilities coordination",
    },
    {
      id: "regional",
      active: people >= 1500,
      count: people >= 1500 ? 1 : 0,
      label: "Regional membrane",
      detail: "watershed, hospitals, universities, regional energy and mutual aid",
    },
  ];
  if (people < 300) {
    layers.unshift({
      id: "micro",
      active: true,
      count: localCells,
      label: "Micro scale",
      detail: "seed/default systems before full village overhead",
    });
  }
  return layers;
}

function capabilityLayer(layer) {
  const status = layer.active ? "active" : "inactive";
  return `
    <div class="capability-layer ${status}">
      <div>
        <span>${layer.label}</span>
        <small>${layer.detail}</small>
      </div>
      <strong>${layer.count}</strong>
    </div>
  `;
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
  renderRuntimeKpis(day);
  renderSnapshot(day);
  renderResources(day);
  renderStorage(day);
  renderMaintenance(day);
  renderPursuit(day);
  renderFailures(day);
  renderSystemDetails();
  renderFailureReasons();
  renderCycle();
}

function renderRuntimeKpis(day = null) {
  const bundle = state.bundle;
  if (!bundle) {
    elements.runtimeKpis.innerHTML = "";
    return;
  }
  const currentDay = day || bundle.timeline.daily_states[state.day - 1] || {};
  const labor = bundle.timeline?.labor || {};
  const resources = currentDay.resources || {};
  const status = bundle.manifest?.status?.simulation || bundle.timeline?.simulation_status || "provisional";
  elements.runtimeKpis.innerHTML = [
    kpi("status", label(status), status),
    kpi("day", `${currentDay.day || state.day}/${bundle.timeline?.days || 1}`, "info"),
    kpi("water", resourceKpi(resources.water_liters), resources.water_liters?.status),
    kpi("food", resourceKpi(resources.food_servings), resources.food_servings?.status),
    kpi("energy", resourceKpi(resources.energy_kwh), resources.energy_kwh?.status),
    kpi("labor", `${formatNumber(labor.modeled_involuntary_labor_minutes_per_resident_per_day)} min/day`, labor.status),
  ].join("");
}

function renderSnapshot(day) {
  const maintenance = day.maintenance || {};
  const failures = (day.active_failures || []).length + selectedScenarioFailuresForDay(day.day).length;
  elements.snapshotSummary.innerHTML = [
    metric("maint h", maintenance.required_hours),
    metric("backlog", maintenance.backlog_count),
    metric("failures", failures),
    metric("unmet", (day.unmet_needs || []).length),
  ].join("");
}

function renderResources(day) {
  const priority = ["water_liters", "food_servings", "energy_kwh", "labor_hours"];
  const resources = priority
    .filter(name => day.resources?.[name])
    .map(name => [name, day.resources[name]]);
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

function renderPursuit(day) {
  const labor = state.bundle?.timeline?.labor || {};
  const dailyLabor = day.labor || {};
  const involuntaryMinutes = labor.modeled_involuntary_labor_minutes_per_resident_per_day
    ?? labor.modeled_required_commons_minutes_per_resident_per_day;
  const discretionaryHours = labor.modeled_discretionary_commons_capacity_hours_per_resident_per_day
    ?? labor.modeled_personal_pursuit_hours_per_resident_per_day;
  const discretionaryWeekly = labor.modeled_discretionary_commons_capacity_hours_per_resident_per_week
    ?? labor.modeled_personal_pursuit_hours_per_resident_per_week;
  elements.pursuitSummary.innerHTML = [
    metric("required min/day", involuntaryMinutes),
    metric("capacity h/day", discretionaryHours),
    metric("capacity h/week", discretionaryWeekly),
    metric("today h/person", dailyLabor.hours_per_resident),
    `<div class="metric metric-wide"><div class="small">Mandatory upkeep only. Food preparation, sleep, education, and voluntary work stay outside this model.</div></div>`,
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
  elements.scenarioSelect.innerHTML = [
    `<option value="-1">Baseline | normal year</option>`,
    ...scenarios.map((scenario, index) => (
      `<option value="${index}">${label(scenario.scenario)} | ${scenario.status}</option>`
    )),
  ].join("");
  elements.scenarioSelect.value = String(state.selectedScenarioIndex);
  renderScenario();
}

function renderScenario() {
  const scenarios = state.bundle?.scenarios || [];
  const selectedIndex = Number(elements.scenarioSelect.value ?? -1);
  const scenario = selectedIndex >= 0 ? scenarios[selectedIndex] : null;
  if (!scenario) {
    const status = state.bundle?.timeline?.simulation_status || state.bundle?.manifest?.status?.simulation || "provisional";
    elements.scenarioSummary.innerHTML = `
      <div class="event-row status-border-${statusClass(status)}">
        <div class="event-title">
          <span>baseline normal year</span>
          <span class="status-chip status-${statusClass(status)}">${label(status)}</span>
        </div>
        <div class="small">Scenario overlays are off. Map colors show baseline system warnings only.</div>
      </div>
    `;
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

function kpi(name, value, status = "provisional") {
  return `
    <div class="kpi status-border-${statusClass(status)}">
      <span>${label(name)}</span>
      <strong>${value}</strong>
    </div>
  `;
}

function resourceKpi(resource) {
  if (!resource) return "n/a";
  if (Number(resource.unmet_demand || 0) > 0) return `${formatNumber(resource.unmet_demand)} unmet`;
  return formatNumber(resource.ending_balance);
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
  if (["recommendation_ready", "reviewing", "running", "paused"].includes(status)) return "warn";
  return "provisional";
}

function statusClass(status) {
  if (["pass", "ready", "ratified"].includes(status)) return "pass";
  if (["warn", "warning", "ready_with_warnings", "running", "paused", "reviewing", "recommendation_ready", "action_recommended"].includes(status)) return "warn";
  if (["fail", "error", "failure", "not_ratified", "blocked"].includes(status)) return "fail";
  return "provisional";
}
