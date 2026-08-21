import pytest
from app.services.mission_control_os.security_event_fabric import SecurityEventFabric

def test_event_validation_schema():
    fabric = SecurityEventFabric()
    evt = fabric.get_event("evt_early_warning_darkstorm")
    assert evt is not None
    assert evt.event_type == "EARLY_WARNING"
    assert evt.confidence == 0.92
