"""Approval Engine & Separation of Duties (Phase 4.0 Part 7 — Sections 34-36, 80).

Enforces four-eyes approval: the user requesting a destructive response action
MUST NOT be the same user who approves it.
"""

from typing import List, Dict, Any, Optional
import uuid
from datetime import datetime, timezone, timedelta
from app.schemas.soc_operations_models import (
    ApprovalRequestDTO,
    ResponseActionDTO,
    ApprovalStatusLiteral,
    IncidentSeverityLiteral,
)


class ApprovalPolicyViolationError(Exception):
    """Raised when an approval rule or separation-of-duties invariant is violated."""
    pass


class ApprovalEngine:
    """Manages authorization requests, four-eyes approval workflows, and status transitions."""

    def __init__(self):
        self._approvals: Dict[str, ApprovalRequestDTO] = {}

    def create_approval_request(
        self,
        action: ResponseActionDTO,
        requested_by: str,
        reason: str,
        risk: IncidentSeverityLiteral = "HIGH",
        expires_in_hours: int = 4,
    ) -> ApprovalRequestDTO:
        now = datetime.now(timezone.utc)
        expires_at = (now + timedelta(hours=expires_in_hours)).isoformat()

        approval = ApprovalRequestDTO(
            approval_id=f"appr_{uuid.uuid4().hex[:12]}",
            action_id=action.action_id,
            incident_id=action.incident_id,
            requested_by=requested_by,
            reason=reason,
            risk=risk,
            evidence=action.evidence_ids,
            expires_at=expires_at,
            status="PENDING",
        )
        self._approvals[approval.approval_id] = approval
        return approval

    def decide_approval(
        self,
        approval_id: str,
        approver_id: str,
        decision: ApprovalStatusLiteral,
        decision_reason: str,
        enforce_separation_of_duties: bool = True,
    ) -> ApprovalRequestDTO:
        approval = self._approvals.get(approval_id)
        if not approval:
            raise KeyError(f"Approval request {approval_id} not found.")

        # 1. Separation of duties check (Section 80, Mandatory Test 3)
        if enforce_separation_of_duties and approval.requested_by == approver_id:
            raise ApprovalPolicyViolationError(
                f"Separation of duties violation: Requesting user '{approval.requested_by}' "
                f"cannot self-approve action '{approval.action_id}'."
            )

        # 2. Expiration check
        now = datetime.now(timezone.utc)
        if datetime.fromisoformat(approval.expires_at) < now:
            approval.status = "EXPIRED"
            return approval

        approval.status = decision
        approval.decided_by = approver_id
        approval.decided_at = now.isoformat()
        approval.decision_reason = decision_reason
        return approval

    def get_approval(self, approval_id: str) -> Optional[ApprovalRequestDTO]:
        return self._approvals.get(approval_id)

    def list_approvals(self, status: Optional[ApprovalStatusLiteral] = None) -> List[ApprovalRequestDTO]:
        if status:
            return [a for a in self._approvals.values() if a.status == status]
        return list(self._approvals.values())
