"""Alembic Migration 025: Reflection & Dynamic Loading Schema (Phase 3.7 Part 1A.17).

Creates tables:
- reflection_calls
- reflection_targets
- dynamic_class_loading
- native_loading
- jni_registration
- hidden_api_usage
- reflection_graph
- dynamic_invocations
with ON DELETE CASCADE foreign key constraints and performance indexes.

Revision ID: 025_reflection_intelligence
Revises: 024_api_intelligence
Create Date: 2026-08-06
"""

from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = "025_reflection_intelligence"
down_revision: Union[str, None] = "024_api_intelligence"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. Create reflection_calls table
    op.create_table(
        "reflection_calls",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("scan_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False),
        sa.Column("caller_method", sa.String(length=512), nullable=False),
        sa.Column("reflection_api", sa.String(length=256), nullable=False),
        sa.Column("target_class", sa.String(length=256), nullable=True),
        sa.Column("target_member", sa.String(length=256), nullable=True),
        sa.Column("offset", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_reflection_calls_scan_id", "reflection_calls", ["scan_id"])
    op.create_index("ix_reflection_calls_caller_method", "reflection_calls", ["caller_method"])
    op.create_index("ix_reflection_calls_target_class", "reflection_calls", ["target_class"])

    # 2. Create reflection_targets table
    op.create_table(
        "reflection_targets",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("scan_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False),
        sa.Column("canonical_target", sa.String(length=512), nullable=False),
        sa.Column("target_type", sa.String(length=64), nullable=False, server_default="'CLASS'"),
        sa.Column("is_resolved", sa.Boolean(), nullable=False, server_default="true"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_reflection_targets_scan_id", "reflection_targets", ["scan_id"])

    # 3. Create dynamic_class_loading table
    op.create_table(
        "dynamic_class_loading",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("scan_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False),
        sa.Column("caller_method", sa.String(length=512), nullable=False),
        sa.Column("loader_type", sa.String(length=128), nullable=False),
        sa.Column("dex_path", sa.String(length=512), nullable=True),
        sa.Column("is_memory_only", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_dynamic_class_loading_scan_id", "dynamic_class_loading", ["scan_id"])
    op.create_index("ix_dynamic_class_loading_loader_type", "dynamic_class_loading", ["loader_type"])

    # 4. Create native_loading table
    op.create_table(
        "native_loading",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("scan_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False),
        sa.Column("caller_method", sa.String(length=512), nullable=False),
        sa.Column("library_name", sa.String(length=256), nullable=False),
        sa.Column("load_api", sa.String(length=128), nullable=False, server_default="'System.loadLibrary'"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_native_loading_scan_id", "native_loading", ["scan_id"])

    # 5. Create jni_registration table
    op.create_table(
        "jni_registration",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("scan_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False),
        sa.Column("native_method", sa.String(length=256), nullable=False),
        sa.Column("java_class", sa.String(length=256), nullable=False),
        sa.Column("symbol_name", sa.String(length=256), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_jni_registration_scan_id", "jni_registration", ["scan_id"])

    # 6. Create hidden_api_usage table
    op.create_table(
        "hidden_api_usage",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("scan_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False),
        sa.Column("api_signature", sa.String(length=512), nullable=False),
        sa.Column("access_mechanism", sa.String(length=64), nullable=False, server_default="'REFLECTION'"),
        sa.Column("restriction_level", sa.String(length=64), nullable=False, server_default="'GREYLIST'"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_hidden_api_usage_scan_id", "hidden_api_usage", ["scan_id"])

    # 7. Create reflection_graph table
    op.create_table(
        "reflection_graph",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("scan_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False),
        sa.Column("caller_method", sa.String(length=512), nullable=False),
        sa.Column("target_symbol", sa.String(length=512), nullable=False),
        sa.Column("invocation_type", sa.String(length=64), nullable=False, server_default="'REFLECTIVE_INVOKE'"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_reflection_graph_scan_id", "reflection_graph", ["scan_id"])

    # 8. Create dynamic_invocations table
    op.create_table(
        "dynamic_invocations",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("scan_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False),
        sa.Column("source_symbol", sa.String(length=512), nullable=False),
        sa.Column("resolved_target", sa.String(length=512), nullable=False),
        sa.Column("confidence", sa.Float(), nullable=False, server_default="1.0"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_dynamic_invocations_scan_id", "dynamic_invocations", ["scan_id"])


def downgrade() -> None:
    op.drop_index("ix_dynamic_invocations_scan_id", table_name="dynamic_invocations")
    op.drop_table("dynamic_invocations")

    op.drop_index("ix_reflection_graph_scan_id", table_name="reflection_graph")
    op.drop_table("reflection_graph")

    op.drop_index("ix_hidden_api_usage_scan_id", table_name="hidden_api_usage")
    op.drop_table("hidden_api_usage")

    op.drop_index("ix_jni_registration_scan_id", table_name="jni_registration")
    op.drop_table("jni_registration")

    op.drop_index("ix_native_loading_scan_id", table_name="native_loading")
    op.drop_table("native_loading")

    op.drop_index("ix_dynamic_class_loading_loader_type", table_name="dynamic_class_loading")
    op.drop_index("ix_dynamic_class_loading_scan_id", table_name="dynamic_class_loading")
    op.drop_table("dynamic_class_loading")

    op.drop_index("ix_reflection_targets_scan_id", table_name="reflection_targets")
    op.drop_table("reflection_targets")

    op.drop_index("ix_reflection_calls_target_class", table_name="reflection_calls")
    op.drop_index("ix_reflection_calls_caller_method", table_name="reflection_calls")
    op.drop_index("ix_reflection_calls_scan_id", table_name="reflection_calls")
    op.drop_table("reflection_calls")
