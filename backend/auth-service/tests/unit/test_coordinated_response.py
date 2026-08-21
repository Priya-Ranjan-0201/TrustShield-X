import pytest
from app.services.global_defense.coordinated_response_engine import CoordinatedResponseEngine

def test_coordinated_response_plan_creation():
    engine = CoordinatedResponseEngine()
    plan = engine.create_response_plan(
        coordination_id="coord_phishing_campaign",
        objective="Block Phishing Sender Domains & Revoke Sessions",
        participants=["tenant_alpha", "tenant_beta"],
        actions=[{"step": 1, "action": "Block MX Domain"}],
        approvals=["CISO", "SOC_LEAD"],
    )
    assert plan.coordination_id == "coord_phishing_campaign"
    assert "CISO" in plan.approvals
    assert len(engine.list_plans()) >= 2
