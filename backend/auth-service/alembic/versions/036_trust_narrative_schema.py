"""Alembic Migration 036: Trust Narrative Schema.

Revision ID: 036_trust_narrative_schema
Revises: 035_digital_trust_report_schema
Create Date: 2026-08-14
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = '036_trust_narrative_schema'
down_revision = '035_digital_trust_report_schema'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'trust_narratives',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('narrative_id', sa.String(128), nullable=False),
        sa.Column('report_id', sa.String(128), nullable=False),
        sa.Column('analysis_id', sa.String(128), nullable=False),
        sa.Column('schema_version', sa.String(64), nullable=False),
        sa.Column('template_version', sa.String(64), nullable=False),
        sa.Column('language', sa.String(16), nullable=False),
        sa.Column('mode', sa.String(32), nullable=False),
        sa.Column('status', sa.String(32), nullable=False),
        sa.Column('json_document', sa.Text(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index('ix_trust_narratives_narrative_id', 'trust_narratives', ['narrative_id'])
    op.create_index('ix_trust_narratives_report_id', 'trust_narratives', ['report_id'])
    op.create_index('ix_trust_narratives_status', 'trust_narratives', ['status'])

    op.create_table(
        'narrative_sections',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('narrative_id', sa.String(128), nullable=False),
        sa.Column('section_id', sa.String(128), nullable=False),
        sa.Column('title', sa.String(256), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index('ix_narrative_sections_narrative_id', 'narrative_sections', ['narrative_id'])

    op.create_table(
        'narrative_statements',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('narrative_id', sa.String(128), nullable=False),
        sa.Column('statement_id', sa.String(128), nullable=False),
        sa.Column('statement_type', sa.String(64), nullable=False),
        sa.Column('source_type', sa.String(64), nullable=False),
        sa.Column('source_id', sa.String(128), nullable=False),
        sa.Column('claim', sa.Text(), nullable=False),
        sa.Column('claim_strength', sa.String(32), nullable=False),
        sa.Column('confidence', sa.String(32), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index('ix_narrative_statements_narrative_id', 'narrative_statements', ['narrative_id'])

    op.create_table(
        'narrative_lineage',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('narrative_id', sa.String(128), nullable=False),
        sa.Column('statement_id', sa.String(128), nullable=False),
        sa.Column('report_id', sa.String(128), nullable=False),
        sa.Column('section_id', sa.String(128), nullable=False),
        sa.Column('source_type', sa.String(64), nullable=False),
        sa.Column('source_id', sa.String(128), nullable=False),
        sa.Column('finding_id', sa.String(128), nullable=False),
        sa.Column('evidence_id', sa.String(128), nullable=False),
        sa.Column('risk_factor_id', sa.String(128), nullable=False),
        sa.Column('generated_by', sa.String(128), nullable=False),
        sa.Column('template_version', sa.String(64), nullable=False),
        sa.Column('language', sa.String(16), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    )

    op.create_table('narrative_versions',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('narrative_id', sa.String(128), nullable=False),
        sa.Column('schema_version', sa.String(64), nullable=False),
        sa.Column('template_version', sa.String(64), nullable=False),
        sa.Column('language_version', sa.String(64), nullable=False),
        sa.Column('change_reason', sa.String(256), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    )

    op.create_table('narrative_templates',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('template_id', sa.String(128), nullable=False),
        sa.Column('template_type', sa.String(64), nullable=False),
        sa.Column('template_content', sa.Text(), nullable=False),
        sa.Column('language', sa.String(16), nullable=False),
        sa.Column('version', sa.String(64), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    )

    op.create_table('narrative_validation_results',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('narrative_id', sa.String(128), nullable=False),
        sa.Column('validation_id', sa.String(128), nullable=False),
        sa.Column('passed', sa.Boolean(), nullable=False),
        sa.Column('checks_performed', sa.Integer(), nullable=False),
        sa.Column('checks_passed', sa.Integer(), nullable=False),
        sa.Column('checks_failed', sa.Integer(), nullable=False),
        sa.Column('failure_details', sa.Text(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    )

    op.create_table('narrative_generation_runs',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('run_id', sa.String(128), nullable=False),
        sa.Column('narrative_id', sa.String(128), nullable=False),
        sa.Column('analysis_id', sa.String(128), nullable=False),
        sa.Column('duration_ms', sa.Integer(), nullable=False),
        sa.Column('status', sa.String(32), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    )

    op.create_table('narrative_generation_errors',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('error_code', sa.String(64), nullable=False),
        sa.Column('narrative_id', sa.String(128), nullable=False),
        sa.Column('error_message', sa.String(1024), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    )

    op.create_table('narrative_translation_records',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('narrative_id', sa.String(128), nullable=False),
        sa.Column('source_language', sa.String(16), nullable=False),
        sa.Column('target_language', sa.String(16), nullable=False),
        sa.Column('translated_document', sa.Text(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    )


def downgrade():
    op.drop_table('narrative_translation_records')
    op.drop_table('narrative_generation_errors')
    op.drop_table('narrative_generation_runs')
    op.drop_table('narrative_validation_results')
    op.drop_table('narrative_templates')
    op.drop_table('narrative_versions')
    op.drop_table('narrative_lineage')
    op.drop_table('narrative_statements')
    op.drop_table('narrative_sections')
    op.drop_table('trust_narratives')
