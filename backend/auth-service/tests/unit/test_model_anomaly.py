import pytest
from app.services.ai_governance.model_behavior_monitoring_engine import ModelBehaviorMonitoringEngine

def test_model_error_rate_nominal():
    engine = ModelBehaviorMonitoringEngine()
    summary = engine.get_monitoring_summary()
    assert summary["error_rate"] < 0.01
