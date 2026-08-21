"""
TruthShield X — Continuous Security Assurance REST API (Phase 24).
"""

from typing import List, Dict, Any, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel

from app.schemas.security_assurance_fabric_models import (
    SecurityControlDTO,
    SecurityAssertionDTO,
    ControlValidationResultDTO,
    SecurityDriftDTO,
    SecurityBaselineDTO,
    SecurityRegressionRunDTO,
    AIControlAssuranceDTO,
    RemediationPlanDTO,
    SecurityGameDayDTO,
    SecurityDebtDTO,
    AssuranceScorecardDTO,
)
from app.services.assurance_fabric.security_assurance_fabric import SecurityAssuranceFabric

router = APIRouter(prefix="/assurance-fabric", tags=["Continuous Security Assurance & Validation"])

# Singleton engine instance
assurance_fabric = SecurityAssuranceFabric()


# ============================================================================
# Overview & Scorecard
# ============================================================================

@router.get("/overview", response_model=Dict[str, Any])
def get_assurance_overview(tenant_id: str = Query("default_tenant")):
    return assurance_fabric.get_complete_assurance_overview(tenant_id)


@router.get("/scorecard", response_model=AssuranceScorecardDTO)
def get_assurance_scorecard(tenant_id: str = Query("default_tenant")):
    return assurance_fabric.scorer.evaluate_scorecard(tenant_id)


# ============================================================================
# Controls & Assertions
# ============================================================================

@router.get("/controls", response_model=List[SecurityControlDTO])
def list_security_controls(tenant_id: str = Query("default_tenant")):
    return assurance_fabric.control_manager.list_controls(tenant_id)


@router.get("/controls/{control_id}", response_model=SecurityControlDTO)
def get_security_control(control_id: str):
    ctl = assurance_fabric.control_manager.get_control(control_id)
    if not ctl:
        raise HTTPException(status_code=404, detail="Security control not found")
    return ctl


@router.get("/assertions", response_model=List[SecurityAssertionDTO])
def list_security_assertions():
    return assurance_fabric.assertion_engine.list_assertions()


# ============================================================================
# Validations & Negative Testing
# ============================================================================

@router.get("/validations", response_model=List[ControlValidationResultDTO])
def list_validation_results():
    return assurance_fabric.validation_engine.list_validation_results()


class ExecuteValidationRequest(BaseModel):
    test_name: str
    expected_result: str
    actual_result: str
    has_evidence: bool = True
    environment: str = "ISOLATED_SANDBOX"


@router.post("/controls/{control_id}/validate", response_model=ControlValidationResultDTO)
def validate_control(control_id: str, payload: ExecuteValidationRequest):
    ctl = assurance_fabric.control_manager.get_control(control_id)
    if not ctl:
        raise HTTPException(status_code=404, detail="Security control not found")
    try:
        return assurance_fabric.validation_engine.execute_validation(
            control_id=control_id,
            test_name=payload.test_name,
            expected_result=payload.expected_result,
            actual_result=payload.actual_result,
            has_evidence=payload.has_evidence,
            environment=payload.environment,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# ============================================================================
# Drift & Baselines
# ============================================================================

@router.get("/drift", response_model=List[SecurityDriftDTO])
def list_security_drift(tenant_id: str = Query("default_tenant")):
    return assurance_fabric.drift_engine.list_drifts(tenant_id)


@router.get("/baselines/{baseline_id}", response_model=SecurityBaselineDTO)
def get_baseline(baseline_id: str):
    base = assurance_fabric.baselines_engine.get_baseline(baseline_id)
    if not base:
        raise HTTPException(status_code=404, detail="Security baseline not found")
    return base


# ============================================================================
# Regression & AI Assurance
# ============================================================================

class RunRegressionRequest(BaseModel):
    trigger_event: str
    changed_components: List[str]
    tenant_id: str = "default_tenant"


@router.post("/regression/run", response_model=SecurityRegressionRunDTO)
def run_security_regression(payload: RunRegressionRequest):
    affected = assurance_fabric.dependency_graph.get_affected_controls(payload.changed_components)
    base = assurance_fabric.baselines_engine.get_baseline("sbase_v1_prod_locked")
    baseline_states = base.control_states if base else {}

    # Synthetic test execution against affected controls
    current_results = {c: "PASS" for c in affected}

    return assurance_fabric.regression_engine.run_regression_suite(
        trigger_event=payload.trigger_event,
        changed_components=payload.changed_components,
        affected_controls=affected,
        baseline_states=baseline_states,
        current_test_results=current_results,
        tenant_id=payload.tenant_id,
    )


@router.get("/ai-assurance", response_model=AIControlAssuranceDTO)
def get_ai_security_assurance():
    return assurance_fabric.ai_assurance_engine.evaluate_ai_safety()


# ============================================================================
# Remediation, Game Days & Security Debt
# ============================================================================

@router.get("/remediation/{remediation_id}", response_model=RemediationPlanDTO)
def get_remediation_plan(remediation_id: str):
    plan = assurance_fabric.remediation_engine.get_plan(remediation_id)
    if not plan:
        raise HTTPException(status_code=404, detail="Remediation plan not found")
    return plan


@router.post("/remediation/{remediation_id}/approve", response_model=RemediationPlanDTO)
def approve_remediation(remediation_id: str, approver_id: str = Query("usr_ciso")):
    try:
        return assurance_fabric.remediation_engine.approve_and_execute(remediation_id, approver_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/remediation/{remediation_id}/revalidate", response_model=RemediationPlanDTO)
def revalidate_remediation(remediation_id: str, test_passed: bool = Query(True)):
    try:
        return assurance_fabric.remediation_engine.revalidate_remediation(remediation_id, test_passed)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/gamedays", response_model=List[SecurityGameDayDTO])
def list_game_days(tenant_id: str = Query("default_tenant")):
    return assurance_fabric.gameday_engine.list_gamedays(tenant_id)


@router.get("/security-debt", response_model=SecurityDebtDTO)
def get_security_debt(tenant_id: str = Query("default_tenant")):
    return assurance_fabric.debt_engine.evaluate_debt(tenant_id=tenant_id)
