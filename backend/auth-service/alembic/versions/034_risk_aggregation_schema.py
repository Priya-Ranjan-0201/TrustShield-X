"""Alembic Migration 034: Enterprise Risk Aggregation Schema.

Revision ID: 034_risk_aggregation_schema
Revises: 033_evidence_consolidation_schema
Create Date: 2026-08-13
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '034_risk_aggregation_schema'
down_revision = '033_evidence_consolidation_schema'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'risk_assessments',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('scan_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('scan_history.id', ondelete='CASCADE'), nullable=False),
        sa.Column('assessment_id', sa.String(length=128), nullable=False),
        sa.Column('risk_score', sa.Float(), nullable=False),
        sa.Column('risk_band', sa.String(length=32), nullable=False),
        sa.Column('confidence_level', sa.String(length=32), nullable=False),
        sa.Column('evidence_sufficiency', sa.String(length=32), nullable=False),
        sa.Column('decision_state', sa.String(length=32), nullable=False),
        sa.Column('primary_risk_category', sa.String(length=64), nullable=False),
        sa.Column('risk_factor_count', sa.Integer(), nullable=False),
        sa.Column('supporting_finding_count', sa.Integer(), nullable=False),
        sa.Column('contradictory_finding_count', sa.Integer(), nullable=False),
        sa.Column('mitigating_factor_count', sa.Integer(), nullable=False),
        sa.Column('protective_factor_count', sa.Integer(), nullable=False),
        sa.Column('uncertainty_count', sa.Integer(), nullable=False),
        sa.Column('engine_version', sa.String(length=64), nullable=False),
        sa.Column('configuration_version', sa.String(length=64), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index('ix_risk_assessments_scan_id', 'risk_assessments', ['scan_id'])
    op.create_index('ix_risk_assessments_assessment_id', 'risk_assessments', ['assessment_id'])
    op.create_index('ix_risk_assessments_risk_score', 'risk_assessments', ['risk_score'])
    op.create_index('ix_risk_assessments_risk_band', 'risk_assessments', ['risk_band'])
    op.create_index('ix_risk_assessments_decision_state', 'risk_assessments', ['decision_state'])

    op.create_table(
        'risk_factors',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('scan_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('scan_history.id', ondelete='CASCADE'), nullable=False),
        sa.Column('factor_id', sa.String(length=128), nullable=False),
        sa.Column('category', sa.String(length=64), nullable=False),
        sa.Column('name', sa.String(length=256), nullable=False),
        sa.Column('description', sa.String(length=512), nullable=False),
        sa.Column('base_contribution', sa.Float(), nullable=False),
        sa.Column('final_contribution', sa.Float(), nullable=False),
        sa.Column('confidence', sa.String(length=32), nullable=False),
        sa.Column('evidence_sufficiency', sa.String(length=32), nullable=False),
        sa.Column('reason', sa.String(length=512), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index('ix_risk_factors_scan_id', 'risk_factors', ['scan_id'])

    op.create_table(
        'risk_category_scores',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('scan_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('scan_history.id', ondelete='CASCADE'), nullable=False),
        sa.Column('category', sa.String(length=64), nullable=False),
        sa.Column('raw_score', sa.Float(), nullable=False),
        sa.Column('normalized_score', sa.Float(), nullable=False),
        sa.Column('risk_band', sa.String(length=32), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    )

    op.create_table(
        'risk_contributions',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('scan_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('scan_history.id', ondelete='CASCADE'), nullable=False),
        sa.Column('finding_id', sa.String(length=128), nullable=False),
        sa.Column('category', sa.String(length=64), nullable=False),
        sa.Column('contribution_weight', sa.Float(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    )

    op.create_table(
        'risk_interactions',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('scan_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('scan_history.id', ondelete='CASCADE'), nullable=False),
        sa.Column('interaction_id', sa.String(length=128), nullable=False),
        sa.Column('factor_a_id', sa.String(length=128), nullable=False),
        sa.Column('factor_b_id', sa.String(length=128), nullable=False),
        sa.Column('amplification_bonus', sa.Float(), nullable=False),
        sa.Column('description', sa.String(length=256), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    )

    op.create_table(
        'risk_mitigations',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('scan_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('scan_history.id', ondelete='CASCADE'), nullable=False),
        sa.Column('mitigation_id', sa.String(length=128), nullable=False),
        sa.Column('description', sa.String(length=256), nullable=False),
        sa.Column('reduction_amount', sa.Float(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    )

    op.create_table(
        'risk_protective_factors',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('scan_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('scan_history.id', ondelete='CASCADE'), nullable=False),
        sa.Column('protective_id', sa.String(length=128), nullable=False),
        sa.Column('description', sa.String(length=256), nullable=False),
        sa.Column('reduction_amount', sa.Float(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    )

    op.create_table(
        'risk_contradictions',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('scan_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('scan_history.id', ondelete='CASCADE'), nullable=False),
        sa.Column('contradiction_id', sa.String(length=128), nullable=False),
        sa.Column('description', sa.String(length=256), nullable=False),
        sa.Column('uncertainty_penalty', sa.Float(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    )

    op.create_table(
        'risk_audit_records',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('scan_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('scan_history.id', ondelete='CASCADE'), nullable=False),
        sa.Column('audit_id', sa.String(length=128), nullable=False),
        sa.Column('policy_version', sa.String(length=64), nullable=False),
        sa.Column('configuration_checksum', sa.String(length=128), nullable=False),
        sa.Column('audit_trail_text', sa.String(length=1024), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    )

    op.create_table(
        'risk_policy_versions',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('policy_version', sa.String(length=64), nullable=False, unique=True),
        sa.Column('author', sa.String(length=128), nullable=False),
        sa.Column('description', sa.String(length=256), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    )

    op.create_table(
        'risk_policy_rules',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('policy_version', sa.String(length=64), nullable=False),
        sa.Column('rule_name', sa.String(length=128), nullable=False),
        sa.Column('weight', sa.Float(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    )

    op.create_table(
        'risk_decision_records',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('scan_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('scan_history.id', ondelete='CASCADE'), nullable=False),
        sa.Column('decision_id', sa.String(length=128), nullable=False),
        sa.Column('decision_state', sa.String(length=32), nullable=False),
        sa.Column('recommendation', sa.String(length=64), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    )

    op.create_table(
        'risk_metrics',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('scan_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('scan_history.id', ondelete='CASCADE'), nullable=False),
        sa.Column('assessments_evaluated', sa.Integer(), nullable=False),
        sa.Column('high_risk_assessments', sa.Integer(), nullable=False),
        sa.Column('critical_risk_assessments', sa.Integer(), nullable=False),
        sa.Column('insufficient_evidence_assessments', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    )


def downgrade():
    op.drop_table('risk_metrics')
    op.drop_table('risk_decision_records')
    op.drop_table('risk_policy_rules')
    op.drop_table('risk_policy_versions')
    op.drop_table('risk_audit_records')
    op.drop_table('risk_contradictions')
    op.drop_table('risk_protective_factors')
    op.drop_table('risk_mitigations')
    op.drop_table('risk_interactions')
    op.drop_table('risk_contributions')
    op.drop_table('risk_category_scores')
    op.drop_table('risk_factors')
    op.drop_table('risk_assessments')
