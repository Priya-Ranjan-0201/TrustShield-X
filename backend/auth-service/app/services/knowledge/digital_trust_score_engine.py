"""Digital Trust Score & Profile Engine (Phase 7 - Sections 16-20).

Calculates multi-dimensional Digital Trust Scores (0-100), maintains entity trust profiles,
tracks trust history transitions, and applies temporal trust decay to derived assessments.
"""

from typing import List, Dict, Any, Optional
from datetime import datetime, timezone, timedelta
import uuid

from app.schemas.knowledge_fabric_models import (
    DigitalTrustScoreDTO,
    DigitalTrustProfileDTO,
    TrustDimensionLiteral,
)
from app.services.knowledge.knowledge_fabric_service import KnowledgeFabricService


class DigitalTrustScoreEngine:
    """Computes 6-dimensional Digital Trust Scores and maintains entity trust profiles."""

    def __init__(self, fabric: Optional[KnowledgeFabricService] = None):
        self.fabric = fabric or KnowledgeFabricService()
        self._profiles: Dict[str, Dict[str, DigitalTrustProfileDTO]] = {}  # tenant_id -> entity_id -> profile

    # -----------------------------------------------------------------------
    # Section 16 & 17: Multi-Dimensional Trust Score Calculation
    # -----------------------------------------------------------------------

    def calculate_trust_score(
        self,
        entity_id: str,
        identity_score: float = 80.0,
        content_score: float = 80.0,
        source_score: float = 85.0,
        infrastructure_score: float = 80.0,
        behavior_score: float = 85.0,
        evidence_score: float = 90.0,
        apply_decay: bool = False,
        days_since_last_seen: int = 0,
    ) -> DigitalTrustScoreDTO:
        """Calculates 6-dimensional digital trust score."""
        dimension_scores = {
            "IDENTITY_TRUST": min(100.0, max(0.0, identity_score)),
            "CONTENT_TRUST": min(100.0, max(0.0, content_score)),
            "SOURCE_TRUST": min(100.0, max(0.0, source_score)),
            "INFRASTRUCTURE_TRUST": min(100.0, max(0.0, infrastructure_score)),
            "BEHAVIOR_TRUST": min(100.0, max(0.0, behavior_score)),
            "EVIDENCE_TRUST": min(100.0, max(0.0, evidence_score)),
        }

        # Weights: Identity 20%, Content 20%, Source 15%, Infra 15%, Behavior 15%, Evidence 15%
        weights = {
            "IDENTITY_TRUST": 0.20,
            "CONTENT_TRUST": 0.20,
            "SOURCE_TRUST": 0.15,
            "INFRASTRUCTURE_TRUST": 0.15,
            "BEHAVIOR_TRUST": 0.15,
            "EVIDENCE_TRUST": 0.15,
        }

        raw_score = sum(dimension_scores[dim] * weights[dim] for dim in weights)

        # Apply Section 20: Temporal Trust Decay to derived assessment
        decay_applied = False
        if apply_decay and days_since_last_seen > 30:
            # Subtle decay (0.5% per month inactive beyond 30 days)
            decay_factor = max(0.60, 1.0 - (days_since_last_seen - 30) * 0.002)
            raw_score = raw_score * decay_factor
            decay_applied = True

        factors = [
            f"Identity integrity: {dimension_scores['IDENTITY_TRUST']}/100",
            f"Content verification: {dimension_scores['CONTENT_TRUST']}/100",
            f"Evidence confidence: {dimension_scores['EVIDENCE_TRUST']}/100",
        ]

        limitations = []
        if days_since_last_seen > 60:
            limitations.append("Historical observation is older than 60 days.")

        return DigitalTrustScoreDTO(
            trust_score=round(raw_score, 1),
            confidence=0.92,
            dimension_scores=dimension_scores,
            factors=factors,
            limitations=limitations,
            decay_applied=decay_applied,
        )

    # -----------------------------------------------------------------------
    # Section 18 & 19: Digital Trust Profile & History Management
    # -----------------------------------------------------------------------

    def get_or_create_profile(
        self,
        entity_id: str,
        initial_risk_score: float = 20.0,
        tenant_id: str = "default_tenant",
    ) -> DigitalTrustProfileDTO:
        """Retrieves or creates a digital trust profile for an entity."""
        if tenant_id not in self._profiles:
            self._profiles[tenant_id] = {}

        if entity_id in self._profiles[tenant_id]:
            return self._profiles[tenant_id][entity_id]

        trust_score_dto = self.calculate_trust_score(entity_id)
        now_iso = datetime.now(timezone.utc).isoformat()
        prof_id = f"tprof_{uuid.uuid4().hex[:12]}"

        profile = DigitalTrustProfileDTO(
            profile_id=prof_id,
            entity_id=entity_id,
            tenant_id=tenant_id,
            trust_score=trust_score_dto.trust_score,
            risk_score=initial_risk_score,
            confidence=trust_score_dto.confidence,
            dimension_scores=trust_score_dto.dimension_scores,
            associated_campaigns=[],
            recent_incidents=[],
            predictions=[],
            trust_history=[{
                "previous_score": 100.0,
                "new_score": trust_score_dto.trust_score,
                "reason": "Initial entity profiling",
                "timestamp": now_iso,
            }],
            updated_at=now_iso,
        )

        self._profiles[tenant_id][entity_id] = profile
        return profile

    def update_trust_profile(
        self,
        entity_id: str,
        new_trust_score: float,
        reason: str,
        evidence_ids: Optional[List[str]] = None,
        associated_campaigns: Optional[List[str]] = None,
        new_risk_score: Optional[float] = None,
        tenant_id: str = "default_tenant",
    ) -> DigitalTrustProfileDTO:
        """Updates trust profile recording previous score, new score, reason, and evidence in history."""
        profile = self.get_or_create_profile(entity_id, tenant_id=tenant_id)
        now_iso = datetime.now(timezone.utc).isoformat()

        history_entry = {
            "previous_score": profile.trust_score,
            "new_score": new_trust_score,
            "reason": reason,
            "evidence_ids": evidence_ids or [],
            "timestamp": now_iso,
        }

        updated_history = list(profile.trust_history) + [history_entry]
        updated_campaigns = list(set(profile.associated_campaigns + (associated_campaigns or [])))

        updated_profile = DigitalTrustProfileDTO(
            profile_id=profile.profile_id,
            entity_id=profile.entity_id,
            tenant_id=profile.tenant_id,
            trust_score=new_trust_score,
            risk_score=new_risk_score if new_risk_score is not None else profile.risk_score,
            confidence=profile.confidence,
            dimension_scores=profile.dimension_scores,
            associated_campaigns=updated_campaigns,
            recent_incidents=profile.recent_incidents,
            predictions=profile.predictions,
            trust_history=updated_history,
            updated_at=now_iso,
        )

        self._profiles[tenant_id][entity_id] = updated_profile
        return updated_profile
