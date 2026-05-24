const SCALING_POLICY_ID = "ciac_scaling_policy_v0";

export const SCALING_POLICY = {
  id: "ciac_scaling_policy_v0",
  version: "v0",
  researchInputs: [
    "docs/scaling_research/ciac_deep_research_scaling_thresholds_part_1_v0_2.md",
    "docs/scaling_research/ciac_deep_research_scaling_thresholds_part_2_v0_2.md",
    "docs/scaling_research/ciac_deep_research_scaling_thresholds_part_3_v0_1.md",
    "docs/scaling_research/ciac_deep_research_scaling_thresholds_part_4_v0_1.md",
  ],
  villageBlock: {
    preferred: 80,
    maximum: 150,
  },
  district: {
    minimum: 300,
    maximum: 500,
  },
  nodes: {
    residential_pod: policy("residential_pod", "duplicate", 12, 20, 24, 30, "privacy, sleep, perceived crowding", "Residential pod is beyond comfortable cluster size. Duplicate or subdivide."),
    elder_high_care_pod: policy("elder_high_care_pod", "duplicate", 6, 10, 12, 14, "care needs, privacy, safeguarding", "High-care residential scale should stay small-house sized."),
    common_house: policy("common_house", "hybrid", 30, 80, 100, 150, "belonging, third-place comfort, institutional feel", "One common house is serving too many residents as a single social heart. Add neighborhood commons."),
    common_meal_wave: policy("common_meal_wave", "duplicate", 12, 40, 60, 80, "dining comfort and labor load", "Shared dining is getting too large for a comfortable meal wave."),
    food_commons: policy("food_commons", "hybrid", 50, 80, 100, 150, "food safety, labor burden, scheduling", "Food commons is approaching kitchen, dining, labor, or hygiene bottleneck. Duplicate pickup or kitchen capacity."),
    shared_kitchen: policy("shared_kitchen", "hybrid", 50, 80, 80, 100, "labor, hygiene, scheduling, food safety", "Shared kitchen is becoming a labor, schedule, cleaning, or food-safety bottleneck."),
    food_service_radius: policy("food_service_radius", "duplicate", 1, 3, 5, 5, "food access, care, mobility, dignity", "Food access exceeds walk/roll threshold for high-need residents. Add meal pickup or delivery node."),
    protein_commons: policy("protein_commons", "hybrid", 50, 80, 150, 150, "food safety, acceptance, labor burden", "Protein commons should not become one opaque technical bottleneck."),
    potable_water: policy("potable_water", "hybrid", 25, 80, 150, 150, "public health, redundancy, emergency access", "Population may trigger public-water-system review. Require legal and public-health review."),
    emergency_potable_reserve: policy("emergency_potable_reserve", "duplicate", 3, 14, 150, 3, "emergency survival, high-need support, accessibility", "Emergency potable water reserve is below CIaC floor or not accessible to all residents."),
    sanitation_access: policy("sanitation_access", "hybrid", 20, 80, 150, 150, "hygiene, dignity, public health", "Sanitation access is using emergency minimum logic. Add dignified local hygiene access."),
    blackwater_treatment: policy("blackwater_treatment", "federate", 1, 1, 1, 1, "pathogen control, public health, worker safety", "Blackwater system lacks approved design, maintenance, or professional/public-health review."),
    care_room: policy("care_room", "hybrid", 50, 80, 100, 150, "privacy, illness separation, medication continuity", "Care access, privacy, or illness separation may require another care room."),
    medication_continuity: policy("medication_continuity", "hybrid", 1, 1, 80, 1, "health continuity, privacy, energy resilience", "Medication continuity or refrigerated medication backup is not protected."),
    high_need_support: policy("high_need_support", "duplicate", 1, 3, 5, 5, "disability access, elder support, privacy", "High-need resident support is not adequately local, private, or backed up."),
    quiet_room: policy("quiet_room", "duplicate", 1, 80, 80, 80, "mental health, privacy, sensory load", "No low-social-energy retreat space is available at this scale."),
    maintenance_tool_cache: policy("maintenance_tool_cache", "hybrid", 50, 80, 150, 500, "response time, autonomy, repairability", "One workshop/tool node is serving too many residents. Add local tool cache or district workshop."),
    central_workshop: policy("central_workshop", "hybrid", 150, 300, 500, 500, "specialization, reliability, safety", "Advanced workshop or hazardous tool access needs training, PPE, and federation."),
    governance_circle: policy("governance_circle", "federate", 30, 80, 80, 150, "participation quality, legitimacy, meeting burden", "Direct assembly burden rising. Federate into circles or delegated roles."),
    operational_circle: policy("operational_circle", "federate", 5, 8, 12, 15, "participation quality, role clarity, anti-capture", "Operational circle is becoming too large for consent or effective stewardship. Split or delegate roles."),
    deliberative_panel: policy("deliberative_panel", "federate", 8, 12, 24, 24, "due process, trust, conflict resolution", "Deliberative or appeal process is too large, informal, or lacks due process."),
    essential_access: policy("essential_access", "duplicate", 1, 3, 5, 5, "accessibility, disability, time burden", "Essential daily functions exceed walk/roll threshold, especially for high-need residents."),
    hands_on_skill_group: policy("hands_on_skill_group", "duplicate", 4, 6, 8, 12, "safety, attention, competence", "Training group is too large for hands-on safety or skill acquisition."),
    apprenticeship_pipeline: policy("apprenticeship_pipeline", "hybrid", 1, 3, 3, 1, "skill redundancy, expert dependency, continuity", "Critical skill has no backup or apprentice pipeline."),
    risk_resilience_cell: policy("risk_resilience_cell", "hybrid", 50, 80, 150, 300, "failure isolation, cascade prevention, recovery", "Critical function depends on one node, role, or external provider."),
    local_redundancy: policy("local_redundancy", "duplicate", 50, 80, 150, 300, "failure isolation, cascading risk, recovery", "Critical system lacks local redundancy for failure isolation."),
    reserve_topology: policy("reserve_topology", "hybrid", 1, 80, 150, 1, "access, redundancy, distribution", "Reserve is centralized, inaccessible, or lacks replenishment/distribution plan."),
    fallback_system: policy("fallback_system", "hybrid", 1, 80, 150, 1, "resilience, simplicity, rights under stress", "Fallback system is too dependent on the normal system it is meant to replace."),
    emergency_governance: policy("emergency_governance", "federate", 1, 80, 150, 1, "anti-capture, emergency speed, rights", "Emergency authority lacks backup, sunset, or anti-capture controls."),
  },
};

export function policyForType(type) {
  return SCALING_POLICY.nodes[type] || null;
}

export function countForPopulation(population, policyId, options = {}) {
  const nodePolicy = policyForType(policyId);
  if (!nodePolicy) return 1;
  const people = Math.max(1, Math.round(Number(population || 1)));
  const capacity = Math.max(1, Number(options.capacity || nodePolicy.preferred || nodePolicy.maximum || 1));
  return Math.max(1, Math.ceil(people / capacity));
}

function policy(id, scaleAction, minimum, preferred, maximum, hardMax, driver, warning) {
  return {
    id,
    policy_id: id,
    source_policy_id: SCALING_POLICY_ID,
    scale_action: scaleAction,
    minimum,
    preferred,
    maximum,
    hard_max: hardMax,
    human_factor_driver: driver,
    ui_warning: warning,
  };
}
