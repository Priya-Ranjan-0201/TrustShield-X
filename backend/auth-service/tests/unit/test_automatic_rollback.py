import pytest
from app.services.autonomous_defense.rollback_engine import RollbackEngine

def test_automatic_rollback_logging():
    engine = RollbackEngine()
    rb = engine.execute_rollback("ctrl_waf", "Revert rate-limiting")
    assert rb.is_verified is True
    assert len(engine.list_rollbacks()) >= 1
