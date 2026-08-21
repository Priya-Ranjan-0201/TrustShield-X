"""Alembic Migration 016: Permission Intelligence Normalization Schema (Phase 3.7 Part 1A.8).

Creates tables:
- permission_catalog
- apk_permission_intelligence
- permission_relationships
- permission_sdk_support
with ON DELETE CASCADE foreign key constraints and performance indexes.

Revision ID: 016_permission_intelligence_schema
Revises: 015_manifest_intelligence_schema
Create Date: 2026-08-06
"""

from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = "016_permission_intelligence_schema"
down_revision: Union[str, None] = "015_manifest_intelligence_schema"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. Create permission_catalog table
    op.create_table(
        "permission_catalog",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("permission_name", sa.String(length=256), nullable=False, unique=True),
        sa.Column("category", sa.String(length=128), nullable=False),
        sa.Column("protection_level", sa.String(length=64), nullable=False),
        sa.Column("permission_group", sa.String(length=256), nullable=True),
        sa.Column("api_introduced", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("api_deprecated", sa.Integer(), nullable=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("doc_url", sa.String(length=512), nullable=True),
        sa.Column("is_runtime", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column("is_install", sa.Boolean(), nullable=False, server_default="true"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_permission_catalog_permission_name", "permission_catalog", ["permission_name"])
    op.create_index("ix_permission_catalog_category", "permission_catalog", ["category"])
    op.create_index("ix_permission_catalog_protection_level", "permission_catalog", ["protection_level"])

    # 2. Create apk_permission_intelligence table
    op.create_table(
        "apk_permission_intelligence",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("scan_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False),
        sa.Column("permission_name", sa.String(length=256), nullable=False),
        sa.Column("category", sa.String(length=128), nullable=False),
        sa.Column("protection_level", sa.String(length=64), nullable=False),
        sa.Column("permission_group", sa.String(length=256), nullable=True),
        sa.Column("is_runtime", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column("is_dangerous", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column("is_custom", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column("is_vendor", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column("is_unknown", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column("target_sdk_supported", sa.Boolean(), nullable=False, server_default="true"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_apk_permission_intel_scan_id", "apk_permission_intelligence", ["scan_id"])
    op.create_index("ix_apk_permission_intel_permission_name", "apk_permission_intelligence", ["permission_name"])
    op.create_index("ix_apk_permission_intel_category", "apk_permission_intelligence", ["category"])
    op.create_index("ix_apk_permission_intel_protection_level", "apk_permission_intelligence", ["protection_level"])
    op.create_index("ix_apk_permission_intel_is_runtime", "apk_permission_intelligence", ["is_runtime"])

    # 3. Create permission_relationships table
    op.create_table(
        "permission_relationships",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("permission_name", sa.String(length=256), nullable=False),
        sa.Column("related_permission_name", sa.String(length=256), nullable=False),
        sa.Column("relationship_type", sa.String(length=64), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_permission_relationships_permission_name", "permission_relationships", ["permission_name"])

    # 4. Create permission_sdk_support table
    op.create_table(
        "permission_sdk_support",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("permission_name", sa.String(length=256), nullable=False),
        sa.Column("min_sdk", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("max_sdk", sa.Integer(), nullable=True),
        sa.Column("status", sa.String(length=64), nullable=False, server_default="'SUPPORTED'"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_permission_sdk_support_permission_name", "permission_sdk_support", ["permission_name"])


def downgrade() -> None:
    op.drop_index("ix_permission_sdk_support_permission_name", table_name="permission_sdk_support")
    op.drop_table("permission_sdk_support")

    op.drop_index("ix_permission_relationships_permission_name", table_name="permission_relationships")
    op.drop_table("permission_relationships")

    op.drop_index("ix_apk_permission_intel_is_runtime", table_name="apk_permission_intelligence")
    op.drop_index("ix_apk_permission_intel_protection_level", table_name="apk_permission_intelligence")
    op.drop_index("ix_apk_permission_intel_category", table_name="apk_permission_intelligence")
    op.drop_index("ix_apk_permission_intel_permission_name", table_name="apk_permission_intelligence")
    op.drop_index("ix_apk_permission_intel_scan_id", table_name="apk_permission_intelligence")
    op.drop_table("apk_permission_intelligence")

    op.drop_index("ix_permission_catalog_protection_level", table_name="permission_catalog")
    op.drop_index("ix_permission_catalog_category", table_name="permission_catalog")
    op.drop_index("ix_permission_catalog_permission_name", table_name="permission_catalog")
    op.drop_table("permission_catalog")
