"""Alembic Migration 015: Android Manifest Intelligence Schema (Phase 3.7 Part 1A.7).

Creates/upgrades tables:
- apk_manifest
- apk_permissions
- apk_activities
- apk_services
- apk_receivers
- apk_providers
- apk_intent_filters
- apk_features
- apk_libraries
- apk_queries
with ON DELETE CASCADE foreign key constraints and performance indexes.

Revision ID: 015_manifest_intelligence_schema
Revises: 014_dex_intelligence_schema
Create Date: 2026-08-06
"""

from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = "015_manifest_intelligence_schema"
down_revision: Union[str, None] = "014_dex_intelligence_schema"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. Create apk_manifest_permissions table
    op.create_table(
        "apk_manifest_permissions",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("manifest_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("apk_manifest.id", ondelete="CASCADE"), nullable=False),
        sa.Column("permission_name", sa.String(length=256), nullable=False),
        sa.Column("protection_level", sa.String(length=64), nullable=True),
        sa.Column("declared", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column("requested", sa.Boolean(), nullable=False, server_default="true"),
        sa.Column("is_custom", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_apk_manifest_permissions_manifest_id", "apk_manifest_permissions", ["manifest_id"])
    op.create_index("ix_apk_manifest_permissions_permission_name", "apk_manifest_permissions", ["permission_name"])

    # 2. Create apk_activities table
    op.create_table(
        "apk_activities",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("manifest_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("apk_manifest.id", ondelete="CASCADE"), nullable=False),
        sa.Column("activity_name", sa.String(length=512), nullable=False),
        sa.Column("exported", sa.Boolean(), nullable=True),
        sa.Column("enabled", sa.Boolean(), nullable=False, server_default="true"),
        sa.Column("permission", sa.String(length=256), nullable=True),
        sa.Column("launch_mode", sa.String(length=64), nullable=True),
        sa.Column("task_affinity", sa.String(length=256), nullable=True),
        sa.Column("theme", sa.String(length=256), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_apk_activities_manifest_id", "apk_activities", ["manifest_id"])
    op.create_index("ix_apk_activities_activity_name", "apk_activities", ["activity_name"])

    # 3. Create apk_services table
    op.create_table(
        "apk_services",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("manifest_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("apk_manifest.id", ondelete="CASCADE"), nullable=False),
        sa.Column("service_name", sa.String(length=512), nullable=False),
        sa.Column("exported", sa.Boolean(), nullable=True),
        sa.Column("enabled", sa.Boolean(), nullable=False, server_default="true"),
        sa.Column("permission", sa.String(length=256), nullable=True),
        sa.Column("foreground_service_type", sa.String(length=128), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_apk_services_manifest_id", "apk_services", ["manifest_id"])

    # 4. Create apk_receivers table
    op.create_table(
        "apk_receivers",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("manifest_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("apk_manifest.id", ondelete="CASCADE"), nullable=False),
        sa.Column("receiver_name", sa.String(length=512), nullable=False),
        sa.Column("exported", sa.Boolean(), nullable=True),
        sa.Column("enabled", sa.Boolean(), nullable=False, server_default="true"),
        sa.Column("permission", sa.String(length=256), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_apk_receivers_manifest_id", "apk_receivers", ["manifest_id"])

    # 5. Create apk_providers table
    op.create_table(
        "apk_providers",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("manifest_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("apk_manifest.id", ondelete="CASCADE"), nullable=False),
        sa.Column("provider_name", sa.String(length=512), nullable=False),
        sa.Column("authorities", sa.String(length=512), nullable=True),
        sa.Column("exported", sa.Boolean(), nullable=True),
        sa.Column("enabled", sa.Boolean(), nullable=False, server_default="true"),
        sa.Column("grant_uri_permissions", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column("read_permission", sa.String(length=256), nullable=True),
        sa.Column("write_permission", sa.String(length=256), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_apk_providers_manifest_id", "apk_providers", ["manifest_id"])
    op.create_index("ix_apk_providers_provider_name", "apk_providers", ["provider_name"])

    # 6. Create apk_queries table
    op.create_table(
        "apk_queries",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("manifest_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("apk_manifest.id", ondelete="CASCADE"), nullable=False),
        sa.Column("query_type", sa.String(length=64), nullable=False),
        sa.Column("target", sa.String(length=512), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_apk_queries_manifest_id", "apk_queries", ["manifest_id"])


def downgrade() -> None:
    op.drop_index("ix_apk_queries_manifest_id", table_name="apk_queries")
    op.drop_table("apk_queries")

    op.drop_index("ix_apk_providers_provider_name", table_name="apk_providers")
    op.drop_index("ix_apk_providers_manifest_id", table_name="apk_providers")
    op.drop_table("apk_providers")

    op.drop_index("ix_apk_receivers_manifest_id", table_name="apk_receivers")
    op.drop_table("apk_receivers")

    op.drop_index("ix_apk_services_manifest_id", table_name="apk_services")
    op.drop_table("apk_services")

    op.drop_index("ix_apk_activities_activity_name", table_name="apk_activities")
    op.drop_index("ix_apk_activities_manifest_id", table_name="apk_activities")
    op.drop_table("apk_activities")

    op.drop_index("ix_apk_manifest_permissions_permission_name", table_name="apk_manifest_permissions")
    op.drop_index("ix_apk_manifest_permissions_manifest_id", table_name="apk_manifest_permissions")
    op.drop_table("apk_manifest_permissions")
