import pytest
from app.services.assurance_fabric.security_assertion_engine import SecurityAssertionEngine
from app.services.knowledge_fabric.security_assertion_engine import SecurityAssertionEngine as KnowledgeAssertionEngine

def test_phase24_security_assertions():
    engine = SecurityAssertionEngine()
    assertions = engine.list_assertions()
    assert len(assertions) >= 2
    asrt = engine.get_assertion("asrt_tenant_isolation")
    assert asrt is not None
    assert asrt.acceptable_state == "ACCESS_DENIED_EXPLICIT"
    assert asrt.is_validated is True

def test_security_assertions_validation_states():
    engine = KnowledgeAssertionEngine()
    asrt = engine.create_assertion(
        statement="Database db_primary_users is isolated from internet egress.",
        supporting_evidence=["ev_firewall_rule_deny_all"],
        contradicting_evidence=[],
        confidence=0.98,
        status="VERIFIED",
    )
    assert asrt.status == "VERIFIED"
    assert asrt.confidence == 0.98
