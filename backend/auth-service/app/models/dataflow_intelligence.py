"""SQLAlchemy 2.0 ORM Models for Enterprise Dataflow & Information-Flow Intelligence Engine (Phase 3.9 Part 1A.21).

Defines database models for 16 dataflow tables:
dataflow_nodes, dataflow_edges, dataflow_paths, dataflow_sources, dataflow_sinks,
dataflow_taint_labels, dataflow_transformations, dataflow_evidence, dataflow_confidence,
information_flow_graphs, source_sink_graphs, flow_boundaries, third_party_dataflows,
jni_dataflows, reflection_dataflows, intent_dataflows.
"""

import uuid
from datetime import datetime, timezone
from typing import Optional, List
from sqlalchemy import String, Integer, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from app.models.base import Base


class DataflowNodeModel(Base):
    __tablename__ = "dataflow_nodes"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scan_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False, index=True)
    node_id: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    node_type: Mapped[str] = mapped_column(String(64), nullable=False, default="SOURCE")
    label: Mapped[str] = mapped_column(String(256), nullable=False)
    class_name: Mapped[str] = mapped_column(String(256), nullable=False)
    method_name: Mapped[str] = mapped_column(String(256), nullable=False)
    instruction_offset: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    data_category: Mapped[str] = mapped_column(String(64), nullable=False, default="IDENTITY")
    confidence: Mapped[str] = mapped_column(String(32), nullable=False, default="HIGH")
    resolution_status: Mapped[str] = mapped_column(String(32), nullable=False, default="RESOLVED")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class DataflowEdgeModel(Base):
    __tablename__ = "dataflow_edges"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scan_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False, index=True)
    source_node_id: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    target_node_id: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    edge_type: Mapped[str] = mapped_column(String(64), nullable=False, default="ASSIGN")
    caller_method: Mapped[str] = mapped_column(String(512), nullable=False)
    instruction_offset: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    confidence: Mapped[str] = mapped_column(String(32), nullable=False, default="HIGH")
    resolution_status: Mapped[str] = mapped_column(String(32), nullable=False, default="RESOLVED")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class DataflowSourceModel(Base):
    __tablename__ = "dataflow_sources"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scan_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False, index=True)
    source_id: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    source_type: Mapped[str] = mapped_column(String(64), nullable=False, default="LOCATION_API")
    data_category: Mapped[str] = mapped_column(String(64), nullable=False, default="LOCATION")
    api_canonical_id: Mapped[str] = mapped_column(String(512), nullable=False)
    source_class: Mapped[str] = mapped_column(String(256), nullable=False)
    source_method: Mapped[str] = mapped_column(String(256), nullable=False)
    confidence: Mapped[str] = mapped_column(String(32), nullable=False, default="HIGH")
    resolution_status: Mapped[str] = mapped_column(String(32), nullable=False, default="RESOLVED")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class DataflowSinkModel(Base):
    __tablename__ = "dataflow_sinks"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scan_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False, index=True)
    sink_id: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    sink_type: Mapped[str] = mapped_column(String(64), nullable=False, default="NETWORK_HTTP")
    target_identifier: Mapped[str] = mapped_column(String(512), nullable=False)
    sink_class: Mapped[str] = mapped_column(String(256), nullable=False)
    sink_method: Mapped[str] = mapped_column(String(256), nullable=False)
    confidence: Mapped[str] = mapped_column(String(32), nullable=False, default="HIGH")
    resolution_status: Mapped[str] = mapped_column(String(32), nullable=False, default="RESOLVED")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class DataflowPathModel(Base):
    __tablename__ = "dataflow_paths"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scan_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False, index=True)
    path_id: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    source_id: Mapped[str] = mapped_column(String(128), nullable=False)
    sink_id: Mapped[str] = mapped_column(String(128), nullable=False)
    flow_classification: Mapped[str] = mapped_column(String(64), nullable=False, default="SOURCE_TO_NETWORK")
    confidence: Mapped[str] = mapped_column(String(32), nullable=False, default="HIGH")
    resolution_status: Mapped[str] = mapped_column(String(32), nullable=False, default="RESOLVED")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class DataflowTaintLabelModel(Base):
    __tablename__ = "dataflow_taint_labels"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scan_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False, index=True)
    node_id: Mapped[str] = mapped_column(String(128), nullable=False)
    taint_label: Mapped[str] = mapped_column(String(64), nullable=False, default="TAINT_LOCATION", index=True)
    original_taint: Mapped[str] = mapped_column(String(64), nullable=False, default="LOCATION")
    is_sanitized: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class DataflowTransformationModel(Base):
    __tablename__ = "dataflow_transformations"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scan_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False, index=True)
    caller_method: Mapped[str] = mapped_column(String(512), nullable=False)
    transformation_type: Mapped[str] = mapped_column(String(64), nullable=False, default="SERIALIZATION")
    input_node_id: Mapped[str] = mapped_column(String(128), nullable=False)
    output_node_id: Mapped[str] = mapped_column(String(128), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class FlowBoundaryModel(Base):
    __tablename__ = "flow_boundaries"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scan_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False, index=True)
    boundary_type: Mapped[str] = mapped_column(String(64), nullable=False, default="CRYPTOGRAPHIC_BOUNDARY")
    source_method: Mapped[str] = mapped_column(String(512), nullable=False)
    target_method: Mapped[str] = mapped_column(String(512), nullable=False)
    resolution_status: Mapped[str] = mapped_column(String(32), nullable=False, default="RESOLVED")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class ThirdPartyDataflowModel(Base):
    __tablename__ = "third_party_dataflows"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scan_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False, index=True)
    source_id: Mapped[str] = mapped_column(String(128), nullable=False)
    sdk_name: Mapped[str] = mapped_column(String(128), nullable=False)
    sdk_category: Mapped[str] = mapped_column(String(64), nullable=False, default="ANALYTICS")
    target_endpoint: Mapped[str] = mapped_column(String(512), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class JNIDataflowModel(Base):
    __tablename__ = "jni_dataflows"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scan_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False, index=True)
    java_method: Mapped[str] = mapped_column(String(256), nullable=False)
    native_symbol: Mapped[str] = mapped_column(String(256), nullable=False)
    library_name: Mapped[str] = mapped_column(String(128), nullable=False)
    direction: Mapped[str] = mapped_column(String(32), nullable=False, default="JAVA_TO_NATIVE")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class ReflectionDataflowModel(Base):
    __tablename__ = "reflection_dataflows"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scan_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False, index=True)
    caller_method: Mapped[str] = mapped_column(String(512), nullable=False)
    reflection_target: Mapped[str] = mapped_column(String(512), nullable=False)
    resolution_status: Mapped[str] = mapped_column(String(32), nullable=False, default="RESOLVED")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class IntentDataflowModel(Base):
    __tablename__ = "intent_dataflows"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scan_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False, index=True)
    source_component: Mapped[str] = mapped_column(String(256), nullable=False)
    target_component: Mapped[str] = mapped_column(String(256), nullable=False)
    extra_key: Mapped[str] = mapped_column(String(128), nullable=False)
    extra_type: Mapped[str] = mapped_column(String(32), nullable=False, default="STRING")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class DataflowEvidenceModel(Base):
    __tablename__ = "dataflow_evidence"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scan_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False, index=True)
    dex_id: Mapped[str] = mapped_column(String(128), nullable=False)
    class_name: Mapped[str] = mapped_column(String(256), nullable=False)
    method_name: Mapped[str] = mapped_column(String(256), nullable=False)
    instruction_offset: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    evidence_type: Mapped[str] = mapped_column(String(64), nullable=False, default="SOURCE_TO_SINK_EDGE")
    raw_evidence: Mapped[str] = mapped_column(String(1024), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class DataflowConfidenceModel(Base):
    __tablename__ = "dataflow_confidence"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scan_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False, index=True)
    path_id: Mapped[str] = mapped_column(String(128), nullable=False)
    confidence_score: Mapped[float] = mapped_column(Float, nullable=False, default=0.95)
    confidence_level: Mapped[str] = mapped_column(String(32), nullable=False, default="HIGH")
    resolution_status: Mapped[str] = mapped_column(String(32), nullable=False, default="RESOLVED")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class InformationFlowGraphModel(Base):
    __tablename__ = "information_flow_graphs"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scan_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False, index=True)
    nodes_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    edges_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    sources_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    sinks_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class SourceSinkGraphModel(Base):
    __tablename__ = "source_sink_graphs"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scan_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False, index=True)
    source_node: Mapped[str] = mapped_column(String(128), nullable=False)
    sink_node: Mapped[str] = mapped_column(String(128), nullable=False)
    path_length: Mapped[int] = mapped_column(Integer, nullable=False, default=2)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
