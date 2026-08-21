import pytest
from app.services.mission_control_os.security_event_fabric import SecurityEventFabric

def test_event_tenant_isolation_partition():
    fabric = SecurityEventFabric()
    fabric.publish_event("ALERT_CREATED", "soc", {}, "idem_tenant_b", tenant_id="tenant_b")
    
    tenant_a_events = fabric.list_events("tenant_a")
    for e in tenant_a_events:
        assert e.tenant_id == "tenant_a"
