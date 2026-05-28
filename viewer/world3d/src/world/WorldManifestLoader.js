import sampleManifest from "../../../../examples/world_manifests/civic_floor_80_v0.world.json";
import sampleAutomationManifest from "../../../../examples/life_manifests/automation_manifest_80_v0.json";
import sampleLifeManifest from "../../../../examples/life_manifests/life_manifest_80_v0.json";

export async function loadDefaultWorldManifest() {
  return sampleManifest;
}

export async function loadDefaultLifeManifest() {
  return sampleLifeManifest;
}

export async function loadDefaultAutomationManifest() {
  return sampleAutomationManifest;
}

export function evidenceCardFor(manifest, object) {
  if (!object?.evidence_card_id) return null;
  return manifest.evidence_cards.find(card => card.id === object.evidence_card_id) || null;
}

export function objectById(manifest, objectId) {
  return [
    ...(manifest.structures || []),
    ...(manifest.infrastructure_nodes || []),
    ...(manifest.zones || []),
    ...(manifest.paths || []),
  ].find(item => item.id === objectId);
}
