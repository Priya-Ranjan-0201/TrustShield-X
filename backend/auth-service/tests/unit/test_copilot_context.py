import pytest
from app.services.copilot.copilot_context_builder import CopilotContextBuilder


def test_copilot_context_role_adaptation():
    builder = CopilotContextBuilder()

    ciso_ctx = builder.build_context("tenant_1", "usr_ciso", "CISO")
    assert "copilot.report" in ciso_ctx.permissions

    hunter_ctx = builder.build_context("tenant_1", "usr_hunter", "HUNTER")
    assert "copilot.hunt" in hunter_ctx.permissions
