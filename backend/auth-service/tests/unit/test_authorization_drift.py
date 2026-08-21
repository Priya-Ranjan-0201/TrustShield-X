import pytest
from app.services.assurance_fabric.security_drift_engine import SecurityDriftEngine

def test_authorization_drift():
    engine = SecurityDriftEngine()
    d = engine.detect_drift("AUTHORIZATION", "role_auditor", "Granted write permissions to auditor")
    assert d.drift_type == "AUTHORIZATION"
