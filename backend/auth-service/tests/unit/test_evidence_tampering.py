import pytest
from app.services.assurance_fabric.negative_testing_engine import NegativeTestingEngine

def test_evidence_tampering():
    engine = NegativeTestingEngine()
    tamper = engine.test_audit_tampering_resistance("abc123hash", "def456hash")
    assert tamper["passed"] is True
    assert "TAMPER_DETECTED" in tamper["verdict"]
