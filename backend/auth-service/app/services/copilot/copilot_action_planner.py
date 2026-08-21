"""
TruthShield X — Copilot Action Planner (Phase 20).

Creates structured action plans requiring explicit multi-tier approval before any execution.
"""

from typing import Dict, List, Optional
from app.schemas.copilot_command_models import (
    CopilotActionPlanDTO,
    ActionStateLiteral,
)


class CopilotActionPlanner:
    """Manages action plan lifecycles, approval gates, and refusal justifications."""

    def __init__(self):
        self._plans: Dict[str, CopilotActionPlanDTO] = {}

    def create_plan(
        self,
        session_id: str,
        action_type: str,
        target_resource: str,
        reason: str,
        evidence_ids: List[str],
        expected_benefit: str,
        possible_impact: str,
        simulation_id: Optional[str] = None,
        rollback_steps: Optional[List[str]] = None,
    ) -> CopilotActionPlanDTO:
        plan = CopilotActionPlanDTO(
            session_id=session_id,
            action_type=action_type,
            target_resource=target_resource,
            reason=reason,
            evidence_ids=evidence_ids,
            expected_benefit=expected_benefit,
            possible_impact=possible_impact,
            simulation_id=simulation_id,
            rollback_steps=rollback_steps or ["Revert to previous security group state"],
            approval_status="APPROVAL_REQUIRED",
            required_approval_tier="TIER_2_FOUR_EYES",
        )
        self._plans[plan.plan_id] = plan
        return plan

    def approve_plan(self, plan_id: str, approver_id: str) -> Optional[CopilotActionPlanDTO]:
        """Approves a plan by authorized human operator."""
        plan = self._plans.get(plan_id)
        if not plan:
            return None

        approved = CopilotActionPlanDTO(
            plan_id=plan.plan_id,
            session_id=plan.session_id,
            action_type=plan.action_type,
            target_resource=plan.target_resource,
            reason=plan.reason,
            evidence_ids=plan.evidence_ids,
            expected_benefit=plan.expected_benefit,
            possible_impact=plan.possible_impact,
            simulation_id=plan.simulation_id,
            rollback_steps=plan.rollback_steps,
            approval_status="APPROVED",
            required_approval_tier=plan.required_approval_tier,
            created_at=plan.created_at,
        )
        self._plans[plan_id] = approved
        return approved

    def get_plan(self, plan_id: str) -> Optional[CopilotActionPlanDTO]:
        return self._plans.get(plan_id)
