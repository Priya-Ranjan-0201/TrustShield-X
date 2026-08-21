"""Alembic Migration 040 — Continuous Intelligence & Real-Time Monitoring Schema (Phase 4.0 Part 6).

Revision ID: 040_continuous_intelligence_schema
Revises: 039_unified_intelligence_graph_schema
Create Date: 2026-08-14
"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "040_continuous_intelligence_schema"
down_revision = "039_unified_intelligence_graph_schema"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # 1. threat_feed_configurations
    op.create_table(
        "threat_feed_configurations",
        sa.Column("feed_id", sa.String(64), primary_key=True),
        sa.Column("provider_name", sa.String(128), nullable=False, index=True),
        sa.Column("provider_type", sa.String(50), nullable=False),
        sa.Column("endpoint", sa.String(512), nullable=False),
        sa.Column("enabled", sa.Boolean(), default=True, nullable=False),
        sa.Column("poll_interval", sa.String(50), default="HOURLY", nullable=False),
        sa.Column("poll_interval_seconds", sa.Integer(), default=3600, nullable=False),
        sa.Column("authentication_mode", sa.String(50), default="NONE", nullable=False),
        sa.Column("timeout_seconds", sa.Integer(), default=30, nullable=False),
        sa.Column("retry_policy", sa.JSON(), nullable=False),
        sa.Column("rate_limit", sa.JSON(), nullable=False),
        sa.Column("supported_types", sa.JSON(), nullable=False),
        sa.Column("trust_level", sa.String(30), default="STANDARD", nullable=False),
        sa.Column("freshness_policy", sa.JSON(), nullable=False),
        sa.Column("organization_id", sa.String(64), nullable=True, index=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
    )

    # 2. threat_feed_health
    op.create_table(
        "threat_feed_health",
        sa.Column("health_id", sa.String(64), primary_key=True),
        sa.Column("feed_id", sa.String(64), sa.ForeignKey("threat_feed_configurations.feed_id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("status", sa.String(30), default="UNKNOWN", nullable=False),
        sa.Column("last_success", sa.DateTime(), nullable=True),
        sa.Column("last_failure", sa.DateTime(), nullable=True),
        sa.Column("last_attempt", sa.DateTime(), nullable=True),
        sa.Column("latency_ms", sa.Float(), default=0.0, nullable=False),
        sa.Column("items_received", sa.Integer(), default=0, nullable=False),
        sa.Column("items_accepted", sa.Integer(), default=0, nullable=False),
        sa.Column("items_rejected", sa.Integer(), default=0, nullable=False),
        sa.Column("parse_errors", sa.Integer(), default=0, nullable=False),
        sa.Column("authentication_errors", sa.Integer(), default=0, nullable=False),
        sa.Column("rate_limit_errors", sa.Integer(), default=0, nullable=False),
        sa.Column("network_errors", sa.Integer(), default=0, nullable=False),
        sa.Column("staleness_days", sa.Float(), default=0.0, nullable=False),
        sa.Column("provider_version", sa.String(30), default="1.0.0", nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
    )

    # 3. threat_feed_versions
    op.create_table(
        "threat_feed_versions",
        sa.Column("version_id", sa.String(64), primary_key=True),
        sa.Column("feed_id", sa.String(64), sa.ForeignKey("threat_feed_configurations.feed_id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("version_tag", sa.String(64), nullable=False),
        sa.Column("content_hash", sa.String(64), nullable=False),
        sa.Column("items_count", sa.Integer(), default=0, nullable=False),
        sa.Column("fetched_at", sa.DateTime(), nullable=False),
    )

    # 4. continuous_intelligence_observations
    op.create_table(
        "continuous_intelligence_observations",
        sa.Column("observation_id", sa.String(64), primary_key=True),
        sa.Column("feed_id", sa.String(64), sa.ForeignKey("threat_feed_configurations.feed_id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("indicator_id", sa.String(128), nullable=False, index=True),
        sa.Column("indicator_type", sa.String(50), nullable=False, index=True),
        sa.Column("indicator_value_hash", sa.String(64), nullable=False, index=True),
        sa.Column("normalized_value", sa.Text(), nullable=False),
        sa.Column("raw_value", sa.Text(), nullable=False),
        sa.Column("observation_type", sa.String(30), default="NEW", nullable=False),
        sa.Column("classification", sa.String(50), default="MALICIOUS", nullable=False),
        sa.Column("confidence", sa.String(20), default="HIGH", nullable=False),
        sa.Column("first_seen", sa.DateTime(), nullable=False),
        sa.Column("last_seen", sa.DateTime(), nullable=False),
        sa.Column("observed_at", sa.DateTime(), nullable=False),
        sa.Column("source_timestamp", sa.DateTime(), nullable=True),
        sa.Column("feed_version", sa.String(30), default="1.0.0", nullable=False),
        sa.Column("raw_reference", sa.Text(), nullable=True),
        sa.Column("status", sa.String(30), default="ACTIVE", nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )

    # 5. intelligence_state_changes
    op.create_table(
        "intelligence_state_changes",
        sa.Column("change_id", sa.String(64), primary_key=True),
        sa.Column("entity_id", sa.String(64), nullable=False, index=True),
        sa.Column("observation_id", sa.String(64), nullable=False, index=True),
        sa.Column("previous_state", sa.String(50), nullable=False),
        sa.Column("new_state", sa.String(50), nullable=False),
        sa.Column("transition_reason", sa.Text(), nullable=False),
        sa.Column("transition_timestamp", sa.DateTime(), nullable=False),
        sa.Column("source", sa.String(128), nullable=False),
    )

    # 6. monitoring_jobs
    op.create_table(
        "monitoring_jobs",
        sa.Column("job_id", sa.String(64), primary_key=True),
        sa.Column("feed_id", sa.String(64), sa.ForeignKey("threat_feed_configurations.feed_id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("job_type", sa.String(50), default="SYNC", nullable=False),
        sa.Column("schedule_type", sa.String(50), default="HOURLY", nullable=False),
        sa.Column("interval_seconds", sa.Integer(), default=3600, nullable=False),
        sa.Column("cron_expression", sa.String(64), nullable=True),
        sa.Column("enabled", sa.Boolean(), default=True, nullable=False),
        sa.Column("next_run_at", sa.DateTime(), nullable=False),
        sa.Column("last_run_at", sa.DateTime(), nullable=True),
        sa.Column("status", sa.String(30), default="QUEUED", nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )

    # 7. monitoring_job_runs
    op.create_table(
        "monitoring_job_runs",
        sa.Column("run_id", sa.String(64), primary_key=True),
        sa.Column("job_id", sa.String(64), sa.ForeignKey("monitoring_jobs.job_id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("feed_id", sa.String(64), nullable=False, index=True),
        sa.Column("status", sa.String(30), default="RUNNING", nullable=False),
        sa.Column("started_at", sa.DateTime(), nullable=False),
        sa.Column("completed_at", sa.DateTime(), nullable=True),
        sa.Column("attempt", sa.Integer(), default=1, nullable=False),
        sa.Column("items_processed", sa.Integer(), default=0, nullable=False),
        sa.Column("items_failed", sa.Integer(), default=0, nullable=False),
        sa.Column("error_code", sa.String(64), nullable=True),
        sa.Column("error_message", sa.Text(), nullable=True),
    )

    # 8. continuous_intelligence_events
    op.create_table(
        "continuous_intelligence_events",
        sa.Column("event_id", sa.String(64), primary_key=True),
        sa.Column("event_type", sa.String(64), nullable=False, index=True),
        sa.Column("event_version", sa.String(20), default="1.0.0", nullable=False),
        sa.Column("schema_version", sa.String(20), default="1.0.0", nullable=False),
        sa.Column("producer", sa.String(128), default="continuous_intelligence_orchestrator", nullable=False),
        sa.Column("entity_id", sa.String(64), nullable=True, index=True),
        sa.Column("analysis_id", sa.String(64), nullable=True, index=True),
        sa.Column("case_id", sa.String(64), nullable=True, index=True),
        sa.Column("timestamp", sa.DateTime(), nullable=False),
        sa.Column("correlation_id", sa.String(64), nullable=False, index=True),
        sa.Column("causation_id", sa.String(64), nullable=True),
        sa.Column("payload", sa.JSON(), nullable=False),
        sa.Column("provenance", sa.Text(), default="", nullable=False),
        sa.Column("deduplication_key", sa.String(128), nullable=False, unique=True, index=True),
    )

    # 9. event_processing_records
    op.create_table(
        "event_processing_records",
        sa.Column("record_id", sa.String(64), primary_key=True),
        sa.Column("event_id", sa.String(64), sa.ForeignKey("continuous_intelligence_events.event_id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("consumer_id", sa.String(128), nullable=False),
        sa.Column("status", sa.String(30), default="PROCESSED", nullable=False),
        sa.Column("attempts", sa.Integer(), default=1, nullable=False),
        sa.Column("processed_at", sa.DateTime(), nullable=False),
        sa.Column("error_message", sa.Text(), nullable=True),
    )

    # 10. event_dead_letters
    op.create_table(
        "event_dead_letters",
        sa.Column("dead_letter_id", sa.String(64), primary_key=True),
        sa.Column("event_id", sa.String(64), nullable=False, index=True),
        sa.Column("error", sa.Text(), nullable=False),
        sa.Column("attempts", sa.Integer(), default=1, nullable=False),
        sa.Column("last_attempt", sa.DateTime(), nullable=False),
        sa.Column("consumer", sa.String(128), nullable=False),
        sa.Column("payload_reference", sa.Text(), nullable=False),
        sa.Column("status", sa.String(30), default="PENDING", nullable=False),
        sa.Column("reprocessed_at", sa.DateTime(), nullable=True),
        sa.Column("reprocessed_by", sa.String(64), nullable=True),
    )

    # 11. security_alerts
    op.create_table(
        "security_alerts",
        sa.Column("alert_id", sa.String(64), primary_key=True),
        sa.Column("case_id", sa.String(64), nullable=True, index=True),
        sa.Column("analysis_id", sa.String(64), nullable=True, index=True),
        sa.Column("event_id", sa.String(64), nullable=True, index=True),
        sa.Column("alert_type", sa.String(64), nullable=False, index=True),
        sa.Column("title", sa.String(255), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("priority", sa.String(30), default="MEDIUM", nullable=False, index=True),
        sa.Column("severity", sa.String(30), default="MEDIUM", nullable=False),
        sa.Column("confidence", sa.String(30), default="HIGH", nullable=False),
        sa.Column("status", sa.String(30), default="NEW", nullable=False, index=True),
        sa.Column("source", sa.String(128), default="THREAT_MONITOR", nullable=False),
        sa.Column("evidence_ids", sa.JSON(), nullable=False),
        sa.Column("finding_ids", sa.JSON(), nullable=False),
        sa.Column("entity_ids", sa.JSON(), nullable=False),
        sa.Column("relationship_ids", sa.JSON(), nullable=False),
        sa.Column("campaign_id", sa.String(64), nullable=True, index=True),
        sa.Column("attack_chain_id", sa.String(64), nullable=True, index=True),
        sa.Column("alert_fingerprint", sa.String(64), nullable=False, index=True),
        sa.Column("organization_id", sa.String(64), nullable=True, index=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.Column("acknowledged_at", sa.DateTime(), nullable=True),
        sa.Column("resolved_at", sa.DateTime(), nullable=True),
        sa.Column("suppressed_until", sa.DateTime(), nullable=True),
    )

    # 12. alert_fingerprints
    op.create_table(
        "alert_fingerprints",
        sa.Column("fingerprint_id", sa.String(64), primary_key=True),
        sa.Column("fingerprint_hash", sa.String(64), nullable=False, unique=True, index=True),
        sa.Column("alert_type", sa.String(64), nullable=False),
        sa.Column("entity_id", sa.String(64), nullable=True),
        sa.Column("case_id", sa.String(64), nullable=True),
        sa.Column("last_seen", sa.DateTime(), nullable=False),
        sa.Column("occurrences", sa.Integer(), default=1, nullable=False),
    )

    # 13. alert_suppressions
    op.create_table(
        "alert_suppressions",
        sa.Column("suppression_id", sa.String(64), primary_key=True),
        sa.Column("alert_fingerprint", sa.String(64), nullable=False, index=True),
        sa.Column("alert_type", sa.String(64), nullable=False),
        sa.Column("reason", sa.Text(), nullable=False),
        sa.Column("suppressed_by", sa.String(64), nullable=False),
        sa.Column("expires_at", sa.DateTime(), nullable=True),
        sa.Column("is_active", sa.Boolean(), default=True, nullable=False),
        sa.Column("allow_critical_override", sa.Boolean(), default=True, nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )

    # 14. alert_acknowledgements
    op.create_table(
        "alert_acknowledgements",
        sa.Column("ack_id", sa.String(64), primary_key=True),
        sa.Column("alert_id", sa.String(64), sa.ForeignKey("security_alerts.alert_id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("user_id", sa.String(64), nullable=False),
        sa.Column("user_name", sa.String(128), nullable=False),
        sa.Column("reason", sa.Text(), nullable=False),
        sa.Column("comment", sa.Text(), nullable=True),
        sa.Column("acknowledged_at", sa.DateTime(), nullable=False),
    )

    # 15. alert_escalations
    op.create_table(
        "alert_escalations",
        sa.Column("escalation_id", sa.String(64), primary_key=True),
        sa.Column("alert_id", sa.String(64), sa.ForeignKey("security_alerts.alert_id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("previous_priority", sa.String(30), nullable=False),
        sa.Column("escalated_priority", sa.String(30), nullable=False),
        sa.Column("escalation_type", sa.String(50), default="TIMEOUT", nullable=False),
        sa.Column("reason", sa.Text(), nullable=False),
        sa.Column("escalated_by", sa.String(64), nullable=True),
        sa.Column("escalated_at", sa.DateTime(), nullable=False),
    )

    # 16. notification_policies
    op.create_table(
        "notification_policies",
        sa.Column("policy_id", sa.String(64), primary_key=True),
        sa.Column("organization_id", sa.String(64), nullable=True, index=True),
        sa.Column("alert_type", sa.String(64), nullable=False),
        sa.Column("min_priority", sa.String(30), default="HIGH", nullable=False),
        sa.Column("channel", sa.String(30), default="IN_APP", nullable=False),
        sa.Column("enabled", sa.Boolean(), default=True, nullable=False),
        sa.Column("cooldown_minutes", sa.Integer(), default=15, nullable=False),
        sa.Column("recipient_scope", sa.String(64), default="SOC_ANALYSTS", nullable=False),
        sa.Column("recipient_targets", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
    )

    # 17. notification_deliveries
    op.create_table(
        "notification_deliveries",
        sa.Column("delivery_id", sa.String(64), primary_key=True),
        sa.Column("alert_id", sa.String(64), sa.ForeignKey("security_alerts.alert_id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("policy_id", sa.String(64), nullable=True),
        sa.Column("channel", sa.String(30), nullable=False),
        sa.Column("recipient", sa.String(255), nullable=False),
        sa.Column("delivery_status", sa.String(30), default="QUEUED", nullable=False),
        sa.Column("sent_at", sa.DateTime(), nullable=True),
        sa.Column("delivered_at", sa.DateTime(), nullable=True),
        sa.Column("error_message", sa.Text(), nullable=True),
        sa.Column("retry_count", sa.Integer(), default=0, nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )

    # 18. intelligence_reassessments
    op.create_table(
        "intelligence_reassessments",
        sa.Column("reassessment_id", sa.String(64), primary_key=True),
        sa.Column("analysis_id", sa.String(64), nullable=False, index=True),
        sa.Column("case_id", sa.String(64), nullable=True, index=True),
        sa.Column("trigger_event_id", sa.String(64), nullable=False),
        sa.Column("impact_level", sa.String(30), nullable=False),
        sa.Column("previous_risk_score", sa.Float(), nullable=False),
        sa.Column("proposed_risk_score", sa.Float(), nullable=False),
        sa.Column("status", sa.String(30), default="PENDING_APPROVAL", nullable=False),
        sa.Column("requested_by", sa.String(64), default="SYSTEM_AUTOMATION", nullable=False),
        sa.Column("approved_by", sa.String(64), nullable=True),
        sa.Column("reason", sa.Text(), default="", nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("resolved_at", sa.DateTime(), nullable=True),
    )

    # 19. risk_assessment_versions
    op.create_table(
        "risk_assessment_versions",
        sa.Column("version_id", sa.String(64), primary_key=True),
        sa.Column("analysis_id", sa.String(64), nullable=False, index=True),
        sa.Column("report_id", sa.String(64), nullable=False, index=True),
        sa.Column("version_number", sa.Integer(), nullable=False),
        sa.Column("risk_score", sa.Float(), nullable=False),
        sa.Column("risk_band", sa.String(30), nullable=False),
        sa.Column("confidence", sa.String(30), nullable=False),
        sa.Column("policy_version", sa.String(30), default="1.0.0", nullable=False),
        sa.Column("trigger_event_id", sa.String(64), nullable=True),
        sa.Column("supporting_intelligence", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )

    # 20. incident_records
    op.create_table(
        "incident_records",
        sa.Column("incident_id", sa.String(64), primary_key=True),
        sa.Column("case_id", sa.String(64), nullable=True, index=True),
        sa.Column("incident_type", sa.String(50), default="UNKNOWN_INCIDENT", nullable=False, index=True),
        sa.Column("title", sa.String(255), nullable=False),
        sa.Column("status", sa.String(30), default="DETECTED", nullable=False, index=True),
        sa.Column("priority", sa.String(30), default="MEDIUM", nullable=False),
        sa.Column("severity", sa.String(30), default="MEDIUM", nullable=False),
        sa.Column("confidence", sa.String(30), default="HIGH", nullable=False),
        sa.Column("first_seen", sa.DateTime(), nullable=False),
        sa.Column("last_seen", sa.DateTime(), nullable=False),
        sa.Column("alert_count", sa.Integer(), default=1, nullable=False),
        sa.Column("entity_count", sa.Integer(), default=1, nullable=False),
        sa.Column("finding_count", sa.Integer(), default=0, nullable=False),
        sa.Column("campaign_id", sa.String(64), nullable=True, index=True),
        sa.Column("attack_chain_id", sa.String(64), nullable=True, index=True),
        sa.Column("organization_id", sa.String(64), nullable=True, index=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
    )

    # 21. report_update_events
    op.create_table(
        "report_update_events",
        sa.Column("update_event_id", sa.String(64), primary_key=True),
        sa.Column("report_id", sa.String(64), nullable=False, index=True),
        sa.Column("previous_version", sa.Integer(), nullable=False),
        sa.Column("new_version", sa.Integer(), nullable=False),
        sa.Column("change_reason", sa.Text(), nullable=False),
        sa.Column("intelligence_source_ids", sa.JSON(), nullable=False),
        sa.Column("triggered_by", sa.String(64), default="SYSTEM_REASSESSMENT", nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )

    # 22. real_time_subscriptions
    op.create_table(
        "real_time_subscriptions",
        sa.Column("subscription_id", sa.String(64), primary_key=True),
        sa.Column("client_id", sa.String(128), nullable=False, index=True),
        sa.Column("user_id", sa.String(64), nullable=False, index=True),
        sa.Column("organization_id", sa.String(64), nullable=True, index=True),
        sa.Column("channel_scope", sa.String(64), default="ALL", nullable=False),
        sa.Column("case_ids", sa.JSON(), nullable=False),
        sa.Column("analysis_ids", sa.JSON(), nullable=False),
        sa.Column("subscribed_at", sa.DateTime(), nullable=False),
        sa.Column("last_heartbeat", sa.DateTime(), nullable=False),
    )


def downgrade() -> None:
    op.drop_table("real_time_subscriptions")
    op.drop_table("report_update_events")
    op.drop_table("incident_records")
    op.drop_table("risk_assessment_versions")
    op.drop_table("intelligence_reassessments")
    op.drop_table("notification_deliveries")
    op.drop_table("notification_policies")
    op.drop_table("alert_escalations")
    op.drop_table("alert_acknowledgements")
    op.drop_table("alert_suppressions")
    op.drop_table("alert_fingerprints")
    op.drop_table("security_alerts")
    op.drop_table("event_dead_letters")
    op.drop_table("event_processing_records")
    op.drop_table("continuous_intelligence_events")
    op.drop_table("monitoring_job_runs")
    op.drop_table("monitoring_jobs")
    op.drop_table("intelligence_state_changes")
    op.drop_table("continuous_intelligence_observations")
    op.drop_table("threat_feed_versions")
    op.drop_table("threat_feed_health")
    op.drop_table("threat_feed_configurations")
