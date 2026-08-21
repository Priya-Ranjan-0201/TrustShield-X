"""SQLAlchemy 2.0 ORM Models for Enterprise Sensitive Android API Intelligence Engine (Phase 3.7 Part 1A.16).

Defines database models for api_catalog, api_capabilities, api_usage,
api_frameworks, api_statistics, api_cross_reference, library_inventory,
and framework_inventory.
"""

import uuid
from datetime import datetime, timezone
from typing import Optional, List
from sqlalchemy import String, Integer, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from app.models.base import Base


class APIModel(Base):
    __tablename__ = "api_catalog"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scan_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False, index=True)
    canonical_id: Mapped[str] = mapped_column(String(512), nullable=False, index=True)
    package_name: Mapped[str] = mapped_column(String(256), nullable=False)
    class_name: Mapped[str] = mapped_column(String(256), nullable=False)
    method_name: Mapped[str] = mapped_column(String(256), nullable=False)
    signature: Mapped[str] = mapped_column(String(512), nullable=False)
    framework: Mapped[str] = mapped_column(String(128), nullable=False, default="ANDROID_SDK")
    min_sdk: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    deprecated: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class APICapabilityModel(Base):
    __tablename__ = "api_capabilities"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scan_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False, index=True)
    api_canonical_id: Mapped[str] = mapped_column(String(512), nullable=False, index=True)
    capability: Mapped[str] = mapped_column(String(64), nullable=False, default="OTHERS", index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class APIUsageModel(Base):
    __tablename__ = "api_usage"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scan_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False, index=True)
    caller_method: Mapped[str] = mapped_column(String(512), nullable=False, index=True)
    api_canonical_id: Mapped[str] = mapped_column(String(512), nullable=False, index=True)
    offset: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class APIFrameworkModel(Base):
    __tablename__ = "api_frameworks"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scan_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False, index=True)
    framework_name: Mapped[str] = mapped_column(String(128), nullable=False)
    version: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    detected_by: Mapped[str] = mapped_column(String(128), nullable=False, default="PACKAGE_PREFIX")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class APIStatisticModel(Base):
    __tablename__ = "api_statistics"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scan_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False, index=True)
    total_apis: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    unique_frameworks: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    most_used_capability: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class APICrossRefModel(Base):
    __tablename__ = "api_cross_reference"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scan_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False, index=True)
    source_symbol: Mapped[str] = mapped_column(String(512), nullable=False)
    api_canonical_id: Mapped[str] = mapped_column(String(512), nullable=False)
    xref_type: Mapped[str] = mapped_column(String(64), nullable=False, default="INVOKE")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class LibraryInventoryModel(Base):
    __tablename__ = "library_inventory"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scan_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False, index=True)
    library_name: Mapped[str] = mapped_column(String(256), nullable=False)
    version: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    package_prefix: Mapped[str] = mapped_column(String(256), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class FrameworkInventoryModel(Base):
    __tablename__ = "framework_inventory"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scan_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False, index=True)
    framework_name: Mapped[str] = mapped_column(String(256), nullable=False)
    version: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    confidence: Mapped[float] = mapped_column(Float, nullable=False, default=1.0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
