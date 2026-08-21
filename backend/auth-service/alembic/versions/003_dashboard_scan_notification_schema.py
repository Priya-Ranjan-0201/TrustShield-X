"""dashboard_scan_notification_schema

Revision ID: 003_dashboard_scan_notification_schema
Revises: 002_production_hardening_schema
Create Date: 2026-08-04 20:38:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = '003_dashboard_scan_notification_schema'
down_revision: Union[str, None] = '002_production_hardening_schema'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. Notifications table
    op.create_table(
        'notifications',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('title', sa.String(255), nullable=False),
        sa.Column('message', sa.Text(), nullable=False),
        sa.Column('read', sa.Boolean(), server_default='false', nullable=False),
        sa.Column('severity', sa.String(30), server_default='info', nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    )
    op.create_index('ix_notifications_user_id', 'notifications', ['user_id'])
    op.create_index('ix_notifications_read', 'notifications', ['read'])
    op.create_index('ix_notifications_created_at', 'notifications', ['created_at'])

    # 2. Scan History table
    op.create_table(
        'scan_history',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('target', sa.String(512), nullable=False),
        sa.Column('scan_type', sa.String(30), nullable=False),
        sa.Column('trust_score', sa.Integer(), nullable=True),
        sa.Column('status', sa.String(30), server_default='PENDING', nullable=False),
        sa.Column('summary', sa.Text(), nullable=True),
        sa.Column('file_path', sa.String(512), nullable=True),
        sa.Column('file_size_bytes', sa.BigInteger(), nullable=True),
        sa.Column('scanned_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    )
    op.create_index('ix_scan_history_user_id', 'scan_history', ['user_id'])
    op.create_index('ix_scan_history_scan_type', 'scan_history', ['scan_type'])
    op.create_index('ix_scan_history_status', 'scan_history', ['status'])
    op.create_index('ix_scan_history_scanned_at', 'scan_history', ['scanned_at'])

    # 3. Reports table
    op.create_table(
        'reports',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('title', sa.String(255), nullable=False),
        sa.Column('category', sa.String(100), nullable=False),
        sa.Column('trust_score', sa.Integer(), nullable=False),
        sa.Column('status', sa.String(30), nullable=False),
        sa.Column('findings_count', sa.Integer(), server_default='0', nullable=False),
        sa.Column('download_url', sa.String(512), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    )
    op.create_index('ix_reports_user_id', 'reports', ['user_id'])
    op.create_index('ix_reports_created_at', 'reports', ['created_at'])


def downgrade() -> None:
    op.drop_table('reports')
    op.drop_table('scan_history')
    op.drop_table('notifications')
