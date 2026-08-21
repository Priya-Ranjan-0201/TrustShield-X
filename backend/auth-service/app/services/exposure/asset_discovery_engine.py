"""
TruthShield X — Asset Discovery & Shadow Asset Detection Engine
"""

import uuid
from typing import Dict, List, Optional
from datetime import datetime, timezone
from app.schemas.exposure_models import ShadowAssetDTO, AssetTypeLiteral
from app.services.exposure.asset_canonicalization_service import AssetCanonicalizationService
from app.services.exposure.asset_inventory_service import AssetInventoryService


class AssetDiscoveryEngine:
    """Discovers undeclared digital assets and classifies shadow infrastructure."""

    def __init__(self, inventory_service: Optional[AssetInventoryService] = None):
        self._inventory = inventory_service or AssetInventoryService()
        # tenant_id -> shadow_id -> ShadowAssetDTO
        self._shadow_assets: Dict[str, Dict[str, ShadowAssetDTO]] = {}

    def discover_candidate(
        self,
        raw_identifier: str,
        asset_type: AssetTypeLiteral,
        discovery_source: str,
        related_brand_or_domain: str,
        confidence: float = 0.75,
        discovery_evidence: Optional[List[str]] = None,
        tenant_id: str = "default_tenant",
    ) -> ShadowAssetDTO:
        """Evaluates a newly observed identifier against the declared inventory to detect shadow assets."""
        canonical_id, _ = AssetCanonicalizationService.canonicalize_identifier(asset_type, raw_identifier)

        # Check if already declared in inventory
        existing_asset = self._inventory.get_asset_by_canonical(canonical_id, tenant_id)

        shadow_status = "UNKNOWN"
        if existing_asset is not None:
            # Asset is already known/declared in inventory
            shadow_status = "VERIFIED_UNDECLARED_ASSET" if existing_asset.ownership_status == "CLAIMED_OWNER" else "UNKNOWN"
        else:
            # Not in declared inventory, determine if it's related to the brand
            if related_brand_or_domain.lower() in canonical_id.lower():
                shadow_status = "PROBABLE_SHADOW_ASSET" if confidence >= 0.80 else "POSSIBLE_SHADOW_ASSET"
            else:
                shadow_status = "POSSIBLE_SHADOW_ASSET"

        shadow_id = f"shd_{uuid.uuid4().hex[:12]}"
        record = ShadowAssetDTO(
            shadow_id=shadow_id,
            canonical_identifier=canonical_id,
            asset_type=asset_type,
            shadow_status=shadow_status,
            discovery_source=discovery_source,
            confidence=confidence,
            related_brand_or_domain=related_brand_or_domain,
            discovery_evidence=discovery_evidence or [f"Observed via {discovery_source}"],
            tenant_id=tenant_id,
            discovered_at=datetime.now(timezone.utc).isoformat(),
        )

        if tenant_id not in self._shadow_assets:
            self._shadow_assets[tenant_id] = {}
        self._shadow_assets[tenant_id][shadow_id] = record

        return record

    def list_shadow_assets(
        self,
        tenant_id: str = "default_tenant",
        status_filter: Optional[str] = None,
    ) -> List[ShadowAssetDTO]:
        """Lists detected shadow assets for a tenant."""
        tenant_shadows = list(self._shadow_assets.get(tenant_id, {}).values())
        if status_filter:
            return [s for s in tenant_shadows if s.shadow_status == status_filter]
        return tenant_shadows
