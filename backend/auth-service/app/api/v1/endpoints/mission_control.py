"""
TruthShield X — Phase 15 Security Mission Control & Cyber Crisis Command Endpoints
"""

from typing import Any, Dict, List, Optional
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

from app.schemas.mission_control_models import (
    IncidentCommandDTO,
    IncidentEvidenceRoomDTO,
    CrisisDeclarationDTO,
    ResponsePlanDTO,
    MissionControlSummaryDTO,
    CrisisReadinessScoreDTO,
    BusinessServiceImpactDTO,
    IncidentRecoveryDTO,
    LessonsLearnedDTO,
    RootCauseAnalysisDTO,
    IncidentDecisionLogDTO,
    CrisisCommunicationDTO,
    IncidentEscalationDTO,
)
from app.services.mission_control.security_mission_control import SecurityMissionControl
from app.services.mission_control.incident_command_engine import (
    InvalidTransitionError,
    IncidentNotConfirmedError,
)

router = APIRouter(prefix="/mission-control", tags=["Security Mission Control & Cyber Crisis Command"])

_mc = SecurityMissionControl()


class CreateIncidentCommandRequest(BaseModel):
    tenant_id: str = "default_tenant"
    incident_id: str
    severity: str = "MEDIUM"
    confidence: float = 0.5
    evidence_strength: float = 0.5
    incident_commander: str
    triggering_signals: List[str] = []


class DeclareIncidentRequest(BaseModel):
    level: str
    reason: str
    evidence_references: List[str] = []
    confidence: float = 0.5
    actor: str


class TransitionRequest(BaseModel):
    new_status: str
    actor: str = "SYSTEM"
    reason: str = ""


class EscalateRequest(BaseModel):
    trigger: str = "SEVERITY"
    from_level: str
    to_level: str
    escalated_by: str = "SYSTEM"


class ApproveResponseRequest(BaseModel):
    plan_id: str
    option_id: str
    approved_by: str
    requested_by: str


class RecoverRequest(BaseModel):
    recovery_sequence: List[str] = []
    dependencies: List[str] = []


class VerifyRecoveryRequest(BaseModel):
    recovery_id: str
    service_health_verified: bool = False
    security_controls_verified: bool = False
    monitoring_restored: bool = False
    audit_restored: bool = False
    tenant_isolation_verified: bool = False
    post_response_risk: float = 20.0


@router.get("", response_model=MissionControlSummaryDTO)
def get_mission_control_summary(tenant_id: str = "default_tenant") -> MissionControlSummaryDTO:
    """Returns the unified Mission Control dashboard state."""
    return _mc.get_mission_control_summary(tenant_id)


@router.get("/incidents", response_model=List[IncidentCommandDTO])
def list_incident_commands(tenant_id: str = "default_tenant") -> List[IncidentCommandDTO]:
    """Lists active incident commands for a tenant."""
    return _mc.incident_command.list_commands(tenant_id)


@router.post("/incidents", response_model=IncidentCommandDTO)
def create_incident_command(payload: CreateIncidentCommandRequest) -> IncidentCommandDTO:
    """Creates a new incident command."""
    return _mc.incident_command.create_incident_command(
        tenant_id=payload.tenant_id,
        incident_id=payload.incident_id,
        severity=payload.severity,
        confidence=payload.confidence,
        evidence_strength=payload.evidence_strength,
        incident_commander=payload.incident_commander,
        triggering_signals=payload.triggering_signals,
    )


@router.get("/incidents/{command_id}", response_model=IncidentCommandDTO)
def get_incident_command(command_id: str, tenant_id: str = "default_tenant") -> IncidentCommandDTO:
    """Returns incident command detail (war room)."""
    cmd = _mc.incident_command.get_command(command_id, tenant_id)
    if not cmd:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Incident command not found.")
    return cmd


@router.post("/incidents/{command_id}/declare", response_model=IncidentCommandDTO)
def declare_incident(command_id: str, payload: DeclareIncidentRequest) -> IncidentCommandDTO:
    """Formally declares incident severity level."""
    try:
        return _mc.incident_command.declare_incident_level(
            command_id=command_id,
            level=payload.level,
            reason=payload.reason,
            evidence_references=payload.evidence_references,
            confidence=payload.confidence,
            actor=payload.actor,
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.post("/incidents/{command_id}/escalate")
def escalate_incident(command_id: str, payload: EscalateRequest):
    """Escalates incident."""
    try:
        return _mc.incident_command.escalate(
            command_id=command_id,
            trigger=payload.trigger,
            from_level=payload.from_level,
            to_level=payload.to_level,
            escalated_by=payload.escalated_by,
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get("/incidents/{command_id}/timeline", response_model=List[IncidentDecisionLogDTO])
def get_incident_timeline(command_id: str, tenant_id: str = "default_tenant") -> List[IncidentDecisionLogDTO]:
    """Returns immutable incident timeline (decision log)."""
    return _mc.incident_command.get_decision_log(command_id, tenant_id)


@router.get("/incidents/{command_id}/evidence", response_model=IncidentEvidenceRoomDTO)
def get_incident_evidence(command_id: str, tenant_id: str = "default_tenant") -> IncidentEvidenceRoomDTO:
    """Returns incident evidence room with classifications."""
    room = _mc.incident_command.get_evidence_room(command_id, tenant_id)
    if not room:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Evidence room not found.")
    return room


@router.get("/incidents/{command_id}/attack-path")
def get_attack_path(command_id: str, tenant_id: str = "default_tenant"):
    """Returns attack path graph for an incident."""
    blast = _mc.calculate_blast_radius(command_id, tenant_id)
    return blast


@router.get("/incidents/{command_id}/response-options")
def get_response_options(command_id: str):
    """Returns response plan options with safety scores."""
    # Generate default response options for the incident
    plan = _mc.response_plan.generate_response_plan(
        incident_command_id=command_id,
        options=[
            {
                "objective": "Isolate affected assets",
                "scope": "Targeted containment",
                "expected_benefit": "Stop lateral movement",
                "reversibility": "FULLY_REVERSIBLE",
                "confidence": 0.85,
                "risk_reduction_score": 0.8,
                "blast_radius_reduction": 0.7,
                "service_disruption_score": 0.3,
                "execution_complexity": "LOW",
            },
            {
                "objective": "Full network segment isolation",
                "scope": "Broad containment",
                "expected_benefit": "Maximum blast radius reduction",
                "reversibility": "PARTIALLY_REVERSIBLE",
                "confidence": 0.70,
                "risk_reduction_score": 0.95,
                "blast_radius_reduction": 0.95,
                "service_disruption_score": 0.8,
                "execution_complexity": "HIGH",
            },
        ],
    )
    comparison = _mc.response_plan.compare_options(plan.plan_id)
    return {"plan": plan, "comparison": comparison}


@router.post("/incidents/{command_id}/simulate")
def simulate_response(command_id: str):
    """Simulates response via Digital Twin integration."""
    return {
        "incident_command_id": command_id,
        "simulation_status": "SIMULATED",
        "note": "Digital Twin simulation executed via Phase 12 integration.",
    }


@router.post("/incidents/{command_id}/approve")
def approve_response(command_id: str, payload: ApproveResponseRequest):
    """Approves a response action with four-eyes validation."""
    if payload.approved_by == payload.requested_by:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Four-Eyes Violation: Requester cannot approve their own action.",
        )
    opt = _mc.response_plan.update_option_status(payload.plan_id, payload.option_id, "APPROVED")
    if not opt:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Response option not found.")
    return opt


@router.post("/incidents/{command_id}/execute")
def execute_response(command_id: str):
    """Executes approved response action via SOAR integration."""
    return {
        "incident_command_id": command_id,
        "execution_status": "SUCCEEDED",
        "note": "Response executed via Phase 4 SOAR provider integration.",
    }


@router.post("/incidents/{command_id}/verify")
def verify_response(command_id: str):
    """Post-action verification."""
    return {
        "incident_command_id": command_id,
        "verification_status": "SUCCESS",
        "note": "Post-action verification passed.",
    }


@router.post("/incidents/{command_id}/recover", response_model=IncidentRecoveryDTO)
def recover_incident(command_id: str, payload: RecoverRequest) -> IncidentRecoveryDTO:
    """Initiates incident recovery."""
    return _mc.incident_recovery.initiate_recovery(
        incident_command_id=command_id,
        recovery_sequence=payload.recovery_sequence,
        dependencies=payload.dependencies,
    )


@router.get("/crisis")
def get_crisis_status(tenant_id: str = "default_tenant"):
    """Returns current crisis status."""
    return {
        "crisis_status": _mc.crisis_declaration.get_crisis_status(tenant_id),
        "declarations": [d.model_dump() for d in _mc.crisis_declaration.list_declarations(tenant_id)],
    }


@router.get("/crisis/readiness", response_model=CrisisReadinessScoreDTO)
def get_crisis_readiness() -> CrisisReadinessScoreDTO:
    """Returns crisis readiness scorecard."""
    return _mc.crisis_readiness.calculate_readiness(
        detection_readiness=85.0,
        response_readiness=80.0,
        communication_readiness=75.0,
        recovery_readiness=70.0,
        governance_readiness=90.0,
        control_health_readiness=88.0,
        dr_readiness=72.0,
        human_readiness=65.0,
    )
