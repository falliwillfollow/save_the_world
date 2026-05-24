import { Html } from "@react-three/drei";
import { assetFor } from "../world/AssetRegistry.js";
import { objectStatusForMode, sizeToArray, statusColor, vecToArray } from "../world/layout.js";

export default function Structure({ structure, mode, selectedScenario, selectedSystem, selected, labelCutoff, onSelect }) {
  const asset = assetFor(structure);
  const size = sizeToArray(structure.size, asset.defaultSize);
  const position = vecToArray(structure.position);
  const status = objectStatusForMode(structure, mode, selectedScenario);
  const systemActive = selectedSystem && (structure.systems || []).includes(selectedSystem);
  const showLabel = shouldShowLabel(structure, selected, systemActive, labelCutoff);
  const color = statusColor(status, asset.color);
  const height = size[1];
  return (
    <group
      position={[position[0], height / 2, position[2]]}
      onClick={event => { event.stopPropagation(); onSelect(structure); }}
    >
      <mesh castShadow receiveShadow>
        <boxGeometry args={size} />
        <meshStandardMaterial color={color} roughness={0.72} metalness={0.02} emissive={systemActive || selected ? color : "#000000"} emissiveIntensity={systemActive ? 0.18 : selected ? 0.12 : 0} />
      </mesh>
      <mesh position={[0, height / 2 + 0.06, 0]} rotation={[-Math.PI / 2, 0, 0]}>
        <planeGeometry args={[size[0] * 0.92, size[2] * 0.92]} />
        <meshStandardMaterial color="#f5f1e8" roughness={0.95} />
      </mesh>
      {showLabel ? (
        <Html position={[0, height + 0.8, 0]} center distanceFactor={32} zIndexRange={[4, 0]}>
          <span className={`scene-label ${selected ? "is-selected" : ""}`}>{structure.label}</span>
        </Html>
      ) : null}
    </group>
  );
}

function shouldShowLabel(structure, selected, systemActive, labelCutoff) {
  if (selected) return true;
  const priority = Number(structure.display?.label_priority ?? 4);
  const cutoff = Number(labelCutoff ?? 5);
  if (priority <= cutoff) return true;
  return cutoff >= 2 && systemActive && priority <= cutoff + 1;
}
