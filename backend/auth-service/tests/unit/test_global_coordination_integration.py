import pytest
from app.services.mission_control_os.global_security_mission_control_engine import GlobalSecurityMissionControlEngine

def test_global_coordination_integration():
    engine = GlobalSecurityMissionControlEngine()
    ov = engine.get_mission_overview()
    assert ov["operational_status"] == "OPERATIONAL"
