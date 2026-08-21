"""SQLAlchemy 2.0 ORM Models for Program Graph Intelligence Engine (Phase 3.7 Part 1A.15).

Defines database models for cfg_nodes, cfg_edges, call_graph_nodes,
call_graph_edges, method_xrefs, loop_analysis, dominators, execution_paths,
scc_analysis, and graph_metrics.
"""

import uuid
from datetime import datetime, timezone
from typing import Optional, List
from sqlalchemy import String, Integer, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from app.models.base import Base


class CFGNodeModel(Base):
    __tablename__ = "cfg_nodes"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scan_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False, index=True)
    method_name: Mapped[str] = mapped_column(String(512), nullable=False, index=True)
    block_id: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    start_offset: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    end_offset: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    instruction_count: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    is_entry: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    is_exit: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    is_loop_header: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class CFGEdgeModel(Base):
    __tablename__ = "cfg_edges"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scan_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False, index=True)
    method_name: Mapped[str] = mapped_column(String(512), nullable=False, index=True)
    source_block_id: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    target_block_id: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    edge_type: Mapped[str] = mapped_column(String(64), nullable=False, default="FALLTHROUGH")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class CallGraphNodeModel(Base):
    __tablename__ = "call_graph_nodes"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scan_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False, index=True)
    method_name: Mapped[str] = mapped_column(String(512), nullable=False, index=True)
    class_name: Mapped[str] = mapped_column(String(512), nullable=False)
    is_reachable: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    in_degree: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    out_degree: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class CallGraphEdgeModel(Base):
    __tablename__ = "call_graph_edges"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scan_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False, index=True)
    caller_method: Mapped[str] = mapped_column(String(512), nullable=False, index=True)
    callee_method: Mapped[str] = mapped_column(String(512), nullable=False, index=True)
    invoke_type: Mapped[str] = mapped_column(String(64), nullable=False, default="INVOKE_VIRTUAL")
    offset: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class MethodXRefModel(Base):
    __tablename__ = "method_xrefs"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scan_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False, index=True)
    source_symbol: Mapped[str] = mapped_column(String(512), nullable=False)
    target_symbol: Mapped[str] = mapped_column(String(512), nullable=False)
    xref_type: Mapped[str] = mapped_column(String(64), nullable=False, default="CALL")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class LoopAnalysisModel(Base):
    __tablename__ = "loop_analysis"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scan_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False, index=True)
    method_name: Mapped[str] = mapped_column(String(512), nullable=False, index=True)
    header_block_id: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    loop_depth: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class DominatorModel(Base):
    __tablename__ = "dominators"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scan_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False, index=True)
    method_name: Mapped[str] = mapped_column(String(512), nullable=False, index=True)
    block_id: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    idom_block_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    depth: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class ExecutionPathModel(Base):
    __tablename__ = "execution_paths"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scan_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False, index=True)
    method_name: Mapped[str] = mapped_column(String(512), nullable=False, index=True)
    path_length: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    branch_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    exit_type: Mapped[str] = mapped_column(String(64), nullable=False, default="RETURN")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class SCCModel(Base):
    __tablename__ = "scc_analysis"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scan_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False, index=True)
    scc_id: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    node_count: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    is_recursive: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class GraphMetricModel(Base):
    __tablename__ = "graph_metrics"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scan_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False, index=True)
    cfg_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    call_graph_nodes_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    call_graph_edges_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    cyclomatic_complexity: Mapped[float] = mapped_column(Float, nullable=False, default=1.0)
    reachable_methods_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    reachability_percentage: Mapped[float] = mapped_column(Float, nullable=False, default=100.0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
