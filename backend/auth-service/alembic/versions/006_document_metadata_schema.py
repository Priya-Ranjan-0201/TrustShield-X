"""document_metadata_schema

Revision ID: 006_document_metadata_schema
Revises: 005_scan_engine_orchestration_schema
Create Date: 2026-08-05 17:00:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = '006_document_metadata_schema'
down_revision: Union[str, None] = '005_scan_engine_orchestration_schema'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'document_metadata',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('scan_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('scan_history.id', ondelete='CASCADE'), nullable=False, index=True),
        sa.Column('document_type', sa.String(50), nullable=False, index=True),
        sa.Column('extracted_fields', sa.JSON(), nullable=False, server_default='{}'),
        sa.Column('ocr_confidence', sa.Float(), nullable=True),
        sa.Column('image_quality_metrics', sa.JSON(), nullable=True, server_default='{}'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )


def downgrade() -> None:
    op.drop_table('document_metadata')
