import pytest
from app.services.global_defense.coordinated_response_engine import CoordinatedResponseEngine

def test_security_assurance_verification_gate():
    engine = CoordinatedResponseEngine()
    plans = engine.list_plans()
    assert "Phase 24" in plans[0].verification_gate
