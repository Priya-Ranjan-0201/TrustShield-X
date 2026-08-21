"""
TruthShield X — Intelligence Localization & Personalized Threat Feed Engine (Phase 16).

Translates global intelligence into tenant-specific relevance scores, filters
irrelevant noise, and recommends targeted local threat hunts.
"""

from typing import Dict, List, Any, Optional
from datetime import datetime, timezone

from app.schemas.collective_defense_models import (
    ThreatIntelligenceObjectDTO,
    TenantRelevanceDTO,
)


class IntelligenceLocalizationEngine:
    """Computes tenant-specific threat relevance and personalized feeds."""

    def compute_tenant_relevance(
        self,
        tenant_id: str,
        tenant_industry: str,
        local_assets: List[str],
        obj: ThreatIntelligenceObjectDTO,
    ) -> TenantRelevanceDTO:
        """Calculates relevance of a global indicator to a specific tenant."""
        # 1. Asset overlap
        asset_overlap = 0.0
        for asset in local_assets:
            if asset.lower() in obj.canonical_identifier.lower() or obj.canonical_identifier.lower() in asset.lower():
                asset_overlap = 1.0
                break

        # 2. Industry sector relevance
        industry_score = 0.5
        if obj.anonymized_tenant_cohort and tenant_industry.upper() in obj.anonymized_tenant_cohort:
            industry_score = 0.9

        # 3. Overall relevance calculation
        overall = (asset_overlap * 0.5) + (industry_score * 0.3) + (obj.confidence * 0.2)
        is_applicable = overall >= 0.40 or asset_overlap > 0.0

        recommended_hunts = []
        if is_applicable:
            recommended_hunts.append(
                f"Hunt for IOC '{obj.canonical_identifier}' across tenant {tenant_id} endpoints and network logs"
            )
            if obj.intelligence_type in ("DOMAIN", "IP", "URL"):
                recommended_hunts.append(f"Check DNS/proxy logs for lookups to {obj.canonical_identifier}")

        return TenantRelevanceDTO(
            tenant_id=tenant_id,
            intelligence_id=obj.intelligence_id,
            overall_relevance_score=round(overall, 2),
            asset_overlap_score=asset_overlap,
            industry_relevance_score=industry_score,
            historical_exposure_score=0.4,
            recommended_hunts=recommended_hunts,
            is_applicable=is_applicable,
        )
