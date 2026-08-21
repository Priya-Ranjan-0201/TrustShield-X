import pytest
from app.services.global_defense.defensive_knowledge_sharing_engine import DefensiveKnowledgeSharingEngine

def test_defense_propagation_reusable_techniques():
    engine = DefensiveKnowledgeSharingEngine()
    k = engine.get_knowledge("dknow_darkstorm_dns_rate_limit")
    assert k is not None
    assert "CORE_DNS" in k.compatibility
