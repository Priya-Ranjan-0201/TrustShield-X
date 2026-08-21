"""
TruthShield X — Intelligence Dispute & Feedback Engine (Phase 16).

Handles tenant dispute submissions against false positive or outdated indicators,
manages review workflows, and updates indicator status accordingly.
"""

from typing import Dict, List, Optional
from datetime import datetime, timezone
import uuid

from app.schemas.collective_defense_models import (
    IntelligenceDisputeDTO,
    DisputeStatusLiteral,
)


class IntelligenceDisputeEngine:
    """Manages indicator dispute lifecycle and feedback processing."""

    def __init__(self):
        self._disputes: Dict[str, IntelligenceDisputeDTO] = {}

    def submit_dispute(
        self,
        intelligence_id: str,
        tenant_id: str,
        dispute_type: str,
        reason: str,
        evidence: str,
    ) -> IntelligenceDisputeDTO:
        """Submits a new dispute against an intelligence indicator."""
        dispute = IntelligenceDisputeDTO(
            intelligence_id=intelligence_id,
            submitter_tenant_id=tenant_id,
            dispute_type=dispute_type,  # type: ignore
            reason=reason,
            evidence_submission=evidence,
            status="OPEN",
        )
        self._disputes[dispute.dispute_id] = dispute
        return dispute

    def resolve_dispute(
        self,
        dispute_id: str,
        resolution: str,
        status: DisputeStatusLiteral = "RESOLVED",
        reviewer_notes: Optional[str] = None,
    ) -> Optional[IntelligenceDisputeDTO]:
        """Resolves an open dispute."""
        dispute = self._disputes.get(dispute_id)
        if not dispute:
            return None

        dispute.status = status
        dispute.resolution = resolution
        dispute.reviewer_notes = reviewer_notes
        dispute.resolved_at = datetime.now(timezone.utc).isoformat()
        return dispute

    def get_dispute(self, dispute_id: str) -> Optional[IntelligenceDisputeDTO]:
        return self._disputes.get(dispute_id)

    def list_disputes_for_indicator(self, intelligence_id: str) -> List[IntelligenceDisputeDTO]:
        return [d for d in self._disputes.values() if d.intelligence_id == intelligence_id]

    def list_all_disputes(self) -> List[IntelligenceDisputeDTO]:
        return list(self._disputes.values())
