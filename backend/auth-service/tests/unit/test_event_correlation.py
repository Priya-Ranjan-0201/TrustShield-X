import pytest
from app.services.mission_control_os.security_event_fabric import SecurityEventFabric

def test_event_correlation_tracking():
    fabric = SecurityEventFabric()
    res = fabric.publish_event("CAMPAIGN_UPDATED", "intel", {}, "idem_3", correlation_id="corr_darkstorm_campaign")
    evt = fabric.get_event(res["event_id"])
    assert evt.correlation_id == "corr_darkstorm_campaign"
