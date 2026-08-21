import pytest
from app.services.digital_twin_lab.digital_twin_state_engine import DigitalTwinStateEngine

def test_twin_multi_tenant_isolation():
    engine = DigitalTwinStateEngine()
    engine.create_snapshot(version="v1.0.0-TENANT-B", tenant_id="tenant_b")
    
    tenant_a_states = engine.list_states("tenant_a")
    for s in tenant_a_states:
        assert s.tenant_id != "tenant_b"
