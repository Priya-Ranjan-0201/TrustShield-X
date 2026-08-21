import pytest
from app.services.knowledge_fabric.security_assertion_engine import SecurityAssertionEngine


def test_governance_reasoning_compliance():
    engine = SecurityAssertionEngine()

    asrt = engine.create_assertion(
        statement="PCI-DSS Requirement 3.4 satisfied by AES-256-GCM column encryption.",
        supporting_evidence=["ev_kms_config_dump"],
        confidence=0.99,
        status="VERIFIED",
    )

    assert asrt.status == "VERIFIED"
    assert "PCI-DSS" in asrt.statement
