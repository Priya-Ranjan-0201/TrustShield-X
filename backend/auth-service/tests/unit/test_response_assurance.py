import pytest
from app.services.assurance.security_invariant_engine import SecurityInvariantEngine


def test_response_assurance_gate():
    engine = SecurityInvariantEngine()
    invariants = engine.evaluate_invariants()

    resp_inv = next(i for i in invariants if i.invariant_id == "inv_resp_01")
    assert resp_inv.is_satisfied is True
    assert resp_inv.evidence["unauthorized_executions"] == 0
