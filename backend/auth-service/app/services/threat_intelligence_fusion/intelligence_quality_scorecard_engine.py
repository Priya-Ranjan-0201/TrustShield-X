"""
TruthShield X — Intelligence Quality Scorecard Engine (Phase 33).

Evaluates 6 independent dimensions of intelligence quality (Source Reliability, Credibility,
Freshness, Corroboration, Context Completeness, Provenance) without collapsing into an opaque single score.
"""

from typing import Dict, List, Any, Optional
from app.schemas.threat_intelligence_fusion_models import IntelligenceQualityScorecardDTO


class IntelligenceQualityScorecardEngine:
    """Generates 6-dimensional forensic intelligence quality scorecards."""

    def evaluate_quality(
        self,
        source_reliability: str = "A",
        information_credibility: str = "1",
        age_in_days: int = 2,
        independent_sources_count: int = 3,
        has_techniques: bool = True,
        has_affected_assets: bool = True,
        has_sha256_provenance: bool = True,
    ) -> IntelligenceQualityScorecardDTO:
        freshness_score = max(0.10, round(1.0 - (age_in_days / 90.0), 2))
        
        context_points = 0
        if has_techniques:
            context_points += 0.5
        if has_affected_assets:
            context_points += 0.5
        context_completeness = round(context_points, 2)

        assessment = "HIGH_QUALITY_GROUNDED"
        if freshness_score < 0.40:
            assessment = "AGING_INTELLIGENCE"
        elif not has_sha256_provenance:
            assessment = "PROVENANCE_INCOMPLETE"
        elif independent_sources_count <= 1 and source_reliability not in ("A", "B"):
            assessment = "UNVERIFIED_SINGLE_SOURCE"

        return IntelligenceQualityScorecardDTO(
            source_reliability=source_reliability,
            information_credibility=information_credibility,
            freshness_score=freshness_score,
            corroboration_count=independent_sources_count,
            context_completeness=context_completeness,
            provenance_verified=has_sha256_provenance,
            overall_quality_assessment=assessment,
        )
