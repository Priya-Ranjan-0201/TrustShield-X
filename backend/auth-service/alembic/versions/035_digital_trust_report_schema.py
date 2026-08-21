"""Alembic Migration 035: Digital Trust Report Schema.

Revision ID: 035_digital_trust_report_schema
Revises: 034_risk_aggregation_schema
Create Date: 2026-08-13
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '035_digital_trust_report_schema'
down_revision = '034_risk_aggregation_schema'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'digital_trust_reports',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('scan_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('scan_history.id', ondelete='CASCADE'), nullable=False),
        sa.Column('report_id', sa.String(length=128), nullable=False),
        sa.Column('analysis_id', sa.String(length=128), nullable=False),
        sa.Column('report_version', sa.String(length=64), nullable=False),
        sa.Column('schema_version', sa.String(length=64), nullable=False),
        sa.Column('status', sa.String(length=32), nullable=False),
        sa.Column('report_type', sa.String(length=64), nullable=False),
        sa.Column('risk_score', sa.Float(), nullable=False),
        sa.Column('risk_band', sa.String(length=32), nullable=False),
        sa.Column('confidence', sa.String(length=32), nullable=False),
        sa.Column('evidence_sufficiency', sa.String(length=32), nullable=False),
        sa.Column('json_document', sa.Text(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index('ix_digital_trust_reports_scan_id', 'digital_trust_reports', ['scan_id'])
    op.create_index('ix_digital_trust_reports_report_id', 'digital_trust_reports', ['report_id'])
    op.create_index('ix_digital_trust_reports_analysis_id', 'digital_trust_reports', ['analysis_id'])
    op.create_index('ix_digital_trust_reports_status', 'digital_trust_reports', ['status'])

    op.create_table(
        'report_sections',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('report_id', sa.String(length=128), nullable=False),
        sa.Column('section_id', sa.String(length=128), nullable=False),
        sa.Column('title', sa.String(length=256), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index('ix_report_sections_report_id', 'report_sections', ['report_id'])

    op.create_table(
        'report_findings',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('report_id', sa.String(length=128), nullable=False),
        sa.Column('finding_id', sa.String(length=128), nullable=False),
        sa.Column('category', sa.String(length=64), nullable=False),
        sa.Column('title', sa.String(length=256), nullable=False),
        sa.Column('description', sa.String(length=512), nullable=False),
        sa.Column('confidence', sa.String(length=32), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index('ix_report_findings_report_id', 'report_findings', ['report_id'])

    op.create_table(
        'report_evidence',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('report_id', sa.String(length=128), nullable=False),
        sa.Column('card_id', sa.String(length=128), nullable=False),
        sa.Column('category', sa.String(length=64), nullable=False),
        sa.Column('title', sa.String(length=256), nullable=False),
        sa.Column('observation', sa.String(length=512), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    )

    op.create_table(
        'report_recommendations',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('report_id', sa.String(length=128), nullable=False),
        sa.Column('recommendation_text', sa.String(length=512), nullable=False),
        sa.Column('priority', sa.String(length=32), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    )

    op.create_table(
        'report_provenance',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('report_id', sa.String(length=128), nullable=False),
        sa.Column('statement_id', sa.String(length=128), nullable=False),
        sa.Column('source_module', sa.String(length=128), nullable=False),
        sa.Column('finding_id', sa.String(length=128), nullable=False),
        sa.Column('evidence_id', sa.String(length=128), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    )

    op.create_table(
        'report_lineage',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('report_id', sa.String(length=128), nullable=False),
        sa.Column('section_id', sa.String(length=128), nullable=False),
        sa.Column('statement_text', sa.String(length=512), nullable=False),
        sa.Column('finding_id', sa.String(length=128), nullable=False),
        sa.Column('evidence_id', sa.String(length=128), nullable=False),
        sa.Column('original_source', sa.String(length=128), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    )

    op.create_table(
        'report_versions',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('report_id', sa.String(length=128), nullable=False),
        sa.Column('report_version', sa.String(length=64), nullable=False),
        sa.Column('change_reason', sa.String(length=256), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    )

    op.create_table(
        'report_generation_runs',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('run_id', sa.String(length=128), nullable=False),
        sa.Column('analysis_id', sa.String(length=128), nullable=False),
        sa.Column('report_id', sa.String(length=128), nullable=False),
        sa.Column('duration_ms', sa.Integer(), nullable=False),
        sa.Column('status', sa.String(length=32), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    )

    op.create_table(
        'report_generation_errors',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('error_code', sa.String(length=64), nullable=False),
        sa.Column('analysis_id', sa.String(length=128), nullable=False),
        sa.Column('error_message', sa.String(length=1024), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    )

    op.create_table(
        'report_metrics',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('reports_generated_total', sa.Integer(), nullable=False),
        sa.Column('reports_failed_total', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    )


def downgrade():
    op.drop_table('report_metrics')
    op.drop_table('report_generation_errors')
    op.drop_table('report_generation_runs')
    op.drop_table('report_versions')
    op.drop_table('report_lineage')
    op.drop_table('report_provenance')
    op.drop_table('report_recommendations')
    op.drop_table('report_evidence')
    op.drop_table('report_findings')
    op.drop_table('report_sections')
    op.drop_table('digital_trust_reports')
