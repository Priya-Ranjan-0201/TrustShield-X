"""SQLAlchemy 2.0 ORM Models for AndroidManifest Intelligence Engine (Phase 3.7 Part 1A.5 & Part 1A.7).

Defines database models for apk_manifest, apk_components, apk_intent_filters, apk_features,
apk_libraries, apk_permissions, apk_activities, apk_services, apk_receivers, apk_providers, and apk_queries.
"""

import uuid
from datetime import datetime, timezone
from typing import List, Optional
from sqlalchemy import String, Integer, Boolean, DateTime, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from app.models.base import Base


class APKManifestModel(Base):
    __tablename__ = "apk_manifest"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scan_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False, index=True)
    package_name: Mapped[str] = mapped_column(String(256), nullable=False, index=True)
    version_name: Mapped[Optional[str]] = mapped_column(String(128), nullable=True)
    version_code: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    min_sdk: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    target_sdk: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    compile_sdk: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    sdk_category: Mapped[str] = mapped_column(String(32), nullable=False, default="UNKNOWN")
    shared_user_id: Mapped[Optional[str]] = mapped_column(String(128), nullable=True)
    application_label: Mapped[Optional[str]] = mapped_column(String(256), nullable=True)
    debuggable: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    allow_backup: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    uses_cleartext_traffic: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    # Relationships
    components: Mapped[List["APKComponentModel"]] = relationship(
        "APKComponentModel", back_populates="manifest", cascade="all, delete-orphan", lazy="selectin"
    )
    features: Mapped[List["APKFeatureModel"]] = relationship(
        "APKFeatureModel", back_populates="manifest", cascade="all, delete-orphan", lazy="selectin"
    )
    libraries: Mapped[List["APKLibraryModel"]] = relationship(
        "APKLibraryModel", back_populates="manifest", cascade="all, delete-orphan", lazy="selectin"
    )
    permissions: Mapped[List["APKPermissionFullModel"]] = relationship(
        "APKPermissionFullModel", back_populates="manifest", cascade="all, delete-orphan", lazy="selectin"
    )
    activities: Mapped[List["APKActivityModel"]] = relationship(
        "APKActivityModel", back_populates="manifest", cascade="all, delete-orphan", lazy="selectin"
    )
    services: Mapped[List["APKServiceModel"]] = relationship(
        "APKServiceModel", back_populates="manifest", cascade="all, delete-orphan", lazy="selectin"
    )
    receivers: Mapped[List["APKReceiverModel"]] = relationship(
        "APKReceiverModel", back_populates="manifest", cascade="all, delete-orphan", lazy="selectin"
    )
    providers: Mapped[List["APKProviderModel"]] = relationship(
        "APKProviderModel", back_populates="manifest", cascade="all, delete-orphan", lazy="selectin"
    )
    queries: Mapped[List["APKQueryModel"]] = relationship(
        "APKQueryModel", back_populates="manifest", cascade="all, delete-orphan", lazy="selectin"
    )


class APKComponentModel(Base):
    __tablename__ = "apk_components"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    manifest_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("apk_manifest.id", ondelete="CASCADE"), nullable=False, index=True)
    component_name: Mapped[str] = mapped_column(String(512), nullable=False, index=True)
    component_type: Mapped[str] = mapped_column(String(32), nullable=False)
    exported: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)
    enabled: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    permission: Mapped[Optional[str]] = mapped_column(String(256), nullable=True, index=True)
    process: Mapped[Optional[str]] = mapped_column(String(128), nullable=True)
    launch_mode: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    authorities: Mapped[Optional[str]] = mapped_column(String(512), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    manifest: Mapped["APKManifestModel"] = relationship("APKManifestModel", back_populates="components")
    intent_filters: Mapped[List["APKIntentFilterModel"]] = relationship(
        "APKIntentFilterModel", back_populates="component", cascade="all, delete-orphan", lazy="selectin"
    )


class APKIntentFilterModel(Base):
    __tablename__ = "apk_intent_filters"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    component_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("apk_components.id", ondelete="CASCADE"), nullable=False, index=True)
    actions: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    categories: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    schemes: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    hosts: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    mime_types: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    priority: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    component: Mapped["APKComponentModel"] = relationship("APKComponentModel", back_populates="intent_filters")


class APKFeatureModel(Base):
    __tablename__ = "apk_features"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    manifest_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("apk_manifest.id", ondelete="CASCADE"), nullable=False, index=True)
    feature_name: Mapped[str] = mapped_column(String(256), nullable=False)
    required: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    gl_version: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    manifest: Mapped["APKManifestModel"] = relationship("APKManifestModel", back_populates="features")


class APKLibraryModel(Base):
    __tablename__ = "apk_libraries"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    manifest_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("apk_manifest.id", ondelete="CASCADE"), nullable=False, index=True)
    library_name: Mapped[str] = mapped_column(String(256), nullable=False)
    required: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    manifest: Mapped["APKManifestModel"] = relationship("APKManifestModel", back_populates="libraries")


class APKPermissionFullModel(Base):
    __tablename__ = "apk_manifest_permissions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    manifest_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("apk_manifest.id", ondelete="CASCADE"), nullable=False, index=True)
    permission_name: Mapped[str] = mapped_column(String(256), nullable=False, index=True)
    protection_level: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    declared: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    requested: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    is_custom: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    manifest: Mapped["APKManifestModel"] = relationship("APKManifestModel", back_populates="permissions")


class APKActivityModel(Base):
    __tablename__ = "apk_activities"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    manifest_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("apk_manifest.id", ondelete="CASCADE"), nullable=False, index=True)
    activity_name: Mapped[str] = mapped_column(String(512), nullable=False, index=True)
    exported: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)
    enabled: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    permission: Mapped[Optional[str]] = mapped_column(String(256), nullable=True)
    launch_mode: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    task_affinity: Mapped[Optional[str]] = mapped_column(String(256), nullable=True)
    theme: Mapped[Optional[str]] = mapped_column(String(256), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    manifest: Mapped["APKManifestModel"] = relationship("APKManifestModel", back_populates="activities")


class APKServiceModel(Base):
    __tablename__ = "apk_services"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    manifest_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("apk_manifest.id", ondelete="CASCADE"), nullable=False, index=True)
    service_name: Mapped[str] = mapped_column(String(512), nullable=False, index=True)
    exported: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)
    enabled: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    permission: Mapped[Optional[str]] = mapped_column(String(256), nullable=True)
    foreground_service_type: Mapped[Optional[str]] = mapped_column(String(128), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    manifest: Mapped["APKManifestModel"] = relationship("APKManifestModel", back_populates="services")


class APKReceiverModel(Base):
    __tablename__ = "apk_receivers"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    manifest_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("apk_manifest.id", ondelete="CASCADE"), nullable=False, index=True)
    receiver_name: Mapped[str] = mapped_column(String(512), nullable=False, index=True)
    exported: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)
    enabled: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    permission: Mapped[Optional[str]] = mapped_column(String(256), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    manifest: Mapped["APKManifestModel"] = relationship("APKManifestModel", back_populates="receivers")


class APKProviderModel(Base):
    __tablename__ = "apk_providers"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    manifest_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("apk_manifest.id", ondelete="CASCADE"), nullable=False, index=True)
    provider_name: Mapped[str] = mapped_column(String(512), nullable=False, index=True)
    authorities: Mapped[Optional[str]] = mapped_column(String(512), nullable=True)
    exported: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)
    enabled: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    grant_uri_permissions: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    read_permission: Mapped[Optional[str]] = mapped_column(String(256), nullable=True)
    write_permission: Mapped[Optional[str]] = mapped_column(String(256), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    manifest: Mapped["APKManifestModel"] = relationship("APKManifestModel", back_populates="providers")


class APKQueryModel(Base):
    __tablename__ = "apk_queries"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    manifest_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("apk_manifest.id", ondelete="CASCADE"), nullable=False, index=True)
    query_type: Mapped[str] = mapped_column(String(64), nullable=False)
    target: Mapped[str] = mapped_column(String(512), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    manifest: Mapped["APKManifestModel"] = relationship("APKManifestModel", back_populates="queries")
