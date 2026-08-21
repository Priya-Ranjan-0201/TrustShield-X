"""SQLAlchemy 2.0 ORM Models for Enterprise Data & Filesystem Intelligence Engine (Phase 3.9 Part 1A.20).

Defines database models for 24 storage tables:
storage_locations, storage_operations, file_system_objects, file_operations, database_instances,
database_tables, database_columns, database_queries, database_relationships, shared_preferences,
datastore_entries, cache_locations, content_providers, content_provider_operations,
document_provider_operations, uri_permissions, serialization_operations, compression_operations,
data_lineage, data_sensitivity, storage_crypto_relationships, storage_network_relationships,
storage_graph, storage_evidence.
"""

import uuid
from datetime import datetime, timezone
from typing import Optional, List
from sqlalchemy import String, Integer, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from app.models.base import Base


class StorageLocationModel(Base):
    __tablename__ = "storage_locations"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scan_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False, index=True)
    location_path: Mapped[str] = mapped_column(String(1024), nullable=False, index=True)
    location_type: Mapped[str] = mapped_column(String(64), nullable=False, default="INTERNAL_FILES")
    access_permission: Mapped[str] = mapped_column(String(32), nullable=False, default="READ_WRITE")
    is_encrypted: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    source_method: Mapped[str] = mapped_column(String(512), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class StorageOperationModel(Base):
    __tablename__ = "storage_operations"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scan_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False, index=True)
    caller_method: Mapped[str] = mapped_column(String(512), nullable=False)
    operation_type: Mapped[str] = mapped_column(String(64), nullable=False)
    target_path: Mapped[str] = mapped_column(String(1024), nullable=False)
    framework: Mapped[str] = mapped_column(String(128), nullable=False, default="Standard Java IO")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class FileSystemObjectModel(Base):
    __tablename__ = "file_system_objects"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scan_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False, index=True)
    path: Mapped[str] = mapped_column(String(1024), nullable=False, index=True)
    file_type: Mapped[str] = mapped_column(String(32), nullable=False, default="FILE")
    mime_type: Mapped[Optional[str]] = mapped_column(String(128), nullable=True)
    is_external: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class FileOperationModel(Base):
    __tablename__ = "file_operations"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scan_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False, index=True)
    caller_method: Mapped[str] = mapped_column(String(512), nullable=False)
    file_path: Mapped[str] = mapped_column(String(1024), nullable=False)
    action: Mapped[str] = mapped_column(String(32), nullable=False, default="READ")
    stream_class: Mapped[Optional[str]] = mapped_column(String(256), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class DatabaseInstanceModel(Base):
    __tablename__ = "database_instances"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scan_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False, index=True)
    database_name: Mapped[str] = mapped_column(String(256), nullable=False, index=True)
    database_type: Mapped[str] = mapped_column(String(32), nullable=False, default="SQLITE")
    file_path: Mapped[Optional[str]] = mapped_column(String(1024), nullable=True)
    is_encrypted: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    framework_version: Mapped[Optional[str]] = mapped_column(String(32), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class DatabaseTableModel(Base):
    __tablename__ = "database_tables"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scan_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False, index=True)
    database_name: Mapped[str] = mapped_column(String(256), nullable=False)
    table_name: Mapped[str] = mapped_column(String(256), nullable=False, index=True)
    primary_key_column: Mapped[Optional[str]] = mapped_column(String(128), nullable=True)
    columns_count: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class DatabaseColumnModel(Base):
    __tablename__ = "database_columns"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scan_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False, index=True)
    table_name: Mapped[str] = mapped_column(String(256), nullable=False)
    column_name: Mapped[str] = mapped_column(String(128), nullable=False)
    data_type: Mapped[str] = mapped_column(String(64), nullable=False, default="TEXT")
    is_primary_key: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    is_nullable: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class DatabaseQueryModel(Base):
    __tablename__ = "database_queries"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scan_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False, index=True)
    caller_method: Mapped[str] = mapped_column(String(512), nullable=False)
    query_type: Mapped[str] = mapped_column(String(32), nullable=False, default="SELECT")
    raw_sql: Mapped[str] = mapped_column(String(2048), nullable=False)
    target_table: Mapped[str] = mapped_column(String(256), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class DatabaseRelationshipModel(Base):
    __tablename__ = "database_relationships"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scan_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False, index=True)
    source_table: Mapped[str] = mapped_column(String(256), nullable=False)
    target_table: Mapped[str] = mapped_column(String(256), nullable=False)
    foreign_key_column: Mapped[str] = mapped_column(String(128), nullable=False)
    relationship_type: Mapped[str] = mapped_column(String(32), nullable=False, default="ONE_TO_MANY")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class SharedPreferenceModel(Base):
    __tablename__ = "shared_preferences"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scan_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False, index=True)
    caller_method: Mapped[str] = mapped_column(String(512), nullable=False)
    preference_file: Mapped[str] = mapped_column(String(256), nullable=False)
    key_name: Mapped[str] = mapped_column(String(256), nullable=False, index=True)
    value_type: Mapped[str] = mapped_column(String(32), nullable=False, default="STRING")
    operation: Mapped[str] = mapped_column(String(16), nullable=False, default="READ")
    is_encrypted: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class DataStoreModel(Base):
    __tablename__ = "datastore_entries"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scan_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False, index=True)
    caller_method: Mapped[str] = mapped_column(String(512), nullable=False)
    datastore_name: Mapped[str] = mapped_column(String(256), nullable=False)
    datastore_type: Mapped[str] = mapped_column(String(32), nullable=False, default="PREFERENCES")
    key_or_message: Mapped[str] = mapped_column(String(256), nullable=False)
    operation: Mapped[str] = mapped_column(String(16), nullable=False, default="READ")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class CacheLocationModel(Base):
    __tablename__ = "cache_locations"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scan_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False, index=True)
    caller_method: Mapped[str] = mapped_column(String(512), nullable=False)
    cache_type: Mapped[str] = mapped_column(String(64), nullable=False, default="LRU_CACHE")
    path: Mapped[Optional[str]] = mapped_column(String(512), nullable=True)
    eviction_policy: Mapped[str] = mapped_column(String(32), nullable=False, default="LRU")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class ContentProviderModel(Base):
    __tablename__ = "content_providers"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scan_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False, index=True)
    authority: Mapped[str] = mapped_column(String(256), nullable=False)
    provider_class: Mapped[str] = mapped_column(String(256), nullable=False)
    is_exported: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    read_permission: Mapped[Optional[str]] = mapped_column(String(256), nullable=True)
    write_permission: Mapped[Optional[str]] = mapped_column(String(256), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class ContentProviderOperationModel(Base):
    __tablename__ = "content_provider_operations"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scan_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False, index=True)
    caller_method: Mapped[str] = mapped_column(String(512), nullable=False)
    authority: Mapped[str] = mapped_column(String(256), nullable=False)
    uri: Mapped[str] = mapped_column(String(512), nullable=False)
    operation: Mapped[str] = mapped_column(String(16), nullable=False, default="QUERY")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class DocumentProviderOperationModel(Base):
    __tablename__ = "document_provider_operations"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scan_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False, index=True)
    caller_method: Mapped[str] = mapped_column(String(512), nullable=False)
    document_uri: Mapped[str] = mapped_column(String(512), nullable=False)
    action: Mapped[str] = mapped_column(String(64), nullable=False, default="OPEN_DOCUMENT")
    has_persistable_permission: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class UriPermissionModel(Base):
    __tablename__ = "uri_permissions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scan_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False, index=True)
    caller_method: Mapped[str] = mapped_column(String(512), nullable=False)
    target_package: Mapped[str] = mapped_column(String(256), nullable=False)
    uri: Mapped[str] = mapped_column(String(512), nullable=False)
    permission_flags: Mapped[str] = mapped_column(String(128), nullable=False, default="GRANT_READ_URI_PERMISSION")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class SerializationOperationModel(Base):
    __tablename__ = "serialization_operations"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scan_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False, index=True)
    caller_method: Mapped[str] = mapped_column(String(512), nullable=False)
    format: Mapped[str] = mapped_column(String(32), nullable=False, default="JSON")
    direction: Mapped[str] = mapped_column(String(32), nullable=False, default="DESERIALIZE")
    data_model_class: Mapped[str] = mapped_column(String(256), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class CompressionOperationModel(Base):
    __tablename__ = "compression_operations"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scan_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False, index=True)
    caller_method: Mapped[str] = mapped_column(String(512), nullable=False)
    algorithm: Mapped[str] = mapped_column(String(32), nullable=False, default="GZIP")
    operation: Mapped[str] = mapped_column(String(32), nullable=False, default="DECOMPRESS")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class DataLineageModel(Base):
    __tablename__ = "data_lineage"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scan_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False, index=True)
    source_node: Mapped[str] = mapped_column(String(512), nullable=False)
    transformation_node: Mapped[str] = mapped_column(String(512), nullable=False)
    target_node: Mapped[str] = mapped_column(String(512), nullable=False)
    flow_type: Mapped[str] = mapped_column(String(64), nullable=False, default="NETWORK_TO_DATABASE")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class DataSensitivityModel(Base):
    __tablename__ = "data_sensitivity"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scan_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False, index=True)
    category: Mapped[str] = mapped_column(String(64), nullable=False, default="CREDENTIALS")
    storage_type: Mapped[str] = mapped_column(String(64), nullable=False, default="SHARED_PREFERENCES")
    location_identifier: Mapped[str] = mapped_column(String(512), nullable=False)
    source_method: Mapped[str] = mapped_column(String(512), nullable=False)
    redaction_status: Mapped[str] = mapped_column(String(32), nullable=False, default="REDACTED")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class StorageCryptoRelationshipModel(Base):
    __tablename__ = "storage_crypto_relationships"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scan_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False, index=True)
    storage_identifier: Mapped[str] = mapped_column(String(512), nullable=False)
    crypto_operation: Mapped[str] = mapped_column(String(128), nullable=False, default="AES-256-GCM")
    key_alias: Mapped[Optional[str]] = mapped_column(String(256), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class StorageNetworkRelationshipModel(Base):
    __tablename__ = "storage_network_relationships"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scan_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False, index=True)
    network_endpoint: Mapped[str] = mapped_column(String(1024), nullable=False)
    parser: Mapped[str] = mapped_column(String(128), nullable=False, default="JSON")
    storage_target: Mapped[str] = mapped_column(String(512), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class StorageGraphModel(Base):
    __tablename__ = "storage_graph"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scan_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False, index=True)
    source_node: Mapped[str] = mapped_column(String(512), nullable=False)
    target_node: Mapped[str] = mapped_column(String(512), nullable=False)
    relationship: Mapped[str] = mapped_column(String(64), nullable=False, default="STORES_DATA")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class StorageEvidenceModel(Base):
    __tablename__ = "storage_evidence"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scan_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False, index=True)
    dex_id: Mapped[str] = mapped_column(String(128), nullable=False)
    class_name: Mapped[str] = mapped_column(String(256), nullable=False)
    method_name: Mapped[str] = mapped_column(String(256), nullable=False)
    instruction_offset: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    evidence_type: Mapped[str] = mapped_column(String(64), nullable=False, default="SQL_QUERY_STRING")
    raw_evidence: Mapped[str] = mapped_column(String(1024), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
