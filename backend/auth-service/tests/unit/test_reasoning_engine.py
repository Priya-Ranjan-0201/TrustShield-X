import pytest
from app.services.knowledge_fabric.security_reasoning_engine import SecurityReasoningEngine


def test_security_reasoning_engine_synthesis():
    engine = SecurityReasoningEngine()

    trace = engine.generate_reasoning_trace(
        statement="Lateral movement possible via compromised service account.",
        supporting_evidence=["ev_token_theft_log"],
        relationships=["usr_admin_svc ACCESSES srv_checkout_production"],
        assumptions=["Token replay mitigation inactive"],
        confidence=0.86,
    )

    assert trace.conclusion_statement.startswith("Lateral movement possible")
    assert trace.confidence == 0.86
    assert trace.epistemic_status == "INFERENCE"
