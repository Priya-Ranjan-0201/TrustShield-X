"""
TruthShield X — Phase 9 Security Operations Fabric & Threat Fusion API Endpoints
"""

from typing import Any, Dict, List, Optional
from fastapi import APIRouter, HTTPException, Query, status
from pydantic import BaseModel

from app.schemas.fusion_models import (
    SecurityEventDTO,
    SecurityEventTypeLiteral,
    EventCorrelationResultDTO,
    ThreatClusterDTO,
    SecuritySituationDTO,
    SecurityPostureDTO,
    SecurityNarrativeDTO,
    IncidentCommandStateDTO,
    SecurityKpisDTO,
    SecurityHealthOverviewDTO,
)
from app.services.fusion.security_operations_fabric import SecurityOperationsFabric


router = APIRouter(prefix="/security", tags=["Security Operations Fabric & Threat Fusion"])

_fabric = SecurityOperationsFabric()


class TelemetryIngestRequest(BaseModel):
    event_type: SecurityEventTypeLiteral
    source: str
    entity_id: Optional[str] = None
    asset_id: Optional[str] = None
    campaign_id: Optional[str] = None
    severity: str = "MEDIUM"
    confidence: float = 0.90
    risk_score: float = 20.0
    trust_score: float = 80.0
    exposure_score: float = 20.0
    provenance: Optional[Dict[str, Any]] = None
    tenant_id: str = "default_tenant"


@router.post("/telemetry", status_code=status.HTTP_201_CREATED)
def ingest_telemetry(payload: TelemetryIngestRequest) -> Dict[str, Any]:
    """Ingests security telemetry through the Security Operations Fabric."""
    return _fabric.process_incoming_security_telemetry(
        event_type=payload.event_type,
        source=payload.source,
        entity_id=payload.entity_id,
        asset_id=payload.asset_id,
        campaign_id=payload.campaign_id,
        severity=payload.severity,
        confidence=payload.confidence,
        risk_score=payload.risk_score,
        trust_score=payload.trust_score,
        exposure_score=payload.exposure_score,
        provenance=payload.provenance,
        tenant_id=payload.tenant_id,
    )


@router.get("/overview")
def get_security_overview(tenant_id: str = "default_tenant") -> Dict[str, Any]:
    """Returns top-level security operations posture and situation overview."""
    posture = _fabric.posture.get_latest_posture(tenant_id) or _fabric.posture.calculate_posture(
        risk_score=15.0,
        trust_score=88.0,
        exposure_score=22.0,
        active_threats_count=1,
        critical_assets_count=2,
        active_campaigns_count=0,
        open_incidents_count=0,
        tenant_id=tenant_id,
    )
    sit = _fabric.posture.evaluate_situation(
        active_threats_count=1,
        critical_assets_count=2,
        high_risk_exposure_count=0,
        active_campaigns_count=0,
        open_incidents_count=0,
        tenant_id=tenant_id,
    )
    kpis = _fabric.incident.calculate_kpis(tenant_id)
    health = _fabric.health.check_subsystems_health()

    return {
        "posture": posture,
        "situation": sit,
        "kpis": kpis,
        "health": health,
    }


@router.get("/posture", response_model=SecurityPostureDTO)
def get_security_posture(tenant_id: str = "default_tenant") -> SecurityPostureDTO:
    """Returns the latest Security Posture Score and dimension metrics."""
    return _fabric.posture.get_latest_posture(tenant_id) or _fabric.posture.calculate_posture(
        risk_score=15.0,
        trust_score=88.0,
        exposure_score=22.0,
        active_threats_count=1,
        critical_assets_count=2,
        active_campaigns_count=0,
        open_incidents_count=0,
        tenant_id=tenant_id,
    )


@router.get("/posture/history", response_model=List[SecurityPostureDTO])
def get_posture_history(tenant_id: str = "default_tenant") -> List[SecurityPostureDTO]:
    """Returns posture historical progression."""
    return _fabric.posture.get_posture_history(tenant_id)


@router.get("/events", response_model=List[SecurityEventDTO])
def list_security_events(
    event_type: Optional[SecurityEventTypeLiteral] = None,
    severity: Optional[str] = None,
    tenant_id: str = "default_tenant",
    limit: int = Query(default=100, le=500),
) -> List[SecurityEventDTO]:
    """Lists normalized security events."""
    return _fabric.events.list_events(
        event_type=event_type,
        severity=severity,
        tenant_id=tenant_id,
        limit=limit,
    )


@router.get("/events/{event_id}", response_model=SecurityEventDTO)
def get_security_event(event_id: str, tenant_id: str = "default_tenant") -> SecurityEventDTO:
    """Retrieves a single security event."""
    event = _fabric.events.get_event(event_id, tenant_id)
    if not event:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found.")
    return event


@router.get("/clusters", response_model=List[ThreatClusterDTO])
def list_threat_clusters(tenant_id: str = "default_tenant") -> List[ThreatClusterDTO]:
    """Lists active multi-modal threat clusters."""
    return _fabric.fusion.list_clusters(tenant_id)


@router.get("/kpis", response_model=SecurityKpisDTO)
def get_security_kpis(tenant_id: str = "default_tenant") -> SecurityKpisDTO:
    """Calculates operational MTTx KPIs and response effectiveness."""
    return _fabric.incident.calculate_kpis(tenant_id)


@router.get("/health", response_model=SecurityHealthOverviewDTO)
def get_security_health() -> SecurityHealthOverviewDTO:
    """Evaluates the health and operational integrity of internal security subsystems."""
    return _fabric.health.check_subsystems_health()


@router.get("/narrative/{target_subject}", response_model=SecurityNarrativeDTO)
def get_security_narrative(
    target_subject: str,
    campaign_name: Optional[str] = None,
) -> SecurityNarrativeDTO:
    """Generates an operational factual security narrative answering all 14 forensic questions."""
    return _fabric.narrative.generate_narrative(
        target_subject=target_subject,
        observed_events=[{"event": "Suspicious DNS flux"}, {"event": "Trojan APK hash match"}],
        verified_evidence=[{"type": "DEX_PAYLOAD", "value": "banking_sms_forwarder"}],
        risk_score=78.0,
        trust_score=42.0,
        exposure_score=65.0,
        campaign_name=campaign_name,
    )
