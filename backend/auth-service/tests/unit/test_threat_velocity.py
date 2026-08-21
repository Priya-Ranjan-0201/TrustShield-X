import pytest
from app.services.global_intelligence.threat_velocity_engine import ThreatVelocityEngine

def test_threat_velocity_surge_calculation():
    engine = ThreatVelocityEngine()
    res = engine.calculate_velocity("cmp_darkstorm_2026", new_indicators_24h=25, baseline_indicators_daily=5)
    assert res["growth_rate_metric"] == 4.0
    assert res["velocity_surge_detected"] is True
    assert res["status"] == "SURGE"
