"""deepfake_infrastructure_schema

Revision ID: 007_deepfake_infrastructure_schema
Revises: 006_document_metadata_schema
Create Date: 2026-08-05 17:30:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = '007_deepfake_infrastructure_schema'
down_revision: Union[str, None] = '006_document_metadata_schema'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. deepfake_metadata table
    op.create_table(
        'deepfake_metadata',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('scan_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('scan_history.id', ondelete='CASCADE'), nullable=False, index=True),
        sa.Column('media_type', sa.String(20), nullable=False, index=True),  # IMAGE, VIDEO
        sa.Column('duration_sec', sa.Float(), nullable=True),
        sa.Column('fps', sa.Float(), nullable=True),
        sa.Column('width', sa.Integer(), nullable=True),
        sa.Column('height', sa.Integer(), nullable=True),
        sa.Column('codec', sa.String(50), nullable=True),
        sa.Column('has_audio', sa.Boolean(), nullable=True, default=False),
        sa.Column('quality_metrics', sa.JSON(), nullable=True, server_default='{}'),
        sa.Column('exif_metadata', sa.JSON(), nullable=True, server_default='{}'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )

    # 2. media_frames table
    op.create_table(
        'media_frames',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('scan_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('scan_history.id', ondelete='CASCADE'), nullable=False, index=True),
        sa.Column('frame_index', sa.Integer(), nullable=False),
        sa.Column('timestamp_sec', sa.Float(), nullable=False),
        sa.Column('width', sa.Integer(), nullable=True),
        sa.Column('height', sa.Integer(), nullable=True),
        sa.Column('sampling_strategy', sa.String(50), nullable=True),
        sa.Column('quality_score', sa.Float(), nullable=True),
        sa.Column('faces_detected_count', sa.Integer(), nullable=False, default=0),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )

    # 3. face_tracks table
    op.create_table(
        'face_tracks',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('scan_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('scan_history.id', ondelete='CASCADE'), nullable=False, index=True),
        sa.Column('track_id', sa.String(50), nullable=False, index=True),
        sa.Column('total_frames_tracked', sa.Integer(), nullable=False, default=0),
        sa.Column('avg_confidence', sa.Float(), nullable=True),
        sa.Column('bounding_boxes_json', sa.JSON(), nullable=False, server_default='[]'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )


def downgrade() -> None:
    op.drop_table('face_tracks')
    op.drop_table('media_frames')
    op.drop_table('deepfake_metadata')
