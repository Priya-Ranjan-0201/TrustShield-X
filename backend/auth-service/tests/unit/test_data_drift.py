import pytest
from app.services.assurance_fabric.model_assurance_engine import ModelAssuranceEngine

def test_data_drift():
    engine = ModelAssuranceEngine()
    drift_res = engine.detect_data_drift({"feature_token_length": 0.25, "feature_entropy": 0.05})
    assert drift_res["drift_detected"] is True
    assert "feature_token_length" in drift_res["drifted_features"]
