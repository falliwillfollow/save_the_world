import { useFrame, useThree } from "@react-three/fiber";
import { useEffect, useMemo, useRef } from "react";
import * as THREE from "three";
import { sizeToArray, vecToArray } from "./layout.js";
import { worldBounds } from "./scaleManifest.js";

const EYE_HEIGHT = 1.72;
const WALK_SPEED = 18;
const SPRINT_SPEED = 30;
const LOOK_SENSITIVITY = 0.0022;
const INSPECTION_DISTANCE = 34;

export default function FirstPersonController({
  manifest,
  active,
  selectedObject,
  onSelectObject,
  onFocusObject,
}) {
  const { camera, gl } = useThree();
  const keys = useRef(new Set());
  const yaw = useRef(0);
  const pitch = useRef(0);
  const targetRef = useRef(null);
  const lastTargetId = useRef("");
  const raycaster = useMemo(() => new THREE.Raycaster(), []);
  const inspectables = useMemo(() => inspectableBounds(manifest), [manifest]);

  useEffect(() => {
    if (!active) return undefined;
    const bounds = worldBounds(manifest);
    camera.position.set(bounds.center[0], EYE_HEIGHT, bounds.center[2] + Math.max(34, bounds.radius * 0.45));
    camera.lookAt(bounds.center[0], EYE_HEIGHT, bounds.center[2]);
    yaw.current = camera.rotation.y;
    pitch.current = camera.rotation.x;
    return undefined;
  }, [active, camera, manifest]);

  useEffect(() => {
    if (!active) {
      keys.current.clear();
      return undefined;
    }

    const canvas = gl.domElement;
    const onPointerDown = () => {
      if (document.pointerLockElement !== canvas) {
        canvas.requestPointerLock?.();
      }
    };
    const onMouseMove = event => {
      if (document.pointerLockElement !== canvas) return;
      yaw.current -= event.movementX * LOOK_SENSITIVITY;
      pitch.current = THREE.MathUtils.clamp(
        pitch.current - event.movementY * LOOK_SENSITIVITY,
        -Math.PI / 2.4,
        Math.PI / 2.4
      );
    };
    const onKeyDown = event => {
      keys.current.add(event.code);
      if (event.code === "KeyE") {
        event.preventDefault();
        if (targetRef.current) {
          onSelectObject(targetRef.current.object);
        }
      }
    };
    const onKeyUp = event => keys.current.delete(event.code);

    canvas.addEventListener("pointerdown", onPointerDown);
    window.addEventListener("mousemove", onMouseMove);
    window.addEventListener("keydown", onKeyDown);
    window.addEventListener("keyup", onKeyUp);
    return () => {
      canvas.removeEventListener("pointerdown", onPointerDown);
      window.removeEventListener("mousemove", onMouseMove);
      window.removeEventListener("keydown", onKeyDown);
      window.removeEventListener("keyup", onKeyUp);
      if (document.pointerLockElement === canvas) {
        document.exitPointerLock?.();
      }
      keys.current.clear();
      lastTargetId.current = "";
      window.dispatchEvent(new CustomEvent("ciac-walk-target", { detail: null }));
    };
  }, [active, gl, onSelectObject]);

  useEffect(() => {
    if (!active || !selectedObject) return;
    const target = inspectables.find(item => item.object.id === selectedObject.id);
    if (target) {
      const center = target.box.getCenter(new THREE.Vector3());
      onFocusObject?.(center);
    }
  }, [active, inspectables, onFocusObject, selectedObject]);

  useFrame((_, delta) => {
    if (!active) return;
    camera.rotation.order = "YXZ";
    camera.rotation.y = yaw.current;
    camera.rotation.x = pitch.current;
    camera.rotation.z = 0;

    const forward = new THREE.Vector3();
    camera.getWorldDirection(forward);
    forward.y = 0;
    forward.normalize();
    const right = new THREE.Vector3().crossVectors(forward, camera.up).normalize();

    const direction = new THREE.Vector3();
    if (keys.current.has("KeyW") || keys.current.has("ArrowUp")) direction.add(forward);
    if (keys.current.has("KeyS") || keys.current.has("ArrowDown")) direction.sub(forward);
    if (keys.current.has("KeyA") || keys.current.has("ArrowLeft")) direction.sub(right);
    if (keys.current.has("KeyD") || keys.current.has("ArrowRight")) direction.add(right);
    if (direction.lengthSq() > 0) {
      direction.normalize();
      const speed = keys.current.has("ShiftLeft") || keys.current.has("ShiftRight") ? SPRINT_SPEED : WALK_SPEED;
      camera.position.addScaledVector(direction, speed * delta);
      camera.position.y = EYE_HEIGHT;
    }

    raycaster.setFromCamera({ x: 0, y: 0 }, camera);
    raycaster.far = INSPECTION_DISTANCE;
    targetRef.current = nearestHit(raycaster.ray, inspectables);
    const target = targetRef.current?.object || null;
    const targetId = target?.id || "";
    if (targetId !== lastTargetId.current) {
      lastTargetId.current = targetId;
      window.dispatchEvent(new CustomEvent("ciac-walk-target", { detail: target }));
    }
  });

  return null;
}

function inspectableBounds(manifest) {
  const structures = (manifest.structures || []).map(structure => {
    const position = vecToArray(structure.position);
    const size = sizeToArray(structure.size);
    return {
      object: structure,
      box: new THREE.Box3().setFromCenterAndSize(
        new THREE.Vector3(position[0], size[1] / 2, position[2]),
        new THREE.Vector3(size[0], Math.max(size[1], 2.5), size[2])
      ),
    };
  });
  const nodes = (manifest.infrastructure_nodes || []).map(node => {
    const position = vecToArray(node.position);
    const size = node.type === "water" ? [5.8, 3.2, 5.8] : [6.2, 3.2, 4.8];
    return {
      object: node,
      box: new THREE.Box3().setFromCenterAndSize(
        new THREE.Vector3(position[0], size[1] / 2, position[2]),
        new THREE.Vector3(size[0], size[1], size[2])
      ),
    };
  });
  return [...structures, ...nodes];
}

function nearestHit(ray, inspectables) {
  let nearest = null;
  let nearestDistance = Infinity;
  const hit = new THREE.Vector3();
  inspectables.forEach(item => {
    if (!ray.intersectBox(item.box, hit)) return;
    const distance = ray.origin.distanceTo(hit);
    if (distance < nearestDistance && distance <= INSPECTION_DISTANCE) {
      nearest = item;
      nearestDistance = distance;
    }
  });
  return nearest;
}
