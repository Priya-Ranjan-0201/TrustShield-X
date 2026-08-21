import pytest
from app.services.mission_control_os.security_event_fabric import SecurityEventFabric

def test_mission_scale_high_event_ingestion():
    fabric = SecurityEventFabric()
    for i in range(50):
        res = fabric.publish_event("ALERT_CREATED", "load_gen", {"i": i}, f"idem_scale_evt_{i}")
        assert res["status"] == "PUBLISHED"
