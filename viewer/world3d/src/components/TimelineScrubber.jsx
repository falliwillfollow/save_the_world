import { Pause, Play, RotateCcw } from "lucide-react";
import { displayClock } from "../world/time.js";

export default function TimelineScrubber({
  value,
  onChange,
  demoPlaying,
  onDemoPlayingChange,
  elapsedDays,
  onResetDemo,
  reducedMotion,
  onReducedMotionChange,
}) {
  return (
    <div className="timeline-strip">
      <div>
        <strong>{displayClock(value)}</strong>
        <span>full day</span>
      </div>
      <div className="demo-controls">
        <button
          type="button"
          className={demoPlaying ? "is-active" : ""}
          onClick={() => onDemoPlayingChange(!demoPlaying)}
          title={demoPlaying ? "Pause demo" : "Play demo"}
          aria-label={demoPlaying ? "Pause demo" : "Play demo"}
        >
          {demoPlaying ? <Pause size={16} aria-hidden="true" /> : <Play size={16} aria-hidden="true" />}
          <span>{demoPlaying ? "Pause" : "Demo"}</span>
        </button>
        <button type="button" onClick={onResetDemo} title="Reset demo" aria-label="Reset demo">
          <RotateCcw size={15} aria-hidden="true" />
        </button>
        <div className="day-counter">
          <strong>{elapsedDays}</strong>
          <span>{elapsedDays === 1 ? "day" : "days"}</span>
        </div>
      </div>
      <input
        type="range"
        min="0"
        max="100"
        value={value}
        onInput={event => onChange(Number(event.target.value))}
        onChange={event => onChange(Number(event.target.value))}
        aria-label="Daily timeline"
      />
      <label className="motion-toggle">
        <input
          type="checkbox"
          checked={reducedMotion}
          onChange={event => onReducedMotionChange(event.target.checked)}
        />
        <span>Reduced motion</span>
      </label>
    </div>
  );
}
