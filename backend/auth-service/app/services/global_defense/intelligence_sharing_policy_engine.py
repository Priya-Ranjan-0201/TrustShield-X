"""
TruthShield X — Intelligence Sharing Policy Engine (Phase 28).

Evaluates granular sharing policies, data classification bounds, and authorization with explicit DENY overrides.
"""

from typing import Dict, List, Any
from app.schemas.global_defense_models import IntelligenceSharingPolicyDTO, DataClassificationLiteral


class IntelligenceSharingPolicyEngine:
    """Enforces fine-grained data classification and sharing authorization policies."""

    def __init__(self):
        self._policies: Dict[str, IntelligenceSharingPolicyDTO] = {}
        self._seed_default_policy()

    def _seed_default_policy(self):
        p1 = IntelligenceSharingPolicyDTO(
            policy_id="pol_strict_sanitized_share",
            tenant_id="default_tenant",
            allowed_classifications=["PUBLIC", "INTERNAL", "CONFIDENTIAL"],
            auto_sanitize=True,
            requires_four_eyes=True,
            sharing_purposes=["THREAT_DEFENSE", "INCIDENT_MITIGATION"],
            recipients=["tenant_finance_alpha", "tenant_cloud_beta"],
        )
        self._policies[p1.policy_id] = p1

    def evaluate_sharing(
        self,
        tenant_id: str,
        recipient: str,
        classification: DataClassificationLiteral,
        purpose: str,
    ) -> Dict[str, Any]:
        # Search for tenant policy
        policy = next((p for p in self._policies.values() if p.tenant_id == tenant_id), None)
        if not policy:
            return {
                "decision": "SHARING_BLOCKED",
                "allowed": False,
                "reason": f"No active sharing policy found for tenant {tenant_id}",
            }

        # Check classification
        if classification not in policy.allowed_classifications:
            return {
                "decision": "SHARING_BLOCKED",
                "allowed": False,
                "reason": f"Data classification {classification} exceeds allowed threshold {policy.allowed_classifications}",
            }

        # Check recipient
        if recipient not in policy.recipients and "ALL_AUTHORIZED_NETWORK_MEMBERS" not in policy.recipients:
            return {
                "decision": "SHARING_BLOCKED",
                "allowed": False,
                "reason": f"Recipient {recipient} is not authorized by policy {policy.policy_id}",
            }

        # Check purpose
        if purpose not in policy.sharing_purposes:
            return {
                "decision": "SHARING_BLOCKED",
                "allowed": False,
                "reason": f"Purpose {purpose} is not approved in policy {policy.policy_id}",
            }

        return {
            "decision": "APPROVED",
            "allowed": True,
            "policy_id": policy.policy_id,
            "requires_four_eyes": policy.requires_four_eyes,
            "auto_sanitize": policy.auto_sanitize,
        }
