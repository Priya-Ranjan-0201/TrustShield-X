"""
TruthShield X — Adaptive Security Policy Engine (Phase 30).

Recommends policy tuning while strictly enforcing non-negotiable safety constraints (authentication, tenant isolation, encryption).
"""

from typing import Dict, List, Optional, Any
from app.schemas.autonomous_defense_models import AdaptivePolicyDTO


class AdaptiveSecurityPolicyEngine:
    """Adapts defensive security policies without permitting automated downgrades to critical protections."""

    def __init__(self):
        self._policies: Dict[str, AdaptivePolicyDTO] = {}
        self._seed_default_policies()

    def _seed_default_policies(self):
        p1 = AdaptivePolicyDTO(
            policy_id="pol_dynamic_rate_limit",
            name="Dynamic Ingress WAF Rate Limiting Policy",
            risk_score=0.15,
            is_weakened=False,
            status="ACTIVE",
        )
        self._policies[p1.policy_id] = p1

    def propose_policy_change(
        self,
        policy_id: str,
        name: str,
        modifies_auth: bool = False,
        modifies_tenant_isolation: bool = False,
        modifies_encryption: bool = False,
    ) -> Dict[str, Any]:
        # Safety Invariant: Never automatically weaken authentication, authorization, tenant isolation, or encryption
        if modifies_auth or modifies_tenant_isolation or modifies_encryption:
            dto = AdaptivePolicyDTO(
                policy_id=policy_id,
                name=name,
                risk_score=0.99,
                is_weakened=True,
                status="BLOCKED",
            )
            self._policies[policy_id] = dto
            return {
                "policy_id": policy_id,
                "status": "BLOCKED",
                "reason": "CRITICAL_POLICY_SAFETY_VIOLATION_AUTOMATED_WEAKENING_FORBIDDEN",
                "requires_manual_ciso_override": True,
            }

        dto = AdaptivePolicyDTO(
            policy_id=policy_id,
            name=name,
            risk_score=0.10,
            is_weakened=False,
            status="PENDING_APPROVAL",
        )
        self._policies[policy_id] = dto
        return {
            "policy_id": policy_id,
            "status": "PENDING_APPROVAL",
            "reason": "SAFE_POLICY_MODIFICATION_PROPOSED",
        }

    def list_policies(self) -> List[AdaptivePolicyDTO]:
        return list(self._policies.values())
