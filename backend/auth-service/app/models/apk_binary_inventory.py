"""SQLAlchemy 2.0 ORM Models for APK Binary Inventory Engine (Phase 3.7 Part 1A.12).

Defines database models for apk_binary_inventory, apk_binary_hashes,
and apk_binary_statistics.
"""

import uuid
from datetime import datetime, timezone
from typing import Optional
from sqlalchemy import String, Integer, Float, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from app.models.base import Base


class APKBinaryFileModel(Base):
    __tablename__ = "apk_binary_inventory"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scan_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False, index=True)
    file_path: Mapped[str] = mapped_column(String(512), nullable=False, index=True)
    filename: Mapped[str] = mapped_column(String(256), nullable=False)
    directory: Mapped[str] = mapped_column(String(512), nullable=False)
    extension: Mapped[str] = mapped_column(String(64), nullable=False)
    file_category: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    uncompressed_size: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    compressed_size: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    compression_method: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    crc32: Mapped[str] = mapped_column(String(16), nullable=False, default="00000000")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    hashes: Mapped[Optional["APKBinaryHashModel"]] = relationship("APKBinaryHashModel", back_populates="binary_file", uselist=False, cascade="all, delete-orphan", lazy="selectin")


class APKBinaryHashModel(Base):
    __tablename__ = "apk_binary_hashes"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    inventory_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("apk_binary_inventory.id", ondelete="CASCADE"), nullable=False, index=True)
    sha256: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    sha1: Mapped[str] = mapped_column(String(40), nullable=False)
    md5: Mapped[str] = mapped_column(String(32), nullable=False)
    crc32: Mapped[str] = mapped_column(String(16), nullable=False)
    entropy: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    mime_type: Mapped[str] = mapped_column(String(128), nullable=False, default="application/octet-stream")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    binary_file: Mapped["APKBinaryFileModel"] = relationship("APKBinaryFileModel", back_populates="hashes")


class APKBinaryStatisticsModel(Base):
    __tablename__ = "apk_binary_statistics"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scan_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False, index=True)
    total_files: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    total_directories: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    total_size_bytes: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    compressed_size_bytes: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    dex_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    native_library_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    assets_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    resources_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    media_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    config_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    unknown_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
