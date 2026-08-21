"""SQLAlchemy 2.0 ORM Models for Android Component Intelligence Engine (Phase 3.7 Part 1A.9).

Defines database models for component_catalog, apk_components_intel,
component_intent_filters, component_relationships, and component_processes.
"""

import uuid
from datetime import datetime, timezone
from typing import List, Optional
from sqlalchemy import String, Integer, Boolean, DateTime, ForeignKey, JSON, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from app.models.base import Base


class ComponentCatalogModel(Base):
    __tablename__ = "component_catalog"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    component_type: Mapped[str] = mapped_column(String(64), nullable=False, unique=True, index=True)
    android_purpose: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    lifecycle_type: Mapped[str] = mapped_column(String(64), nullable=False, default="UI_LIFECYCLE")
    default_exported_behavior: Mapped[str] = mapped_column(String(64), nullable=False, default="FALSE")
    supports_intent_filters: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    supports_permissions: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    doc_url: Mapped[Optional[str]] = mapped_column(String(512), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class APKComponentIntelligenceModel(Base):
    __tablename__ = "apk_components_intel"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scan_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False, index=True)
    component_name: Mapped[str] = mapped_column(String(512), nullable=False, index=True)
    component_type: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    exported_status: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    is_enabled: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    permission: Mapped[Optional[str]] = mapped_column(String(256), nullable=True, index=True)
    process_name: Mapped[str] = mapped_column(String(256), nullable=False, default="default", index=True)
    is_launcher: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    is_foreground: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    # Relationships
    intent_filters: Mapped[List["ComponentIntentFilterFullModel"]] = relationship(
        "ComponentIntentFilterFullModel", back_populates="component", cascade="all, delete-orphan", lazy="selectin"
    )


class ComponentIntentFilterFullModel(Base):
    __tablename__ = "component_intent_filters_full"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    component_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("apk_components_intel.id", ondelete="CASCADE"), nullable=False, index=True)
    actions: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    categories: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    schemes: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    hosts: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    ports: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    paths: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    mime_types: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    priority: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    auto_verify: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    is_deep_link: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    component: Mapped["APKComponentIntelligenceModel"] = relationship("APKComponentIntelligenceModel", back_populates="intent_filters")


class ComponentRelationshipModel(Base):
    __tablename__ = "component_relationships"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scan_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False, index=True)
    parent_component: Mapped[str] = mapped_column(String(512), nullable=False)
    child_component: Mapped[str] = mapped_column(String(512), nullable=False)
    relationship_type: Mapped[str] = mapped_column(String(64), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class ComponentProcessModel(Base):
    __tablename__ = "component_processes"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scan_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False, index=True)
    process_name: Mapped[str] = mapped_column(String(256), nullable=False, index=True)
    process_type: Mapped[str] = mapped_column(String(64), nullable=False, default="DEFAULT")
    component_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
