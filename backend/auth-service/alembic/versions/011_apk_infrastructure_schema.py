"""apk_infrastructure_schema

Revision ID: 011_apk_infrastructure_schema
Revises: 010_voice_clone_production_schema
Create Date: 2026-08-05 20:30:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = '011_apk_infrastructure_schema'
down_revision: Union[str, None] = '010_voice_clone_production_schema'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. apk_metadata table
    op.create_table(
        'apk_metadata',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('scan_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('scan_history.id', ondelete='CASCADE'), nullable=False),
        sa.Column('package_name', sa.String(255), nullable=True),
        sa.Column('version_name', sa.String(100), nullable=True),
        sa.Column('version_code', sa.Integer(), nullable=True),
        sa.Column('application_label', sa.String(255), nullable=True),
        sa.Column('min_sdk', sa.Integer(), nullable=True),
        sa.Column('target_sdk', sa.Integer(), nullable=True),
        sa.Column('compile_sdk', sa.Integer(), nullable=True),
        sa.Column('apk_size', sa.BigInteger(), nullable=False, server_default='0'),
        sa.Column('apk_sha256', sa.String(64), nullable=False),
        sa.Column('parsed_successfully', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('now()')),
    )
    op.create_index('idx_apk_metadata_scan_id', 'apk_metadata', ['scan_id'])
    op.create_index('idx_apk_metadata_package_name', 'apk_metadata', ['package_name'])
    op.create_index('idx_apk_metadata_sha256', 'apk_metadata', ['apk_sha256'])
    op.create_index('idx_apk_meta_scan_sha', 'apk_metadata', ['scan_id', 'apk_sha256'], unique=True)

    # 2. apk_permissions table
    op.create_table(
        'apk_permissions',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('apk_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('apk_metadata.id', ondelete='CASCADE'), nullable=False),
        sa.Column('permission_name', sa.String(255), nullable=False),
        sa.Column('protection_level', sa.String(50), nullable=True),
        sa.Column('declared_by_app', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('now()')),
    )
    op.create_index('idx_apk_permissions_apk_id', 'apk_permissions', ['apk_id'])
    op.create_index('idx_apk_permissions_name', 'apk_permissions', ['permission_name'])

    # 3. apk_dex table
    op.create_table(
        'apk_dex',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('apk_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('apk_metadata.id', ondelete='CASCADE'), nullable=False),
        sa.Column('filename', sa.String(255), nullable=False),
        sa.Column('sha256', sa.String(64), nullable=False),
        sa.Column('size', sa.BigInteger(), nullable=False, server_default='0'),
        sa.Column('method_count', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('class_count', sa.Integer(), nullable=False, server_default='0'),
    )
    op.create_index('idx_apk_dex_apk_id', 'apk_dex', ['apk_id'])

    # 4. apk_native_libraries table
    op.create_table(
        'apk_native_libraries',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('apk_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('apk_metadata.id', ondelete='CASCADE'), nullable=False),
        sa.Column('library_name', sa.String(255), nullable=False),
        sa.Column('architecture', sa.String(50), nullable=False),
        sa.Column('sha256', sa.String(64), nullable=False),
        sa.Column('size', sa.BigInteger(), nullable=False, server_default='0'),
    )
    op.create_index('idx_apk_native_libs_apk_id', 'apk_native_libraries', ['apk_id'])

    # 5. apk_certificates table
    op.create_table(
        'apk_certificates',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('apk_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('apk_metadata.id', ondelete='CASCADE'), nullable=False),
        sa.Column('subject', sa.String(512), nullable=True),
        sa.Column('issuer', sa.String(512), nullable=True),
        sa.Column('sha256', sa.String(64), nullable=False),
        sa.Column('sha1', sa.String(40), nullable=True),
        sa.Column('signature_algorithm', sa.String(100), nullable=True),
        sa.Column('public_key_algorithm', sa.String(50), nullable=True),
        sa.Column('key_size', sa.Integer(), nullable=True),
        sa.Column('valid_from', sa.String(100), nullable=True),
        sa.Column('valid_until', sa.String(100), nullable=True),
        sa.Column('expired', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('self_signed', sa.Boolean(), nullable=False, server_default='false'),
    )
    op.create_index('idx_apk_certs_apk_id', 'apk_certificates', ['apk_id'])
    op.create_index('idx_apk_certs_sha256', 'apk_certificates', ['sha256'])


def downgrade() -> None:
    op.drop_table('apk_certificates')
    op.drop_table('apk_native_libraries')
    op.drop_table('apk_dex')
    op.drop_table('apk_permissions')
    op.drop_table('apk_metadata')
