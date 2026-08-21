import pytest
from app.services.mission_control_os.security_event_fabric import SecurityEventFabric

def test_event_causal_ordering():
    fabric = SecurityEventFabric()
    res1 = fabric.publish_event("THREAT_DETECTED", "intel", {"ip": "1.2.3.4"}, "idem_1", causation_id=None)
    evt1_id = res1["event_id"]
    
    res2 = fabric.publish_event("ALERT_CREATED", "soc", {"alert": "c2"}, "idem_2", causation_id=evt1_id)
    evt2 = fabric.get_event(res2["event_id"])
    assert evt2.causation_id == evt1_id
