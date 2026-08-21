"""
TruthShield X — Phase 8 Exposure Management & Continuous Digital Trust Monitoring API Endpoints
"""

from typing import Any, Dict, List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel, Field

from app.schemas.exposure_models import (
    AssetDTO,
    AssetTypeLiteral,
    OwnershipStatusLiteral,
    AssetCriticalityLiteral,
    ExposureFindingDTO,
    CorrelatedExposureEventDTO,
    ShadowAssetDTO,
    BrandImpersonationFindingDTO,
    AttackSurfaceSummaryDTO,
)
from app.services.exposure.asset_inventory_service import AssetInventoryService
from app.services.exposure.asset_baseline_engine import AssetBaselineEngine
from app.services.exposure.change_detection_engine import ChangeDetectionEngine
from app.services.exposure.exposure_scoring_engine import ExposureScoringEngine
from app.services.exposure.exposure_prioritization_engine import ExposurePrioritizationEngine
from app.services.exposure.asset_discovery_engine import AssetDiscoveryEngine
from app.services.exposure.brand_impersonation_engine import BrandImpersonationMonitoringEngine
from app.services.exposure.continuous_monitoring_scheduler import ContinuousMonitoringScheduler
from app.services.exposure.exposure_alert_correlation_engine import ExposureAlertCorrelationEngine
from app.services.exposure.asset_canonicalization_service import AssetCanonicalizationService


router = APIRouter(prefix="/exposure", tags=["Continuous Monitoring & Exposure Management"])

# Singletons
_inventory_service = AssetInventoryService()
_baseline_engine = AssetBaselineEngine()
_change_engine = ChangeDetectionEngine()
_prioritization_engine = ExposurePrioritizationEngine()
_discovery_engine = AssetDiscoveryEngine(_inventory_service)
_impersonation_engine = BrandImpersonationMonitoringEngine()
_scheduler = ContinuousMonitoringScheduler()
_correlation_engine = ExposureAlertCorrelationEngine()


# Request Schemas
class AssetRegisterRequest(BaseModel):
    asset_type: AssetTypeLiteral
    raw_identifier: str
    ownership_status: OwnershipStatusLiteral = "UNKNOWN"
    criticality: AssetCriticalityLiteral = "MEDIUM"
    tenant_id: str = "default_tenant"
    classification: str = "INTERNAL"
    monitoring_frequency: str = "HOURLY"
    metadata: Optional[Dict[str, Any]] = None


class DiscoverCandidateRequest(BaseModel):
    raw_identifier: str
    asset_type: AssetTypeLiteral
    discovery_source: str
    related_brand_or_domain: str
    confidence: float = 0.75
    tenant_id: str = "default_tenant"


class ScheduleMonitoringRequest(BaseModel):
    mode: str = "PASSIVE"
    tenant_id: str = "default_tenant"


@router.post("/assets", response_model=AssetDTO, status_code=status.HTTP_201_CREATED)
def register_asset(payload: AssetRegisterRequest) -> AssetDTO:
    """Registers a new digital asset in the tenant inventory."""
    return _inventory_service.register_asset(
        asset_type=payload.asset_type,
        raw_identifier=payload.raw_identifier,
        ownership_status=payload.ownership_status,
        criticality=payload.criticality,
        tenant_id=payload.tenant_id,
        classification=payload.classification,
        monitoring_frequency=payload.monitoring_frequency,
        metadata=payload.metadata,
    )


@router.get("/assets", response_model=List[AssetDTO])
def list_assets(
    asset_type: Optional[AssetTypeLiteral] = None,
    criticality: Optional[AssetCriticalityLiteral] = None,
    tenant_id: str = "default_tenant",
    limit: int = Query(default=100, le=500),
) -> List[AssetDTO]:
    """Lists registered digital assets for the tenant."""
    return _inventory_service.list_assets(
        asset_type=asset_type,
        criticality=criticality,
        tenant_id=tenant_id,
        limit=limit,
    )


@router.get("/assets/{asset_id}", response_model=AssetDTO)
def get_asset(asset_id: str, tenant_id: str = "default_tenant") -> AssetDTO:
    """Retrieves an asset by asset_id within tenant context."""
    asset = _inventory_service.get_asset(asset_id, tenant_id)
    if not asset:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Asset not found.")
    return asset


@router.get("/assets/{asset_id}/changes")
def get_asset_changes(asset_id: str, tenant_id: str = "default_tenant") -> List[Any]:
    """Retrieves all detected changes for an asset."""
    return _change_engine.get_changes_for_asset(asset_id, tenant_id)


@router.post("/assets/{asset_id}/monitoring")
def schedule_asset_monitoring(asset_id: str, payload: ScheduleMonitoringRequest) -> Dict[str, Any]:
    """Schedules continuous monitoring for an asset with safety and SSRF validation."""
    asset = _inventory_service.get_asset(asset_id, payload.tenant_id)
    if not asset:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Asset not found.")

    if payload.mode == "AUTHORIZED_ACTIVE":
        # SSRF and Target safety check
        safety = AssetCanonicalizationService.validate_target_safety(asset.canonical_identifier)
        if not safety["is_safe"]:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Active monitoring rejected: {safety['reason']}")

    return _scheduler.schedule_monitoring_job(asset, mode=payload.mode, tenant_id=payload.tenant_id)


@router.get("/findings", response_model=List[ExposureFindingDTO])
def list_exposure_findings(
    severity: Optional[str] = None,
    lifecycle_state: Optional[str] = None,
    tenant_id: str = "default_tenant",
) -> List[ExposureFindingDTO]:
    """Lists prioritized exposure findings."""
    return _prioritization_engine.list_findings(
        tenant_id=tenant_id,
        severity_filter=severity,
        lifecycle_filter=lifecycle_state,
    )


@router.get("/events", response_model=List[CorrelatedExposureEventDTO])
def list_exposure_events(tenant_id: str = "default_tenant") -> List[CorrelatedExposureEventDTO]:
    """Lists correlated exposure incidents."""
    return _correlation_engine.list_correlated_events(tenant_id)


@router.post("/discover", response_model=ShadowAssetDTO)
def discover_shadow_asset(payload: DiscoverCandidateRequest) -> ShadowAssetDTO:
    """Discovers and evaluates an undeclared candidate asset."""
    return _discovery_engine.discover_candidate(
        raw_identifier=payload.raw_identifier,
        asset_type=payload.asset_type,
        discovery_source=payload.discovery_source,
        related_brand_or_domain=payload.related_brand_or_domain,
        confidence=payload.confidence,
        tenant_id=payload.tenant_id,
    )


@router.get("/shadow-assets", response_model=List[ShadowAssetDTO])
def list_shadow_assets(tenant_id: str = "default_tenant") -> List[ShadowAssetDTO]:
    """Lists detected shadow assets for a tenant."""
    return _discovery_engine.list_shadow_assets(tenant_id)


@router.get("/impersonations", response_model=List[BrandImpersonationFindingDTO])
def list_brand_impersonations(tenant_id: str = "default_tenant") -> List[BrandImpersonationFindingDTO]:
    """Lists brand impersonations and typosquats."""
    return _impersonation_engine.list_impersonations(tenant_id)


@router.get("/dashboard", response_model=AttackSurfaceSummaryDTO)
def get_attack_surface_dashboard(tenant_id: str = "default_tenant") -> AttackSurfaceSummaryDTO:
    """Provides an executive scorecard of attack surface exposure."""
    assets = _inventory_service.list_assets(tenant_id=tenant_id, limit=1000)
    shadows = _discovery_engine.list_shadow_assets(tenant_id)
    findings = _prioritization_engine.list_findings(tenant_id)
    impersonations = _impersonation_engine.list_impersonations(tenant_id)

    total_assets = len(assets)
    monitored = sum(1 for a in assets if a.monitoring_status in ("CONFIGURED", "SCHEDULED", "RUNNING"))
    unknown_own = sum(1 for a in assets if a.ownership_status == "UNKNOWN")
    high_exp = sum(1 for a in assets if a.exposure_score >= 60.0)
    crit_exp = sum(1 for a in assets if a.exposure_score >= 80.0)

    mean_exp = sum(a.exposure_score for a in assets) / total_assets if total_assets > 0 else 0.0
    mean_trust = sum(a.trust_score for a in assets) / total_assets if total_assets > 0 else 0.0

    return AttackSurfaceSummaryDTO(
        tenant_id=tenant_id,
        total_assets=total_assets,
        monitored_assets=monitored,
        unmonitored_assets=total_assets - monitored,
        unknown_ownership_assets=unknown_own,
        high_exposure_assets=high_exp,
        critical_exposure_assets=crit_exp,
        active_findings_count=len(findings),
        shadow_assets_count=len(shadows),
        brand_impersonations_count=len(impersonations),
        mean_exposure_score=round(mean_exp, 1),
        mean_trust_score=round(mean_trust, 1),
    )
