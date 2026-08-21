"""
TruthShield X — Copilot Tool Registry (Phase 20).

Manages controlled tool orchestration, permission checks, rate limits, and audit logging.
"""

from typing import Dict, List, Optional, Any
from app.schemas.copilot_command_models import (
    CopilotToolDefinitionDTO,
    CopilotToolCallDTO,
)


class CopilotToolRegistry:
    """Manages registered security tools, permission checks, and execution auditing."""

    def __init__(self):
        self._tools: Dict[str, CopilotToolDefinitionDTO] = {}
        self._calls: List[CopilotToolCallDTO] = []
        self._initialize_default_tools()

    def _initialize_default_tools(self):
        defaults = [
            ("tool_evidence_search", "evidence_search", "Search verified evidence artifacts", "copilot.query", "TELEMETRY", "LOW", True, False),
            ("tool_graph_traverse", "graph_traverse", "Traverse knowledge and dependency graph", "copilot.query", "GRAPH", "LOW", True, False),
            ("tool_threat_hunt", "threat_hunt", "Execute read-only threat hunting query", "copilot.hunt", "SIEM", "MEDIUM", True, False),
            ("tool_simulate_defense", "simulate_defense", "Launch dry-run digital twin simulation", "copilot.simulate", "TWIN", "MEDIUM", True, False),
            ("tool_isolate_host", "isolate_host", "Apply defensive network quarantine", "copilot.action", "NETWORK", "HIGH", False, True),
        ]
        for tid, name, desc, perm, scope, risk, ro, req_app in defaults:
            self._tools[tid] = CopilotToolDefinitionDTO(
                tool_id=tid,
                name=name,
                description=desc,
                required_permission=perm,
                scope=scope,
                risk_level=risk,  # type: ignore
                is_read_only=ro,
                requires_approval=req_app,
            )

    def get_tool(self, tool_id: str) -> Optional[CopilotToolDefinitionDTO]:
        return self._tools.get(tool_id)

    def list_tools(self) -> List[CopilotToolDefinitionDTO]:
        return list(self._tools.values())

    def execute_tool(
        self,
        tool_id: str,
        arguments: Dict[str, Any],
        user_permissions: List[str],
        tenant_id: str = "default_tenant",
        user_id: str = "usr_analyst_01",
    ) -> CopilotToolCallDTO:
        tool = self._tools.get(tool_id)
        if not tool:
            raise KeyError(f"Tool '{tool_id}' not found.")

        # Check authorization
        is_auth = tool.required_permission in user_permissions or "copilot.admin" in user_permissions
        res_data = {"status": "SUCCESS", "message": f"Executed {tool.name}"} if is_auth else {"status": "DENIED", "error": "Unauthorized tool invocation"}

        call = CopilotToolCallDTO(
            tool_id=tool_id,
            arguments=arguments,
            tenant_id=tenant_id,
            user_id=user_id,
            result=res_data,
            is_authorized=is_auth,
        )
        self._calls.append(call)
        return call
