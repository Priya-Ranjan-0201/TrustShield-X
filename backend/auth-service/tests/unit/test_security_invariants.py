import pytest
from app.services.assurance.security_invariant_engine import SecurityInvariantEngine


def test_security_invariants_evaluation():
    engine = SecurityInvariantEngine()
    invariants = engine.evaluate_invariants()

    assert len(invariants) >= 5
    for inv in invariants:
        assert inv.is_satisfied is True
        assert inv.criticality in ("HIGH", "CRITICAL")
        assert len(inv.evidence) >= 1
