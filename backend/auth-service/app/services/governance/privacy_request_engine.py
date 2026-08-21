"""Privacy Request & DPDP Rights Workflow Engine (Phase 4.0 Part 8 — Sections 40-41, 97).

Orchestrates data principal rights workflows with identity verification and legal hold barriers.
"""

from typing import List, Dict, Any, Optional
import uuid
from datetime import datetime, timezone
from app.schemas.governance_models import (
    PrivacyRequestDTO,
    PrivacyRequestTypeLiteral,
)
from app.services.governance.legal_hold_engine import LegalHoldEngine


class PrivacyRequestEngine:
    """Manages DPDP and GDPR data subject rights workflows."""

    def __init__(self, legal_hold_engine: Optional[LegalHoldEngine] = None):
        self._requests: Dict[str, PrivacyRequestDTO] = {}
        self.legal_hold_engine = legal_hold_engine or LegalHoldEngine()

    def submit_privacy_request(
        self,
        organization_id: str,
        data_principal_id: str,
        request_type: PrivacyRequestTypeLiteral,
        reason: str = "",
    ) -> PrivacyRequestDTO:
        req = PrivacyRequestDTO(
            organization_id=organization_id,
            data_principal_id=data_principal_id,
            request_type=request_type,
            reason=reason,
            status="PENDING",
        )
        self._requests[req.request_id] = req
        return req

    def process_privacy_request(
        self,
        request_id: str,
        actor_id: str,
        verify_identity: bool = True,
    ) -> PrivacyRequestDTO:
        req = self._requests.get(request_id)
        if not req:
            raise KeyError(f"Privacy request {request_id} not found.")

        req.identity_verified = verify_identity
        if not verify_identity:
            req.status = "REJECTED"
            return req

        # Check Legal Hold for data principal
        has_hold = self.legal_hold_engine.is_under_legal_hold(req.data_principal_id)
        req.legal_hold_checked = True

        if req.request_type == "DELETION" and has_hold:
            req.status = "REJECTED"
            req.reason = "Deletion rejected: Data principal records are subject to active legal hold."
            return req

        req.status = "COMPLETED"
        req.completed_at = datetime.now(timezone.utc).isoformat()
        return req

    def get_request(self, request_id: str) -> Optional[PrivacyRequestDTO]:
        return self._requests.get(request_id)

    def list_requests(self, organization_id: Optional[str] = None) -> List[PrivacyRequestDTO]:
        if organization_id:
            return [r for r in self._requests.values() if r.organization_id == organization_id]
        return list(self._requests.values())
