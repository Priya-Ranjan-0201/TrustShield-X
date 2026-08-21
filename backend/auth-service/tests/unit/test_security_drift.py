import pytest
from app.services.assurance_fabric.security_drift_engine import SecurityDriftEngine
from app.services.assurance.security_drift_engine import SecurityDriftEngine as AssuranceDriftEngine

def test_phase24_security_drift():
    engine = SecurityDriftEngine()
    drifts = engine.list_drifts()
    assert len(drifts) >= 1
    d = engine.detect_drift("CONFIGURATION", "firewall_rule", "Port 22 opened unexpectedly")
    assert d.is_reconciled is False
    rec = engine.reconcile_drift(d.drift_id)
    assert rec.is_reconciled is True

def test_legacy_security_drift():
    engine = AssuranceDriftEngine()
    assert engine is not None
