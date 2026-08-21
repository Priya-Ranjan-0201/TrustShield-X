"""Alembic Migration 017: Android Component Intelligence Schema (Phase 3.7 Part 1A.9).

Creates tables:
- component_catalog
- apk_components_intel
- component_intent_filters
- component_relationships
- component_processes
with ON DELETE CASCADE foreign key constraints and performance indexes.

Revision ID: 017_component_intelligence_schema
Revises: 016_permission_intelligence_schema
Create Date: 2026-08-06
"""

from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = "017_component_intelligence_schema"
down_revision: Union[str, None] = "016_permission_intelligence_schema"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. Create component_catalog table
    op.create_table(
        "component_catalog",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("component_type", sa.String(length=64), nullable=False, unique=True),
        sa.Column("android_purpose", sa.Text(), nullable=True),
        sa.Column("lifecycle_type", sa.String(length=64), nullable=False, server_default="'UI_LIFECYCLE'"),
        sa.Column("default_exported_behavior", sa.String(length=64), nullable=False, server_default="'FALSE'"),
        sa.Column("supports_intent_filters", sa.Boolean(), nullable=False, server_default="true"),
        sa.Column("supports_permissions", sa.Boolean(), nullable=False, server_default="true"),
        sa.Column("doc_url", sa.String(length=512), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_component_catalog_component_type", "component_catalog", ["component_type"])

    # 2. Create apk_components_intel table
    op.create_table(
        "apk_components_intel",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("scan_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False),
        sa.Column("component_name", sa.String(length=512), nullable=False),
        sa.Column("component_type", sa.String(length=64), nullable=False),
        sa.Column("exported_status", sa.String(length=64), nullable=False),
        sa.Column("is_enabled", sa.Boolean(), nullable=False, server_default="true"),
        sa.Column("permission", sa.String(length=256), nullable=True),
        sa.Column("process_name", sa.String(length=256), nullable=False, server_default="'default'"),
        sa.Column("is_launcher", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column("is_foreground", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_apk_components_intel_scan_id", "apk_components_intel", ["scan_id"])
    op.create_index("ix_apk_components_intel_component_name", "apk_components_intel", ["component_name"])
    op.create_index("ix_apk_components_intel_component_type", "apk_components_intel", ["component_type"])
    op.create_index("ix_apk_components_intel_exported_status", "apk_components_intel", ["exported_status"])
    op.create_index("ix_apk_components_intel_process_name", "apk_components_intel", ["process_name"])

    # 3. Create component_intent_filters table (re-used name for full intelligence schema)
    op.create_table(
        "component_intent_filters_full",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("component_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("apk_components_intel.id", ondelete="CASCADE"), nullable=False),
        sa.Column("actions", postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column("categories", postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column("schemes", postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column("hosts", postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column("ports", postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column("paths", postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column("mime_types", postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column("priority", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("auto_verify", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column("is_deep_link", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_comp_intent_filters_full_comp_id", "component_intent_filters_full", ["component_id"])

    # 4. Create component_relationships table
    op.create_table(
        "component_relationships",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("scan_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False),
        sa.Column("parent_component", sa.String(length=512), nullable=False),
        sa.Column("child_component", sa.String(length=512), nullable=False),
        sa.Column("relationship_type", sa.String(length=64), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_component_relationships_scan_id", "component_relationships", ["scan_id"])

    # 5. Create component_processes table
    op.create_table(
        "component_processes",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("scan_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False),
        sa.Column("process_name", sa.String(length=256), nullable=False),
        sa.Column("process_type", sa.String(length=64), nullable=False, server_default="'DEFAULT'"),
        sa.Column("component_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_component_processes_scan_id", "component_processes", ["scan_id"])
    op.create_index("ix_component_processes_process_name", "component_processes", ["process_name"])


def downgrade() -> None:
    op.drop_index("ix_component_processes_process_name", table_name="component_processes")
    op.drop_index("ix_component_processes_scan_id", table_name="component_processes")
    op.drop_table("component_processes")

    op.drop_index("ix_component_relationships_scan_id", table_name="component_relationships")
    op.drop_table("component_relationships")

    op.drop_index("ix_comp_intent_filters_full_comp_id", table_name="component_intent_filters_full")
    op.drop_table("component_intent_filters_full")

    op.drop_index("ix_apk_components_intel_process_name", table_name="apk_components_intel")
    op.drop_index("ix_apk_components_intel_exported_status", table_name="apk_components_intel")
    op.drop_index("ix_apk_components_intel_component_type", table_name="apk_components_intel")
    op.drop_index("ix_apk_components_intel_component_name", table_name="apk_components_intel")
    op.drop_index("ix_apk_components_intel_scan_id", table_name="apk_components_intel")
    op.drop_table("apk_components_intel")

    op.drop_index("ix_component_catalog_component_type", table_name="component_catalog")
    op.drop_table("component_catalog")
