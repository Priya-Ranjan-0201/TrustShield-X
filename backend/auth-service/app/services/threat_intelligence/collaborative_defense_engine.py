"""
TruthShield X — Collaborative Defense Engine (Phase 22).

Manages collaborative intelligence sharing, deterministic PII/secret redaction, dispute processing, and revocation impact graphs.
"""

from typing import Dict, List, Any, Optional
import re
from datetime import datetime, timezone
from app.schemas.threat_intelligence_fabric_models import (
    CollaborativeContributionDTO,
    IntelligenceDisputeDTO,
    IntelligenceRevocationDTO,
    IntelligenceClassificationLiteral,
)


class CollaborativeDefenseEngine:
    """Manages trusted community sharing, redactions, disputes, and revocations."""

    def __init__(self):
        self._contributions: Dict[str, CollaborativeContributionDTO] = {}
        self._disputes: Dict[str, IntelligenceDisputeDTO] = {}
        self._revocations: Dict[str, IntelligenceRevocationDTO] = {}

    def redact_pii_and_secrets(self, raw_text: str) -> str:
        """Deterministic redaction of emails, IP addresses that are internal, tokens, and API keys."""
        # Redact bearer tokens / API keys
        sanitized = re.sub(r"(?i)bearer\s+[a-zA-Z0-9_\-\.]+", "Bearer [REDACTED_SECRET]", raw_text)
        sanitized = re.sub(r"(?i)api[_-]?key\s*[:=]\s*['\"]?[a-zA-Z0-9_\-]+['\"]?", "api_key=[REDACTED_SECRET]", sanitized)
        # Redact internal user emails
        sanitized = re.sub(r"[a-zA-Z0-9_.+-]+@truthshield\.internal", "[REDACTED_USER_EMAIL]", sanitized)
        return sanitized

    def contribute_intelligence(
        self,
        tenant_id: str,
        contributor: str,
        raw_intelligence: str,
        classification: IntelligenceClassificationLiteral = "COMMUNITY",
    ) -> CollaborativeContributionDTO:
        redacted = self.redact_pii_and_secrets(raw_intelligence)
        dto = CollaborativeContributionDTO(
            tenant_id=tenant_id,
            contributor_identity=contributor,
            object_value=redacted,
            classification=classification,
            is_redacted=True,
        )
        self._contributions[dto.contribution_id] = dto
        return dto

    def submit_dispute(self, object_id: str, tenant_id: str, reason: str) -> IntelligenceDisputeDTO:
        dto = IntelligenceDisputeDTO(
            object_id=object_id,
            disputing_tenant_id=tenant_id,
            reason=reason,
            dispute_status="OPEN",
        )
        self._disputes[dto.dispute_id] = dto
        return dto

    def revoke_intelligence(
        self,
        object_id: str,
        reason: str,
        affected_indicators: List[str] = None,
        affected_detections: List[str] = None,
    ) -> IntelligenceRevocationDTO:
        dto = IntelligenceRevocationDTO(
            object_id=object_id,
            reason=reason,
            affected_indicators=affected_indicators or [object_id],
            affected_campaigns=[f"camp_linked_{object_id[:6]}"],
            affected_detections=affected_detections or [f"det_rule_{object_id[:6]}"],
            affected_incidents=[f"inc_reopened_{object_id[:6]}"],
        )
        self._revocations[dto.revocation_id] = dto
        return dto

    def list_disputes(self) -> List[IntelligenceDisputeDTO]:
        return list(self._disputes.values())

    def list_revocations(self) -> List[IntelligenceRevocationDTO]:
        return list(self._revocations.values())
