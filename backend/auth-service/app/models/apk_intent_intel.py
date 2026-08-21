"""SQLAlchemy 2.0 ORM Models for Intent & Deep Link Intelligence Engine (Phase 3.7 Part 1A.10).

Defines database models for intent_catalog, apk_intents, apk_intent_actions,
apk_intent_categories, apk_deep_links, and navigation_graph.
"""

import uuid
from datetime import datetime, timezone
from typing import List, Optional
from sqlalchemy import String, Integer, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from app.models.base import Base


class IntentCatalogModel(Base):
    __tablename__ = "intent_catalog"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    action_name: Mapped[str] = mapped_column(String(256), nullable=False, unique=True, index=True)
    category: Mapped[str] = mapped_column(String(64), nullable=False, default="SYSTEM_BROADCAST")
    purpose: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    is_system_only: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    api_introduced: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    doc_url: Mapped[Optional[str]] = mapped_column(String(512), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class APKIntentModel(Base):
    __tablename__ = "apk_intents"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scan_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False, index=True)
    component_name: Mapped[str] = mapped_column(String(512), nullable=False, index=True)
    priority: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    auto_verify: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    is_exported: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    actions: Mapped[List["IntentActionModel"]] = relationship("IntentActionModel", back_populates="intent", cascade="all, delete-orphan", lazy="selectin")
    categories: Mapped[List["IntentCategoryModel"]] = relationship("IntentCategoryModel", back_populates="intent", cascade="all, delete-orphan", lazy="selectin")
    deep_links: Mapped[List["DeepLinkModel"]] = relationship("DeepLinkModel", back_populates="intent", cascade="all, delete-orphan", lazy="selectin")


class IntentActionModel(Base):
    __tablename__ = "apk_intent_actions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    intent_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("apk_intents.id", ondelete="CASCADE"), nullable=False, index=True)
    action_name: Mapped[str] = mapped_column(String(256), nullable=False, index=True)
    action_type: Mapped[str] = mapped_column(String(64), nullable=False, default="CUSTOM")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    intent: Mapped["APKIntentModel"] = relationship("APKIntentModel", back_populates="actions")


class IntentCategoryModel(Base):
    __tablename__ = "apk_intent_categories"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    intent_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("apk_intents.id", ondelete="CASCADE"), nullable=False, index=True)
    category_name: Mapped[str] = mapped_column(String(256), nullable=False, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    intent: Mapped["APKIntentModel"] = relationship("APKIntentModel", back_populates="categories")


class DeepLinkModel(Base):
    __tablename__ = "apk_deep_links"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    intent_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("apk_intents.id", ondelete="CASCADE"), nullable=False, index=True)
    scheme: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    host: Mapped[Optional[str]] = mapped_column(String(256), nullable=True, index=True)
    port: Mapped[Optional[str]] = mapped_column(String(32), nullable=True)
    path: Mapped[Optional[str]] = mapped_column(String(512), nullable=True)
    mime_type: Mapped[Optional[str]] = mapped_column(String(128), nullable=True)
    is_app_link: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    is_browsable: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    intent: Mapped["APKIntentModel"] = relationship("APKIntentModel", back_populates="deep_links")


class NavigationGraphModel(Base):
    __tablename__ = "navigation_graph"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scan_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False, index=True)
    source_component: Mapped[str] = mapped_column(String(512), nullable=False)
    intent_action: Mapped[str] = mapped_column(String(256), nullable=False, index=True)
    target_scheme: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    target_host: Mapped[Optional[str]] = mapped_column(String(256), nullable=True)
    destination_component: Mapped[str] = mapped_column(String(512), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
