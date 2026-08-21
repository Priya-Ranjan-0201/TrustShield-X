import pytest
from app.services.global_defense.defensive_knowledge_sharing_engine import DefensiveKnowledgeSharingEngine

def test_defense_reuse_compatibility_checks():
    engine = DefensiveKnowledgeSharingEngine()
    items = engine.list_knowledge()
    assert len(items) >= 1
    assert "NGINX_INGRESS" in items[0].compatibility
