"""scan_engine_orchestration_schema

Revision ID: 005_scan_engine_orchestration_schema
Revises: 004_scan_metadata_telemetry_schema
Create Date: 2026-08-04 21:00:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = '005_scan_engine_orchestration_schema'
down_revision: Union[str, None] = '004_scan_metadata_telemetry_schema'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. scan_modules table
    op.create_table(
        'scan_modules',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('name', sa.String(100), nullable=False),
        sa.Column('code', sa.String(50), nullable=False),
        sa.Column('scan_type', sa.String(30), nullable=False),
        sa.Column('version', sa.String(30), server_default='v1.0', nullable=False),
        sa.Column('is_active', sa.Boolean(), server_default='true', nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    )
    op.create_index('ix_scan_modules_code', 'scan_modules', ['code'], unique=True)
    op.create_index('ix_scan_modules_scan_type', 'scan_modules', ['scan_type'])

    # 2. scan_results table
    op.create_table(
        'scan_results',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('scan_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('scan_history.id', ondelete='CASCADE'), nullable=False),
        sa.Column('module_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('scan_modules.id', ondelete='SET NULL'), nullable=True),
        sa.Column('trust_score', sa.Integer(), nullable=False),
        sa.Column('risk_score', sa.Integer(), nullable=False),
        sa.Column('confidence_score', sa.Float(), nullable=False),
        sa.Column('findings_json', postgresql.JSONB(), server_default='{}', nullable=False),
        sa.Column('execution_time_ms', sa.Integer(), server_default='0', nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    )
    op.create_index('ix_scan_results_scan_id', 'scan_results', ['scan_id'])
    op.create_index('ix_scan_results_module_id', 'scan_results', ['module_id'])

    # 3. scan_events table
    op.create_table(
        'scan_events',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('scan_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('scan_history.id', ondelete='CASCADE'), nullable=False),
        sa.Column('event_type', sa.String(50), nullable=False),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('event_data_json', postgresql.JSONB(), server_default='{}', nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    )
    op.create_index('ix_scan_events_scan_id', 'scan_events', ['scan_id'])
    op.create_index('ix_scan_events_event_type', 'scan_events', ['event_type'])
    op.create_index('ix_scan_events_created_at', 'scan_events', ['created_at'])


def downgrade() -> None:
    op.drop_table('scan_events')
    op.drop_table('scan_results')
    op.drop_table('scan_modules')
