import pytest
from app.services.copilot.copilot_tool_registry import CopilotToolRegistry


def test_copilot_authorization_tool_invocation():
    registry = CopilotToolRegistry()

    # Analyst lacks action execution permission
    call_denied = registry.execute_tool(
        tool_id="tool_isolate_host",
        arguments={"target": "srv_db_prod"},
        user_permissions=["copilot.read", "copilot.query"],
    )
    assert call_denied.is_authorized is False
    assert call_denied.result["status"] == "DENIED"

    # Admin with action permission succeeds
    call_granted = registry.execute_tool(
        tool_id="tool_isolate_host",
        arguments={"target": "srv_db_prod"},
        user_permissions=["copilot.action"],
    )
    assert call_granted.is_authorized is True
    assert call_granted.result["status"] == "SUCCESS"
