import pytest
from app.services.assurance_fabric.security_drift_engine import SecurityDriftEngine

def test_recovery_drift():
    engine = SecurityDriftEngine()
    d = engine.detect_drift("RECOVERY", "dr_postgres_plan", "Missing replica sync in failover")
    assert d.drift_type == "RECOVERY"
