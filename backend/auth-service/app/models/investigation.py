"""SQLAlchemy 2.0 ORM Models for Digital Trust Investigation Workspace (Phase 4.0 Part 4 — Section 71).

Defines 13 database tables:
investigation_workspaces, investigation_cases, case_analyses, case_notes,
case_bookmarks, case_tasks, case_shares, investigation_annotations,
investigation_saved_views, investigation_search_history, investigation_audit_events,
investigation_correlations, investigation_workspace_state.
"""

import uuid
from datetime import datetime, timezone
from sqlalchemy import String, Integer, Float, Boolean, DateTime, Text
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID
from app.models.base import Base


class InvestigationWorkspaceModel(Base):
    __tablename__ = "investigation_workspaces"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    workspace_id: Mapped[str] = mapped_column(String(128), nullable=False, unique=True, index=True)
    title: Mapped[str] = mapped_column(String(256), nullable=False)
    case_id: Mapped[str] = mapped_column(String(128), nullable=True, index=True)
    analysis_id: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    report_id: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    user_id: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    organization_id: Mapped[str] = mapped_column(String(128), nullable=False, default="org_default", index=True)
    role: Mapped[str] = mapped_column(String(64), nullable=False, default="ANALYST")
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="ACTIVE")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    last_accessed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class InvestigationCaseModel(Base):
    __tablename__ = "investigation_cases"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    case_id: Mapped[str] = mapped_column(String(128), nullable=False, unique=True, index=True)
    organization_id: Mapped[str] = mapped_column(String(128), nullable=False, default="org_default", index=True)
    title: Mapped[str] = mapped_column(String(256), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False, default="")
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="OPEN", index=True)
    priority: Mapped[str] = mapped_column(String(32), nullable=False, default="MEDIUM", index=True)
    owner_id: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    created_by: Mapped[str] = mapped_column(String(128), nullable=False)
    classification: Mapped[str] = mapped_column(String(64), nullable=False, default="CONFIDENTIAL")
    retention_policy: Mapped[str] = mapped_column(String(64), nullable=False, default="DEFAULT_30D")
    closed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class CaseAnalysisModel(Base):
    __tablename__ = "case_analyses"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    link_id: Mapped[str] = mapped_column(String(128), nullable=False, unique=True, index=True)
    case_id: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    analysis_id: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    module_type: Mapped[str] = mapped_column(String(64), nullable=False)
    target_identifier: Mapped[str] = mapped_column(String(256), nullable=False, default="")
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="COMPLETED")
    risk_score: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    risk_band: Mapped[str] = mapped_column(String(64), nullable=False, default="TRUSTED")
    attached_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class CaseNoteModel(Base):
    __tablename__ = "case_notes"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    note_id: Mapped[str] = mapped_column(String(128), nullable=False, unique=True, index=True)
    case_id: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    analysis_id: Mapped[str] = mapped_column(String(128), nullable=True, index=True)
    finding_id: Mapped[str] = mapped_column(String(128), nullable=True, index=True)
    evidence_id: Mapped[str] = mapped_column(String(128), nullable=True, index=True)
    author_id: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    note_type: Mapped[str] = mapped_column(String(64), nullable=False, default="OBSERVATION")
    content: Mapped[str] = mapped_column(Text, nullable=False)
    visibility: Mapped[str] = mapped_column(String(32), nullable=False, default="INTERNAL")
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="ACTIVE")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class CaseBookmarkModel(Base):
    __tablename__ = "case_bookmarks"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    bookmark_id: Mapped[str] = mapped_column(String(128), nullable=False, unique=True, index=True)
    case_id: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    user_id: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    item_type: Mapped[str] = mapped_column(String(64), nullable=False)
    item_id: Mapped[str] = mapped_column(String(128), nullable=False)
    label: Mapped[str] = mapped_column(String(256), nullable=False, default="")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class CaseTaskModel(Base):
    __tablename__ = "case_tasks"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    task_id: Mapped[str] = mapped_column(String(128), nullable=False, unique=True, index=True)
    case_id: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(256), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False, default="")
    assigned_to: Mapped[str] = mapped_column(String(128), nullable=False, default="")
    priority: Mapped[str] = mapped_column(String(32), nullable=False, default="MEDIUM")
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="TODO", index=True)
    due_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    completed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class CaseShareModel(Base):
    __tablename__ = "case_shares"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    share_id: Mapped[str] = mapped_column(String(128), nullable=False, unique=True, index=True)
    report_id: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    case_id: Mapped[str] = mapped_column(String(128), nullable=True, index=True)
    created_by: Mapped[str] = mapped_column(String(128), nullable=False)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    permission: Mapped[str] = mapped_column(String(64), nullable=False, default="VIEW_ONLY")
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="ACTIVE", index=True)
    access_limit: Mapped[int] = mapped_column(Integer, nullable=False, default=100)
    access_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    revoked_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class InvestigationAnnotationModel(Base):
    __tablename__ = "investigation_annotations"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    annotation_id: Mapped[str] = mapped_column(String(128), nullable=False, unique=True, index=True)
    target_type: Mapped[str] = mapped_column(String(32), nullable=False)
    target_id: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    author_id: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    tag: Mapped[str] = mapped_column(String(64), nullable=False)
    comment: Mapped[str] = mapped_column(Text, nullable=False, default="")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class SavedViewModel(Base):
    __tablename__ = "investigation_saved_views"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    view_id: Mapped[str] = mapped_column(String(128), nullable=False, unique=True, index=True)
    user_id: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(256), nullable=False)
    description: Mapped[str] = mapped_column(String(512), nullable=False, default="")
    view_config: Mapped[str] = mapped_column(Text, nullable=False, default="{}")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class SearchHistoryModel(Base):
    __tablename__ = "investigation_search_history"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    search_id: Mapped[str] = mapped_column(String(128), nullable=False, unique=True, index=True)
    user_id: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    query: Mapped[str] = mapped_column(String(512), nullable=False)
    results_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class InvestigationAuditEventModel(Base):
    __tablename__ = "investigation_audit_events"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    event_id: Mapped[str] = mapped_column(String(128), nullable=False, unique=True, index=True)
    user_id: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    case_id: Mapped[str] = mapped_column(String(128), nullable=True, index=True)
    analysis_id: Mapped[str] = mapped_column(String(128), nullable=True, index=True)
    action: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    object_type: Mapped[str] = mapped_column(String(64), nullable=False)
    object_id: Mapped[str] = mapped_column(String(128), nullable=False)
    ip_address: Mapped[str] = mapped_column(String(64), nullable=False, default="127.0.0.1")
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class InvestigationCorrelationModel(Base):
    __tablename__ = "investigation_correlations"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    correlation_id: Mapped[str] = mapped_column(String(128), nullable=False, unique=True, index=True)
    case_id: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    source_analysis_id: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    target_analysis_id: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    source_module: Mapped[str] = mapped_column(String(64), nullable=False)
    target_module: Mapped[str] = mapped_column(String(64), nullable=False)
    source_finding_id: Mapped[str] = mapped_column(String(128), nullable=False)
    target_finding_id: Mapped[str] = mapped_column(String(128), nullable=False)
    relationship: Mapped[str] = mapped_column(String(64), nullable=False)
    confidence: Mapped[str] = mapped_column(String(32), nullable=False, default="HIGH")
    evidence_reference: Mapped[str] = mapped_column(String(128), nullable=False, default="")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class WorkspaceStateModel(Base):
    __tablename__ = "investigation_workspace_state"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    state_id: Mapped[str] = mapped_column(String(128), nullable=False, unique=True, index=True)
    workspace_id: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    user_id: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    state_json: Mapped[str] = mapped_column(Text, nullable=False, default="{}")
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
