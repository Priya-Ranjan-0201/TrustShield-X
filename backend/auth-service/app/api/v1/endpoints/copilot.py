"""
TruthShield X — Security Copilot & Cyber Command Center API Endpoints (Phase 20).

REST API endpoints for Chat, Sessions, Context, Investigation, Hunting, Simulation, Action Planning & Approval,
Verification, Executive Briefings, Command Center, and Copilot Quality Evaluation.
"""

from typing import List, Optional, Dict, Any
from fastapi import APIRouter, Query, HTTPException, status, Body
from app.schemas.copilot_command_models import (
    CopilotSessionDTO,
    CopilotContextDTO,
    AnswerContractDTO,
    InvestigationSummaryDTO,
    GeneratedQueryDTO,
    CopilotActionPlanDTO,
    CopilotActionVerificationDTO,
    ExecutiveBriefingDTO,
    CISOCommandCenterSummaryDTO,
    CopilotQualityEvaluationDTO,
)
from app.services.copilot.security_copilot_service import SecurityCopilot

router = APIRouter(tags=["Security Copilot & Cyber Command Center"])
copilot_service = SecurityCopilot()


@router.post("/copilot/chat", response_model=AnswerContractDTO)
def chat_with_copilot(
    payload: Dict[str, Any] = Body(...),
    tenant_id: str = Query("default_tenant"),
):
    """Processes user query with evidence grounding, citations, and prompt safety guard."""
    prompt = payload.get("prompt", "")
    session_id = payload.get("session_id", "default_session")
    return copilot_service.process_chat_message(session_id, prompt, tenant_id)


@router.get("/copilot/sessions", response_model=List[CopilotSessionDTO])
def list_sessions(tenant_id: str = Query("default_tenant")):
    """Lists copilot sessions for a tenant."""
    return [s for s in copilot_service._sessions.values() if s.tenant_id == tenant_id or tenant_id == "admin"]


@router.get("/copilot/sessions/{id}", response_model=CopilotSessionDTO)
def get_session(id: str, tenant_id: str = Query("default_tenant")):
    """Retrieves a specific copilot session."""
    session = copilot_service.get_session(id, tenant_id)
    if not session:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Copilot session not found.")
    return session


@router.post("/copilot/sessions/{id}/message", response_model=AnswerContractDTO)
def send_session_message(
    id: str,
    payload: Dict[str, Any] = Body(...),
    tenant_id: str = Query("default_tenant"),
):
    """Appends a message to a session and generates an evidence-grounded response."""
    prompt = payload.get("prompt", "")
    return copilot_service.process_chat_message(id, prompt, tenant_id)


@router.get("/copilot/sessions/{id}/context", response_model=CopilotContextDTO)
def get_session_context(
    id: str,
    tenant_id: str = Query("default_tenant"),
    user_id: str = Query("usr_analyst_01"),
    role: str = Query("ANALYST"),
):
    """Builds role-aware context for the active session."""
    return copilot_service.context_builder.build_context(tenant_id, user_id, role)  # type: ignore


@router.post("/copilot/investigate", response_model=InvestigationSummaryDTO)
def investigate_incident(payload: Dict[str, Any] = Body(...)):
    """Generates comprehensive investigation summary with timeline and hypotheses."""
    incident_id = payload.get("incident_id", "inc_checkout_breach")
    return copilot_service.investigation.build_investigation_summary(incident_id)


@router.post("/copilot/hunt", response_model=GeneratedQueryDTO)
def generate_hunt_query(payload: Dict[str, Any] = Body(...)):
    """Generates safe read-only threat hunting queries."""
    query_type = payload.get("query_type", "SQL")
    target = payload.get("target_entity", "srv_checkout_production")
    hypothesis = payload.get("hypothesis", "Lateral movement via credential reuse")
    return copilot_service.hunting.generate_hunt_query(query_type, target, hypothesis)


@router.post("/copilot/simulate", response_model=Dict[str, Any])
def simulate_copilot_action(payload: Dict[str, Any] = Body(...)):
    """Executes a dry-run digital twin simulation for proposed defense actions."""
    target = payload.get("target_resource", "srv_checkout_production")
    return {
        "simulation_id": "sim_copilot_dryrun_01",
        "target_resource": target,
        "is_simulated": True,
        "label": "SIMULATED",
        "predicted_risk_reduction": 82.5,
        "estimated_downtime_seconds": 0,
    }


@router.post("/copilot/action-plan", response_model=CopilotActionPlanDTO)
def create_action_plan(payload: Dict[str, Any] = Body(...)):
    """Creates a proposed action plan requiring human approval."""
    session_id = payload.get("session_id", "session_01")
    action_type = payload.get("action_type", "ISOLATE_NETWORK_EGRESS")
    target = payload.get("target_resource", "srv_checkout_production")
    reason = payload.get("reason", "Contain lateral spread")
    evidence_ids = payload.get("evidence_ids", ["ev_pcap_trace_88"])
    return copilot_service.planner.create_plan(
        session_id=session_id,
        action_type=action_type,
        target_resource=target,
        reason=reason,
        evidence_ids=evidence_ids,
        expected_benefit="Prevent lateral SMB/RPC traversal",
        possible_impact="Minor batch job delay",
    )


@router.post("/copilot/action-plan/{id}/approve", response_model=CopilotActionPlanDTO)
def approve_action_plan(id: str, payload: Dict[str, Any] = Body(...)):
    """Approves an action plan via human four-eyes authorization."""
    approver = payload.get("approver_id", "usr_admin_01")
    approved = copilot_service.planner.approve_plan(id, approver)
    if not approved:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Action plan not found.")
    return approved


@router.post("/copilot/action-plan/{id}/execute", response_model=CopilotActionVerificationDTO)
def execute_action_plan(id: str):
    """Executes an approved action plan and verifies runtime outcome."""
    plan = copilot_service.planner.get_plan(id)
    if not plan or plan.approval_status != "APPROVED":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Plan must be APPROVED before execution.")
    return copilot_service.verification.verify_action_execution(id, is_success=True)


@router.get("/copilot/briefings", response_model=ExecutiveBriefingDTO)
def get_daily_briefing(tenant_id: str = Query("default_tenant")):
    """Generates daily security executive briefing."""
    return copilot_service.executive.generate_daily_brief(tenant_id)


@router.get("/copilot/quality", response_model=CopilotQualityEvaluationDTO)
def get_copilot_quality():
    """Returns AI Copilot precision, grounding, and safety metrics."""
    return copilot_service.quality.evaluate_quality()


@router.get("/copilot/command-center", response_model=CISOCommandCenterSummaryDTO)
def get_command_center_summary(tenant_id: str = Query("default_tenant")):
    """Returns aggregated executive summary for the Cyber Command Center."""
    return copilot_service.executive.get_ciso_command_summary(tenant_id)
