"""Trust Monitoring Engine Master Facade (Phase 4.0 Part 6 — Section 1).

Coordinates continuous intelligence monitoring, scheduled sync jobs, real-time alerting,
and versioned reassessments.
"""

from typing import List, Dict, Any, Optional, Tuple
from app.schemas.continuous_intelligence_models import (
    ThreatFeedConfigurationDTO,
    ThreatFeedHealthDTO,
    ThreatFeedSyncResponseDTO,
    SecurityAlertDTO,
    SecurityIncidentDTO,
    IntelligenceEventDTO,
    RealtimeSubscriptionDTO,
    IntelligenceReassessmentDTO,
    RiskAssessmentVersionDTO,
    ReportUpdateEventDTO,
    AlertAcknowledgementDTO,
    AlertEscalationDTO,
    AlertSuppressionDTO,
    AlertPriorityLiteral,
    AlertStatusLiteral,
)
from app.services.monitoring.continuous_intelligence_orchestrator import ContinuousIntelligenceOrchestrator
from app.services.monitoring.monitoring_scheduler import MonitoringScheduler
from app.services.monitoring.threat_intelligence_provider import JSONFeedProvider, ThreatIntelligenceProvider
from app.services.monitoring.reassessment_orchestrator import ReassessmentOrchestrator


class TrustMonitoringEngine:
    """Master facade for TruthShield X continuous trust intelligence and monitoring."""

    def __init__(self):
        self.orchestrator = ContinuousIntelligenceOrchestrator()
        self.scheduler = MonitoringScheduler()
        self._feeds: Dict[str, ThreatFeedConfigurationDTO] = {}
        self._reassessments: Dict[str, IntelligenceReassessmentDTO] = {}

    def register_feed(self, config: ThreatFeedConfigurationDTO) -> ThreatFeedConfigurationDTO:
        """Register a new threat intelligence feed."""
        self._feeds[config.feed_id] = config
        self.scheduler.register_feed(config)
        return config

    def get_feed(self, feed_id: str) -> Optional[ThreatFeedConfigurationDTO]:
        return self._feeds.get(feed_id)

    def list_feeds(self) -> List[ThreatFeedConfigurationDTO]:
        return list(self._feeds.values())

    def sync_feed(self, feed_id: str, provider: Optional[ThreatIntelligenceProvider] = None) -> ThreatFeedSyncResponseDTO:
        """Manually trigger synchronization of a registered threat feed."""
        config = self._feeds.get(feed_id)
        if not config:
            raise KeyError(f"Feed {feed_id} not found.")

        feed_provider = provider or JSONFeedProvider(config)
        return self.orchestrator.synchronize_feed(config, feed_provider)

    def list_alerts(
        self,
        status: Optional[AlertStatusLiteral] = None,
        priority: Optional[AlertPriorityLiteral] = None,
        case_id: Optional[str] = None,
    ) -> List[SecurityAlertDTO]:
        return self.orchestrator.alert_engine.list_alerts(status=status, priority=priority, case_id=case_id)

    def get_alert(self, alert_id: str) -> Optional[SecurityAlertDTO]:
        return self.orchestrator.alert_engine.get_alert(alert_id)

    def acknowledge_alert(
        self,
        alert_id: str,
        user_id: str,
        user_name: str,
        reason: str,
        comment: Optional[str] = None,
    ) -> Tuple[SecurityAlertDTO, AlertAcknowledgementDTO]:
        return self.orchestrator.alert_engine.acknowledge_alert(alert_id, user_id, user_name, reason, comment)

    def escalate_alert(
        self,
        alert_id: str,
        new_priority: AlertPriorityLiteral,
        reason: str,
        escalated_by: Optional[str] = None,
    ) -> Tuple[SecurityAlertDTO, AlertEscalationDTO]:
        return self.orchestrator.alert_engine.escalate_alert(alert_id, new_priority, reason, escalated_by)

    def suppress_alert(
        self,
        alert_id: str,
        reason: str,
        suppressed_by: str,
        duration_hours: int = 24,
    ) -> Tuple[SecurityAlertDTO, AlertSuppressionDTO]:
        return self.orchestrator.alert_engine.suppress_alert(alert_id, reason, suppressed_by, duration_hours)

    def resolve_alert(self, alert_id: str, resolution_note: str = "") -> SecurityAlertDTO:
        return self.orchestrator.alert_engine.resolve_alert(alert_id, resolution_note)

    def list_incidents(self) -> List[SecurityIncidentDTO]:
        return self.orchestrator.incident_engine.list_incidents()

    def get_incident(self, incident_id: str) -> Optional[SecurityIncidentDTO]:
        return self.orchestrator.incident_engine.get_incident(incident_id)

    def subscribe_realtime(
        self,
        client_id: str,
        user_id: str,
        organization_id: Optional[str] = None,
        case_ids: Optional[List[str]] = None,
        analysis_ids: Optional[List[str]] = None,
    ) -> RealtimeSubscriptionDTO:
        return self.orchestrator.realtime_hub.subscribe(client_id, user_id, organization_id, case_ids, analysis_ids)

    def list_events(self) -> List[IntelligenceEventDTO]:
        return self.orchestrator.event_bus.get_events()
