"""
TruthShield X — Closed-Loop SOC Orchestration Endpoints (Phase 21).

REST API endpoints for Alert Processing, Priority, State Machine, Blast Radius, Playbooks, Action Verification,
Emergency Controls, and SOC Scorecards.
"""

from typing import List, Optional, Dict, Any
from fastapi import APIRouter, Query, HTTPException, status, Body
from app.schemas.autonomous_soc_models import (
    SOCAlertNormalizedDTO,
    AlertClusterDTO,
    AlertPriorityDTO,
    IncidentStateMachineDTO,
    IncidentBlastRadiusDTO,
    ResponsePlanDetailedDTO,
    SecurePlaybookDTO,
    PlaybookValidationResultDTO,
    ResponseActionExecutionDTO,
    ActionVerificationResultDTO,
    AutomationGuardrailsDTO,
    SecurityCaseDTO,
    SOCScorecardDTO,
)
from app.services.soc.security_operations_orchestrator import SecurityOperationsOrchestrator

router = APIRouter(prefix="/soc-orchestration", tags=["Autonomous SOC Orchestration & Closed-Loop Defense"])
orchestrator = SecurityOperationsOrchestrator()


@router.post("/alerts", response_model=SOCAlertNormalizedDTO)
def ingest_alert(payload: Dict[str, Any] = Body(...), tenant_id: str = Query("default_tenant")):
    """Ingests and normalizes an alert."""
    return orchestrator.ingest_alert(
        tenant_id=tenant_id,
        source=payload.get("source", "SIEM_CONNECTOR"),
        asset=payload.get("asset", "srv_checkout_production"),
        severity=payload.get("severity", "HIGH"),
        confidence=payload.get("confidence", 0.92),
        evidence=payload.get("evidence", ["ev_pcap_88"]),
        indicator=payload.get("indicator", "198.51.100.42"),
    )


@router.get("/alerts/clusters", response_model=List[AlertClusterDTO])
def list_alert_clusters(tenant_id: str = Query("default_tenant")):
    """Retrieves deduplicated alert clusters."""
    return orchestrator.correlate_and_cluster(tenant_id)


@router.post("/alerts/{alert_id}/priority", response_model=AlertPriorityDTO)
def compute_alert_priority(alert_id: str):
    """Computes explainable alert priority score."""
    alert = orchestrator._alerts.get(alert_id)
    if not alert:
        alert = SOCAlertNormalizedDTO(alert_id=alert_id, source="SIEM", asset="srv_checkout")
    return orchestrator.priority_engine.compute_priority(alert)


@router.post("/incidents/{incident_id}/transition", response_model=IncidentStateMachineDTO)
def transition_incident_state(incident_id: str, payload: Dict[str, Any] = Body(...)):
    """Executes validated incident lifecycle state transition."""
    new_state = payload.get("new_state", "TRIAGED")
    actor = payload.get("actor", "usr_analyst_01")
    try:
        return orchestrator.state_machine.transition(incident_id, new_state, actor)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/incidents/{incident_id}/blast-radius", response_model=IncidentBlastRadiusDTO)
def evaluate_blast_radius(incident_id: str, payload: Dict[str, Any] = Body(...)):
    """Computes observed vs potential blast radius."""
    observed = payload.get("observed_assets", ["srv_checkout_production"])
    deps = payload.get("dependency_map", {"srv_checkout_production": ["srv_payment_gateway", "db_primary_users"]})
    return orchestrator.blast_radius_engine.evaluate_blast_radius(incident_id, observed, deps)


@router.post("/incidents/{incident_id}/response-plan", response_model=ResponsePlanDetailedDTO)
def generate_response_plan(incident_id: str, payload: Dict[str, Any] = Body(...)):
    """Generates structured response plan with safety checks."""
    target = payload.get("target_resource", "srv_checkout_production")
    threat_type = payload.get("threat_type", "RCE_CONTAINMENT")
    return orchestrator.plan_generator.generate_plan(incident_id, target, threat_type)


@router.get("/playbooks", response_model=List[SecurePlaybookDTO])
def list_playbooks(tenant_id: str = Query("default_tenant")):
    """Lists registered SOAR defensive playbooks."""
    return orchestrator.playbook_engine.list_playbooks(tenant_id)


@router.post("/playbooks/validate", response_model=PlaybookValidationResultDTO)
def validate_playbook(payload: Dict[str, Any] = Body(...)):
    """Validates structural safety and approval requirements of a playbook."""
    pb_id = payload.get("playbook_id", "pb_phishing_containment")
    pb = orchestrator.playbook_engine.get_playbook(pb_id)
    if not pb:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Playbook not found.")
    return orchestrator.playbook_validator.validate_playbook(pb)


@router.post("/actions/execute", response_model=Dict[str, Any])
def execute_action(payload: Dict[str, Any] = Body(...), tenant_id: str = Query("default_tenant")):
    """Executes an action with Four-Eyes authorization check and empirical verification."""
    incident_id = payload.get("incident_id", "inc_01")
    target = payload.get("target", "srv_checkout_production")
    requester = payload.get("requester_id", "usr_analyst_01")
    approver = payload.get("approver_id", "usr_admin_01")

    try:
        action, ver = orchestrator.execute_and_verify_action(
            incident_id=incident_id,
            target=target,
            requester_id=requester,
            approver_id=approver,
            tenant_id=tenant_id,
        )
        return {"action": action.model_dump(), "verification": ver.model_dump()}
    except (PermissionError, RuntimeError) as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))


@router.post("/automation/pause", response_model=AutomationGuardrailsDTO)
def pause_automation(payload: Dict[str, Any] = Body(...), tenant_id: str = Query("default_tenant")):
    """Emergency Pause Stop for all automated actions."""
    user = payload.get("user_id", "usr_soc_lead")
    reason = payload.get("reason", "Manual emergency stop triggered from SOC console.")
    return orchestrator.guardrails_engine.pause_automation(tenant_id, user, reason)


@router.post("/automation/resume", response_model=AutomationGuardrailsDTO)
def resume_automation(payload: Dict[str, Any] = Body(...), tenant_id: str = Query("default_tenant")):
    """Resumes automation following emergency stop."""
    user = payload.get("user_id", "usr_soc_lead")
    return orchestrator.guardrails_engine.resume_automation(tenant_id, user)


@router.get("/scorecard", response_model=SOCScorecardDTO)
def get_soc_scorecard(tenant_id: str = Query("default_tenant")):
    """Returns SOC Health Scorecard and performance SLA metrics."""
    return orchestrator.scorecard_engine.compute_scorecard(tenant_id)
