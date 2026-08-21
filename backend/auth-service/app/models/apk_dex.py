"""SQLAlchemy 2.0 ORM Models for DEX & Multi-DEX Intelligence Engine (Phase 3.7 Part 1A.6).

Defines database models for apk_dex_files, apk_dex_classes, apk_dex_methods, apk_dex_fields, and apk_packages.
"""

import uuid
from datetime import datetime, timezone
from typing import List, Optional
from sqlalchemy import String, Integer, Boolean, DateTime, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from app.models.base import Base


class APKDexFileModel(Base):
    __tablename__ = "apk_dex_files"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scan_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False, index=True)
    dex_name: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    dex_order: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    sha256: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    sha1: Mapped[str] = mapped_column(String(40), nullable=False)
    checksum: Mapped[str] = mapped_column(String(16), nullable=False)
    checksum_valid: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    file_size: Mapped[int] = mapped_column(Integer, nullable=False)
    header_size: Mapped[int] = mapped_column(Integer, nullable=False, default=112)
    endian_tag: Mapped[str] = mapped_column(String(32), nullable=False, default="0x12345678")
    string_ids_size: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    type_ids_size: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    proto_ids_size: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    field_ids_size: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    method_ids_size: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    class_defs_size: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    # Relationship
    classes: Mapped[List["APKDexClassModel"]] = relationship(
        "APKDexClassModel", back_populates="dex_file", cascade="all, delete-orphan", lazy="selectin"
    )


class APKDexClassModel(Base):
    __tablename__ = "apk_dex_classes"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    dex_file_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("apk_dex_files.id", ondelete="CASCADE"), nullable=False, index=True)
    class_name: Mapped[str] = mapped_column(String(512), nullable=False, index=True)
    package_name: Mapped[str] = mapped_column(String(256), nullable=False, index=True)
    superclass: Mapped[Optional[str]] = mapped_column(String(512), nullable=True)
    access_flags: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    is_interface: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    is_enum: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    is_abstract: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    source_file: Mapped[Optional[str]] = mapped_column(String(256), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    # Relationships
    dex_file: Mapped["APKDexFileModel"] = relationship("APKDexFileModel", back_populates="classes")
    methods: Mapped[List["APKDexMethodModel"]] = relationship(
        "APKDexMethodModel", back_populates="dex_class", cascade="all, delete-orphan", lazy="selectin"
    )
    fields: Mapped[List["APKDexFieldModel"]] = relationship(
        "APKDexFieldModel", back_populates="dex_class", cascade="all, delete-orphan", lazy="selectin"
    )


class APKDexMethodModel(Base):
    __tablename__ = "apk_dex_methods"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    class_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("apk_dex_classes.id", ondelete="CASCADE"), nullable=False, index=True)
    method_name: Mapped[str] = mapped_column(String(256), nullable=False, index=True)
    return_type: Mapped[str] = mapped_column(String(256), nullable=False, default="V")
    parameter_types: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    access_flags: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    is_direct: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    is_virtual: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    is_native: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    is_constructor: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    # Relationship
    dex_class: Mapped["APKDexClassModel"] = relationship("APKDexClassModel", back_populates="methods")


class APKDexFieldModel(Base):
    __tablename__ = "apk_dex_fields"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    class_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("apk_dex_classes.id", ondelete="CASCADE"), nullable=False, index=True)
    field_name: Mapped[str] = mapped_column(String(256), nullable=False)
    field_type: Mapped[str] = mapped_column(String(256), nullable=False)
    access_flags: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    is_static: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    is_final: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    # Relationship
    dex_class: Mapped["APKDexClassModel"] = relationship("APKDexClassModel", back_populates="fields")


class APKPackageModel(Base):
    __tablename__ = "apk_packages"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scan_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False, index=True)
    package_name: Mapped[str] = mapped_column(String(256), nullable=False, index=True)
    class_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    depth: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
