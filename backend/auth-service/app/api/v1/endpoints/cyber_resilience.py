"""
TruthShield X — Cyber Resilience & Autonomous Recovery REST API (Phase 23).
"""

from typing import List, Dict, Any, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel

from app.schemas.cyber_resilience_models import (
    ResilienceAssetDTO,
    BusinessServiceDTO,
    ServiceDependencyGraphDTO,
    ResilienceGapDTO,
    BackupValidationDTO,
    RecoveryPlanDTO,
    RecoveryActionExecutionDTO,
    RecoveryVerificationDTO,
    DisasterRecoveryDrillDTO,
    RecoveryDriftDTO,
    ResilienceScorecardDTO,
)
from app.services.resilience.cyber_resilience_engine import CyberResilienceEngine

router = APIRouter(prefix="/resilience", tags=["Cyber Resilience & Autonomous Recovery"])

# Singleton engine instance
resilience_engine = CyberResilienceEngine()


# ============================================================================
# Overview & Scorecard
# ============================================================================

@router.get("/overview", response_model=Dict[str, Any])
def get_resilience_overview(tenant_id: str = Query("default_tenant")):
    return resilience_engine.get_complete_resilience_overview(tenant_id)


@router.get("/scorecard", response_model=ResilienceScorecardDTO)
def get_resilience_scorecard(tenant_id: str = Query("default_tenant")):
    return resilience_engine.score_engine.evaluate_scorecard(tenant_id)


# ============================================================================
# Assets & Business Services
# ============================================================================

@router.get("/assets", response_model=List[ResilienceAssetDTO])
def list_resilience_assets(tenant_id: str = Query("default_tenant")):
    return resilience_engine.asset_manager.list_assets(tenant_id)


@router.get("/services", response_model=List[BusinessServiceDTO])
def list_business_services(tenant_id: str = Query("default_tenant")):
    return resilience_engine.asset_manager.list_business_services(tenant_id)


@router.get("/services/{service_id}", response_model=BusinessServiceDTO)
def get_business_service(service_id: str):
    svc = resilience_engine.asset_manager.get_business_service(service_id)
    if not svc:
        raise HTTPException(status_code=404, detail="Business service not found")
    return svc


@router.get("/dependencies", response_model=ServiceDependencyGraphDTO)
def get_resilience_dependency_graph(tenant_id: str = Query("default_tenant")):
    return resilience_engine.dependency_graph_engine.build_graph(tenant_id)


# ============================================================================
# Gaps & Backups
# ============================================================================

@router.get("/gaps", response_model=List[ResilienceGapDTO])
def list_resilience_gaps(tenant_id: str = Query("default_tenant")):
    return resilience_engine.gap_engine.list_gaps(tenant_id)


@router.get("/backups", response_model=List[BackupValidationDTO])
def list_backups(tenant_id: str = Query("default_tenant")):
    return list(resilience_engine.backup_engine._backups.values())


class ValidateBackupRequest(BaseModel):
    asset_id: str
    checksum_valid: bool = True
    schema_valid: bool = True
    is_poisoned: bool = False


@router.post("/backups/{backup_id}/validate", response_model=BackupValidationDTO)
def validate_backup(backup_id: str, payload: ValidateBackupRequest):
    return resilience_engine.backup_engine.validate_backup(
        backup_id=backup_id,
        asset_id=payload.asset_id,
        checksum_valid=payload.checksum_valid,
        schema_valid=payload.schema_valid,
        is_poisoned=payload.is_poisoned,
    )


# ============================================================================
# Recovery Plans & Execution
# ============================================================================

@router.get("/recovery-plans", response_model=List[RecoveryPlanDTO])
def list_recovery_plans(tenant_id: str = Query("default_tenant")):
    return resilience_engine.plan_engine.list_plans(tenant_id)


@router.get("/recovery-plans/{plan_id}", response_model=RecoveryPlanDTO)
def get_recovery_plan(plan_id: str):
    plan = resilience_engine.plan_engine.get_plan(plan_id)
    if not plan:
        raise HTTPException(status_code=404, detail="Recovery plan not found")
    return plan


class CreateRecoveryPlanRequest(BaseModel):
    service_name: str
    ordered_dependencies: List[str]
    tenant_id: str = "default_tenant"


@router.post("/recovery-plans", response_model=RecoveryPlanDTO)
def create_recovery_plan(payload: CreateRecoveryPlanRequest):
    return resilience_engine.plan_engine.generate_plan(
        service_name=payload.service_name,
        ordered_dependencies=payload.ordered_dependencies,
        tenant_id=payload.tenant_id,
    )


@router.post("/recovery-plans/{plan_id}/approve", response_model=RecoveryPlanDTO)
def approve_recovery_plan(plan_id: str, approver_id: str = Query("usr_ciso")):
    try:
        return resilience_engine.plan_engine.approve_plan(plan_id, approver_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/recovery-plans/{plan_id}/simulate", response_model=Dict[str, Any])
def simulate_recovery_plan(plan_id: str):
    plan = resilience_engine.plan_engine.get_plan(plan_id)
    if not plan:
        raise HTTPException(status_code=404, detail="Recovery plan not found")
    return resilience_engine.twin_engine.simulate_attack_and_disruption(
        initial_failure_target=plan.dependencies[0] if plan.dependencies else "ast_pg_primary"
    )


class ExecuteStepRequest(BaseModel):
    step_id: str
    target: str
    action: str
    requester_id: str
    approver_id: str
    target_environment: str = "ISOLATED_SANDBOX"


@router.post("/recovery-plans/{plan_id}/execute", response_model=RecoveryActionExecutionDTO)
def execute_recovery_step(plan_id: str, payload: ExecuteStepRequest):
    plan = resilience_engine.plan_engine.get_plan(plan_id)
    if not plan:
        raise HTTPException(status_code=404, detail="Recovery plan not found")
    try:
        return resilience_engine.execution_engine.execute_step(
            plan=plan,
            step_id=payload.step_id,
            target=payload.target,
            action=payload.action,
            requester_id=payload.requester_id,
            approver_id=payload.approver_id,
            target_environment=payload.target_environment,
        )
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))


# ============================================================================
# Drills & Drift
# ============================================================================

@router.get("/drills", response_model=List[DisasterRecoveryDrillDTO])
def list_drills(tenant_id: str = Query("default_tenant")):
    return resilience_engine.drill_engine.list_drills(tenant_id)


class ScheduleDrillRequest(BaseModel):
    drill_type: str
    environment: str = "ISOLATED_SANDBOX"
    scope: str = "SANDBOX_FAILOVER_TEST"
    tenant_id: str = "default_tenant"


@router.post("/drills", response_model=DisasterRecoveryDrillDTO)
def schedule_drill(payload: ScheduleDrillRequest):
    try:
        return resilience_engine.drill_engine.schedule_drill(
            drill_type=payload.drill_type,  # type: ignore
            environment=payload.environment,
            scope=payload.scope,
            tenant_id=payload.tenant_id,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/drills/{drill_id}/abort", response_model=DisasterRecoveryDrillDTO)
def abort_drill(drill_id: str, reason: str = Query("Drill Safety Abort Triggered")):
    try:
        return resilience_engine.drill_engine.abort_drill(drill_id, reason)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/drift", response_model=List[RecoveryDriftDTO])
def list_recovery_drift(tenant_id: str = Query("default_tenant")):
    return resilience_engine.drift_engine.list_drifts(tenant_id)
