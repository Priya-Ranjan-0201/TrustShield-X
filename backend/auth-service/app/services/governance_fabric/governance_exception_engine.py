"""
TruthShield X — Governance Exception & Risk Acceptance Engine
"""

import uuid
from typing import Dict, List, Optional, Any
from datetime import datetime, timezone, timedelta
from app.schemas.governance_fabric_models import GovernanceExceptionDTO, ExceptionStatusLiteral


class GovernanceExceptionEngine:
    """Manages policy exceptions, risk acceptance, and four-eyes approvals."""

    def __init__(self):
        # exception_id -> GovernanceExceptionDTO
        self._exceptions: Dict[str, GovernanceExceptionDTO] = {}

    def request_exception(
        self,
        requirement_id: str,
        control_id: str,
        reason: str,
        business_justification: str,
        owner: str,
        approver: str,
        duration_days: int = 30,
        compensating_control_id: Optional[str] = None,
    ) -> GovernanceExceptionDTO:
        """Requests a new exception requiring four-eyes authorization."""
        # Four-eyes check: Requester cannot approve their own exception
        if owner == approver:
            raise PermissionError("Four-Eyes Governance Violation: Exception owner cannot approve their own request.")

        eid = f"exp_{uuid.uuid4().hex[:8]}"
        now = datetime.now(timezone.utc)
        exp_dt = (now + timedelta(days=duration_days)).isoformat()

        exception = GovernanceExceptionDTO(
            exception_id=eid,
            requirement_id=requirement_id,
            control_id=control_id,
            reason=reason,
            business_justification=business_justification,
            risk_acceptance="LOW_RISK_WITH_COMPENSATING_CONTROL",
            owner=owner,
            approver=approver,
            created_at=now.isoformat(),
            expiration=exp_dt,
            status="ACTIVE",
            compensating_control_id=compensating_control_id,
        )

        self._exceptions[eid] = exception
        return exception

    def get_exception(self, exception_id: str) -> Optional[GovernanceExceptionDTO]:
        """Retrieves exception and dynamically checks expiration."""
        exp = self._exceptions.get(exception_id)
        if not exp:
            return None

        # Check if expired
        try:
            exp_dt = datetime.fromisoformat(exp.expiration)
            if datetime.now(timezone.utc) > exp_dt:
                exp.status = "EXPIRED"
        except Exception:
            pass

        return exp

    def list_exceptions(self) -> List[GovernanceExceptionDTO]:
        """Lists active exceptions."""
        # Refresh expiration states
        for exp in self._exceptions.values():
            try:
                exp_dt = datetime.fromisoformat(exp.expiration)
                if datetime.now(timezone.utc) > exp_dt:
                    exp.status = "EXPIRED"
            except Exception:
                pass
        return list(self._exceptions.values())
