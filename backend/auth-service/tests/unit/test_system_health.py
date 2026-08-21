import pytest
from app.services.mission_control_os.mission_control_health_engine import MissionControlHealthEngine

def test_system_health_all_subsystems_online():
    engine = MissionControlHealthEngine()
    h = engine.check_health()
    assert h.overall_health == "HEALTHY"
    assert h.api_health == "HEALTHY"
    assert h.db_health == "HEALTHY"
    assert h.event_fabric_health == "HEALTHY"
