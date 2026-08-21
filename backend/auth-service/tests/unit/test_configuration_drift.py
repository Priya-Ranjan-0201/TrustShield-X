import pytest
from app.services.assurance_fabric.security_drift_engine import SecurityDriftEngine

def test_configuration_drift():
    engine = SecurityDriftEngine()
    d = engine.detect_drift("CONFIGURATION", "tls_version", "TLS 1.0 enabled on legacy endpoint")
    assert d.drift_type == "CONFIGURATION"
    assert d.is_reconciled is False
