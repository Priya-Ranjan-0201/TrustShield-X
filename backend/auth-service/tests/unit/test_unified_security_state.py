import pytest
from app.services.mission_control_os.unified_security_state_engine import UnifiedSecurityStateEngine

def test_unified_security_state_retrieval():
    engine = UnifiedSecurityStateEngine()
    state = engine.get_unified_state("default_tenant")
    assert state.tenant_id == "default_tenant"
    assert state.active_threats_count >= 1
    assert state.active_incidents_count >= 1
