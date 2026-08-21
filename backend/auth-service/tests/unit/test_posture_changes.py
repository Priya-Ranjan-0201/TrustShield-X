import pytest
from app.services.fusion.security_posture_engine import SecurityPostureEngine


def test_posture_degradation_trend_detection():
    engine = SecurityPostureEngine()

    # Initial healthy state
    pos1 = engine.calculate_posture(
        risk_score=10.0,
        trust_score=95.0,
        exposure_score=15.0,
        active_threats_count=0,
        critical_assets_count=1,
        active_campaigns_count=0,
        open_incidents_count=0,
        tenant_id="tenant_trend",
    )
    assert pos1.trend == "stable"

    # Sudden surge in threat activity and incidents -> rapid degradation
    pos2 = engine.calculate_posture(
        risk_score=85.0,
        trust_score=40.0,
        exposure_score=80.0,
        active_threats_count=8,
        critical_assets_count=1,
        active_campaigns_count=3,
        open_incidents_count=4,
        tenant_id="tenant_trend",
    )
    assert pos2.trend in ("degrading", "rapidly_degrading")
    assert pos2.overall_posture_score < pos1.overall_posture_score
