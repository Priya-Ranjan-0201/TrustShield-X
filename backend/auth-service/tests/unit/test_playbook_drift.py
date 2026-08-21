import pytest
from app.services.assurance_fabric.security_drift_engine import SecurityDriftEngine

def test_playbook_drift():
    engine = SecurityDriftEngine()
    d = engine.detect_drift("PLAYBOOK", "pb_isolate_host", "Approval gate bypassed in yaml")
    assert d.drift_type == "PLAYBOOK"
