import pytest
from app.services.assurance.security_invariant_engine import SecurityInvariantEngine


def test_assurance_security_sandbox_invariants():
    engine = SecurityInvariantEngine()
    invariants = engine.evaluate_invariants()

    sim_inv = next(i for i in invariants if i.invariant_id == "inv_sim_01")
    assert sim_inv.is_satisfied is True
    assert sim_inv.evidence["production_writes_from_sim"] == 0
