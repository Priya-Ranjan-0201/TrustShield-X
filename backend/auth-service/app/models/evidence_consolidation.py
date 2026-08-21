"""SQLAlchemy 2.0 ORM Models for Enterprise Evidence Consolidation Layer (Phase 3.9 Part 1A.25).

Defines database models for 16 consolidation tables:
canonical_entities, canonical_evidence, canonical_findings, evidence_relationships,
evidence_independence, evidence_groups, finding_conflicts, finding_lineage,
finding_versions, finding_sources, finding_statistics, confidence_fusion_records,
evidence_provenance_graphs, finding_graphs, consolidation_runs, consolidation_metrics.
"""

import uuid
from datetime import datetime, timezone
from typing import Optional, List
from sqlalchemy import String, Integer, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from app.models.base import Base


class CanonicalEntityModel(Base):
    __tablename__ = "canonical_entities"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scan_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False, index=True)
    entity_id: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    entity_type: Mapped[str] = mapped_column(String(64), nullable=False, default="DOMAIN")
    canonical_value: Mapped[str] = mapped_column(String(512), nullable=False, index=True)
    display_name: Mapped[str] = mapped_column(String(512), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class CanonicalEvidenceModel(Base):
    __tablename__ = "canonical_evidence"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scan_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False, index=True)
    evidence_id: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    canonical_entity_id: Mapped[str] = mapped_column(String(128), nullable=False)
    source_module: Mapped[str] = mapped_column(String(128), nullable=False)
    evidence_type: Mapped[str] = mapped_column(String(64), nullable=False, default="NETWORK")
    evidence_subtype: Mapped[str] = mapped_column(String(64), nullable=False, default="DOMAIN_OBSERVATION")
    class_name: Mapped[Optional[str]] = mapped_column(String(256), nullable=True)
    method_name: Mapped[Optional[str]] = mapped_column(String(256), nullable=True)
    confidence: Mapped[str] = mapped_column(String(32), nullable=False, default="HIGH")
    resolution_status: Mapped[str] = mapped_column(String(32), nullable=False, default="RESOLVED")
    provenance_reference: Mapped[str] = mapped_column(String(512), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class CanonicalFindingModel(Base):
    __tablename__ = "canonical_findings"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scan_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False, index=True)
    finding_id: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    finding_type: Mapped[str] = mapped_column(String(128), nullable=False, default="NETWORK_ENDPOINT_OBSERVED")
    finding_category: Mapped[str] = mapped_column(String(64), nullable=False, default="NETWORK")
    title: Mapped[str] = mapped_column(String(256), nullable=False)
    description: Mapped[str] = mapped_column(String(512), nullable=False)
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="CORRELATED", index=True)
    confidence_level: Mapped[str] = mapped_column(String(32), nullable=False, default="HIGH", index=True)
    evidence_strength: Mapped[str] = mapped_column(String(32), nullable=False, default="STRONG")
    resolution_status: Mapped[str] = mapped_column(String(32), nullable=False, default="RESOLVED")
    source_count: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    independent_source_count: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    evidence_count: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    direct_evidence_count: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    inferred_evidence_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    contradiction_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class EvidenceRelationshipModel(Base):
    __tablename__ = "evidence_relationships"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scan_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False, index=True)
    source_evidence_id: Mapped[str] = mapped_column(String(128), nullable=False)
    target_evidence_id: Mapped[str] = mapped_column(String(128), nullable=False)
    relationship: Mapped[str] = mapped_column(String(64), nullable=False, default="SUPPORTS")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class EvidenceIndependenceModel(Base):
    __tablename__ = "evidence_independence"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scan_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False, index=True)
    evidence_id: Mapped[str] = mapped_column(String(128), nullable=False)
    group_id: Mapped[str] = mapped_column(String(128), nullable=False)
    independence_type: Mapped[str] = mapped_column(String(64), nullable=False, default="CROSS_MODULE")
    source_provider: Mapped[str] = mapped_column(String(128), nullable=False)
    is_independent: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    reason: Mapped[str] = mapped_column(String(256), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class EvidenceGroupModel(Base):
    __tablename__ = "evidence_groups"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scan_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False, index=True)
    group_id: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    group_name: Mapped[str] = mapped_column(String(128), nullable=False, default="NETWORK_GROUP")
    member_evidence_count: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class FindingConflictModel(Base):
    __tablename__ = "finding_conflicts"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scan_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False, index=True)
    conflict_id: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    finding_id: Mapped[str] = mapped_column(String(128), nullable=False)
    evidence_a_id: Mapped[str] = mapped_column(String(128), nullable=False)
    evidence_b_id: Mapped[str] = mapped_column(String(128), nullable=False)
    conflict_type: Mapped[str] = mapped_column(String(64), nullable=False, default="CONTRADICTORY_CLAIMS")
    explanation: Mapped[str] = mapped_column(String(512), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class FindingLineageModel(Base):
    __tablename__ = "finding_lineage"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scan_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False, index=True)
    lineage_id: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    finding_id: Mapped[str] = mapped_column(String(128), nullable=False)
    parent_evidence_id: Mapped[str] = mapped_column(String(128), nullable=False)
    transformation_step: Mapped[str] = mapped_column(String(128), nullable=False, default="CORRELATION_TO_CANONICAL")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class FindingVersionModel(Base):
    __tablename__ = "finding_versions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scan_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False, index=True)
    finding_id: Mapped[str] = mapped_column(String(128), nullable=False)
    finding_version: Mapped[str] = mapped_column(String(64), nullable=False, default="1.0.0")
    engine_version: Mapped[str] = mapped_column(String(64), nullable=False, default="1.0.0")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class FindingSourceModel(Base):
    __tablename__ = "finding_sources"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scan_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False, index=True)
    finding_id: Mapped[str] = mapped_column(String(128), nullable=False)
    source_module: Mapped[str] = mapped_column(String(128), nullable=False)
    source_reliability: Mapped[str] = mapped_column(String(32), nullable=False, default="HIGH")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class FindingStatisticModel(Base):
    __tablename__ = "finding_statistics"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scan_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False, index=True)
    total_canonical_findings: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    total_canonical_evidence: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class ConfidenceFusionModel(Base):
    __tablename__ = "confidence_fusion_records"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scan_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False, index=True)
    fusion_id: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    finding_id: Mapped[str] = mapped_column(String(128), nullable=False)
    fused_confidence: Mapped[str] = mapped_column(String(32), nullable=False, default="HIGH")
    confidence_ceiling_applied: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    ceiling_reason: Mapped[Optional[str]] = mapped_column(String(512), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class EvidenceProvenanceGraphModel(Base):
    __tablename__ = "evidence_provenance_graphs"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scan_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False, index=True)
    nodes_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    edges_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class FindingGraphModel(Base):
    __tablename__ = "finding_graphs"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scan_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False, index=True)
    nodes_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    edges_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class ConsolidationRunModel(Base):
    __tablename__ = "consolidation_runs"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scan_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False, index=True)
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="COMPLETED")
    duration_ms: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class ConsolidationMetricModel(Base):
    __tablename__ = "consolidation_metrics"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scan_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False, index=True)
    input_findings_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    canonical_entities_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    canonical_evidence_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    duplicate_evidence_suppressed: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    merged_findings_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    split_findings_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    conflicted_findings_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
