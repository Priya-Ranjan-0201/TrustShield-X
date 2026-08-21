import pytest
from app.services.cyber_digital_twin.attack_path_prediction_engine import AttackPathPredictionEngine

def test_ai_predicted_attack_path_unverified():
    engine = AttackPathPredictionEngine()
    pred = engine.predict_attack_paths("AI-PRED-01", "t1", "WEB", "DB")
    assert pred["status"] == "PREDICTED_ATTACK_PATH"
    assert pred["is_hypothetical"] is True
