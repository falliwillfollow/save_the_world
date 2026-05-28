from __future__ import annotations

import unittest

from ciac.io import load_data
from ciac.research_registry import build_research_registry, extract_sources_from_document
from ciac.validation import validate_data
from ciac.world_manifest import build_world_manifest


class ResearchRegistryTests(unittest.TestCase):
    def test_research_registry_validates_and_maps_sources_to_fields(self) -> None:
        policy = load_data("capability_policies/ciac_capability_policy_v0.yaml")
        registry = build_research_registry(policy, source_path="capability_policies/ciac_capability_policy_v0.yaml")

        self.assertTrue(validate_data(registry, "research-registry").ok)
        by_id = {entry["id"]: entry for entry in registry["entries"]}
        self.assertIn("CDC_HUMAN_WASTE_WORKER_SAFETY", by_id)
        self.assertIn("sanitation", by_id["CDC_HUMAN_WASTE_WORKER_SAFETY"]["domains"])
        self.assertTrue(by_id["CDC_HUMAN_WASTE_WORKER_SAFETY"]["model_fields"])

    def test_world_evidence_cards_resolve_source_details(self) -> None:
        runtime = load_data("examples/generated/micro_commons_runtime_bundle.json")
        registry = load_data("research_registry/ciac_research_registry_v0.yaml")
        manifest = build_world_manifest(runtime, population=80, research_registry=registry)
        cards = {card["id"]: card for card in manifest["evidence_cards"]}

        sanitation = cards["evidence_sanitation_node"]
        self.assertIn("CDC_HUMAN_WASTE_WORKER_SAFETY", sanitation["source_ids"])
        self.assertTrue(any(source.get("organization") == "CDC" for source in sanitation["sources"]))
        self.assertIn("not approvals", sanitation["source_note"])
        food = cards["evidence_food_commons"]
        self.assertIn("FDA_FOOD_CODE_2022", food["source_ids"])

    def test_research_registry_ingests_document_sources(self) -> None:
        sources = extract_sources_from_document("docs/scaling_research/ciac_deep_research_scaling_thresholds_part_3_v0_1.md")

        self.assertTrue(any(source["id"] == "FDA_FOOD_CODE_2022" for source in sources))
        self.assertTrue(any("food" in source["domains"] for source in sources))
        self.assertTrue(any(source["url"].startswith("https://") for source in sources))


if __name__ == "__main__":
    unittest.main()
