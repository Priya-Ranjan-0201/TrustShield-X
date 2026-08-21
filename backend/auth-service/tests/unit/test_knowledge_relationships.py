import pytest
from app.services.knowledge_fabric.knowledge_relationship_manager import KnowledgeRelationshipManager


def test_knowledge_relationships_provenance():
    manager = KnowledgeRelationshipManager()

    rel = manager.create_relationship(
        source_id="srv_database_prod",
        target_id="ctrl_encryption_vault",
        relation_type="PROTECTS",
        evidence=["ev_vault_audit_log"],
        confidence=0.97,
        source="SECURITY_AGENT",
    )

    assert rel.relationship_id.startswith("krel_")
    assert rel.relation_type == "PROTECTS"
    assert rel.evidence == ["ev_vault_audit_log"]

    node_rels = manager.get_relationships_for_node("srv_database_prod")
    assert any(r.relationship_id == rel.relationship_id for r in node_rels)
