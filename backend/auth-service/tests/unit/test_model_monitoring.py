import pytest
from app.services.ai_governance.model_behavior_monitoring_engine import ModelBehaviorMonitoringEngine

def test_model_runtime_monitoring():
    engine = ModelBehaviorMonitoringEngine()
    summary = engine.get_monitoring_summary()
    assert summary["telemetry_health"] == "HEALTHY"
    assert summary["avg_latency_ms"] < 50.0
