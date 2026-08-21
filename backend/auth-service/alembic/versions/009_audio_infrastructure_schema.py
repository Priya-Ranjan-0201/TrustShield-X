"""audio_infrastructure_schema

Revision ID: 009_audio_infrastructure_schema
Revises: 008_deepfake_production_integration_schema
Create Date: 2026-08-05 18:30:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = '009_audio_infrastructure_schema'
down_revision: Union[str, None] = '008_deepfake_production_integration_schema'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. audio_metadata table
    op.create_table(
        'audio_metadata',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('scan_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('scan_history.id', ondelete='CASCADE'), nullable=False, index=True),
        sa.Column('duration_sec', sa.Float(), nullable=True),
        sa.Column('sample_rate', sa.Integer(), nullable=True),
        sa.Column('channels', sa.Integer(), nullable=True),
        sa.Column('bit_depth', sa.Integer(), nullable=True),
        sa.Column('codec', sa.String(50), nullable=True),
        sa.Column('bitrate', sa.Integer(), nullable=True),
        sa.Column('loudness_lufs', sa.Float(), nullable=True),
        sa.Column('quality_metrics', sa.JSON(), nullable=True, server_default='{}'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )

    # 2. speech_segments table
    op.create_table(
        'speech_segments',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('scan_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('scan_history.id', ondelete='CASCADE'), nullable=False, index=True),
        sa.Column('segment_index', sa.Integer(), nullable=False),
        sa.Column('start_time_sec', sa.Float(), nullable=False),
        sa.Column('end_time_sec', sa.Float(), nullable=False),
        sa.Column('duration_sec', sa.Float(), nullable=False),
        sa.Column('speaker_id', sa.String(50), nullable=True, index=True),
        sa.Column('is_speech', sa.Boolean(), nullable=False, default=True),
        sa.Column('confidence', sa.Float(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )

    # 3. speaker_tracks table
    op.create_table(
        'speaker_tracks',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('scan_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('scan_history.id', ondelete='CASCADE'), nullable=False, index=True),
        sa.Column('speaker_id', sa.String(50), nullable=False, index=True),
        sa.Column('total_speaking_duration', sa.Float(), nullable=False, default=0.0),
        sa.Column('segment_count', sa.Integer(), nullable=False, default=0),
        sa.Column('timeline_json', sa.JSON(), nullable=False, server_default='[]'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )


def downgrade() -> None:
    op.drop_table('speaker_tracks')
    op.drop_table('speech_segments')
    op.drop_table('audio_metadata')
