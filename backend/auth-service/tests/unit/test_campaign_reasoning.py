import pytest
from app.services.knowledge_fabric.knowledge_relationship_manager import KnowledgeRelationshipManager


def test_campaign_reasoning_indicators():
    manager = KnowledgeRelationshipManager()

    rels = manager.get_relationships_for_node("camp_shadow_hydra")
    assert len(rels) >= 1
    assert any(r.relation_type == "INDICATES" for r in rels)
