"""Response Policy & Automation Governance Engine (Phase 4.0 Part 7 — Sections 52-54).

Enforces automation boundaries and determines whether human authorization is required.
"""

from typing import List, Dict, Any, Optional
from app.schemas.soc_operations_models import (
    ResponsePolicyDTO,
    ResponseActionDTO,
    SecurityIncidentDTO,
    AutomationLevelLiteral,
    ActionTypeLiteral,
)

HIGH_IMPACT_ACTIONS = {
    "BLOCK_DOMAIN",
    "BLOCK_IP",
    "BLOCK_URL",
    "QUARANTINE_FILE",
    "ISOLATE_DEVICE",
    "DISABLE_ACCOUNT",
    "REVOKE_TOKEN",
    "REVOKE_SESSION",
    "RESET_CREDENTIAL",
    "DISABLE_APPLICATION",
    "UPDATE_FIREWALL_RULE",
    "ADD_WAF_RULE",
}


class ResponsePolicyEngine:
    """Evaluates organization response policies to determine automation eligibility."""

    def __init__(self):
        self._policies: Dict[str, ResponsePolicyDTO] = {}

    def register_policy(self, policy: ResponsePolicyDTO) -> None:
        self._policies[policy.policy_id] = policy

    def evaluate_action_policy(
        self,
        action_type: ActionTypeLiteral,
        incident: SecurityIncidentDTO,
    ) -> AutomationLevelLiteral:
        """Determines automation level for an action under an incident."""
        # Find matching policy
        for pol in self._policies.values():
            if pol.action_type == action_type:
                return pol.automation_level

        # Mandatory Default (Sections 32, 53, Mandatory Test 2): High-impact actions require approval by default
        if action_type in HIGH_IMPACT_ACTIONS:
            return "APPROVAL_REQUIRED"

        return "AUTOMATIC_ALLOWED"
