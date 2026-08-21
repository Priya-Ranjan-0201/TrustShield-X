"""Alembic Migration 013: AndroidManifest Intelligence Schema (Phase 3.7 Part 1A.5).

Creates tables:
- apk_manifest
- apk_components
- apk_intent_filters
- apk_features
- apk_libraries
with ON DELETE CASCADE foreign key constraints and performance indexes.

Revision ID: 013_manifest_intelligence_schema
Revises: 012_workspace_schema
Create Date: 2026-08-06
"""

from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = "013_manifest_intelligence_schema"
down_revision: Union[str, None] = "012_workspace_schema"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. Create apk_manifest table
    op.create_table(
        "apk_manifest",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("scan_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False),
        sa.Column("package_name", sa.String(length=256), nullable=False),
        sa.Column("version_name", sa.String(length=128), nullable=True),
        sa.Column("version_code", sa.Integer(), nullable=True),
        sa.Column("min_sdk", sa.Integer(), nullable=True),
        sa.Column("target_sdk", sa.Integer(), nullable=True),
        sa.Column("compile_sdk", sa.Integer(), nullable=True),
        sa.Column("sdk_category", sa.String(length=32), nullable=False, server_default="UNKNOWN"),
        sa.Column("shared_user_id", sa.String(length=128), nullable=True),
        sa.Column("application_label", sa.String(length=256), nullable=True),
        sa.Column("debuggable", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column("allow_backup", sa.Boolean(), nullable=False, server_default="true"),
        sa.Column("uses_cleartext_traffic", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_apk_manifest_scan_id", "apk_manifest", ["scan_id"])
    op.create_index("ix_apk_manifest_package_name", "apk_manifest", ["package_name"])

    # 2. Create apk_components table
    op.create_table(
        "apk_components",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("manifest_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("apk_manifest.id", ondelete="CASCADE"), nullable=False),
        sa.Column("component_name", sa.String(length=512), nullable=False),
        sa.Column("component_type", sa.String(length=32), nullable=False),
        sa.Column("exported", sa.Boolean(), nullable=True),
        sa.Column("enabled", sa.Boolean(), nullable=False, server_default="true"),
        sa.Column("permission", sa.String(length=256), nullable=True),
        sa.Column("process", sa.String(length=128), nullable=True),
        sa.Column("launch_mode", sa.String(length=64), nullable=True),
        sa.Column("authorities", sa.String(length=512), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_apk_components_manifest_id", "apk_components", ["manifest_id"])
    op.create_index("ix_apk_components_component_name", "apk_components", ["component_name"])
    op.create_index("ix_apk_components_permission", "apk_components", ["permission"])

    # 3. Create apk_intent_filters table
    op.create_table(
        "apk_intent_filters",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("component_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("apk_components.id", ondelete="CASCADE"), nullable=False),
        sa.Column("actions", postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column("categories", postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column("schemes", postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column("hosts", postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column("mime_types", postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column("priority", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_apk_intent_filters_component_id", "apk_intent_filters", ["component_id"])

    # 4. Create apk_features table
    op.create_table(
        "apk_features",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("manifest_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("apk_manifest.id", ondelete="CASCADE"), nullable=False),
        sa.Column("feature_name", sa.String(length=256), nullable=False),
        sa.Column("required", sa.Boolean(), nullable=False, server_default="true"),
        sa.Column("gl_version", sa.String(length=64), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_apk_features_manifest_id", "apk_features", ["manifest_id"])

    # 5. Create apk_libraries table
    op.create_table(
        "apk_libraries",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("manifest_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("apk_manifest.id", ondelete="CASCADE"), nullable=False),
        sa.Column("library_name", sa.String(length=256), nullable=False),
        sa.Column("required", sa.Boolean(), nullable=False, server_default="true"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_apk_libraries_manifest_id", "apk_libraries", ["manifest_id"])


def downgrade() -> None:
    op.drop_index("ix_apk_libraries_manifest_id", table_name="apk_libraries")
    op.drop_table("apk_libraries")

    op.drop_index("ix_apk_features_manifest_id", table_name="apk_features")
    op.drop_table("apk_features")

    op.drop_index("ix_apk_intent_filters_component_id", table_name="apk_intent_filters")
    op.drop_table("apk_intent_filters")

    op.drop_index("ix_apk_components_permission", table_name="apk_components")
    op.drop_index("ix_apk_components_component_name", table_name="apk_components")
    op.drop_index("ix_apk_components_manifest_id", table_name="apk_components")
    op.drop_table("apk_components")

    op.drop_index("ix_apk_manifest_package_name", table_name="apk_manifest")
    op.drop_index("ix_apk_manifest_scan_id", table_name="apk_manifest")
    op.drop_table("apk_manifest")
