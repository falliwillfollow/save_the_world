import sampleManifest from "../../../../examples/world_manifests/civic_floor_80_v0.world.json";

export async function loadDefaultWorldManifest() {
  return sampleManifest;
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
