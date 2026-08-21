"""Data Retention & Lifecycle Governance Engine (Phase 4.0 Part 8 — Sections 31-33, 96).

Evaluates data retention schedules and enforces legal hold preservation rules.
"""

from typing import List, Dict, Any, Optional
from datetime import datetime, timezone, timedelta
from app.schemas.governance_models import (
    RetentionPolicyDTO,
    RetentionStateLiteral,
    DataClassificationLiteral,
)
from app.services.governance.legal_hold_engine import LegalHoldEngine


class DataRetentionEngine:
    """Manages organization retention policies and evaluates resource lifecycle states."""

    def __init__(self, legal_hold_engine: Optional[LegalHoldEngine] = None):
        self._policies: Dict[str, RetentionPolicyDTO] = {}
        self.legal_hold_engine = legal_hold_engine or LegalHoldEngine()

    def set_retention_policy(
        self,
        organization_id: str,
        resource_type: str,
        retention_period_days: int = 365,
        classification: DataClassificationLiteral = "INTERNAL",
        deletion_strategy: str = "SOFT_DELETE",
    ) -> RetentionPolicyDTO:
        policy = RetentionPolicyDTO(
            organization_id=organization_id,
            resource_type=resource_type,
            classification=classification,
            retention_period_days=retention_period_days,
            deletion_strategy=deletion_strategy,
        )
        self._policies[f"{organization_id}:{resource_type}"] = policy
        return policy

    def evaluate_resource_retention_state(
        self,
        organization_id: str,
        resource_type: str,
        resource_id: str,
        created_at: datetime,
    ) -> RetentionStateLiteral:
        """Section 35, Mandatory Test 8, 15: Legal hold ALWAYS overrides automated retention deletion."""
        # 1. Legal Hold Check (Highest Precedence)
        if self.legal_hold_engine.is_under_legal_hold(resource_id):
            return "LEGAL_HOLD"

        # 2. Retention Schedule Check
        policy = self._policies.get(f"{organization_id}:{resource_type}")
        retention_days = policy.retention_period_days if policy else 365

        now = datetime.now(timezone.utc)
        if created_at.tzinfo is None:
            created_at = created_at.replace(tzinfo=timezone.utc)

        age_days = (now - created_at).total_seconds() / 86400.0
        if age_days >= retention_days:
            return "DUE_FOR_DELETION"

        if age_days >= (retention_days * 0.75):
            return "DUE_FOR_ARCHIVE"

        return "ACTIVE"
