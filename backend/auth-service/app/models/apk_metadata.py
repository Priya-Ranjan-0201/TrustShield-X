"""SQLAlchemy 2.0 ORM Models for AI Android APK Security Engine (Phase 3.7 Part 1A Message 3A).

Defines database schemas for APK metadata, permissions, DEX inventory, native libraries, and certificates.
All relationships use lazy="selectin" for 100% async SQLAlchemy 2.0 compatibility.
"""

import uuid
from datetime import datetime, timezone
from typing import List, Optional
from sqlalchemy import String, Integer, BigInteger, Boolean, DateTime, ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID

from app.models.base import Base


class APKMetadataModel(Base):
    __tablename__ = "apk_metadata"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scan_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False, index=True)

    package_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True, index=True)
    version_name: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    version_code: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    application_label: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

    min_sdk: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    target_sdk: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    compile_sdk: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    apk_size: Mapped[int] = mapped_column(BigInteger, nullable=False, default=0)
    apk_sha256: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    parsed_successfully: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    # Relationships (lazy="selectin" for async SQLAlchemy compatibility)
    permissions: Mapped[List["APKPermissionModel"]] = relationship("APKPermissionModel", back_populates="apk_metadata", cascade="all, delete-orphan", lazy="selectin")
    dex_files: Mapped[List["APKDEXModel"]] = relationship("APKDEXModel", back_populates="apk_metadata", cascade="all, delete-orphan", lazy="selectin")
    native_libraries: Mapped[List["APKNativeLibraryModel"]] = relationship("APKNativeLibraryModel", back_populates="apk_metadata", cascade="all, delete-orphan", lazy="selectin")
    certificates: Mapped[List["APKCertificateModel"]] = relationship("APKCertificateModel", back_populates="apk_metadata", cascade="all, delete-orphan", lazy="selectin")

    __table_args__ = (
        Index("idx_apk_meta_scan_sha", "scan_id", "apk_sha256", unique=True),
    )


class APKPermissionModel(Base):
    __tablename__ = "apk_permissions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    apk_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("apk_metadata.id", ondelete="CASCADE"), nullable=False, index=True)

    permission_name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    protection_level: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    declared_by_app: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    apk_metadata: Mapped["APKMetadataModel"] = relationship("APKMetadataModel", back_populates="permissions")


class APKDEXModel(Base):
    __tablename__ = "apk_dex"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    apk_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("apk_metadata.id", ondelete="CASCADE"), nullable=False, index=True)

    filename: Mapped[str] = mapped_column(String(255), nullable=False)
    sha256: Mapped[str] = mapped_column(String(64), nullable=False)
    size: Mapped[int] = mapped_column(BigInteger, nullable=False, default=0)
    method_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    class_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    apk_metadata: Mapped["APKMetadataModel"] = relationship("APKMetadataModel", back_populates="dex_files")


class APKNativeLibraryModel(Base):
    __tablename__ = "apk_native_libraries"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    apk_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("apk_metadata.id", ondelete="CASCADE"), nullable=False, index=True)

    library_name: Mapped[str] = mapped_column(String(255), nullable=False)
    architecture: Mapped[str] = mapped_column(String(50), nullable=False)
    sha256: Mapped[str] = mapped_column(String(64), nullable=False)
    size: Mapped[int] = mapped_column(BigInteger, nullable=False, default=0)

    apk_metadata: Mapped["APKMetadataModel"] = relationship("APKMetadataModel", back_populates="native_libraries")


class APKCertificateModel(Base):
    __tablename__ = "apk_certificates"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    apk_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("apk_metadata.id", ondelete="CASCADE"), nullable=False, index=True)

    subject: Mapped[Optional[str]] = mapped_column(String(512), nullable=True)
    issuer: Mapped[Optional[str]] = mapped_column(String(512), nullable=True)
    sha256: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    sha1: Mapped[Optional[str]] = mapped_column(String(40), nullable=True)

    signature_algorithm: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    public_key_algorithm: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    key_size: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    valid_from: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    valid_until: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    expired: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    self_signed: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    apk_metadata: Mapped["APKMetadataModel"] = relationship("APKMetadataModel", back_populates="certificates")
