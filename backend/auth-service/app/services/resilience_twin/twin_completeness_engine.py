"""
TruthShield X — Twin Completeness & Confidence Scoring Engine (Phase 18).

Calculates multi-dimensional completeness, confidence, and telemetry freshness without compression into an opaque metric.
"""

from typing import Dict, Optional
from datetime import datetime, timezone

from app.schemas.cyber_resilience_twin_models import (
    TwinCompletenessScoreDTO,
    TwinConfidenceScoreDTO,
)


class TwinCompletenessEngine:
    """Evaluates multi-dimensional visibility and confidence separation."""

    def __init__(self):
        self._completeness_scores: Dict[str, TwinCompletenessScoreDTO] = {}
        self._confidence_scores: Dict[str, TwinConfidenceScoreDTO] = {}

    def calculate_completeness(
        self,
        tenant_id: str = "default_tenant",
        asset_vis: float = 95.0,
        ident_vis: float = 90.0,
        serv_vis: float = 92.0,
        dep_vis: float = 84.0,
        ctrl_vis: float = 96.0,
        threat_vis: float = 88.0,
        biz_map: float = 78.0,
        rec_map: float = 82.0,
    ) -> TwinCompletenessScoreDTO:
        """Calculates granular 8-dimension completeness scorecard."""
        dims = [asset_vis, ident_vis, serv_vis, dep_vis, ctrl_vis, threat_vis, biz_map, rec_map]
        overall = sum(dims) / len(dims)

        score = TwinCompletenessScoreDTO(
            tenant_id=tenant_id,
            asset_visibility=round(asset_vis, 1),
            identity_visibility=round(ident_vis, 1),
            service_visibility=round(serv_vis, 1),
            dependency_visibility=round(dep_vis, 1),
            control_visibility=round(ctrl_vis, 1),
            threat_visibility=round(threat_vis, 1),
            business_mapping=round(biz_map, 1),
            recovery_mapping=round(rec_map, 1),
            overall_completeness=round(overall, 2),
        )

        self._completeness_scores[tenant_id] = score
        return score

    def get_confidence_breakdown(
        self,
        tenant_id: str = "default_tenant",
        completeness: float = 88.0,
        confidence: float = 91.0,
        freshness: float = 96.0,
    ) -> TwinConfidenceScoreDTO:
        """Separates completeness, confidence, and freshness."""
        score = TwinConfidenceScoreDTO(
            tenant_id=tenant_id,
            completeness=completeness,
            confidence=confidence,
            freshness=freshness,
        )
        self._confidence_scores[tenant_id] = score
        return score

    def get_completeness(self, tenant_id: str = "default_tenant") -> Optional[TwinCompletenessScoreDTO]:
        return self._completeness_scores.get(tenant_id)
