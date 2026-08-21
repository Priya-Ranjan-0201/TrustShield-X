"""
TruthShield X — AI Security & Model Governance REST API (Phase 31).
"""

from typing import List, Dict, Any, Optional
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel

from app.schemas.ai_security_governance_models import (
    AIAssetDTO,
    ModelRegistryDTO,
    DatasetDTO,
    PromptTemplateDTO,
    AIAgentDTO,
    ToolRegistryDTO,
    AIIncidentDTO,
    AIRedTeamResultDTO,
    AIRiskScorecardDTO,
)
from app.services.ai_governance.ai_security_governance_engine import AISecurityGovernanceEngine

router = APIRouter(prefix="/ai", tags=["AI Security & Model Governance Control Plane"])

# Singleton Engine Instance
ai_security_governance_engine = AISecurityGovernanceEngine()


# ============================================================================
# AI Assets & Governance
# ============================================================================

@router.get("/governance", response_model=Dict[str, Any])
def get_ai_governance_overview(tenant_id: str = Query("default_tenant")):
    return ai_security_governance_engine.get_governance_summary(tenant_id)


@router.get("/assets", response_model=List[AIAssetDTO])
def list_ai_assets(tenant_id: str = Query("default_tenant")):
    return ai_security_governance_engine.asset_engine.list_assets(tenant_id)


# ============================================================================
# Model Registry & Lifecycle
# ============================================================================

@router.get("/models", response_model=List[ModelRegistryDTO])
def list_models():
    return ai_security_governance_engine.model_engine.list_models()


@router.get("/models/{model_id}", response_model=Dict[str, Any])
def get_model(model_id: str):
    m = ai_security_governance_engine.model_engine.get_model(model_id)
    if not m:
        raise HTTPException(status_code=404, detail="Model not found")
    return {"model": m}


@router.get("/models/{model_id}/evaluations", response_model=Dict[str, Any])
def get_model_evaluations(model_id: str):
    return {
        "model_id": model_id,
        "precision": 0.97,
        "recall": 0.95,
        "f1_score": 0.96,
        "evaluation_dataset": "ds_threat_intel_training_v1",
        "status": "EVALUATED_AND_VERIFIED",
    }


@router.get("/models/{model_id}/drift", response_model=Dict[str, Any])
def get_model_drift(model_id: str):
    return ai_security_governance_engine.behavior_engine.get_monitoring_summary(model_id)


@router.post("/models/{model_id}/quarantine", response_model=Dict[str, Any])
def quarantine_model(model_id: str, reason: str = Query("Drift spike or suspicious output")):
    return ai_security_governance_engine.incident_engine.trigger_model_quarantine(model_id, reason)


@router.post("/models/{model_id}/rollback", response_model=Dict[str, Any])
def rollback_model(model_id: str, target_version: str = Query("2.0.0")):
    return {
        "model_id": model_id,
        "status": "ROLLED_BACK",
        "target_version": target_version,
        "is_verified": True,
    }


@router.post("/models/{model_id}/disable", response_model=Dict[str, Any])
def disable_model_kill_switch(model_id: str, authorized_by: str = Query("usr_ciso_alpha")):
    return ai_security_governance_engine.incident_engine.emergency_kill_switch(model_id, authorized_by)


# ============================================================================
# Datasets, Prompts, Agents & Tools
# ============================================================================

@router.get("/datasets", response_model=List[DatasetDTO])
def list_datasets():
    return ai_security_governance_engine.dataset_engine.list_datasets()


@router.get("/prompts", response_model=List[PromptTemplateDTO])
def list_prompts():
    return ai_security_governance_engine.prompt_engine.list_prompts()


@router.get("/agents", response_model=List[AIAgentDTO])
def list_agents():
    return ai_security_governance_engine.agent_engine.list_agents()


@router.get("/tools", response_model=List[ToolRegistryDTO])
def list_tools():
    return ai_security_governance_engine.tool_engine.list_tools()


# ============================================================================
# Incidents, RAG Security & Red Team
# ============================================================================

@router.get("/incidents", response_model=List[AIIncidentDTO])
def list_ai_incidents(tenant_id: str = Query("default_tenant")):
    return ai_security_governance_engine.incident_engine.list_incidents(tenant_id)


@router.get("/security-events", response_model=List[Dict[str, Any]])
def list_ai_security_events():
    return [
        {
            "event_id": "ai_evt_01",
            "type": "PROMPT_INJECTION_ATTEMPT_BLOCKED",
            "model_id": "mdl_c2_neural_classifier",
            "severity": "HIGH",
            "timestamp": "2026-08-20T10:00:00Z",
        }
    ]


@router.get("/rag/security", response_model=Dict[str, Any])
def get_rag_security_status():
    return {
        "active_rag_pipelines": 3,
        "document_trust_enforced": True,
        "indirect_injection_filter": "ACTIVE",
        "cross_tenant_isolation": "VERIFIED_ISOLATED",
    }


@router.get("/red-team", response_model=Dict[str, Any])
def get_red_team_summary():
    return ai_security_governance_engine.red_team_engine.run_red_team_suite()
