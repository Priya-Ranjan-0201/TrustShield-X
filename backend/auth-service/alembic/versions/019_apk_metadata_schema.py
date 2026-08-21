"""Alembic Migration 019: APK Metadata & Package Intelligence Schema (Phase 3.7 Part 1A.11).

Creates tables:
- apk_metadata_intel
- apk_versions
- apk_sdk_profiles
- apk_application_flags
- apk_resources_intel
with ON DELETE CASCADE foreign key constraints and performance indexes.

Revision ID: 019_apk_metadata_schema
Revises: 018_intent_intelligence_schema
Create Date: 2026-08-06
"""

from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = "019_apk_metadata_schema"
down_revision: Union[str, None] = "018_intent_intelligence_schema"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. Create apk_metadata_intel table
    op.create_table(
        "apk_metadata_intel",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("scan_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False),
        sa.Column("package_name", sa.String(length=256), nullable=False),
        sa.Column("app_label", sa.String(length=256), nullable=True),
        sa.Column("app_class", sa.String(length=512), nullable=True),
        sa.Column("version_name", sa.String(length=64), nullable=False, server_default="'1.0'"),
        sa.Column("version_code", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("target_sdk", sa.Integer(), nullable=False, server_default="33"),
        sa.Column("min_sdk", sa.Integer(), nullable=False, server_default="21"),
        sa.Column("compile_sdk", sa.Integer(), nullable=True),
        sa.Column("install_location", sa.String(length=64), nullable=False, server_default="'AUTO'"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_apk_metadata_intel_scan_id", "apk_metadata_intel", ["scan_id"])
    op.create_index("ix_apk_metadata_intel_package_name", "apk_metadata_intel", ["package_name"])
    op.create_index("ix_apk_metadata_intel_version_code", "apk_metadata_intel", ["version_code"])
    op.create_index("ix_apk_metadata_intel_target_sdk", "apk_metadata_intel", ["target_sdk"])
    op.create_index("ix_apk_metadata_intel_min_sdk", "apk_metadata_intel", ["min_sdk"])

    # 2. Create apk_versions table
    op.create_table(
        "apk_versions",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("scan_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False),
        sa.Column("version_name", sa.String(length=64), nullable=False),
        sa.Column("version_code", sa.Integer(), nullable=False),
        sa.Column("major", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("minor", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("patch", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("build", sa.Integer(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_apk_versions_scan_id", "apk_versions", ["scan_id"])

    # 3. Create apk_sdk_profiles table
    op.create_table(
        "apk_sdk_profiles",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("scan_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False),
        sa.Column("min_sdk", sa.Integer(), nullable=False, server_default="21"),
        sa.Column("target_sdk", sa.Integer(), nullable=False, server_default="33"),
        sa.Column("compile_sdk", sa.Integer(), nullable=True),
        sa.Column("max_sdk", sa.Integer(), nullable=True),
        sa.Column("platform_version", sa.String(length=64), nullable=False),
        sa.Column("generation_name", sa.String(length=128), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_apk_sdk_profiles_scan_id", "apk_sdk_profiles", ["scan_id"])

    # 4. Create apk_application_flags table
    op.create_table(
        "apk_application_flags",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("scan_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False),
        sa.Column("is_debuggable", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column("is_persistent", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column("is_test_only", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column("allow_backup", sa.Boolean(), nullable=False, server_default="true"),
        sa.Column("large_heap", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column("uses_cleartext", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column("supports_rtl", sa.Boolean(), nullable=False, server_default="true"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_apk_application_flags_scan_id", "apk_application_flags", ["scan_id"])

    # 5. Create apk_resources_intel table
    op.create_table(
        "apk_resources_intel",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("scan_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False),
        sa.Column("icon_ref", sa.String(length=256), nullable=True),
        sa.Column("round_icon_ref", sa.String(length=256), nullable=True),
        sa.Column("banner_ref", sa.String(length=256), nullable=True),
        sa.Column("logo_ref", sa.String(length=256), nullable=True),
        sa.Column("theme_ref", sa.String(length=256), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_apk_resources_intel_scan_id", "apk_resources_intel", ["scan_id"])


def downgrade() -> None:
    op.drop_index("ix_apk_resources_intel_scan_id", table_name="apk_resources_intel")
    op.drop_table("apk_resources_intel")

    op.drop_index("ix_apk_application_flags_scan_id", table_name="apk_application_flags")
    op.drop_table("apk_application_flags")

    op.drop_index("ix_apk_sdk_profiles_scan_id", table_name="apk_sdk_profiles")
    op.drop_table("apk_sdk_profiles")

    op.drop_index("ix_apk_versions_scan_id", table_name="apk_versions")
    op.drop_table("apk_versions")

    op.drop_index("ix_apk_metadata_intel_min_sdk", table_name="apk_metadata_intel")
    op.drop_index("ix_apk_metadata_intel_target_sdk", table_name="apk_metadata_intel")
    op.drop_index("ix_apk_metadata_intel_version_code", table_name="apk_metadata_intel")
    op.drop_index("ix_apk_metadata_intel_package_name", table_name="apk_metadata_intel")
    op.drop_index("ix_apk_metadata_intel_scan_id", table_name="apk_metadata_intel")
    op.drop_table("apk_metadata_intel")
