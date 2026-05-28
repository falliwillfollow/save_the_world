import { Bot, ShieldCheck } from "lucide-react";

export default function AutomationSubstratePanel({ automationManifest, onHighlightObjects }) {
  const tasks = automationManifest?.tasks || [];
  const visibleTargets = ["node_water_reserve", "structure_food_commons", "structure_maintenance_shop", "structure_care_room", "node_sanitation_waste"];

  return (
    <section className="abundance-section automation-substrate">
      <div className="abundance-section-head">
        <h2>Automation Substrate</h2>
        <button type="button" onClick={() => onHighlightObjects?.(visibleTargets)} title="Highlight visible automation support targets">
          <Bot size={15} aria-hidden="true" />
          <span>Highlight</span>
        </button>
      </div>
      <p>{automationManifest?.automation_thesis?.tagline}</p>
      <div className="automation-task-list">
        {tasks.map(task => (
          <article key={task.id} className="automation-task">
            <strong>{task.id.replaceAll("_", " ")}</strong>
            <span>{task.domain} | {task.actor} | {task.trigger}</span>
            <small><ShieldCheck size={13} aria-hidden="true" /> {task.review_gate || "review"} | {task.privacy_level}</small>
          </article>
        ))}
      </div>
    </section>
  );
}
