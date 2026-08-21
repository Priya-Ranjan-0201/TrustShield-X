"""Alembic Migration 033: Enterprise Evidence Consolidation Schema.

Revision ID: 033_evidence_consolidation_schema
Revises: 032_behavior_rule_engine_schema
Create Date: 2026-08-12
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '033_evidence_consolidation_schema'
down_revision = '032_behavior_rule_engine_schema'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'canonical_entities',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('scan_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('scan_history.id', ondelete='CASCADE'), nullable=False),
        sa.Column('entity_id', sa.String(length=128), nullable=False),
        sa.Column('entity_type', sa.String(length=64), nullable=False),
        sa.Column('canonical_value', sa.String(length=512), nullable=False),
        sa.Column('display_name', sa.String(length=512), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index('ix_canonical_entities_scan_id', 'canonical_entities', ['scan_id'])
    op.create_index('ix_canonical_entities_entity_id', 'canonical_entities', ['entity_id'])

    op.create_table(
        'canonical_evidence',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('scan_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('scan_history.id', ondelete='CASCADE'), nullable=False),
        sa.Column('evidence_id', sa.String(length=128), nullable=False),
        sa.Column('canonical_entity_id', sa.String(length=128), nullable=False),
        sa.Column('source_module', sa.String(length=128), nullable=False),
        sa.Column('evidence_type', sa.String(length=64), nullable=False),
        sa.Column('evidence_subtype', sa.String(length=64), nullable=False),
        sa.Column('class_name', sa.String(length=256), nullable=True),
        sa.Column('method_name', sa.String(length=256), nullable=True),
        sa.Column('confidence', sa.String(length=32), nullable=False),
        sa.Column('resolution_status', sa.String(length=32), nullable=False),
        sa.Column('provenance_reference', sa.String(length=512), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index('ix_canonical_evidence_scan_id', 'canonical_evidence', ['scan_id'])
    op.create_index('ix_canonical_evidence_evidence_id', 'canonical_evidence', ['evidence_id'])

    op.create_table(
        'canonical_findings',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('scan_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('scan_history.id', ondelete='CASCADE'), nullable=False),
        sa.Column('finding_id', sa.String(length=128), nullable=False),
        sa.Column('finding_type', sa.String(length=128), nullable=False),
        sa.Column('finding_category', sa.String(length=64), nullable=False),
        sa.Column('title', sa.String(length=256), nullable=False),
        sa.Column('description', sa.String(length=512), nullable=False),
        sa.Column('status', sa.String(length=32), nullable=False),
        sa.Column('confidence_level', sa.String(length=32), nullable=False),
        sa.Column('evidence_strength', sa.String(length=32), nullable=False),
        sa.Column('resolution_status', sa.String(length=32), nullable=False),
        sa.Column('source_count', sa.Integer(), nullable=False),
        sa.Column('independent_source_count', sa.Integer(), nullable=False),
        sa.Column('evidence_count', sa.Integer(), nullable=False),
        sa.Column('direct_evidence_count', sa.Integer(), nullable=False),
        sa.Column('inferred_evidence_count', sa.Integer(), nullable=False),
        sa.Column('contradiction_count', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index('ix_canonical_findings_scan_id', 'canonical_findings', ['scan_id'])
    op.create_index('ix_canonical_findings_finding_id', 'canonical_findings', ['finding_id'])
    op.create_index('ix_canonical_findings_status', 'canonical_findings', ['status'])

    op.create_table(
        'evidence_relationships',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('scan_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('scan_history.id', ondelete='CASCADE'), nullable=False),
        sa.Column('source_evidence_id', sa.String(length=128), nullable=False),
        sa.Column('target_evidence_id', sa.String(length=128), nullable=False),
        sa.Column('relationship', sa.String(length=64), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    )

    op.create_table(
        'evidence_independence',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('scan_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('scan_history.id', ondelete='CASCADE'), nullable=False),
        sa.Column('evidence_id', sa.String(length=128), nullable=False),
        sa.Column('group_id', sa.String(length=128), nullable=False),
        sa.Column('independence_type', sa.String(length=64), nullable=False),
        sa.Column('source_provider', sa.String(length=128), nullable=False),
        sa.Column('is_independent', sa.Boolean(), nullable=False),
        sa.Column('reason', sa.String(length=256), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    )

    op.create_table(
        'evidence_groups',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('scan_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('scan_history.id', ondelete='CASCADE'), nullable=False),
        sa.Column('group_id', sa.String(length=128), nullable=False),
        sa.Column('group_name', sa.String(length=128), nullable=False),
        sa.Column('member_evidence_count', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    )

    op.create_table(
        'finding_conflicts',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('scan_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('scan_history.id', ondelete='CASCADE'), nullable=False),
        sa.Column('conflict_id', sa.String(length=128), nullable=False),
        sa.Column('finding_id', sa.String(length=128), nullable=False),
        sa.Column('evidence_a_id', sa.String(length=128), nullable=False),
        sa.Column('evidence_b_id', sa.String(length=128), nullable=False),
        sa.Column('conflict_type', sa.String(length=64), nullable=False),
        sa.Column('explanation', sa.String(length=512), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    )

    op.create_table(
        'finding_lineage',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('scan_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('scan_history.id', ondelete='CASCADE'), nullable=False),
        sa.Column('lineage_id', sa.String(length=128), nullable=False),
        sa.Column('finding_id', sa.String(length=128), nullable=False),
        sa.Column('parent_evidence_id', sa.String(length=128), nullable=False),
        sa.Column('transformation_step', sa.String(length=128), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    )

    op.create_table(
        'finding_versions',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('scan_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('scan_history.id', ondelete='CASCADE'), nullable=False),
        sa.Column('finding_id', sa.String(length=128), nullable=False),
        sa.Column('finding_version', sa.String(length=64), nullable=False),
        sa.Column('engine_version', sa.String(length=64), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    )

    op.create_table(
        'finding_sources',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('scan_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('scan_history.id', ondelete='CASCADE'), nullable=False),
        sa.Column('finding_id', sa.String(length=128), nullable=False),
        sa.Column('source_module', sa.String(length=128), nullable=False),
        sa.Column('source_reliability', sa.String(length=32), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    )

    op.create_table(
        'finding_statistics',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('scan_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('scan_history.id', ondelete='CASCADE'), nullable=False),
        sa.Column('total_canonical_findings', sa.Integer(), nullable=False),
        sa.Column('total_canonical_evidence', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    )

    op.create_table(
        'confidence_fusion_records',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('scan_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('scan_history.id', ondelete='CASCADE'), nullable=False),
        sa.Column('fusion_id', sa.String(length=128), nullable=False),
        sa.Column('finding_id', sa.String(length=128), nullable=False),
        sa.Column('fused_confidence', sa.String(length=32), nullable=False),
        sa.Column('confidence_ceiling_applied', sa.Boolean(), nullable=False),
        sa.Column('ceiling_reason', sa.String(length=512), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    )

    op.create_table(
        'evidence_provenance_graphs',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('scan_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('scan_history.id', ondelete='CASCADE'), nullable=False),
        sa.Column('nodes_count', sa.Integer(), nullable=False),
        sa.Column('edges_count', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    )

    op.create_table(
        'finding_graphs',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('scan_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('scan_history.id', ondelete='CASCADE'), nullable=False),
        sa.Column('nodes_count', sa.Integer(), nullable=False),
        sa.Column('edges_count', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    )

    op.create_table(
        'consolidation_runs',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('scan_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('scan_history.id', ondelete='CASCADE'), nullable=False),
        sa.Column('status', sa.String(length=32), nullable=False),
        sa.Column('duration_ms', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    )

    op.create_table(
        'consolidation_metrics',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('scan_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('scan_history.id', ondelete='CASCADE'), nullable=False),
        sa.Column('input_findings_count', sa.Integer(), nullable=False),
        sa.Column('canonical_entities_count', sa.Integer(), nullable=False),
        sa.Column('canonical_evidence_count', sa.Integer(), nullable=False),
        sa.Column('duplicate_evidence_suppressed', sa.Integer(), nullable=False),
        sa.Column('merged_findings_count', sa.Integer(), nullable=False),
        sa.Column('split_findings_count', sa.Integer(), nullable=False),
        sa.Column('conflicted_findings_count', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    )


def downgrade():
    op.drop_table('consolidation_metrics')
    op.drop_table('consolidation_runs')
    op.drop_table('finding_graphs')
    op.drop_table('evidence_provenance_graphs')
    op.drop_table('confidence_fusion_records')
    op.drop_table('finding_statistics')
    op.drop_table('finding_sources')
    op.drop_table('finding_versions')
    op.drop_table('finding_lineage')
    op.drop_table('finding_conflicts')
    op.drop_table('evidence_groups')
    op.drop_table('evidence_independence')
    op.drop_table('evidence_relationships')
    op.drop_table('canonical_findings')
    op.drop_table('canonical_evidence')
    op.drop_table('canonical_entities')
