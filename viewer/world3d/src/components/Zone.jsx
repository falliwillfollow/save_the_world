import { Html } from "@react-three/drei";
import { tokenColor } from "../world/AssetRegistry.js";
import { vecToArray } from "../world/layout.js";

export default function Zone({ zone, selected, labelCutoff, onSelect }) {
  const [x, y, z] = vecToArray(zone.position);
  const color = tokenColor(zone.color_token, "#9fb2c8");
  const showLabel = selected || Number(zone.display?.label_priority ?? 1) <= Number(labelCutoff ?? 5) + 1;
  return (
    <group position={[x, y, z]} onClick={event => { event.stopPropagation(); onSelect(zone); }}>
      <mesh rotation={[-Math.PI / 2, 0, 0]} receiveShadow>
        <planeGeometry args={[zone.size.x, zone.size.z]} />
        <meshStandardMaterial color={color} transparent opacity={selected ? 0.34 : 0.18} roughness={0.9} />
      </mesh>
      {showLabel ? (
        <Html position={[0, 0.18, 0]} center distanceFactor={34} zIndexRange={[4, 0]}>
          <span className={`scene-label ${selected ? "is-selected" : ""}`}>{zone.label}</span>
        </Html>
      ) : null}
    </group>
  );
}
