"""Alembic Migration 041 — SOC Intelligence, Alert Correlation, Incident Response & SOAR Schema (Phase 4.0 Part 7).

Revision ID: 041_soc_operations_schema
Revises: 040_continuous_intelligence_schema
Create Date: 2026-08-14
"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "041_soc_operations_schema"
down_revision = "040_continuous_intelligence_schema"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # 1. soc_alerts
    op.create_table(
        "soc_alerts",
        sa.Column("alert_id", sa.String(64), primary_key=True),
        sa.Column("source_alert_id", sa.String(64), nullable=True, index=True),
        sa.Column("source_system", sa.String(64), nullable=False, default="INTERNAL_DETECTOR"),
        sa.Column("alert_type", sa.String(64), nullable=False, index=True),
        sa.Column("category", sa.String(64), nullable=False, default="OTHER", index=True),
        sa.Column("subcategory", sa.String(64), nullable=True),
        sa.Column("title", sa.String(255), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("severity", sa.String(32), nullable=False, default="MEDIUM", index=True),
        sa.Column("priority", sa.String(32), nullable=False, default="MEDIUM", index=True),
        sa.Column("confidence", sa.String(32), nullable=False, default="HIGH"),
        sa.Column("status", sa.String(32), nullable=False, default="NEW", index=True),
        sa.Column("entity_ids", sa.JSON(), nullable=False),
        sa.Column("finding_ids", sa.JSON(), nullable=False),
        sa.Column("evidence_ids", sa.JSON(), nullable=False),
        sa.Column("relationship_ids", sa.JSON(), nullable=False),
        sa.Column("campaign_id", sa.String(64), nullable=True, index=True),
        sa.Column("attack_chain_id", sa.String(64), nullable=True, index=True),
        sa.Column("case_id", sa.String(64), nullable=True, index=True),
        sa.Column("incident_id", sa.String(64), nullable=True, index=True),
        sa.Column("organization_id", sa.String(64), nullable=True, index=True),
        sa.Column("raw_payload", sa.JSON(), nullable=False),
        sa.Column("first_seen", sa.DateTime(timezone=True), nullable=False),
        sa.Column("last_seen", sa.DateTime(timezone=True), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 2. alert_clusters
    op.create_table(
        "alert_clusters",
        sa.Column("cluster_id", sa.String(64), primary_key=True),
        sa.Column("alert_ids", sa.JSON(), nullable=False),
        sa.Column("entity_ids", sa.JSON(), nullable=False),
        sa.Column("campaign_id", sa.String(64), nullable=True, index=True),
        sa.Column("confidence", sa.Float(), nullable=False, default=1.0),
        sa.Column("cluster_type", sa.String(64), nullable=False, default="SAME_ENTITY", index=True),
        sa.Column("first_seen", sa.DateTime(timezone=True), nullable=False),
        sa.Column("last_seen", sa.DateTime(timezone=True), nullable=False),
        sa.Column("status", sa.String(32), nullable=False, default="ACTIVE", index=True),
        sa.Column("organization_id", sa.String(64), nullable=True, index=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 3. soc_security_incidents
    op.create_table(
        "soc_security_incidents",
        sa.Column("incident_id", sa.String(64), primary_key=True),
        sa.Column("incident_number", sa.String(32), nullable=False, unique=True, index=True),
        sa.Column("title", sa.String(255), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("incident_type", sa.String(64), nullable=False, default="UNKNOWN_INCIDENT", index=True),
        sa.Column("severity", sa.String(32), nullable=False, default="MEDIUM", index=True),
        sa.Column("priority", sa.String(32), nullable=False, default="MEDIUM", index=True),
        sa.Column("confidence", sa.String(32), nullable=False, default="HIGH"),
        sa.Column("status", sa.String(32), nullable=False, default="NEW", index=True),
        sa.Column("owner_id", sa.String(64), nullable=True, index=True),
        sa.Column("team_id", sa.String(64), nullable=True, index=True),
        sa.Column("source_alert_count", sa.Integer(), nullable=False, default=0),
        sa.Column("entity_count", sa.Integer(), nullable=False, default=0),
        sa.Column("finding_count", sa.Integer(), nullable=False, default=0),
        sa.Column("evidence_count", sa.Integer(), nullable=False, default=0),
        sa.Column("campaign_id", sa.String(64), nullable=True, index=True),
        sa.Column("attack_chain_id", sa.String(64), nullable=True, index=True),
        sa.Column("case_id", sa.String(64), nullable=True, index=True),
        sa.Column("incident_fingerprint", sa.String(128), nullable=False, default="", index=True),
        sa.Column("organization_id", sa.String(64), nullable=True, index=True),
        sa.Column("first_seen", sa.DateTime(timezone=True), nullable=False),
        sa.Column("last_seen", sa.DateTime(timezone=True), nullable=False),
        sa.Column("detected_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("acknowledged_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("contained_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("resolved_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("closed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 4. soc_incident_alerts
    op.create_table(
        "soc_incident_alerts",
        sa.Column("id", sa.String(64), primary_key=True),
        sa.Column("incident_id", sa.String(64), sa.ForeignKey("soc_security_incidents.incident_id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("alert_id", sa.String(64), sa.ForeignKey("soc_alerts.alert_id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("linked_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 5. soc_incident_entities
    op.create_table(
        "soc_incident_entities",
        sa.Column("id", sa.String(64), primary_key=True),
        sa.Column("incident_id", sa.String(64), sa.ForeignKey("soc_security_incidents.incident_id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("entity_id", sa.String(64), nullable=False, index=True),
        sa.Column("role", sa.String(64), nullable=False, default="TARGET"),
        sa.Column("linked_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 6. soc_incident_findings
    op.create_table(
        "soc_incident_findings",
        sa.Column("id", sa.String(64), primary_key=True),
        sa.Column("incident_id", sa.String(64), sa.ForeignKey("soc_security_incidents.incident_id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("finding_id", sa.String(64), nullable=False, index=True),
        sa.Column("linked_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 7. soc_incident_evidence
    op.create_table(
        "soc_incident_evidence",
        sa.Column("id", sa.String(64), primary_key=True),
        sa.Column("incident_id", sa.String(64), sa.ForeignKey("soc_security_incidents.incident_id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("evidence_id", sa.String(64), nullable=False, index=True),
        sa.Column("linked_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 8. soc_incident_timeline
    op.create_table(
        "soc_incident_timeline",
        sa.Column("timeline_event_id", sa.String(64), primary_key=True),
        sa.Column("incident_id", sa.String(64), sa.ForeignKey("soc_security_incidents.incident_id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("event_type", sa.String(64), nullable=False, index=True),
        sa.Column("source", sa.String(64), nullable=False, default="SOC_AUTOMATION"),
        sa.Column("timestamp", sa.DateTime(timezone=True), nullable=False, index=True),
        sa.Column("actor", sa.String(64), nullable=False, default="SYSTEM"),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("entity_ids", sa.JSON(), nullable=False),
        sa.Column("evidence_ids", sa.JSON(), nullable=False),
        sa.Column("alert_id", sa.String(64), nullable=True),
        sa.Column("action_id", sa.String(64), nullable=True),
        sa.Column("provenance", sa.String(255), nullable=False, default=""),
    )

    # 9. soc_incident_assignments
    op.create_table(
        "soc_incident_assignments",
        sa.Column("assignment_id", sa.String(64), primary_key=True),
        sa.Column("incident_id", sa.String(64), sa.ForeignKey("soc_security_incidents.incident_id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("analyst_id", sa.String(64), nullable=False, index=True),
        sa.Column("team_id", sa.String(64), nullable=True, index=True),
        sa.Column("assigned_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("assigned_by", sa.String(64), nullable=False, default="SOC_LEAD"),
        sa.Column("reason", sa.String(255), nullable=False, default="Automated routing"),
        sa.Column("status", sa.String(32), nullable=False, default="ACTIVE", index=True),
    )

    # 10. soc_incident_sla
    op.create_table(
        "soc_incident_sla",
        sa.Column("sla_id", sa.String(64), primary_key=True),
        sa.Column("incident_id", sa.String(64), sa.ForeignKey("soc_security_incidents.incident_id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("ack_deadline", sa.DateTime(timezone=True), nullable=False),
        sa.Column("triage_deadline", sa.DateTime(timezone=True), nullable=False),
        sa.Column("containment_deadline", sa.DateTime(timezone=True), nullable=False),
        sa.Column("resolution_deadline", sa.DateTime(timezone=True), nullable=False),
        sa.Column("status", sa.String(32), nullable=False, default="ON_TRACK", index=True),
        sa.Column("time_to_acknowledge_seconds", sa.Float(), nullable=True),
        sa.Column("time_to_triage_seconds", sa.Float(), nullable=True),
        sa.Column("time_to_containment_seconds", sa.Float(), nullable=True),
        sa.Column("time_to_resolution_seconds", sa.Float(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 11. soc_response_playbooks
    op.create_table(
        "soc_response_playbooks",
        sa.Column("playbook_id", sa.String(64), primary_key=True),
        sa.Column("name", sa.String(128), nullable=False, index=True),
        sa.Column("current_version", sa.Integer(), nullable=False, default=1),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("incident_types", sa.JSON(), nullable=False),
        sa.Column("required_permissions", sa.JSON(), nullable=False),
        sa.Column("approval_policy", sa.JSON(), nullable=False),
        sa.Column("enabled", sa.Boolean(), nullable=False, default=True, index=True),
        sa.Column("organization_id", sa.String(64), nullable=True, index=True),
        sa.Column("created_by", sa.String(64), nullable=False, default="SOC_ADMIN"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 12. soc_response_playbook_versions
    op.create_table(
        "soc_response_playbook_versions",
        sa.Column("version_id", sa.String(64), primary_key=True),
        sa.Column("playbook_id", sa.String(64), sa.ForeignKey("soc_response_playbooks.playbook_id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("version_number", sa.Integer(), nullable=False, index=True),
        sa.Column("content_hash", sa.String(128), nullable=False),
        sa.Column("author", sa.String(64), nullable=False, default="SOC_ADMIN"),
        sa.Column("steps_snapshot", sa.JSON(), nullable=False),
        sa.Column("published_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 13. soc_response_playbook_steps
    op.create_table(
        "soc_response_playbook_steps",
        sa.Column("step_id", sa.String(64), primary_key=True),
        sa.Column("playbook_id", sa.String(64), sa.ForeignKey("soc_response_playbooks.playbook_id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("step_number", sa.Integer(), nullable=False, index=True),
        sa.Column("name", sa.String(128), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("action_type", sa.String(64), nullable=False, index=True),
        sa.Column("risk_level", sa.String(32), nullable=False, default="MEDIUM"),
        sa.Column("approval_required", sa.Boolean(), nullable=False, default=True),
        sa.Column("dry_run_supported", sa.Boolean(), nullable=False, default=True),
        sa.Column("rollback_supported", sa.Boolean(), nullable=False, default=False),
        sa.Column("timeout", sa.Integer(), nullable=False, default=30),
        sa.Column("retry_policy", sa.JSON(), nullable=False),
        sa.Column("conditions", sa.JSON(), nullable=False),
    )

    # 14. soc_response_actions
    op.create_table(
        "soc_response_actions",
        sa.Column("action_id", sa.String(64), primary_key=True),
        sa.Column("incident_id", sa.String(64), sa.ForeignKey("soc_security_incidents.incident_id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("playbook_id", sa.String(64), nullable=True, index=True),
        sa.Column("playbook_version", sa.Integer(), nullable=False, default=1),
        sa.Column("step_id", sa.String(64), nullable=True),
        sa.Column("action_type", sa.String(64), nullable=False, index=True),
        sa.Column("target", sa.String(255), nullable=False, index=True),
        sa.Column("target_type", sa.String(64), nullable=False, default="DOMAIN"),
        sa.Column("requested_by", sa.String(64), nullable=False, index=True),
        sa.Column("approved_by", sa.String(64), nullable=True, index=True),
        sa.Column("approval_status", sa.String(32), nullable=False, default="PENDING", index=True),
        sa.Column("dry_run", sa.Boolean(), nullable=False, default=False),
        sa.Column("status", sa.String(32), nullable=False, default="QUEUED", index=True),
        sa.Column("reason", sa.Text(), nullable=False),
        sa.Column("evidence_ids", sa.JSON(), nullable=False),
        sa.Column("idempotency_key", sa.String(128), nullable=False, index=True),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("error_code", sa.String(64), nullable=True),
        sa.Column("result_reference", sa.String(255), nullable=True),
        sa.Column("rollback_action_id", sa.String(64), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 15. soc_response_approvals
    op.create_table(
        "soc_response_approvals",
        sa.Column("approval_id", sa.String(64), primary_key=True),
        sa.Column("action_id", sa.String(64), sa.ForeignKey("soc_response_actions.action_id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("incident_id", sa.String(64), nullable=False, index=True),
        sa.Column("requested_by", sa.String(64), nullable=False, index=True),
        sa.Column("approver_scope", sa.String(64), nullable=False, default="SOC_LEAD"),
        sa.Column("reason", sa.Text(), nullable=False),
        sa.Column("risk", sa.String(32), nullable=False, default="HIGH"),
        sa.Column("evidence", sa.JSON(), nullable=False),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("status", sa.String(32), nullable=False, default="PENDING", index=True),
        sa.Column("decision_reason", sa.Text(), nullable=True),
        sa.Column("decided_by", sa.String(64), nullable=True, index=True),
        sa.Column("decided_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 16. soc_response_simulations
    op.create_table(
        "soc_response_simulations",
        sa.Column("simulation_id", sa.String(64), primary_key=True),
        sa.Column("action_id", sa.String(64), sa.ForeignKey("soc_response_actions.action_id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("target", sa.String(255), nullable=False),
        sa.Column("provider", sa.String(64), nullable=False),
        sa.Column("expected_effect", sa.Text(), nullable=False),
        sa.Column("risk_assessment", sa.Text(), nullable=False),
        sa.Column("required_permissions", sa.JSON(), nullable=False),
        sa.Column("rollback_supported", sa.Boolean(), nullable=False, default=False),
        sa.Column("side_effects", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 17. soc_response_executions
    op.create_table(
        "soc_response_executions",
        sa.Column("execution_id", sa.String(64), primary_key=True),
        sa.Column("action_id", sa.String(64), sa.ForeignKey("soc_response_actions.action_id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("provider_name", sa.String(64), nullable=False, index=True),
        sa.Column("status", sa.String(32), nullable=False, index=True),
        sa.Column("request_payload", sa.JSON(), nullable=False),
        sa.Column("response_payload", sa.JSON(), nullable=False),
        sa.Column("execution_time_ms", sa.Float(), nullable=False, default=0.0),
        sa.Column("error_message", sa.Text(), nullable=True),
        sa.Column("executed_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 18. soc_response_verifications
    op.create_table(
        "soc_response_verifications",
        sa.Column("verification_id", sa.String(64), primary_key=True),
        sa.Column("action_id", sa.String(64), sa.ForeignKey("soc_response_actions.action_id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("target", sa.String(255), nullable=False),
        sa.Column("verification_status", sa.String(32), nullable=False, index=True),
        sa.Column("evidence_gathered", sa.JSON(), nullable=False),
        sa.Column("observations", sa.Text(), nullable=False),
        sa.Column("verified_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 19. soc_response_rollbacks
    op.create_table(
        "soc_response_rollbacks",
        sa.Column("rollback_id", sa.String(64), primary_key=True),
        sa.Column("action_id", sa.String(64), sa.ForeignKey("soc_response_actions.action_id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("target", sa.String(255), nullable=False),
        sa.Column("rollback_status", sa.String(32), nullable=False, index=True),
        sa.Column("reason", sa.Text(), nullable=False),
        sa.Column("executed_by", sa.String(64), nullable=False),
        sa.Column("error_message", sa.Text(), nullable=True),
        sa.Column("executed_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 20. soc_response_policies
    op.create_table(
        "soc_response_policies",
        sa.Column("policy_id", sa.String(64), primary_key=True),
        sa.Column("name", sa.String(128), nullable=False, index=True),
        sa.Column("action_type", sa.String(64), nullable=False, index=True),
        sa.Column("min_incident_severity", sa.String(32), nullable=False, default="HIGH"),
        sa.Column("automation_level", sa.String(32), nullable=False, default="APPROVAL_REQUIRED", index=True),
        sa.Column("protected_targets", sa.JSON(), nullable=False),
        sa.Column("allow_auto_approval", sa.Boolean(), nullable=False, default=False),
        sa.Column("organization_id", sa.String(64), nullable=True, index=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 21. soc_response_provider_registry
    op.create_table(
        "soc_response_provider_registry",
        sa.Column("provider_id", sa.String(64), primary_key=True),
        sa.Column("name", sa.String(64), nullable=False, unique=True, index=True),
        sa.Column("provider_type", sa.String(64), nullable=False, index=True),
        sa.Column("supported_actions", sa.JSON(), nullable=False),
        sa.Column("endpoint", sa.String(255), nullable=True),
        sa.Column("health_status", sa.String(32), nullable=False, default="HEALTHY", index=True),
        sa.Column("last_health_check", sa.DateTime(timezone=True), nullable=False),
    )

    # 22. soc_evidence_collection_records
    op.create_table(
        "soc_evidence_collection_records",
        sa.Column("collection_id", sa.String(64), primary_key=True),
        sa.Column("incident_id", sa.String(64), sa.ForeignKey("soc_security_incidents.incident_id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("source", sa.String(128), nullable=False),
        sa.Column("collector_id", sa.String(64), nullable=False, index=True),
        sa.Column("evidence_type", sa.String(64), nullable=False, index=True),
        sa.Column("sha256_hash", sa.String(64), nullable=False, index=True),
        sa.Column("storage_reference", sa.String(255), nullable=False),
        sa.Column("integrity_status", sa.String(32), nullable=False, default="VERIFIED", index=True),
        sa.Column("collection_method", sa.String(64), nullable=False, default="SECURE_API_PULL"),
        sa.Column("access_log", sa.JSON(), nullable=False),
        sa.Column("collected_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 23. soc_incident_merges
    op.create_table(
        "soc_incident_merges",
        sa.Column("merge_id", sa.String(64), primary_key=True),
        sa.Column("primary_incident_id", sa.String(64), sa.ForeignKey("soc_security_incidents.incident_id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("merged_incident_ids", sa.JSON(), nullable=False),
        sa.Column("merged_by", sa.String(64), nullable=False, index=True),
        sa.Column("reason", sa.Text(), nullable=False),
        sa.Column("status", sa.String(32), nullable=False, default="MERGED"),
        sa.Column("merged_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 24. soc_incident_splits
    op.create_table(
        "soc_incident_splits",
        sa.Column("split_id", sa.String(64), primary_key=True),
        sa.Column("original_incident_id", sa.String(64), sa.ForeignKey("soc_security_incidents.incident_id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("new_incident_ids", sa.JSON(), nullable=False),
        sa.Column("split_by", sa.String(64), nullable=False, index=True),
        sa.Column("reason", sa.Text(), nullable=False),
        sa.Column("split_at", sa.DateTime(timezone=True), nullable=False),
    )


def downgrade() -> None:
    op.drop_table("soc_incident_splits")
    op.drop_table("soc_incident_merges")
    op.drop_table("soc_evidence_collection_records")
    op.drop_table("soc_response_provider_registry")
    op.drop_table("soc_response_policies")
    op.drop_table("soc_response_rollbacks")
    op.drop_table("soc_response_verifications")
    op.drop_table("soc_response_executions")
    op.drop_table("soc_response_simulations")
    op.drop_table("soc_response_approvals")
    op.drop_table("soc_response_actions")
    op.drop_table("soc_response_playbook_steps")
    op.drop_table("soc_response_playbook_versions")
    op.drop_table("soc_response_playbooks")
    op.drop_table("soc_incident_sla")
    op.drop_table("soc_incident_assignments")
    op.drop_table("soc_incident_timeline")
    op.drop_table("soc_incident_evidence")
    op.drop_table("soc_incident_findings")
    op.drop_table("soc_incident_entities")
    op.drop_table("soc_incident_alerts")
    op.drop_table("soc_security_incidents")
    op.drop_table("alert_clusters")
    op.drop_table("soc_alerts")
