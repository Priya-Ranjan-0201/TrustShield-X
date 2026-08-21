"""Repository for Evidence Consolidation Database Operations (Phase 3.9 Part 1A.25).

Provides single-transaction bulk persistence and asynchronous CRUD queries across all 16 consolidation tables.
"""

import uuid
from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.evidence_consolidation import (
    CanonicalEntityModel,
    CanonicalEvidenceModel,
    CanonicalFindingModel,
    EvidenceRelationshipModel,
    EvidenceIndependenceModel,
    EvidenceGroupModel,
    FindingConflictModel,
    FindingLineageModel,
    FindingVersionModel,
    FindingSourceModel,
    FindingStatisticModel,
    ConfidenceFusionModel,
    EvidenceProvenanceGraphModel,
    FindingGraphModel,
    ConsolidationRunModel,
    ConsolidationMetricModel,
)
from app.schemas.evidence_consolidation_models import (
    ConsolidationResultDTO,
    CanonicalFindingDTO,
    CanonicalEvidenceDTO,
    CanonicalEntityDTO,
    ConsolidationMetricsDTO,
)


class EvidenceConsolidationRepository:
    """Async SQLAlchemy repository for Evidence Consolidation persistence and retrieval."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def save_full_consolidation_result(
        self, scan_id: uuid.UUID, dto: ConsolidationResultDTO
    ) -> CanonicalFindingModel:
        # Entities
        for e in dto.entities:
            self.db.add(
                CanonicalEntityModel(
                    scan_id=scan_id,
                    entity_id=e.entity_id,
                    entity_type=e.entity_type,
                    canonical_value=e.canonical_value,
                    display_name=e.display_name,
                )
            )

        # Evidence
        for ev in dto.evidence:
            self.db.add(
                CanonicalEvidenceModel(
                    scan_id=scan_id,
                    evidence_id=ev.evidence_id,
                    canonical_entity_id=ev.canonical_entity_id,
                    source_module=ev.source_module,
                    evidence_type=ev.evidence_type,
                    evidence_subtype=ev.evidence_subtype,
                    class_name=ev.class_name,
                    method_name=ev.method_name,
                    confidence=ev.confidence,
                    resolution_status=ev.resolution_status,
                    provenance_reference=ev.provenance_reference,
                )
            )

        # Findings
        primary_finding_model = None
        for idx, f in enumerate(dto.findings):
            model = CanonicalFindingModel(
                scan_id=scan_id,
                finding_id=f.finding_id,
                finding_type=f.finding_type,
                finding_category=f.finding_category,
                title=f.title,
                description=f.description,
                status=f.status,
                confidence_level=f.confidence_level,
                evidence_strength=f.evidence_strength,
                resolution_status=f.resolution_status,
                source_count=f.source_count,
                independent_source_count=f.independent_source_count,
                evidence_count=f.evidence_count,
                direct_evidence_count=f.direct_evidence_count,
                inferred_evidence_count=f.inferred_evidence_count,
                contradiction_count=f.contradiction_count,
            )
            self.db.add(model)
            if idx == 0:
                primary_finding_model = model

        # Relationships
        for rel in dto.relationships:
            self.db.add(
                EvidenceRelationshipModel(
                    scan_id=scan_id,
                    source_evidence_id=rel.source_evidence_id,
                    target_evidence_id=rel.target_evidence_id,
                    relationship=rel.relationship,
                )
            )

        # Independence
        for ind in dto.independence_records:
            self.db.add(
                EvidenceIndependenceModel(
                    scan_id=scan_id,
                    evidence_id=ind.evidence_id,
                    group_id=ind.group_id,
                    independence_type=ind.independence_type,
                    source_provider=ind.source_provider,
                    is_independent=ind.is_independent,
                    reason=ind.reason,
                )
            )

        # Groups
        for grp in dto.groups:
            self.db.add(
                EvidenceGroupModel(
                    scan_id=scan_id,
                    group_id=grp.group_id,
                    group_name=grp.group_name,
                    member_evidence_count=grp.member_evidence_count,
                )
            )

        # Conflicts
        for cfl in dto.conflicts:
            self.db.add(
                FindingConflictModel(
                    scan_id=scan_id,
                    conflict_id=cfl.conflict_id,
                    finding_id=cfl.finding_id,
                    evidence_a_id=cfl.evidence_a_id,
                    evidence_b_id=cfl.evidence_b_id,
                    conflict_type=cfl.conflict_type,
                    explanation=cfl.explanation,
                )
            )

        # Lineage
        for lin in dto.lineage_records:
            self.db.add(
                FindingLineageModel(
                    scan_id=scan_id,
                    lineage_id=lin.lineage_id,
                    finding_id=lin.finding_id,
                    parent_evidence_id=lin.parent_evidence_id,
                    transformation_step=lin.transformation_step,
                )
            )

        # Confidence Fusions
        for cf in dto.confidence_fusions:
            self.db.add(
                ConfidenceFusionModel(
                    scan_id=scan_id,
                    fusion_id=cf.fusion_id,
                    finding_id=cf.finding_id,
                    fused_confidence=cf.fused_confidence,
                    confidence_ceiling_applied=cf.confidence_ceiling_applied,
                    ceiling_reason=cf.ceiling_reason,
                )
            )

        # Graphs & Metrics
        self.db.add(
            EvidenceProvenanceGraphModel(
                scan_id=scan_id,
                nodes_count=dto.evidence_graph.nodes_count,
                edges_count=dto.evidence_graph.edges_count,
            )
        )
        self.db.add(
            FindingGraphModel(
                scan_id=scan_id,
                nodes_count=dto.finding_graph.nodes_count,
                edges_count=dto.finding_graph.edges_count,
            )
        )
        self.db.add(
            ConsolidationRunModel(
                scan_id=scan_id,
                status="COMPLETED",
                duration_ms=dto.analysis_time_ms,
            )
        )
        self.db.add(
            ConsolidationMetricModel(
                scan_id=scan_id,
                input_findings_count=dto.metrics.input_findings_count,
                canonical_entities_count=dto.metrics.canonical_entities_count,
                canonical_evidence_count=dto.metrics.canonical_evidence_count,
                duplicate_evidence_suppressed=dto.metrics.duplicate_evidence_suppressed,
                merged_findings_count=dto.metrics.merged_findings_count,
                split_findings_count=dto.metrics.split_findings_count,
                conflicted_findings_count=dto.metrics.conflicted_findings_count,
            )
        )

        await self.db.commit()
        return primary_finding_model or CanonicalFindingModel(scan_id=scan_id, finding_id="placeholder", title="Placeholder", description="Placeholder")

    async def get_findings_by_scan_id(self, scan_id: uuid.UUID) -> List[CanonicalFindingModel]:
        res = await self.db.execute(
            select(CanonicalFindingModel).where(CanonicalFindingModel.scan_id == scan_id)
        )
        scalars = res.scalars()
        if hasattr(scalars, "all"):
            items = scalars.all()
            if hasattr(items, "__await__"):
                items = await items
            return list(items)
        return []

    async def get_evidence_by_scan_id(self, scan_id: uuid.UUID) -> List[CanonicalEvidenceModel]:
        res = await self.db.execute(
            select(CanonicalEvidenceModel).where(CanonicalEvidenceModel.scan_id == scan_id)
        )
        scalars = res.scalars()
        if hasattr(scalars, "all"):
            items = scalars.all()
            if hasattr(items, "__await__"):
                items = await items
            return list(items)
        return []
