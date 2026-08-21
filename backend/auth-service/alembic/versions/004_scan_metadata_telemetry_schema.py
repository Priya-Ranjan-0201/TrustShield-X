"""scan_metadata_telemetry_schema

Revision ID: 004_scan_metadata_telemetry_schema
Revises: 003_dashboard_scan_notification_schema
Create Date: 2026-08-04 20:50:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = '004_scan_metadata_telemetry_schema'
down_revision: Union[str, None] = '003_dashboard_scan_notification_schema'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('scan_history', sa.Column('risk_score', sa.Integer(), nullable=True))
    op.add_column('scan_history', sa.Column('confidence_score', sa.Float(), nullable=True))
    op.add_column('scan_history', sa.Column('sha256_checksum', sa.String(64), nullable=True))
    op.add_column('scan_history', sa.Column('mime_type', sa.String(100), nullable=True))
    op.add_column('scan_history', sa.Column('processing_time_ms', sa.Integer(), nullable=True))
    op.add_column('scan_history', sa.Column('queue_time_ms', sa.Integer(), nullable=True))
    op.add_column('scan_history', sa.Column('module_used', sa.String(100), nullable=True))
    op.add_column('scan_history', sa.Column('result_version', sa.String(30), server_default='v1', nullable=True))

    op.create_index('ix_scan_history_sha256_checksum', 'scan_history', ['sha256_checksum'])


def downgrade() -> None:
    op.drop_index('ix_scan_history_sha256_checksum', table_name='scan_history')
    op.drop_column('scan_history', 'result_version')
    op.drop_column('scan_history', 'module_used')
    op.drop_column('scan_history', 'queue_time_ms')
    op.drop_column('scan_history', 'processing_time_ms')
    op.drop_column('scan_history', 'mime_type')
    op.drop_column('scan_history', 'sha256_checksum')
    op.drop_column('scan_history', 'confidence_score')
    op.drop_column('scan_history', 'risk_score')
