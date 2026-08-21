"""
TruthShield X — Canonical Digital Asset Inventory Service
"""

import uuid
from typing import Dict, List, Optional, Any
from datetime import datetime, timezone
from app.schemas.exposure_models import (
    AssetDTO,
    AssetTypeLiteral,
    OwnershipStatusLiteral,
    AssetCriticalityLiteral,
    MonitoringStatusLiteral,
)
from app.services.exposure.asset_canonicalization_service import AssetCanonicalizationService


class AssetInventoryService:
    """Manages the canonical digital asset inventory with strict tenant isolation and ownership tracking."""

    def __init__(self):
        # tenant_id -> asset_id -> AssetDTO
        self._assets: Dict[str, Dict[str, AssetDTO]] = {}
        # tenant_id -> canonical_identifier -> asset_id
        self._canonical_index: Dict[str, Dict[str, str]] = {}

    def register_asset(
        self,
        asset_type: AssetTypeLiteral,
        raw_identifier: str,
        ownership_status: OwnershipStatusLiteral = "UNKNOWN",
        criticality: AssetCriticalityLiteral = "MEDIUM",
        tenant_id: str = "default_tenant",
        classification: str = "INTERNAL",
        monitoring_frequency: str = "HOURLY",
        metadata: Optional[Dict[str, Any]] = None,
    ) -> AssetDTO:
        """Registers a new canonical digital asset in the tenant inventory."""
        canonical_id, display_id = AssetCanonicalizationService.canonicalize_identifier(asset_type, raw_identifier)

        if tenant_id not in self._assets:
            self._assets[tenant_id] = {}
            self._canonical_index[tenant_id] = {}

        # Check if already exists in tenant context
        if canonical_id in self._canonical_index[tenant_id]:
            existing_id = self._canonical_index[tenant_id][canonical_id]
            existing_asset = self._assets[tenant_id][existing_id]
            # Update last seen and metadata
            existing_asset.last_seen = datetime.now(timezone.utc).isoformat()
            if metadata:
                existing_asset.metadata.update(metadata)
            return existing_asset

        asset_id = f"ast_{uuid.uuid4().hex[:12]}"
        now_iso = datetime.now(timezone.utc).isoformat()

        # Invariant: Never infer verified ownership merely from domain or IP registration
        auth_status = "AUTHORIZED" if ownership_status in ("VERIFIED_OWNER", "AUTHORIZED_MONITORING") else "PENDING_VERIFICATION"

        asset = AssetDTO(
            asset_id=asset_id,
            asset_type=asset_type,
            canonical_identifier=canonical_id,
            display_identifier=display_id,
            ownership_status=ownership_status,
            authorization_status=auth_status,
            criticality=criticality,
            tenant_id=tenant_id,
            classification=classification,
            first_seen=now_iso,
            last_seen=now_iso,
            current_state="ACTIVE",
            trust_score=85.0,
            risk_score=15.0,
            exposure_score=20.0,
            monitoring_status="CONFIGURED",
            monitoring_frequency=monitoring_frequency,
            metadata=metadata or {},
            created_at=now_iso,
            updated_at=now_iso,
        )

        self._assets[tenant_id][asset_id] = asset
        self._canonical_index[tenant_id][canonical_id] = asset_id
        return asset

    def get_asset(self, asset_id: str, tenant_id: str = "default_tenant") -> Optional[AssetDTO]:
        """Retrieves an asset by asset_id within the tenant boundary."""
        return self._assets.get(tenant_id, {}).get(asset_id)

    def get_asset_by_canonical(self, canonical_identifier: str, tenant_id: str = "default_tenant") -> Optional[AssetDTO]:
        """Retrieves an asset by canonical identifier within tenant boundary."""
        asset_id = self._canonical_index.get(tenant_id, {}).get(canonical_identifier)
        if asset_id:
            return self.get_asset(asset_id, tenant_id)
        return None

    def list_assets(
        self,
        asset_type: Optional[AssetTypeLiteral] = None,
        criticality: Optional[AssetCriticalityLiteral] = None,
        monitoring_status: Optional[MonitoringStatusLiteral] = None,
        tenant_id: str = "default_tenant",
        limit: int = 100,
    ) -> List[AssetDTO]:
        """Lists assets matching criteria in the authorized tenant space."""
        tenant_assets = list(self._assets.get(tenant_id, {}).values())
        results = []
        for a in tenant_assets:
            if asset_type and a.asset_type != asset_type:
                continue
            if criticality and a.criticality != criticality:
                continue
            if monitoring_status and a.monitoring_status != monitoring_status:
                continue
            results.append(a)
            if len(results) >= limit:
                break
        return results

    def update_ownership_status(
        self,
        asset_id: str,
        new_status: OwnershipStatusLiteral,
        tenant_id: str = "default_tenant",
    ) -> AssetDTO:
        """Updates ownership verification status with safety validation."""
        asset = self.get_asset(asset_id, tenant_id)
        if not asset:
            raise KeyError(f"Asset '{asset_id}' not found in tenant context.")

        asset.ownership_status = new_status
        asset.authorization_status = "AUTHORIZED" if new_status in ("VERIFIED_OWNER", "AUTHORIZED_MONITORING") else "PENDING_VERIFICATION"
        asset.updated_at = datetime.now(timezone.utc).isoformat()
        return asset

    def update_scores(
        self,
        asset_id: str,
        exposure_score: Optional[float] = None,
        trust_score: Optional[float] = None,
        risk_score: Optional[float] = None,
        tenant_id: str = "default_tenant",
    ) -> AssetDTO:
        """Updates exposure, trust, and risk scores on an asset."""
        asset = self.get_asset(asset_id, tenant_id)
        if not asset:
            raise KeyError(f"Asset '{asset_id}' not found in tenant context.")

        if exposure_score is not None:
            asset.exposure_score = max(0.0, min(100.0, exposure_score))
        if trust_score is not None:
            asset.trust_score = max(0.0, min(100.0, trust_score))
        if risk_score is not None:
            asset.risk_score = max(0.0, min(100.0, risk_score))

        asset.updated_at = datetime.now(timezone.utc).isoformat()
        return asset
