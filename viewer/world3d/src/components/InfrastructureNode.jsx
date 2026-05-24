import { Html } from "@react-three/drei";
import { assetFor } from "../world/AssetRegistry.js";
import { objectStatusForMode, statusColor, vecToArray } from "../world/layout.js";

export default function InfrastructureNode({ node, mode, selectedScenario, selectedSystem, selected, labelCutoff, onSelect }) {
  const asset = assetFor(node);
  const position = vecToArray(node.position);
  const status = objectStatusForMode(node, mode, selectedScenario);
  const color = statusColor(status, asset.color);
  const active = selectedSystem && node.type === selectedSystem;
  const showLabel = shouldShowLabel(node, selected, active, labelCutoff);
  return (
    <group position={[position[0], 1.5, position[2]]} onClick={event => { event.stopPropagation(); onSelect(node); }}>
      {asset.component === "cylinder" ? (
        <mesh castShadow receiveShadow>
          <cylinderGeometry args={[2.8, 2.8, 3, 24]} />
          <meshStandardMaterial color={color} emissive={active || selected ? color : "#000"} emissiveIntensity={active ? 0.18 : selected ? 0.12 : 0} />
        </mesh>
      ) : (
        <mesh castShadow receiveShadow>
          <boxGeometry args={[5.5, 3, 4]} />
          <meshStandardMaterial color={color} roughness={0.65} emissive={active || selected ? color : "#000"} emissiveIntensity={active ? 0.18 : selected ? 0.12 : 0} />
        </mesh>
      )}
      {showLabel ? (
        <Html position={[0, 2.7, 0]} center distanceFactor={30} zIndexRange={[4, 0]}>
          <span className={`scene-label node-label ${selected ? "is-selected" : ""}`}>{node.label}</span>
        </Html>
      ) : null}
    </group>
  );
}

function shouldShowLabel(node, selected, active, labelCutoff) {
  if (selected) return true;
  const priority = Number(node.display?.label_priority ?? 4);
  const cutoff = Number(labelCutoff ?? 5);
  if (priority <= cutoff) return true;
  return cutoff >= 2 && active && priority <= cutoff + 1;
}
