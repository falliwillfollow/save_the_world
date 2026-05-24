import { COLOR_TOKENS } from "../world/AssetRegistry.js";
import { label } from "../world/layout.js";

const KEYS = ["housing", "food", "water", "energy", "sanitation", "maintenance", "care", "governance", "risk", "mobility"];

export default function Legend({ activeSystem, onSelectSystem }) {
  return (
    <aside className="legend-panel">
      <h2>Overlays</h2>
      <div className="legend-list">
        {KEYS.map(key => (
          <button
            key={key}
            type="button"
            className={activeSystem === key ? "is-active" : ""}
            onClick={() => onSelectSystem(key)}
            title={`Show ${label(key)} overlay`}
          >
            <i style={{ background: COLOR_TOKENS[key] || "#777" }} />
            <span>{label(key)}</span>
          </button>
        ))}
      </div>
    </aside>
  );
}
