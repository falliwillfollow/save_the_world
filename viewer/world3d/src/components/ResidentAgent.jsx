import { Html } from "@react-three/drei";
import { useFrame } from "@react-three/fiber";
import { useMemo, useRef } from "react";
import { percentToHour } from "../world/time.js";
import { allWorldObjects, eventTargetFor, vecToArray } from "../world/layout.js";

export default function ResidentAgent({ resident, manifest, timePercent, reducedMotion, visible, labelCutoff, onSelect }) {
  const ref = useRef();
  const activity = useMemo(() => activityForResident(manifest, resident, timePercent), [manifest, resident, timePercent]);
  const position = [activity.position[0], 1.1, activity.position[2]];

  useFrame(({ clock }) => {
    if (!ref.current || reducedMotion) return;
    ref.current.position.y = position[1] + Math.sin(clock.elapsedTime * 2 + resident.id.length) * 0.08;
  });

  if (!visible) return null;
  return (
    <group ref={ref} position={position} onClick={event => { event.stopPropagation(); onSelect({ ...resident, type: "resident_archetype", evidence_card_id: activity.target?.evidence_card_id, state: { status: activity.label } }); }}>
      <mesh castShadow>
        <sphereGeometry args={[0.72, 18, 18]} />
        <meshStandardMaterial color="#25364a" roughness={0.6} />
      </mesh>
      <mesh position={[0, -0.9, 0]} castShadow>
        <capsuleGeometry args={[0.42, 0.9, 8, 16]} />
        <meshStandardMaterial color="#5d7d8c" roughness={0.7} />
      </mesh>
      {Number(labelCutoff ?? 5) >= 5 ? (
        <Html position={[0, 1.1, 0]} center distanceFactor={28} zIndexRange={[4, 0]}>
          <span className="scene-label resident-label">{resident.label}</span>
        </Html>
      ) : null}
    </group>
  );
}

function activityForResident(manifest, resident, timePercent) {
  const home = allWorldObjects(manifest).find(item => item.id === resident.home_structure_id);
  const homePosition = vecToArray(resident.position);
  const currentMinute = percentToMinute(timePercent);
  const events = (manifest.daily_events || [])
    .filter(event => event.resident_id === resident.id)
    .map(event => ({ ...event, startMinute: parseTime(event.time), endMinute: parseTime(event.time) + Number(event.duration_minutes || 0) }))
    .sort((a, b) => a.startMinute - b.startMinute);

  for (const event of events) {
    const target = eventTargetFor(manifest, event);
    if (!target) continue;
    const targetPosition = vecToArray(target.position);
    const walkStart = event.startMinute - 45;
    const returnEnd = event.endMinute + 45;
    if (currentMinute >= walkStart && currentMinute < event.startMinute) {
      return {
        position: interpolate(homePosition, targetPosition, (currentMinute - walkStart) / 45),
        label: "walking_to_task",
        target,
      };
    }
    if (currentMinute >= event.startMinute && currentMinute <= event.endMinute) {
      return {
        position: targetPosition,
        label: event.type,
        target,
      };
    }
    if (currentMinute > event.endMinute && currentMinute <= returnEnd) {
      return {
        position: interpolate(targetPosition, homePosition, (currentMinute - event.endMinute) / 45),
        label: "returning_home",
        target,
      };
    }
  }

  return {
    position: homePosition,
    label: "at_home",
    target: home,
  };
}

function parseTime(value) {
  const [hours, minutes] = String(value || "00:00").split(":").map(part => Number(part || 0));
  return Math.max(0, Math.min(1439, hours * 60 + minutes));
}

function percentToMinute(value) {
  return percentToHour(value) * 60 + Math.floor(((Number(value || 0) % (100 / 24)) / (100 / 24)) * 60);
}

function interpolate(start, end, amount) {
  const t = Math.max(0, Math.min(1, amount));
  return [
    start[0] + (end[0] - start[0]) * t,
    start[1] + (end[1] - start[1]) * t,
    start[2] + (end[2] - start[2]) * t,
  ];
}
