"""
TruthShield X — Intelligence Quality Scoring Engine (Phase 16).

Evaluates multi-dimensional quality scores: Freshness, Provenance Quality,
Source Reliability, Corroboration, Validation Status, and Dispute Penalties.
"""

from typing import Dict, Optional
from datetime import datetime, timezone

from app.schemas.collective_defense_models import (
    ThreatIntelligenceObjectDTO,
    IntelligenceQualityScoreDTO,
    FreshnessStatusLiteral,
)


class IntelligenceQualityEngine:
    """Computes multi-dimensional quality metrics for threat intelligence."""

    def evaluate_quality(
        self,
        obj: ThreatIntelligenceObjectDTO,
        has_active_disputes: bool = False,
    ) -> IntelligenceQualityScoreDTO:
        """Calculates multi-dimensional quality score."""
        # 1. Freshness assessment
        created_dt = datetime.fromisoformat(obj.created_at)
        age_hours = (datetime.now(timezone.utc) - created_dt).total_seconds() / 3600.0

        if age_hours <= 48:
            freshness_status: FreshnessStatusLiteral = "FRESH"
            freshness_score = 1.0
        elif age_hours <= 168:
            freshness_status = "AGING"
            freshness_score = 0.75
        elif age_hours <= 720:
            freshness_status = "STALE"
            freshness_score = 0.40
        else:
            freshness_status = "EXPIRED"
            freshness_score = 0.10

        # 2. Provenance score
        provenance_score = 0.90 if obj.provenance.get("origin_source_id") else 0.50

        # 3. Corroboration score
        sources = obj.provenance.get("source_history", [])
        corroboration_score = min(1.0, 0.50 + 0.15 * len(sources))

        # 4. Source reliability
        source_rel_score = obj.reliability

        # 5. Validation state
        val_map = {
            "VALIDATED": 1.0,
            "CORRELATED": 0.90,
            "SHARED": 0.85,
            "OBSERVED": 0.60,
            "VALIDATING": 0.50,
            "SUBMITTED": 0.40,
            "DISPUTED": 0.20,
            "REVOKED": 0.0,
            "EXPIRED": 0.10,
            "REJECTED": 0.0,
        }
        val_score = val_map.get(obj.validation_state, 0.50)

        # 6. Dispute penalty
        dispute_penalty = 0.30 if has_active_disputes else 0.0

        # Overall weighted harmonic mean
        weighted_sum = (
            0.20 * freshness_score
            + 0.20 * provenance_score
            + 0.20 * corroboration_score
            + 0.20 * source_rel_score
            + 0.20 * val_score
        )
        overall = max(0.0, min(1.0, weighted_sum - dispute_penalty))

        return IntelligenceQualityScoreDTO(
            intelligence_id=obj.intelligence_id,
            freshness_status=freshness_status,
            freshness_score=round(freshness_score, 2),
            provenance_score=round(provenance_score, 2),
            corroboration_score=round(corroboration_score, 2),
            source_reliability_score=round(source_rel_score, 2),
            validation_score=round(val_score, 2),
            dispute_penalty=round(dispute_penalty, 2),
            overall_quality_score=round(overall, 2),
        )
