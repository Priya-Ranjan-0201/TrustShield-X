"""Alembic Migration 021: DEX Structure Intelligence Schema (Phase 3.7 Part 1A.13).

Creates tables:
- dex_packages
- dex_classes
- dex_methods
- dex_fields
- dex_strings
- dex_types
- dex_statistics
with ON DELETE CASCADE foreign key constraints and performance indexes.

Revision ID: 021_dex_structure
Revises: 020_apk_binary_inventory
Create Date: 2026-08-06
"""

from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = "021_dex_structure"
down_revision: Union[str, None] = "020_apk_binary_inventory"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. Create dex_packages table
    op.create_table(
        "dex_packages",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("scan_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False),
        sa.Column("package_name", sa.String(length=256), nullable=False),
        sa.Column("parent_package", sa.String(length=256), nullable=True),
        sa.Column("depth", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("class_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("method_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_dex_packages_scan_id", "dex_packages", ["scan_id"])
    op.create_index("ix_dex_packages_package_name", "dex_packages", ["package_name"])

    # 2. Create dex_classes table
    op.create_table(
        "dex_classes",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("scan_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False),
        sa.Column("class_name", sa.String(length=512), nullable=False),
        sa.Column("simple_name", sa.String(length=256), nullable=False),
        sa.Column("package_name", sa.String(length=256), nullable=False),
        sa.Column("superclass", sa.String(length=512), nullable=True),
        sa.Column("interfaces", sa.JSON(), nullable=False, server_default=sa.text("'[]'::json")),
        sa.Column("access_flags", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("is_abstract", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column("is_final", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column("is_inner", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column("source_file", sa.String(length=256), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_dex_classes_scan_id", "dex_classes", ["scan_id"])
    op.create_index("ix_dex_classes_class_name", "dex_classes", ["class_name"])
    op.create_index("ix_dex_classes_package_name", "dex_classes", ["package_name"])

    # 3. Create dex_methods table
    op.create_table(
        "dex_methods",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("scan_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False),
        sa.Column("class_name", sa.String(length=512), nullable=False),
        sa.Column("method_name", sa.String(length=256), nullable=False),
        sa.Column("return_type", sa.String(length=128), nullable=False, server_default="'V'"),
        sa.Column("parameter_types", sa.JSON(), nullable=False, server_default=sa.text("'[]'::json")),
        sa.Column("access_flags", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("is_constructor", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column("is_static", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column("is_native", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column("register_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("instruction_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_dex_methods_scan_id", "dex_methods", ["scan_id"])
    op.create_index("ix_dex_methods_class_name", "dex_methods", ["class_name"])
    op.create_index("ix_dex_methods_method_name", "dex_methods", ["method_name"])

    # 4. Create dex_fields table
    op.create_table(
        "dex_fields",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("scan_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False),
        sa.Column("class_name", sa.String(length=512), nullable=False),
        sa.Column("field_name", sa.String(length=256), nullable=False),
        sa.Column("field_type", sa.String(length=128), nullable=False),
        sa.Column("access_flags", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("is_static", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column("is_final", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_dex_fields_scan_id", "dex_fields", ["scan_id"])
    op.create_index("ix_dex_fields_class_name", "dex_fields", ["class_name"])

    # 5. Create dex_strings table
    op.create_table(
        "dex_strings",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("scan_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False),
        sa.Column("string_value", sa.String(length=1024), nullable=False),
        sa.Column("string_hash", sa.String(length=64), nullable=False),
        sa.Column("length", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("offset", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_dex_strings_scan_id", "dex_strings", ["scan_id"])
    op.create_index("ix_dex_strings_string_hash", "dex_strings", ["string_hash"])

    # 6. Create dex_types table
    op.create_table(
        "dex_types",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("scan_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False),
        sa.Column("type_name", sa.String(length=512), nullable=False),
        sa.Column("kind", sa.String(length=64), nullable=False, server_default="'OBJECT'"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_dex_types_scan_id", "dex_types", ["scan_id"])

    # 7. Create dex_statistics table
    op.create_table(
        "dex_statistics",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("scan_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False),
        sa.Column("total_packages", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("total_classes", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("total_methods", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("total_fields", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("total_strings", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("avg_methods_per_class", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("largest_package", sa.String(length=256), nullable=True),
        sa.Column("largest_class", sa.String(length=512), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_dex_statistics_scan_id", "dex_statistics", ["scan_id"])


def downgrade() -> None:
    op.drop_index("ix_dex_statistics_scan_id", table_name="dex_statistics")
    op.drop_table("dex_statistics")

    op.drop_index("ix_dex_types_scan_id", table_name="dex_types")
    op.drop_table("dex_types")

    op.drop_index("ix_dex_strings_string_hash", table_name="dex_strings")
    op.drop_index("ix_dex_strings_scan_id", table_name="dex_strings")
    op.drop_table("dex_strings")

    op.drop_index("ix_dex_fields_class_name", table_name="dex_fields")
    op.drop_index("ix_dex_fields_scan_id", table_name="dex_fields")
    op.drop_table("dex_fields")

    op.drop_index("ix_dex_methods_method_name", table_name="dex_methods")
    op.drop_index("ix_dex_methods_class_name", table_name="dex_methods")
    op.drop_index("ix_dex_methods_scan_id", table_name="dex_methods")
    op.drop_table("dex_methods")

    op.drop_index("ix_dex_classes_package_name", table_name="dex_classes")
    op.drop_index("ix_dex_classes_class_name", table_name="dex_classes")
    op.drop_index("ix_dex_classes_scan_id", table_name="dex_classes")
    op.drop_table("dex_classes")

    op.drop_index("ix_dex_packages_package_name", table_name="dex_packages")
    op.drop_index("ix_dex_packages_scan_id", table_name="dex_packages")
    op.drop_table("dex_packages")
