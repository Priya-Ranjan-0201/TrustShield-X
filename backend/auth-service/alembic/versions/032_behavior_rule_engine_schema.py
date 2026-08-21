"""Alembic Migration 032: Behavior Rule Engine Schema (Phase 3.9 Part 1A.24).

Creates 13 behavior rule engine tables:
behavior_rules, behavior_rule_versions, behavior_rule_packs, behavior_rule_dependencies,
behavior_rule_conditions, behavior_rule_evaluations, behavior_rule_condition_results,
behavior_rule_execution_traces, behavior_rule_evidence, behavior_rule_suppressions,
behavior_rule_exceptions, behavior_rule_conflicts, behavior_rule_metrics
with ON DELETE CASCADE foreign key constraints and performance indexes.

Revision ID: 032_behavior_rule_engine_schema
Revises: 031_threat_intelligence_schema
Create Date: 2026-08-12
"""

from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = "032_behavior_rule_engine_schema"
down_revision: Union[str, None] = "031_threat_intelligence_schema"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. behavior_rules
    op.create_table(
        "behavior_rules",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("scan_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False),
        sa.Column("rule_id", sa.String(length=128), nullable=False),
        sa.Column("rule_version", sa.String(length=64), nullable=False, server_default="'1.0.0'"),
        sa.Column("namespace", sa.String(length=64), nullable=False, server_default="'DATAFLOW'"),
        sa.Column("name", sa.String(length=256), nullable=False),
        sa.Column("description", sa.String(length=512), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False, server_default="'ACTIVE'"),
        sa.Column("severity_hint", sa.String(length=32), nullable=False, server_default="'HIGH'"),
        sa.Column("confidence_hint", sa.String(length=32), nullable=False, server_default="'HIGH'"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_behavior_rules_scan_id", "behavior_rules", ["scan_id"])
    op.create_index("ix_behavior_rules_rule_id", "behavior_rules", ["rule_id"])

    # 2. behavior_rule_versions
    op.create_table(
        "behavior_rule_versions",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("scan_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False),
        sa.Column("rule_id", sa.String(length=128), nullable=False),
        sa.Column("rule_version", sa.String(length=64), nullable=False, server_default="'1.0.0'"),
        sa.Column("author", sa.String(length=128), nullable=False, server_default="'TruthShield Core Team'"),
        sa.Column("status", sa.String(length=32), nullable=False, server_default="'ACTIVE'"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_behavior_rule_versions_scan_id", "behavior_rule_versions", ["scan_id"])

    # 3. behavior_rule_packs
    op.create_table(
        "behavior_rule_packs",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("scan_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False),
        sa.Column("pack_id", sa.String(length=128), nullable=False),
        sa.Column("pack_version", sa.String(length=64), nullable=False, server_default="'1.0.0'"),
        sa.Column("rules_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("checksum", sa.String(length=128), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_behavior_rule_packs_scan_id", "behavior_rule_packs", ["scan_id"])

    # 4. behavior_rule_dependencies
    op.create_table(
        "behavior_rule_dependencies",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("scan_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False),
        sa.Column("rule_id", sa.String(length=128), nullable=False),
        sa.Column("depends_on_rule_id", sa.String(length=128), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_behavior_rule_dependencies_scan_id", "behavior_rule_dependencies", ["scan_id"])

    # 5. behavior_rule_conditions
    op.create_table(
        "behavior_rule_conditions",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("scan_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False),
        sa.Column("rule_id", sa.String(length=128), nullable=False),
        sa.Column("condition_id", sa.String(length=128), nullable=False),
        sa.Column("condition_type", sa.String(length=64), nullable=False),
        sa.Column("expected", sa.String(length=256), nullable=False),
        sa.Column("operator", sa.String(length=32), nullable=False, server_default="'AND'"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_behavior_rule_conditions_scan_id", "behavior_rule_conditions", ["scan_id"])

    # 6. behavior_rule_evaluations
    op.create_table(
        "behavior_rule_evaluations",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("scan_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False),
        sa.Column("evaluation_id", sa.String(length=128), nullable=False),
        sa.Column("rule_id", sa.String(length=128), nullable=False),
        sa.Column("rule_version", sa.String(length=64), nullable=False, server_default="'1.0.0'"),
        sa.Column("namespace", sa.String(length=64), nullable=False),
        sa.Column("state", sa.String(length=32), nullable=False, server_default="'MATCHED'"),
        sa.Column("confidence", sa.String(length=32), nullable=False, server_default="'HIGH'"),
        sa.Column("evidence_provenance", sa.String(length=512), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_behavior_rule_evaluations_scan_id", "behavior_rule_evaluations", ["scan_id"])
    op.create_index("ix_behavior_rule_evaluations_state", "behavior_rule_evaluations", ["state"])

    # 7. behavior_rule_condition_results
    op.create_table(
        "behavior_rule_condition_results",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("scan_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False),
        sa.Column("rule_id", sa.String(length=128), nullable=False),
        sa.Column("condition_id", sa.String(length=128), nullable=False),
        sa.Column("condition_type", sa.String(length=64), nullable=False),
        sa.Column("expected", sa.String(length=256), nullable=False),
        sa.Column("actual", sa.String(length=256), nullable=False),
        sa.Column("matched", sa.Boolean(), nullable=False, server_default="true"),
        sa.Column("confidence", sa.String(length=32), nullable=False, server_default="'HIGH'"),
        sa.Column("reason", sa.String(length=512), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_behavior_rule_condition_results_scan_id", "behavior_rule_condition_results", ["scan_id"])

    # 8. behavior_rule_execution_traces
    op.create_table(
        "behavior_rule_execution_traces",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("scan_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False),
        sa.Column("trace_id", sa.String(length=128), nullable=False),
        sa.Column("rule_id", sa.String(length=128), nullable=False),
        sa.Column("rule_version", sa.String(length=64), nullable=False),
        sa.Column("duration_ms", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("final_state", sa.String(length=32), nullable=False, server_default="'MATCHED'"),
        sa.Column("confidence", sa.String(length=32), nullable=False, server_default="'HIGH'"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_behavior_rule_execution_traces_scan_id", "behavior_rule_execution_traces", ["scan_id"])

    # 9. behavior_rule_evidence
    op.create_table(
        "behavior_rule_evidence",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("scan_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False),
        sa.Column("evidence_id", sa.String(length=128), nullable=False),
        sa.Column("rule_id", sa.String(length=128), nullable=False),
        sa.Column("evidence_type", sa.String(length=64), nullable=False),
        sa.Column("source_module", sa.String(length=128), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_behavior_rule_evidence_scan_id", "behavior_rule_evidence", ["scan_id"])

    # 10. behavior_rule_suppressions
    op.create_table(
        "behavior_rule_suppressions",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("scan_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False),
        sa.Column("suppression_id", sa.String(length=128), nullable=False),
        sa.Column("rule_id", sa.String(length=128), nullable=False),
        sa.Column("reason", sa.String(length=512), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_behavior_rule_suppressions_scan_id", "behavior_rule_suppressions", ["scan_id"])

    # 11. behavior_rule_exceptions
    op.create_table(
        "behavior_rule_exceptions",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("scan_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False),
        sa.Column("exception_id", sa.String(length=128), nullable=False),
        sa.Column("rule_id", sa.String(length=128), nullable=False),
        sa.Column("scope", sa.String(length=256), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_behavior_rule_exceptions_scan_id", "behavior_rule_exceptions", ["scan_id"])

    # 12. behavior_rule_conflicts
    op.create_table(
        "behavior_rule_conflicts",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("scan_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False),
        sa.Column("conflict_id", sa.String(length=128), nullable=False),
        sa.Column("rule_a_id", sa.String(length=128), nullable=False),
        sa.Column("rule_b_id", sa.String(length=128), nullable=False),
        sa.Column("reason", sa.String(length=512), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_behavior_rule_conflicts_scan_id", "behavior_rule_conflicts", ["scan_id"])

    # 13. behavior_rule_metrics
    op.create_table(
        "behavior_rule_metrics",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("scan_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False),
        sa.Column("rules_loaded", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("rules_evaluated", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("rules_matched", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("rules_partially_matched", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("rules_not_evaluable", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("rules_suppressed", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("rules_conflicted", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_behavior_rule_metrics_scan_id", "behavior_rule_metrics", ["scan_id"])


def downgrade() -> None:
    for tbl in [
        "behavior_rule_metrics", "behavior_rule_conflicts", "behavior_rule_exceptions",
        "behavior_rule_suppressions", "behavior_rule_evidence", "behavior_rule_execution_traces",
        "behavior_rule_condition_results", "behavior_rule_evaluations", "behavior_rule_conditions",
        "behavior_rule_dependencies", "behavior_rule_packs", "behavior_rule_versions", "behavior_rules",
    ]:
        op.drop_index(f"ix_{tbl}_scan_id", table_name=tbl)
        op.drop_table(tbl)
