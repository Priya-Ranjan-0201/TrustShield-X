"""
TruthShield X — Evidence Strength Engine (Phase 19).

Evaluates evidence quality across 7 distinct dimensions (source reliability, directness, freshness, corroboration, reproducibility, integrity, independence).
"""

from typing import Dict, List, Optional
from app.schemas.cyber_knowledge_fabric_models import EvidenceStrengthDTO


class EvidenceStrengthEngine:
    """Computes multidimensional strength scores without collapsing them into an opaque single value."""

    def evaluate_strength(
        self,
        source_reliability: float = 0.90,
        directness: float = 0.85,
        freshness: float = 0.95,
        corroboration: float = 0.80,
        reproducibility: float = 0.90,
        integrity: float = 0.99,
        independence: float = 0.85,
    ) -> EvidenceStrengthDTO:
        """Calculates 7-dimension evidence strength metrics."""
        overall = round(
            (source_reliability + directness + freshness + corroboration + reproducibility + integrity + independence) / 7.0,
            4,
        )
        return EvidenceStrengthDTO(
            source_reliability=source_reliability,
            directness=directness,
            freshness=freshness,
            corroboration=corroboration,
            reproducibility=reproducibility,
            integrity=integrity,
            independence=independence,
            overall_strength=overall,
        )

    def evaluate_independence(self, source_identities: List[str]) -> float:
        """Computes true evidence independence. Multiple copies from the same source do NOT count as independent corroborations."""
        if not source_identities:
            return 0.0
        unique_sources = set(source_identities)
        # Ratio of unique sources to total observations
        return round(len(unique_sources) / len(source_identities), 4)
