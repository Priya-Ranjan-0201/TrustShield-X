"""
TruthShield X — Knowledge Quality Engine (Phase 19).

Computes comprehensive health scorecards across 7 knowledge dimensions.
"""

from app.schemas.cyber_knowledge_fabric_models import KnowledgeQualityScorecardDTO


class KnowledgeQualityEngine:
    """Computes quality and health scorecards for the knowledge fabric."""

    def compute_scorecard(
        self,
        data_quality: float = 92.5,
        evidence_quality: float = 94.0,
        graph_quality: float = 91.0,
        provenance_completeness: float = 98.0,
        freshness_score: float = 95.0,
        contradiction_rate: float = 2.1,
    ) -> KnowledgeQualityScorecardDTO:
        # Contradiction penalty
        penalty = contradiction_rate * 0.5
        base = (data_quality + evidence_quality + graph_quality + provenance_completeness + freshness_score) / 5.0
        overall = round(max(0.0, min(100.0, base - penalty)), 1)

        return KnowledgeQualityScorecardDTO(
            data_quality=data_quality,
            evidence_quality=evidence_quality,
            graph_quality=graph_quality,
            provenance_completeness=provenance_completeness,
            freshness_score=freshness_score,
            contradiction_rate=contradiction_rate,
            overall_health_score=overall,
        )
