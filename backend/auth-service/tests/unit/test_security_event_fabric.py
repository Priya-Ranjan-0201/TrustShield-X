import pytest
from app.services.mission_control_os.security_event_fabric import SecurityEventFabric

def test_security_event_fabric_publish_and_retrieve():
    fabric = SecurityEventFabric()
    res = fabric.publish_event(
        event_type="ALERT_CREATED",
        source="soc_sensor",
        payload={"alert": "credential_stuffing_detected"},
        idempotency_key="idem_evt_1001",
    )
    assert res["status"] == "PUBLISHED"
    assert res["duplicated"] is False
    assert len(fabric.list_events("default_tenant")) >= 2
