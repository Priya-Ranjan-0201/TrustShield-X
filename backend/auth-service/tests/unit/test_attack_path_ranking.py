import pytest
from app.services.cyber_digital_twin.attack_path_prediction_engine import AttackPathPredictionEngine

def test_attack_path_ranking():
    engine = AttackPathPredictionEngine()
    paths = [
        {"id": "P1", "reachability_rank": 0.3, "risk_score": 3.0},
        {"id": "P2", "reachability_rank": 0.9, "risk_score": 9.0},
        {"id": "P3", "reachability_rank": 0.6, "risk_score": 6.0}
    ]
    ranked = engine.rank_attack_paths(paths)
    assert ranked[0]["id"] == "P2"
    assert ranked[2]["id"] == "P1"
