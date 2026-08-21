import pytest
from app.services.knowledge_fabric.knowledge_revocation_engine import KnowledgeRevocationEngine


def test_knowledge_revocation_impact():
    engine = KnowledgeRevocationEngine()
    impact = engine.revoke_source("ev_false_feed_01")

    assert impact.requires_reassessment is True
    assert "asrt_checkout_at_risk" in impact.affected_assertions
    assert "inc_2026_001" in impact.affected_incidents
