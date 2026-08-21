"""
TruthShield X — Remediation & Closed-Loop Verification Engine (Phase 24).

Orchestrates remediation workflows and enforces independent re-testing before certifying resolution.
"""

from typing import Dict, List, Optional
from datetime import datetime, timezone
from app.schemas.security_assurance_fabric_models import RemediationPlanDTO


class RemediationEngine:
    """Coordinates remediation plans and requires independent re-validation."""

    def __init__(self):
        self._plans: Dict[str, RemediationPlanDTO] = {}

    def create_remediation_plan(
        self,
        control_id: str,
        failure_reason: str,
        actions: List[str],
        root_cause_category: str = "ROOT_CAUSE",
    ) -> RemediationPlanDTO:
        dto = RemediationPlanDTO(
            control_id=control_id,
            failure_reason=failure_reason,
            root_cause_category=root_cause_category,  # type: ignore
            actions=actions,
            is_approved=False,
            execution_status="PENDING",
        )
        self._plans[dto.remediation_id] = dto
        return dto

    def approve_and_execute(self, remediation_id: str, approver_id: str) -> RemediationPlanDTO:
        plan = self._plans.get(remediation_id)
        if not plan:
            raise ValueError(f"Remediation plan '{remediation_id}' not found.")

        executed = RemediationPlanDTO(
            remediation_id=plan.remediation_id,
            control_id=plan.control_id,
            failure_reason=plan.failure_reason,
            root_cause_category=plan.root_cause_category,
            actions=plan.actions,
            is_approved=True,
            approver_id=approver_id,
            execution_status="EXECUTED",
        )
        self._plans[remediation_id] = executed
        return executed

    def revalidate_remediation(self, remediation_id: str, test_passed: bool) -> RemediationPlanDTO:
        plan = self._plans.get(remediation_id)
        if not plan:
            raise ValueError(f"Remediation plan '{remediation_id}' not found.")

        status = "REMEDIATED" if test_passed else "REMEDIATION_NOT_VERIFIED"
        updated = RemediationPlanDTO(
            remediation_id=plan.remediation_id,
            control_id=plan.control_id,
            failure_reason=plan.failure_reason,
            root_cause_category=plan.root_cause_category,
            actions=plan.actions,
            is_approved=plan.is_approved,
            approver_id=plan.approver_id,
            execution_status=status,  # type: ignore
            revalidated_at=datetime.now(timezone.utc).isoformat(),
        )
        self._plans[remediation_id] = updated
        return updated

    def get_plan(self, remediation_id: str) -> Optional[RemediationPlanDTO]:
        return self._plans.get(remediation_id)
