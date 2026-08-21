import pytest
from app.services.knowledge_fabric.knowledge_relationship_manager import KnowledgeRelationshipManager


def test_control_reasoning_links():
    manager = KnowledgeRelationshipManager()

    rels = manager.get_relationships_for_node("ctrl_waf_edge_01")
    assert len(rels) >= 1
    assert any(r.relation_type == "PROTECTS" for r in rels)
