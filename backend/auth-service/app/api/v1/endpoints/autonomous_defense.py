"""
TruthShield X — Autonomous SOC & Self-Optimizing Cyber Defense REST API (Phase 30).
"""

from typing import List, Dict, Any, Optional
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel

from app.schemas.autonomous_defense_models import (
    SecurityDecisionRecordDTO,
    DefensiveLessonDTO,
    AlertOptimizationDTO,
    DetectionOptimizationDTO,
    ThreatHuntingOptimizationDTO,
    ResponseOptimizationDTO,
    ControlOptimizationDTO,
    AdaptivePolicyDTO,
    SecurityExperimentDTO,
    ModelGovernanceDTO,
    AutonomousDefenseScorecardDTO,
    RollbackRecordDTO,
)
from app.services.autonomous_defense.autonomous_soc_engine import AutonomousSOCEngine

router = APIRouter(prefix="/autonomy", tags=["Autonomous SOC & Self-Optimizing Cyber Defense"])

# Singleton Engine Instance
autonomous_soc_engine = AutonomousSOCEngine()


# ============================================================================
# Status & Scorecard
# ============================================================================

@router.get("/status", response_model=AutonomousDefenseScorecardDTO)
def get_autonomous_defense_status(tenant_id: str = Query("default_tenant")):
    return autonomous_soc_engine.get_autonomous_defense_scorecard(tenant_id)


# ============================================================================
# Decisions & Recommendations
# ============================================================================

@router.get("/decisions", response_model=List[SecurityDecisionRecordDTO])
def list_security_decisions(tenant_id: str = Query("default_tenant")):
    return autonomous_soc_engine.decision_engine.list_decisions(tenant_id)


@router.get("/recommendations", response_model=List[SecurityDecisionRecordDTO])
def list_recommendations(tenant_id: str = Query("default_tenant")):
    return [d for d in autonomous_soc_engine.decision_engine.list_decisions(tenant_id) if d.decision_type == "RESPONSE_RECOMMENDATION"]


@router.post("/recommendations/{decision_id}/approve", response_model=Dict[str, Any])
def approve_recommendation(decision_id: str, approver: str = Query("usr_ciso_alpha")):
    dec = autonomous_soc_engine.decision_engine.get_decision(decision_id)
    if not dec:
        raise HTTPException(status_code=404, detail="Recommendation not found")
    return {"decision_id": decision_id, "status": "APPROVED", "approver": approver}


@router.post("/recommendations/{decision_id}/reject", response_model=Dict[str, Any])
def reject_recommendation(decision_id: str, reason: str = Query("Does not meet policy")):
    dec = autonomous_soc_engine.decision_engine.get_decision(decision_id)
    if not dec:
        raise HTTPException(status_code=404, detail="Recommendation not found")
    return {"decision_id": decision_id, "status": "REJECTED", "reason": reason}


# ============================================================================
# Experiments
# ============================================================================

@router.get("/experiments", response_model=List[SecurityExperimentDTO])
def list_security_experiments():
    return autonomous_soc_engine.experiment_engine.list_experiments()


class CreateExperimentRequest(BaseModel):
    hypothesis: str
    baseline_strategy: str
    candidate_strategy: str
    rollback_procedure: str


@router.post("/experiments", response_model=SecurityExperimentDTO)
def create_security_experiment(payload: CreateExperimentRequest):
    return autonomous_soc_engine.experiment_engine.run_experiment(
        hypothesis=payload.hypothesis,
        baseline_strategy=payload.baseline_strategy,
        candidate_strategy=payload.candidate_strategy,
        rollback_procedure=payload.rollback_procedure,
    )


# ============================================================================
# Models & Governance
# ============================================================================

@router.get("/models", response_model=List[ModelGovernanceDTO])
def list_ai_models():
    return autonomous_soc_engine.model_engine.list_models()


@router.get("/models/{model_id}", response_model=Dict[str, Any])
def get_model_details(model_id: str):
    models = {m.model_id: m for m in autonomous_soc_engine.model_engine.list_models()}
    if model_id not in models:
        raise HTTPException(status_code=404, detail="Model not found")
    return {"model": models[model_id]}


# ============================================================================
# Learning & Optimization Metrics
# ============================================================================

@router.get("/learning", response_model=List[DefensiveLessonDTO])
def list_defensive_learning(tenant_id: str = Query("default_tenant")):
    return autonomous_soc_engine.memory_engine.get_applicable_lessons(tenant_id)


@router.get("/detection-quality", response_model=List[DetectionOptimizationDTO])
def get_detection_quality():
    return autonomous_soc_engine.detection_engine.list_rules()


@router.get("/response-effectiveness", response_model=Optional[ResponseOptimizationDTO])
def get_response_effectiveness(response_id: str = Query("rsp_darkstorm_waf")):
    return autonomous_soc_engine.response_engine.get_response_metrics(response_id)


@router.get("/control-effectiveness", response_model=List[ControlOptimizationDTO])
def list_control_effectiveness():
    return autonomous_soc_engine.control_engine.list_controls()


@router.get("/drift", response_model=Dict[str, Any])
def get_drift_status():
    return {
        "rule_drift": "STABLE",
        "model_drift": "STABLE",
        "environment_drift": "STABLE",
    }


@router.get("/rollbacks", response_model=List[RollbackRecordDTO])
def list_rollback_records():
    return autonomous_soc_engine.rollback_engine.list_rollbacks()
