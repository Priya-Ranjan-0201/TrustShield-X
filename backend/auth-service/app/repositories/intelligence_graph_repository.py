"""Repository Layer for Unified Trust Intelligence Graph (Phase 4.0 Part 5 — Sections 46, 84).

Provides async database operations for entities, relationships, campaigns, attack chains,
snapshots, correlation runs, review queue items, and graph traversal queries.
"""

from typing import List, Optional, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete, and_, or_
from app.models.intelligence_graph import (
    CanonicalEntityModel,
    EntityAliasModel,
    EntityObservationModel,
    EntityResolutionRecordModel,
    IntelligenceRelationshipModel,
    RelationshipEvidenceModel,
    RelationshipProvenanceModel,
    CorrelationCandidateModel,
    CorrelationRunModel,
    ThreatCampaignModel,
    CampaignEntityModel,
    CampaignRelationshipModel,
    AttackChainModel,
    AttackChainStepModel,
    ThreatActorAssociationModel,
    GraphVersionModel,
    GraphSnapshotModel,
    GraphChangeModel,
    CorrelationReviewQueueModel,
)


class IntelligenceGraphRepository:
    """Async repository for Intelligence Graph persistence and queries."""

    def __init__(self, db: AsyncSession):
        self.db = db

    # -----------------------------------------------------------------------
    # Entity Operations
    # -----------------------------------------------------------------------

    async def create_entity(self, entity_data: Dict[str, Any]) -> CanonicalEntityModel:
        entity = CanonicalEntityModel(**entity_data)
        self.db.add(entity)
        await self.db.flush()
        return entity

    async def get_entity(self, entity_id: str) -> Optional[CanonicalEntityModel]:
        stmt = select(CanonicalEntityModel).where(CanonicalEntityModel.entity_id == entity_id)
        res = await self.db.execute(stmt)
        return res.scalar_one_or_none()

    async def get_entity_by_hash(self, value_hash: str) -> Optional[CanonicalEntityModel]:
        stmt = select(CanonicalEntityModel).where(CanonicalEntityModel.value_hash == value_hash)
        res = await self.db.execute(stmt)
        return res.scalar_one_or_none()

    async def search_entities(
        self, query: str, entity_types: Optional[List[str]] = None, organization_id: Optional[str] = None, limit: int = 50
    ) -> List[CanonicalEntityModel]:
        q = f"%{query.strip()}%"
        stmt = select(CanonicalEntityModel).where(
            or_(
                CanonicalEntityModel.canonical_value.ilike(q),
                CanonicalEntityModel.display_value.ilike(q),
                CanonicalEntityModel.normalized_value.ilike(q),
            )
        )
        if entity_types:
            stmt = stmt.where(CanonicalEntityModel.entity_type.in_(entity_types))
        if organization_id:
            stmt = stmt.where(
                or_(
                    CanonicalEntityModel.organization_id == organization_id,
                    CanonicalEntityModel.organization_id.is_(None),
                )
            )
        stmt = stmt.limit(limit)
        res = await self.db.execute(stmt)
        return list(res.scalars().all())

    # -----------------------------------------------------------------------
    # Relationship Operations
    # -----------------------------------------------------------------------

    async def create_relationship(self, rel_data: Dict[str, Any]) -> IntelligenceRelationshipModel:
        rel = IntelligenceRelationshipModel(**rel_data)
        self.db.add(rel)
        await self.db.flush()
        return rel

    async def get_relationship(self, relationship_id: str) -> Optional[IntelligenceRelationshipModel]:
        stmt = select(IntelligenceRelationshipModel).where(
            IntelligenceRelationshipModel.relationship_id == relationship_id
        )
        res = await self.db.execute(stmt)
        return res.scalar_one_or_none()

    async def list_neighbors(
        self, entity_id: str, depth: int = 1, limit: int = 100
    ) -> List[IntelligenceRelationshipModel]:
        stmt = select(IntelligenceRelationshipModel).where(
            or_(
                IntelligenceRelationshipModel.source_entity_id == entity_id,
                IntelligenceRelationshipModel.target_entity_id == entity_id,
            )
        ).limit(limit)
        res = await self.db.execute(stmt)
        return list(res.scalars().all())

    # -----------------------------------------------------------------------
    # Campaign & Attack Chain Operations
    # -----------------------------------------------------------------------

    async def create_campaign(self, camp_data: Dict[str, Any]) -> ThreatCampaignModel:
        camp = ThreatCampaignModel(**camp_data)
        self.db.add(camp)
        await self.db.flush()
        return camp

    async def get_campaign(self, campaign_id: str) -> Optional[ThreatCampaignModel]:
        stmt = select(ThreatCampaignModel).where(ThreatCampaignModel.campaign_id == campaign_id)
        res = await self.db.execute(stmt)
        return res.scalar_one_or_none()

    async def list_campaigns(self, limit: int = 50) -> List[ThreatCampaignModel]:
        stmt = select(ThreatCampaignModel).order_by(ThreatCampaignModel.created_at.desc()).limit(limit)
        res = await self.db.execute(stmt)
        return list(res.scalars().all())

    async def create_attack_chain(self, chain_data: Dict[str, Any]) -> AttackChainModel:
        chain = AttackChainModel(**chain_data)
        self.db.add(chain)
        await self.db.flush()
        return chain

    async def get_attack_chain(self, chain_id: str) -> Optional[AttackChainModel]:
        stmt = select(AttackChainModel).where(AttackChainModel.chain_id == chain_id)
        res = await self.db.execute(stmt)
        return res.scalar_one_or_none()

    # -----------------------------------------------------------------------
    # Review Queue & Correlation Runs
    # -----------------------------------------------------------------------

    async def create_review_item(self, item_data: Dict[str, Any]) -> CorrelationReviewQueueModel:
        item = CorrelationReviewQueueModel(**item_data)
        self.db.add(item)
        await self.db.flush()
        return item

    async def list_pending_reviews(self, limit: int = 50) -> List[CorrelationReviewQueueModel]:
        stmt = select(CorrelationReviewQueueModel).where(
            CorrelationReviewQueueModel.status == "PENDING"
        ).order_by(CorrelationReviewQueueModel.created_at.desc()).limit(limit)
        res = await self.db.execute(stmt)
        return list(res.scalars().all())

    async def create_correlation_run(self, run_data: Dict[str, Any]) -> CorrelationRunModel:
        run = CorrelationRunModel(**run_data)
        self.db.add(run)
        await self.db.flush()
        return run
