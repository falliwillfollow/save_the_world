import { LockKeyhole } from "lucide-react";

export default function HumanSovereigntyPanel({ automationManifest, lifeManifest }) {
  const blocked = automationManifest?.blocked_automation_domains || [];
  const boundaries = automationManifest?.human_sovereignty_boundaries || [];
  const blockers = lifeManifest?.promotion_blockers || [];

  return (
    <section className="abundance-section sovereignty-panel">
      <h2>Human Sovereignty</h2>
      <div className="sovereignty-list">
        {blocked.map(domain => (
          <span key={domain}><LockKeyhole size={12} aria-hidden="true" /> {domain.replaceAll("_", " ")}</span>
        ))}
      </div>
      <h3>Boundaries</h3>
      <ul>
        {boundaries.slice(0, 4).map(boundary => (
          <li key={boundary.id}>{boundary.rule}</li>
        ))}
      </ul>
      <h3>Promotion Blockers</h3>
      {blockers.length ? (
        <ul>
          {blockers.map(blocker => (
            <li key={blocker.id}>{blocker.domain}: {blocker.message}</li>
          ))}
        </ul>
      ) : (
        <p>No promotion blockers are reported by the current capability policy gate.</p>
      )}
    </section>
  );
}
