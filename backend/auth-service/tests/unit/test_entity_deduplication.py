"""Unit Tests — Entity Deduplication & Merge Safety (Phase 4.0 Part 5 — Sections 41-42, 90)."""

import pytest
from app.schemas.intelligence_graph_models import CanonicalEntityDTO
from app.services.graph.entity_deduplication import EntityDeduplicationEngine


class TestEntityDeduplication:
    def test_deduplicate_identical_domains_merges_sources(self):
        ent1 = CanonicalEntityDTO(
            entity_id="ent_01",
            entity_type="DOMAIN",
            canonical_value="example.com",
            display_value="example.com",
            normalized_value="example.com",
            value_hash="hash_01",
            source_count=1,
            aliases=["www.example.com"],
        )
        ent2 = CanonicalEntityDTO(
            entity_id="ent_02",
            entity_type="DOMAIN",
            canonical_value="example.com",
            display_value="example.com",
            normalized_value="example.com",
            value_hash="hash_01",
            source_count=2,
            aliases=["login.example.com"],
        )

        deduped = EntityDeduplicationEngine.deduplicate_entities([ent1, ent2])
        assert len(deduped) == 1
        merged = deduped[0]
        assert merged.source_count == 3
        assert "www.example.com" in merged.aliases
        assert "login.example.com" in merged.aliases

    def test_merge_safety_protects_people_and_upi(self):
        ent_person1 = CanonicalEntityDTO(
            entity_id="p1",
            entity_type="PERSON",
            canonical_value="John Doe",
            display_value="John Doe",
            normalized_value="john doe",
            value_hash="h1",
        )
        ent_person2 = CanonicalEntityDTO(
            entity_id="p2",
            entity_type="PERSON",
            canonical_value="John Doe Jr",
            display_value="John Doe Jr",
            normalized_value="john doe jr",
            value_hash="h2",
        )

        can_merge = EntityDeduplicationEngine.can_merge(ent_person1, ent_person2)
        assert can_merge is False
