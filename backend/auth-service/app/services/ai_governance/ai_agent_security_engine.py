"""
TruthShield X — AI Agent Security Engine (Phase 31).

Restricts autonomous AI agent execution within least-privilege boundaries and applies circuit breakers against runaway loops.
"""

from typing import Dict, List, Optional, Any
from app.schemas.ai_security_governance_models import AIAgentDTO


class AIAgentSecurityEngine:
    """Manages AI agent permissions, execution loops, and sandboxing."""

    def __init__(self):
        self._agents: Dict[str, AIAgentDTO] = {}
        self._seed_default_agent()

    def _seed_default_agent(self):
        a1 = AIAgentDTO(
            agent_id="agt_soc_investigator",
            name="Autonomous SOC Evidence Collector Agent",
            purpose="Automated gathering of threat telemetry across endpoints",
            allowed_tools=["query_telemetry", "get_asset_exposure"],
            permissions=["telemetry:read", "exposure:read"],
            autonomy_level="LEVEL_2",
            tenant_id="default_tenant",
            owner="SOC_LEAD",
            status="ACTIVE",
        )
        self._agents[a1.agent_id] = a1

    def validate_agent_execution(
        self,
        agent_id: str,
        tool_name: str,
        iteration_count: int = 1,
    ) -> Dict[str, Any]:
        agent = self._agents.get(agent_id)
        if not agent:
            raise ValueError(f"Agent '{agent_id}' not found.")

        # 1. Loop Protection / Circuit Breaker
        if iteration_count > 10:
            return {
                "agent_id": agent_id,
                "allowed": False,
                "status": "CIRCUIT_BREAKER_TRIGGERED",
                "reason": f"ITERATION_LIMIT_{iteration_count}_EXCEEDED",
            }

        # 2. Tool allowlist check
        if tool_name not in agent.allowed_tools:
            return {
                "agent_id": agent_id,
                "allowed": False,
                "status": "TOOL_NOT_AUTHORIZED",
                "reason": f"TOOL_{tool_name}_NOT_IN_ALLOWLIST",
            }

        return {
            "agent_id": agent_id,
            "allowed": True,
            "status": "AGENT_ACTION_AUTHORIZED",
            "reason": "WITHIN_PERMISSION_BOUNDARIES",
        }

    def list_agents(self) -> List[AIAgentDTO]:
        return list(self._agents.values())
