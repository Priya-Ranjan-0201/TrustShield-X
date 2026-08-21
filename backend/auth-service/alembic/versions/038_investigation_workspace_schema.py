"""Alembic Migration 038: Investigation Workspace Schema.

Revision ID: 038_investigation_workspace_schema
Revises: 037_report_rendering_schema
Create Date: 2026-08-14
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = '038_investigation_workspace_schema'
down_revision = '037_report_rendering_schema'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'investigation_workspaces',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('workspace_id', sa.String(128), nullable=False),
        sa.Column('title', sa.String(256), nullable=False),
        sa.Column('case_id', sa.String(128), nullable=True),
        sa.Column('analysis_id', sa.String(128), nullable=False),
        sa.Column('report_id', sa.String(128), nullable=False),
        sa.Column('user_id', sa.String(128), nullable=False),
        sa.Column('organization_id', sa.String(128), nullable=False),
        sa.Column('role', sa.String(64), nullable=False),
        sa.Column('status', sa.String(32), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('last_accessed_at', sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index('ix_investigation_workspaces_workspace_id', 'investigation_workspaces', ['workspace_id'], unique=True)
    op.create_index('ix_investigation_workspaces_case_id', 'investigation_workspaces', ['case_id'])
    op.create_index('ix_investigation_workspaces_analysis_id', 'investigation_workspaces', ['analysis_id'])
    op.create_index('ix_investigation_workspaces_user_id', 'investigation_workspaces', ['user_id'])
    op.create_index('ix_investigation_workspaces_organization_id', 'investigation_workspaces', ['organization_id'])

    op.create_table(
        'investigation_cases',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('case_id', sa.String(128), nullable=False),
        sa.Column('organization_id', sa.String(128), nullable=False),
        sa.Column('title', sa.String(256), nullable=False),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('status', sa.String(32), nullable=False),
        sa.Column('priority', sa.String(32), nullable=False),
        sa.Column('owner_id', sa.String(128), nullable=False),
        sa.Column('created_by', sa.String(128), nullable=False),
        sa.Column('classification', sa.String(64), nullable=False),
        sa.Column('retention_policy', sa.String(64), nullable=False),
        sa.Column('closed_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index('ix_investigation_cases_case_id', 'investigation_cases', ['case_id'], unique=True)
    op.create_index('ix_investigation_cases_organization_id', 'investigation_cases', ['organization_id'])
    op.create_index('ix_investigation_cases_status', 'investigation_cases', ['status'])
    op.create_index('ix_investigation_cases_priority', 'investigation_cases', ['priority'])
    op.create_index('ix_investigation_cases_owner_id', 'investigation_cases', ['owner_id'])

    op.create_table(
        'case_analyses',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('link_id', sa.String(128), nullable=False),
        sa.Column('case_id', sa.String(128), nullable=False),
        sa.Column('analysis_id', sa.String(128), nullable=False),
        sa.Column('module_type', sa.String(64), nullable=False),
        sa.Column('target_identifier', sa.String(256), nullable=False),
        sa.Column('status', sa.String(32), nullable=False),
        sa.Column('risk_score', sa.Float(), nullable=False),
        sa.Column('risk_band', sa.String(64), nullable=False),
        sa.Column('attached_at', sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index('ix_case_analyses_link_id', 'case_analyses', ['link_id'], unique=True)
    op.create_index('ix_case_analyses_case_id', 'case_analyses', ['case_id'])
    op.create_index('ix_case_analyses_analysis_id', 'case_analyses', ['analysis_id'])

    op.create_table(
        'case_notes',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('note_id', sa.String(128), nullable=False),
        sa.Column('case_id', sa.String(128), nullable=False),
        sa.Column('analysis_id', sa.String(128), nullable=True),
        sa.Column('finding_id', sa.String(128), nullable=True),
        sa.Column('evidence_id', sa.String(128), nullable=True),
        sa.Column('author_id', sa.String(128), nullable=False),
        sa.Column('note_type', sa.String(64), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('visibility', sa.String(32), nullable=False),
        sa.Column('status', sa.String(32), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index('ix_case_notes_note_id', 'case_notes', ['note_id'], unique=True)
    op.create_index('ix_case_notes_case_id', 'case_notes', ['case_id'])
    op.create_index('ix_case_notes_author_id', 'case_notes', ['author_id'])

    op.create_table(
        'case_bookmarks',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('bookmark_id', sa.String(128), nullable=False),
        sa.Column('case_id', sa.String(128), nullable=False),
        sa.Column('user_id', sa.String(128), nullable=False),
        sa.Column('item_type', sa.String(64), nullable=False),
        sa.Column('item_id', sa.String(128), nullable=False),
        sa.Column('label', sa.String(256), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index('ix_case_bookmarks_bookmark_id', 'case_bookmarks', ['bookmark_id'], unique=True)
    op.create_index('ix_case_bookmarks_case_id', 'case_bookmarks', ['case_id'])
    op.create_index('ix_case_bookmarks_user_id', 'case_bookmarks', ['user_id'])

    op.create_table(
        'case_tasks',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('task_id', sa.String(128), nullable=False),
        sa.Column('case_id', sa.String(128), nullable=False),
        sa.Column('title', sa.String(256), nullable=False),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('assigned_to', sa.String(128), nullable=False),
        sa.Column('priority', sa.String(32), nullable=False),
        sa.Column('status', sa.String(32), nullable=False),
        sa.Column('due_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('completed_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index('ix_case_tasks_task_id', 'case_tasks', ['task_id'], unique=True)
    op.create_index('ix_case_tasks_case_id', 'case_tasks', ['case_id'])
    op.create_index('ix_case_tasks_status', 'case_tasks', ['status'])

    op.create_table(
        'case_shares',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('share_id', sa.String(128), nullable=False),
        sa.Column('report_id', sa.String(128), nullable=False),
        sa.Column('case_id', sa.String(128), nullable=True),
        sa.Column('created_by', sa.String(128), nullable=False),
        sa.Column('expires_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('permission', sa.String(64), nullable=False),
        sa.Column('status', sa.String(32), nullable=False),
        sa.Column('access_limit', sa.Integer(), nullable=False),
        sa.Column('access_count', sa.Integer(), nullable=False),
        sa.Column('revoked_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index('ix_case_shares_share_id', 'case_shares', ['share_id'], unique=True)
    op.create_index('ix_case_shares_report_id', 'case_shares', ['report_id'])
    op.create_index('ix_case_shares_status', 'case_shares', ['status'])

    op.create_table(
        'investigation_annotations',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('annotation_id', sa.String(128), nullable=False),
        sa.Column('target_type', sa.String(32), nullable=False),
        sa.Column('target_id', sa.String(128), nullable=False),
        sa.Column('author_id', sa.String(128), nullable=False),
        sa.Column('tag', sa.String(64), nullable=False),
        sa.Column('comment', sa.Text(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index('ix_investigation_annotations_annotation_id', 'investigation_annotations', ['annotation_id'], unique=True)
    op.create_index('ix_investigation_annotations_target_id', 'investigation_annotations', ['target_id'])

    op.create_table(
        'investigation_saved_views',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('view_id', sa.String(128), nullable=False),
        sa.Column('user_id', sa.String(128), nullable=False),
        sa.Column('name', sa.String(256), nullable=False),
        sa.Column('description', sa.String(512), nullable=False),
        sa.Column('view_config', sa.Text(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index('ix_investigation_saved_views_view_id', 'investigation_saved_views', ['view_id'], unique=True)
    op.create_index('ix_investigation_saved_views_user_id', 'investigation_saved_views', ['user_id'])

    op.create_table(
        'investigation_search_history',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('search_id', sa.String(128), nullable=False),
        sa.Column('user_id', sa.String(128), nullable=False),
        sa.Column('query', sa.String(512), nullable=False),
        sa.Column('results_count', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index('ix_investigation_search_history_search_id', 'investigation_search_history', ['search_id'], unique=True)

    op.create_table(
        'investigation_audit_events',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('event_id', sa.String(128), nullable=False),
        sa.Column('user_id', sa.String(128), nullable=False),
        sa.Column('case_id', sa.String(128), nullable=True),
        sa.Column('analysis_id', sa.String(128), nullable=True),
        sa.Column('action', sa.String(128), nullable=False),
        sa.Column('object_type', sa.String(64), nullable=False),
        sa.Column('object_id', sa.String(128), nullable=False),
        sa.Column('ip_address', sa.String(64), nullable=False),
        sa.Column('timestamp', sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index('ix_investigation_audit_events_event_id', 'investigation_audit_events', ['event_id'], unique=True)
    op.create_index('ix_investigation_audit_events_case_id', 'investigation_audit_events', ['case_id'])
    op.create_index('ix_investigation_audit_events_action', 'investigation_audit_events', ['action'])

    op.create_table(
        'investigation_correlations',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('correlation_id', sa.String(128), nullable=False),
        sa.Column('case_id', sa.String(128), nullable=False),
        sa.Column('source_analysis_id', sa.String(128), nullable=False),
        sa.Column('target_analysis_id', sa.String(128), nullable=False),
        sa.Column('source_module', sa.String(64), nullable=False),
        sa.Column('target_module', sa.String(64), nullable=False),
        sa.Column('source_finding_id', sa.String(128), nullable=False),
        sa.Column('target_finding_id', sa.String(128), nullable=False),
        sa.Column('relationship', sa.String(64), nullable=False),
        sa.Column('confidence', sa.String(32), nullable=False),
        sa.Column('evidence_reference', sa.String(128), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index('ix_investigation_correlations_correlation_id', 'investigation_correlations', ['correlation_id'], unique=True)
    op.create_index('ix_investigation_correlations_case_id', 'investigation_correlations', ['case_id'])

    op.create_table(
        'investigation_workspace_state',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('state_id', sa.String(128), nullable=False),
        sa.Column('workspace_id', sa.String(128), nullable=False),
        sa.Column('user_id', sa.String(128), nullable=False),
        sa.Column('state_json', sa.Text(), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index('ix_investigation_workspace_state_state_id', 'investigation_workspace_state', ['state_id'], unique=True)
    op.create_index('ix_investigation_workspace_state_workspace_id', 'investigation_workspace_state', ['workspace_id'])


def downgrade():
    op.drop_table('investigation_workspace_state')
    op.drop_table('investigation_correlations')
    op.drop_table('investigation_audit_events')
    op.drop_table('investigation_search_history')
    op.drop_table('investigation_saved_views')
    op.drop_table('investigation_annotations')
    op.drop_table('case_shares')
    op.drop_table('case_tasks')
    op.drop_table('case_bookmarks')
    op.drop_table('case_notes')
    op.drop_table('case_analyses')
    op.drop_table('investigation_cases')
    op.drop_table('investigation_workspaces')
