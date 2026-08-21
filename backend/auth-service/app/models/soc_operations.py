"""SQLAlchemy 2.0 ORM Models for SOC Intelligence, Alert Correlation, Incident Response & SOAR (Phase 4.0 Part 7)."""

from typing import List, Dict, Any, Optional
from datetime import datetime, timezone
import uuid
from sqlalchemy import (
    Column,
    String,
    Integer,
    Float,
    Boolean,
    DateTime,
    Text,
    ForeignKey,
    JSON,
    Index,
)
from sqlalchemy.orm import relationship
from app.models.base import Base


class SOCAlertModel(Base):
    __tablename__ = "soc_alerts"

    alert_id = Column(String(64), primary_key=True, default=lambda: f"soc_alt_{uuid.uuid4().hex[:12]}")
    source_alert_id = Column(String(64), nullable=True, index=True)
    source_system = Column(String(64), nullable=False, default="INTERNAL_DETECTOR")
    alert_type = Column(String(64), nullable=False, index=True)
    category = Column(String(64), nullable=False, default="OTHER", index=True)
    subcategory = Column(String(64), nullable=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    severity = Column(String(32), nullable=False, default="MEDIUM", index=True)
    priority = Column(String(32), nullable=False, default="MEDIUM", index=True)
    confidence = Column(String(32), nullable=False, default="HIGH")
    status = Column(String(32), nullable=False, default="NEW", index=True)
    entity_ids = Column(JSON, nullable=False, default=list)
    finding_ids = Column(JSON, nullable=False, default=list)
    evidence_ids = Column(JSON, nullable=False, default=list)
    relationship_ids = Column(JSON, nullable=False, default=list)
    campaign_id = Column(String(64), nullable=True, index=True)
    attack_chain_id = Column(String(64), nullable=True, index=True)
    case_id = Column(String(64), nullable=True, index=True)
    incident_id = Column(String(64), nullable=True, index=True)
    organization_id = Column(String(64), nullable=True, index=True)
    raw_payload = Column(JSON, nullable=False, default=dict)
    first_seen = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    last_seen = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)


class AlertClusterModel(Base):
    __tablename__ = "alert_clusters"

    cluster_id = Column(String(64), primary_key=True, default=lambda: f"clst_{uuid.uuid4().hex[:12]}")
    alert_ids = Column(JSON, nullable=False, default=list)
    entity_ids = Column(JSON, nullable=False, default=list)
    campaign_id = Column(String(64), nullable=True, index=True)
    confidence = Column(Float, nullable=False, default=1.0)
    cluster_type = Column(String(64), nullable=False, default="SAME_ENTITY", index=True)
    first_seen = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    last_seen = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    status = Column(String(32), nullable=False, default="ACTIVE", index=True)
    organization_id = Column(String(64), nullable=True, index=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class SecurityIncidentModel(Base):
    __tablename__ = "soc_security_incidents"

    incident_id = Column(String(64), primary_key=True, default=lambda: f"inc_{uuid.uuid4().hex[:12]}")
    incident_number = Column(String(32), nullable=False, unique=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    incident_type = Column(String(64), nullable=False, default="UNKNOWN_INCIDENT", index=True)
    severity = Column(String(32), nullable=False, default="MEDIUM", index=True)
    priority = Column(String(32), nullable=False, default="MEDIUM", index=True)
    confidence = Column(String(32), nullable=False, default="HIGH")
    status = Column(String(32), nullable=False, default="NEW", index=True)
    owner_id = Column(String(64), nullable=True, index=True)
    team_id = Column(String(64), nullable=True, index=True)
    source_alert_count = Column(Integer, nullable=False, default=0)
    entity_count = Column(Integer, nullable=False, default=0)
    finding_count = Column(Integer, nullable=False, default=0)
    evidence_count = Column(Integer, nullable=False, default=0)
    campaign_id = Column(String(64), nullable=True, index=True)
    attack_chain_id = Column(String(64), nullable=True, index=True)
    case_id = Column(String(64), nullable=True, index=True)
    incident_fingerprint = Column(String(128), nullable=False, default="", index=True)
    organization_id = Column(String(64), nullable=True, index=True)
    first_seen = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    last_seen = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    detected_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    acknowledged_at = Column(DateTime(timezone=True), nullable=True)
    contained_at = Column(DateTime(timezone=True), nullable=True)
    resolved_at = Column(DateTime(timezone=True), nullable=True)
    closed_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)


class IncidentAlertLinkModel(Base):
    __tablename__ = "soc_incident_alerts"

    id = Column(String(64), primary_key=True, default=lambda: f"ial_{uuid.uuid4().hex[:12]}")
    incident_id = Column(String(64), ForeignKey("soc_security_incidents.incident_id", ondelete="CASCADE"), nullable=False, index=True)
    alert_id = Column(String(64), ForeignKey("soc_alerts.alert_id", ondelete="CASCADE"), nullable=False, index=True)
    linked_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class IncidentEntityLinkModel(Base):
    __tablename__ = "soc_incident_entities"

    id = Column(String(64), primary_key=True, default=lambda: f"iel_{uuid.uuid4().hex[:12]}")
    incident_id = Column(String(64), ForeignKey("soc_security_incidents.incident_id", ondelete="CASCADE"), nullable=False, index=True)
    entity_id = Column(String(64), nullable=False, index=True)
    role = Column(String(64), nullable=False, default="TARGET")
    linked_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class IncidentFindingLinkModel(Base):
    __tablename__ = "soc_incident_findings"

    id = Column(String(64), primary_key=True, default=lambda: f"ifl_{uuid.uuid4().hex[:12]}")
    incident_id = Column(String(64), ForeignKey("soc_security_incidents.incident_id", ondelete="CASCADE"), nullable=False, index=True)
    finding_id = Column(String(64), nullable=False, index=True)
    linked_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class IncidentEvidenceLinkModel(Base):
    __tablename__ = "soc_incident_evidence"

    id = Column(String(64), primary_key=True, default=lambda: f"iev_{uuid.uuid4().hex[:12]}")
    incident_id = Column(String(64), ForeignKey("soc_security_incidents.incident_id", ondelete="CASCADE"), nullable=False, index=True)
    evidence_id = Column(String(64), nullable=False, index=True)
    linked_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class IncidentTimelineModel(Base):
    __tablename__ = "soc_incident_timeline"

    timeline_event_id = Column(String(64), primary_key=True, default=lambda: f"tle_{uuid.uuid4().hex[:12]}")
    incident_id = Column(String(64), ForeignKey("soc_security_incidents.incident_id", ondelete="CASCADE"), nullable=False, index=True)
    event_type = Column(String(64), nullable=False, index=True)
    source = Column(String(64), nullable=False, default="SOC_AUTOMATION")
    timestamp = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False, index=True)
    actor = Column(String(64), nullable=False, default="SYSTEM")
    description = Column(Text, nullable=False)
    entity_ids = Column(JSON, nullable=False, default=list)
    evidence_ids = Column(JSON, nullable=False, default=list)
    alert_id = Column(String(64), nullable=True)
    action_id = Column(String(64), nullable=True)
    provenance = Column(String(255), nullable=False, default="")


class IncidentAssignmentModel(Base):
    __tablename__ = "soc_incident_assignments"

    assignment_id = Column(String(64), primary_key=True, default=lambda: f"asgn_{uuid.uuid4().hex[:12]}")
    incident_id = Column(String(64), ForeignKey("soc_security_incidents.incident_id", ondelete="CASCADE"), nullable=False, index=True)
    analyst_id = Column(String(64), nullable=False, index=True)
    team_id = Column(String(64), nullable=True, index=True)
    assigned_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    assigned_by = Column(String(64), nullable=False, default="SOC_LEAD")
    reason = Column(String(255), nullable=False, default="Automated routing")
    status = Column(String(32), nullable=False, default="ACTIVE", index=True)


class IncidentSLAModel(Base):
    __tablename__ = "soc_incident_sla"

    sla_id = Column(String(64), primary_key=True, default=lambda: f"sla_{uuid.uuid4().hex[:12]}")
    incident_id = Column(String(64), ForeignKey("soc_security_incidents.incident_id", ondelete="CASCADE"), nullable=False, index=True)
    ack_deadline = Column(DateTime(timezone=True), nullable=False)
    triage_deadline = Column(DateTime(timezone=True), nullable=False)
    containment_deadline = Column(DateTime(timezone=True), nullable=False)
    resolution_deadline = Column(DateTime(timezone=True), nullable=False)
    status = Column(String(32), nullable=False, default="ON_TRACK", index=True)
    time_to_acknowledge_seconds = Column(Float, nullable=True)
    time_to_triage_seconds = Column(Float, nullable=True)
    time_to_containment_seconds = Column(Float, nullable=True)
    time_to_resolution_seconds = Column(Float, nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class ResponsePlaybookModel(Base):
    __tablename__ = "soc_response_playbooks"

    playbook_id = Column(String(64), primary_key=True, default=lambda: f"pbk_{uuid.uuid4().hex[:12]}")
    name = Column(String(128), nullable=False, index=True)
    current_version = Column(Integer, nullable=False, default=1)
    description = Column(Text, nullable=False)
    incident_types = Column(JSON, nullable=False, default=list)
    required_permissions = Column(JSON, nullable=False, default=list)
    approval_policy = Column(JSON, nullable=False, default=dict)
    enabled = Column(Boolean, nullable=False, default=True, index=True)
    organization_id = Column(String(64), nullable=True, index=True)
    created_by = Column(String(64), nullable=False, default="SOC_ADMIN")
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)


class ResponsePlaybookVersionModel(Base):
    __tablename__ = "soc_response_playbook_versions"

    version_id = Column(String(64), primary_key=True, default=lambda: f"pbv_{uuid.uuid4().hex[:12]}")
    playbook_id = Column(String(64), ForeignKey("soc_response_playbooks.playbook_id", ondelete="CASCADE"), nullable=False, index=True)
    version_number = Column(Integer, nullable=False, index=True)
    content_hash = Column(String(128), nullable=False)
    author = Column(String(64), nullable=False, default="SOC_ADMIN")
    steps_snapshot = Column(JSON, nullable=False, default=list)
    published_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class ResponsePlaybookStepModel(Base):
    __tablename__ = "soc_response_playbook_steps"

    step_id = Column(String(64), primary_key=True, default=lambda: f"step_{uuid.uuid4().hex[:12]}")
    playbook_id = Column(String(64), ForeignKey("soc_response_playbooks.playbook_id", ondelete="CASCADE"), nullable=False, index=True)
    step_number = Column(Integer, nullable=False, index=True)
    name = Column(String(128), nullable=False)
    description = Column(Text, nullable=False)
    action_type = Column(String(64), nullable=False, index=True)
    risk_level = Column(String(32), nullable=False, default="MEDIUM")
    approval_required = Column(Boolean, nullable=False, default=True)
    dry_run_supported = Column(Boolean, nullable=False, default=True)
    rollback_supported = Column(Boolean, nullable=False, default=False)
    timeout = Column(Integer, nullable=False, default=30)
    retry_policy = Column(JSON, nullable=False, default=dict)
    conditions = Column(JSON, nullable=False, default=dict)


class ResponseActionModel(Base):
    __tablename__ = "soc_response_actions"

    action_id = Column(String(64), primary_key=True, default=lambda: f"act_{uuid.uuid4().hex[:12]}")
    incident_id = Column(String(64), ForeignKey("soc_security_incidents.incident_id", ondelete="CASCADE"), nullable=False, index=True)
    playbook_id = Column(String(64), nullable=True, index=True)
    playbook_version = Column(Integer, nullable=False, default=1)
    step_id = Column(String(64), nullable=True)
    action_type = Column(String(64), nullable=False, index=True)
    target = Column(String(255), nullable=False, index=True)
    target_type = Column(String(64), nullable=False, default="DOMAIN")
    requested_by = Column(String(64), nullable=False, index=True)
    approved_by = Column(String(64), nullable=True, index=True)
    approval_status = Column(String(32), nullable=False, default="PENDING", index=True)
    dry_run = Column(Boolean, nullable=False, default=False)
    status = Column(String(32), nullable=False, default="QUEUED", index=True)
    reason = Column(Text, nullable=False)
    evidence_ids = Column(JSON, nullable=False, default=list)
    idempotency_key = Column(String(128), nullable=False, index=True)
    started_at = Column(DateTime(timezone=True), nullable=True)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    error_code = Column(String(64), nullable=True)
    result_reference = Column(String(255), nullable=True)
    rollback_action_id = Column(String(64), nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class ResponseApprovalModel(Base):
    __tablename__ = "soc_response_approvals"

    approval_id = Column(String(64), primary_key=True, default=lambda: f"appr_{uuid.uuid4().hex[:12]}")
    action_id = Column(String(64), ForeignKey("soc_response_actions.action_id", ondelete="CASCADE"), nullable=False, index=True)
    incident_id = Column(String(64), nullable=False, index=True)
    requested_by = Column(String(64), nullable=False, index=True)
    approver_scope = Column(String(64), nullable=False, default="SOC_LEAD")
    reason = Column(Text, nullable=False)
    risk = Column(String(32), nullable=False, default="HIGH")
    evidence = Column(JSON, nullable=False, default=list)
    expires_at = Column(DateTime(timezone=True), nullable=False)
    status = Column(String(32), nullable=False, default="PENDING", index=True)
    decision_reason = Column(Text, nullable=True)
    decided_by = Column(String(64), nullable=True, index=True)
    decided_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class ResponseSimulationModel(Base):
    __tablename__ = "soc_response_simulations"

    simulation_id = Column(String(64), primary_key=True, default=lambda: f"sim_{uuid.uuid4().hex[:12]}")
    action_id = Column(String(64), ForeignKey("soc_response_actions.action_id", ondelete="CASCADE"), nullable=False, index=True)
    target = Column(String(255), nullable=False)
    provider = Column(String(64), nullable=False)
    expected_effect = Column(Text, nullable=False)
    risk_assessment = Column(Text, nullable=False)
    required_permissions = Column(JSON, nullable=False, default=list)
    rollback_supported = Column(Boolean, nullable=False, default=False)
    side_effects = Column(JSON, nullable=False, default=list)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class ResponseExecutionModel(Base):
    __tablename__ = "soc_response_executions"

    execution_id = Column(String(64), primary_key=True, default=lambda: f"exec_{uuid.uuid4().hex[:12]}")
    action_id = Column(String(64), ForeignKey("soc_response_actions.action_id", ondelete="CASCADE"), nullable=False, index=True)
    provider_name = Column(String(64), nullable=False, index=True)
    status = Column(String(32), nullable=False, index=True)
    request_payload = Column(JSON, nullable=False, default=dict)
    response_payload = Column(JSON, nullable=False, default=dict)
    execution_time_ms = Column(Float, nullable=False, default=0.0)
    error_message = Column(Text, nullable=True)
    executed_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class ResponseVerificationModel(Base):
    __tablename__ = "soc_response_verifications"

    verification_id = Column(String(64), primary_key=True, default=lambda: f"ver_{uuid.uuid4().hex[:12]}")
    action_id = Column(String(64), ForeignKey("soc_response_actions.action_id", ondelete="CASCADE"), nullable=False, index=True)
    target = Column(String(255), nullable=False)
    verification_status = Column(String(32), nullable=False, index=True)
    evidence_gathered = Column(JSON, nullable=False, default=list)
    observations = Column(Text, nullable=False)
    verified_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class ResponseRollbackModel(Base):
    __tablename__ = "soc_response_rollbacks"

    rollback_id = Column(String(64), primary_key=True, default=lambda: f"rol_{uuid.uuid4().hex[:12]}")
    action_id = Column(String(64), ForeignKey("soc_response_actions.action_id", ondelete="CASCADE"), nullable=False, index=True)
    target = Column(String(255), nullable=False)
    rollback_status = Column(String(32), nullable=False, index=True)
    reason = Column(Text, nullable=False)
    executed_by = Column(String(64), nullable=False)
    error_message = Column(Text, nullable=True)
    executed_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class ResponsePolicyModel(Base):
    __tablename__ = "soc_response_policies"

    policy_id = Column(String(64), primary_key=True, default=lambda: f"pol_{uuid.uuid4().hex[:12]}")
    name = Column(String(128), nullable=False, index=True)
    action_type = Column(String(64), nullable=False, index=True)
    min_incident_severity = Column(String(32), nullable=False, default="HIGH")
    automation_level = Column(String(32), nullable=False, default="APPROVAL_REQUIRED", index=True)
    protected_targets = Column(JSON, nullable=False, default=list)
    allow_auto_approval = Column(Boolean, nullable=False, default=False)
    organization_id = Column(String(64), nullable=True, index=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class ResponseProviderRegistryModel(Base):
    __tablename__ = "soc_response_provider_registry"

    provider_id = Column(String(64), primary_key=True, default=lambda: f"prv_{uuid.uuid4().hex[:12]}")
    name = Column(String(64), nullable=False, unique=True, index=True)
    provider_type = Column(String(64), nullable=False, index=True)
    supported_actions = Column(JSON, nullable=False, default=list)
    endpoint = Column(String(255), nullable=True)
    health_status = Column(String(32), nullable=False, default="HEALTHY", index=True)
    last_health_check = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class EvidenceCollectionRecordModel(Base):
    __tablename__ = "soc_evidence_collection_records"

    collection_id = Column(String(64), primary_key=True, default=lambda: f"evc_{uuid.uuid4().hex[:12]}")
    incident_id = Column(String(64), ForeignKey("soc_security_incidents.incident_id", ondelete="CASCADE"), nullable=False, index=True)
    source = Column(String(128), nullable=False)
    collector_id = Column(String(64), nullable=False, index=True)
    evidence_type = Column(String(64), nullable=False, index=True)
    sha256_hash = Column(String(64), nullable=False, index=True)
    storage_reference = Column(String(255), nullable=False)
    integrity_status = Column(String(32), nullable=False, default="VERIFIED", index=True)
    collection_method = Column(String(64), nullable=False, default="SECURE_API_PULL")
    access_log = Column(JSON, nullable=False, default=list)
    collected_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class IncidentMergeModel(Base):
    __tablename__ = "soc_incident_merges"

    merge_id = Column(String(64), primary_key=True, default=lambda: f"mrg_{uuid.uuid4().hex[:12]}")
    primary_incident_id = Column(String(64), ForeignKey("soc_security_incidents.incident_id", ondelete="CASCADE"), nullable=False, index=True)
    merged_incident_ids = Column(JSON, nullable=False, default=list)
    merged_by = Column(String(64), nullable=False, index=True)
    reason = Column(Text, nullable=False)
    status = Column(String(32), nullable=False, default="MERGED")
    merged_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class IncidentSplitModel(Base):
    __tablename__ = "soc_incident_splits"

    split_id = Column(String(64), primary_key=True, default=lambda: f"splt_{uuid.uuid4().hex[:12]}")
    original_incident_id = Column(String(64), ForeignKey("soc_security_incidents.incident_id", ondelete="CASCADE"), nullable=False, index=True)
    new_incident_ids = Column(JSON, nullable=False, default=list)
    split_by = Column(String(64), nullable=False, index=True)
    reason = Column(Text, nullable=False)
    split_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
