import pytest
from app.services.mission_control_os.subsystem_integration_bridge import SubsystemIntegrationBridge

def test_security_engineering_subsystem_integration():
    bridge = SubsystemIntegrationBridge()
    ctx = bridge.query_cross_subsystem_context()
    assert "PLAYBOOK_VERSIONED" in ctx["security_engineering"]["improvement_status"]
