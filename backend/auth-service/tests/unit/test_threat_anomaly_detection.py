import pytest
from app.services.global_intelligence.threat_velocity_engine import ThreatVelocityEngine

def test_threat_nominal_velocity():
    engine = ThreatVelocityEngine()
    res = engine.calculate_velocity("cmp_quiet", new_indicators_24h=6, baseline_indicators_daily=5)
    assert res["velocity_surge_detected"] is False
    assert res["status"] == "NOMINAL"
