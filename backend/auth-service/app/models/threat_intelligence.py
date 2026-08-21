"""SQLAlchemy 2.0 ORM Models for Enterprise Threat Intelligence Engine (Phase 3.9 Part 1A.23).

Defines database models for 17 threat intelligence tables:
threat_indicators, threat_sources, threat_feeds, threat_feed_records, threat_matches,
threat_relationships, threat_entities, threat_conflicts, threat_evidence, threat_behavior_correlations,
threat_dataflow_correlations, threat_sync_runs, threat_sync_metrics, threat_graphs, yara_matches,
stix_objects, taxii_collections.
"""

import uuid
from datetime import datetime, timezone
from typing import Optional, List
from sqlalchemy import String, Integer, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from app.models.base import Base


class ThreatIndicatorModel(Base):
    __tablename__ = "threat_indicators"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scan_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False, index=True)
    indicator_id: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    indicator_type: Mapped[str] = mapped_column(String(64), nullable=False, default="DOMAIN")
    normalized_value: Mapped[str] = mapped_column(String(512), nullable=False, index=True)
    display_value: Mapped[str] = mapped_column(String(512), nullable=False)
    value_hash: Mapped[str] = mapped_column(String(128), nullable=False)
    source_module: Mapped[str] = mapped_column(String(128), nullable=False)
    source_location: Mapped[str] = mapped_column(String(512), nullable=False)
    resolution_status: Mapped[str] = mapped_column(String(32), nullable=False, default="RESOLVED")
    confidence: Mapped[str] = mapped_column(String(32), nullable=False, default="HIGH")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class ThreatSourceModel(Base):
    __tablename__ = "threat_sources"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scan_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False, index=True)
    source_id: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    provider: Mapped[str] = mapped_column(String(256), nullable=False)
    source_type: Mapped[str] = mapped_column(String(64), nullable=False, default="OFFLINE_FEED")
    reliability: Mapped[str] = mapped_column(String(32), nullable=False, default="HIGH")
    version: Mapped[str] = mapped_column(String(64), nullable=False, default="1.0")
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="ACTIVE")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class ThreatFeedModel(Base):
    __tablename__ = "threat_feeds"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scan_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False, index=True)
    feed_id: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    feed_name: Mapped[str] = mapped_column(String(256), nullable=False)
    provider: Mapped[str] = mapped_column(String(256), nullable=False)
    version: Mapped[str] = mapped_column(String(64), nullable=False, default="1.0.0")
    record_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    freshness_state: Mapped[str] = mapped_column(String(32), nullable=False, default="CURRENT")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class ThreatFeedRecordModel(Base):
    __tablename__ = "threat_feed_records"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scan_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False, index=True)
    feed_id: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    indicator_value: Mapped[str] = mapped_column(String(512), nullable=False)
    reputation: Mapped[str] = mapped_column(String(64), nullable=False, default="SUSPICIOUS")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class ThreatMatchModel(Base):
    __tablename__ = "threat_matches"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scan_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False, index=True)
    match_id: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    indicator_id: Mapped[str] = mapped_column(String(128), nullable=False)
    source_id: Mapped[str] = mapped_column(String(128), nullable=False)
    match_type: Mapped[str] = mapped_column(String(64), nullable=False, default="EXACT_MATCH")
    reputation: Mapped[str] = mapped_column(String(64), nullable=False, default="SUSPICIOUS_REPORTED")
    confidence: Mapped[str] = mapped_column(String(32), nullable=False, default="HIGH")
    freshness_state: Mapped[str] = mapped_column(String(32), nullable=False, default="CURRENT")
    provenance: Mapped[str] = mapped_column(String(512), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class ThreatRelationshipModel(Base):
    __tablename__ = "threat_relationships"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scan_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False, index=True)
    source_entity_id: Mapped[str] = mapped_column(String(128), nullable=False)
    target_entity_id: Mapped[str] = mapped_column(String(128), nullable=False)
    relationship: Mapped[str] = mapped_column(String(64), nullable=False, default="ASSOCIATED_WITH")
    confidence: Mapped[str] = mapped_column(String(32), nullable=False, default="HIGH")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class ThreatEntityModel(Base):
    __tablename__ = "threat_entities"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scan_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False, index=True)
    entity_id: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    entity_type: Mapped[str] = mapped_column(String(64), nullable=False, default="INDICATOR")
    name: Mapped[str] = mapped_column(String(256), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class ThreatConflictModel(Base):
    __tablename__ = "threat_conflicts"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scan_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False, index=True)
    conflict_id: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    indicator_value: Mapped[str] = mapped_column(String(512), nullable=False)
    source_a_claim: Mapped[str] = mapped_column(String(256), nullable=False)
    source_b_claim: Mapped[str] = mapped_column(String(256), nullable=False)
    resolution_status: Mapped[str] = mapped_column(String(32), nullable=False, default="CONFLICTED")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class ThreatEvidenceModel(Base):
    __tablename__ = "threat_evidence"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scan_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False, index=True)
    evidence_id: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    indicator_id: Mapped[str] = mapped_column(String(128), nullable=False)
    matched_rule_or_feed: Mapped[str] = mapped_column(String(256), nullable=False)
    provenance: Mapped[str] = mapped_column(String(512), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class ThreatBehaviorCorrelationModel(Base):
    __tablename__ = "threat_behavior_correlations"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scan_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False, index=True)
    correlation_id: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    behavior_type: Mapped[str] = mapped_column(String(128), nullable=False)
    indicator_value: Mapped[str] = mapped_column(String(512), nullable=False)
    threat_claim: Mapped[str] = mapped_column(String(256), nullable=False)
    confidence: Mapped[str] = mapped_column(String(32), nullable=False, default="HIGH")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class ThreatDataflowCorrelationModel(Base):
    __tablename__ = "threat_dataflow_correlations"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scan_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False, index=True)
    correlation_id: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    dataflow_path_id: Mapped[str] = mapped_column(String(128), nullable=False)
    endpoint_url: Mapped[str] = mapped_column(String(512), nullable=False)
    threat_claim: Mapped[str] = mapped_column(String(256), nullable=False)
    confidence: Mapped[str] = mapped_column(String(32), nullable=False, default="HIGH")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class ThreatSyncRunModel(Base):
    __tablename__ = "threat_sync_runs"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scan_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False, index=True)
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="COMPLETED")
    duration_ms: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class ThreatSyncMetricModel(Base):
    __tablename__ = "threat_sync_metrics"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scan_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False, index=True)
    indicators_processed: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    matches_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    conflicts_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    expired_indicators_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class ThreatGraphModel(Base):
    __tablename__ = "threat_graphs"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scan_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False, index=True)
    nodes_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    edges_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class YaraMatchModel(Base):
    __tablename__ = "yara_matches"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scan_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False, index=True)
    rule_name: Mapped[str] = mapped_column(String(128), nullable=False)
    rule_namespace: Mapped[str] = mapped_column(String(128), nullable=False, default="default")
    matched_file: Mapped[str] = mapped_column(String(256), nullable=False)
    offset: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    match_confidence: Mapped[str] = mapped_column(String(32), nullable=False, default="HIGH")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class StixObjectModel(Base):
    __tablename__ = "stix_objects"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scan_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False, index=True)
    object_id: Mapped[str] = mapped_column(String(128), nullable=False)
    object_type: Mapped[str] = mapped_column(String(64), nullable=False, default="indicator")
    name: Mapped[str] = mapped_column(String(256), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class TaxiiCollectionModel(Base):
    __tablename__ = "taxii_collections"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scan_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False, index=True)
    collection_id: Mapped[str] = mapped_column(String(128), nullable=False)
    title: Mapped[str] = mapped_column(String(256), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
