import pytest
from app.services.assurance.security_invariant_engine import SecurityInvariantEngine


def test_governance_authorization_precedence():
    engine = SecurityInvariantEngine()
    invariants = engine.evaluate_invariants()

    deny_inv = next(i for i in invariants if i.invariant_id == "inv_deny_01")
    assert deny_inv.is_satisfied is True
