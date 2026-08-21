"""
TruthShield X — Autonomous Security Engineering REST API (Phase 25).
"""

from typing import List, Dict, Any, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel

from app.schemas.security_engineering_models import (
    SecurityImprovementDTO,
    SecurityGapDTO,
    RootCauseAnalysisDTO,
    ImpactAnalysisDTO,
    SimulationResultDTO,
    DeploymentRolloutDTO,
    RollbackRecordDTO,
    OutcomeMeasurementDTO,
    SecurityExperimentDTO,
    IncidentLearningRecordDTO,
    AutonomyGovernanceConfigDTO,
)
from app.services.security_engineering.autonomous_security_engineering_engine import AutonomousSecurityEngineeringEngine

router = APIRouter(prefix="/security-engineering", tags=["Autonomous Security Engineering & Adaptive Defense"])

# Singleton engine instance
security_engineering_engine = AutonomousSecurityEngineeringEngine()


# ============================================================================
# Overview & Health
# ============================================================================

@router.get("/overview", response_model=Dict[str, Any])
def get_engineering_overview(tenant_id: str = Query("default_tenant")):
    return security_engineering_engine.get_engineering_overview(tenant_id)


# ============================================================================
# Gaps & Root Cause
# ============================================================================

@router.get("/gaps", response_model=List[SecurityGapDTO])
def list_security_gaps(tenant_id: str = Query("default_tenant")):
    return security_engineering_engine.gap_engine.list_gaps(tenant_id)


@router.get("/gaps/{gap_id}", response_model=SecurityGapDTO)
def get_security_gap(gap_id: str):
    gap = security_engineering_engine.gap_engine.get_gap(gap_id)
    if not gap:
        raise HTTPException(status_code=404, detail="Security gap not found")
    return gap


# ============================================================================
# Improvements Lifecycle
# ============================================================================

@router.get("/improvements", response_model=List[SecurityImprovementDTO])
def list_security_improvements(tenant_id: str = Query("default_tenant")):
    return security_engineering_engine.improvement_engine.list_improvements(tenant_id)


@router.get("/improvements/{improvement_id}", response_model=SecurityImprovementDTO)
def get_security_improvement(improvement_id: str):
    imp = security_engineering_engine.improvement_engine.get_improvement(improvement_id)
    if not imp:
        raise HTTPException(status_code=404, detail="Security improvement not found")
    return imp


class GenerateImprovementRequest(BaseModel):
    category: str = "DETECTION"
    title: str
    description: str
    problem: str
    proposed_change: str
    expected_benefit: str
    expected_risk: str
    evidence: Optional[List[str]] = None
    confidence: float = 0.95
    impact_score: float = 0.85
    reversibility: str = "FULLY_REVERSIBLE"
    tenant_id: str = "default_tenant"


@router.post("/improvements", response_model=SecurityImprovementDTO)
def create_improvement(payload: GenerateImprovementRequest):
    try:
        return security_engineering_engine.improvement_engine.generate_improvement(
            category=payload.category,  # type: ignore
            title=payload.title,
            description=payload.description,
            problem=payload.problem,
            proposed_change=payload.proposed_change,
            expected_benefit=payload.expected_benefit,
            expected_risk=payload.expected_risk,
            evidence=payload.evidence,
            confidence=payload.confidence,
            impact_score=payload.impact_score,
            reversibility=payload.reversibility,
            tenant_id=payload.tenant_id,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/improvements/{improvement_id}/impact", response_model=ImpactAnalysisDTO)
def analyze_impact(improvement_id: str):
    imp = security_engineering_engine.improvement_engine.get_improvement(improvement_id)
    if not imp:
        raise HTTPException(status_code=404, detail="Security improvement not found")
    return security_engineering_engine.impact_engine.analyze_impact(improvement_id)


@router.post("/improvements/{improvement_id}/simulate", response_model=SimulationResultDTO)
def simulate_improvement(improvement_id: str):
    imp = security_engineering_engine.improvement_engine.get_improvement(improvement_id)
    if not imp:
        raise HTTPException(status_code=404, detail="Security improvement not found")
    return security_engineering_engine.simulation_engine.simulate_improvement(improvement_id)


@router.post("/improvements/{improvement_id}/validate", response_model=Dict[str, Any])
def validate_change(improvement_id: str):
    imp = security_engineering_engine.improvement_engine.get_improvement(improvement_id)
    if not imp:
        raise HTTPException(status_code=404, detail="Security improvement not found")
    return security_engineering_engine.validation_engine.validate_change(improvement_id)


@router.post("/improvements/{improvement_id}/deploy", response_model=DeploymentRolloutDTO)
def deploy_improvement(improvement_id: str, strategy: str = Query("CANARY")):
    imp = security_engineering_engine.improvement_engine.get_improvement(improvement_id)
    if not imp:
        raise HTTPException(status_code=404, detail="Security improvement not found")
    return security_engineering_engine.rollout_engine.deploy_change(improvement_id, strategy=strategy)  # type: ignore


# ============================================================================
# Experiments & Learnings
# ============================================================================

@router.get("/experiments", response_model=List[SecurityExperimentDTO])
def list_experiments(tenant_id: str = Query("default_tenant")):
    return security_engineering_engine.experiment_engine.list_experiments(tenant_id)


@router.get("/learnings", response_model=List[IncidentLearningRecordDTO])
def list_incident_learnings():
    return security_engineering_engine.incident_learning_engine.list_learnings()


@router.get("/optimization", response_model=Dict[str, Any])
def get_optimization_report():
    return {
        "detection_optimization": security_engineering_engine.detection_opt_engine.evaluate_detection_ruleset(),
        "policy_optimization": security_engineering_engine.policy_opt_engine.analyze_policy_health(),
        "soar_optimization": security_engineering_engine.soar_opt_engine.evaluate_playbook_performance(),
    }
