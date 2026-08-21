import pytest
from app.services.mission_control_os.subsystem_integration_bridge import SubsystemIntegrationBridge

def test_resilience_subsystem_integration():
    bridge = SubsystemIntegrationBridge()
    ctx = bridge.query_cross_subsystem_context()
    assert ctx["resilience_recovery"]["status"] == "VERIFIED_OPERATIONAL"
