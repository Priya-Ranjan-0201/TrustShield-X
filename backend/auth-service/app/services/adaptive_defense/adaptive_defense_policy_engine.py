"""
TruthShield X — Adaptive Defense Policy Engine (Phase 17).

Evaluates ABAC/RBAC defense policies with deterministic explicit DENY override rules.
"""

from typing import Dict, List, Optional, Any
from app.schemas.adaptive_defense_models import (
    AdaptiveControlRecommendationDTO,
    ActionClassificationLiteral,
)


class AdaptiveDefensePolicyEngine:
    """Policy decision point for autonomous and human-approved defense adaptations."""

    def __init__(self):
        self._explicit_denials: List[Dict[str, Any]] = []

    def add_explicit_deny(self, match_type: str, match_value: str, reason: str):
        """Registers an explicit DENY override rule."""
        self._explicit_denials.append({
            "type": match_type.upper(),
            "value": match_value.lower(),
            "reason": reason,
        })

    def evaluate_action_policy(
        self,
        recommendation: AdaptiveControlRecommendationDTO,
        actor_roles: Optional[List[str]] = None,
        has_human_approval: bool = False,
    ) -> Dict[str, Any]:
        """Evaluates whether an adaptive action may proceed."""
        # 1. Explicit DENY check (Section 17, 70)
        target_lower = recommendation.target_resource.lower()
        for d in self._explicit_denials:
            if d["type"] == "TARGET" and d["value"] in target_lower:
                return {
                    "decision": "BLOCKED",
                    "reason": f"Explicit Deny: {d['reason']}",
                    "requires_approval": False,
                }
            if d["type"] == "TENANT" and d["value"] == recommendation.tenant_id.lower():
                return {
                    "decision": "BLOCKED",
                    "reason": f"Explicit Tenant Deny: {d['reason']}",
                    "requires_approval": False,
                }

        # 2. Check Automation Level & Human Approval Requirements
        if recommendation.automation_level == "LEVEL_2_HUMAN_APPROVAL" and not has_human_approval:
            return {
                "decision": "APPROVAL_REQUIRED",
                "reason": "High-impact action requires Four-Eyes human authorization.",
                "requires_approval": True,
            }

        if recommendation.action_classification in ("ASSET_ISOLATION", "SERVICE_CONTROL") and not has_human_approval:
            return {
                "decision": "APPROVAL_REQUIRED",
                "reason": f"{recommendation.action_classification} requires explicit human sign-off.",
                "requires_approval": True,
            }

        # 3. Permitted Execution
        return {
            "decision": "EXECUTE_ALLOWED",
            "reason": "Policy requirements satisfied.",
            "requires_approval": False,
        }
