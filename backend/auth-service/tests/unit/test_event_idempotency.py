import pytest
from app.services.mission_control_os.security_event_fabric import SecurityEventFabric

def test_event_idempotency_duplicate_prevention():
    fabric = SecurityEventFabric()
    
    # 1. Publish event
    res1 = fabric.publish_event(
        event_type="INCIDENT_CREATED",
        source="soc",
        payload={"incident_id": "inc_1"},
        idempotency_key="idem_unique_key_999",
    )
    assert res1["status"] == "PUBLISHED"
    
    # 2. Re-publish with exact same idempotency_key
    res2 = fabric.publish_event(
        event_type="INCIDENT_CREATED",
        source="soc",
        payload={"incident_id": "inc_1"},
        idempotency_key="idem_unique_key_999",
    )
    assert res2["status"] == "IGNORE_DUPLICATE"
    assert res2["duplicated"] is True
