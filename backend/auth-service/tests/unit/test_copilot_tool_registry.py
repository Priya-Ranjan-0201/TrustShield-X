import pytest
from app.services.copilot.copilot_tool_registry import CopilotToolRegistry


def test_copilot_tool_registry_definitions():
    registry = CopilotToolRegistry()
    tools = registry.list_tools()

    assert len(tools) >= 5
    tool_names = [t.name for t in tools]
    assert "evidence_search" in tool_names
    assert "simulate_defense" in tool_names
    assert "isolate_host" in tool_names
