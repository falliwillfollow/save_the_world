import { percentToHour } from "../world/time.js";

export function visibleLifeEvents(manifest, timePercent) {
  const hour = percentToHour(timePercent);
  return (manifest.daily_events || []).filter(event => {
    const eventHour = Number(String(event.time || "00:00").slice(0, 2));
    return Math.abs(eventHour - hour) <= 2;
  });
}

export function lifeModeSummary(manifest, timePercent) {
  const events = visibleLifeEvents(manifest, timePercent);
  return {
    title: "Life Mode",
    summary: `${events.length} archetypal routines visible around the civic floor.`,
    events,
  };
}
