import pytest
from app.services.soc.automation_guardrails_engine import AutomationGuardrailsEngine


def test_policy_enforcement_max_execution_depth():
    guardrails = AutomationGuardrailsEngine()

    # Allowed depth
    assert guardrails.is_action_permitted("tenant_1", depth=3) is True

    # Exceeds max depth (10)
    assert guardrails.is_action_permitted("tenant_1", depth=15) is False
