"""Alembic Migration 024: API Intelligence Schema (Phase 3.7 Part 1A.16).

Creates tables:
- api_catalog
- api_capabilities
- api_usage
- api_frameworks
- api_statistics
- api_cross_reference
- library_inventory
- framework_inventory
with ON DELETE CASCADE foreign key constraints and performance indexes.

Revision ID: 024_api_intelligence
Revises: 023_program_graph
Create Date: 2026-08-06
"""

from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = "024_api_intelligence"
down_revision: Union[str, None] = "023_program_graph"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. Create api_catalog table
    op.create_table(
        "api_catalog",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("scan_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False),
        sa.Column("canonical_id", sa.String(length=512), nullable=False),
        sa.Column("package_name", sa.String(length=256), nullable=False),
        sa.Column("class_name", sa.String(length=256), nullable=False),
        sa.Column("method_name", sa.String(length=256), nullable=False),
        sa.Column("signature", sa.String(length=512), nullable=False),
        sa.Column("framework", sa.String(length=128), nullable=False, server_default="'ANDROID_SDK'"),
        sa.Column("min_sdk", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("deprecated", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_api_catalog_scan_id", "api_catalog", ["scan_id"])
    op.create_index("ix_api_catalog_canonical_id", "api_catalog", ["canonical_id"])

    # 2. Create api_capabilities table
    op.create_table(
        "api_capabilities",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("scan_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False),
        sa.Column("api_canonical_id", sa.String(length=512), nullable=False),
        sa.Column("capability", sa.String(length=64), nullable=False, server_default="'OTHERS'"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_api_capabilities_scan_id", "api_capabilities", ["scan_id"])
    op.create_index("ix_api_capabilities_api_canonical_id", "api_capabilities", ["api_canonical_id"])
    op.create_index("ix_api_capabilities_capability", "api_capabilities", ["capability"])

    # 3. Create api_usage table
    op.create_table(
        "api_usage",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("scan_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False),
        sa.Column("caller_method", sa.String(length=512), nullable=False),
        sa.Column("api_canonical_id", sa.String(length=512), nullable=False),
        sa.Column("offset", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_api_usage_scan_id", "api_usage", ["scan_id"])
    op.create_index("ix_api_usage_caller_method", "api_usage", ["caller_method"])
    op.create_index("ix_api_usage_api_canonical_id", "api_usage", ["api_canonical_id"])

    # 4. Create api_frameworks table
    op.create_table(
        "api_frameworks",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("scan_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False),
        sa.Column("framework_name", sa.String(length=128), nullable=False),
        sa.Column("version", sa.String(length=64), nullable=True),
        sa.Column("detected_by", sa.String(length=128), nullable=False, server_default="'PACKAGE_PREFIX'"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_api_frameworks_scan_id", "api_frameworks", ["scan_id"])

    # 5. Create api_statistics table
    op.create_table(
        "api_statistics",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("scan_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False),
        sa.Column("total_apis", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("unique_frameworks", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("most_used_capability", sa.String(length=64), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_api_statistics_scan_id", "api_statistics", ["scan_id"])

    # 6. Create api_cross_reference table
    op.create_table(
        "api_cross_reference",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("scan_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False),
        sa.Column("source_symbol", sa.String(length=512), nullable=False),
        sa.Column("api_canonical_id", sa.String(length=512), nullable=False),
        sa.Column("xref_type", sa.String(length=64), nullable=False, server_default="'INVOKE'"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_api_cross_reference_scan_id", "api_cross_reference", ["scan_id"])

    # 7. Create library_inventory table
    op.create_table(
        "library_inventory",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("scan_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False),
        sa.Column("library_name", sa.String(length=256), nullable=False),
        sa.Column("version", sa.String(length=64), nullable=True),
        sa.Column("package_prefix", sa.String(length=256), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_library_inventory_scan_id", "library_inventory", ["scan_id"])

    # 8. Create framework_inventory table
    op.create_table(
        "framework_inventory",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("scan_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False),
        sa.Column("framework_name", sa.String(length=256), nullable=False),
        sa.Column("version", sa.String(length=64), nullable=True),
        sa.Column("confidence", sa.Float(), nullable=False, server_default="1.0"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_framework_inventory_scan_id", "framework_inventory", ["scan_id"])


def downgrade() -> None:
    op.drop_index("ix_framework_inventory_scan_id", table_name="framework_inventory")
    op.drop_table("framework_inventory")

    op.drop_index("ix_library_inventory_scan_id", table_name="library_inventory")
    op.drop_table("library_inventory")

    op.drop_index("ix_api_cross_reference_scan_id", table_name="api_cross_reference")
    op.drop_table("api_cross_reference")

    op.drop_index("ix_api_statistics_scan_id", table_name="api_statistics")
    op.drop_table("api_statistics")

    op.drop_index("ix_api_frameworks_scan_id", table_name="api_frameworks")
    op.drop_table("api_frameworks")

    op.drop_index("ix_api_usage_api_canonical_id", table_name="api_usage")
    op.drop_index("ix_api_usage_caller_method", table_name="api_usage")
    op.drop_index("ix_api_usage_scan_id", table_name="api_usage")
    op.drop_table("api_usage")

    op.drop_index("ix_api_capabilities_capability", table_name="api_capabilities")
    op.drop_index("ix_api_capabilities_api_canonical_id", table_name="api_capabilities")
    op.drop_index("ix_api_capabilities_scan_id", table_name="api_capabilities")
    op.drop_table("api_capabilities")

    op.drop_index("ix_api_catalog_canonical_id", table_name="api_catalog")
    op.drop_index("ix_api_catalog_scan_id", table_name="api_catalog")
    op.drop_table("api_catalog")
