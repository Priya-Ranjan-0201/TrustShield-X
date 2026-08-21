"""
TruthShield X — Intelligence Corroboration & Confidence Scoring Engine
"""

from typing import Dict, List, Optional, Any
from app.schemas.federation_models import FederatedIntelligenceObjectDTO


class IntelligenceCorroborationEngine:
    """Evaluates multi-source independence, corroboration depth, and computes composite confidence scores."""

    def evaluate_corroboration(
        self,
        target_indicator: str,
        observations: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """Corroborates observations across distinct sources without double-counting duplicate feeds."""
        unique_sources = set(obs.get("source_id") for obs in observations if obs.get("source_id"))
        source_count = len(unique_sources)

        if source_count == 0:
            return {
                "indicator": target_indicator,
                "corroboration_level": "NONE",
                "independent_sources_count": 0,
                "confidence_score": 0.50,
                "verification_status": "UNVERIFIED",
            }

        # Calculate weighted confidence
        avg_rel = sum(float(obs.get("source_reliability", 0.8)) for obs in observations) / len(observations)
        corroboration_bonus = min(0.35, (source_count - 1) * 0.12)
        final_conf = min(0.99, max(0.40, avg_rel + corroboration_bonus))

        if source_count >= 3 and final_conf >= 0.90:
            status = "VERIFIED"
            level = "HIGH_MULTI_SOURCE_VERIFICATION"
        elif source_count >= 2:
            status = "CORROBORATED"
            level = "CORROBORATED_INDEPENDENT_SOURCES"
        else:
            status = "OBSERVED"
            level = "SINGLE_SOURCE_OBSERVATION"

        return {
            "indicator": target_indicator,
            "corroboration_level": level,
            "independent_sources_count": source_count,
            "confidence_score": round(final_conf, 3),
            "verification_status": status,
            "sources": list(unique_sources),
        }
