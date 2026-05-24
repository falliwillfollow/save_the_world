export function percentToHour(value) {
  const percent = Number(value || 0);
  return Math.floor((Math.max(0, Math.min(100, percent)) / 100) * 24) % 24;
}

export function displayClock(value) {
  if (Number(value || 0) >= 100) {
    return "24:00";
  }
  return `${String(percentToHour(value)).padStart(2, "0")}:00`;
}
