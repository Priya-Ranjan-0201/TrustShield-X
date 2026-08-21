import pytest
from app.services.ai_governance.model_behavior_monitoring_engine import ModelBehaviorMonitoringEngine

def test_model_drift_status():
    engine = ModelBehaviorMonitoringEngine()
    summary = engine.get_monitoring_summary()
    assert summary["input_drift_status"] == "STABLE"
    assert summary["output_drift_status"] == "STABLE"
