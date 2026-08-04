"""production hardening schema

Revision ID: 002_production_hardening_schema
Revises: 001_initial_auth_schema
Create Date: 2026-08-04 14:30:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = '002_production_hardening_schema'
down_revision: Union[str, None] = '001_initial_auth_schema'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. Create email_verifications table
    op.create_table(
        'email_verifications',
        sa.Column('id', sa.Uuid(as_uuid=True), nullable=False),
        sa.Column('user_id', sa.Uuid(as_uuid=True), nullable=False),
        sa.Column('token_hash', sa.String(length=255), nullable=False),
        sa.Column('expires_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('used_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_email_verifications_token_hash'), 'email_verifications', ['token_hash'], unique=True)
    op.create_index(op.f('ix_email_verifications_user_id'), 'email_verifications', ['user_id'], unique=False)

    # 2. Create user_sessions table
    op.create_table(
        'user_sessions',
        sa.Column('id', sa.Uuid(as_uuid=True), nullable=False),
        sa.Column('user_id', sa.Uuid(as_uuid=True), nullable=False),
        sa.Column('device_name', sa.String(length=100), nullable=True),
        sa.Column('browser', sa.String(length=100), nullable=True),
        sa.Column('operating_system', sa.String(length=100), nullable=True),
        sa.Column('ip_address', sa.String(length=45), nullable=False),
        sa.Column('country', sa.String(length=100), nullable=True),
        sa.Column('last_activity', sa.DateTime(timezone=True), nullable=False),
        sa.Column('refresh_token_jti', sa.String(length=255), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default=sa.text('true')),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('expires_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_sessions_is_active'), 'user_sessions', ['is_active'], unique=False)
    op.create_index(op.f('ix_user_sessions_refresh_token_jti'), 'user_sessions', ['refresh_token_jti'], unique=True)
    op.create_index(op.f('ix_user_sessions_user_id'), 'user_sessions', ['user_id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_user_sessions_user_id'), table_name='user_sessions')
    op.drop_index(op.f('ix_user_sessions_refresh_token_jti'), table_name='user_sessions')
    op.drop_index(op.f('ix_user_sessions_is_active'), table_name='user_sessions')
    op.drop_table('user_sessions')

    op.drop_index(op.f('ix_email_verifications_user_id'), table_name='email_verifications')
    op.drop_index(op.f('ix_email_verifications_token_hash'), table_name='email_verifications')
    op.drop_table('email_verifications')
