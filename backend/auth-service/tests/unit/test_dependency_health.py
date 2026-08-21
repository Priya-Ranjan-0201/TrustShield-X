import pytest
from app.services.mission_control_os.mission_control_health_engine import MissionControlHealthEngine

def test_dependency_health_for_automation():
    engine = MissionControlHealthEngine()
    assert engine.is_subsystem_available_for_automation("soar") is True
    assert engine.is_subsystem_available_for_automation("digital_twin") is True
