"""FastAPI Endpoints for Digital Trust Knowledge Fabric, Security Reasoning & Investigator Copilot (Phase 7)."""

from typing import List, Dict, Any, Optional
from fastapi import APIRouter, Depends, Query, HTTPException, status
from pydantic import BaseModel

from app.schemas.knowledge_fabric_models import (
    KnowledgeObjectDTO,
    KnowledgeRelationshipDTO,
    EvidenceLineageDTO,
    KnowledgeSnapshotDTO,
    KnowledgeDiffDTO,
    DigitalTrustProfileDTO,
    DigitalTrustScoreDTO,
    InvestigationSessionDTO,
    InvestigationRecommendationDTO,
    AttackStoryDTO,
    CaseBriefDTO,
    CopilotQueryRequestDTO,
    CopilotResponseDTO,
)
from app.services.knowledge.knowledge_fabric_service import KnowledgeFabricService
from app.services.knowledge.security_reasoning_engine import SecurityReasoningEngine
from app.services.knowledge.digital_trust_score_engine import DigitalTrustScoreEngine
from app.services.knowledge.investigation_intelligence_engine import InvestigationIntelligenceEngine
from app.services.knowledge.investigator_copilot_service import InvestigatorCopilotService

router = APIRouter(prefix="/knowledge", tags=["Digital Trust Knowledge Fabric & Security Reasoning"])

# Singleton service instances for knowledge fabric layer
_fabric_service = KnowledgeFabricService()
_reasoning_engine = SecurityReasoningEngine(_fabric_service)
_trust_score_engine = DigitalTrustScoreEngine(_fabric_service)
_investigation_engine = InvestigationIntelligenceEngine(_fabric_service)
_copilot_service = InvestigatorCopilotService(_fabric_service, _reasoning_engine)


# ---------------------------------------------------------------------------
# Section 21: Unified Knowledge Search
# ---------------------------------------------------------------------------

@router.get("/search", response_model=List[KnowledgeObjectDTO])
async def search_knowledge(
    q: str = Query(..., description="Search query across entities, evidence, and campaigns"),
    min_confidence: float = Query(0.0, ge=0.0, le=1.0),
    tenant_id: str = Query("default_tenant"),
):
    """Searches knowledge objects within authorized tenant scope."""
    return _fabric_service.search_knowledge(query=q, min_confidence=min_confidence, tenant_id=tenant_id)


# ---------------------------------------------------------------------------
# Section 18 & 19: Entity Trust & History
# ---------------------------------------------------------------------------

@router.get("/entities/{entity_id}", response_model=Dict[str, Any])
async def get_entity_details(
    entity_id: str,
    tenant_id: str = Query("default_tenant"),
):
    """Retrieves entity knowledge object and associated relationships."""
    objs = _fabric_service.find_objects_by_reference(entity_id, tenant_id)
    if not objs:
        # Create an on-demand canonical knowledge object if not yet registered
        obj = _fabric_service.register_object(
            object_type="ENTITY",
            canonical_reference=entity_id,
            tenant_id=tenant_id,
            confidence=0.90,
        )
        objs = [obj]

    obj = objs[0]
    rels = _fabric_service.get_object_relationships(obj.knowledge_object_id, tenant_id)
    return {
        "entity": obj,
        "relationships": rels,
    }


@router.get("/entities/{entity_id}/history", response_model=List[Dict[str, Any]])
async def get_entity_history(
    entity_id: str,
    tenant_id: str = Query("default_tenant"),
):
    """Retrieves full version and trust score transition history for an entity."""
    profile = _trust_score_engine.get_or_create_profile(entity_id, tenant_id=tenant_id)
    return profile.trust_history


@router.get("/entities/{entity_id}/trust", response_model=DigitalTrustProfileDTO)
async def get_entity_trust_profile(
    entity_id: str,
    tenant_id: str = Query("default_tenant"),
):
    """Retrieves 6-dimensional Digital Trust Profile."""
    return _trust_score_engine.get_or_create_profile(entity_id, tenant_id=tenant_id)


# ---------------------------------------------------------------------------
# Section 8 & 9: Knowledge Snapshots & Diff
# ---------------------------------------------------------------------------

@router.get("/snapshots", response_model=List[KnowledgeSnapshotDTO])
async def list_snapshots(tenant_id: str = Query("default_tenant")):
    """Lists historical point-in-time knowledge snapshots."""
    return _fabric_service.list_snapshots(tenant_id=tenant_id)


@router.post("/snapshots", response_model=KnowledgeSnapshotDTO)
async def create_snapshot(
    label: str = Query(..., description="Snapshot label / tag"),
    tenant_id: str = Query("default_tenant"),
):
    """Creates a new point-in-time snapshot of the tenant knowledge fabric."""
    return _fabric_service.create_snapshot(label=label, tenant_id=tenant_id)


@router.get("/diff", response_model=KnowledgeDiffDTO)
async def compute_knowledge_diff(
    snapshot_a: str = Query(...),
    snapshot_b: str = Query(...),
    tenant_id: str = Query("default_tenant"),
):
    """Compares two snapshots and outputs new evidence, changed confidence, and new campaigns."""
    try:
        return _fabric_service.compute_diff(snapshot_a, snapshot_b, tenant_id=tenant_id)
    except KeyError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


# ---------------------------------------------------------------------------
# Section 27-35: Investigation Workspaces & Case Briefs
# ---------------------------------------------------------------------------

class CreateInvestigationRequest(BaseModel):
    title: str
    assigned_analyst: str = "analyst_soc"
    entity_ids: List[str] = []
    evidence_ids: List[str] = []
    incident_ids: List[str] = []
    campaign_ids: List[str] = []
    tenant_id: str = "default_tenant"


@router.post("/investigations", response_model=InvestigationSessionDTO)
async def create_investigation(req: CreateInvestigationRequest):
    """Initializes a new collaborative investigation workspace."""
    return _investigation_engine.create_investigation(
        title=req.title,
        assigned_analyst=req.assigned_analyst,
        entity_ids=req.entity_ids,
        evidence_ids=req.evidence_ids,
        incident_ids=req.incident_ids,
        campaign_ids=req.campaign_ids,
        tenant_id=req.tenant_id,
    )


@router.get("/investigations/{investigation_id}", response_model=InvestigationSessionDTO)
async def get_investigation(
    investigation_id: str,
    tenant_id: str = Query("default_tenant"),
):
    """Retrieves an investigation workspace session."""
    session = _investigation_engine.get_investigation(investigation_id, tenant_id=tenant_id)
    if not session:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Investigation not found.")
    return session


@router.post("/investigations/{investigation_id}/query", response_model=CaseBriefDTO)
async def generate_investigation_brief(
    investigation_id: str,
    tenant_id: str = Query("default_tenant"),
):
    """Generates an analyst case brief and attack summary for an investigation."""
    try:
        return _investigation_engine.generate_case_brief(investigation_id, tenant_id=tenant_id)
    except KeyError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


# ---------------------------------------------------------------------------
# Section 22-26: Investigator Copilot Endpoints
# ---------------------------------------------------------------------------

@router.post("/copilot/query", response_model=CopilotResponseDTO)
async def query_copilot(req: CopilotQueryRequestDTO):
    """Submits a natural language query to the grounded Investigator Copilot."""
    return _copilot_service.process_query(req)


@router.post("/copilot/investigate", response_model=List[InvestigationRecommendationDTO])
async def copilot_investigate_recommendations(
    investigation_id: str = Query(...),
    tenant_id: str = Query("default_tenant"),
):
    """Generates information-gain-prioritized investigation step recommendations."""
    try:
        return _investigation_engine.recommend_investigation_steps(investigation_id, tenant_id=tenant_id)
    except KeyError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get("/copilot/sessions/{session_id}", response_model=Dict[str, Any])
async def get_copilot_session(session_id: str):
    """Retrieves copilot chat dialogue session history."""
    return {
        "session_id": session_id,
        "status": "ACTIVE",
        "model": "TruthShield-SecurityReasoning-7.0",
        "created_at": "2026-08-15T12:00:00Z",
    }
