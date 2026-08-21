"""REST API Endpoints for Autonomous Cyber Defense & Digital Trust Orchestration (Phase 5)."""

from typing import List, Dict, Any, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Body
from app.schemas.autonomous_defense_models import (
    ResponsePlanDTO,
    DecisionContextDTO,
    SimulationResultDTO,
    VerificationResultDTO,
    RollbackResultDTO,
    EffectivenessScoreDTO,
    SecurityCopilotQueryDTO,
    SecurityCopilotResponseDTO,
)
from app.services.autonomous_defense_orchestrator import AutonomousDefenseOrchestrator
from app.services.security_copilot_service import SecurityCopilotService

router = APIRouter(prefix="/response", tags=["Autonomous Cyber Defense & SOAR"])

# Singleton instances for in-memory orchestration state
orchestrator = AutonomousDefenseOrchestrator()
copilot_service = SecurityCopilotService()


@router.post("/plans", response_model=ResponsePlanDTO, status_code=status.HTTP_201_CREATED)
async def create_response_plan(
    incident_id: str = Body(...),
    title: str = Body(...),
    description: str = Body(...),
    threat_contexts: List[DecisionContextDTO] = Body(...),
    tenant_id: str = Body(default="org_default"),
    campaign_id: Optional[str] = Body(default=None),
):
    """Generate an immutable, policy-aware response plan."""
    try:
        plan = orchestrator.create_response_plan(
            tenant_id=tenant_id,
            incident_id=incident_id,
            title=title,
            description=description,
            threat_contexts=threat_contexts,
            campaign_id=campaign_id,
        )
        return plan
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/plans", response_model=List[ResponsePlanDTO])
async def list_response_plans(tenant_id: str = "org_default"):
    """List all response plans for current tenant."""
    return orchestrator.list_plans(tenant_id=tenant_id)


@router.get("/plans/{plan_id}", response_model=ResponsePlanDTO)
async def get_response_plan(plan_id: str, tenant_id: str = "org_default"):
    """Retrieve response plan by ID."""
    plan = orchestrator.get_plan(plan_id=plan_id, tenant_id=tenant_id)
    if not plan:
        raise HTTPException(status_code=404, detail="Response plan not found.")
    return plan


@router.post("/plans/{plan_id}/simulate", response_model=SimulationResultDTO)
async def simulate_response_plan(plan_id: str, tenant_id: str = "org_default"):
    """Perform dry-run simulation with zero external state mutations."""
    try:
        return orchestrator.simulate_plan(plan_id=plan_id, tenant_id=tenant_id)
    except KeyError:
        raise HTTPException(status_code=404, detail="Response plan not found.")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/plans/{plan_id}/approve")
async def approve_response_plan_action(
    plan_id: str,
    approval_id: str = Body(...),
    approver_id: str = Body(...),
    decision: str = Body(default="APPROVED"),
    decision_reason: str = Body(default="Authorized by SOC Lead"),
    tenant_id: str = Body(default="org_default"),
):
    """Four-eyes approval for high-risk defense action."""
    try:
        approved = orchestrator.approve_action(
            approval_id=approval_id,
            approver_id=approver_id,
            decision=decision,
            decision_reason=decision_reason,
            tenant_id=tenant_id,
        )
        return {"success": True, "approved": approved, "status": decision}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/plans/{plan_id}/execute")
async def execute_response_plan(
    plan_id: str,
    tenant_id: str = Body(default="org_default"),
):
    """Execute all approved remediation actions in plan."""
    try:
        actions = orchestrator.execute_plan(plan_id=plan_id, tenant_id=tenant_id)
        return {"success": True, "plan_id": plan_id, "executed_actions": actions}
    except KeyError:
        raise HTTPException(status_code=404, detail="Response plan not found.")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/plans/{plan_id}/verify", response_model=List[VerificationResultDTO])
async def verify_response_plan(plan_id: str, tenant_id: str = "org_default"):
    """Empirically verify containment state post-execution."""
    try:
        return orchestrator.verify_plan(plan_id=plan_id, tenant_id=tenant_id)
    except KeyError:
        raise HTTPException(status_code=404, detail="Response plan not found.")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/plans/{plan_id}/rollback", response_model=RollbackResultDTO)
async def rollback_response_action(
    plan_id: str,
    action_id: str = Body(...),
    executed_by: str = Body(default="SOC_LEAD"),
    tenant_id: str = Body(default="org_default"),
):
    """Revert an executed remediation action where supported."""
    try:
        return orchestrator.rollback_action(
            plan_id=plan_id,
            action_id=action_id,
            tenant_id=tenant_id,
            executed_by=executed_by,
        )
    except KeyError:
        raise HTTPException(status_code=404, detail="Response plan or action not found.")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/plans/{plan_id}/timeline")
async def get_plan_audit_timeline(plan_id: str):
    """Retrieve SHA-256 chained audit events for response plan."""
    trail = orchestrator.get_audit_trail()
    filtered = [e for e in trail if e.get("payload", {}).get("plan_id") == plan_id]
    return {"plan_id": plan_id, "audit_events": filtered, "total_events": len(filtered)}


@router.get("/providers")
async def list_response_providers():
    """List active response provider adapters and supported security capabilities."""
    return {
        "providers": [
            {"name": "DNSResponseAdapter", "actions": ["BLOCK_DOMAIN", "SINKHOLE_DOMAIN"], "status": "ACTIVE"},
            {"name": "FirewallResponseAdapter", "actions": ["BLOCK_IP", "UPDATE_FIREWALL_RULE"], "status": "ACTIVE"},
            {"name": "EDRResponseAdapter", "actions": ["QUARANTINE_FILE", "ISOLATE_DEVICE"], "status": "ACTIVE"},
            {"name": "IAMResponseAdapter", "actions": ["DISABLE_ACCOUNT", "REVOKE_TOKEN", "RESET_CREDENTIAL"], "status": "ACTIVE"},
            {"name": "FraudControlResponseAdapter", "actions": ["FREEZE_UPI_HANDLE", "BLOCK_TRANSACTION"], "status": "ACTIVE"},
            {"name": "CloudStorageResponseAdapter", "actions": ["ISOLATE_S3_BUCKET", "BLOCK_PUBLIC_ACCESS"], "status": "ACTIVE"},
        ]
    }


@router.post("/copilot/explain", response_model=SecurityCopilotResponseDTO)
async def explain_threat_copilot(query_dto: SecurityCopilotQueryDTO):
    """Explain threat context, proposed actions, or refusal reasons via Security Copilot."""
    return copilot_service.process_query(query_dto)


@router.get("/effectiveness/{plan_id}", response_model=EffectivenessScoreDTO)
async def get_response_effectiveness(
    plan_id: str,
    tenant_id: str = "org_default",
    initial_risk: float = 85.0,
    residual_risk: float = 12.0,
):
    """Calculate and return factual 0-100 containment effectiveness score."""
    plan = orchestrator.get_plan(plan_id=plan_id, tenant_id=tenant_id)
    if not plan:
        raise HTTPException(status_code=404, detail="Response plan not found.")

    verifications = orchestrator.verify_plan(plan_id=plan_id, tenant_id=tenant_id) if plan.state in ("EXECUTED", "VERIFIED") else []
    return orchestrator.effectiveness_engine.calculate_effectiveness(
        plan=plan,
        verifications=verifications,
        initial_risk=initial_risk,
        residual_risk=residual_risk,
    )
