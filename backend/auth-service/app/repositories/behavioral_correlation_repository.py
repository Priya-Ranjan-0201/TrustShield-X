"""Async Behavioral Correlation Repository Layer (Phase 3.9 Part 1A.22).

Provides database operations for persisting and retrieving behavior_entities,
behavior_relationships, behavior_chains, behavior_findings, behavior_evidence,
behavior_conflicts, behavior_summaries, behavior_graphs, correlation_runs,
correlation_metrics, third_party_behaviors.
"""

import uuid
from typing import Optional, List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.behavioral_correlation_intelligence import (
    BehaviorEntityModel,
    BehaviorRelationshipModel,
    BehaviorChainModel,
    BehaviorFindingModel,
    BehaviorEvidenceModel,
    BehaviorConflictModel,
    BehaviorSummaryModel,
    BehaviorGraphModel,
    CorrelationRunModel,
    CorrelationMetricModel,
    ThirdPartyBehaviorModel,
)
from app.schemas.behavioral_correlation_models import BehavioralCorrelationResultDTO


class BehavioralCorrelationRepository:
    """Async repository for Behavioral Correlation DB operations."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def save_full_behavioral_correlation(
        self,
        scan_id: uuid.UUID,
        dto: BehavioralCorrelationResultDTO,
    ) -> BehaviorFindingModel:
        """Saves all 11 behavioral correlation datasets inside one atomic transaction."""
        first_model = None

        for ent in dto.entities:
            self.db.add(
                BehaviorEntityModel(
                    scan_id=scan_id,
                    entity_id=ent.entity_id,
                    entity_type=ent.entity_type,
                    canonical_name=ent.canonical_name,
                    source_module=ent.source_module,
                )
            )

        for rel in dto.relationships:
            self.db.add(
                BehaviorRelationshipModel(
                    scan_id=scan_id,
                    source_entity_id=rel.source_entity_id,
                    target_entity_id=rel.target_entity_id,
                    relationship_type=rel.relationship_type,
                    confidence=rel.confidence,
                    resolution_status=rel.resolution_status,
                )
            )

        for ch in dto.chains:
            self.db.add(
                BehaviorChainModel(
                    scan_id=scan_id,
                    chain_id=ch.chain_id,
                    chain_type=ch.chain_type,
                    start_node=ch.start_node,
                    end_node=ch.end_node,
                    confidence=ch.confidence,
                    resolution_status=ch.resolution_status,
                )
            )

        for f in dto.findings:
            m = BehaviorFindingModel(
                scan_id=scan_id,
                finding_id=f.finding_id,
                finding_type=f.finding_type,
                category=f.category,
                evidence_strength=f.evidence_strength,
                confidence=f.confidence,
                resolution_status=f.resolution_status,
                summary=f.summary,
            )
            self.db.add(m)
            if not first_model:
                first_model = m

        for ev in dto.evidence:
            self.db.add(
                BehaviorEvidenceModel(
                    scan_id=scan_id,
                    evidence_id=ev.evidence_id,
                    module=ev.module,
                    entity_type=ev.entity_type,
                    entity_id=ev.entity_id,
                    class_name=ev.class_name,
                    method_name=ev.method_name,
                    instruction_offset=ev.instruction_offset,
                    source_location=ev.source_location,
                    rule_id=ev.rule_id,
                    evidence_type=ev.evidence_type,
                    confidence=ev.confidence,
                    resolution_status=ev.resolution_status,
                    provenance=ev.provenance,
                )
            )

        for conf in dto.conflicts:
            self.db.add(
                BehaviorConflictModel(
                    scan_id=scan_id,
                    conflict_id=conf.conflict_id,
                    conflict_type=conf.conflict_type,
                    evidence_a=conf.evidence_a,
                    evidence_b=conf.evidence_b,
                    resolution_status=conf.resolution_status,
                )
            )

        for s in dto.summaries:
            self.db.add(
                BehaviorSummaryModel(
                    scan_id=scan_id,
                    title=s.title,
                    summary_text=s.summary_text,
                    findings_count=s.findings_count,
                )
            )

        self.db.add(
            BehaviorGraphModel(
                scan_id=scan_id,
                nodes_count=dto.behavior_graph.nodes_count,
                edges_count=dto.behavior_graph.edges_count,
            )
        )

        self.db.add(
            CorrelationRunModel(
                scan_id=scan_id,
                status="COMPLETED",
                duration_ms=dto.analysis_time_ms,
            )
        )

        self.db.add(
            CorrelationMetricModel(
                scan_id=scan_id,
                entities_processed=dto.metrics.entities_processed,
                relationships_processed=dto.metrics.relationships_processed,
                findings_count=dto.metrics.findings_count,
                chains_count=dto.metrics.chains_count,
                conflicts_count=dto.metrics.conflicts_count,
            )
        )

        for tp in dto.third_party_behaviors:
            self.db.add(
                ThirdPartyBehaviorModel(
                    scan_id=scan_id,
                    sdk_name=tp.sdk_name,
                    sdk_category=tp.sdk_category,
                    data_collected=tp.data_collected,
                    network_endpoint=tp.network_endpoint,
                )
            )

        if not first_model:
            first_model = BehaviorFindingModel(
                scan_id=scan_id,
                finding_id="find_default",
                finding_type="STANDARD_APPLICATION_BEHAVIOR",
                category="DATA_COLLECTION",
                evidence_strength="DIRECT",
                confidence="HIGH",
                resolution_status="RESOLVED",
                summary="Standard execution behavior.",
            )
            self.db.add(first_model)

        await self.db.commit()
        return first_model

    async def get_behavioral_correlation(self, scan_id: uuid.UUID) -> List[BehaviorFindingModel]:
        stmt = select(BehaviorFindingModel).where(BehaviorFindingModel.scan_id == scan_id)
        res = await self.db.execute(stmt)
        return list(res.scalars().all())
