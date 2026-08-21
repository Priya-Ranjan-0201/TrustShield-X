"""SQLAlchemy 2.0 ORM Models for Real-Time Trust Monitoring & Continuous Intelligence (Phase 4.0 Part 6).

Defines 22 database tables:
1. threat_feed_configurations
2. threat_feed_health
3. threat_feed_versions
4. intelligence_observations
5. intelligence_state_changes
6. monitoring_jobs
7. monitoring_job_runs
8. intelligence_events
9. event_processing_records
10. event_dead_letters
11. security_alerts
12. alert_fingerprints
13. alert_suppressions
14. alert_acknowledgements
15. alert_escalations
16. notification_policies
17. notification_deliveries
18. intelligence_reassessments
19. risk_assessment_versions
20. incident_records
21. report_update_events
22. real_time_subscriptions
"""

import uuid
from datetime import datetime, timezone
from sqlalchemy import (
    Column,
    String,
    Integer,
    Float,
    Boolean,
    DateTime,
    Text,
    JSON,
    ForeignKey,
    Index,
)
from app.models.base import Base


class ThreatFeedConfigurationModel(Base):
    __tablename__ = "threat_feed_configurations"

    feed_id = Column(String(64), primary_key=True, default=lambda: f"feed_{uuid.uuid4().hex[:12]}")
    provider_name = Column(String(128), nullable=False, index=True)
    provider_type = Column(String(50), nullable=False)
    endpoint = Column(String(512), nullable=False)
    enabled = Column(Boolean, default=True, nullable=False)
    poll_interval = Column(String(50), default="HOURLY", nullable=False)
    poll_interval_seconds = Column(Integer, default=3600, nullable=False)
    authentication_mode = Column(String(50), default="NONE", nullable=False)
    timeout_seconds = Column(Integer, default=30, nullable=False)
    retry_policy = Column(JSON, default=dict, nullable=False)
    rate_limit = Column(JSON, default=dict, nullable=False)
    supported_types = Column(JSON, default=list, nullable=False)
    trust_level = Column(String(30), default="STANDARD", nullable=False)
    freshness_policy = Column(JSON, default=dict, nullable=False)
    organization_id = Column(String(64), nullable=True, index=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)


class ThreatFeedHealthModel(Base):
    __tablename__ = "threat_feed_health"

    health_id = Column(String(64), primary_key=True, default=lambda: f"fhl_{uuid.uuid4().hex[:12]}")
    feed_id = Column(String(64), ForeignKey("threat_feed_configurations.feed_id", ondelete="CASCADE"), nullable=False, index=True)
    status = Column(String(30), default="UNKNOWN", nullable=False)
    last_success = Column(DateTime, nullable=True)
    last_failure = Column(DateTime, nullable=True)
    last_attempt = Column(DateTime, nullable=True)
    latency_ms = Column(Float, default=0.0, nullable=False)
    items_received = Column(Integer, default=0, nullable=False)
    items_accepted = Column(Integer, default=0, nullable=False)
    items_rejected = Column(Integer, default=0, nullable=False)
    parse_errors = Column(Integer, default=0, nullable=False)
    authentication_errors = Column(Integer, default=0, nullable=False)
    rate_limit_errors = Column(Integer, default=0, nullable=False)
    network_errors = Column(Integer, default=0, nullable=False)
    staleness_days = Column(Float, default=0.0, nullable=False)
    provider_version = Column(String(30), default="1.0.0", nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)


class ThreatFeedVersionModel(Base):
    __tablename__ = "threat_feed_versions"

    version_id = Column(String(64), primary_key=True, default=lambda: f"fver_{uuid.uuid4().hex[:12]}")
    feed_id = Column(String(64), ForeignKey("threat_feed_configurations.feed_id", ondelete="CASCADE"), nullable=False, index=True)
    version_tag = Column(String(64), nullable=False)
    content_hash = Column(String(64), nullable=False)
    items_count = Column(Integer, default=0, nullable=False)
    fetched_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)


class IntelligenceObservationModel(Base):
    __tablename__ = "continuous_intelligence_observations"

    observation_id = Column(String(64), primary_key=True, default=lambda: f"obs_{uuid.uuid4().hex[:12]}")
    feed_id = Column(String(64), ForeignKey("threat_feed_configurations.feed_id", ondelete="CASCADE"), nullable=False, index=True)
    indicator_id = Column(String(128), nullable=False, index=True)
    indicator_type = Column(String(50), nullable=False, index=True)
    indicator_value_hash = Column(String(64), nullable=False, index=True)
    normalized_value = Column(Text, nullable=False)
    raw_value = Column(Text, nullable=False)
    observation_type = Column(String(30), default="NEW", nullable=False)
    classification = Column(String(50), default="MALICIOUS", nullable=False)
    confidence = Column(String(20), default="HIGH", nullable=False)
    first_seen = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    last_seen = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    observed_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    source_timestamp = Column(DateTime, nullable=True)
    feed_version = Column(String(30), default="1.0.0", nullable=False)
    raw_reference = Column(Text, nullable=True)
    status = Column(String(30), default="ACTIVE", nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)


class IntelligenceStateChangeModel(Base):
    __tablename__ = "intelligence_state_changes"

    change_id = Column(String(64), primary_key=True, default=lambda: f"isch_{uuid.uuid4().hex[:12]}")
    entity_id = Column(String(64), nullable=False, index=True)
    observation_id = Column(String(64), nullable=False, index=True)
    previous_state = Column(String(50), nullable=False)
    new_state = Column(String(50), nullable=False)
    transition_reason = Column(Text, nullable=False)
    transition_timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    source = Column(String(128), nullable=False)


class MonitoringJobModel(Base):
    __tablename__ = "monitoring_jobs"

    job_id = Column(String(64), primary_key=True, default=lambda: f"mjob_{uuid.uuid4().hex[:12]}")
    feed_id = Column(String(64), ForeignKey("threat_feed_configurations.feed_id", ondelete="CASCADE"), nullable=False, index=True)
    job_type = Column(String(50), default="SYNC", nullable=False)
    schedule_type = Column(String(50), default="HOURLY", nullable=False)
    interval_seconds = Column(Integer, default=3600, nullable=False)
    cron_expression = Column(String(64), nullable=True)
    enabled = Column(Boolean, default=True, nullable=False)
    next_run_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    last_run_at = Column(DateTime, nullable=True)
    status = Column(String(30), default="QUEUED", nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)


class MonitoringJobRunModel(Base):
    __tablename__ = "monitoring_job_runs"

    run_id = Column(String(64), primary_key=True, default=lambda: f"mjr_{uuid.uuid4().hex[:12]}")
    job_id = Column(String(64), ForeignKey("monitoring_jobs.job_id", ondelete="CASCADE"), nullable=False, index=True)
    feed_id = Column(String(64), nullable=False, index=True)
    status = Column(String(30), default="RUNNING", nullable=False)
    started_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    completed_at = Column(DateTime, nullable=True)
    attempt = Column(Integer, default=1, nullable=False)
    items_processed = Column(Integer, default=0, nullable=False)
    items_failed = Column(Integer, default=0, nullable=False)
    error_code = Column(String(64), nullable=True)
    error_message = Column(Text, nullable=True)


class IntelligenceEventModel(Base):
    __tablename__ = "continuous_intelligence_events"

    event_id = Column(String(64), primary_key=True, default=lambda: f"evt_{uuid.uuid4().hex[:12]}")
    event_type = Column(String(64), nullable=False, index=True)
    event_version = Column(String(20), default="1.0.0", nullable=False)
    schema_version = Column(String(20), default="1.0.0", nullable=False)
    producer = Column(String(128), default="continuous_intelligence_orchestrator", nullable=False)
    entity_id = Column(String(64), nullable=True, index=True)
    analysis_id = Column(String(64), nullable=True, index=True)
    case_id = Column(String(64), nullable=True, index=True)
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    correlation_id = Column(String(64), nullable=False, index=True)
    causation_id = Column(String(64), nullable=True)
    payload = Column(JSON, default=dict, nullable=False)
    provenance = Column(Text, default="", nullable=False)
    deduplication_key = Column(String(128), nullable=False, unique=True, index=True)


class EventProcessingRecordModel(Base):
    __tablename__ = "event_processing_records"

    record_id = Column(String(64), primary_key=True, default=lambda: f"epr_{uuid.uuid4().hex[:12]}")
    event_id = Column(String(64), ForeignKey("continuous_intelligence_events.event_id", ondelete="CASCADE"), nullable=False, index=True)
    consumer_id = Column(String(128), nullable=False)
    status = Column(String(30), default="PROCESSED", nullable=False)
    attempts = Column(Integer, default=1, nullable=False)
    processed_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    error_message = Column(Text, nullable=True)


class EventDeadLetterModel(Base):
    __tablename__ = "event_dead_letters"

    dead_letter_id = Column(String(64), primary_key=True, default=lambda: f"edl_{uuid.uuid4().hex[:12]}")
    event_id = Column(String(64), nullable=False, index=True)
    error = Column(Text, nullable=False)
    attempts = Column(Integer, default=1, nullable=False)
    last_attempt = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    consumer = Column(String(128), nullable=False)
    payload_reference = Column(Text, nullable=False)
    status = Column(String(30), default="PENDING", nullable=False)
    reprocessed_at = Column(DateTime, nullable=True)
    reprocessed_by = Column(String(64), nullable=True)


class SecurityAlertModel(Base):
    __tablename__ = "security_alerts"

    alert_id = Column(String(64), primary_key=True, default=lambda: f"alt_{uuid.uuid4().hex[:12]}")
    case_id = Column(String(64), nullable=True, index=True)
    analysis_id = Column(String(64), nullable=True, index=True)
    event_id = Column(String(64), nullable=True, index=True)
    alert_type = Column(String(64), nullable=False, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    priority = Column(String(30), default="MEDIUM", nullable=False, index=True)
    severity = Column(String(30), default="MEDIUM", nullable=False)
    confidence = Column(String(30), default="HIGH", nullable=False)
    status = Column(String(30), default="NEW", nullable=False, index=True)
    source = Column(String(128), default="THREAT_MONITOR", nullable=False)
    evidence_ids = Column(JSON, default=list, nullable=False)
    finding_ids = Column(JSON, default=list, nullable=False)
    entity_ids = Column(JSON, default=list, nullable=False)
    relationship_ids = Column(JSON, default=list, nullable=False)
    campaign_id = Column(String(64), nullable=True, index=True)
    attack_chain_id = Column(String(64), nullable=True, index=True)
    alert_fingerprint = Column(String(64), nullable=False, index=True)
    organization_id = Column(String(64), nullable=True, index=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)
    acknowledged_at = Column(DateTime, nullable=True)
    resolved_at = Column(DateTime, nullable=True)
    suppressed_until = Column(DateTime, nullable=True)


class AlertFingerprintModel(Base):
    __tablename__ = "alert_fingerprints"

    fingerprint_id = Column(String(64), primary_key=True, default=lambda: f"afp_{uuid.uuid4().hex[:12]}")
    fingerprint_hash = Column(String(64), nullable=False, unique=True, index=True)
    alert_type = Column(String(64), nullable=False)
    entity_id = Column(String(64), nullable=True)
    case_id = Column(String(64), nullable=True)
    last_seen = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    occurrences = Column(Integer, default=1, nullable=False)


class AlertSuppressionModel(Base):
    __tablename__ = "alert_suppressions"

    suppression_id = Column(String(64), primary_key=True, default=lambda: f"sup_{uuid.uuid4().hex[:12]}")
    alert_fingerprint = Column(String(64), nullable=False, index=True)
    alert_type = Column(String(64), nullable=False)
    reason = Column(Text, nullable=False)
    suppressed_by = Column(String(64), nullable=False)
    expires_at = Column(DateTime, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    allow_critical_override = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)


class AlertAcknowledgementModel(Base):
    __tablename__ = "alert_acknowledgements"

    ack_id = Column(String(64), primary_key=True, default=lambda: f"ack_{uuid.uuid4().hex[:12]}")
    alert_id = Column(String(64), ForeignKey("security_alerts.alert_id", ondelete="CASCADE"), nullable=False, index=True)
    user_id = Column(String(64), nullable=False)
    user_name = Column(String(128), nullable=False)
    reason = Column(Text, nullable=False)
    comment = Column(Text, nullable=True)
    acknowledged_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)


class AlertEscalationModel(Base):
    __tablename__ = "alert_escalations"

    escalation_id = Column(String(64), primary_key=True, default=lambda: f"esc_{uuid.uuid4().hex[:12]}")
    alert_id = Column(String(64), ForeignKey("security_alerts.alert_id", ondelete="CASCADE"), nullable=False, index=True)
    previous_priority = Column(String(30), nullable=False)
    escalated_priority = Column(String(30), nullable=False)
    escalation_type = Column(String(50), default="TIMEOUT", nullable=False)
    reason = Column(Text, nullable=False)
    escalated_by = Column(String(64), nullable=True)
    escalated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)


class NotificationPolicyModel(Base):
    __tablename__ = "notification_policies"

    policy_id = Column(String(64), primary_key=True, default=lambda: f"npol_{uuid.uuid4().hex[:12]}")
    organization_id = Column(String(64), nullable=True, index=True)
    alert_type = Column(String(64), nullable=False)
    min_priority = Column(String(30), default="HIGH", nullable=False)
    channel = Column(String(30), default="IN_APP", nullable=False)
    enabled = Column(Boolean, default=True, nullable=False)
    cooldown_minutes = Column(Integer, default=15, nullable=False)
    recipient_scope = Column(String(64), default="SOC_ANALYSTS", nullable=False)
    recipient_targets = Column(JSON, default=list, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)


class NotificationDeliveryModel(Base):
    __tablename__ = "notification_deliveries"

    delivery_id = Column(String(64), primary_key=True, default=lambda: f"ndel_{uuid.uuid4().hex[:12]}")
    alert_id = Column(String(64), ForeignKey("security_alerts.alert_id", ondelete="CASCADE"), nullable=False, index=True)
    policy_id = Column(String(64), nullable=True)
    channel = Column(String(30), nullable=False)
    recipient = Column(String(255), nullable=False)
    delivery_status = Column(String(30), default="QUEUED", nullable=False)
    sent_at = Column(DateTime, nullable=True)
    delivered_at = Column(DateTime, nullable=True)
    error_message = Column(Text, nullable=True)
    retry_count = Column(Integer, default=0, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)


class IntelligenceReassessmentModel(Base):
    __tablename__ = "intelligence_reassessments"

    reassessment_id = Column(String(64), primary_key=True, default=lambda: f"reass_{uuid.uuid4().hex[:12]}")
    analysis_id = Column(String(64), nullable=False, index=True)
    case_id = Column(String(64), nullable=True, index=True)
    trigger_event_id = Column(String(64), nullable=False)
    impact_level = Column(String(30), nullable=False)
    previous_risk_score = Column(Float, nullable=False)
    proposed_risk_score = Column(Float, nullable=False)
    status = Column(String(30), default="PENDING_APPROVAL", nullable=False)
    requested_by = Column(String(64), default="SYSTEM_AUTOMATION", nullable=False)
    approved_by = Column(String(64), nullable=True)
    reason = Column(Text, default="", nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    resolved_at = Column(DateTime, nullable=True)


class RiskAssessmentVersionModel(Base):
    __tablename__ = "risk_assessment_versions"

    version_id = Column(String(64), primary_key=True, default=lambda: f"rav_{uuid.uuid4().hex[:12]}")
    analysis_id = Column(String(64), nullable=False, index=True)
    report_id = Column(String(64), nullable=False, index=True)
    version_number = Column(Integer, nullable=False)
    risk_score = Column(Float, nullable=False)
    risk_band = Column(String(30), nullable=False)
    confidence = Column(String(30), nullable=False)
    policy_version = Column(String(30), default="1.0.0", nullable=False)
    trigger_event_id = Column(String(64), nullable=True)
    supporting_intelligence = Column(JSON, default=list, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)


class SecurityIncidentModel(Base):
    __tablename__ = "incident_records"

    incident_id = Column(String(64), primary_key=True, default=lambda: f"inc_{uuid.uuid4().hex[:12]}")
    case_id = Column(String(64), nullable=True, index=True)
    incident_type = Column(String(50), default="UNKNOWN_INCIDENT", nullable=False, index=True)
    title = Column(String(255), nullable=False)
    status = Column(String(30), default="DETECTED", nullable=False, index=True)
    priority = Column(String(30), default="MEDIUM", nullable=False)
    severity = Column(String(30), default="MEDIUM", nullable=False)
    confidence = Column(String(30), default="HIGH", nullable=False)
    first_seen = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    last_seen = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    alert_count = Column(Integer, default=1, nullable=False)
    entity_count = Column(Integer, default=1, nullable=False)
    finding_count = Column(Integer, default=0, nullable=False)
    campaign_id = Column(String(64), nullable=True, index=True)
    attack_chain_id = Column(String(64), nullable=True, index=True)
    organization_id = Column(String(64), nullable=True, index=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)


class ReportUpdateEventModel(Base):
    __tablename__ = "report_update_events"

    update_event_id = Column(String(64), primary_key=True, default=lambda: f"rue_{uuid.uuid4().hex[:12]}")
    report_id = Column(String(64), nullable=False, index=True)
    previous_version = Column(Integer, nullable=False)
    new_version = Column(Integer, nullable=False)
    change_reason = Column(Text, nullable=False)
    intelligence_source_ids = Column(JSON, default=list, nullable=False)
    triggered_by = Column(String(64), default="SYSTEM_REASSESSMENT", nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)


class RealtimeSubscriptionModel(Base):
    __tablename__ = "real_time_subscriptions"

    subscription_id = Column(String(64), primary_key=True, default=lambda: f"rsub_{uuid.uuid4().hex[:12]}")
    client_id = Column(String(128), nullable=False, index=True)
    user_id = Column(String(64), nullable=False, index=True)
    organization_id = Column(String(64), nullable=True, index=True)
    channel_scope = Column(String(64), default="ALL", nullable=False)
    case_ids = Column(JSON, default=list, nullable=False)
    analysis_ids = Column(JSON, default=list, nullable=False)
    subscribed_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    last_heartbeat = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
