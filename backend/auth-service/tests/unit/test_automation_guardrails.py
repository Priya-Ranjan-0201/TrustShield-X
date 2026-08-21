import pytest
from app.services.soc.automation_guardrails_engine import AutomationGuardrailsEngine


def test_automation_guardrails_circuit_breaker():
    engine = AutomationGuardrailsEngine()
    g = engine.get_guardrails("tenant_cb")
    assert g.circuit_breaker_tripped is False

    engine.pause_automation("tenant_cb", "usr_lead", "Anomaly surge detected")
    g_paused = engine.get_guardrails("tenant_cb")
    assert g_paused.circuit_breaker_tripped is True
    assert g_paused.is_paused is True
