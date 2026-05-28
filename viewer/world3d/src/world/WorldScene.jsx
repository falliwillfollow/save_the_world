import { Environment, OrbitControls, PerspectiveCamera } from "@react-three/drei";
import { Canvas } from "@react-three/fiber";
import { useMemo } from "react";
import InfrastructureNode from "../components/InfrastructureNode.jsx";
import Path from "../components/Path.jsx";
import ResidentAgent from "../components/ResidentAgent.jsx";
import Structure from "../components/Structure.jsx";
import Zone from "../components/Zone.jsx";
import FirstPersonController from "./FirstPersonController.jsx";
import { worldBounds } from "./scaleManifest.js";

export default function WorldScene({
  manifest,
  mode,
  selectedObject,
  selectedSystem,
  selectedScenario,
  highlightedObjectIds,
  timePercent,
  reducedMotion,
  onSelectObject,
}) {
  const selectedId = selectedObject?.id;
  const highlighted = new Set(highlightedObjectIds || []);
  const bounds = useMemo(() => worldBounds(manifest), [manifest]);
  const labelCutoff = labelCutoffFor(manifest.population?.residents || 80);
  const cameraDistance = Math.max(56, bounds.radius * 0.9);
  const cameraHeight = Math.max(36, bounds.radius * 0.55);
  return (
    <Canvas
      shadows
      dpr={[1, 2]}
      gl={{ alpha: false, preserveDrawingBuffer: true }}
      className="world-canvas"
      onPointerMissed={() => onSelectObject(null)}
    >
      <PerspectiveCamera makeDefault position={[bounds.center[0] + cameraDistance, cameraHeight, bounds.center[2] + cameraDistance]} fov={45} />
      <color attach="background" args={["#eef3f4"]} />
      {mode === "walk" ? <fog attach="fog" args={["#dfe7e7", 38, Math.max(130, bounds.radius * 1.15)]} /> : null}
      <ambientLight intensity={0.62} />
      <directionalLight position={[20, 38, 16]} intensity={1.9} castShadow shadow-mapSize-width={2048} shadow-mapSize-height={2048} />
      <hemisphereLight args={["#dbe8f1", "#9a8f7a", 0.48]} />
      <mesh rotation={[-Math.PI / 2, 0, 0]} position={[bounds.center[0], -0.1, bounds.center[2]]} receiveShadow>
        <planeGeometry args={[bounds.size[0], bounds.size[2], 20, 20]} />
        <meshStandardMaterial color="#d7dccf" roughness={1} />
      </mesh>
      {(manifest.zones || []).map(zone => (
        <Zone key={zone.id} zone={zone} selected={selectedId === zone.id || highlighted.has(zone.id)} labelCutoff={labelCutoff} onSelect={onSelectObject} />
      ))}
      {(manifest.paths || []).map(path => (
        <Path key={path.id} path={path} mode={mode} selectedScenario={selectedScenario} selected={selectedId === path.id || highlighted.has(path.id)} onSelect={onSelectObject} />
      ))}
      {(manifest.structures || []).map(structure => (
        <Structure
          key={structure.id}
          structure={structure}
          mode={mode}
          selectedScenario={selectedScenario}
          selectedSystem={selectedSystem}
          selected={selectedId === structure.id || highlighted.has(structure.id)}
          labelCutoff={labelCutoff}
          onSelect={onSelectObject}
        />
      ))}
      {(manifest.infrastructure_nodes || []).map(node => (
        <InfrastructureNode
          key={node.id}
          node={node}
          mode={mode}
          selectedScenario={selectedScenario}
          selectedSystem={selectedSystem}
          selected={selectedId === node.id || highlighted.has(node.id)}
          labelCutoff={labelCutoff}
          onSelect={onSelectObject}
        />
      ))}
      {(manifest.residents || []).map(resident => (
        <ResidentAgent
          key={resident.id}
          resident={resident}
          manifest={manifest}
          timePercent={timePercent}
          reducedMotion={reducedMotion}
          visible={mode === "life"}
          labelCutoff={labelCutoff}
          onSelect={onSelectObject}
        />
      ))}
      <Environment preset="city" />
      {mode === "walk" ? (
        <FirstPersonController
          manifest={manifest}
          active={mode === "walk"}
          selectedObject={selectedObject}
          onSelectObject={onSelectObject}
        />
      ) : (
        <OrbitControls target={bounds.center} minDistance={28} maxDistance={Math.max(105, bounds.radius * 1.6)} maxPolarAngle={Math.PI / 2.25} enableDamping={!reducedMotion} />
      )}
    </Canvas>
  );
}

function labelCutoffFor(population) {
  const people = Number(population || 80);
  if (people <= 150) return 5;
  if (people <= 500) return 2;
  return 1;
}
