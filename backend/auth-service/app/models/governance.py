"""SQLAlchemy 2.0 ORM Models for Enterprise Governance (Phase 4.0 Part 8 — Section 84).

Defines database models for organizations, users, RBAC, ABAC, policies, retention,
legal holds, deletion, privacy, exports, audit events, compliance, sessions, and API keys.
"""

from datetime import datetime, timezone
from typing import Optional, List, Dict, Any
from sqlalchemy import (
    String,
    Text,
    Integer,
    Float,
    Boolean,
    DateTime,
    ForeignKey,
    Index,
    JSON,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base


class OrganizationModel(Base):
    """Organization tenant master table (Section 2)."""
    __tablename__ = "gov_organizations"

    organization_id: Mapped[str] = mapped_column(String(64), primary_key=True)
    organization_name: Mapped[str] = mapped_column(String(255), nullable=False)
    slug: Mapped[str] = mapped_column(String(128), unique=True, index=True, nullable=False)
    status: Mapped[str] = mapped_column(String(32), default="ACTIVE", index=True)
    plan: Mapped[str] = mapped_column(String(64), default="ENTERPRISE")
    region: Mapped[str] = mapped_column(String(64), default="ap-south-1")
    timezone: Mapped[str] = mapped_column(String(64), default="Asia/Kolkata")
    data_residency: Mapped[str] = mapped_column(String(32), default="IN")
    security_profile: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict)
    compliance_profile: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))


class OrganizationUserModel(Base):
    """Organization user membership and lifecycle (Section 6-7)."""
    __tablename__ = "gov_organization_users"

    user_id: Mapped[str] = mapped_column(String(64), primary_key=True)
    organization_id: Mapped[str] = mapped_column(String(64), ForeignKey("gov_organizations.organization_id", ondelete="CASCADE"), index=True)
    email: Mapped[str] = mapped_column(String(255), index=True, nullable=False)
    full_name: Mapped[str] = mapped_column(String(255), default="")
    status: Mapped[str] = mapped_column(String(32), default="ACTIVE", index=True)
    roles: Mapped[List[str]] = mapped_column(JSON, default=list)
    mfa_enforced: Mapped[bool] = mapped_column(Boolean, default=False)
    mfa_enabled: Mapped[bool] = mapped_column(Boolean, default=False)
    last_login_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))


class RoleModel(Base):
    """RBAC Role definitions (Section 8)."""
    __tablename__ = "gov_roles"

    role_id: Mapped[str] = mapped_column(String(64), primary_key=True)
    organization_id: Mapped[Optional[str]] = mapped_column(String(64), nullable=True, index=True)
    name: Mapped[str] = mapped_column(String(128), nullable=False)
    description: Mapped[str] = mapped_column(Text, default="")
    system_role: Mapped[bool] = mapped_column(Boolean, default=False)
    permissions: Mapped[List[str]] = mapped_column(JSON, default=list)
    scope: Mapped[str] = mapped_column(String(64), default="ORGANIZATION")
    version: Mapped[int] = mapped_column(Integer, default=1)
    status: Mapped[str] = mapped_column(String(32), default="ACTIVE")
    created_by: Mapped[str] = mapped_column(String(255), default="SYSTEM")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))


class RoleVersionModel(Base):
    """Immutable role version snapshot (Section 8)."""
    __tablename__ = "gov_role_versions"

    version_id: Mapped[str] = mapped_column(String(64), primary_key=True)
    role_id: Mapped[str] = mapped_column(String(64), ForeignKey("gov_roles.role_id", ondelete="CASCADE"), index=True)
    version_number: Mapped[int] = mapped_column(Integer, nullable=False)
    content_hash: Mapped[str] = mapped_column(String(64), nullable=False)
    permissions: Mapped[List[str]] = mapped_column(JSON, default=list)
    created_by: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


class PermissionModel(Base):
    """Master permission catalog (Section 11)."""
    __tablename__ = "gov_permissions"

    permission_id: Mapped[str] = mapped_column(String(64), primary_key=True)
    resource: Mapped[str] = mapped_column(String(128), index=True, nullable=False)
    action: Mapped[str] = mapped_column(String(128), index=True, nullable=False)
    description: Mapped[str] = mapped_column(Text, default="")
    scope: Mapped[str] = mapped_column(String(64), default="ORGANIZATION")


class GovernancePolicyModel(Base):
    """Enterprise governance & security policies (Section 19)."""
    __tablename__ = "gov_policies"

    policy_id: Mapped[str] = mapped_column(String(64), primary_key=True)
    organization_id: Mapped[str] = mapped_column(String(64), ForeignKey("gov_organizations.organization_id", ondelete="CASCADE"), index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, default="")
    policy_type: Mapped[str] = mapped_column(String(64), index=True, default="ACCESS_CONTROL")
    version: Mapped[int] = mapped_column(Integer, default=1)
    status: Mapped[str] = mapped_column(String(32), default="ACTIVE", index=True)
    rules: Mapped[List[Dict[str, Any]]] = mapped_column(JSON, default=list)
    priority: Mapped[int] = mapped_column(Integer, default=100)
    created_by: Mapped[str] = mapped_column(String(255), default="ADMIN")
    approved_by: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    effective_from: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    effective_until: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))


class PolicyVersionModel(Base):
    """Immutable policy version snapshot (Section 21)."""
    __tablename__ = "gov_policy_versions"

    version_id: Mapped[str] = mapped_column(String(64), primary_key=True)
    policy_id: Mapped[str] = mapped_column(String(64), ForeignKey("gov_policies.policy_id", ondelete="CASCADE"), index=True)
    version_number: Mapped[int] = mapped_column(Integer, nullable=False)
    content_hash: Mapped[str] = mapped_column(String(64), nullable=False)
    rules: Mapped[List[Dict[str, Any]]] = mapped_column(JSON, default=list)
    created_by: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


class RetentionPolicyModel(Base):
    """Data retention rules (Section 32)."""
    __tablename__ = "gov_retention_policies"

    policy_id: Mapped[str] = mapped_column(String(64), primary_key=True)
    organization_id: Mapped[str] = mapped_column(String(64), ForeignKey("gov_organizations.organization_id", ondelete="CASCADE"), index=True)
    resource_type: Mapped[str] = mapped_column(String(64), index=True, nullable=False)
    classification: Mapped[str] = mapped_column(String(32), default="INTERNAL")
    retention_period_days: Mapped[int] = mapped_column(Integer, default=365)
    deletion_strategy: Mapped[str] = mapped_column(String(32), default="SOFT_DELETE")
    legal_hold_behavior: Mapped[str] = mapped_column(String(64), default="SHIELD_FROM_DELETION")
    archive_strategy: Mapped[str] = mapped_column(String(64), default="COLD_STORAGE")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))


class LegalHoldModel(Base):
    """Legal hold records shielding resources from deletion (Section 34)."""
    __tablename__ = "gov_legal_holds"

    hold_id: Mapped[str] = mapped_column(String(64), primary_key=True)
    organization_id: Mapped[str] = mapped_column(String(64), ForeignKey("gov_organizations.organization_id", ondelete="CASCADE"), index=True)
    resource_type: Mapped[str] = mapped_column(String(64), index=True, nullable=False)
    resource_id: Mapped[str] = mapped_column(String(128), index=True, nullable=False)
    reason: Mapped[str] = mapped_column(Text, nullable=False)
    created_by: Mapped[str] = mapped_column(String(255), nullable=False)
    approved_by: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    status: Mapped[str] = mapped_column(String(32), default="ACTIVE", index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    released_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)


class DeletionRequestModel(Base):
    """Data deletion governance records (Section 36)."""
    __tablename__ = "gov_deletion_requests"

    deletion_id: Mapped[str] = mapped_column(String(64), primary_key=True)
    organization_id: Mapped[str] = mapped_column(String(64), ForeignKey("gov_organizations.organization_id", ondelete="CASCADE"), index=True)
    resource_type: Mapped[str] = mapped_column(String(64), index=True, nullable=False)
    resource_id: Mapped[str] = mapped_column(String(128), index=True, nullable=False)
    requested_by: Mapped[str] = mapped_column(String(255), nullable=False)
    approved_by: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    deletion_type: Mapped[str] = mapped_column(String(64), default="PRIVACY_REQUEST")
    status: Mapped[str] = mapped_column(String(32), default="PENDING", index=True)
    verification_evidence: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)


class PrivacyRequestModel(Base):
    """DPDP and privacy requests (Section 40)."""
    __tablename__ = "gov_privacy_requests"

    request_id: Mapped[str] = mapped_column(String(64), primary_key=True)
    organization_id: Mapped[str] = mapped_column(String(64), ForeignKey("gov_organizations.organization_id", ondelete="CASCADE"), index=True)
    data_principal_id: Mapped[str] = mapped_column(String(128), index=True, nullable=False)
    request_type: Mapped[str] = mapped_column(String(32), default="ACCESS")
    status: Mapped[str] = mapped_column(String(32), default="PENDING", index=True)
    identity_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    legal_hold_checked: Mapped[bool] = mapped_column(Boolean, default=False)
    reason: Mapped[str] = mapped_column(Text, default="")
    assigned_to: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)


class DataExportModel(Base):
    """Controlled data exports with manifests (Section 42-44)."""
    __tablename__ = "gov_data_exports"

    export_id: Mapped[str] = mapped_column(String(64), primary_key=True)
    organization_id: Mapped[str] = mapped_column(String(64), ForeignKey("gov_organizations.organization_id", ondelete="CASCADE"), index=True)
    requester_id: Mapped[str] = mapped_column(String(255), nullable=False)
    scope: Mapped[str] = mapped_column(String(128), default="CASE")
    resource_count: Mapped[int] = mapped_column(Integer, default=0)
    classification: Mapped[str] = mapped_column(String(32), default="CONFIDENTIAL")
    integrity_hash: Mapped[str] = mapped_column(String(64), nullable=False)
    status: Mapped[str] = mapped_column(String(32), default="READY", index=True)
    download_token: Mapped[str] = mapped_column(String(128), unique=True, index=True)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


class AuditEventModel(Base):
    """Append-only audit event logging (Section 46-49)."""
    __tablename__ = "gov_audit_events"

    audit_id: Mapped[str] = mapped_column(String(64), primary_key=True)
    organization_id: Mapped[str] = mapped_column(String(64), ForeignKey("gov_organizations.organization_id", ondelete="CASCADE"), index=True)
    actor_type: Mapped[str] = mapped_column(String(32), default="USER")
    actor_id: Mapped[str] = mapped_column(String(255), index=True, nullable=False)
    action: Mapped[str] = mapped_column(String(128), index=True, nullable=False)
    resource_type: Mapped[str] = mapped_column(String(128), index=True, nullable=False)
    resource_id: Mapped[str] = mapped_column(String(128), index=True, nullable=False)
    result: Mapped[str] = mapped_column(String(32), default="SUCCESS", index=True)
    reason: Mapped[str] = mapped_column(Text, default="")
    previous_hash: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    event_hash: Mapped[str] = mapped_column(String(64), nullable=False)
    session_reference: Mapped[Optional[str]] = mapped_column(String(128), nullable=True)
    request_id: Mapped[Optional[str]] = mapped_column(String(128), nullable=True)
    correlation_id: Mapped[Optional[str]] = mapped_column(String(128), nullable=True)
    policy_id: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    policy_version: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    metadata_payload: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict)
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)


class AuditIntegrityCheckpointModel(Base):
    """Cryptographic audit checkpoints (Section 49)."""
    __tablename__ = "gov_audit_integrity_checkpoints"

    checkpoint_id: Mapped[str] = mapped_column(String(64), primary_key=True)
    organization_id: Mapped[str] = mapped_column(String(64), ForeignKey("gov_organizations.organization_id", ondelete="CASCADE"), index=True)
    start_audit_id: Mapped[str] = mapped_column(String(64), nullable=False)
    end_audit_id: Mapped[str] = mapped_column(String(64), nullable=False)
    event_count: Mapped[int] = mapped_column(Integer, nullable=False)
    merkle_root_hash: Mapped[str] = mapped_column(String(64), nullable=False)
    verified: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


class GovernanceAlertModel(Base):
    """Administrative security and anomaly alerts (Section 51-52)."""
    __tablename__ = "gov_governance_alerts"

    alert_id: Mapped[str] = mapped_column(String(64), primary_key=True)
    organization_id: Mapped[str] = mapped_column(String(64), ForeignKey("gov_organizations.organization_id", ondelete="CASCADE"), index=True)
    alert_type: Mapped[str] = mapped_column(String(64), index=True, nullable=False)
    severity: Mapped[str] = mapped_column(String(32), default="HIGH")
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, default="")
    actor_id: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    affected_resource: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    status: Mapped[str] = mapped_column(String(32), default="ACTIVE", index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


class ComplianceFrameworkModel(Base):
    """Compliance framework definitions (Section 54)."""
    __tablename__ = "gov_compliance_frameworks"

    framework_id: Mapped[str] = mapped_column(String(64), primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    version: Mapped[str] = mapped_column(String(32), default="2024")
    jurisdiction: Mapped[str] = mapped_column(String(64), default="GLOBAL")
    description: Mapped[str] = mapped_column(Text, default="")
    control_count: Mapped[int] = mapped_column(Integer, default=0)
    status: Mapped[str] = mapped_column(String(32), default="ACTIVE")


class ComplianceControlModel(Base):
    """Framework control items (Section 55)."""
    __tablename__ = "gov_compliance_controls"

    control_id: Mapped[str] = mapped_column(String(64), primary_key=True)
    framework_id: Mapped[str] = mapped_column(String(64), ForeignKey("gov_compliance_frameworks.framework_id", ondelete="CASCADE"), index=True)
    control_code: Mapped[str] = mapped_column(String(64), index=True, nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, default="")
    requirement: Mapped[str] = mapped_column(Text, default="")
    implementation_status: Mapped[str] = mapped_column(String(32), default="NOT_ASSESSED")
    evidence_requirements: Mapped[List[str]] = mapped_column(JSON, default=list)
    owner: Mapped[str] = mapped_column(String(255), default="COMPLIANCE_LEAD")


class ComplianceEvidenceModel(Base):
    """Evidence linked to compliance controls (Section 57)."""
    __tablename__ = "gov_compliance_evidence"

    evidence_id: Mapped[str] = mapped_column(String(64), primary_key=True)
    control_id: Mapped[str] = mapped_column(String(64), ForeignKey("gov_compliance_controls.control_id", ondelete="CASCADE"), index=True)
    resource_type: Mapped[str] = mapped_column(String(64), nullable=False)
    resource_id: Mapped[str] = mapped_column(String(128), nullable=False)
    source: Mapped[str] = mapped_column(String(255), nullable=False)
    integrity_hash: Mapped[str] = mapped_column(String(64), nullable=False)
    valid_until: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    status: Mapped[str] = mapped_column(String(32), default="VERIFIED")
    collected_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


class ComplianceAssessmentModel(Base):
    """Compliance assessment runs and scores (Section 59)."""
    __tablename__ = "gov_compliance_assessments"

    assessment_id: Mapped[str] = mapped_column(String(64), primary_key=True)
    framework_id: Mapped[str] = mapped_column(String(64), ForeignKey("gov_compliance_frameworks.framework_id", ondelete="CASCADE"), index=True)
    organization_id: Mapped[str] = mapped_column(String(64), ForeignKey("gov_organizations.organization_id", ondelete="CASCADE"), index=True)
    status: Mapped[str] = mapped_column(String(32), default="COMPLETED")
    score_percentage: Mapped[float] = mapped_column(Float, default=0.0)
    control_count: Mapped[int] = mapped_column(Integer, default=0)
    implemented_count: Mapped[int] = mapped_column(Integer, default=0)
    partial_count: Mapped[int] = mapped_column(Integer, default=0)
    failed_count: Mapped[int] = mapped_column(Integer, default=0)
    exception_count: Mapped[int] = mapped_column(Integer, default=0)
    assessed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    assessor: Mapped[str] = mapped_column(String(255), default="AUTOMATED_GOVERNANCE_ENGINE")


class UserSessionModel(Base):
    """Active user sessions & device governance (Section 72-74)."""
    __tablename__ = "gov_user_sessions"

    session_id: Mapped[str] = mapped_column(String(64), primary_key=True)
    user_id: Mapped[str] = mapped_column(String(64), index=True, nullable=False)
    organization_id: Mapped[str] = mapped_column(String(64), ForeignKey("gov_organizations.organization_id", ondelete="CASCADE"), index=True)
    authentication_strength: Mapped[str] = mapped_column(String(64), default="PASSWORD")
    mfa_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    device_reference: Mapped[str] = mapped_column(String(255), default="Unknown")
    ip_reference: Mapped[str] = mapped_column(String(64), default="127.0.0.1")
    status: Mapped[str] = mapped_column(String(32), default="ACTIVE", index=True)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    last_seen: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


class ServiceAccountModel(Base):
    """Machine/Service accounts (Section 77)."""
    __tablename__ = "gov_service_accounts"

    service_account_id: Mapped[str] = mapped_column(String(64), primary_key=True)
    organization_id: Mapped[str] = mapped_column(String(64), ForeignKey("gov_organizations.organization_id", ondelete="CASCADE"), index=True)
    name: Mapped[str] = mapped_column(String(128), nullable=False)
    description: Mapped[str] = mapped_column(Text, default="")
    permissions: Mapped[List[str]] = mapped_column(JSON, default=list)
    status: Mapped[str] = mapped_column(String(32), default="ACTIVE", index=True)
    created_by: Mapped[str] = mapped_column(String(255), nullable=False)
    expires_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


class APIKeyModel(Base):
    """Secure hashed API keys (Section 78-79)."""
    __tablename__ = "gov_api_keys"

    key_id: Mapped[str] = mapped_column(String(64), primary_key=True)
    organization_id: Mapped[str] = mapped_column(String(64), ForeignKey("gov_organizations.organization_id", ondelete="CASCADE"), index=True)
    name: Mapped[str] = mapped_column(String(128), nullable=False)
    key_prefix: Mapped[str] = mapped_column(String(16), index=True, nullable=False)
    hashed_secret: Mapped[str] = mapped_column(String(128), nullable=False)  # SHA-256 hash of secret
    scope: Mapped[str] = mapped_column(String(64), default="ORGANIZATION")
    permissions: Mapped[List[str]] = mapped_column(JSON, default=list)
    status: Mapped[str] = mapped_column(String(32), default="ACTIVE", index=True)
    owner_id: Mapped[str] = mapped_column(String(255), nullable=False)
    expires_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    last_used_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
