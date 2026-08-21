import pytest
from app.services.enterprise_governance.continuous_control_monitoring_engine import ContinuousControlMonitoringEngine

def test_continuous_control_monitoring_status():
    engine = ContinuousControlMonitoringEngine()
    status = engine.evaluate_live_monitoring("default_tenant")
    assert status["monitoring_status"] == "CONTINUOUS_ASSURANCE_NOMINAL"
    assert status["failed_controls"] == 0
