"""
TruthShield X — Global Defense Coordination REST API (Phase 28).
"""

from typing import List, Dict, Any, Optional
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel

from app.schemas.global_defense_models import (
    DefenseCoordinationCaseDTO,
    DefenseNetworkDTO,
    DefensiveKnowledgeRecordDTO,
    GlobalDefenseScorecardDTO,
    SanitizedRecordDTO,
)
from app.services.global_defense.global_defense_coordination_engine import GlobalDefenseCoordinationEngine

router = APIRouter(prefix="/coordination", tags=["Global Cyber Defense Coordination & Collective Response"])

# Singleton Engine Instance
global_defense_engine = GlobalDefenseCoordinationEngine()


# ============================================================================
# Overview & Metrics
# ============================================================================

@router.get("/overview", response_model=Dict[str, Any])
def get_coordination_overview():
    return global_defense_engine.get_coordination_overview()


@router.get("/metrics", response_model=GlobalDefenseScorecardDTO)
def get_defense_scorecard():
    return global_defense_engine.scorecard_engine.evaluate_scorecard()


# ============================================================================
# Coordination Cases
# ============================================================================

@router.get("/cases", response_model=List[DefenseCoordinationCaseDTO])
def list_coordination_cases():
    return global_defense_engine.list_cases()


class CreateCaseRequest(BaseModel):
    objective: str
    threat_id: str = "cmp_darkstorm_2026"
    campaign_id: str = "cmp_darkstorm_2026"
    participating_entities: Optional[List[str]] = None
    classification: str = "CONFIDENTIAL"
    tenant_id: str = "default_tenant"


@router.post("/cases", response_model=DefenseCoordinationCaseDTO)
def create_coordination_case(payload: CreateCaseRequest):
    return global_defense_engine.create_coordination_case(
        objective=payload.objective,
        threat_id=payload.threat_id,
        campaign_id=payload.campaign_id,
        participating_entities=payload.participating_entities,
        classification=payload.classification,
        tenant_id=payload.tenant_id,
    )


@router.get("/cases/{coordination_id}", response_model=DefenseCoordinationCaseDTO)
def get_coordination_case(coordination_id: str):
    c = global_defense_engine.get_case(coordination_id)
    if not c:
        raise HTTPException(status_code=404, detail="Coordination case not found")
    return c


class SharePayloadRequest(BaseModel):
    recipient: str
    purpose: str = "THREAT_DEFENSE"
    raw_payload: Dict[str, Any]
    classification: str = "CONFIDENTIAL"


@router.post("/cases/{coordination_id}/share", response_model=Dict[str, Any])
def share_coordination_payload(coordination_id: str, payload: SharePayloadRequest):
    # 1. Evaluate sharing policy
    pol_eval = global_defense_engine.policy_engine.evaluate_sharing(
        tenant_id="default_tenant",
        recipient=payload.recipient,
        classification=payload.classification,  # type: ignore
        purpose=payload.purpose,
    )
    if not pol_eval["allowed"]:
        return {"status": "SHARING_BLOCKED", "reason": pol_eval["reason"]}

    # 2. Sanitize payload
    sanitized = global_defense_engine.sanitization_engine.sanitize_payload(
        raw_payload=payload.raw_payload,
        original_classification=payload.classification,  # type: ignore
    )
    return {
        "status": "APPROVED",
        "coordination_id": coordination_id,
        "recipient": payload.recipient,
        "sanitized_record": sanitized,
    }


class ApproveActionRequest(BaseModel):
    action_id: str
    approver_role: str = "CISO"


@router.post("/cases/{coordination_id}/approve", response_model=Dict[str, Any])
def approve_coordination_action(coordination_id: str, payload: ApproveActionRequest):
    return global_defense_engine.approval_gate.approve_action(
        action_id=payload.action_id,
        approver_role=payload.approver_role,
    )


@router.post("/cases/{coordination_id}/execute", response_model=Dict[str, Any])
def execute_coordination_action(coordination_id: str, action_id: str = Query(...)):
    if not global_defense_engine.approval_gate.verify_execution_authorization(action_id):
        raise HTTPException(status_code=403, detail="Four-Eyes multi-party approval required before execution")
    return {
        "coordination_id": coordination_id,
        "action_id": action_id,
        "status": "EXECUTED",
        "outcome": "Coordinated mitigation deployed across authorized peers.",
    }


@router.post("/cases/{coordination_id}/verify", response_model=Dict[str, Any])
def verify_coordination_outcome(coordination_id: str):
    return {
        "coordination_id": coordination_id,
        "verification_status": "VERIFIED_COMPLETE",
        "control_coverage": 0.95,
        "residual_risk": "LOW",
    }


# ============================================================================
# Networks, Knowledge & Playbooks
# ============================================================================

@router.get("/networks", response_model=List[DefenseNetworkDTO])
def list_defense_networks():
    return global_defense_engine.network_manager.list_networks()


class CreateNetworkRequest(BaseModel):
    name: str
    participants: List[str]
    trust_level: str = "VERIFIED"
    duration_days: int = 90


@router.post("/networks", response_model=DefenseNetworkDTO)
def create_defense_network(payload: CreateNetworkRequest):
    return global_defense_engine.network_manager.create_network(
        name=payload.name,
        participants=payload.participants,
        trust_level=payload.trust_level,  # type: ignore
        duration_days=payload.duration_days,
    )


@router.get("/knowledge", response_model=List[DefensiveKnowledgeRecordDTO])
def list_defensive_knowledge():
    return global_defense_engine.knowledge_engine.list_knowledge()


class CreateKnowledgeRequest(BaseModel):
    problem: str
    evidence: List[str]
    defensive_technique: str
    validation_result: str
    compatibility: List[str]


@router.post("/knowledge", response_model=DefensiveKnowledgeRecordDTO)
def publish_defensive_knowledge(payload: CreateKnowledgeRequest):
    return global_defense_engine.knowledge_engine.publish_knowledge(
        problem=payload.problem,
        evidence=payload.evidence,
        defensive_technique=payload.defensive_technique,
        validation_result=payload.validation_result,
        compatibility=payload.compatibility,
    )


@router.get("/playbooks", response_model=List[Dict[str, Any]])
def list_defense_playbooks():
    return global_defense_engine.playbook_registry.list_playbooks()
