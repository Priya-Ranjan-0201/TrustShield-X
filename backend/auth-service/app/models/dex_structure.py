"""SQLAlchemy 2.0 ORM Models for DEX Structure Intelligence Engine (Phase 3.7 Part 1A.13).

Defines database models for dex_packages, dex_classes, dex_methods,
dex_fields, dex_strings, dex_types, and dex_statistics.
"""

import uuid
from datetime import datetime, timezone
from typing import Optional, List
from sqlalchemy import String, Integer, Float, Boolean, DateTime, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from app.models.base import Base


class DEXPackageModel(Base):
    __tablename__ = "dex_packages"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scan_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False, index=True)
    package_name: Mapped[str] = mapped_column(String(256), nullable=False, index=True)
    parent_package: Mapped[Optional[str]] = mapped_column(String(256), nullable=True)
    depth: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    class_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    method_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class DEXClassModel(Base):
    __tablename__ = "dex_classes"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scan_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False, index=True)
    class_name: Mapped[str] = mapped_column(String(512), nullable=False, index=True)
    simple_name: Mapped[str] = mapped_column(String(256), nullable=False)
    package_name: Mapped[str] = mapped_column(String(256), nullable=False, index=True)
    superclass: Mapped[Optional[str]] = mapped_column(String(512), nullable=True)
    interfaces: Mapped[List[str]] = mapped_column(JSON, nullable=False, default=list)
    access_flags: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    is_abstract: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    is_final: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    is_inner: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    source_file: Mapped[Optional[str]] = mapped_column(String(256), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class DEXMethodModel(Base):
    __tablename__ = "dex_methods"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scan_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False, index=True)
    class_name: Mapped[str] = mapped_column(String(512), nullable=False, index=True)
    method_name: Mapped[str] = mapped_column(String(256), nullable=False, index=True)
    return_type: Mapped[str] = mapped_column(String(128), nullable=False, default="V")
    parameter_types: Mapped[List[str]] = mapped_column(JSON, nullable=False, default=list)
    access_flags: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    is_constructor: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    is_static: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    is_native: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    register_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    instruction_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class DEXFieldModel(Base):
    __tablename__ = "dex_fields"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scan_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False, index=True)
    class_name: Mapped[str] = mapped_column(String(512), nullable=False, index=True)
    field_name: Mapped[str] = mapped_column(String(256), nullable=False)
    field_type: Mapped[str] = mapped_column(String(128), nullable=False)
    access_flags: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    is_static: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    is_final: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class DEXStringModel(Base):
    __tablename__ = "dex_strings"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scan_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False, index=True)
    string_value: Mapped[str] = mapped_column(String(1024), nullable=False)
    string_hash: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    length: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    offset: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class DEXTypeModel(Base):
    __tablename__ = "dex_types"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scan_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False, index=True)
    type_name: Mapped[str] = mapped_column(String(512), nullable=False)
    kind: Mapped[str] = mapped_column(String(64), nullable=False, default="OBJECT")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class DEXStatisticsModel(Base):
    __tablename__ = "dex_statistics"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scan_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False, index=True)
    total_packages: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    total_classes: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    total_methods: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    total_fields: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    total_strings: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    avg_methods_per_class: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    largest_package: Mapped[Optional[str]] = mapped_column(String(256), nullable=True)
    largest_class: Mapped[Optional[str]] = mapped_column(String(512), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
