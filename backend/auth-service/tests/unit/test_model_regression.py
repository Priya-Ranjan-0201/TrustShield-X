import pytest
from app.services.assurance_fabric.model_assurance_engine import ModelAssuranceEngine

def test_model_regression():
    engine = ModelAssuranceEngine()
    degraded = engine.evaluate_model_metrics("clf_fraud_v1", precision=0.75, recall=0.60)
    assert degraded["status"] == "MODEL_REGRESSION_DETECTED"
