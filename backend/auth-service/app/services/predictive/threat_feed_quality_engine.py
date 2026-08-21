"""Threat Feed Quality & Source Reliability Engine (Phase 6 - Section 3).

Evaluates external intelligence feed accuracy, freshness, consistency, and false-positive rates
to produce calibrated source reliability scores.
"""

from typing import List, Dict, Any, Optional
from datetime import datetime, timezone
import uuid

from app.schemas.predictive_threat_models import ThreatSourceReliabilityDTO


class ThreatFeedQualityEngine:
    """Evaluates and maintains source reliability ratings for intelligence feeds."""

    def __init__(self):
        self._sources: Dict[str, ThreatSourceReliabilityDTO] = {}
        # Seed standard sources
        self.register_or_update_source(
            source_id="src_internal_canonical",
            provider="TruthShield Internal Verified Analyzers",
            historical_accuracy=0.98,
            freshness_score=0.99,
            false_positive_rate=0.01,
            is_authoritative=True,
        )
        self.register_or_update_source(
            source_id="src_commercial_threat_feed",
            provider="Global Commercial Cyber Threat Intelligence",
            historical_accuracy=0.88,
            freshness_score=0.90,
            false_positive_rate=0.06,
            is_authoritative=False,
        )
        self.register_or_update_source(
            source_id="src_community_osint",
            provider="Open-Source Community Blocklist",
            historical_accuracy=0.68,
            freshness_score=0.75,
            false_positive_rate=0.18,
            is_authoritative=False,
        )

    def register_or_update_source(
        self,
        source_id: str,
        provider: str,
        historical_accuracy: float = 0.85,
        freshness_score: float = 0.90,
        false_positive_rate: float = 0.05,
        is_authoritative: bool = False,
    ) -> ThreatSourceReliabilityDTO:
        """Calculates and updates source reliability score."""
        # Reliability formula: (Accuracy * 0.45) + (Freshness * 0.35) + ((1 - FP_rate) * 0.20)
        accuracy_weight = historical_accuracy * 0.45
        freshness_weight = freshness_score * 0.35
        fp_weight = max(0.0, 1.0 - false_positive_rate) * 0.20
        overall_reliability = min(1.0, max(0.10, accuracy_weight + freshness_weight + fp_weight))

        dto = ThreatSourceReliabilityDTO(
            source_id=source_id,
            provider=provider,
            source_reliability_score=round(overall_reliability, 3),
            historical_accuracy=historical_accuracy,
            freshness_score=freshness_score,
            false_positive_rate=false_positive_rate,
            is_authoritative=is_authoritative,
            last_evaluated=datetime.now(timezone.utc).isoformat(),
        )
        self._sources[source_id] = dto
        return dto

    def get_source_reliability(self, source_id: str) -> ThreatSourceReliabilityDTO:
        """Retrieves reliability record for a threat intelligence source."""
        if source_id in self._sources:
            return self._sources[source_id]
        # Unknown source gets low baseline reliability
        return ThreatSourceReliabilityDTO(
            source_id=source_id,
            provider="Unknown Intelligence Provider",
            source_reliability_score=0.40,
            historical_accuracy=0.50,
            freshness_score=0.50,
            false_positive_rate=0.25,
            is_authoritative=False,
        )

    def weight_signal_confidence(self, source_id: str, raw_confidence: float) -> float:
        """Weights raw signal confidence by the source's empirical reliability."""
        rel = self.get_source_reliability(source_id)
        # Multiply raw confidence by source reliability
        weighted = raw_confidence * rel.source_reliability_score
        return round(min(1.0, max(0.05, weighted)), 2)
