"""
TruthShield X — Phase 17 Adaptive Cyber Defense & Closed-Loop Mesh Endpoints.
"""

from typing import Any, Dict, List, Optional
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

from app.schemas.adaptive_defense_models import (
    DefensePostureDTO,
    AttackSurfaceScoreDTO,
    AdaptiveControlRecommendationDTO,
    DefenseSimulationResultDTO,
    DefenseDecisionRecordDTO,
    DefenseChangeRecordDTO,
    AutomationControlStateDTO,
    DefenseEffectivenessScoreDTO,
    AdaptiveDefenseCenterSummaryDTO,
    AdaptiveDefenseGraphDTO,
)
from app.services.adaptive_defense.adaptive_defense_fabric import AdaptiveDefenseFabric

router = APIRouter(prefix="/defense", tags=["Adaptive Cyber Defense & Closed-Loop Mesh"])

_fabric = AdaptiveDefenseFabric()


class CreateRecommendationRequest(BaseModel):
    tenant_id: str = "default_tenant"
    title: str
    action_classification: str = "MONITORING_CHANGE"
    target_resource: str
    automation_level: str = "LEVEL_2_HUMAN_APPROVAL"
    evidence_references: List[str] = []
    duration_minutes: int = 60


class ExecuteActionRequest(BaseModel):
    has_human_approval: bool = False
    operator_id: str = "SOC_AUTOMATION"


class KillSwitchRequest(BaseModel):
    operator_id: str = "SOC_LEAD"


@router.get("", response_model=AdaptiveDefenseCenterSummaryDTO)
@router.get("/summary", response_model=AdaptiveDefenseCenterSummaryDTO)
def get_defense_summary(tenant_id: str = "default_tenant") -> AdaptiveDefenseCenterSummaryDTO:
    """Returns real-time aggregated executive defense posture summary."""
    return _fabric.get_summary(tenant_id)


@router.get("/posture", response_model=DefensePostureDTO)
def get_defense_posture(tenant_id: str = "default_tenant") -> DefensePostureDTO:
    """Returns current evidence-driven defense posture."""
    return _fabric.posture.get_or_create_posture(tenant_id)


@router.get("/exposure", response_model=AttackSurfaceScoreDTO)
def get_attack_surface(tenant_id: str = "default_tenant") -> AttackSurfaceScoreDTO:
    """Returns multidimensional attack surface scorecard."""
    return _fabric.exposure.calculate_attack_surface(tenant_id)


@router.get("/recommendations", response_model=List[AdaptiveControlRecommendationDTO])
def list_recommendations() -> List[AdaptiveControlRecommendationDTO]:
    """Lists active adaptive control recommendations."""
    return list(_fabric._recommendations.values())


@router.post("/recommendations", response_model=AdaptiveControlRecommendationDTO)
def create_recommendation(payload: CreateRecommendationRequest) -> AdaptiveControlRecommendationDTO:
    """Creates a new evidence-referenced defense recommendation."""
    return _fabric.create_recommendation(
        tenant_id=payload.tenant_id,
        title=payload.title,
        action_classification=payload.action_classification,
        target_resource=payload.target_resource,
        automation_level=payload.automation_level,
        evidence_references=payload.evidence_references,
        duration_minutes=payload.duration_minutes,
    )


@router.post("/actions/{recommendation_id}/simulate", response_model=DefenseSimulationResultDTO)
def simulate_defense_action(recommendation_id: str) -> DefenseSimulationResultDTO:
    """Simulates a defense action in the Digital Security Twin."""
    rec = _fabric._recommendations.get(recommendation_id)
    if not rec:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Recommendation not found.")
    return _fabric.simulation.simulate_adaptation(rec)


@router.post("/actions/{recommendation_id}/execute")
def execute_closed_loop_action(recommendation_id: str, payload: ExecuteActionRequest) -> Dict[str, Any]:
    """Executes full closed-loop defense lifecycle for a recommendation."""
    try:
        return _fabric.execute_closed_loop_defense(
            recommendation_id=recommendation_id,
            has_human_approval=payload.has_human_approval,
            operator_id=payload.operator_id,
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/automation", response_model=AutomationControlStateDTO)
def get_automation_status(tenant_id: str = "default_tenant") -> AutomationControlStateDTO:
    """Returns automation control state, pause flags, and circuit breaker status."""
    return _fabric.circuit_breaker.get_or_create_control_state(tenant_id)


@router.post("/automation/pause", response_model=AutomationControlStateDTO)
def pause_automation(tenant_id: str = "default_tenant", operator_id: str = "SOC_LEAD") -> AutomationControlStateDTO:
    """Pauses automated adaptations for a tenant."""
    ctrl = _fabric.circuit_breaker.get_or_create_control_state(tenant_id)
    ctrl.automation_enabled = False
    ctrl.last_modified_by = operator_id
    return ctrl


@router.post("/automation/resume", response_model=AutomationControlStateDTO)
def resume_automation(tenant_id: str = "default_tenant", operator_id: str = "SOC_LEAD") -> AutomationControlStateDTO:
    """Resumes automated adaptations for a tenant."""
    ctrl = _fabric.circuit_breaker.get_or_create_control_state(tenant_id)
    ctrl.automation_enabled = True
    ctrl.last_modified_by = operator_id
    return ctrl


@router.post("/automation/kill-switch", response_model=AutomationControlStateDTO)
def trigger_emergency_kill_switch(tenant_id: str = "default_tenant", payload: Optional[KillSwitchRequest] = None) -> AutomationControlStateDTO:
    """Immediately trips global emergency kill switch halting all automated changes."""
    op = payload.operator_id if payload else "SOC_LEAD"
    _fabric.circuit_breaker.activate_kill_switch(tenant_id, op)
    return _fabric.circuit_breaker.get_or_create_control_state(tenant_id)


@router.get("/effectiveness", response_model=List[DefenseEffectivenessScoreDTO])
def list_effectiveness_scores(tenant_id: str = "default_tenant") -> List[DefenseEffectivenessScoreDTO]:
    """Returns post-action defense effectiveness metrics."""
    return _fabric.effectiveness.list_scores(tenant_id)


@router.get("/graph", response_model=AdaptiveDefenseGraphDTO)
def get_adaptive_defense_graph() -> AdaptiveDefenseGraphDTO:
    """Returns adaptive defense knowledge graph topology."""
    return _fabric.get_defense_graph()
