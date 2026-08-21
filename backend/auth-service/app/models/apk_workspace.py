"""SQLAlchemy 2.0 ORM Models for APK Workspace Extraction Layer (Phase 3.7 Part 1A.4).

Defines database models for apk_workspace, workspace_files, and workspace_statistics.
"""

import uuid
from datetime import datetime, timezone
from typing import List, Optional
from sqlalchemy import String, Integer, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from app.models.base import Base


class WorkspaceModel(Base):
    __tablename__ = "apk_workspace"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    workspace_id: Mapped[str] = mapped_column(String(64), unique=True, nullable=False, index=True)
    scan_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False, index=True)
    apk_sha256: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    workspace_path: Mapped[str] = mapped_column(String(512), nullable=False)
    status: Mapped[str] = mapped_column(String(64), nullable=False, default="READY_FOR_STATIC_ANALYSIS")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    deleted_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    # Relationships
    files: Mapped[List["WorkspaceFileModel"]] = relationship(
        "WorkspaceFileModel", back_populates="workspace", cascade="all, delete-orphan", lazy="selectin"
    )
    statistics: Mapped[Optional["WorkspaceStatisticsModel"]] = relationship(
        "WorkspaceStatisticsModel", back_populates="workspace", uselist=False, cascade="all, delete-orphan", lazy="selectin"
    )


class WorkspaceFileModel(Base):
    __tablename__ = "workspace_files"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    workspace_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("apk_workspace.id", ondelete="CASCADE"), nullable=False, index=True)
    relative_path: Mapped[str] = mapped_column(String(512), nullable=False)
    mime_type: Mapped[str] = mapped_column(String(128), nullable=False)
    sha256: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    size: Mapped[int] = mapped_column(Integer, nullable=False)
    entropy: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    category: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    # Relationship
    workspace: Mapped["WorkspaceModel"] = relationship("WorkspaceModel", back_populates="files")


class WorkspaceStatisticsModel(Base):
    __tablename__ = "workspace_statistics"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    workspace_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("apk_workspace.id", ondelete="CASCADE"), nullable=False, index=True)
    file_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    directory_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    dex_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    library_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    asset_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    resource_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    binary_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    xml_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    certificate_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    # Relationship
    workspace: Mapped["WorkspaceModel"] = relationship("WorkspaceModel", back_populates="statistics")
