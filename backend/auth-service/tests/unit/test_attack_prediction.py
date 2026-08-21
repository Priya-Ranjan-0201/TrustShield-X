import pytest
from app.services.cyber_digital_twin.attack_path_prediction_engine import AttackPathPredictionEngine

def test_attack_path_prediction():
    engine = AttackPathPredictionEngine()
    pred = engine.predict_attack_paths("PRED-01", "t1", "EXT-WEB", "CORE-VAULT", current_controls=["MFA", "FIREWALL"])
    assert pred["status"] == "PREDICTED_ATTACK_PATH"
    assert pred["is_hypothetical"] is True
    assert len(pred["predicted_next_steps"]) == 3
