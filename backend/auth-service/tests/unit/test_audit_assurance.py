import pytest
from app.services.assurance.security_invariant_engine import SecurityInvariantEngine


def test_audit_assurance_immutability():
    engine = SecurityInvariantEngine()
    invariants = engine.evaluate_invariants()

    audit_inv = next(i for i in invariants if i.invariant_id == "inv_audit_01")
    assert audit_inv.is_satisfied is True
    assert audit_inv.evidence["broken_hashes_count"] == 0
