import { Activity, Route, SearchCheck, Users } from "lucide-react";

const MODES = [
  { id: "life", label: "Life", Icon: Users },
  { id: "systems", label: "Systems", Icon: Route },
  { id: "stress", label: "Stress", Icon: Activity },
  { id: "insight", label: "Insight", Icon: SearchCheck },
];

export default function ModeSwitcher({ mode, onChange }) {
  return (
    <div className="mode-switcher" role="tablist" aria-label="World mode">
      {MODES.map(({ id, label, Icon }) => (
        <button
          key={id}
          type="button"
          className={mode === id ? "is-active" : ""}
          onClick={() => onChange(id)}
          role="tab"
          aria-selected={mode === id}
          title={`${label} mode`}
        >
          <Icon size={16} aria-hidden="true" />
          <span>{label}</span>
        </button>
      ))}
    </div>
  );
}
