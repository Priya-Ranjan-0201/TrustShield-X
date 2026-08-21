"""Alembic Migration 014: DEX & Multi-DEX Intelligence Schema (Phase 3.7 Part 1A.6).

Creates tables:
- apk_dex_files
- apk_dex_classes
- apk_dex_methods
- apk_dex_fields
- apk_packages
with ON DELETE CASCADE foreign key constraints and performance indexes.

Revision ID: 014_dex_intelligence_schema
Revises: 013_manifest_intelligence_schema
Create Date: 2026-08-06
"""

from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = "014_dex_intelligence_schema"
down_revision: Union[str, None] = "013_manifest_intelligence_schema"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. Create apk_dex_files table
    op.create_table(
        "apk_dex_files",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("scan_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False),
        sa.Column("dex_name", sa.String(length=128), nullable=False),
        sa.Column("dex_order", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("sha256", sa.String(length=64), nullable=False),
        sa.Column("sha1", sa.String(length=40), nullable=False),
        sa.Column("checksum", sa.String(length=16), nullable=False),
        sa.Column("checksum_valid", sa.Boolean(), nullable=False, server_default="true"),
        sa.Column("file_size", sa.Integer(), nullable=False),
        sa.Column("header_size", sa.Integer(), nullable=False, server_default="112"),
        sa.Column("endian_tag", sa.String(length=32), nullable=False, server_default="0x12345678"),
        sa.Column("string_ids_size", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("type_ids_size", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("proto_ids_size", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("field_ids_size", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("method_ids_size", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("class_defs_size", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_apk_dex_files_scan_id", "apk_dex_files", ["scan_id"])
    op.create_index("ix_apk_dex_files_dex_name", "apk_dex_files", ["dex_name"])
    op.create_index("ix_apk_dex_files_sha256", "apk_dex_files", ["sha256"])

    # 2. Create apk_dex_classes table
    op.create_table(
        "apk_dex_classes",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("dex_file_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("apk_dex_files.id", ondelete="CASCADE"), nullable=False),
        sa.Column("class_name", sa.String(length=512), nullable=False),
        sa.Column("package_name", sa.String(length=256), nullable=False),
        sa.Column("superclass", sa.String(length=512), nullable=True),
        sa.Column("access_flags", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("is_interface", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column("is_enum", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column("is_abstract", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column("source_file", sa.String(length=256), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_apk_dex_classes_dex_file_id", "apk_dex_classes", ["dex_file_id"])
    op.create_index("ix_apk_dex_classes_class_name", "apk_dex_classes", ["class_name"])
    op.create_index("ix_apk_dex_classes_package_name", "apk_dex_classes", ["package_name"])

    # 3. Create apk_dex_methods table
    op.create_table(
        "apk_dex_methods",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("class_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("apk_dex_classes.id", ondelete="CASCADE"), nullable=False),
        sa.Column("method_name", sa.String(length=256), nullable=False),
        sa.Column("return_type", sa.String(length=256), nullable=False, server_default="V"),
        sa.Column("parameter_types", postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column("access_flags", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("is_direct", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column("is_virtual", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column("is_native", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column("is_constructor", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_apk_dex_methods_class_id", "apk_dex_methods", ["class_id"])
    op.create_index("ix_apk_dex_methods_method_name", "apk_dex_methods", ["method_name"])

    # 4. Create apk_dex_fields table
    op.create_table(
        "apk_dex_fields",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("class_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("apk_dex_classes.id", ondelete="CASCADE"), nullable=False),
        sa.Column("field_name", sa.String(length=256), nullable=False),
        sa.Column("field_type", sa.String(length=256), nullable=False),
        sa.Column("access_flags", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("is_static", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column("is_final", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_apk_dex_fields_class_id", "apk_dex_fields", ["class_id"])

    # 5. Create apk_packages table
    op.create_table(
        "apk_packages",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("scan_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False),
        sa.Column("package_name", sa.String(length=256), nullable=False),
        sa.Column("class_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("depth", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_apk_packages_scan_id", "apk_packages", ["scan_id"])
    op.create_index("ix_apk_packages_package_name", "apk_packages", ["package_name"])


def downgrade() -> None:
    op.drop_index("ix_apk_packages_package_name", table_name="apk_packages")
    op.drop_index("ix_apk_packages_scan_id", table_name="apk_packages")
    op.drop_table("apk_packages")

    op.drop_index("ix_apk_dex_fields_class_id", table_name="apk_dex_fields")
    op.drop_table("apk_dex_fields")

    op.drop_index("ix_apk_dex_methods_method_name", table_name="apk_dex_methods")
    op.drop_index("ix_apk_dex_methods_class_id", table_name="apk_dex_methods")
    op.drop_table("apk_dex_methods")

    op.drop_index("ix_apk_dex_classes_package_name", table_name="apk_dex_classes")
    op.drop_index("ix_apk_dex_classes_class_name", table_name="apk_dex_classes")
    op.drop_index("ix_apk_dex_classes_dex_file_id", table_name="apk_dex_classes")
    op.drop_table("apk_dex_classes")

    op.drop_index("ix_apk_dex_files_sha256", table_name="apk_dex_files")
    op.drop_index("ix_apk_dex_files_dex_name", table_name="apk_dex_files")
    op.drop_index("ix_apk_dex_files_scan_id", table_name="apk_dex_files")
    op.drop_table("apk_dex_files")
