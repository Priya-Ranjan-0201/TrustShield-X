"""SQLAlchemy 2.0 ORM Models for APK Metadata & Package Intelligence Engine (Phase 3.7 Part 1A.11).

Defines database models for apk_metadata_intel, apk_versions,
apk_sdk_profiles, apk_application_flags, and apk_resources_intel.
"""

import uuid
from datetime import datetime, timezone
from typing import Optional
from sqlalchemy import String, Integer, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from app.models.base import Base


class APKMetadataFullModel(Base):
    __tablename__ = "apk_metadata_intel"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scan_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False, index=True)
    package_name: Mapped[str] = mapped_column(String(256), nullable=False, index=True)
    app_label: Mapped[Optional[str]] = mapped_column(String(256), nullable=True)
    app_class: Mapped[Optional[str]] = mapped_column(String(512), nullable=True)
    version_name: Mapped[str] = mapped_column(String(64), nullable=False, default="1.0")
    version_code: Mapped[int] = mapped_column(Integer, nullable=False, default=1, index=True)
    target_sdk: Mapped[int] = mapped_column(Integer, nullable=False, default=33, index=True)
    min_sdk: Mapped[int] = mapped_column(Integer, nullable=False, default=21, index=True)
    compile_sdk: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    install_location: Mapped[str] = mapped_column(String(64), nullable=False, default="AUTO")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class APKVersionModel(Base):
    __tablename__ = "apk_versions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scan_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False, index=True)
    version_name: Mapped[str] = mapped_column(String(64), nullable=False)
    version_code: Mapped[int] = mapped_column(Integer, nullable=False)
    major: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    minor: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    patch: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    build: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class SDKProfileModel(Base):
    __tablename__ = "apk_sdk_profiles"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scan_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False, index=True)
    min_sdk: Mapped[int] = mapped_column(Integer, nullable=False, default=21)
    target_sdk: Mapped[int] = mapped_column(Integer, nullable=False, default=33)
    compile_sdk: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    max_sdk: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    platform_version: Mapped[str] = mapped_column(String(64), nullable=False)
    generation_name: Mapped[str] = mapped_column(String(128), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class ApplicationFlagsModel(Base):
    __tablename__ = "apk_application_flags"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scan_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False, index=True)
    is_debuggable: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    is_persistent: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    is_test_only: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    allow_backup: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    large_heap: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    uses_cleartext: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    supports_rtl: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class APKResourceModel(Base):
    __tablename__ = "apk_resources_intel"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scan_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False, index=True)
    icon_ref: Mapped[Optional[str]] = mapped_column(String(256), nullable=True)
    round_icon_ref: Mapped[Optional[str]] = mapped_column(String(256), nullable=True)
    banner_ref: Mapped[Optional[str]] = mapped_column(String(256), nullable=True)
    logo_ref: Mapped[Optional[str]] = mapped_column(String(256), nullable=True)
    theme_ref: Mapped[Optional[str]] = mapped_column(String(256), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
