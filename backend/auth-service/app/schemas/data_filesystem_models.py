"""Pydantic v2 DTO Schemas for Enterprise Data & Filesystem Intelligence Engine (Phase 3.9 Part 1A.20).

Strictly typed DTOs for storage locations, storage operations, file objects, file operations,
databases, tables, columns, queries, database relationships, shared preferences, datastore,
cache, content providers, document providers, URI permissions, serialization, compression,
data lineage, data sensitivity, crypto relationships, network relationships, storage graph,
evidence, metrics, and result DTO.
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, ConfigDict, Field


class StorageLocationDTO(BaseModel):
    location_path: str
    location_type: str = "INTERNAL_FILES"  # INTERNAL_FILES, INTERNAL_CACHE, EXTERNAL_FILES, EXTERNAL_MEDIA, DATABASE, PREFERENCE
    access_permission: str = "READ_WRITE"
    is_encrypted: bool = False
    source_method: str

    model_config = ConfigDict(frozen=True, from_attributes=True)


class StorageOperationDTO(BaseModel):
    caller_method: str
    operation_type: str  # READ, WRITE, DELETE, CREATE, QUERY, UPDATE
    target_path: str
    framework: str = "Standard Java IO"

    model_config = ConfigDict(frozen=True, from_attributes=True)


class FileSystemObjectDTO(BaseModel):
    path: str
    file_type: str = "FILE"  # FILE, DIRECTORY, SYMLINK, TEMPORARY, CACHE
    mime_type: Optional[str] = "application/octet-stream"
    is_external: bool = False

    model_config = ConfigDict(frozen=True, from_attributes=True)


class FileOperationDTO(BaseModel):
    caller_method: str
    file_path: str
    action: str = "READ"  # READ, WRITE, STREAM, MAP_MEMORY
    stream_class: Optional[str] = "java.io.FileInputStream"

    model_config = ConfigDict(frozen=True, from_attributes=True)


class DatabaseInstanceDTO(BaseModel):
    database_name: str
    database_type: str = "SQLITE"  # SQLITE, ROOM, REALM, OBJECTBOX, MMKV, LEVELDB
    file_path: Optional[str] = None
    is_encrypted: bool = False
    framework_version: Optional[str] = "2.5.0"

    model_config = ConfigDict(frozen=True, from_attributes=True)


class DatabaseTableDTO(BaseModel):
    database_name: str
    table_name: str
    primary_key_column: Optional[str] = "id"
    columns_count: int = 1

    model_config = ConfigDict(frozen=True, from_attributes=True)


class DatabaseColumnDTO(BaseModel):
    table_name: str
    column_name: str
    data_type: str = "TEXT"
    is_primary_key: bool = False
    is_nullable: bool = True

    model_config = ConfigDict(frozen=True, from_attributes=True)


class DatabaseQueryDTO(BaseModel):
    caller_method: str
    query_type: str = "SELECT"  # SELECT, INSERT, UPDATE, DELETE, CREATE_TABLE
    raw_sql: str
    target_table: str

    model_config = ConfigDict(frozen=True, from_attributes=True)


class DatabaseRelationshipDTO(BaseModel):
    source_table: str
    target_table: str
    foreign_key_column: str
    relationship_type: str = "ONE_TO_MANY"

    model_config = ConfigDict(frozen=True, from_attributes=True)


class SharedPreferenceDTO(BaseModel):
    caller_method: str
    preference_file: str = "user_prefs"
    key_name: str
    value_type: str = "STRING"
    operation: str = "READ"  # READ, WRITE
    is_encrypted: bool = False

    model_config = ConfigDict(frozen=True, from_attributes=True)


class DataStoreDTO(BaseModel):
    caller_method: str
    datastore_name: str = "settings.preferences_pb"
    datastore_type: str = "PREFERENCES"  # PREFERENCES, PROTO
    key_or_message: str
    operation: str = "READ"

    model_config = ConfigDict(frozen=True, from_attributes=True)


class CacheLocationDTO(BaseModel):
    caller_method: str
    cache_type: str = "LRU_CACHE"  # LRU_CACHE, DISK_CACHE, OKHTTP_CACHE, GLIDE_CACHE
    path: Optional[str] = "/cache"
    eviction_policy: str = "LRU"

    model_config = ConfigDict(frozen=True, from_attributes=True)


class ContentProviderDTO(BaseModel):
    authority: str
    provider_class: str
    is_exported: bool = False
    read_permission: Optional[str] = None
    write_permission: Optional[str] = None

    model_config = ConfigDict(frozen=True, from_attributes=True)


class ContentProviderOperationDTO(BaseModel):
    caller_method: str
    authority: str
    uri: str
    operation: str = "QUERY"  # QUERY, INSERT, UPDATE, DELETE

    model_config = ConfigDict(frozen=True, from_attributes=True)


class DocumentProviderOperationDTO(BaseModel):
    caller_method: str
    document_uri: str
    action: str = "OPEN_DOCUMENT"
    has_persistable_permission: bool = False

    model_config = ConfigDict(frozen=True, from_attributes=True)


class UriPermissionDTO(BaseModel):
    caller_method: str
    target_package: str
    uri: str
    permission_flags: str = "GRANT_READ_URI_PERMISSION"

    model_config = ConfigDict(frozen=True, from_attributes=True)


class SerializationOperationDTO(BaseModel):
    caller_method: str
    format: str = "JSON"  # JSON, GSON, MOSHI, PROTOBUF, PARCELABLE, XML
    direction: str = "DESERIALIZE"  # SERIALIZE, DESERIALIZE
    data_model_class: str

    model_config = ConfigDict(frozen=True, from_attributes=True)


class CompressionOperationDTO(BaseModel):
    caller_method: str
    algorithm: str = "GZIP"  # GZIP, ZIP, DEFLATE, ZSTD
    operation: str = "DECOMPRESS"

    model_config = ConfigDict(frozen=True, from_attributes=True)


class DataLineageDTO(BaseModel):
    source_node: str
    transformation_node: str
    target_node: str
    flow_type: str = "NETWORK_TO_DATABASE"

    model_config = ConfigDict(frozen=True, from_attributes=True)


class DataSensitivityDTO(BaseModel):
    category: str = "CREDENTIALS"  # CREDENTIALS, TOKENS, PII, FINANCIAL, HEALTH, LOCATION
    storage_type: str = "SHARED_PREFERENCES"
    location_identifier: str
    source_method: str
    redaction_status: str = "REDACTED"

    model_config = ConfigDict(frozen=True, from_attributes=True)


class StorageCryptoRelationshipDTO(BaseModel):
    storage_identifier: str
    crypto_operation: str = "AES-256-GCM"
    key_alias: Optional[str] = "master_key"

    model_config = ConfigDict(frozen=True, from_attributes=True)


class StorageNetworkRelationshipDTO(BaseModel):
    network_endpoint: str
    parser: str = "JSON"
    storage_target: str

    model_config = ConfigDict(frozen=True, from_attributes=True)


class StorageGraphEdgeDTO(BaseModel):
    source_node: str
    target_node: str
    relationship: str = "STORES_DATA"

    model_config = ConfigDict(frozen=True, from_attributes=True)


class StorageEvidenceDTO(BaseModel):
    dex_id: str
    class_name: str
    method_name: str
    instruction_offset: int = 0
    evidence_type: str = "SQL_QUERY_STRING"
    raw_evidence: str

    model_config = ConfigDict(frozen=True, from_attributes=True)


class StorageMetricsDTO(BaseModel):
    locations_count: int = 0
    databases_count: int = 0
    tables_count: int = 0
    queries_count: int = 0
    preferences_count: int = 0
    sensitive_locations_count: int = 0

    model_config = ConfigDict(frozen=True, from_attributes=True)


class DataFilesystemResultDTO(BaseModel):
    locations: List[StorageLocationDTO] = Field(default_factory=list)
    operations: List[StorageOperationDTO] = Field(default_factory=list)
    files: List[FileSystemObjectDTO] = Field(default_factory=list)
    file_operations: List[FileOperationDTO] = Field(default_factory=list)
    databases: List[DatabaseInstanceDTO] = Field(default_factory=list)
    tables: List[DatabaseTableDTO] = Field(default_factory=list)
    columns: List[DatabaseColumnDTO] = Field(default_factory=list)
    queries: List[DatabaseQueryDTO] = Field(default_factory=list)
    relationships: List[DatabaseRelationshipDTO] = Field(default_factory=list)
    shared_preferences: List[SharedPreferenceDTO] = Field(default_factory=list)
    datastore_entries: List[DataStoreDTO] = Field(default_factory=list)
    cache_locations: List[CacheLocationDTO] = Field(default_factory=list)
    content_providers: List[ContentProviderDTO] = Field(default_factory=list)
    content_provider_operations: List[ContentProviderOperationDTO] = Field(default_factory=list)
    document_provider_operations: List[DocumentProviderOperationDTO] = Field(default_factory=list)
    uri_permissions: List[UriPermissionDTO] = Field(default_factory=list)
    serialization_operations: List[SerializationOperationDTO] = Field(default_factory=list)
    compression_operations: List[CompressionOperationDTO] = Field(default_factory=list)
    data_lineage: List[DataLineageDTO] = Field(default_factory=list)
    data_sensitivity: List[DataSensitivityDTO] = Field(default_factory=list)
    crypto_relationships: List[StorageCryptoRelationshipDTO] = Field(default_factory=list)
    network_relationships: List[StorageNetworkRelationshipDTO] = Field(default_factory=list)
    storage_graph: List[StorageGraphEdgeDTO] = Field(default_factory=list)
    evidence: List[StorageEvidenceDTO] = Field(default_factory=list)
    metrics: StorageMetricsDTO = Field(default_factory=StorageMetricsDTO)
    json_export: Optional[str] = None
    csv_export: Optional[str] = None
    graphml_export: Optional[str] = None
    dot_export: Optional[str] = None
    mermaid_export: Optional[str] = None
    analysis_time_ms: int = 0

    model_config = ConfigDict(frozen=True, from_attributes=True)
