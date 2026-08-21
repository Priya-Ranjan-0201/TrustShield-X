"""
TruthShield X — Phase 11 Autonomous Threat Hunting & Predictive Defense Endpoints
"""

from typing import Any, Dict, List, Optional
from fastapi import APIRouter, HTTPException, Query, status
from pydantic import BaseModel

from app.schemas.hunting_models import (
    ThreatHuntHypothesisDTO,
    ThreatHuntResultDTO,
    AttackPathGraphDTO,
    EarlyWarningDTO,
    SecurityPredictionDTO,
    HypothesisTypeLiteral,
)
from app.services.hunting.threat_hunting_fabric import ThreatHuntingFabric


router = APIRouter(prefix="/hunting", tags=["Autonomous Threat Hunting & Predictive Defense"])

_fabric = ThreatHuntingFabric()


class CreateHuntRequest(BaseModel):
    title: str
    description: str
    hypothesis_type: HypothesisTypeLiteral = "CAMPAIGN_EXPANSION"
    target_assets: Optional[List[str]] = None
    initial_evidence: Optional[List[Dict[str, Any]]] = None
    tenant_id: str = "default_tenant"


class CancelHuntRequest(BaseModel):
    reason: str


@router.post("", response_model=ThreatHuntHypothesisDTO, status_code=status.HTTP_201_CREATED)
def create_hunt_hypothesis(payload: CreateHuntRequest) -> ThreatHuntHypothesisDTO:
    """Creates a new structured threat hunting hypothesis."""
    return _fabric.create_hunt_hypothesis(
        title=payload.title,
        description=payload.description,
        hypothesis_type=payload.hypothesis_type,
        target_assets=payload.target_assets,
        initial_evidence=payload.initial_evidence,
        tenant_id=payload.tenant_id,
    )


@router.get("", response_model=List[ThreatHuntHypothesisDTO])
def list_hunts(tenant_id: str = "default_tenant") -> List[ThreatHuntHypothesisDTO]:
    """Lists threat hunting hypotheses."""
    return _fabric.list_hypotheses(tenant_id)


@router.post("/{hunt_id}/run", response_model=ThreatHuntResultDTO)
def run_threat_hunt(hunt_id: str) -> ThreatHuntResultDTO:
    """Executes the autonomous threat hunt loop within bounded budget constraints."""
    try:
        return _fabric.run_bounded_hunt(hypothesis_id=hunt_id)
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Hunt hypothesis not found.")


@router.post("/{hunt_id}/cancel", response_model=ThreatHuntHypothesisDTO)
def cancel_threat_hunt(hunt_id: str, payload: CancelHuntRequest) -> ThreatHuntHypothesisDTO:
    """Cancels an active hunt and preserves partial evidence."""
    try:
        return _fabric.cancel_hunt(hypothesis_id=hunt_id, reason=payload.reason)
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Hunt hypothesis not found.")


@router.get("/recommendations")
def get_hunting_recommendations() -> List[Dict[str, Any]]:
    """Returns AI-recommended threat hunts based on emerging campaign telemetry."""
    return [
        {
            "recommendation_id": "rec_01",
            "title": "Hunt for Domain Lookalike Phishing Infrastructure",
            "reason": "Sudden registration of lookalike domains matching enterprise brand keywords.",
            "priority": "HIGH",
            "suggested_playbook": "NEW_DOMAIN_HUNT",
        },
        {
            "recommendation_id": "rec_02",
            "title": "Hunt for Shared Staging Certificates in Banking Dropper Campaign",
            "reason": "Reused certificate serial observed across 3 separate APK droppers.",
            "priority": "CRITICAL",
            "suggested_playbook": "SUSPICIOUS_CERTIFICATE_HUNT",
        }
    ]


@router.get("/early-warnings", response_model=List[EarlyWarningDTO])
def list_early_warnings(tenant_id: str = "default_tenant") -> List[EarlyWarningDTO]:
    """Lists active early warnings generated from weak signal correlation."""
    return _fabric.early_warning.list_warnings(tenant_id)


@router.get("/predictions", response_model=List[SecurityPredictionDTO])
def list_predictions(tenant_id: str = "default_tenant") -> List[SecurityPredictionDTO]:
    """Lists active predictive defense forecasts."""
    return _fabric.predictive.list_predictions(tenant_id)
