import pytest
from app.services.mission_control_os.subsystem_integration_bridge import SubsystemIntegrationBridge

def test_assurance_subsystem_integration():
    bridge = SubsystemIntegrationBridge()
    ctx = bridge.query_cross_subsystem_context()
    assert ctx["security_assurance"]["control_status"] == "PASSING"
