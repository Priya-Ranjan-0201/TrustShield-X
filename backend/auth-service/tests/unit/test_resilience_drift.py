import pytest
from app.services.resilience.resilience_drift_engine import ResilienceDriftEngine

def test_resilience_drift():
    engine = ResilienceDriftEngine()
    drifts = engine.list_drifts()
    assert len(drifts) >= 1
    d = engine.record_drift("INFRASTRUCTURE", "New replica added", "Mark plan OUTDATED")
    assert d.is_reconciled is False
    rec = engine.reconcile_drift(d.drift_id)
    assert rec.is_reconciled is True
