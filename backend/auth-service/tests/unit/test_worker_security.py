import pytest
from app.services.soc.automation_guardrails_engine import AutomationGuardrailsEngine


def test_worker_security_execution_bounds():
    guardrails = AutomationGuardrailsEngine()
    g = guardrails.get_guardrails("tenant_worker")

    assert g.max_execution_depth == 10
    assert g.execution_timeout_seconds == 600
