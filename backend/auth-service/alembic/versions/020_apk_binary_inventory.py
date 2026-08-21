"""Alembic Migration 020: APK Binary Inventory & File Intelligence Schema (Phase 3.7 Part 1A.12).

Creates tables:
- apk_binary_inventory
- apk_binary_hashes
- apk_binary_statistics
with ON DELETE CASCADE foreign key constraints and performance indexes.

Revision ID: 020_apk_binary_inventory
Revises: 019_apk_metadata_schema
Create Date: 2026-08-06
"""

from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = "020_apk_binary_inventory"
down_revision: Union[str, None] = "019_apk_metadata_schema"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. Create apk_binary_inventory table
    op.create_table(
        "apk_binary_inventory",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("scan_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False),
        sa.Column("file_path", sa.String(length=512), nullable=False),
        sa.Column("filename", sa.String(length=256), nullable=False),
        sa.Column("directory", sa.String(length=512), nullable=False),
        sa.Column("extension", sa.String(length=64), nullable=False),
        sa.Column("file_category", sa.String(length=64), nullable=False),
        sa.Column("uncompressed_size", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("compressed_size", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("compression_method", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("crc32", sa.String(length=16), nullable=False, server_default="'00000000'"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_apk_binary_inventory_scan_id", "apk_binary_inventory", ["scan_id"])
    op.create_index("ix_apk_binary_inventory_file_path", "apk_binary_inventory", ["file_path"])
    op.create_index("ix_apk_binary_inventory_file_category", "apk_binary_inventory", ["file_category"])

    # 2. Create apk_binary_hashes table
    op.create_table(
        "apk_binary_hashes",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("inventory_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("apk_binary_inventory.id", ondelete="CASCADE"), nullable=False),
        sa.Column("sha256", sa.String(length=64), nullable=False),
        sa.Column("sha1", sa.String(length=40), nullable=False),
        sa.Column("md5", sa.String(length=32), nullable=False),
        sa.Column("crc32", sa.String(length=16), nullable=False),
        sa.Column("entropy", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("mime_type", sa.String(length=128), nullable=False, server_default="'application/octet-stream'"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_apk_binary_hashes_inventory_id", "apk_binary_hashes", ["inventory_id"])
    op.create_index("ix_apk_binary_hashes_sha256", "apk_binary_hashes", ["sha256"])

    # 3. Create apk_binary_statistics table
    op.create_table(
        "apk_binary_statistics",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("scan_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False),
        sa.Column("total_files", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("total_directories", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("total_size_bytes", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("compressed_size_bytes", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("dex_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("native_library_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("assets_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("resources_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("media_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("config_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("unknown_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_apk_binary_statistics_scan_id", "apk_binary_statistics", ["scan_id"])


def downgrade() -> None:
    op.drop_index("ix_apk_binary_statistics_scan_id", table_name="apk_binary_statistics")
    op.drop_table("apk_binary_statistics")

    op.drop_index("ix_apk_binary_hashes_sha256", table_name="apk_binary_hashes")
    op.drop_index("ix_apk_binary_hashes_inventory_id", table_name="apk_binary_hashes")
    op.drop_table("apk_binary_hashes")

    op.drop_index("ix_apk_binary_inventory_file_category", table_name="apk_binary_inventory")
    op.drop_index("ix_apk_binary_inventory_file_path", table_name="apk_binary_inventory")
    op.drop_index("ix_apk_binary_inventory_scan_id", table_name="apk_binary_inventory")
    op.drop_table("apk_binary_inventory")
