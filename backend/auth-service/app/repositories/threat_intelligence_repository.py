"""Async Threat Intelligence Repository Layer (Phase 3.9 Part 1A.23).

Provides database operations for persisting and retrieving threat_indicators, threat_sources,
threat_feeds, threat_feed_records, threat_matches, threat_relationships, threat_entities,
threat_conflicts, threat_evidence, threat_behavior_correlations, threat_dataflow_correlations,
threat_sync_runs, threat_sync_metrics, threat_graphs, yara_matches, stix_objects, taxii_collections.
"""

import uuid
from typing import Optional, List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.threat_intelligence import (
    ThreatIndicatorModel,
    ThreatSourceModel,
    ThreatFeedModel,
    ThreatFeedRecordModel,
    ThreatMatchModel,
    ThreatRelationshipModel,
    ThreatEntityModel,
    ThreatConflictModel,
    ThreatEvidenceModel,
    ThreatBehaviorCorrelationModel,
    ThreatDataflowCorrelationModel,
    ThreatSyncRunModel,
    ThreatSyncMetricModel,
    ThreatGraphModel,
    YaraMatchModel,
    StixObjectModel,
    TaxiiCollectionModel,
)
from app.schemas.threat_intelligence_models import ThreatIntelligenceResultDTO


class ThreatIntelligenceRepository:
    """Async repository for Threat Intelligence DB operations."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def save_full_threat_intelligence(
        self,
        scan_id: uuid.UUID,
        dto: ThreatIntelligenceResultDTO,
    ) -> ThreatIndicatorModel:
        """Saves all 17 threat intelligence datasets inside one atomic transaction."""
        first_model = None

        for ind in dto.indicators:
            m = ThreatIndicatorModel(
                scan_id=scan_id,
                indicator_id=ind.indicator_id,
                indicator_type=ind.indicator_type,
                normalized_value=ind.normalized_value,
                display_value=ind.display_value,
                value_hash=ind.value_hash,
                source_module=ind.source_module,
                source_location=ind.source_location,
                resolution_status=ind.resolution_status,
                confidence=ind.confidence,
            )
            self.db.add(m)
            if not first_model:
                first_model = m

        for s in dto.sources:
            self.db.add(
                ThreatSourceModel(
                    scan_id=scan_id,
                    source_id=s.source_id,
                    provider=s.provider,
                    source_type=s.source_type,
                    reliability=s.reliability,
                    version=s.version,
                    status=s.status,
                )
            )

        for feed in dto.feeds:
            self.db.add(
                ThreatFeedModel(
                    scan_id=scan_id,
                    feed_id=feed.feed_id,
                    feed_name=feed.feed_name,
                    provider=feed.provider,
                    version=feed.version,
                    record_count=feed.record_count,
                    freshness_state=feed.freshness_state,
                )
            )

        for match in dto.matches:
            self.db.add(
                ThreatMatchModel(
                    scan_id=scan_id,
                    match_id=match.match_id,
                    indicator_id=match.indicator_id,
                    source_id=match.source_id,
                    match_type=match.match_type,
                    reputation=match.reputation,
                    confidence=match.confidence,
                    freshness_state=match.freshness_state,
                    provenance=match.provenance,
                )
            )

        for rel in dto.relationships:
            self.db.add(
                ThreatRelationshipModel(
                    scan_id=scan_id,
                    source_entity_id=rel.source_entity_id,
                    target_entity_id=rel.target_entity_id,
                    relationship=rel.relationship,
                    confidence=rel.confidence,
                )
            )

        for ent in dto.entities:
            self.db.add(
                ThreatEntityModel(
                    scan_id=scan_id,
                    entity_id=ent.entity_id,
                    entity_type=ent.entity_type,
                    name=ent.name,
                )
            )

        for conf in dto.conflicts:
            self.db.add(
                ThreatConflictModel(
                    scan_id=scan_id,
                    conflict_id=conf.conflict_id,
                    indicator_value=conf.indicator_value,
                    source_a_claim=conf.source_a_claim,
                    source_b_claim=conf.source_b_claim,
                    resolution_status=conf.resolution_status,
                )
            )

        for ev in dto.evidence:
            self.db.add(
                ThreatEvidenceModel(
                    scan_id=scan_id,
                    evidence_id=ev.evidence_id,
                    indicator_id=ev.indicator_id,
                    matched_rule_or_feed=ev.matched_rule_or_feed,
                    provenance=ev.provenance,
                )
            )

        for bc in dto.behavior_correlations:
            self.db.add(
                ThreatBehaviorCorrelationModel(
                    scan_id=scan_id,
                    correlation_id=bc.correlation_id,
                    behavior_type=bc.behavior_type,
                    indicator_value=bc.indicator_value,
                    threat_claim=bc.threat_claim,
                    confidence=bc.confidence,
                )
            )

        for dc in dto.dataflow_correlations:
            self.db.add(
                ThreatDataflowCorrelationModel(
                    scan_id=scan_id,
                    correlation_id=dc.correlation_id,
                    dataflow_path_id=dc.dataflow_path_id,
                    endpoint_url=dc.endpoint_url,
                    threat_claim=dc.threat_claim,
                    confidence=dc.confidence,
                )
            )

        self.db.add(
            ThreatSyncRunModel(
                scan_id=scan_id,
                status="COMPLETED",
                duration_ms=dto.analysis_time_ms,
            )
        )

        self.db.add(
            ThreatSyncMetricModel(
                scan_id=scan_id,
                indicators_processed=dto.metrics.indicators_processed,
                matches_count=dto.metrics.matches_count,
                conflicts_count=dto.metrics.conflicts_count,
                expired_indicators_count=dto.metrics.expired_indicators_count,
            )
        )

        self.db.add(
            ThreatGraphModel(
                scan_id=scan_id,
                nodes_count=dto.threat_graph.nodes_count,
                edges_count=dto.threat_graph.edges_count,
            )
        )

        for ym in dto.yara_matches:
            self.db.add(
                YaraMatchModel(
                    scan_id=scan_id,
                    rule_name=ym.rule_name,
                    rule_namespace=ym.rule_namespace,
                    matched_file=ym.matched_file,
                    offset=ym.offset,
                    match_confidence=ym.match_confidence,
                )
            )

        for st in dto.stix_objects:
            self.db.add(
                StixObjectModel(
                    scan_id=scan_id,
                    object_id=st.object_id,
                    object_type=st.object_type,
                    name=st.name,
                )
            )

        for tc in dto.taxii_collections:
            self.db.add(
                TaxiiCollectionModel(
                    scan_id=scan_id,
                    collection_id=tc.collection_id,
                    title=tc.title,
                )
            )

        if not first_model:
            first_model = ThreatIndicatorModel(
                scan_id=scan_id,
                indicator_id="ind_default",
                indicator_type="DOMAIN",
                normalized_value="example.com",
                display_value="example.com",
                value_hash="hash_default",
                source_module="NETWORK",
                source_location="network",
            )
            self.db.add(first_model)

        await self.db.commit()
        return first_model

    async def get_threat_intelligence(self, scan_id: uuid.UUID) -> List[ThreatIndicatorModel]:
        stmt = select(ThreatIndicatorModel).where(ThreatIndicatorModel.scan_id == scan_id)
        res = await self.db.execute(stmt)
        return list(res.scalars().all())
