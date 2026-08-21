"""SQLAlchemy 2.0 ORM Models for Permission Intelligence Normalization Engine (Phase 3.7 Part 1A.8).

Defines database models for permission_catalog, apk_permission_intelligence,
permission_relationships, and permission_sdk_support.
"""

import uuid
from datetime import datetime, timezone
from typing import List, Optional
from sqlalchemy import String, Integer, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from app.models.base import Base


class PermissionCatalogModel(Base):
    __tablename__ = "permission_catalog"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    permission_name: Mapped[str] = mapped_column(String(256), nullable=False, unique=True, index=True)
    category: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    protection_level: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    permission_group: Mapped[Optional[str]] = mapped_column(String(256), nullable=True)
    api_introduced: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    api_deprecated: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    doc_url: Mapped[Optional[str]] = mapped_column(String(512), nullable=True)
    is_runtime: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    is_install: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class APKPermissionIntelligenceModel(Base):
    __tablename__ = "apk_permission_intelligence"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scan_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False, index=True)
    permission_name: Mapped[str] = mapped_column(String(256), nullable=False, index=True)
    category: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    protection_level: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    permission_group: Mapped[Optional[str]] = mapped_column(String(256), nullable=True)
    is_runtime: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False, index=True)
    is_dangerous: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    is_custom: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    is_vendor: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    is_unknown: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    target_sdk_supported: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class PermissionRelationshipModel(Base):
    __tablename__ = "permission_relationships"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    permission_name: Mapped[str] = mapped_column(String(256), nullable=False, index=True)
    related_permission_name: Mapped[str] = mapped_column(String(256), nullable=False)
    relationship_type: Mapped[str] = mapped_column(String(64), nullable=False)  # foreground_background, dependency, variant
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class PermissionSDKSupportModel(Base):
    __tablename__ = "permission_sdk_support"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    permission_name: Mapped[str] = mapped_column(String(256), nullable=False, index=True)
    min_sdk: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    max_sdk: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    status: Mapped[str] = mapped_column(String(64), nullable=False, default="SUPPORTED")  # SUPPORTED, DEPRECATED, IGNORED
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
