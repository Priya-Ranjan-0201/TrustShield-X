"""Pydantic v2 DTO Schemas for Digital Trust Investigation Workspace (Phase 4.0 Part 4).

Strictly typed DTOs for workspaces, cases, analyses, notes, bookmarks, tasks,
shares, annotations, graph nodes/edges, timeline events, search, correlations,
and role-aware views.
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, ConfigDict, Field


# ---------------------------------------------------------------------------
# Section 3: Workspace & Context DTOs
# ---------------------------------------------------------------------------

class WorkspaceContextDTO(BaseModel):
    """Context identifying a specific active investigation."""
    workspace_id: str
    case_id: Optional[str] = None
    analysis_id: str
    report_id: str
    report_version: str = "1.0.0"
    user_id: str
    organization_id: str = "org_default"
    role: str = "ANALYST"  # EXECUTIVE, ANALYST, TECHNICAL, AUDITOR, ADMIN
    created_at: str = ""
    last_accessed_at: str = ""

    model_config = ConfigDict(frozen=True, from_attributes=True)


class WorkspaceStateDTO(BaseModel):
    """Client UI state for restoring viewport, filters, and expanded items."""
    state_id: str
    workspace_id: str
    user_id: str
    active_tab: str = "overview"
    selected_finding_id: Optional[str] = None
    selected_evidence_id: Optional[str] = None
    active_filters: Dict[str, Any] = Field(default_factory=dict)
    graph_position: Dict[str, float] = Field(default_factory=dict)
    timeline_range: Dict[str, str] = Field(default_factory=dict)
    view_mode: str = "ANALYST"
    updated_at: str = ""

    model_config = ConfigDict(frozen=True, from_attributes=True)


class InvestigationWorkspaceDTO(BaseModel):
    """High-level workspace object aggregating case and analysis data."""
    workspace_id: str
    title: str
    context: WorkspaceContextDTO
    state: Optional[WorkspaceStateDTO] = None
    status: str = "ACTIVE"
    created_at: str = ""

    model_config = ConfigDict(frozen=True, from_attributes=True)


# ---------------------------------------------------------------------------
# Sections 30-33: Case Management DTOs
# ---------------------------------------------------------------------------

class InvestigationCaseDTO(BaseModel):
    """Represents a multi-modal security investigation case."""
    case_id: str
    organization_id: str = "org_default"
    title: str
    description: str = ""
    status: str = "OPEN"  # OPEN, IN_PROGRESS, REVIEW, CONTAINED, RESOLVED, CLOSED, ARCHIVED
    priority: str = "MEDIUM"  # CRITICAL, HIGH, MEDIUM, LOW, INFORMATIONAL
    owner_id: str
    created_by: str
    created_at: str = ""
    updated_at: str = ""
    closed_at: Optional[str] = None
    classification: str = "CONFIDENTIAL"
    retention_policy: str = "DEFAULT_30D"
    analysis_count: int = 0
    note_count: int = 0
    task_count: int = 0

    model_config = ConfigDict(frozen=True, from_attributes=True)


class CaseAnalysisDTO(BaseModel):
    """Links an analysis (APK, Web, Audio, Document, QR) to a case."""
    link_id: str
    case_id: str
    analysis_id: str
    module_type: str  # APK, WEBSITE, AUDIO, DOCUMENT, QR, DEEPFAKE
    target_identifier: str = ""
    status: str = "COMPLETED"
    risk_score: float = 0.0
    risk_band: str = "TRUSTED"
    attached_at: str = ""

    model_config = ConfigDict(frozen=True, from_attributes=True)


class CaseCreateRequestDTO(BaseModel):
    title: str
    description: Optional[str] = ""
    priority: Optional[str] = "MEDIUM"
    classification: Optional[str] = "CONFIDENTIAL"
    analysis_ids: List[str] = Field(default_factory=list)

    model_config = ConfigDict(frozen=True, from_attributes=True)


class CaseUpdateRequestDTO(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    priority: Optional[str] = None
    classification: Optional[str] = None

    model_config = ConfigDict(frozen=True, from_attributes=True)


# ---------------------------------------------------------------------------
# Sections 34-37 & 50: Notes, Bookmarks, Tasks, and Shares DTOs
# ---------------------------------------------------------------------------

class CaseNoteDTO(BaseModel):
    """Analyst-authored notes explicitly distinguished from machine findings."""
    note_id: str
    case_id: str
    analysis_id: Optional[str] = None
    finding_id: Optional[str] = None
    evidence_id: Optional[str] = None
    author_id: str
    note_type: str = "OBSERVATION"  # OBSERVATION, HYPOTHESIS, FOLLOW_UP, INVESTIGATION, FALSE_POSITIVE_REVIEW, ESCALATION, GENERAL
    content: str
    visibility: str = "INTERNAL"  # INTERNAL, RESTRICTED, PUBLIC
    status: str = "ACTIVE"
    created_at: str = ""
    updated_at: str = ""

    model_config = ConfigDict(frozen=True, from_attributes=True)


class CaseBookmarkDTO(BaseModel):
    """Analyst bookmark for fast navigation."""
    bookmark_id: str
    case_id: str
    user_id: str
    item_type: str  # FINDING, EVIDENCE, RISK_FACTOR, IOC, DATAFLOW, BEHAVIOR, TIMELINE_EVENT, REPORT_SECTION
    item_id: str
    label: str = ""
    created_at: str = ""

    model_config = ConfigDict(frozen=True, from_attributes=True)


class CaseTaskDTO(BaseModel):
    """Workflow task inside an investigation case."""
    task_id: str
    case_id: str
    title: str
    description: str = ""
    assigned_to: str = ""
    priority: str = "MEDIUM"  # CRITICAL, HIGH, MEDIUM, LOW
    status: str = "TODO"  # TODO, IN_PROGRESS, BLOCKED, COMPLETED, CANCELLED
    due_at: Optional[str] = None
    created_at: str = ""
    completed_at: Optional[str] = None

    model_config = ConfigDict(frozen=True, from_attributes=True)


class CaseShareDTO(BaseModel):
    """Secure ephemeral sharing record."""
    share_id: str
    report_id: str
    case_id: Optional[str] = None
    created_by: str
    expires_at: str
    permission: str = "VIEW_ONLY"  # VIEW_ONLY, DOWNLOAD_ALLOWED, EVIDENCE_VIEW, TECHNICAL_VIEW, FULL_ACCESS
    status: str = "ACTIVE"  # ACTIVE, EXPIRED, REVOKED
    access_limit: int = 100
    access_count: int = 0
    created_at: str = ""
    revoked_at: Optional[str] = None

    model_config = ConfigDict(frozen=True, from_attributes=True)


class InvestigationAnnotationDTO(BaseModel):
    """Finding or evidence tag / annotation."""
    annotation_id: str
    target_type: str  # FINDING, EVIDENCE
    target_id: str
    author_id: str
    tag: str
    comment: str = ""
    created_at: str = ""

    model_config = ConfigDict(frozen=True, from_attributes=True)


# ---------------------------------------------------------------------------
# Sections 13-16: Evidence Graph DTOs
# ---------------------------------------------------------------------------

class GraphNodeDTO(BaseModel):
    id: str
    label: str
    type: str  # ANALYSIS, FINDING, EVIDENCE, RISK_FACTOR, IOC, DOMAIN, IP, PACKAGE, PERMISSION, API, BEHAVIOR, DATAFLOW, THREAT_INTEL, RECOMMENDATION, MODULE
    category: str = "DEFAULT"
    confidence: str = "HIGH"
    risk_contribution: float = 0.0
    properties: Dict[str, Any] = Field(default_factory=dict)

    model_config = ConfigDict(frozen=True, from_attributes=True)


class GraphEdgeDTO(BaseModel):
    id: str
    source: str
    target: str
    relationship: str  # SUPPORTS, CONTRIBUTES_TO, DERIVED_FROM, CORRELATED_WITH, MATCHES, FLOWS_TO, TRIGGERS, MITIGATED_BY, CONTRADICTS, SOURCE_OF
    resolution_status: str = "RESOLVED"  # RESOLVED, PARTIAL, UNKNOWN
    confidence: str = "HIGH"
    metadata: Dict[str, Any] = Field(default_factory=dict)

    model_config = ConfigDict(frozen=True, from_attributes=True)


class InvestigationGraphResponseDTO(BaseModel):
    analysis_id: str
    nodes: List[GraphNodeDTO] = Field(default_factory=list)
    edges: List[GraphEdgeDTO] = Field(default_factory=list)
    total_nodes: int = 0
    total_edges: int = 0
    truncated: bool = False
    next_cursor: Optional[str] = None

    model_config = ConfigDict(frozen=True, from_attributes=True)


# ---------------------------------------------------------------------------
# Sections 19-20: Timeline DTOs
# ---------------------------------------------------------------------------

class TimelineEventDTO(BaseModel):
    event_id: str
    analysis_id: str
    timestamp: str
    event_type: str  # ANALYSIS_STARTED, FINDING_CREATED, EVIDENCE_OBSERVED, THREAT_MATCH, RISK_ASSESSMENT, REPORT_GENERATED, ANNOTATION_ADDED, CASE_UPDATED, ARTIFACT_EXPORTED, VERIFICATION_EVENT
    title: str
    description: str
    severity: str = "INFORMATIONAL"
    source_module: str = "SYSTEM"
    related_entity_id: Optional[str] = None

    model_config = ConfigDict(frozen=True, from_attributes=True)


class TimelineResponseDTO(BaseModel):
    analysis_id: str
    events: List[TimelineEventDTO] = Field(default_factory=list)
    total_events: int = 0

    model_config = ConfigDict(frozen=True, from_attributes=True)


# ---------------------------------------------------------------------------
# Section 17-18: Cross-Modal Correlation DTOs
# ---------------------------------------------------------------------------

class InvestigationCorrelationDTO(BaseModel):
    correlation_id: str
    case_id: str
    source_analysis_id: str
    target_analysis_id: str
    source_module: str
    target_module: str
    source_finding_id: str
    target_finding_id: str
    relationship: str
    confidence: str = "HIGH"
    evidence_reference: str = ""
    created_at: str = ""

    model_config = ConfigDict(frozen=True, from_attributes=True)


class CrossModalCorrelationResponseDTO(BaseModel):
    case_id: str
    correlations: List[InvestigationCorrelationDTO] = Field(default_factory=list)
    total_correlations: int = 0

    model_config = ConfigDict(frozen=True, from_attributes=True)


# ---------------------------------------------------------------------------
# Sections 52-54: Search DTOs
# ---------------------------------------------------------------------------

class InvestigationSearchRequestDTO(BaseModel):
    query: str
    case_id: Optional[str] = None
    analysis_id: Optional[str] = None
    object_types: List[str] = Field(default_factory=list)  # FINDING, EVIDENCE, IOC, DOMAIN, NOTE, BEHAVIOR, DATAFLOW
    limit: int = 50
    offset: int = 0

    model_config = ConfigDict(frozen=True, from_attributes=True)


class InvestigationSearchResultDTO(BaseModel):
    object_type: str
    object_id: str
    title: str
    summary: str
    risk_reference: Optional[str] = None
    timestamp: str
    source_module: str
    case_id: Optional[str] = None

    model_config = ConfigDict(frozen=True, from_attributes=True)


class InvestigationSearchResponseDTO(BaseModel):
    query: str
    results: List[InvestigationSearchResultDTO] = Field(default_factory=list)
    total_results: int = 0

    model_config = ConfigDict(frozen=True, from_attributes=True)


# ---------------------------------------------------------------------------
# Section 39-43: Role-Aware View DTOs
# ---------------------------------------------------------------------------

class RoleAwareViewDTO(BaseModel):
    role: str  # EXECUTIVE, ANALYST, TECHNICAL, AUDITOR, ADMIN
    visible_panels: List[str] = Field(default_factory=list)
    show_raw_technical_data: bool = False
    show_audit_metadata: bool = False
    show_provenance_links: bool = True
    permissions: List[str] = Field(default_factory=list)

    model_config = ConfigDict(frozen=True, from_attributes=True)


class SavedViewDTO(BaseModel):
    view_id: str
    user_id: str
    name: str
    description: str = ""
    view_config: Dict[str, Any] = Field(default_factory=dict)
    created_at: str = ""

    model_config = ConfigDict(frozen=True, from_attributes=True)


class InvestigationAuditEventDTO(BaseModel):
    event_id: str
    user_id: str
    case_id: Optional[str] = None
    analysis_id: Optional[str] = None
    action: str
    object_type: str
    object_id: str
    ip_address: str = "127.0.0.1"
    timestamp: str = ""

    model_config = ConfigDict(frozen=True, from_attributes=True)
