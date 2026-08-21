import pytest
from app.services.assurance_fabric.control_validation_engine import ControlValidationEngine

def test_assurance_audit():
    engine = ControlValidationEngine()
    res = engine.execute_validation("ctl_audit", "AUDIT_CHAIN_TEST", "CHAIN_VALID", "CHAIN_VALID", has_evidence=True)
    assert res.evidence_hash.startswith("sha256_")
