"""Alembic Migration 030: Behavioral Correlation Schema (Phase 3.9 Part 1A.22).

Creates 11 behavior correlation tables:
behavior_entities, behavior_relationships, behavior_chains, behavior_findings, behavior_evidence,
behavior_conflicts, behavior_summaries, behavior_graphs, correlation_runs, correlation_metrics,
third_party_behaviors
with ON DELETE CASCADE foreign key constraints and performance indexes.

Revision ID: 030_behavioral_correlation_schema
Revises: 029_dataflow_information_flow_schema
Create Date: 2026-08-12
"""

from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = "030_behavioral_correlation_schema"
down_revision: Union[str, None] = "029_dataflow_information_flow_schema"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. behavior_entities
    op.create_table(
        "behavior_entities",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("scan_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False),
        sa.Column("entity_id", sa.String(length=128), nullable=False),
        sa.Column("entity_type", sa.String(length=64), nullable=False, server_default="'CLASS'"),
        sa.Column("canonical_name", sa.String(length=512), nullable=False),
        sa.Column("source_module", sa.String(length=128), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_behavior_entities_scan_id", "behavior_entities", ["scan_id"])
    op.create_index("ix_behavior_entities_entity_id", "behavior_entities", ["entity_id"])

    # 2. behavior_relationships
    op.create_table(
        "behavior_relationships",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("scan_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False),
        sa.Column("source_entity_id", sa.String(length=128), nullable=False),
        sa.Column("target_entity_id", sa.String(length=128), nullable=False),
        sa.Column("relationship_type", sa.String(length=64), nullable=False, server_default="'CALLS'"),
        sa.Column("confidence", sa.String(length=32), nullable=False, server_default="'HIGH'"),
        sa.Column("resolution_status", sa.String(length=32), nullable=False, server_default="'RESOLVED'"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_behavior_relationships_scan_id", "behavior_relationships", ["scan_id"])

    # 3. behavior_chains
    op.create_table(
        "behavior_chains",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("scan_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False),
        sa.Column("chain_id", sa.String(length=128), nullable=False),
        sa.Column("chain_type", sa.String(length=64), nullable=False, server_default="'MULTI_STAGE_DATA_FLOW'"),
        sa.Column("start_node", sa.String(length=256), nullable=False),
        sa.Column("end_node", sa.String(length=256), nullable=False),
        sa.Column("confidence", sa.String(length=32), nullable=False, server_default="'HIGH'"),
        sa.Column("resolution_status", sa.String(length=32), nullable=False, server_default="'RESOLVED'"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_behavior_chains_scan_id", "behavior_chains", ["scan_id"])

    # 4. behavior_findings
    op.create_table(
        "behavior_findings",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("scan_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False),
        sa.Column("finding_id", sa.String(length=128), nullable=False),
        sa.Column("finding_type", sa.String(length=128), nullable=False),
        sa.Column("category", sa.String(length=64), nullable=False, server_default="'DATA_TRANSMISSION'"),
        sa.Column("evidence_strength", sa.String(length=32), nullable=False, server_default="'DIRECT'"),
        sa.Column("confidence", sa.String(length=32), nullable=False, server_default="'HIGH'"),
        sa.Column("resolution_status", sa.String(length=32), nullable=False, server_default="'RESOLVED'"),
        sa.Column("summary", sa.String(length=1024), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_behavior_findings_scan_id", "behavior_findings", ["scan_id"])
    op.create_index("ix_behavior_findings_finding_type", "behavior_findings", ["finding_type"])

    # 5. behavior_evidence
    op.create_table(
        "behavior_evidence",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("scan_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False),
        sa.Column("evidence_id", sa.String(length=128), nullable=False),
        sa.Column("module", sa.String(length=128), nullable=False),
        sa.Column("entity_type", sa.String(length=64), nullable=False, server_default="'API'"),
        sa.Column("entity_id", sa.String(length=128), nullable=False),
        sa.Column("class_name", sa.String(length=256), nullable=False),
        sa.Column("method_name", sa.String(length=256), nullable=False),
        sa.Column("instruction_offset", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("source_location", sa.String(length=512), nullable=False),
        sa.Column("rule_id", sa.String(length=128), nullable=False),
        sa.Column("evidence_type", sa.String(length=64), nullable=False, server_default="'API_USAGE'"),
        sa.Column("confidence", sa.String(length=32), nullable=False, server_default="'HIGH'"),
        sa.Column("resolution_status", sa.String(length=32), nullable=False, server_default="'RESOLVED'"),
        sa.Column("provenance", sa.String(length=512), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_behavior_evidence_scan_id", "behavior_evidence", ["scan_id"])

    # 6. behavior_conflicts
    op.create_table(
        "behavior_conflicts",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("scan_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False),
        sa.Column("conflict_id", sa.String(length=128), nullable=False),
        sa.Column("conflict_type", sa.String(length=128), nullable=False, server_default="'CONTRADICTORY_CONFIGURATION'"),
        sa.Column("evidence_a", sa.String(length=512), nullable=False),
        sa.Column("evidence_b", sa.String(length=512), nullable=False),
        sa.Column("resolution_status", sa.String(length=32), nullable=False, server_default="'CONFLICTED'"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_behavior_conflicts_scan_id", "behavior_conflicts", ["scan_id"])

    # 7. behavior_summaries
    op.create_table(
        "behavior_summaries",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("scan_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False),
        sa.Column("title", sa.String(length=256), nullable=False),
        sa.Column("summary_text", sa.String(length=2048), nullable=False),
        sa.Column("findings_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_behavior_summaries_scan_id", "behavior_summaries", ["scan_id"])

    # 8. behavior_graphs
    op.create_table(
        "behavior_graphs",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("scan_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False),
        sa.Column("nodes_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("edges_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_behavior_graphs_scan_id", "behavior_graphs", ["scan_id"])

    # 9. correlation_runs
    op.create_table(
        "correlation_runs",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("scan_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False, server_default="'COMPLETED'"),
        sa.Column("duration_ms", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_correlation_runs_scan_id", "correlation_runs", ["scan_id"])

    # 10. correlation_metrics
    op.create_table(
        "correlation_metrics",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("scan_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False),
        sa.Column("entities_processed", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("relationships_processed", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("findings_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("chains_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("conflicts_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_correlation_metrics_scan_id", "correlation_metrics", ["scan_id"])

    # 11. third_party_behaviors
    op.create_table(
        "third_party_behaviors",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("scan_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False),
        sa.Column("sdk_name", sa.String(length=128), nullable=False),
        sa.Column("sdk_category", sa.String(length=64), nullable=False, server_default="'ANALYTICS'"),
        sa.Column("data_collected", sa.String(length=256), nullable=False),
        sa.Column("network_endpoint", sa.String(length=512), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_third_party_behaviors_scan_id", "third_party_behaviors", ["scan_id"])


def downgrade() -> None:
    for tbl in [
        "third_party_behaviors", "correlation_metrics", "correlation_runs",
        "behavior_graphs", "behavior_summaries", "behavior_conflicts",
        "behavior_evidence", "behavior_findings", "behavior_chains",
        "behavior_relationships", "behavior_entities",
    ]:
        op.drop_index(f"ix_{tbl}_scan_id", table_name=tbl)
        op.drop_table(tbl)
