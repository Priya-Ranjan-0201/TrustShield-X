"""
TruthShield X — Cyber Resilience Scoring Engine (Phase 18).

Calculates comprehensive 7-dimensional cyber resilience scorecards.
"""

from typing import Dict, Optional
from datetime import datetime, timezone

from app.schemas.cyber_resilience_twin_models import CyberResilienceScoreDTO


class CyberResilienceScorer:
    """Computes multidimensional resilience metrics."""

    def __init__(self):
        self._scores: Dict[str, CyberResilienceScoreDTO] = {}

    def calculate_resilience(
        self,
        tenant_id: str = "default_tenant",
        prevention: float = 88.0,
        detection: float = 92.0,
        containment: float = 85.0,
        recovery: float = 80.0,
        adaptability: float = 90.0,
        dependency_resilience: float = 82.0,
        governance_readiness: float = 94.0,
    ) -> CyberResilienceScoreDTO:
        """Calculates 7-dimensional resilience scorecard."""
        dims = [
            prevention,
            detection,
            containment,
            recovery,
            adaptability,
            dependency_resilience,
            governance_readiness,
        ]
        overall = sum(dims) / len(dims)

        score = CyberResilienceScoreDTO(
            tenant_id=tenant_id,
            prevention=round(prevention, 1),
            detection=round(detection, 1),
            containment=round(containment, 1),
            recovery=round(recovery, 1),
            adaptability=round(adaptability, 1),
            dependency_resilience=round(dependency_resilience, 1),
            governance_readiness=round(governance_readiness, 1),
            overall_resilience_score=round(overall, 2),
        )

        self._scores[tenant_id] = score
        return score

    def get_score(self, tenant_id: str = "default_tenant") -> Optional[CyberResilienceScoreDTO]:
        return self._scores.get(tenant_id)
