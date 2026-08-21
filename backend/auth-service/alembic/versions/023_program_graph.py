"""Alembic Migration 023: Program Graph Intelligence Schema (Phase 3.7 Part 1A.15).

Creates tables:
- cfg_nodes
- cfg_edges
- call_graph_nodes
- call_graph_edges
- method_xrefs
- loop_analysis
- dominators
- execution_paths
- scc_analysis
- graph_metrics
with ON DELETE CASCADE foreign key constraints and performance indexes.

Revision ID: 023_program_graph
Revises: 022_dex_instruction
Create Date: 2026-08-06
"""

from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = "023_program_graph"
down_revision: Union[str, None] = "022_dex_instruction"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. Create cfg_nodes table
    op.create_table(
        "cfg_nodes",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("scan_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False),
        sa.Column("method_name", sa.String(length=512), nullable=False),
        sa.Column("block_id", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("start_offset", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("end_offset", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("instruction_count", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("is_entry", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column("is_exit", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column("is_loop_header", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_cfg_nodes_scan_id", "cfg_nodes", ["scan_id"])
    op.create_index("ix_cfg_nodes_method_name", "cfg_nodes", ["method_name"])

    # 2. Create cfg_edges table
    op.create_table(
        "cfg_edges",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("scan_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False),
        sa.Column("method_name", sa.String(length=512), nullable=False),
        sa.Column("source_block_id", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("target_block_id", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("edge_type", sa.String(length=64), nullable=False, server_default="'FALLTHROUGH'"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_cfg_edges_scan_id", "cfg_edges", ["scan_id"])

    # 3. Create call_graph_nodes table
    op.create_table(
        "call_graph_nodes",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("scan_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False),
        sa.Column("method_name", sa.String(length=512), nullable=False),
        sa.Column("class_name", sa.String(length=512), nullable=False),
        sa.Column("is_reachable", sa.Boolean(), nullable=False, server_default="true"),
        sa.Column("in_degree", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("out_degree", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_call_graph_nodes_scan_id", "call_graph_nodes", ["scan_id"])
    op.create_index("ix_call_graph_nodes_method_name", "call_graph_nodes", ["method_name"])

    # 4. Create call_graph_edges table
    op.create_table(
        "call_graph_edges",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("scan_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False),
        sa.Column("caller_method", sa.String(length=512), nullable=False),
        sa.Column("callee_method", sa.String(length=512), nullable=False),
        sa.Column("invoke_type", sa.String(length=64), nullable=False, server_default="'INVOKE_VIRTUAL'"),
        sa.Column("offset", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_call_graph_edges_scan_id", "call_graph_edges", ["scan_id"])
    op.create_index("ix_call_graph_edges_caller_method", "call_graph_edges", ["caller_method"])
    op.create_index("ix_call_graph_edges_callee_method", "call_graph_edges", ["callee_method"])

    # 5. Create method_xrefs table
    op.create_table(
        "method_xrefs",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("scan_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False),
        sa.Column("source_symbol", sa.String(length=512), nullable=False),
        sa.Column("target_symbol", sa.String(length=512), nullable=False),
        sa.Column("xref_type", sa.String(length=64), nullable=False, server_default="'CALL'"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_method_xrefs_scan_id", "method_xrefs", ["scan_id"])

    # 6. Create loop_analysis table
    op.create_table(
        "loop_analysis",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("scan_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False),
        sa.Column("method_name", sa.String(length=512), nullable=False),
        sa.Column("header_block_id", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("loop_depth", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_loop_analysis_scan_id", "loop_analysis", ["scan_id"])

    # 7. Create dominators table
    op.create_table(
        "dominators",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("scan_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False),
        sa.Column("method_name", sa.String(length=512), nullable=False),
        sa.Column("block_id", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("idom_block_id", sa.Integer(), nullable=True),
        sa.Column("depth", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_dominators_scan_id", "dominators", ["scan_id"])

    # 8. Create execution_paths table
    op.create_table(
        "execution_paths",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("scan_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False),
        sa.Column("method_name", sa.String(length=512), nullable=False),
        sa.Column("path_length", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("branch_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("exit_type", sa.String(length=64), nullable=False, server_default="'RETURN'"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_execution_paths_scan_id", "execution_paths", ["scan_id"])

    # 9. Create scc_analysis table
    op.create_table(
        "scc_analysis",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("scan_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False),
        sa.Column("scc_id", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("node_count", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("is_recursive", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_scc_analysis_scan_id", "scc_analysis", ["scan_id"])

    # 10. Create graph_metrics table
    op.create_table(
        "graph_metrics",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("scan_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False),
        sa.Column("cfg_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("call_graph_nodes_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("call_graph_edges_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("cyclomatic_complexity", sa.Float(), nullable=False, server_default="1.0"),
        sa.Column("reachable_methods_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("reachability_percentage", sa.Float(), nullable=False, server_default="100.0"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_graph_metrics_scan_id", "graph_metrics", ["scan_id"])


def downgrade() -> None:
    op.drop_index("ix_graph_metrics_scan_id", table_name="graph_metrics")
    op.drop_table("graph_metrics")

    op.drop_index("ix_scc_analysis_scan_id", table_name="scc_analysis")
    op.drop_table("scc_analysis")

    op.drop_index("ix_execution_paths_scan_id", table_name="execution_paths")
    op.drop_table("execution_paths")

    op.drop_index("ix_dominators_scan_id", table_name="dominators")
    op.drop_table("dominators")

    op.drop_index("ix_loop_analysis_scan_id", table_name="loop_analysis")
    op.drop_table("loop_analysis")

    op.drop_index("ix_method_xrefs_scan_id", table_name="method_xrefs")
    op.drop_table("method_xrefs")

    op.drop_index("ix_call_graph_edges_callee_method", table_name="call_graph_edges")
    op.drop_index("ix_call_graph_edges_caller_method", table_name="call_graph_edges")
    op.drop_index("ix_call_graph_edges_scan_id", table_name="call_graph_edges")
    op.drop_table("call_graph_edges")

    op.drop_index("ix_call_graph_nodes_method_name", table_name="call_graph_nodes")
    op.drop_index("ix_call_graph_nodes_scan_id", table_name="call_graph_nodes")
    op.drop_table("call_graph_nodes")

    op.drop_index("ix_cfg_edges_scan_id", table_name="cfg_edges")
    op.drop_table("cfg_edges")

    op.drop_index("ix_cfg_nodes_method_name", table_name="cfg_nodes")
    op.drop_index("ix_cfg_nodes_scan_id", table_name="cfg_nodes")
    op.drop_table("cfg_nodes")
