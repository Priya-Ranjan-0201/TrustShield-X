import pytest
from app.services.fusion.security_posture_engine import SecurityPostureEngine


def test_security_situation_evaluation():
    engine = SecurityPostureEngine()
    sit = engine.evaluate_situation(
        active_threats_count=4,
        critical_assets_count=2,
        high_risk_exposure_count=1,
        active_campaigns_count=2,
        open_incidents_count=3,
        tenant_id="tenant_sit",
    )
    assert sit.situation_id.startswith("sit_")
    assert sit.overall_threat_level == "CRITICAL"
    assert "open incident(s)" in sit.summary
