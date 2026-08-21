import pytest
from app.services.mission_control_os.subsystem_integration_bridge import SubsystemIntegrationBridge

def test_campaign_incident_correlation():
    bridge = SubsystemIntegrationBridge()
    ctx = bridge.query_cross_subsystem_context("cmp_darkstorm_2026")
    assert ctx["integration_verified"] is True
