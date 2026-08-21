import pytest
from app.services.autonomous_defense.rollback_engine import RollbackEngine

def test_model_rollback_verified():
    engine = RollbackEngine()
    rb = engine.execute_rollback("mdl_c2_neural_classifier", "Revert to v2.0.0")
    assert rb.is_verified is True
