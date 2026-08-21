"""
TruthShield X — Copilot Context Builder (Phase 20).

Constructs role-aware, tenant-isolated execution context with permission enforcement.
"""

from typing import Dict, List, Optional, Any
from app.schemas.copilot_command_models import (
    CopilotContextDTO,
    CopilotRoleLiteral,
)


class CopilotContextBuilder:
    """Builds authorized session context for Copilot requests."""

    def __init__(self):
        self._role_permissions: Dict[CopilotRoleLiteral, List[str]] = {
            "ANALYST": ["copilot.read", "copilot.query", "copilot.investigate"],
            "HUNTER": ["copilot.read", "copilot.query", "copilot.hunt"],
            "INCIDENT_RESPONDER": ["copilot.read", "copilot.query", "copilot.investigate", "copilot.recommend"],
            "ENGINEER": ["copilot.read", "copilot.query", "copilot.simulate", "copilot.action"],
            "GOVERNANCE": ["copilot.read", "copilot.query", "copilot.report"],
            "ADMIN": ["copilot.read", "copilot.query", "copilot.investigate", "copilot.hunt", "copilot.simulate", "copilot.action", "copilot.admin"],
            "CISO": ["copilot.read", "copilot.query", "copilot.report", "copilot.recommend"],
            "EXECUTIVE": ["copilot.read", "copilot.query", "copilot.report"],
        }

    def build_context(
        self,
        tenant_id: str,
        user_id: str,
        role: CopilotRoleLiteral = "ANALYST",
        incident_id: Optional[str] = None,
        asset_id: Optional[str] = None,
        campaign_id: Optional[str] = None,
        environment: str = "PRODUCTION",
    ) -> CopilotContextDTO:
        perms = self._role_permissions.get(role, ["copilot.read", "copilot.query"])
        return CopilotContextDTO(
            tenant_id=tenant_id,
            user_id=user_id,
            user_role=role,
            permissions=perms,
            current_incident=incident_id,
            selected_asset=asset_id,
            selected_campaign=campaign_id,
            environment=environment,
            relevant_policies=["POL_SEC_DEFAULT_DENY", "POL_SEC_FOUR_EYES"],
            relevant_evidence=["ev_pcap_trace_88", "ev_vuln_scan_44"],
        )
