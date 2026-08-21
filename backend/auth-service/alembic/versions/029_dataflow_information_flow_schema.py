"""Alembic Migration 029: Dataflow & Information Flow Schema (Phase 3.9 Part 1A.21).

Creates 16 dataflow tables:
dataflow_nodes, dataflow_edges, dataflow_paths, dataflow_sources, dataflow_sinks,
dataflow_taint_labels, dataflow_transformations, dataflow_evidence, dataflow_confidence,
information_flow_graphs, source_sink_graphs, flow_boundaries, third_party_dataflows,
jni_dataflows, reflection_dataflows, intent_dataflows
with ON DELETE CASCADE foreign key constraints and performance indexes.

Revision ID: 029_dataflow_information_flow_schema
Revises: 028_data_filesystem_intelligence
Create Date: 2026-08-12
"""

from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = "029_dataflow_information_flow_schema"
down_revision: Union[str, None] = "028_data_filesystem_intelligence"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. dataflow_nodes
    op.create_table(
        "dataflow_nodes",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("scan_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False),
        sa.Column("node_id", sa.String(length=128), nullable=False),
        sa.Column("node_type", sa.String(length=64), nullable=False, server_default="'SOURCE'"),
        sa.Column("label", sa.String(length=256), nullable=False),
        sa.Column("class_name", sa.String(length=256), nullable=False),
        sa.Column("method_name", sa.String(length=256), nullable=False),
        sa.Column("instruction_offset", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("data_category", sa.String(length=64), nullable=False, server_default="'IDENTITY'"),
        sa.Column("confidence", sa.String(length=32), nullable=False, server_default="'HIGH'"),
        sa.Column("resolution_status", sa.String(length=32), nullable=False, server_default="'RESOLVED'"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_dataflow_nodes_scan_id", "dataflow_nodes", ["scan_id"])
    op.create_index("ix_dataflow_nodes_node_id", "dataflow_nodes", ["node_id"])

    # 2. dataflow_edges
    op.create_table(
        "dataflow_edges",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("scan_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False),
        sa.Column("source_node_id", sa.String(length=128), nullable=False),
        sa.Column("target_node_id", sa.String(length=128), nullable=False),
        sa.Column("edge_type", sa.String(length=64), nullable=False, server_default="'ASSIGN'"),
        sa.Column("caller_method", sa.String(length=512), nullable=False),
        sa.Column("instruction_offset", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("confidence", sa.String(length=32), nullable=False, server_default="'HIGH'"),
        sa.Column("resolution_status", sa.String(length=32), nullable=False, server_default="'RESOLVED'"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_dataflow_edges_scan_id", "dataflow_edges", ["scan_id"])
    op.create_index("ix_dataflow_edges_source_node_id", "dataflow_edges", ["source_node_id"])
    op.create_index("ix_dataflow_edges_target_node_id", "dataflow_edges", ["target_node_id"])

    # 3. dataflow_sources
    op.create_table(
        "dataflow_sources",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("scan_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False),
        sa.Column("source_id", sa.String(length=128), nullable=False),
        sa.Column("source_type", sa.String(length=64), nullable=False, server_default="'LOCATION_API'"),
        sa.Column("data_category", sa.String(length=64), nullable=False, server_default="'LOCATION'"),
        sa.Column("api_canonical_id", sa.String(length=512), nullable=False),
        sa.Column("source_class", sa.String(length=256), nullable=False),
        sa.Column("source_method", sa.String(length=256), nullable=False),
        sa.Column("confidence", sa.String(length=32), nullable=False, server_default="'HIGH'"),
        sa.Column("resolution_status", sa.String(length=32), nullable=False, server_default="'RESOLVED'"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_dataflow_sources_scan_id", "dataflow_sources", ["scan_id"])
    op.create_index("ix_dataflow_sources_source_id", "dataflow_sources", ["source_id"])

    # 4. dataflow_sinks
    op.create_table(
        "dataflow_sinks",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("scan_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False),
        sa.Column("sink_id", sa.String(length=128), nullable=False),
        sa.Column("sink_type", sa.String(length=64), nullable=False, server_default="'NETWORK_HTTP'"),
        sa.Column("target_identifier", sa.String(length=512), nullable=False),
        sa.Column("sink_class", sa.String(length=256), nullable=False),
        sa.Column("sink_method", sa.String(length=256), nullable=False),
        sa.Column("confidence", sa.String(length=32), nullable=False, server_default="'HIGH'"),
        sa.Column("resolution_status", sa.String(length=32), nullable=False, server_default="'RESOLVED'"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_dataflow_sinks_scan_id", "dataflow_sinks", ["scan_id"])
    op.create_index("ix_dataflow_sinks_sink_id", "dataflow_sinks", ["sink_id"])

    # 5. dataflow_paths
    op.create_table(
        "dataflow_paths",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("scan_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False),
        sa.Column("path_id", sa.String(length=128), nullable=False),
        sa.Column("source_id", sa.String(length=128), nullable=False),
        sa.Column("sink_id", sa.String(length=128), nullable=False),
        sa.Column("flow_classification", sa.String(length=64), nullable=False, server_default="'SOURCE_TO_NETWORK'"),
        sa.Column("confidence", sa.String(length=32), nullable=False, server_default="'HIGH'"),
        sa.Column("resolution_status", sa.String(length=32), nullable=False, server_default="'RESOLVED'"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_dataflow_paths_scan_id", "dataflow_paths", ["scan_id"])
    op.create_index("ix_dataflow_paths_path_id", "dataflow_paths", ["path_id"])

    # 6. dataflow_taint_labels
    op.create_table(
        "dataflow_taint_labels",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("scan_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False),
        sa.Column("node_id", sa.String(length=128), nullable=False),
        sa.Column("taint_label", sa.String(length=64), nullable=False, server_default="'TAINT_LOCATION'"),
        sa.Column("original_taint", sa.String(length=64), nullable=False, server_default="'LOCATION'"),
        sa.Column("is_sanitized", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_dataflow_taint_labels_scan_id", "dataflow_taint_labels", ["scan_id"])
    op.create_index("ix_dataflow_taint_labels_taint_label", "dataflow_taint_labels", ["taint_label"])

    # 7. dataflow_transformations
    op.create_table(
        "dataflow_transformations",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("scan_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False),
        sa.Column("caller_method", sa.String(length=512), nullable=False),
        sa.Column("transformation_type", sa.String(length=64), nullable=False, server_default="'SERIALIZATION'"),
        sa.Column("input_node_id", sa.String(length=128), nullable=False),
        sa.Column("output_node_id", sa.String(length=128), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_dataflow_transformations_scan_id", "dataflow_transformations", ["scan_id"])

    # 8. flow_boundaries
    op.create_table(
        "flow_boundaries",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("scan_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False),
        sa.Column("boundary_type", sa.String(length=64), nullable=False, server_default="'CRYPTOGRAPHIC_BOUNDARY'"),
        sa.Column("source_method", sa.String(length=512), nullable=False),
        sa.Column("target_method", sa.String(length=512), nullable=False),
        sa.Column("resolution_status", sa.String(length=32), nullable=False, server_default="'RESOLVED'"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_flow_boundaries_scan_id", "flow_boundaries", ["scan_id"])

    # 9. third_party_dataflows
    op.create_table(
        "third_party_dataflows",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("scan_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False),
        sa.Column("source_id", sa.String(length=128), nullable=False),
        sa.Column("sdk_name", sa.String(length=128), nullable=False),
        sa.Column("sdk_category", sa.String(length=64), nullable=False, server_default="'ANALYTICS'"),
        sa.Column("target_endpoint", sa.String(length=512), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_third_party_dataflows_scan_id", "third_party_dataflows", ["scan_id"])

    # 10. jni_dataflows
    op.create_table(
        "jni_dataflows",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("scan_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False),
        sa.Column("java_method", sa.String(length=256), nullable=False),
        sa.Column("native_symbol", sa.String(length=256), nullable=False),
        sa.Column("library_name", sa.String(length=128), nullable=False),
        sa.Column("direction", sa.String(length=32), nullable=False, server_default="'JAVA_TO_NATIVE'"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_jni_dataflows_scan_id", "jni_dataflows", ["scan_id"])

    # 11. reflection_dataflows
    op.create_table(
        "reflection_dataflows",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("scan_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False),
        sa.Column("caller_method", sa.String(length=512), nullable=False),
        sa.Column("reflection_target", sa.String(length=512), nullable=False),
        sa.Column("resolution_status", sa.String(length=32), nullable=False, server_default="'RESOLVED'"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_reflection_dataflows_scan_id", "reflection_dataflows", ["scan_id"])

    # 12. intent_dataflows
    op.create_table(
        "intent_dataflows",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("scan_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False),
        sa.Column("source_component", sa.String(length=256), nullable=False),
        sa.Column("target_component", sa.String(length=256), nullable=False),
        sa.Column("extra_key", sa.String(length=128), nullable=False),
        sa.Column("extra_type", sa.String(length=32), nullable=False, server_default="'STRING'"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_intent_dataflows_scan_id", "intent_dataflows", ["scan_id"])

    # 13. dataflow_evidence
    op.create_table(
        "dataflow_evidence",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("scan_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False),
        sa.Column("dex_id", sa.String(length=128), nullable=False),
        sa.Column("class_name", sa.String(length=256), nullable=False),
        sa.Column("method_name", sa.String(length=256), nullable=False),
        sa.Column("instruction_offset", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("evidence_type", sa.String(length=64), nullable=False, server_default="'SOURCE_TO_SINK_EDGE'"),
        sa.Column("raw_evidence", sa.String(length=1024), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_dataflow_evidence_scan_id", "dataflow_evidence", ["scan_id"])

    # 14. dataflow_confidence
    op.create_table(
        "dataflow_confidence",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("scan_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False),
        sa.Column("path_id", sa.String(length=128), nullable=False),
        sa.Column("confidence_score", sa.Float(), nullable=False, server_default="0.95"),
        sa.Column("confidence_level", sa.String(length=32), nullable=False, server_default="'HIGH'"),
        sa.Column("resolution_status", sa.String(length=32), nullable=False, server_default="'RESOLVED'"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_dataflow_confidence_scan_id", "dataflow_confidence", ["scan_id"])

    # 15. information_flow_graphs
    op.create_table(
        "information_flow_graphs",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("scan_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False),
        sa.Column("nodes_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("edges_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("sources_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("sinks_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_information_flow_graphs_scan_id", "information_flow_graphs", ["scan_id"])

    # 16. source_sink_graphs
    op.create_table(
        "source_sink_graphs",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("scan_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False),
        sa.Column("source_node", sa.String(length=128), nullable=False),
        sa.Column("sink_node", sa.String(length=128), nullable=False),
        sa.Column("path_length", sa.Integer(), nullable=False, server_default="2"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_source_sink_graphs_scan_id", "source_sink_graphs", ["scan_id"])


def downgrade() -> None:
    for tbl in [
        "source_sink_graphs", "information_flow_graphs", "dataflow_confidence",
        "dataflow_evidence", "intent_dataflows", "reflection_dataflows",
        "jni_dataflows", "third_party_dataflows", "flow_boundaries",
        "dataflow_transformations", "dataflow_taint_labels", "dataflow_paths",
        "dataflow_sinks", "dataflow_sources", "dataflow_edges", "dataflow_nodes",
    ]:
        op.drop_index(f"ix_{tbl}_scan_id", table_name=tbl)
        op.drop_table(tbl)
