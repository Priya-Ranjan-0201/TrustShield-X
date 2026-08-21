"""SQLAlchemy 2.0 ORM Models for Enterprise Reflection & Dynamic Code Loading Intelligence Engine (Phase 3.7 Part 1A.17).

Defines database models for reflection_calls, reflection_targets,
dynamic_class_loading, native_loading, jni_registration, hidden_api_usage,
reflection_graph, and dynamic_invocations.
"""

import uuid
from datetime import datetime, timezone
from typing import Optional, List
from sqlalchemy import String, Integer, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from app.models.base import Base


class ReflectionCallModel(Base):
    __tablename__ = "reflection_calls"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scan_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False, index=True)
    caller_method: Mapped[str] = mapped_column(String(512), nullable=False, index=True)
    reflection_api: Mapped[str] = mapped_column(String(256), nullable=False)
    target_class: Mapped[Optional[str]] = mapped_column(String(256), nullable=True, index=True)
    target_member: Mapped[Optional[str]] = mapped_column(String(256), nullable=True)
    offset: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class ReflectionTargetModel(Base):
    __tablename__ = "reflection_targets"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scan_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False, index=True)
    canonical_target: Mapped[str] = mapped_column(String(512), nullable=False)
    target_type: Mapped[str] = mapped_column(String(64), nullable=False, default="CLASS")
    is_resolved: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class DynamicClassModel(Base):
    __tablename__ = "dynamic_class_loading"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scan_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False, index=True)
    caller_method: Mapped[str] = mapped_column(String(512), nullable=False)
    loader_type: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    dex_path: Mapped[Optional[str]] = mapped_column(String(512), nullable=True)
    is_memory_only: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class NativeLibraryModel(Base):
    __tablename__ = "native_loading"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scan_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False, index=True)
    caller_method: Mapped[str] = mapped_column(String(512), nullable=False)
    library_name: Mapped[str] = mapped_column(String(256), nullable=False)
    load_api: Mapped[str] = mapped_column(String(128), nullable=False, default="System.loadLibrary")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class JNIBindingModel(Base):
    __tablename__ = "jni_registration"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scan_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False, index=True)
    native_method: Mapped[str] = mapped_column(String(256), nullable=False)
    java_class: Mapped[str] = mapped_column(String(256), nullable=False)
    symbol_name: Mapped[str] = mapped_column(String(256), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class HiddenAPIModel(Base):
    __tablename__ = "hidden_api_usage"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scan_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False, index=True)
    api_signature: Mapped[str] = mapped_column(String(512), nullable=False)
    access_mechanism: Mapped[str] = mapped_column(String(64), nullable=False, default="REFLECTION")
    restriction_level: Mapped[str] = mapped_column(String(64), nullable=False, default="GREYLIST")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class ReflectionGraphModel(Base):
    __tablename__ = "reflection_graph"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scan_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False, index=True)
    caller_method: Mapped[str] = mapped_column(String(512), nullable=False)
    target_symbol: Mapped[str] = mapped_column(String(512), nullable=False)
    invocation_type: Mapped[str] = mapped_column(String(64), nullable=False, default="REFLECTIVE_INVOKE")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class DynamicInvocationModel(Base):
    __tablename__ = "dynamic_invocations"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scan_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False, index=True)
    source_symbol: Mapped[str] = mapped_column(String(512), nullable=False)
    resolved_target: Mapped[str] = mapped_column(String(512), nullable=False)
    confidence: Mapped[float] = mapped_column(Float, nullable=False, default=1.0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
