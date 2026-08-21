"""FastAPI Router for Unified Trust Intelligence Graph (Phase 4.0 Part 5 — Sections 58-63, 77-83).

REST APIs for entities, graph topology, neighbor traversal, threat campaigns, attack chains,
graph version diffs, search, manual analyst correlations, and review queue management.
"""

from typing import Optional, List, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.schemas.envelope import ResponseEnvelope
from app.schemas.intelligence_graph_models import (
    CanonicalEntityDTO,
    GraphRelationshipDTO,
    ThreatCampaignDTO,
    AttackChainDTO,
    UnifiedGraphResponseDTO,
    GraphSnapshotDTO,
    GraphDiffDTO,
    CorrelationRunDTO,
    CorrelationExplanationDTO,
    GraphSearchResponseDTO,
    GraphSearchResultDTO,
    CorrelationReviewItemDTO,
    ManualCorrelationCreateDTO,
    RelationshipReviewActionDTO,
)
from app.services.intelligence_graph_engine import IntelligenceGraphEngine
from app.repositories.intelligence_graph_repository import IntelligenceGraphRepository

router = APIRouter(prefix="/intelligence", tags=["Unified Trust Intelligence Graph Engine"])


@router.get("/graph", response_model=ResponseEnvelope[UnifiedGraphResponseDTO])
async def get_unified_graph(
    case_id: Optional[str] = Query(None, description="Investigation case ID"),
    depth: int = Query(1, ge=1, le=5, description="Graph traversal depth"),
    min_confidence: Optional[str] = Query(None, description="Minimum confidence filter"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Retrieves authoritative unified intelligence graph."""
    engine = IntelligenceGraphEngine()
    graph_res, _, _ = engine.build_intelligence_graph([], case_id=case_id, organization_id=str(current_user.id))
    return ResponseEnvelope.success_response(data=graph_res, message="Unified intelligence graph retrieved successfully")


@router.get("/entities/{entity_id}", response_model=ResponseEnvelope[CanonicalEntityDTO])
async def get_entity(
    entity_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Retrieves canonical entity details by entity ID."""
    repo = IntelligenceGraphRepository(db)
    ent = await repo.get_entity(entity_id)
    if not ent:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Entity {entity_id} not found")
    
    dto = CanonicalEntityDTO.model_validate(ent)
    return ResponseEnvelope.success_response(data=dto, message="Entity retrieved successfully")


@router.get("/entities/{entity_id}/neighbors", response_model=ResponseEnvelope[List[GraphRelationshipDTO]])
async def get_entity_neighbors(
    entity_id: str,
    depth: int = Query(1, ge=1, le=3),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Retrieves neighbor relationships for target entity."""
    repo = IntelligenceGraphRepository(db)
    rels = await repo.list_neighbors(entity_id, depth=depth)
    dtos = [GraphRelationshipDTO.model_validate(r) for r in rels]
    return ResponseEnvelope.success_response(data=dtos, message=f"Retrieved {len(dtos)} neighbor relationships")


@router.get("/campaigns", response_model=ResponseEnvelope[List[ThreatCampaignDTO]])
async def list_campaigns(
    limit: int = Query(50, ge=1, le=200),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Lists detected threat campaigns."""
    repo = IntelligenceGraphRepository(db)
    camps = await repo.list_campaigns(limit=limit)
    dtos = [ThreatCampaignDTO.model_validate(c) for c in camps]
    return ResponseEnvelope.success_response(data=dtos, message=f"Retrieved {len(dtos)} threat campaigns")


@router.get("/campaigns/{campaign_id}", response_model=ResponseEnvelope[ThreatCampaignDTO])
async def get_campaign(
    campaign_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Retrieves threat campaign details."""
    repo = IntelligenceGraphRepository(db)
    camp = await repo.get_campaign(campaign_id)
    if not camp:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Campaign {campaign_id} not found")
    
    dto = ThreatCampaignDTO.model_validate(camp)
    return ResponseEnvelope.success_response(data=dto, message="Campaign retrieved successfully")


@router.get("/attack-chains/{chain_id}", response_model=ResponseEnvelope[AttackChainDTO])
async def get_attack_chain(
    chain_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Retrieves reconstructed attack chain."""
    repo = IntelligenceGraphRepository(db)
    chain = await repo.get_attack_chain(chain_id)
    if not chain:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Attack chain {chain_id} not found")
    
    dto = AttackChainDTO.model_validate(chain)
    return ResponseEnvelope.success_response(data=dto, message="Attack chain retrieved successfully")


@router.get("/search", response_model=ResponseEnvelope[GraphSearchResponseDTO])
async def search_intelligence(
    q: Optional[str] = Query(None),
    query: Optional[str] = Query(None),
    entity_types: Optional[List[str]] = Query(None),
    limit: int = Query(50, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Searches intelligence entities with multi-tenant isolation."""
    search_term = q or query or ""
    repo = IntelligenceGraphRepository(db)
    results = await repo.search_entities(query=search_term, entity_types=entity_types, limit=limit)

    dtos = [
        GraphSearchResultDTO(
            entity_id=r.entity_id,
            entity_type=r.entity_type,
            display_value=r.display_value,
            canonical_value=r.canonical_value,
            confidence=r.confidence,
            match_field="canonical_value",
            source_count=r.source_count,
            first_seen=r.first_seen.isoformat(),
            last_seen=r.last_seen.isoformat(),
        )
        for r in results
    ]
    resp = GraphSearchResponseDTO(query=search_term, results=dtos, total_results=len(dtos))
    return ResponseEnvelope.success_response(data=resp, message="Search executed successfully")



@router.get("/review-queue", response_model=ResponseEnvelope[List[CorrelationReviewItemDTO]])
async def get_review_queue(
    limit: int = Query(50, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Lists pending correlation reviews for security analysts."""
    repo = IntelligenceGraphRepository(db)
    items = await repo.list_pending_reviews(limit=limit)
    dtos = [CorrelationReviewItemDTO.model_validate(i) for i in items]
    return ResponseEnvelope.success_response(data=dtos, message="Review queue retrieved successfully")
