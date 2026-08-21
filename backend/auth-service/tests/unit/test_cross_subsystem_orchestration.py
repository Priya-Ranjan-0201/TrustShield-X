import pytest
from app.services.mission_control_os.subsystem_integration_bridge import SubsystemIntegrationBridge

def test_cross_subsystem_end_to_end_context():
    bridge = SubsystemIntegrationBridge()
    ctx = bridge.query_cross_subsystem_context()
    assert "threat_intelligence" in ctx
    assert "digital_twin_lab" in ctx
    assert "security_assurance" in ctx
    assert "security_engineering" in ctx
    assert "resilience_recovery" in ctx
