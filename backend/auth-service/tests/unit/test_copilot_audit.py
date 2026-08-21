import pytest
from app.services.copilot.copilot_tool_registry import CopilotToolRegistry


def test_copilot_tool_execution_audit_logging():
    registry = CopilotToolRegistry()

    call = registry.execute_tool(
        tool_id="tool_evidence_search",
        arguments={"query": "pcap"},
        user_permissions=["copilot.query"],
        tenant_id="tenant_audit",
        user_id="usr_analyst_01",
    )

    assert call.call_id.startswith("call_")
    assert call.tenant_id == "tenant_audit"
    assert call.is_authorized is True
    assert len(registry._calls) >= 1
