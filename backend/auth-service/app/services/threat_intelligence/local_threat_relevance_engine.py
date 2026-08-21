"""
TruthShield X — Local Threat Relevance Engine (Phase 22).

Computes contextual relevance of global threats to tenant-specific asset inventory and exposures.
"""

from typing import List, Dict, Any, Optional
from app.schemas.threat_intelligence_fabric_models import LocalThreatRelevanceDTO


class LocalThreatRelevanceEngine:
    """Evaluates technical, exposure, and threat relevance for tenant assets."""

    def compute_relevance(
        self,
        tenant_id: str,
        threat_entity_id: str,
        targeted_technologies: List[str],
        tenant_inventory_techs: List[str],
        exposed_assets: List[str],
    ) -> LocalThreatRelevanceDTO:
        # Technical relevance: overlap between threat TTP/target and local stack
        overlap = set(targeted_technologies).intersection(set(tenant_inventory_techs))
        tech_score = 90.0 if overlap else 25.0

        # Exposure score
        exposure_score = 85.0 if exposed_assets else 30.0

        # Threat activity score
        threat_score = 88.0

        # Weighted calculation
        overall = round((tech_score * 0.45) + (exposure_score * 0.35) + (threat_score * 0.20), 1)

        recommendation = "MONITOR"
        if overall > 75.0:
            recommendation = "APPLY_VIRTUAL_PATCH_AND_SIMULATE_CONTAINMENT"
        elif overall > 50.0:
            recommendation = "ENHANCE_TELEMETRY_LOGGING_AND_SEARCH_QUERIES"

        return LocalThreatRelevanceDTO(
            tenant_id=tenant_id,
            threat_entity_id=threat_entity_id,
            technical_relevance_score=tech_score,
            exposure_relevance_score=exposure_score,
            threat_activity_score=threat_score,
            overall_relevance_score=overall,
            affected_local_assets=exposed_assets if overlap else [],
            recommended_defensive_action=recommendation,
        )
