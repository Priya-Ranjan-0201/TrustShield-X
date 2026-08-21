"""SQLAlchemy 2.0 ORM Models for Enterprise Behavioral Correlation & Intelligence Fusion Engine (Phase 3.9 Part 1A.22).

Defines database models for 11 behavior correlation tables:
behavior_entities, behavior_relationships, behavior_chains, behavior_findings, behavior_evidence,
behavior_conflicts, behavior_summaries, behavior_graphs, correlation_runs, correlation_metrics,
third_party_behaviors.
"""

import uuid
from datetime import datetime, timezone
from typing import Optional, List
from sqlalchemy import String, Integer, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from app.models.base import Base


class BehaviorEntityModel(Base):
    __tablename__ = "behavior_entities"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scan_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False, index=True)
    entity_id: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    entity_type: Mapped[str] = mapped_column(String(64), nullable=False, default="CLASS")
    canonical_name: Mapped[str] = mapped_column(String(512), nullable=False)
    source_module: Mapped[str] = mapped_column(String(128), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class BehaviorRelationshipModel(Base):
    __tablename__ = "behavior_relationships"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scan_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False, index=True)
    source_entity_id: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    target_entity_id: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    relationship_type: Mapped[str] = mapped_column(String(64), nullable=False, default="CALLS")
    confidence: Mapped[str] = mapped_column(String(32), nullable=False, default="HIGH")
    resolution_status: Mapped[str] = mapped_column(String(32), nullable=False, default="RESOLVED")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class BehaviorChainModel(Base):
    __tablename__ = "behavior_chains"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scan_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False, index=True)
    chain_id: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    chain_type: Mapped[str] = mapped_column(String(64), nullable=False, default="MULTI_STAGE_DATA_FLOW")
    start_node: Mapped[str] = mapped_column(String(256), nullable=False)
    end_node: Mapped[str] = mapped_column(String(256), nullable=False)
    confidence: Mapped[str] = mapped_column(String(32), nullable=False, default="HIGH")
    resolution_status: Mapped[str] = mapped_column(String(32), nullable=False, default="RESOLVED")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class BehaviorFindingModel(Base):
    __tablename__ = "behavior_findings"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scan_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False, index=True)
    finding_id: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    finding_type: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    category: Mapped[str] = mapped_column(String(64), nullable=False, default="DATA_TRANSMISSION")
    evidence_strength: Mapped[str] = mapped_column(String(32), nullable=False, default="DIRECT")
    confidence: Mapped[str] = mapped_column(String(32), nullable=False, default="HIGH")
    resolution_status: Mapped[str] = mapped_column(String(32), nullable=False, default="RESOLVED")
    summary: Mapped[str] = mapped_column(String(1024), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class BehaviorEvidenceModel(Base):
    __tablename__ = "behavior_evidence"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scan_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False, index=True)
    evidence_id: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    module: Mapped[str] = mapped_column(String(128), nullable=False)
    entity_type: Mapped[str] = mapped_column(String(64), nullable=False, default="API")
    entity_id: Mapped[str] = mapped_column(String(128), nullable=False)
    class_name: Mapped[str] = mapped_column(String(256), nullable=False)
    method_name: Mapped[str] = mapped_column(String(256), nullable=False)
    instruction_offset: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    source_location: Mapped[str] = mapped_column(String(512), nullable=False)
    rule_id: Mapped[str] = mapped_column(String(128), nullable=False)
    evidence_type: Mapped[str] = mapped_column(String(64), nullable=False, default="API_USAGE")
    confidence: Mapped[str] = mapped_column(String(32), nullable=False, default="HIGH")
    resolution_status: Mapped[str] = mapped_column(String(32), nullable=False, default="RESOLVED")
    provenance: Mapped[str] = mapped_column(String(512), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class BehaviorConflictModel(Base):
    __tablename__ = "behavior_conflicts"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scan_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False, index=True)
    conflict_id: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    conflict_type: Mapped[str] = mapped_column(String(128), nullable=False, default="CONTRADICTORY_CONFIGURATION")
    evidence_a: Mapped[str] = mapped_column(String(512), nullable=False)
    evidence_b: Mapped[str] = mapped_column(String(512), nullable=False)
    resolution_status: Mapped[str] = mapped_column(String(32), nullable=False, default="CONFLICTED")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class BehaviorSummaryModel(Base):
    __tablename__ = "behavior_summaries"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scan_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(256), nullable=False)
    summary_text: Mapped[str] = mapped_column(String(2048), nullable=False)
    findings_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class BehaviorGraphModel(Base):
    __tablename__ = "behavior_graphs"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scan_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False, index=True)
    nodes_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    edges_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class CorrelationRunModel(Base):
    __tablename__ = "correlation_runs"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scan_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False, index=True)
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="COMPLETED")
    duration_ms: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class CorrelationMetricModel(Base):
    __tablename__ = "correlation_metrics"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scan_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False, index=True)
    entities_processed: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    relationships_processed: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    findings_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    chains_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    conflicts_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class ThirdPartyBehaviorModel(Base):
    __tablename__ = "third_party_behaviors"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scan_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False, index=True)
    sdk_name: Mapped[str] = mapped_column(String(128), nullable=False)
    sdk_category: Mapped[str] = mapped_column(String(64), nullable=False, default="ANALYTICS")
    data_collected: Mapped[str] = mapped_column(String(256), nullable=False)
    network_endpoint: Mapped[str] = mapped_column(String(512), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
