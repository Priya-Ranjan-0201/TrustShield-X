"""
TruthShield X — Global Security Mission Control REST API (Phase 29).
"""

from typing import List, Dict, Any, Optional
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel

from app.schemas.mission_control_os_models import (
    UnifiedSecurityStateDTO,
    SecurityEventDTO,
    MissionTaskDTO,
    MissionWorkflowDTO,
    SecurityPostureDTO,
    IncidentCommandMissionDTO,
    MissionControlHealthDTO,
    StateConflictDTO,
)
from app.services.mission_control_os.global_security_mission_control_engine import GlobalSecurityMissionControlEngine

router = APIRouter(prefix="/mission-control-os", tags=["Global Security Mission Control Operating System"])

# Singleton Engine Instance
mission_control_os_engine = GlobalSecurityMissionControlEngine()


# ============================================================================
# Overview, State & Posture
# ============================================================================

@router.get("/overview", response_model=Dict[str, Any])
def get_mission_overview(tenant_id: str = Query("default_tenant")):
    return mission_control_os_engine.get_mission_overview(tenant_id)


@router.get("/state", response_model=UnifiedSecurityStateDTO)
def get_unified_security_state(tenant_id: str = Query("default_tenant")):
    return mission_control_os_engine.state_engine.get_unified_state(tenant_id)


@router.get("/posture", response_model=SecurityPostureDTO)
def get_security_posture():
    return mission_control_os_engine.posture_engine.evaluate_posture()


@router.get("/situational-awareness", response_model=Dict[str, Any])
def get_situational_awareness(tenant_id: str = Query("default_tenant")):
    return mission_control_os_engine.situational_engine.get_situational_overview(tenant_id)


# ============================================================================
# Events & Event Fabric
# ============================================================================

@router.get("/events", response_model=List[SecurityEventDTO])
def list_security_events(tenant_id: str = Query("default_tenant")):
    return mission_control_os_engine.event_fabric.list_events(tenant_id)


class IngestEventRequest(BaseModel):
    event_type: str = "ALERT_CREATED"
    source: str = "soc_orchestrator"
    payload: Dict[str, Any]
    idempotency_key: str
    tenant_id: str = "default_tenant"
    confidence: float = 0.95


@router.post("/events", response_model=Dict[str, Any])
def ingest_security_event(payload: IngestEventRequest):
    return mission_control_os_engine.event_fabric.publish_event(
        event_type=payload.event_type,  # type: ignore
        source=payload.source,
        payload=payload.payload,
        idempotency_key=payload.idempotency_key,
        tenant_id=payload.tenant_id,
        confidence=payload.confidence,
    )


# ============================================================================
# Incidents & Timeline
# ============================================================================

@router.get("/incidents", response_model=List[IncidentCommandMissionDTO])
def list_mission_incidents():
    return mission_control_os_engine.incident_engine.list_incidents()


@router.get("/incidents/{incident_id}/timeline", response_model=List[Dict[str, str]])
def get_incident_verified_timeline(incident_id: str):
    return mission_control_os_engine.incident_engine.get_verified_timeline(incident_id)


# ============================================================================
# Tasks & SLA
# ============================================================================

@router.get("/tasks", response_model=List[MissionTaskDTO])
def list_mission_tasks():
    return mission_control_os_engine.task_engine.list_tasks()


class CreateTaskRequest(BaseModel):
    title: str
    task_type: str = "INVESTIGATE"
    owner: str = "SOC_ANALYST"
    priority: str = "HIGH"
    sla_seconds: float = 1800.0
    dependencies: Optional[List[str]] = None


@router.post("/tasks", response_model=MissionTaskDTO)
def create_mission_task(payload: CreateTaskRequest):
    return mission_control_os_engine.task_engine.create_task(
        title=payload.title,
        task_type=payload.task_type,
        owner=payload.owner,
        priority=payload.priority,  # type: ignore
        sla_seconds=payload.sla_seconds,
        dependencies=payload.dependencies,
    )


@router.get("/sla/evaluate", response_model=Dict[str, Any])
def evaluate_task_sla(task_id: str = Query(...), allocated: float = Query(1800.0), elapsed: float = Query(600.0)):
    return mission_control_os_engine.sla_engine.evaluate_task_sla(
        task_id=task_id,
        allocated_sla_seconds=allocated,
        elapsed_seconds=elapsed,
    )


# ============================================================================
# Workflows & Health
# ============================================================================

@router.get("/workflows", response_model=List[MissionWorkflowDTO])
def list_mission_workflows():
    return mission_control_os_engine.workflow_orchestrator.list_workflows()


@router.get("/health", response_model=MissionControlHealthDTO)
def get_mission_control_health():
    return mission_control_os_engine.health_engine.check_health()


@router.get("/conflicts", response_model=List[StateConflictDTO])
def list_state_conflicts():
    return mission_control_os_engine.conflict_engine.list_conflicts()
