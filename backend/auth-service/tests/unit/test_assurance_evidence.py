import pytest
from app.services.assurance_fabric.control_validation_engine import ControlValidationEngine

def test_assurance_evidence():
    engine = ControlValidationEngine()
    res = engine.execute_validation("ctl_1", "TEST_EVIDENCE", "OK", "OK", has_evidence=True)
    assert res.evidence_hash.startswith("sha256_")
    assert "TEST_EVIDENCE" in res.evidence_details
