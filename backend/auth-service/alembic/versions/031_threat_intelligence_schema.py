"""Alembic Migration 031: Threat Intelligence Schema (Phase 3.9 Part 1A.23).

Creates 17 threat intelligence tables:
threat_indicators, threat_sources, threat_feeds, threat_feed_records, threat_matches,
threat_relationships, threat_entities, threat_conflicts, threat_evidence, threat_behavior_correlations,
threat_dataflow_correlations, threat_sync_runs, threat_sync_metrics, threat_graphs, yara_matches,
stix_objects, taxii_collections
with ON DELETE CASCADE foreign key constraints and performance indexes.

Revision ID: 031_threat_intelligence_schema
Revises: 030_behavioral_correlation_schema
Create Date: 2026-08-12
"""

from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = "031_threat_intelligence_schema"
down_revision: Union[str, None] = "030_behavioral_correlation_schema"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. threat_indicators
    op.create_table(
        "threat_indicators",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("scan_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False),
        sa.Column("indicator_id", sa.String(length=128), nullable=False),
        sa.Column("indicator_type", sa.String(length=64), nullable=False, server_default="'DOMAIN'"),
        sa.Column("normalized_value", sa.String(length=512), nullable=False),
        sa.Column("display_value", sa.String(length=512), nullable=False),
        sa.Column("value_hash", sa.String(length=128), nullable=False),
        sa.Column("source_module", sa.String(length=128), nullable=False),
        sa.Column("source_location", sa.String(length=512), nullable=False),
        sa.Column("resolution_status", sa.String(length=32), nullable=False, server_default="'RESOLVED'"),
        sa.Column("confidence", sa.String(length=32), nullable=False, server_default="'HIGH'"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_threat_indicators_scan_id", "threat_indicators", ["scan_id"])
    op.create_index("ix_threat_indicators_indicator_id", "threat_indicators", ["indicator_id"])
    op.create_index("ix_threat_indicators_normalized_value", "threat_indicators", ["normalized_value"])

    # 2. threat_sources
    op.create_table(
        "threat_sources",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("scan_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False),
        sa.Column("source_id", sa.String(length=128), nullable=False),
        sa.Column("provider", sa.String(length=256), nullable=False),
        sa.Column("source_type", sa.String(length=64), nullable=False, server_default="'OFFLINE_FEED'"),
        sa.Column("reliability", sa.String(length=32), nullable=False, server_default="'HIGH'"),
        sa.Column("version", sa.String(length=64), nullable=False, server_default="'1.0'"),
        sa.Column("status", sa.String(length=32), nullable=False, server_default="'ACTIVE'"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_threat_sources_scan_id", "threat_sources", ["scan_id"])

    # 3. threat_feeds
    op.create_table(
        "threat_feeds",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("scan_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False),
        sa.Column("feed_id", sa.String(length=128), nullable=False),
        sa.Column("feed_name", sa.String(length=256), nullable=False),
        sa.Column("provider", sa.String(length=256), nullable=False),
        sa.Column("version", sa.String(length=64), nullable=False, server_default="'1.0.0'"),
        sa.Column("record_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("freshness_state", sa.String(length=32), nullable=False, server_default="'CURRENT'"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_threat_feeds_scan_id", "threat_feeds", ["scan_id"])

    # 4. threat_feed_records
    op.create_table(
        "threat_feed_records",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("scan_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False),
        sa.Column("feed_id", sa.String(length=128), nullable=False),
        sa.Column("indicator_value", sa.String(length=512), nullable=False),
        sa.Column("reputation", sa.String(length=64), nullable=False, server_default="'SUSPICIOUS'"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_threat_feed_records_scan_id", "threat_feed_records", ["scan_id"])

    # 5. threat_matches
    op.create_table(
        "threat_matches",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("scan_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False),
        sa.Column("match_id", sa.String(length=128), nullable=False),
        sa.Column("indicator_id", sa.String(length=128), nullable=False),
        sa.Column("source_id", sa.String(length=128), nullable=False),
        sa.Column("match_type", sa.String(length=64), nullable=False, server_default="'EXACT_MATCH'"),
        sa.Column("reputation", sa.String(length=64), nullable=False, server_default="'SUSPICIOUS_REPORTED'"),
        sa.Column("confidence", sa.String(length=32), nullable=False, server_default="'HIGH'"),
        sa.Column("freshness_state", sa.String(length=32), nullable=False, server_default="'CURRENT'"),
        sa.Column("provenance", sa.String(length=512), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_threat_matches_scan_id", "threat_matches", ["scan_id"])

    # 6. threat_relationships
    op.create_table(
        "threat_relationships",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("scan_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False),
        sa.Column("source_entity_id", sa.String(length=128), nullable=False),
        sa.Column("target_entity_id", sa.String(length=128), nullable=False),
        sa.Column("relationship", sa.String(length=64), nullable=False, server_default="'ASSOCIATED_WITH'"),
        sa.Column("confidence", sa.String(length=32), nullable=False, server_default="'HIGH'"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_threat_relationships_scan_id", "threat_relationships", ["scan_id"])

    # 7. threat_entities
    op.create_table(
        "threat_entities",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("scan_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False),
        sa.Column("entity_id", sa.String(length=128), nullable=False),
        sa.Column("entity_type", sa.String(length=64), nullable=False, server_default="'INDICATOR'"),
        sa.Column("name", sa.String(length=256), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_threat_entities_scan_id", "threat_entities", ["scan_id"])

    # 8. threat_conflicts
    op.create_table(
        "threat_conflicts",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("scan_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False),
        sa.Column("conflict_id", sa.String(length=128), nullable=False),
        sa.Column("indicator_value", sa.String(length=512), nullable=False),
        sa.Column("source_a_claim", sa.String(length=256), nullable=False),
        sa.Column("source_b_claim", sa.String(length=256), nullable=False),
        sa.Column("resolution_status", sa.String(length=32), nullable=False, server_default="'CONFLICTED'"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_threat_conflicts_scan_id", "threat_conflicts", ["scan_id"])

    # 9. threat_evidence
    op.create_table(
        "threat_evidence",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("scan_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False),
        sa.Column("evidence_id", sa.String(length=128), nullable=False),
        sa.Column("indicator_id", sa.String(length=128), nullable=False),
        sa.Column("matched_rule_or_feed", sa.String(length=256), nullable=False),
        sa.Column("provenance", sa.String(length=512), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_threat_evidence_scan_id", "threat_evidence", ["scan_id"])

    # 10. threat_behavior_correlations
    op.create_table(
        "threat_behavior_correlations",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("scan_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False),
        sa.Column("correlation_id", sa.String(length=128), nullable=False),
        sa.Column("behavior_type", sa.String(length=128), nullable=False),
        sa.Column("indicator_value", sa.String(length=512), nullable=False),
        sa.Column("threat_claim", sa.String(length=256), nullable=False),
        sa.Column("confidence", sa.String(length=32), nullable=False, server_default="'HIGH'"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_threat_behavior_correlations_scan_id", "threat_behavior_correlations", ["scan_id"])

    # 11. threat_dataflow_correlations
    op.create_table(
        "threat_dataflow_correlations",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("scan_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False),
        sa.Column("correlation_id", sa.String(length=128), nullable=False),
        sa.Column("dataflow_path_id", sa.String(length=128), nullable=False),
        sa.Column("endpoint_url", sa.String(length=512), nullable=False),
        sa.Column("threat_claim", sa.String(length=256), nullable=False),
        sa.Column("confidence", sa.String(length=32), nullable=False, server_default="'HIGH'"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_threat_dataflow_correlations_scan_id", "threat_dataflow_correlations", ["scan_id"])

    # 12. threat_sync_runs
    op.create_table(
        "threat_sync_runs",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("scan_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False, server_default="'COMPLETED'"),
        sa.Column("duration_ms", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_threat_sync_runs_scan_id", "threat_sync_runs", ["scan_id"])

    # 13. threat_sync_metrics
    op.create_table(
        "threat_sync_metrics",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("scan_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False),
        sa.Column("indicators_processed", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("matches_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("conflicts_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("expired_indicators_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_threat_sync_metrics_scan_id", "threat_sync_metrics", ["scan_id"])

    # 14. threat_graphs
    op.create_table(
        "threat_graphs",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("scan_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False),
        sa.Column("nodes_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("edges_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_threat_graphs_scan_id", "threat_graphs", ["scan_id"])

    # 15. yara_matches
    op.create_table(
        "yara_matches",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("scan_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False),
        sa.Column("rule_name", sa.String(length=128), nullable=False),
        sa.Column("rule_namespace", sa.String(length=128), nullable=False, server_default="'default'"),
        sa.Column("matched_file", sa.String(length=256), nullable=False),
        sa.Column("offset", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("match_confidence", sa.String(length=32), nullable=False, server_default="'HIGH'"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_yara_matches_scan_id", "yara_matches", ["scan_id"])

    # 16. stix_objects
    op.create_table(
        "stix_objects",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("scan_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False),
        sa.Column("object_id", sa.String(length=128), nullable=False),
        sa.Column("object_type", sa.String(length=64), nullable=False, server_default="'indicator'"),
        sa.Column("name", sa.String(length=256), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_stix_objects_scan_id", "stix_objects", ["scan_id"])

    # 17. taxii_collections
    op.create_table(
        "taxii_collections",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("scan_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False),
        sa.Column("collection_id", sa.String(length=128), nullable=False),
        sa.Column("title", sa.String(length=256), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_taxii_collections_scan_id", "taxii_collections", ["scan_id"])


def downgrade() -> None:
    for tbl in [
        "taxii_collections", "stix_objects", "yara_matches", "threat_graphs",
        "threat_sync_metrics", "threat_sync_runs", "threat_dataflow_correlations",
        "threat_behavior_correlations", "threat_evidence", "threat_conflicts",
        "threat_entities", "threat_relationships", "threat_matches", "threat_feed_records",
        "threat_feeds", "threat_sources", "threat_indicators",
    ]:
        op.drop_index(f"ix_{tbl}_scan_id", table_name=tbl)
        op.drop_table(tbl)
