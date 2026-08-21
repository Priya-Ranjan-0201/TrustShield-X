"""Alembic Migration 018: Intent & Deep Link Intelligence Schema (Phase 3.7 Part 1A.10).

Creates tables:
- intent_catalog
- apk_intents
- apk_intent_actions
- apk_intent_categories
- apk_deep_links
- navigation_graph
with ON DELETE CASCADE foreign key constraints and performance indexes.

Revision ID: 018_intent_intelligence_schema
Revises: 017_component_intelligence_schema
Create Date: 2026-08-06
"""

from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = "018_intent_intelligence_schema"
down_revision: Union[str, None] = "017_component_intelligence_schema"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. Create intent_catalog table
    op.create_table(
        "intent_catalog",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("action_name", sa.String(length=256), nullable=False, unique=True),
        sa.Column("category", sa.String(length=64), nullable=False, server_default="'SYSTEM_BROADCAST'"),
        sa.Column("purpose", sa.Text(), nullable=True),
        sa.Column("is_system_only", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column("api_introduced", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("doc_url", sa.String(length=512), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_intent_catalog_action_name", "intent_catalog", ["action_name"])

    # 2. Create apk_intents table
    op.create_table(
        "apk_intents",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("scan_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False),
        sa.Column("component_name", sa.String(length=512), nullable=False),
        sa.Column("priority", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("auto_verify", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column("is_exported", sa.Boolean(), nullable=False, server_default="true"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_apk_intents_scan_id", "apk_intents", ["scan_id"])
    op.create_index("ix_apk_intents_component_name", "apk_intents", ["component_name"])

    # 3. Create apk_intent_actions table
    op.create_table(
        "apk_intent_actions",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("intent_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("apk_intents.id", ondelete="CASCADE"), nullable=False),
        sa.Column("action_name", sa.String(length=256), nullable=False),
        sa.Column("action_type", sa.String(length=64), nullable=False, server_default="'CUSTOM'"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_apk_intent_actions_intent_id", "apk_intent_actions", ["intent_id"])
    op.create_index("ix_apk_intent_actions_action_name", "apk_intent_actions", ["action_name"])

    # 4. Create apk_intent_categories table
    op.create_table(
        "apk_intent_categories",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("intent_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("apk_intents.id", ondelete="CASCADE"), nullable=False),
        sa.Column("category_name", sa.String(length=256), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_apk_intent_categories_intent_id", "apk_intent_categories", ["intent_id"])
    op.create_index("ix_apk_intent_categories_category_name", "apk_intent_categories", ["category_name"])

    # 5. Create apk_deep_links table
    op.create_table(
        "apk_deep_links",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("intent_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("apk_intents.id", ondelete="CASCADE"), nullable=False),
        sa.Column("scheme", sa.String(length=64), nullable=False),
        sa.Column("host", sa.String(length=256), nullable=True),
        sa.Column("port", sa.String(length=32), nullable=True),
        sa.Column("path", sa.String(length=512), nullable=True),
        sa.Column("mime_type", sa.String(length=128), nullable=True),
        sa.Column("is_app_link", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column("is_browsable", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_apk_deep_links_intent_id", "apk_deep_links", ["intent_id"])
    op.create_index("ix_apk_deep_links_scheme", "apk_deep_links", ["scheme"])
    op.create_index("ix_apk_deep_links_host", "apk_deep_links", ["host"])

    # 6. Create navigation_graph table
    op.create_table(
        "navigation_graph",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("scan_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False),
        sa.Column("source_component", sa.String(length=512), nullable=False),
        sa.Column("intent_action", sa.String(length=256), nullable=False),
        sa.Column("target_scheme", sa.String(length=64), nullable=True),
        sa.Column("target_host", sa.String(length=256), nullable=True),
        sa.Column("destination_component", sa.String(length=512), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_navigation_graph_scan_id", "navigation_graph", ["scan_id"])
    op.create_index("ix_navigation_graph_intent_action", "navigation_graph", ["intent_action"])


def downgrade() -> None:
    op.drop_index("ix_navigation_graph_intent_action", table_name="navigation_graph")
    op.drop_index("ix_navigation_graph_scan_id", table_name="navigation_graph")
    op.drop_table("navigation_graph")

    op.drop_index("ix_apk_deep_links_host", table_name="apk_deep_links")
    op.drop_index("ix_apk_deep_links_scheme", table_name="apk_deep_links")
    op.drop_index("ix_apk_deep_links_intent_id", table_name="apk_deep_links")
    op.drop_table("apk_deep_links")

    op.drop_index("ix_apk_intent_categories_category_name", table_name="apk_intent_categories")
    op.drop_index("ix_apk_intent_categories_intent_id", table_name="apk_intent_categories")
    op.drop_table("apk_intent_categories")

    op.drop_index("ix_apk_intent_actions_action_name", table_name="apk_intent_actions")
    op.drop_index("ix_apk_intent_actions_intent_id", table_name="apk_intent_actions")
    op.drop_table("apk_intent_actions")

    op.drop_index("ix_apk_intents_component_name", table_name="apk_intents")
    op.drop_index("ix_apk_intents_scan_id", table_name="apk_intents")
    op.drop_table("apk_intents")

    op.drop_index("ix_intent_catalog_action_name", table_name="intent_catalog")
    op.drop_table("intent_catalog")
