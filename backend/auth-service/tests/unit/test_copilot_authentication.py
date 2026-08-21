import pytest
from app.services.copilot.copilot_context_builder import CopilotContextBuilder


def test_copilot_authentication_and_identity_context():
    builder = CopilotContextBuilder()
    ctx = builder.build_context(
        tenant_id="tenant_bank_01",
        user_id="usr_analyst_smith",
        role="ANALYST",
    )

    assert ctx.tenant_id == "tenant_bank_01"
    assert ctx.user_id == "usr_analyst_smith"
    assert ctx.user_role == "ANALYST"
    assert "copilot.read" in ctx.permissions
