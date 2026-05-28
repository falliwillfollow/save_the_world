import { useMemo, useState } from "react";
import AutomationSubstratePanel from "./AutomationSubstratePanel.jsx";
import BaselineComparisonPanel from "./BaselineComparisonPanel.jsx";
import HumanSovereigntyPanel from "./HumanSovereigntyPanel.jsx";
import LifeReturnedCard from "./LifeReturnedCard.jsx";
import ResidentStoryCard from "./ResidentStoryCard.jsx";
import TimeBudgetWheel from "./TimeBudgetWheel.jsx";

export default function AbundanceMode({ lifeManifest, automationManifest, onHighlightObjects }) {
  const archetypes = lifeManifest?.resident_archetypes || [];
  const [selectedId, setSelectedId] = useState(archetypes[0]?.id || "");
  const selectedArchetype = useMemo(
    () => archetypes.find(archetype => archetype.id === selectedId) || archetypes[0],
    [archetypes, selectedId]
  );

  if (!lifeManifest || !automationManifest) {
    return (
      <aside className="abundance-panel">
        <section className="abundance-section">
          <h2>Abundance Mode</h2>
          <p>Life and automation manifests are not loaded.</p>
        </section>
      </aside>
    );
  }

  return (
    <aside className="abundance-panel" aria-label="Abundance mode">
      <LifeReturnedCard lifeManifest={lifeManifest} />
      <ResidentStoryCard archetypes={archetypes} selectedId={selectedArchetype?.id} onSelect={setSelectedId} />
      <BaselineComparisonPanel selectedArchetype={selectedArchetype} />
      <TimeBudgetWheel baseline={selectedArchetype?.baseline_life} civic={selectedArchetype?.civic_floor_life} />
      <AutomationSubstratePanel automationManifest={automationManifest} onHighlightObjects={onHighlightObjects} />
      <HumanSovereigntyPanel automationManifest={automationManifest} lifeManifest={lifeManifest} />
    </aside>
  );
}
