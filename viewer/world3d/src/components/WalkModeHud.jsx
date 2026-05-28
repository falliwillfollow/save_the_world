import { Eye, MousePointer2 } from "lucide-react";

export default function WalkModeHud({ target }) {
  return (
    <div className="walk-hud" aria-live="polite">
      <div className="walk-reticle" aria-hidden="true" />
      <div className="walk-instructions">
        <strong><MousePointer2 size={15} aria-hidden="true" /> Walk Mode</strong>
        <span>Click the world to capture mouse. WASD moves, Shift moves faster, Esc releases.</span>
      </div>
      <div className={`walk-target ${target ? "has-target" : ""}`}>
        <Eye size={15} aria-hidden="true" />
        <span>{target ? `E - inspect ${target.label || target.id}` : "Look at a structure or node"}</span>
      </div>
    </div>
  );
}
