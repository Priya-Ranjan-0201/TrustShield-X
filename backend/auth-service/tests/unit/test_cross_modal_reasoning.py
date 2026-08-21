import pytest
from app.services.knowledge_fabric.knowledge_relationship_manager import KnowledgeRelationshipManager


def test_cross_modal_reasoning_links():
    manager = KnowledgeRelationshipManager()

    rel = manager.create_relationship(
        source_id="qr_phish_landing_page",
        target_id="apk_malware_stealer",
        relation_type="RESOLVES",
        evidence=["ev_redirect_chain_log"],
        confidence=0.94,
    )

    assert rel.relation_type == "RESOLVES"
    assert rel.confidence == 0.94
