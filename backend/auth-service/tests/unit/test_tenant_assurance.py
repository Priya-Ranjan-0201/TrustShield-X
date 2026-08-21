import pytest
from app.services.assurance.security_invariant_engine import SecurityInvariantEngine


def test_tenant_isolation_assurance():
    engine = SecurityInvariantEngine()
    invariants = engine.evaluate_invariants()

    iso_inv = next(i for i in invariants if i.invariant_id == "inv_iso_01")
    assert iso_inv.is_satisfied is True
    assert iso_inv.evidence["leakage_count"] == 0
