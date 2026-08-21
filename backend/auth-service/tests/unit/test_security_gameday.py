import pytest
from app.services.assurance_fabric.security_gameday_engine import SecurityGameDayEngine

def test_security_gameday():
    engine = SecurityGameDayEngine()
    gamedays = engine.list_gamedays()
    assert len(gamedays) >= 1
    g = engine.execute_gameday(
        scenario_name="RANSOMWARE_CONTAINMENT_SIMULATION",
        phases=["DETECTION", "CONTAINMENT", "RECOVERY", "VALIDATION"],
        mttd=38.0,
        mtta=95.0,
    )
    assert g.status == "COMPLETED"
    assert g.mttd_seconds == 38.0
