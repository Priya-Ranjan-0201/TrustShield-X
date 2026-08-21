"""FastAPI Endpoints for SOC Intelligence, Incident Response & SOAR Foundation (Phase 4.0 Part 7 — Sections 75-78)."""

from typing import List, Dict, Any, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel
from app.api.deps import get_current_user
from app.models.user import User
from app.schemas.soc_operations_models import (
    SOCAlertDTO,
    SecurityIncidentDTO,
    TriageResultDTO,
    ResponsePlaybookDTO,
    ResponseActionDTO,
    ApprovalRequestDTO,
    EvidenceCollectionRecordDTO,
)
from app.services.soc_operations_engine import SOCOperationsEngine

router = APIRouter(prefix="/soc", tags=["Security Operations Center (SOC) & Incident Response"])

# Global SOC engine instance
soc_engine = SOCOperationsEngine()


class ActionCreateRequest(BaseModel):
    action_type: str
    target: str
    reason: str
    requires_approval: bool = True


class ApprovalDecisionRequest(BaseModel):
    reason: str = "Approved from SOC Console"


class AssignRequest(BaseModel):
    analyst_id: str


class MergeRequest(BaseModel):
    merged_incident_ids: List[str]
    reason: str


class SplitRequest(BaseModel):
    new_incident_titles: List[str]
    reason: str


# ============================================================================
# SOC Alerts Endpoints (Section 75)
# ============================================================================

@router.get("/alerts", response_model=Dict[str, Any])
async def list_alerts(
    current_user: User = Depends(get_current_user),
):
    alerts = soc_engine.list_alerts()
    return {"success": True, "message": "SOC alerts retrieved", "data": alerts}


@router.get("/alerts/{alert_id}", response_model=Dict[str, Any])
async def get_alert(
    alert_id: str,
    current_user: User = Depends(get_current_user),
):
    alert = next((a for a in soc_engine.list_alerts() if a.alert_id == alert_id), None)
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    return {"success": True, "message": "SOC alert retrieved", "data": alert}


# ============================================================================
# Security Incidents Endpoints (Section 75)
# ============================================================================

@router.get("/incidents", response_model=Dict[str, Any])
async def list_incidents(
    current_user: User = Depends(get_current_user),
):
    incidents = soc_engine.list_incidents()
    return {"success": True, "message": "Security incidents retrieved", "data": incidents}


@router.get("/incidents/{incident_id}", response_model=Dict[str, Any])
async def get_incident(
    incident_id: str,
    current_user: User = Depends(get_current_user),
):
    incident = soc_engine.get_incident(incident_id)
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")
    return {"success": True, "message": "Security incident retrieved", "data": incident}


@router.post("/incidents/{incident_id}/assign", response_model=Dict[str, Any])
async def assign_incident(
    incident_id: str,
    payload: AssignRequest,
    current_user: User = Depends(get_current_user),
):
    try:
        incident = soc_engine.assign_incident(
            incident_id=incident_id,
            analyst_id=payload.analyst_id,
            assigned_by=current_user.email,
        )
        return {"success": True, "message": "Incident assigned", "data": incident}
    except KeyError:
        raise HTTPException(status_code=404, detail="Incident not found")


@router.post("/incidents/{incident_id}/triage", response_model=Dict[str, Any])
async def triage_incident(
    incident_id: str,
    current_user: User = Depends(get_current_user),
):
    try:
        triage = soc_engine.triage_incident(incident_id)
        return {"success": True, "message": "Automated triage completed", "data": triage}
    except KeyError:
        raise HTTPException(status_code=404, detail="Incident not found")


@router.post("/incidents/{incident_id}/merge", response_model=Dict[str, Any])
async def merge_incidents(
    incident_id: str,
    payload: MergeRequest,
    current_user: User = Depends(get_current_user),
):
    try:
        primary, rec = soc_engine.incident_engine.merge_incidents(
            primary_incident_id=incident_id,
            merged_incident_ids=payload.merged_incident_ids,
            merged_by=current_user.email,
            reason=payload.reason,
        )
        return {"success": True, "message": "Incidents merged", "data": {"incident": primary, "merge_record": rec}}
    except KeyError:
        raise HTTPException(status_code=404, detail="Incident not found")


@router.post("/incidents/{incident_id}/split", response_model=Dict[str, Any])
async def split_incident(
    incident_id: str,
    payload: SplitRequest,
    current_user: User = Depends(get_current_user),
):
    try:
        orig, new_incs, rec = soc_engine.incident_engine.split_incident(
            original_incident_id=incident_id,
            split_by=current_user.email,
            reason=payload.reason,
            new_incident_titles=payload.new_incident_titles,
        )
        return {"success": True, "message": "Incident split", "data": {"original": orig, "new_incidents": new_incs, "split_record": rec}}
    except KeyError:
        raise HTTPException(status_code=404, detail="Incident not found")


# ============================================================================
# Playbook Endpoints (Section 76)
# ============================================================================

@router.get("/playbooks", response_model=Dict[str, Any])
async def list_playbooks(
    current_user: User = Depends(get_current_user),
):
    playbooks = soc_engine.playbook_engine.list_playbooks()
    return {"success": True, "message": "Response playbooks retrieved", "data": playbooks}


@router.get("/playbooks/{playbook_id}", response_model=Dict[str, Any])
async def get_playbook(
    playbook_id: str,
    current_user: User = Depends(get_current_user),
):
    pb = soc_engine.playbook_engine.get_playbook(playbook_id)
    if not pb:
        raise HTTPException(status_code=404, detail="Playbook not found")
    return {"success": True, "message": "Response playbook retrieved", "data": pb}


# ============================================================================
# Response Actions & Approvals Endpoints (Section 77)
# ============================================================================

@router.post("/incidents/{incident_id}/actions", response_model=Dict[str, Any])
async def create_action(
    incident_id: str,
    payload: ActionCreateRequest,
    current_user: User = Depends(get_current_user),
):
    try:
        action, approval = soc_engine.create_response_action(
            incident_id=incident_id,
            action_type=payload.action_type,
            target=payload.target,
            requested_by=current_user.email,
            reason=payload.reason,
            requires_approval=payload.requires_approval,
        )
        return {"success": True, "message": "Response action created", "data": {"action": action, "approval": approval}}
    except KeyError:
        raise HTTPException(status_code=404, detail="Incident not found")


@router.post("/actions/{action_id}/simulate", response_model=Dict[str, Any])
async def simulate_action(
    action_id: str,
    current_user: User = Depends(get_current_user),
):
    action = soc_engine._actions.get(action_id)
    if not action:
        raise HTTPException(status_code=404, detail="Action not found")
    sim = soc_engine.simulation_engine.simulate_action(action)
    return {"success": True, "message": "Dry-run simulation completed", "data": sim}


@router.post("/approvals/{approval_id}/approve", response_model=Dict[str, Any])
async def approve_action_endpoint(
    approval_id: str,
    payload: ApprovalDecisionRequest,
    current_user: User = Depends(get_current_user),
):
    try:
        action = soc_engine.approve_action(approval_id, approver_id=current_user.email, reason=payload.reason)
        return {"success": True, "message": "Action approved", "data": action}
    except Exception as ex:
        raise HTTPException(status_code=400, detail=str(ex))


@router.post("/approvals/{approval_id}/reject", response_model=Dict[str, Any])
async def reject_action_endpoint(
    approval_id: str,
    payload: ApprovalDecisionRequest,
    current_user: User = Depends(get_current_user),
):
    try:
        action = soc_engine.reject_action(approval_id, approver_id=current_user.email, reason=payload.reason)
        return {"success": True, "message": "Action rejected", "data": action}
    except Exception as ex:
        raise HTTPException(status_code=400, detail=str(ex))


@router.post("/actions/{action_id}/execute", response_model=Dict[str, Any])
async def execute_action_endpoint(
    action_id: str,
    current_user: User = Depends(get_current_user),
):
    try:
        action, exec_dto, ver_dto = soc_engine.execute_action(action_id)
        return {
            "success": True,
            "message": "Action executed and verified",
            "data": {"action": action, "execution": exec_dto, "verification": ver_dto},
        }
    except Exception as ex:
        raise HTTPException(status_code=400, detail=str(ex))


@router.post("/actions/{action_id}/rollback", response_model=Dict[str, Any])
async def rollback_action_endpoint(
    action_id: str,
    current_user: User = Depends(get_current_user),
):
    try:
        action, rol_dto = soc_engine.rollback_action(action_id, executed_by=current_user.email)
        return {"success": True, "message": "Rollback completed", "data": {"action": action, "rollback": rol_dto}}
    except Exception as ex:
        raise HTTPException(status_code=400, detail=str(ex))


# ============================================================================
# Evidence Endpoints (Section 78)
# ============================================================================

@router.get("/incidents/{incident_id}/evidence", response_model=Dict[str, Any])
async def list_incident_evidence(
    incident_id: str,
    current_user: User = Depends(get_current_user),
):
    ev_list = soc_engine.evidence_engine.list_incident_evidence(incident_id)
    return {"success": True, "message": "Incident evidence retrieved", "data": ev_list}
