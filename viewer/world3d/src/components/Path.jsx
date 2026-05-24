import { Line } from "@react-three/drei";
import { vecToArray } from "../world/layout.js";

export default function Path({ path, mode, selectedScenario, selected, onSelect }) {
  const affected = mode === "stress" && selectedScenario?.timeline?.some(step => (step.affected_objects || []).includes(path.id));
  const color = affected ? "#b3261e" : selected ? "#17212f" : path.type === "service" ? "#667b8a" : "#7a8f55";
  const points = (path.points || []).map(point => {
    const [x, y, z] = vecToArray(point);
    return [x, y + 0.12, z];
  });
  return (
    <Line
      points={points}
      color={color}
      lineWidth={selected ? 4 : 1.35}
      transparent
      opacity={affected || selected ? 0.95 : 0.28}
      onClick={event => { event.stopPropagation(); onSelect(path); }}
    />
  );
}
