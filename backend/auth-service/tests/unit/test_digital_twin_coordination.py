import pytest
from app.services.global_defense.defensive_knowledge_sharing_engine import DefensiveKnowledgeSharingEngine

def test_digital_twin_simulation_validation_link():
    engine = DefensiveKnowledgeSharingEngine()
    k = engine.get_knowledge("dknow_darkstorm_dns_rate_limit")
    assert "Digital Twin" in k.validation_result
