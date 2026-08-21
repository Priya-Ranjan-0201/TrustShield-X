"""Alembic Migration 042 — Enterprise Governance, Advanced RBAC/ABAC, Policy Management, Compliance, Audit Intelligence, Data Governance & Regulatory Evidence (Phase 4.0 Part 8 — Section 84).

Revision ID: 042_enterprise_governance_schema
Revises: 041_soc_operations_schema
Create Date: 2026-08-14
"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "042_enterprise_governance_schema"
down_revision = "041_soc_operations_schema"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # 1. gov_organizations
    op.create_table(
        "gov_organizations",
        sa.Column("organization_id", sa.String(64), primary_key=True),
        sa.Column("organization_name", sa.String(255), nullable=False),
        sa.Column("slug", sa.String(128), unique=True, index=True, nullable=False),
        sa.Column("status", sa.String(32), default="ACTIVE", index=True),
        sa.Column("plan", sa.String(64), default="ENTERPRISE"),
        sa.Column("region", sa.String(64), default="ap-south-1"),
        sa.Column("timezone", sa.String(64), default="Asia/Kolkata"),
        sa.Column("data_residency", sa.String(32), default="IN"),
        sa.Column("security_profile", sa.JSON(), default=dict),
        sa.Column("compliance_profile", sa.JSON(), default=dict),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 2. gov_organization_users
    op.create_table(
        "gov_organization_users",
        sa.Column("user_id", sa.String(64), primary_key=True),
        sa.Column("organization_id", sa.String(64), sa.ForeignKey("gov_organizations.organization_id", ondelete="CASCADE"), index=True),
        sa.Column("email", sa.String(255), index=True, nullable=False),
        sa.Column("full_name", sa.String(255), default=""),
        sa.Column("status", sa.String(32), default="ACTIVE", index=True),
        sa.Column("roles", sa.JSON(), default=list),
        sa.Column("mfa_enforced", sa.Boolean(), default=False),
        sa.Column("mfa_enabled", sa.Boolean(), default=False),
        sa.Column("last_login_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 3. gov_roles
    op.create_table(
        "gov_roles",
        sa.Column("role_id", sa.String(64), primary_key=True),
        sa.Column("organization_id", sa.String(64), nullable=True, index=True),
        sa.Column("name", sa.String(128), nullable=False),
        sa.Column("description", sa.Text(), default=""),
        sa.Column("system_role", sa.Boolean(), default=False),
        sa.Column("permissions", sa.JSON(), default=list),
        sa.Column("scope", sa.String(64), default="ORGANIZATION"),
        sa.Column("version", sa.Integer(), default=1),
        sa.Column("status", sa.String(32), default="ACTIVE"),
        sa.Column("created_by", sa.String(255), default="SYSTEM"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 4. gov_role_versions
    op.create_table(
        "gov_role_versions",
        sa.Column("version_id", sa.String(64), primary_key=True),
        sa.Column("role_id", sa.String(64), sa.ForeignKey("gov_roles.role_id", ondelete="CASCADE"), index=True),
        sa.Column("version_number", sa.Integer(), nullable=False),
        sa.Column("content_hash", sa.String(64), nullable=False),
        sa.Column("permissions", sa.JSON(), default=list),
        sa.Column("created_by", sa.String(255), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 5. gov_permissions
    op.create_table(
        "gov_permissions",
        sa.Column("permission_id", sa.String(64), primary_key=True),
        sa.Column("resource", sa.String(128), index=True, nullable=False),
        sa.Column("action", sa.String(128), index=True, nullable=False),
        sa.Column("description", sa.Text(), default=""),
        sa.Column("scope", sa.String(64), default="ORGANIZATION"),
    )

    # 6. gov_policies
    op.create_table(
        "gov_policies",
        sa.Column("policy_id", sa.String(64), primary_key=True),
        sa.Column("organization_id", sa.String(64), sa.ForeignKey("gov_organizations.organization_id", ondelete="CASCADE"), index=True),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("description", sa.Text(), default=""),
        sa.Column("policy_type", sa.String(64), index=True, default="ACCESS_CONTROL"),
        sa.Column("version", sa.Integer(), default=1),
        sa.Column("status", sa.String(32), default="ACTIVE", index=True),
        sa.Column("rules", sa.JSON(), default=list),
        sa.Column("priority", sa.Integer(), default=100),
        sa.Column("created_by", sa.String(255), default="ADMIN"),
        sa.Column("approved_by", sa.String(255), nullable=True),
        sa.Column("effective_from", sa.DateTime(timezone=True), nullable=False),
        sa.Column("effective_until", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 7. gov_policy_versions
    op.create_table(
        "gov_policy_versions",
        sa.Column("version_id", sa.String(64), primary_key=True),
        sa.Column("policy_id", sa.String(64), sa.ForeignKey("gov_policies.policy_id", ondelete="CASCADE"), index=True),
        sa.Column("version_number", sa.Integer(), nullable=False),
        sa.Column("content_hash", sa.String(64), nullable=False),
        sa.Column("rules", sa.JSON(), default=list),
        sa.Column("created_by", sa.String(255), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 8. gov_retention_policies
    op.create_table(
        "gov_retention_policies",
        sa.Column("policy_id", sa.String(64), primary_key=True),
        sa.Column("organization_id", sa.String(64), sa.ForeignKey("gov_organizations.organization_id", ondelete="CASCADE"), index=True),
        sa.Column("resource_type", sa.String(64), index=True, nullable=False),
        sa.Column("classification", sa.String(32), default="INTERNAL"),
        sa.Column("retention_period_days", sa.Integer(), default=365),
        sa.Column("deletion_strategy", sa.String(32), default="SOFT_DELETE"),
        sa.Column("legal_hold_behavior", sa.String(64), default="SHIELD_FROM_DELETION"),
        sa.Column("archive_strategy", sa.String(64), default="COLD_STORAGE"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 9. gov_legal_holds
    op.create_table(
        "gov_legal_holds",
        sa.Column("hold_id", sa.String(64), primary_key=True),
        sa.Column("organization_id", sa.String(64), sa.ForeignKey("gov_organizations.organization_id", ondelete="CASCADE"), index=True),
        sa.Column("resource_type", sa.String(64), index=True, nullable=False),
        sa.Column("resource_id", sa.String(128), index=True, nullable=False),
        sa.Column("reason", sa.Text(), nullable=False),
        sa.Column("created_by", sa.String(255), nullable=False),
        sa.Column("approved_by", sa.String(255), nullable=True),
        sa.Column("status", sa.String(32), default="ACTIVE", index=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("released_at", sa.DateTime(timezone=True), nullable=True),
    )

    # 10. gov_deletion_requests
    op.create_table(
        "gov_deletion_requests",
        sa.Column("deletion_id", sa.String(64), primary_key=True),
        sa.Column("organization_id", sa.String(64), sa.ForeignKey("gov_organizations.organization_id", ondelete="CASCADE"), index=True),
        sa.Column("resource_type", sa.String(64), index=True, nullable=False),
        sa.Column("resource_id", sa.String(128), index=True, nullable=False),
        sa.Column("requested_by", sa.String(255), nullable=False),
        sa.Column("approved_by", sa.String(255), nullable=True),
        sa.Column("deletion_type", sa.String(64), default="PRIVACY_REQUEST"),
        sa.Column("status", sa.String(32), default="PENDING", index=True),
        sa.Column("verification_evidence", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
    )

    # 11. gov_privacy_requests
    op.create_table(
        "gov_privacy_requests",
        sa.Column("request_id", sa.String(64), primary_key=True),
        sa.Column("organization_id", sa.String(64), sa.ForeignKey("gov_organizations.organization_id", ondelete="CASCADE"), index=True),
        sa.Column("data_principal_id", sa.String(128), index=True, nullable=False),
        sa.Column("request_type", sa.String(32), default="ACCESS"),
        sa.Column("status", sa.String(32), default="PENDING", index=True),
        sa.Column("identity_verified", sa.Boolean(), default=False),
        sa.Column("legal_hold_checked", sa.Boolean(), default=False),
        sa.Column("reason", sa.Text(), default=""),
        sa.Column("assigned_to", sa.String(255), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
    )

    # 12. gov_data_exports
    op.create_table(
        "gov_data_exports",
        sa.Column("export_id", sa.String(64), primary_key=True),
        sa.Column("organization_id", sa.String(64), sa.ForeignKey("gov_organizations.organization_id", ondelete="CASCADE"), index=True),
        sa.Column("requester_id", sa.String(255), nullable=False),
        sa.Column("scope", sa.String(128), default="CASE"),
        sa.Column("resource_count", sa.Integer(), default=0),
        sa.Column("classification", sa.String(32), default="CONFIDENTIAL"),
        sa.Column("integrity_hash", sa.String(64), nullable=False),
        sa.Column("status", sa.String(32), default="READY", index=True),
        sa.Column("download_token", sa.String(128), unique=True, index=True),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 13. gov_audit_events
    op.create_table(
        "gov_audit_events",
        sa.Column("audit_id", sa.String(64), primary_key=True),
        sa.Column("organization_id", sa.String(64), sa.ForeignKey("gov_organizations.organization_id", ondelete="CASCADE"), index=True),
        sa.Column("actor_type", sa.String(32), default="USER"),
        sa.Column("actor_id", sa.String(255), index=True, nullable=False),
        sa.Column("action", sa.String(128), index=True, nullable=False),
        sa.Column("resource_type", sa.String(128), index=True, nullable=False),
        sa.Column("resource_id", sa.String(128), index=True, nullable=False),
        sa.Column("result", sa.String(32), default="SUCCESS", index=True),
        sa.Column("reason", sa.Text(), default=""),
        sa.Column("previous_hash", sa.String(64), nullable=True),
        sa.Column("event_hash", sa.String(64), nullable=False),
        sa.Column("session_reference", sa.String(128), nullable=True),
        sa.Column("request_id", sa.String(128), nullable=True),
        sa.Column("correlation_id", sa.String(128), nullable=True),
        sa.Column("policy_id", sa.String(64), nullable=True),
        sa.Column("policy_version", sa.Integer(), nullable=True),
        sa.Column("metadata_payload", sa.JSON(), default=dict),
        sa.Column("timestamp", sa.DateTime(timezone=True), nullable=False, index=True),
    )

    # 14. gov_audit_integrity_checkpoints
    op.create_table(
        "gov_audit_integrity_checkpoints",
        sa.Column("checkpoint_id", sa.String(64), primary_key=True),
        sa.Column("organization_id", sa.String(64), sa.ForeignKey("gov_organizations.organization_id", ondelete="CASCADE"), index=True),
        sa.Column("start_audit_id", sa.String(64), nullable=False),
        sa.Column("end_audit_id", sa.String(64), nullable=False),
        sa.Column("event_count", sa.Integer(), nullable=False),
        sa.Column("merkle_root_hash", sa.String(64), nullable=False),
        sa.Column("verified", sa.Boolean(), default=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 15. gov_governance_alerts
    op.create_table(
        "gov_governance_alerts",
        sa.Column("alert_id", sa.String(64), primary_key=True),
        sa.Column("organization_id", sa.String(64), sa.ForeignKey("gov_organizations.organization_id", ondelete="CASCADE"), index=True),
        sa.Column("alert_type", sa.String(64), index=True, nullable=False),
        sa.Column("severity", sa.String(32), default="HIGH"),
        sa.Column("title", sa.String(255), nullable=False),
        sa.Column("description", sa.Text(), default=""),
        sa.Column("actor_id", sa.String(255), nullable=True),
        sa.Column("affected_resource", sa.String(255), nullable=True),
        sa.Column("status", sa.String(32), default="ACTIVE", index=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 16. gov_compliance_frameworks
    op.create_table(
        "gov_compliance_frameworks",
        sa.Column("framework_id", sa.String(64), primary_key=True),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("version", sa.String(32), default="2024"),
        sa.Column("jurisdiction", sa.String(64), default="GLOBAL"),
        sa.Column("description", sa.Text(), default=""),
        sa.Column("control_count", sa.Integer(), default=0),
        sa.Column("status", sa.String(32), default="ACTIVE"),
    )

    # 17. gov_compliance_controls
    op.create_table(
        "gov_compliance_controls",
        sa.Column("control_id", sa.String(64), primary_key=True),
        sa.Column("framework_id", sa.String(64), sa.ForeignKey("gov_compliance_frameworks.framework_id", ondelete="CASCADE"), index=True),
        sa.Column("control_code", sa.String(64), index=True, nullable=False),
        sa.Column("title", sa.String(255), nullable=False),
        sa.Column("description", sa.Text(), default=""),
        sa.Column("requirement", sa.Text(), default=""),
        sa.Column("implementation_status", sa.String(32), default="NOT_ASSESSED"),
        sa.Column("evidence_requirements", sa.JSON(), default=list),
        sa.Column("owner", sa.String(255), default="COMPLIANCE_LEAD"),
    )

    # 18. gov_compliance_evidence
    op.create_table(
        "gov_compliance_evidence",
        sa.Column("evidence_id", sa.String(64), primary_key=True),
        sa.Column("control_id", sa.String(64), sa.ForeignKey("gov_compliance_controls.control_id", ondelete="CASCADE"), index=True),
        sa.Column("resource_type", sa.String(64), nullable=False),
        sa.Column("resource_id", sa.String(128), nullable=False),
        sa.Column("source", sa.String(255), nullable=False),
        sa.Column("integrity_hash", sa.String(64), nullable=False),
        sa.Column("valid_until", sa.DateTime(timezone=True), nullable=False),
        sa.Column("status", sa.String(32), default="VERIFIED"),
        sa.Column("collected_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 19. gov_compliance_assessments
    op.create_table(
        "gov_compliance_assessments",
        sa.Column("assessment_id", sa.String(64), primary_key=True),
        sa.Column("framework_id", sa.String(64), sa.ForeignKey("gov_compliance_frameworks.framework_id", ondelete="CASCADE"), index=True),
        sa.Column("organization_id", sa.String(64), sa.ForeignKey("gov_organizations.organization_id", ondelete="CASCADE"), index=True),
        sa.Column("status", sa.String(32), default="COMPLETED"),
        sa.Column("score_percentage", sa.Float(), default=0.0),
        sa.Column("control_count", sa.Integer(), default=0),
        sa.Column("implemented_count", sa.Integer(), default=0),
        sa.Column("partial_count", sa.Integer(), default=0),
        sa.Column("failed_count", sa.Integer(), default=0),
        sa.Column("exception_count", sa.Integer(), default=0),
        sa.Column("assessed_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("assessor", sa.String(255), default="AUTOMATED_GOVERNANCE_ENGINE"),
    )

    # 20. gov_user_sessions
    op.create_table(
        "gov_user_sessions",
        sa.Column("session_id", sa.String(64), primary_key=True),
        sa.Column("user_id", sa.String(64), index=True, nullable=False),
        sa.Column("organization_id", sa.String(64), sa.ForeignKey("gov_organizations.organization_id", ondelete="CASCADE"), index=True),
        sa.Column("authentication_strength", sa.String(64), default="PASSWORD"),
        sa.Column("mfa_verified", sa.Boolean(), default=False),
        sa.Column("device_reference", sa.String(255), default="Unknown"),
        sa.Column("ip_reference", sa.String(64), default="127.0.0.1"),
        sa.Column("status", sa.String(32), default="ACTIVE", index=True),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("last_seen", sa.DateTime(timezone=True), nullable=False),
    )

    # 21. gov_service_accounts
    op.create_table(
        "gov_service_accounts",
        sa.Column("service_account_id", sa.String(64), primary_key=True),
        sa.Column("organization_id", sa.String(64), sa.ForeignKey("gov_organizations.organization_id", ondelete="CASCADE"), index=True),
        sa.Column("name", sa.String(128), nullable=False),
        sa.Column("description", sa.Text(), default=""),
        sa.Column("permissions", sa.JSON(), default=list),
        sa.Column("status", sa.String(32), default="ACTIVE", index=True),
        sa.Column("created_by", sa.String(255), nullable=False),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 22. gov_api_keys
    op.create_table(
        "gov_api_keys",
        sa.Column("key_id", sa.String(64), primary_key=True),
        sa.Column("organization_id", sa.String(64), sa.ForeignKey("gov_organizations.organization_id", ondelete="CASCADE"), index=True),
        sa.Column("name", sa.String(128), nullable=False),
        sa.Column("key_prefix", sa.String(16), index=True, nullable=False),
        sa.Column("hashed_secret", sa.String(128), nullable=False),
        sa.Column("scope", sa.String(64), default="ORGANIZATION"),
        sa.Column("permissions", sa.JSON(), default=list),
        sa.Column("status", sa.String(32), default="ACTIVE", index=True),
        sa.Column("owner_id", sa.String(255), nullable=False),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("last_used_at", sa.DateTime(timezone=True), nullable=True),
    )


def downgrade() -> None:
    op.drop_table("gov_api_keys")
    op.drop_table("gov_service_accounts")
    op.drop_table("gov_user_sessions")
    op.drop_table("gov_compliance_assessments")
    op.drop_table("gov_compliance_evidence")
    op.drop_table("gov_compliance_controls")
    op.drop_table("gov_compliance_frameworks")
    op.drop_table("gov_governance_alerts")
    op.drop_table("gov_audit_integrity_checkpoints")
    op.drop_table("gov_audit_events")
    op.drop_table("gov_data_exports")
    op.drop_table("gov_privacy_requests")
    op.drop_table("gov_deletion_requests")
    op.drop_table("gov_legal_holds")
    op.drop_table("gov_retention_policies")
    op.drop_table("gov_policy_versions")
    op.drop_table("gov_policies")
    op.drop_table("gov_permissions")
    op.drop_table("gov_role_versions")
    op.drop_table("gov_roles")
    op.drop_table("gov_organization_users")
    op.drop_table("gov_organizations")
