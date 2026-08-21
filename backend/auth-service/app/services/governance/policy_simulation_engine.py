"""Policy Simulation & Dry-Run Engine (Phase 4.0 Part 8 — Sections 24-26, 95).

Simulates policy changes and rule impacts without mutating production authorization state.
"""

from typing import List, Dict, Any, Optional
import uuid
from datetime import datetime, timezone
from app.schemas.governance_models import (
    GovernancePolicyDTO,
    PolicySimulationDTO,
    UserLifecycleDTO,
)
from app.services.governance.policy_engine import PolicyEngine


class PolicySimulationEngine:
    """Performs zero-side-effect simulations of draft governance policies."""

    @staticmethod
    def simulate_policy(
        policy: GovernancePolicyDTO,
        sample_users: Optional[List[UserLifecycleDTO]] = None,
        sample_resources: Optional[List[Dict[str, Any]]] = None,
    ) -> PolicySimulationDTO:
        users = sample_users or []
        resources = sample_resources or [
            {"resource": "incident", "action": "read"},
            {"resource": "incident", "action": "update"},
            {"resource": "response", "action": "execute"},
            {"resource": "report", "action": "export"},
            {"resource": "evidence", "action": "delete"},
        ]

        engine = PolicyEngine()
        conflicts = engine.detect_conflicts(policy.rules)

        new_denials = 0
        new_approvals = 0

        for rule in policy.rules:
            effect = rule.get("effect", "ALLOW")
            if effect == "DENY":
                new_denials += 1
            elif effect in ("REQUIRE_APPROVAL", "REQUIRE_TWO_PERSON_APPROVAL"):
                new_approvals += 1

        return PolicySimulationDTO(
            simulation_id=f"psim_{uuid.uuid4().hex[:12]}",
            policy_id=policy.policy_id,
            affected_users_count=len(users),
            affected_resources_count=len(resources),
            new_denials_count=new_denials,
            new_approvals_count=new_approvals,
            conflicts_detected=conflicts,
            simulation_verdict="SIMULATION_PASSED_ZERO_PRODUCTION_MUTATION",
        )
