import pytest
from app.services.mission_control_os.subsystem_integration_bridge import SubsystemIntegrationBridge

def test_threat_incident_correlation_state():
    bridge = SubsystemIntegrationBridge()
    ctx = bridge.query_cross_subsystem_context("cmp_darkstorm_2026")
    assert ctx["threat_intelligence"]["campaign_id"] == "cmp_darkstorm_2026"
    assert ctx["soc_incident_command"]["incident_status"] == "CONTAINED"
