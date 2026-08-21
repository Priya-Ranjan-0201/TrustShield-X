import pytest
from app.services.copilot.copilot_tool_registry import CopilotToolRegistry


def test_copilot_tool_authorization_guards():
    registry = CopilotToolRegistry()

    # Hunter permission only
    res = registry.execute_tool(
        tool_id="tool_threat_hunt",
        arguments={"query": "SELECT 1;"},
        user_permissions=["copilot.hunt"],
    )
    assert res.is_authorized is True

    # Lacking hunt permission
    res_unauth = registry.execute_tool(
        tool_id="tool_threat_hunt",
        arguments={"query": "SELECT 1;"},
        user_permissions=["copilot.read"],
    )
    assert res_unauth.is_authorized is False
