"""Alembic Migration 037: Report Rendering Schema.

Revision ID: 037_report_rendering_schema
Revises: 036_trust_narrative_schema
Create Date: 2026-08-14
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = '037_report_rendering_schema'
down_revision = '036_trust_narrative_schema'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'report_artifacts',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('artifact_id', sa.String(128), nullable=False),
        sa.Column('report_id', sa.String(128), nullable=False),
        sa.Column('analysis_id', sa.String(128), nullable=False),
        sa.Column('report_version', sa.String(64), nullable=False),
        sa.Column('artifact_version', sa.String(64), nullable=False),
        sa.Column('format', sa.String(32), nullable=False),
        sa.Column('mime_type', sa.String(128), nullable=False),
        sa.Column('file_extension', sa.String(16), nullable=False),
        sa.Column('size_bytes', sa.Integer(), nullable=False),
        sa.Column('sha256', sa.String(64), nullable=False),
        sa.Column('content_encoding', sa.String(32), nullable=False),
        sa.Column('renderer_name', sa.String(128), nullable=False),
        sa.Column('renderer_version', sa.String(64), nullable=False),
        sa.Column('schema_version', sa.String(64), nullable=False),
        sa.Column('generated_at', sa.String(64), nullable=False),
        sa.Column('generation_duration_ms', sa.Float(), nullable=False),
        sa.Column('storage_location', sa.String(512), nullable=False),
        sa.Column('status', sa.String(32), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index('ix_report_artifacts_artifact_id', 'report_artifacts', ['artifact_id'])
    op.create_index('ix_report_artifacts_report_id', 'report_artifacts', ['report_id'])
    op.create_index('ix_report_artifacts_format', 'report_artifacts', ['format'])
    op.create_index('ix_report_artifacts_status', 'report_artifacts', ['status'])
    op.create_index('ix_report_artifacts_sha256', 'report_artifacts', ['sha256'])

    op.create_table(
        'report_export_jobs',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('job_id', sa.String(128), nullable=False),
        sa.Column('report_id', sa.String(128), nullable=False),
        sa.Column('format', sa.String(32), nullable=False),
        sa.Column('status', sa.String(32), nullable=False),
        sa.Column('progress', sa.Integer(), nullable=False),
        sa.Column('requested_by', sa.String(128), nullable=False),
        sa.Column('started_at', sa.String(64), nullable=True),
        sa.Column('completed_at', sa.String(64), nullable=True),
        sa.Column('artifact_id', sa.String(128), nullable=True),
        sa.Column('error_code', sa.String(64), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index('ix_report_export_jobs_job_id', 'report_export_jobs', ['job_id'])
    op.create_index('ix_report_export_jobs_report_id', 'report_export_jobs', ['report_id'])
    op.create_index('ix_report_export_jobs_status', 'report_export_jobs', ['status'])

    op.create_table(
        'report_signatures',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('signature_id', sa.String(128), nullable=False),
        sa.Column('artifact_id', sa.String(128), nullable=False),
        sa.Column('algorithm', sa.String(64), nullable=False),
        sa.Column('key_id', sa.String(128), nullable=False),
        sa.Column('signature', sa.Text(), nullable=False),
        sa.Column('signed_hash', sa.String(64), nullable=False),
        sa.Column('signed_at', sa.String(64), nullable=False),
        sa.Column('status', sa.String(32), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index('ix_report_signatures_signature_id', 'report_signatures', ['signature_id'])
    op.create_index('ix_report_signatures_artifact_id', 'report_signatures', ['artifact_id'])

    op.create_table(
        'report_integrity_records',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('integrity_id', sa.String(128), nullable=False),
        sa.Column('report_id', sa.String(128), nullable=False),
        sa.Column('artifact_id', sa.String(128), nullable=False),
        sa.Column('content_hash', sa.String(64), nullable=False),
        sa.Column('artifact_hash', sa.String(64), nullable=False),
        sa.Column('is_valid', sa.Boolean(), nullable=False),
        sa.Column('verified_at', sa.String(64), nullable=False),
        sa.Column('detected_tampering', sa.Boolean(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index('ix_report_integrity_records_integrity_id', 'report_integrity_records', ['integrity_id'])
    op.create_index('ix_report_integrity_records_report_id', 'report_integrity_records', ['report_id'])

    op.create_table(
        'report_manifests',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('report_id', sa.String(128), nullable=False),
        sa.Column('analysis_id', sa.String(128), nullable=False),
        sa.Column('report_version', sa.String(64), nullable=False),
        sa.Column('artifact_id', sa.String(128), nullable=False),
        sa.Column('artifact_format', sa.String(32), nullable=False),
        sa.Column('artifact_sha256', sa.String(64), nullable=False),
        sa.Column('content_sha256', sa.String(64), nullable=False),
        sa.Column('manifest_json', sa.Text(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index('ix_report_manifests_report_id', 'report_manifests', ['report_id'])

    op.create_table(
        'artifact_storage_records',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('storage_id', sa.String(128), nullable=False),
        sa.Column('artifact_id', sa.String(128), nullable=False),
        sa.Column('provider', sa.String(64), nullable=False),
        sa.Column('bucket_or_path', sa.String(512), nullable=False),
        sa.Column('object_key', sa.String(256), nullable=False),
        sa.Column('size_bytes', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index('ix_artifact_storage_records_artifact_id', 'artifact_storage_records', ['artifact_id'])

    op.create_table(
        'report_rendering_runs',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('run_id', sa.String(128), nullable=False),
        sa.Column('report_id', sa.String(128), nullable=False),
        sa.Column('artifact_id', sa.String(128), nullable=False),
        sa.Column('format', sa.String(32), nullable=False),
        sa.Column('duration_ms', sa.Float(), nullable=False),
        sa.Column('status', sa.String(32), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index('ix_report_rendering_runs_run_id', 'report_rendering_runs', ['run_id'])

    op.create_table(
        'report_rendering_errors',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('error_id', sa.String(128), nullable=False),
        sa.Column('report_id', sa.String(128), nullable=False),
        sa.Column('error_code', sa.String(64), nullable=False),
        sa.Column('error_message', sa.String(1024), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index('ix_report_rendering_errors_error_code', 'report_rendering_errors', ['error_code'])

    op.create_table(
        'report_format_validations',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('validation_id', sa.String(128), nullable=False),
        sa.Column('report_id', sa.String(128), nullable=False),
        sa.Column('formats_tested', sa.String(256), nullable=False),
        sa.Column('consistent', sa.Boolean(), nullable=False),
        sa.Column('discrepancies', sa.Text(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    )

    op.create_table(
        'report_download_audits',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('audit_id', sa.String(128), nullable=False),
        sa.Column('artifact_id', sa.String(128), nullable=False),
        sa.Column('user_id', sa.String(128), nullable=False),
        sa.Column('ip_address', sa.String(64), nullable=False),
        sa.Column('downloaded_at', sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index('ix_report_download_audits_artifact_id', 'report_download_audits', ['artifact_id'])


def downgrade():
    op.drop_table('report_download_audits')
    op.drop_table('report_format_validations')
    op.drop_table('report_rendering_errors')
    op.drop_table('report_rendering_runs')
    op.drop_table('artifact_storage_records')
    op.drop_table('report_manifests')
    op.drop_table('report_integrity_records')
    op.drop_table('report_signatures')
    op.drop_table('report_export_jobs')
    op.drop_table('report_artifacts')
