import pytest
from app.services.mission_control_os.security_event_fabric import SecurityEventFabric

def test_cross_tenant_event_isolation():
    fabric = SecurityEventFabric()
    fabric.publish_event("ALERT_CREATED", "soc", {"data": 123}, "idem_t_alpha", tenant_id="tenant_alpha")
    
    t_beta_events = fabric.list_events("tenant_beta")
    assert all(e.tenant_id == "tenant_beta" for e in t_beta_events)
