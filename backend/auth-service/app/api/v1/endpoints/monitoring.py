"""FastAPI Endpoints for Continuous Intelligence & Real-Time Monitoring (Phase 4.0 Part 6 — Sections 99-104)."""

from typing import List, Dict, Any, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.schemas.continuous_intelligence_models import (
    ThreatFeedConfigurationDTO,
    ThreatFeedSyncResponseDTO,
    SecurityAlertDTO,
    SecurityIncidentDTO,
    IntelligenceEventDTO,
    RealtimeSubscriptionDTO,
    AlertAcknowledgeRequestDTO,
    AlertEscalateRequestDTO,
    AlertSuppressRequestDTO,
)
from app.services.trust_monitoring_engine import TrustMonitoringEngine

router = APIRouter()

# Global monitoring engine instance
monitoring_engine = TrustMonitoringEngine()


# ============================================================================
# Threat Feed Management Endpoints (Section 99)
# ============================================================================

@router.post("/intelligence/feeds", response_model=Dict[str, Any], status_code=status.HTTP_201_CREATED)
async def create_feed(
    payload: ThreatFeedConfigurationDTO,
    current_user: User = Depends(get_current_user),
):
    feed = monitoring_engine.register_feed(payload)
    return {"success": True, "message": "Threat feed registered successfully", "data": feed}


@router.get("/intelligence/feeds", response_model=Dict[str, Any])
async def list_feeds(
    current_user: User = Depends(get_current_user),
):
    feeds = monitoring_engine.list_feeds()
    return {"success": True, "message": "Threat feeds retrieved", "data": feeds}


@router.get("/intelligence/feeds/{feed_id}", response_model=Dict[str, Any])
async def get_feed(
    feed_id: str,
    current_user: User = Depends(get_current_user),
):
    feed = monitoring_engine.get_feed(feed_id)
    if not feed:
        raise HTTPException(status_code=404, detail="Feed not found")
    return {"success": True, "message": "Threat feed retrieved", "data": feed}


@router.post("/intelligence/feeds/{feed_id}/sync", response_model=Dict[str, Any])
async def sync_feed(
    feed_id: str,
    current_user: User = Depends(get_current_user),
):
    try:
        res = monitoring_engine.sync_feed(feed_id)
        return {"success": True, "message": "Threat feed synchronized", "data": res}
    except KeyError:
        raise HTTPException(status_code=404, detail="Feed not found")


# ============================================================================
# Security Alerts Endpoints (Section 100)
# ============================================================================

@router.get("/security/alerts", response_model=Dict[str, Any])
async def list_alerts(
    status: Optional[str] = Query(None),
    priority: Optional[str] = Query(None),
    case_id: Optional[str] = Query(None),
    current_user: User = Depends(get_current_user),
):
    alerts = monitoring_engine.list_alerts(status=status, priority=priority, case_id=case_id)
    return {"success": True, "message": "Security alerts retrieved", "data": alerts}


@router.get("/security/alerts/{alert_id}", response_model=Dict[str, Any])
async def get_alert(
    alert_id: str,
    current_user: User = Depends(get_current_user),
):
    alert = monitoring_engine.get_alert(alert_id)
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    return {"success": True, "message": "Security alert retrieved", "data": alert}


@router.post("/security/alerts/{alert_id}/acknowledge", response_model=Dict[str, Any])
async def acknowledge_alert(
    alert_id: str,
    payload: AlertAcknowledgeRequestDTO,
    current_user: User = Depends(get_current_user),
):
    try:
        alert, ack = monitoring_engine.acknowledge_alert(
            alert_id=alert_id,
            user_id=str(current_user.id),
            user_name=current_user.email,
            reason=payload.reason,
            comment=payload.comment,
        )
        return {"success": True, "message": "Alert acknowledged", "data": {"alert": alert, "acknowledgement": ack}}
    except KeyError:
        raise HTTPException(status_code=404, detail="Alert not found")


@router.post("/security/alerts/{alert_id}/escalate", response_model=Dict[str, Any])
async def escalate_alert(
    alert_id: str,
    payload: AlertEscalateRequestDTO,
    current_user: User = Depends(get_current_user),
):
    try:
        alert, esc = monitoring_engine.escalate_alert(
            alert_id=alert_id,
            new_priority=payload.priority,
            reason=payload.reason,
            escalated_by=current_user.email,
        )
        return {"success": True, "message": "Alert escalated", "data": {"alert": alert, "escalation": esc}}
    except KeyError:
        raise HTTPException(status_code=404, detail="Alert not found")


@router.post("/security/alerts/{alert_id}/suppress", response_model=Dict[str, Any])
async def suppress_alert(
    alert_id: str,
    payload: AlertSuppressRequestDTO,
    current_user: User = Depends(get_current_user),
):
    try:
        alert, supp = monitoring_engine.suppress_alert(
            alert_id=alert_id,
            reason=payload.reason,
            suppressed_by=current_user.email,
            duration_hours=payload.duration_hours or 24,
        )
        return {"success": True, "message": "Alert suppressed", "data": {"alert": alert, "suppression": supp}}
    except KeyError:
        raise HTTPException(status_code=404, detail="Alert not found")


@router.post("/security/alerts/{alert_id}/resolve", response_model=Dict[str, Any])
async def resolve_alert(
    alert_id: str,
    current_user: User = Depends(get_current_user),
):
    try:
        alert = monitoring_engine.resolve_alert(alert_id)
        return {"success": True, "message": "Alert resolved", "data": alert}
    except KeyError:
        raise HTTPException(status_code=404, detail="Alert not found")


# ============================================================================
# Security Incidents Endpoints (Section 101)
# ============================================================================

@router.get("/security/incidents", response_model=Dict[str, Any])
async def list_incidents(
    current_user: User = Depends(get_current_user),
):
    incidents = monitoring_engine.list_incidents()
    return {"success": True, "message": "Security incidents retrieved", "data": incidents}


@router.get("/security/incidents/{incident_id}", response_model=Dict[str, Any])
async def get_incident(
    incident_id: str,
    current_user: User = Depends(get_current_user),
):
    inc = monitoring_engine.get_incident(incident_id)
    if not inc:
        raise HTTPException(status_code=404, detail="Incident not found")
    return {"success": True, "message": "Security incident retrieved", "data": inc}


# ============================================================================
# Real-Time & Event Endpoints (Section 102)
# ============================================================================

@router.get("/realtime/events", response_model=Dict[str, Any])
async def list_realtime_events(
    current_user: User = Depends(get_current_user),
):
    events = monitoring_engine.list_events()
    return {"success": True, "message": "Real-time events retrieved", "data": events}
