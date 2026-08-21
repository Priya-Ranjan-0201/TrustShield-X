import pytest
from app.services.mission_control_os.security_event_fabric import SecurityEventFabric

def test_event_replay_protection():
    fabric = SecurityEventFabric()
    res = fabric.publish_event("RESPONSE_STARTED", "soar", {}, "idem_darkstorm_seed_01")
    assert res["status"] == "IGNORE_DUPLICATE"
