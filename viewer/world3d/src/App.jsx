import { useEffect, useMemo, useRef, useState } from "react";
import InfoCard from "./components/InfoCard.jsx";
import Legend from "./components/Legend.jsx";
import ModeSwitcher from "./components/ModeSwitcher.jsx";
import OverlayPanel from "./components/OverlayPanel.jsx";
import PopulationCommitControl from "./components/PopulationCommitControl.jsx";
import ResearchLoopPanel from "./components/ResearchLoopPanel.jsx";
import ResourceDashboard from "./components/ResourceDashboard.jsx";
import TimelineScrubber from "./components/TimelineScrubber.jsx";
import WorldScene from "./world/WorldScene.jsx";
import { evidenceCardFor, loadDefaultWorldManifest } from "./world/WorldManifestLoader.js";
import { inferScale, scaleWorldManifest } from "./world/scaleManifest.js";

const PROVISIONALITY = "This is a provisional civic simulation. It visualizes model assumptions and stress tests. It does not certify real-world safety, legality, affordability, engineering, public health, accessibility, resident consent, or buildability.";

export default function App() {
  const [baseManifest, setBaseManifest] = useState(null);
  const [manifest, setManifest] = useState(null);
  const [mode, setMode] = useState("life");
  const [selectedObject, setSelectedObject] = useState(null);
  const [selectedSystem, setSelectedSystem] = useState("food");
  const [highlightedObjectIds, setHighlightedObjectIds] = useState([]);
  const [selectedScenarioId, setSelectedScenarioId] = useState("scenario_normal_day");
  const [draftPopulation, setDraftPopulation] = useState(80);
  const [committedPopulation, setCommittedPopulation] = useState(80);
  const [demoClock, setDemoClock] = useState({ timePercent: 0, elapsedDays: 0 });
  const [demoPlaying, setDemoPlaying] = useState(false);
  const [reducedMotion, setReducedMotion] = useState(false);
  const [researchFocus, setResearchFocus] = useState("care_health");
  const [researchResponses, setResearchResponses] = useState({});
  const [researchLoading, setResearchLoading] = useState(false);
  const [researchError, setResearchError] = useState("");
  const [materializingPatchId, setMaterializingPatchId] = useState("");
  const [analyzingPatchId, setAnalyzingPatchId] = useState("");
  const [promotingPatchId, setPromotingPatchId] = useState("");
  const [materializationReports, setMaterializationReports] = useState({});
  const [impactReports, setImpactReports] = useState({});
  const [promotionReports, setPromotionReports] = useState({});
  const demoFrameTimeRef = useRef(null);
  const { timePercent, elapsedDays } = demoClock;

  useEffect(() => {
    loadDefaultWorldManifest().then(world => {
      const population = Number(world.population?.residents || 80);
      setBaseManifest(world);
      setManifest(scaleWorldManifest(world, population));
      setDraftPopulation(population);
      setCommittedPopulation(population);
      setSelectedScenarioId(world.scenario_states?.[0]?.id || "scenario_normal_day");
    });
  }, []);

  useEffect(() => {
    if (!demoPlaying) {
      demoFrameTimeRef.current = null;
      return undefined;
    }
    let frameId = 0;
    const tick = now => {
      if (demoFrameTimeRef.current === null) {
        demoFrameTimeRef.current = now;
      }
      const elapsedMs = Math.min(250, now - demoFrameTimeRef.current);
      demoFrameTimeRef.current = now;
      setDemoClock(current => {
        const next = current.timePercent + (elapsedMs / 1000) * 16;
        const completedDays = Math.floor(next / 100);
        return {
          timePercent: next % 100,
          elapsedDays: current.elapsedDays + completedDays,
        };
      });
      frameId = window.requestAnimationFrame(tick);
    };
    frameId = window.requestAnimationFrame(tick);
    return () => window.cancelAnimationFrame(frameId);
  }, [demoPlaying]);

  const selectedScenario = useMemo(
    () => manifest?.scenario_states?.find(scenario => scenario.id === selectedScenarioId) || manifest?.scenario_states?.[0],
    [manifest, selectedScenarioId]
  );
  const evidenceCard = useMemo(() => evidenceCardFor(manifest || {}, selectedObject), [manifest, selectedObject]);
  const draftScale = useMemo(() => inferScale(draftPopulation), [draftPopulation]);
  const activeResearchResponse = researchResponses[researchFocus] || null;

  function commitPopulation() {
    if (!baseManifest) return;
    const nextPopulation = Math.max(12, Math.min(1500, Math.round(Number(draftPopulation || committedPopulation))));
    setCommittedPopulation(nextPopulation);
    setDraftPopulation(nextPopulation);
    setManifest(scaleWorldManifest(baseManifest, nextPopulation));
    setSelectedObject(null);
    setHighlightedObjectIds([]);
    setDemoPlaying(false);
    demoFrameTimeRef.current = null;
    setDemoClock({ timePercent: 0, elapsedDays: 0 });
    setResearchResponses({});
    setResearchError("");
    setMaterializationReports({});
    setImpactReports({});
    setPromotionReports({});
    setMaterializingPatchId("");
    setAnalyzingPatchId("");
    setPromotingPatchId("");
  }

  async function runResearchLoop() {
    if (!manifest || researchLoading) return;
    const requestedFocus = researchFocus;
    setResearchLoading(true);
    setResearchError("");
    try {
      const response = await fetch("/api/research-loop", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          focus: requestedFocus,
          world_manifest: manifest,
          runtime_bundle_path: "examples/generated/micro_commons_runtime_bundle.json",
        }),
      });
      if (!response.ok) {
        throw new Error(await response.text());
      }
      const result = await response.json();
      const resultFocus = result?.research_loop?.source?.focus || requestedFocus;
      setResearchResponses(current => ({ ...current, [resultFocus]: result }));
      setMode("insight");
    } catch (error) {
      setResearchError(
        `Research loop unavailable. Start the Python viewer server on port 8765, then retry. ${String(error.message || error)}`
      );
    } finally {
      setResearchLoading(false);
    }
  }

  async function materializePatch(patch) {
    if (!patch || materializingPatchId) return;
    setMaterializingPatchId(patch.id);
    setResearchError("");
    try {
      const response = await fetch("/api/materialize-patch", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ patch_proposal: patch }),
      });
      if (!response.ok) {
        throw new Error(await response.text());
      }
      const result = await response.json();
      setMaterializationReports(current => ({
        ...current,
        [patch.id]: result.materialization,
      }));
      setImpactReports(current => {
        const next = { ...current };
        delete next[patch.id];
        return next;
      });
      setPromotionReports(current => {
        const next = { ...current };
        delete next[patch.id];
        return next;
      });
    } catch (error) {
      setResearchError(`Patch materialization unavailable. ${String(error.message || error)}`);
    } finally {
      setMaterializingPatchId("");
    }
  }

  async function analyzePatch(patch) {
    const materialization = materializationReports[patch?.id];
    if (!patch || !materialization || analyzingPatchId) return;
    setAnalyzingPatchId(patch.id);
    setResearchError("");
    try {
      const response = await fetch("/api/analyze-materialized-patch", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ materialization }),
      });
      if (!response.ok) {
        throw new Error(await response.text());
      }
      const result = await response.json();
      setImpactReports(current => ({
        ...current,
        [patch.id]: result.impact,
      }));
    } catch (error) {
      setResearchError(`Patch impact analysis unavailable. ${String(error.message || error)}`);
    } finally {
      setAnalyzingPatchId("");
    }
  }

  async function promotePatch(patch) {
    const materialization = materializationReports[patch?.id];
    const impact = impactReports[patch?.id];
    if (!patch || !materialization || !impact?.acceptance?.can_promote || promotingPatchId) return;
    setPromotingPatchId(patch.id);
    setResearchError("");
    try {
      const response = await fetch("/api/promote-materialized-patch", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ materialization }),
      });
      if (!response.ok) {
        throw new Error(await response.text());
      }
      const result = await response.json();
      setPromotionReports(current => ({
        ...current,
        [patch.id]: result.promotion,
      }));
      if (result.world_manifest) {
        setBaseManifest(result.world_manifest);
        setManifest(scaleWorldManifest(result.world_manifest, committedPopulation));
      }
    } catch (error) {
      setResearchError(`Patch promotion unavailable. ${String(error.message || error)}`);
    } finally {
      setPromotingPatchId("");
    }
  }

  if (!manifest) {
    return <main className="app-shell loading">Loading civic floor world...</main>;
  }

  return (
    <main className={`app-shell mode-${mode}`}>
      <WorldScene
        manifest={manifest}
        mode={mode}
        selectedObject={selectedObject}
        selectedSystem={selectedSystem}
        selectedScenario={selectedScenario}
        highlightedObjectIds={highlightedObjectIds}
        timePercent={timePercent}
        reducedMotion={reducedMotion}
        onSelectObject={setSelectedObject}
      />

      <header className="world-header">
        <div>
          <h1>Civic Floor World</h1>
          <p>{manifest.population.residents} residents | {manifest.scale.scale_class.replaceAll("_", " ")}</p>
        </div>
        <ModeSwitcher mode={mode} onChange={setMode} />
        <PopulationCommitControl
          draftPopulation={draftPopulation}
          committedPopulation={committedPopulation}
          scale={draftScale}
          onDraftChange={setDraftPopulation}
          onCommit={commitPopulation}
        />
        <div className="scenario-box">
          <label>
            <span>Scenario</span>
            <select value={selectedScenarioId} onChange={event => { setSelectedScenarioId(event.target.value); setMode("stress"); }}>
              {manifest.scenario_states.map(scenario => (
                <option value={scenario.id} key={scenario.id}>{scenario.label}</option>
              ))}
            </select>
          </label>
        </div>
      </header>

      <div className="provisional-banner">{PROVISIONALITY}</div>
      <ResourceDashboard telemetry={manifest.resource_telemetry} timePercent={timePercent} elapsedDays={elapsedDays} />
      <Legend activeSystem={selectedSystem} onSelectSystem={system => { setSelectedSystem(system); setMode("systems"); }} />
      <OverlayPanel
        manifest={manifest}
        mode={mode}
        timePercent={timePercent}
        selectedSystem={selectedSystem}
        selectedScenarioId={selectedScenarioId}
        onSystemChange={setSelectedSystem}
        onScenarioChange={value => { setSelectedScenarioId(value); setMode("stress"); }}
        onSelectObject={setSelectedObject}
        onHighlightObjects={setHighlightedObjectIds}
      />
      {mode === "insight" ? (
        <ResearchLoopPanel
          focus={researchFocus}
          onFocusChange={setResearchFocus}
          response={activeResearchResponse}
          loading={researchLoading}
          error={researchError}
          onRun={runResearchLoop}
          onMaterializePatch={materializePatch}
          onAnalyzePatch={analyzePatch}
          onPromotePatch={promotePatch}
          materializingPatchId={materializingPatchId}
          analyzingPatchId={analyzingPatchId}
          promotingPatchId={promotingPatchId}
          materializationReports={materializationReports}
          impactReports={impactReports}
          promotionReports={promotionReports}
        />
      ) : null}
      <InfoCard object={selectedObject} evidenceCard={evidenceCard} manifest={manifest} mode={mode} scenario={selectedScenario} />
      <TimelineScrubber
        value={timePercent}
        onChange={value => setDemoClock(current => ({ ...current, timePercent: value }))}
        demoPlaying={demoPlaying}
        onDemoPlayingChange={setDemoPlaying}
        elapsedDays={elapsedDays}
        onResetDemo={() => {
          setDemoPlaying(false);
          demoFrameTimeRef.current = null;
          setDemoClock({ timePercent: 0, elapsedDays: 0 });
        }}
        reducedMotion={reducedMotion}
        onReducedMotionChange={setReducedMotion}
      />
    </main>
  );
}
