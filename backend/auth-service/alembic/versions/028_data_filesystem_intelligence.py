"""Alembic Migration 028: Data & Filesystem Communication Schema (Phase 3.9 Part 1A.20).

Creates 24 storage tables:
storage_locations, storage_operations, file_system_objects, file_operations, database_instances,
database_tables, database_columns, database_queries, database_relationships, shared_preferences,
datastore_entries, cache_locations, content_providers, content_provider_operations,
document_provider_operations, uri_permissions, serialization_operations, compression_operations,
data_lineage, data_sensitivity, storage_crypto_relationships, storage_network_relationships,
storage_graph, storage_evidence
with ON DELETE CASCADE foreign key constraints and performance indexes.

Revision ID: 028_data_filesystem_intelligence
Revises: 027_network_intelligence
Create Date: 2026-08-12
"""

from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = "028_data_filesystem_intelligence"
down_revision: Union[str, None] = "027_network_intelligence"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. storage_locations
    op.create_table(
        "storage_locations",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("scan_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False),
        sa.Column("location_path", sa.String(length=1024), nullable=False),
        sa.Column("location_type", sa.String(length=64), nullable=False, server_default="'INTERNAL_FILES'"),
        sa.Column("access_permission", sa.String(length=32), nullable=False, server_default="'READ_WRITE'"),
        sa.Column("is_encrypted", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column("source_method", sa.String(length=512), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_storage_locations_scan_id", "storage_locations", ["scan_id"])
    op.create_index("ix_storage_locations_location_path", "storage_locations", ["location_path"])

    # 2. storage_operations
    op.create_table(
        "storage_operations",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("scan_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False),
        sa.Column("caller_method", sa.String(length=512), nullable=False),
        sa.Column("operation_type", sa.String(length=64), nullable=False),
        sa.Column("target_path", sa.String(length=1024), nullable=False),
        sa.Column("framework", sa.String(length=128), nullable=False, server_default="'Standard Java IO'"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_storage_operations_scan_id", "storage_operations", ["scan_id"])

    # 3. file_system_objects
    op.create_table(
        "file_system_objects",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("scan_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False),
        sa.Column("path", sa.String(length=1024), nullable=False),
        sa.Column("file_type", sa.String(length=32), nullable=False, server_default="'FILE'"),
        sa.Column("mime_type", sa.String(length=128), nullable=True),
        sa.Column("is_external", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_file_system_objects_scan_id", "file_system_objects", ["scan_id"])

    # 4. file_operations
    op.create_table(
        "file_operations",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("scan_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False),
        sa.Column("caller_method", sa.String(length=512), nullable=False),
        sa.Column("file_path", sa.String(length=1024), nullable=False),
        sa.Column("action", sa.String(length=32), nullable=False, server_default="'READ'"),
        sa.Column("stream_class", sa.String(length=256), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_file_operations_scan_id", "file_operations", ["scan_id"])

    # 5. database_instances
    op.create_table(
        "database_instances",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("scan_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False),
        sa.Column("database_name", sa.String(length=256), nullable=False),
        sa.Column("database_type", sa.String(length=32), nullable=False, server_default="'SQLITE'"),
        sa.Column("file_path", sa.String(length=1024), nullable=True),
        sa.Column("is_encrypted", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column("framework_version", sa.String(length=32), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_database_instances_scan_id", "database_instances", ["scan_id"])
    op.create_index("ix_database_instances_database_name", "database_instances", ["database_name"])

    # 6. database_tables
    op.create_table(
        "database_tables",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("scan_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False),
        sa.Column("database_name", sa.String(length=256), nullable=False),
        sa.Column("table_name", sa.String(length=256), nullable=False),
        sa.Column("primary_key_column", sa.String(length=128), nullable=True),
        sa.Column("columns_count", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_database_tables_scan_id", "database_tables", ["scan_id"])
    op.create_index("ix_database_tables_table_name", "database_tables", ["table_name"])

    # 7. database_columns
    op.create_table(
        "database_columns",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("scan_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False),
        sa.Column("table_name", sa.String(length=256), nullable=False),
        sa.Column("column_name", sa.String(length=128), nullable=False),
        sa.Column("data_type", sa.String(length=64), nullable=False, server_default="'TEXT'"),
        sa.Column("is_primary_key", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column("is_nullable", sa.Boolean(), nullable=False, server_default="true"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_database_columns_scan_id", "database_columns", ["scan_id"])

    # 8. database_queries
    op.create_table(
        "database_queries",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("scan_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False),
        sa.Column("caller_method", sa.String(length=512), nullable=False),
        sa.Column("query_type", sa.String(length=32), nullable=False, server_default="'SELECT'"),
        sa.Column("raw_sql", sa.String(length=2048), nullable=False),
        sa.Column("target_table", sa.String(length=256), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_database_queries_scan_id", "database_queries", ["scan_id"])

    # 9. database_relationships
    op.create_table(
        "database_relationships",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("scan_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False),
        sa.Column("source_table", sa.String(length=256), nullable=False),
        sa.Column("target_table", sa.String(length=256), nullable=False),
        sa.Column("foreign_key_column", sa.String(length=128), nullable=False),
        sa.Column("relationship_type", sa.String(length=32), nullable=False, server_default="'ONE_TO_MANY'"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_database_relationships_scan_id", "database_relationships", ["scan_id"])

    # 10. shared_preferences
    op.create_table(
        "shared_preferences",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("scan_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False),
        sa.Column("caller_method", sa.String(length=512), nullable=False),
        sa.Column("preference_file", sa.String(length=256), nullable=False),
        sa.Column("key_name", sa.String(length=256), nullable=False),
        sa.Column("value_type", sa.String(length=32), nullable=False, server_default="'STRING'"),
        sa.Column("operation", sa.String(length=16), nullable=False, server_default="'READ'"),
        sa.Column("is_encrypted", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_shared_preferences_scan_id", "shared_preferences", ["scan_id"])
    op.create_index("ix_shared_preferences_key_name", "shared_preferences", ["key_name"])

    # 11. datastore_entries
    op.create_table(
        "datastore_entries",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("scan_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False),
        sa.Column("caller_method", sa.String(length=512), nullable=False),
        sa.Column("datastore_name", sa.String(length=256), nullable=False),
        sa.Column("datastore_type", sa.String(length=32), nullable=False, server_default="'PREFERENCES'"),
        sa.Column("key_or_message", sa.String(length=256), nullable=False),
        sa.Column("operation", sa.String(length=16), nullable=False, server_default="'READ'"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_datastore_entries_scan_id", "datastore_entries", ["scan_id"])

    # 12. cache_locations
    op.create_table(
        "cache_locations",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("scan_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False),
        sa.Column("caller_method", sa.String(length=512), nullable=False),
        sa.Column("cache_type", sa.String(length=64), nullable=False, server_default="'LRU_CACHE'"),
        sa.Column("path", sa.String(length=512), nullable=True),
        sa.Column("eviction_policy", sa.String(length=32), nullable=False, server_default="'LRU'"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_cache_locations_scan_id", "cache_locations", ["scan_id"])

    # 13. content_providers
    op.create_table(
        "content_providers",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("scan_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False),
        sa.Column("authority", sa.String(length=256), nullable=False),
        sa.Column("provider_class", sa.String(length=256), nullable=False),
        sa.Column("is_exported", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column("read_permission", sa.String(length=256), nullable=True),
        sa.Column("write_permission", sa.String(length=256), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_content_providers_scan_id", "content_providers", ["scan_id"])

    # 14. content_provider_operations
    op.create_table(
        "content_provider_operations",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("scan_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False),
        sa.Column("caller_method", sa.String(length=512), nullable=False),
        sa.Column("authority", sa.String(length=256), nullable=False),
        sa.Column("uri", sa.String(length=512), nullable=False),
        sa.Column("operation", sa.String(length=16), nullable=False, server_default="'QUERY'"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_content_provider_operations_scan_id", "content_provider_operations", ["scan_id"])

    # 15. document_provider_operations
    op.create_table(
        "document_provider_operations",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("scan_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False),
        sa.Column("caller_method", sa.String(length=512), nullable=False),
        sa.Column("document_uri", sa.String(length=512), nullable=False),
        sa.Column("action", sa.String(length=64), nullable=False, server_default="'OPEN_DOCUMENT'"),
        sa.Column("has_persistable_permission", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_document_provider_operations_scan_id", "document_provider_operations", ["scan_id"])

    # 16. uri_permissions
    op.create_table(
        "uri_permissions",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("scan_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False),
        sa.Column("caller_method", sa.String(length=512), nullable=False),
        sa.Column("target_package", sa.String(length=256), nullable=False),
        sa.Column("uri", sa.String(length=512), nullable=False),
        sa.Column("permission_flags", sa.String(length=128), nullable=False, server_default="'GRANT_READ_URI_PERMISSION'"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_uri_permissions_scan_id", "uri_permissions", ["scan_id"])

    # 17. serialization_operations
    op.create_table(
        "serialization_operations",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("scan_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False),
        sa.Column("caller_method", sa.String(length=512), nullable=False),
        sa.Column("format", sa.String(length=32), nullable=False, server_default="'JSON'"),
        sa.Column("direction", sa.String(length=32), nullable=False, server_default="'DESERIALIZE'"),
        sa.Column("data_model_class", sa.String(length=256), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_serialization_operations_scan_id", "serialization_operations", ["scan_id"])

    # 18. compression_operations
    op.create_table(
        "compression_operations",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("scan_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False),
        sa.Column("caller_method", sa.String(length=512), nullable=False),
        sa.Column("algorithm", sa.String(length=32), nullable=False, server_default="'GZIP'"),
        sa.Column("operation", sa.String(length=32), nullable=False, server_default="'DECOMPRESS'"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_compression_operations_scan_id", "compression_operations", ["scan_id"])

    # 19. data_lineage
    op.create_table(
        "data_lineage",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("scan_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False),
        sa.Column("source_node", sa.String(length=512), nullable=False),
        sa.Column("transformation_node", sa.String(length=512), nullable=False),
        sa.Column("target_node", sa.String(length=512), nullable=False),
        sa.Column("flow_type", sa.String(length=64), nullable=False, server_default="'NETWORK_TO_DATABASE'"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_data_lineage_scan_id", "data_lineage", ["scan_id"])

    # 20. data_sensitivity
    op.create_table(
        "data_sensitivity",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("scan_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False),
        sa.Column("category", sa.String(length=64), nullable=False, server_default="'CREDENTIALS'"),
        sa.Column("storage_type", sa.String(length=64), nullable=False, server_default="'SHARED_PREFERENCES'"),
        sa.Column("location_identifier", sa.String(length=512), nullable=False),
        sa.Column("source_method", sa.String(length=512), nullable=False),
        sa.Column("redaction_status", sa.String(length=32), nullable=False, server_default="'REDACTED'"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_data_sensitivity_scan_id", "data_sensitivity", ["scan_id"])

    # 21. storage_crypto_relationships
    op.create_table(
        "storage_crypto_relationships",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("scan_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False),
        sa.Column("storage_identifier", sa.String(length=512), nullable=False),
        sa.Column("crypto_operation", sa.String(length=128), nullable=False, server_default="'AES-256-GCM'"),
        sa.Column("key_alias", sa.String(length=256), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_storage_crypto_relationships_scan_id", "storage_crypto_relationships", ["scan_id"])

    # 22. storage_network_relationships
    op.create_table(
        "storage_network_relationships",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("scan_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False),
        sa.Column("network_endpoint", sa.String(length=1024), nullable=False),
        sa.Column("parser", sa.String(length=128), nullable=False, server_default="'JSON'"),
        sa.Column("storage_target", sa.String(length=512), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_storage_network_relationships_scan_id", "storage_network_relationships", ["scan_id"])

    # 23. storage_graph
    op.create_table(
        "storage_graph",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("scan_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False),
        sa.Column("source_node", sa.String(length=512), nullable=False),
        sa.Column("target_node", sa.String(length=512), nullable=False),
        sa.Column("relationship", sa.String(length=64), nullable=False, server_default="'STORES_DATA'"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_storage_graph_scan_id", "storage_graph", ["scan_id"])

    # 24. storage_evidence
    op.create_table(
        "storage_evidence",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("scan_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False),
        sa.Column("dex_id", sa.String(length=128), nullable=False),
        sa.Column("class_name", sa.String(length=256), nullable=False),
        sa.Column("method_name", sa.String(length=256), nullable=False),
        sa.Column("instruction_offset", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("evidence_type", sa.String(length=64), nullable=False, server_default="'SQL_QUERY_STRING'"),
        sa.Column("raw_evidence", sa.String(length=1024), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_storage_evidence_scan_id", "storage_evidence", ["scan_id"])


def downgrade() -> None:
    for tbl in [
        "storage_evidence", "storage_graph", "storage_network_relationships",
        "storage_crypto_relationships", "data_sensitivity", "data_lineage",
        "compression_operations", "serialization_operations", "uri_permissions",
        "document_provider_operations", "content_provider_operations", "content_providers",
        "cache_locations", "datastore_entries", "shared_preferences", "database_relationships",
        "database_queries", "database_columns", "database_tables", "database_instances",
        "file_operations", "file_system_objects", "storage_operations", "storage_locations",
    ]:
        op.drop_index(f"ix_{tbl}_scan_id", table_name=tbl)
        op.drop_table(tbl)
