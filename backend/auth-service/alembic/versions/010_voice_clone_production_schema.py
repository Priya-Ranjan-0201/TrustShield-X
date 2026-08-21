"""voice_clone_production_schema

Revision ID: 010_voice_clone_production_schema
Revises: 009_audio_infrastructure_schema
Create Date: 2026-08-05 19:00:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = '010_voice_clone_production_schema'
down_revision: Union[str, None] = '009_audio_infrastructure_schema'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. Extend audio_metadata table
    op.add_column('audio_metadata', sa.Column('clone_probability', sa.Float(), nullable=True))
    op.add_column('audio_metadata', sa.Column('real_probability', sa.Float(), nullable=True))
    op.add_column('audio_metadata', sa.Column('confidence', sa.Float(), nullable=True))
    op.add_column('audio_metadata', sa.Column('calibrated_confidence', sa.Float(), nullable=True))
    op.add_column('audio_metadata', sa.Column('prediction', sa.String(50), nullable=True))
    op.add_column('audio_metadata', sa.Column('prediction_reason', sa.Text(), nullable=True))
    op.add_column('audio_metadata', sa.Column('model_name', sa.String(100), nullable=True))
    op.add_column('audio_metadata', sa.Column('model_version', sa.String(50), nullable=True))
    op.add_column('audio_metadata', sa.Column('inference_time_ms', sa.Integer(), nullable=True))
    op.add_column('audio_metadata', sa.Column('embedding_dimension', sa.Integer(), nullable=True))
    op.add_column('audio_metadata', sa.Column('embedding_model', sa.String(100), nullable=True))
    op.add_column('audio_metadata', sa.Column('device_used', sa.String(50), nullable=True))
    op.add_column('audio_metadata', sa.Column('explanation_available', sa.Boolean(), nullable=True, server_default='true'))
    op.add_column('audio_metadata', sa.Column('evidence_available', sa.Boolean(), nullable=True, server_default='true'))
    op.add_column('audio_metadata', sa.Column('recommendation_available', sa.Boolean(), nullable=True, server_default='true'))

    # 2. Create voice_clone_results table
    op.create_table(
        'voice_clone_results',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('scan_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('scan_history.id', ondelete='CASCADE'), nullable=False, index=True),
        sa.Column('speaker_id', sa.String(50), nullable=False, index=True),
        sa.Column('segment_id', sa.String(50), nullable=True),
        sa.Column('clone_probability', sa.Float(), nullable=False),
        sa.Column('similarity_score', sa.Float(), nullable=True),
        sa.Column('confidence', sa.Float(), nullable=True),
        sa.Column('verdict', sa.String(50), nullable=False),
        sa.Column('evidence_json', sa.JSON(), nullable=True, server_default='[]'),
        sa.Column('recommendation_json', sa.JSON(), nullable=True, server_default='[]'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )

    # 3. Create conversation_analysis table
    op.create_table(
        'conversation_analysis',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('scan_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('scan_history.id', ondelete='CASCADE'), nullable=False, index=True),
        sa.Column('total_speakers', sa.Integer(), nullable=False, default=1),
        sa.Column('conversation_duration', sa.Float(), nullable=False, default=0.0),
        sa.Column('conversation_quality', sa.Integer(), nullable=True),
        sa.Column('conversation_risk', sa.Integer(), nullable=False, default=0),
        sa.Column('conversation_confidence', sa.Float(), nullable=True),
        sa.Column('dominant_speaker', sa.String(50), nullable=True),
        sa.Column('summary_json', sa.JSON(), nullable=False, server_default='{}'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )


def downgrade() -> None:
    op.drop_table('conversation_analysis')
    op.drop_table('voice_clone_results')

    op.drop_column('audio_metadata', 'recommendation_available')
    op.drop_column('audio_metadata', 'evidence_available')
    op.drop_column('audio_metadata', 'explanation_available')
    op.drop_column('audio_metadata', 'device_used')
    op.drop_column('audio_metadata', 'embedding_model')
    op.drop_column('audio_metadata', 'embedding_dimension')
    op.drop_column('audio_metadata', 'inference_time_ms')
    op.drop_column('audio_metadata', 'model_version')
    op.drop_column('audio_metadata', 'model_name')
    op.drop_column('audio_metadata', 'prediction_reason')
    op.drop_column('audio_metadata', 'prediction')
    op.drop_column('audio_metadata', 'calibrated_confidence')
    op.drop_column('audio_metadata', 'confidence')
    op.drop_column('audio_metadata', 'real_probability')
    op.drop_column('audio_metadata', 'clone_probability')
