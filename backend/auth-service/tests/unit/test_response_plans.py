import pytest
from app.services.global_defense.coordinated_response_engine import CoordinatedResponseEngine

def test_response_plan_retrieval():
    engine = CoordinatedResponseEngine()
    plans = engine.list_plans()
    assert len(plans) >= 1
    assert plans[0].verification_gate == "Phase 24 Control Re-Verification"
