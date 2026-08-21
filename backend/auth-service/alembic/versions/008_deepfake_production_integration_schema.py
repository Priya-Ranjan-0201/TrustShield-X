"""deepfake_production_integration_schema

Revision ID: 008_deepfake_production_integration_schema
Revises: 007_deepfake_infrastructure_schema
Create Date: 2026-08-05 18:00:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = '008_deepfake_production_integration_schema'
down_revision: Union[str, None] = '007_deepfake_infrastructure_schema'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. Add inference & telemetry columns to deepfake_metadata
    op.add_column('deepfake_metadata', sa.Column('fake_probability', sa.Float(), nullable=True))
    op.add_column('deepfake_metadata', sa.Column('real_probability', sa.Float(), nullable=True))
    op.add_column('deepfake_metadata', sa.Column('confidence', sa.Float(), nullable=True))
    op.add_column('deepfake_metadata', sa.Column('inference_time_ms', sa.Integer(), nullable=True))
    op.add_column('deepfake_metadata', sa.Column('model_name', sa.String(100), nullable=True))
    op.add_column('deepfake_metadata', sa.Column('model_version', sa.String(50), nullable=True))
    op.add_column('deepfake_metadata', sa.Column('processing_device', sa.String(50), nullable=True))
    op.add_column('deepfake_metadata', sa.Column('total_frame_count', sa.Integer(), nullable=True))
    op.add_column('deepfake_metadata', sa.Column('manipulated_frame_count', sa.Integer(), nullable=True))
    op.add_column('deepfake_metadata', sa.Column('highest_risk_frame', sa.Integer(), nullable=True))
    op.add_column('deepfake_metadata', sa.Column('average_frame_score', sa.Float(), nullable=True))
    op.add_column('deepfake_metadata', sa.Column('explanation_available', sa.Boolean(), nullable=True, server_default='true'))
    op.add_column('deepfake_metadata', sa.Column('heatmap_available', sa.Boolean(), nullable=True, server_default='true'))

    # 2. Add prediction & risk columns to media_frames
    op.add_column('media_frames', sa.Column('prediction', sa.Float(), nullable=True))
    op.add_column('media_frames', sa.Column('confidence', sa.Float(), nullable=True))
    op.add_column('media_frames', sa.Column('risk_score', sa.Integer(), nullable=True))
    op.add_column('media_frames', sa.Column('face_track_id', sa.String(50), nullable=True))
    op.add_column('media_frames', sa.Column('processing_time_ms', sa.Integer(), nullable=True))
    op.add_column('media_frames', sa.Column('explanation_ref', sa.JSON(), nullable=True, server_default='{}'))


def downgrade() -> None:
    op.drop_column('media_frames', 'explanation_ref')
    op.drop_column('media_frames', 'processing_time_ms')
    op.drop_column('media_frames', 'face_track_id')
    op.drop_column('media_frames', 'risk_score')
    op.drop_column('media_frames', 'confidence')
    op.drop_column('media_frames', 'prediction')

    op.drop_column('deepfake_metadata', 'heatmap_available')
    op.drop_column('deepfake_metadata', 'explanation_available')
    op.drop_column('deepfake_metadata', 'average_frame_score')
    op.drop_column('deepfake_metadata', 'highest_risk_frame')
    op.drop_column('deepfake_metadata', 'manipulated_frame_count')
    op.drop_column('deepfake_metadata', 'total_frame_count')
    op.drop_column('deepfake_metadata', 'processing_device')
    op.drop_column('deepfake_metadata', 'model_version')
    op.drop_column('deepfake_metadata', 'model_name')
    op.drop_column('deepfake_metadata', 'inference_time_ms')
    op.drop_column('deepfake_metadata', 'confidence')
    op.drop_column('deepfake_metadata', 'real_probability')
    op.drop_column('deepfake_metadata', 'fake_probability')
