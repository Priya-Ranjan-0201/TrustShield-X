"""
TruthShield X — Continuous Assurance REST API Endpoints
========================================================
Exposes endpoints for:
- Change Registration & Impact Analysis
- Automated Regression Selection
- AI Golden Dataset Model Evaluation & Promotion
- AI Model Rollback & RAG Poisoning Defense
- Full Continuous Assurance Cycle Execution
- Release Gate Decisions & Risk Scorecard
"""

from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Any, List, Optional
from pydantic import BaseModel

from app.services.continuous_assurance import (
    continuous_assurance_engine,
    ai_regression_engine,
)

router = APIRouter(prefix="/continuous-assurance", tags=["Continuous Assurance & Release Safety"])


class RegisterChangeRequest(BaseModel):
    change_type: str
    author: str
    affected_components: List[str]
    description: Optional[str] = ""
    raw_payload: Optional[Dict[str, Any]] = None


class EvaluateModelRequest(BaseModel):
    model_id: str
    prompt_version: Optional[str] = "v4.0"


class PromoteModelRequest(BaseModel):
    model_id: str
    approver: Optional[str] = "SecOps_CISO"


class AIRollbackRequest(BaseModel):
    reason: str


class KnowledgePoisonCheckRequest(BaseModel):
    retrieved_context: str


@router.post("/changes/register")
async def register_change(request: RegisterChangeRequest) -> Dict[str, Any]:
    """Registers and risk-classifies a change across 17 vectors, generating an impact graph."""
    return continuous_assurance_engine.detect_and_register_change(
        change_type=request.change_type,
        author=request.author,
        affected_components=request.affected_components,
        description=request.description or "",
        raw_payload=request.raw_payload
    )


@router.get("/changes/history")
async def get_change_history() -> Dict[str, Any]:
    """Retrieves full changelog with risk classifications and regression selection mappings."""
    history = continuous_assurance_engine.get_change_history()
    return {"changes_count": len(history), "changes": history}


@router.post("/cycle/run")
async def run_assurance_cycle(change_type: str = "CONFIG_UPDATE") -> Dict[str, Any]:
    """Executes a full continuous assurance verification cycle."""
    return continuous_assurance_engine.run_full_assurance_cycle(candidate_change_type=change_type)


@router.get("/decisions/history")
async def get_release_decisions() -> Dict[str, Any]:
    """Retrieves all release gate decisions and 6D release risk scores."""
    decisions = continuous_assurance_engine.get_release_decisions()
    return {"decisions_count": len(decisions), "decisions": decisions}


@router.post("/ai/evaluate")
async def evaluate_ai_model(request: EvaluateModelRequest) -> Dict[str, Any]:
    """Evaluates candidate AI model against the versioned AI Golden Dataset."""
    return ai_regression_engine.evaluate_model(
        candidate_model_id=request.model_id,
        prompt_version=request.prompt_version or "v4.0"
    )


@router.post("/ai/promote")
async def promote_ai_model(request: PromoteModelRequest) -> Dict[str, Any]:
    """Promotes security-validated AI model to production with human governance."""
    result = ai_regression_engine.promote_model_to_production(
        model_id=request.model_id,
        approver=request.approver or "SecOps_CISO"
    )
    if not result.get("success", False):
        raise HTTPException(status_code=400, detail=result.get("error", "Model promotion blocked"))
    return result


@router.post("/ai/rollback")
async def rollback_ai_model(request: AIRollbackRequest) -> Dict[str, Any]:
    """Executes automated AI rollback to the last verified baseline."""
    return ai_regression_engine.trigger_ai_rollback(reason=request.reason)


@router.post("/ai/detect-poisoning")
async def detect_rag_knowledge_poisoning(request: KnowledgePoisonCheckRequest) -> Dict[str, Any]:
    """Scans retrieved context for indirect prompt injection or instruction hijacking."""
    return ai_regression_engine.detect_knowledge_poisoning(retrieved_context=request.retrieved_context)
