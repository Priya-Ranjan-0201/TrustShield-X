import pytest
from app.services.assurance_fabric.negative_testing_engine import NegativeTestingEngine

def test_negative_testing():
    engine = NegativeTestingEngine()
    t1 = engine.test_cross_tenant_isolation("tenant_a", "tenant_b")
    assert t1["passed"] is True
    assert t1["rejection_code"] == "403_FORBIDDEN"

    t2 = engine.test_four_eyes_bypass("usr_same", "usr_same")
    assert t2["passed"] is True
    assert t2["rejection_code"] == "FOUR_EYES_VIOLATION"
