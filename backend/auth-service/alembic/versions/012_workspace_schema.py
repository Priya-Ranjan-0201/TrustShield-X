"""Alembic Migration 012: APK Workspace Extraction Schema (Phase 3.7 Part 1A.4).

Creates tables:
- apk_workspace
- workspace_files
- workspace_statistics
with ON DELETE CASCADE foreign key constraints and performance indexes.

Revision ID: 012_workspace_schema
Revises: 011_apk_infrastructure_schema
Create Date: 2026-08-06
"""

from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = "012_workspace_schema"
down_revision: Union[str, None] = "011_apk_infrastructure_schema"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. Create apk_workspace table
    op.create_table(
        "apk_workspace",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("workspace_id", sa.String(length=64), nullable=False, unique=True),
        sa.Column("scan_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False),
        sa.Column("apk_sha256", sa.String(length=64), nullable=False),
        sa.Column("workspace_path", sa.String(length=512), nullable=False),
        sa.Column("status", sa.String(length=64), nullable=False, server_default="READY_FOR_STATIC_ANALYSIS"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.create_index("ix_apk_workspace_workspace_id", "apk_workspace", ["workspace_id"], unique=True)
    op.create_index("ix_apk_workspace_scan_id", "apk_workspace", ["scan_id"])
    op.create_index("ix_apk_workspace_apk_sha256", "apk_workspace", ["apk_sha256"])

    # 2. Create workspace_files table
    op.create_table(
        "workspace_files",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("workspace_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("apk_workspace.id", ondelete="CASCADE"), nullable=False),
        sa.Column("relative_path", sa.String(length=512), nullable=False),
        sa.Column("mime_type", sa.String(length=128), nullable=False),
        sa.Column("sha256", sa.String(length=64), nullable=False),
        sa.Column("size", sa.Integer(), nullable=False),
        sa.Column("entropy", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("category", sa.String(length=64), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_workspace_files_workspace_id", "workspace_files", ["workspace_id"])
    op.create_index("ix_workspace_files_sha256", "workspace_files", ["sha256"])
    op.create_index("ix_workspace_files_category", "workspace_files", ["category"])

    # 3. Create workspace_statistics table
    op.create_table(
        "workspace_statistics",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("workspace_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("apk_workspace.id", ondelete="CASCADE"), nullable=False),
        sa.Column("file_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("directory_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("dex_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("library_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("asset_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("resource_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("binary_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("xml_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("certificate_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_workspace_statistics_workspace_id", "workspace_statistics", ["workspace_id"])


def downgrade() -> None:
    op.drop_index("ix_workspace_statistics_workspace_id", table_name="workspace_statistics")
    op.drop_table("workspace_statistics")

    op.drop_index("ix_workspace_files_category", table_name="workspace_files")
    op.drop_index("ix_workspace_files_sha256", table_name="workspace_files")
    op.drop_index("ix_workspace_files_workspace_id", table_name="workspace_files")
    op.drop_table("workspace_files")

    op.drop_index("ix_apk_workspace_apk_sha256", table_name="apk_workspace")
    op.drop_index("ix_apk_workspace_scan_id", table_name="apk_workspace")
    op.drop_index("ix_apk_workspace_workspace_id", table_name="apk_workspace")
    op.drop_table("apk_workspace")
