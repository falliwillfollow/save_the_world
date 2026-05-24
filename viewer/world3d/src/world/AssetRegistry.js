export const COLOR_TOKENS = {
  common_core: "#b96f3d",
  housing: "#c9b8a2",
  food: "#5e9d57",
  protein: "#24a994",
  water: "#2f79b9",
  energy: "#d8b33f",
  sanitation: "#77716b",
  maintenance: "#c77f3f",
  care: "#c95b68",
  governance: "#7d5aa6",
  social: "#8d7cb8",
  risk: "#4f4f57",
  mobility: "#667b8a",
  service_edge: "#7a7f84",
  labor_time: "#4f8a7f",
  dignity_privacy: "#9a8f7a",
};

export const ASSET_REGISTRY = {
  common_house: { component: "box", color: "#b96f3d", defaultSize: [13, 4, 9], icon: "house" },
  residential_pod: { component: "box", color: "#c9b8a2", defaultSize: [10, 3, 8], icon: "bed" },
  food_commons: { component: "box", color: "#5e9d57", defaultSize: [12, 3.5, 7], icon: "leaf" },
  protein_commons: { component: "box", color: "#24a994", defaultSize: [9, 3, 6], icon: "sprout" },
  care_room: { component: "box", color: "#c95b68", defaultSize: [7, 3, 6], icon: "heart" },
  social_cultural: { component: "box", color: "#8d7cb8", defaultSize: [10, 3, 6], icon: "sparkles" },
  maintenance_shop: { component: "box", color: "#c77f3f", defaultSize: [11, 3, 7], icon: "wrench" },
  quiet_studio: { component: "box", color: "#4f8a7f", defaultSize: [8, 3, 6], icon: "palette" },
  water: { component: "cylinder", color: "#2f79b9", defaultSize: [5, 3, 5], icon: "droplets" },
  energy: { component: "box", color: "#d8b33f", defaultSize: [6, 2.5, 5], icon: "zap" },
  sanitation: { component: "box", color: "#77716b", defaultSize: [7, 2.8, 5], icon: "shield" },
  risk: { component: "box", color: "#4f4f57", defaultSize: [5, 3, 3], icon: "activity" },
};

export function assetFor(object) {
  return ASSET_REGISTRY[object.type] || ASSET_REGISTRY[object.asset_key] || ASSET_REGISTRY.common_house;
}

export function tokenColor(token, fallback = "#8c96a3") {
  return COLOR_TOKENS[token] || fallback;
}
