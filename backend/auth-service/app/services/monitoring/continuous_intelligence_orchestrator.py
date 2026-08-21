"""Continuous Intelligence Orchestrator (Phase 4.0 Part 6 — Section 84).

Executes the full end-to-end continuous intelligence synchronization pipeline.
"""

from typing import List, Dict, Any, Optional, Tuple
import time
import uuid
from datetime import datetime, timezone
from app.schemas.continuous_intelligence_models import (
    ThreatFeedConfigurationDTO,
    ThreatFeedHealthDTO,
    ThreatFeedSyncResponseDTO,
    IntelligenceObservationDTO,
    IntelligenceChangeEventDTO,
    IntelligenceEventDTO,
    SecurityAlertDTO,
)
from app.services.monitoring.threat_intelligence_provider import (
    ThreatIntelligenceProvider,
    JSONFeedProvider,
    STIXTAXIIProvider,
    CSVFeedProvider,
    RESTAPIProvider,
    LocalDatabaseProvider,
)
from app.services.monitoring.feed_validator import FeedValidator
from app.services.monitoring.intelligence_change_detector import IntelligenceChangeDetector
from app.services.monitoring.intelligence_event_bus import IntelligenceEventBus
from app.services.monitoring.intelligence_impact_engine import IntelligenceImpactEngine
from app.services.monitoring.security_alert_engine import SecurityAlertEngine
from app.services.monitoring.notification_router import NotificationRouter
from app.services.monitoring.incident_correlation_engine import IncidentCorrelationEngine
from app.services.monitoring.realtime_hub import RealtimeHub


class ContinuousIntelligenceOrchestrator:
    """Coordinates the continuous synchronization, change detection, impact analysis, and alert workflow."""

    def __init__(
        self,
        event_bus: Optional[IntelligenceEventBus] = None,
        alert_engine: Optional[SecurityAlertEngine] = None,
        notification_router: Optional[NotificationRouter] = None,
        incident_engine: Optional[IncidentCorrelationEngine] = None,
        realtime_hub: Optional[RealtimeHub] = None,
    ):
        self.event_bus = event_bus or IntelligenceEventBus()
        self.alert_engine = alert_engine or SecurityAlertEngine()
        self.notification_router = notification_router or NotificationRouter()
        self.incident_engine = incident_engine or IncidentCorrelationEngine()
        self.realtime_hub = realtime_hub or RealtimeHub()
        self.historical_observations: Dict[str, IntelligenceObservationDTO] = {}
        self.monitored_entities: List[str] = []

    def register_monitored_entity(self, entity_value_hash: str) -> None:
        if entity_value_hash not in self.monitored_entities:
            self.monitored_entities.append(entity_value_hash)

    def synchronize_feed(
        self,
        config: ThreatFeedConfigurationDTO,
        provider: ThreatIntelligenceProvider,
    ) -> ThreatFeedSyncResponseDTO:
        """Execute full feed synchronization cycle (Section 84)."""
        start_time = time.time()
        items_received = 0
        items_accepted = 0
        items_rejected = 0
        changes_detected = 0
        events_published = 0
        alerts_generated = 0

        try:
            # 1. Fetch data from provider
            raw_items = provider.fetch_indicators()
            items_received = len(raw_items)

            # 2. Validate and normalize each item
            normalized_obs: List[IntelligenceObservationDTO] = []
            for item in raw_items:
                obs = FeedValidator.validate_and_normalize_item(config, item)
                if obs:
                    normalized_obs.append(obs)
                    items_accepted += 1
                else:
                    items_rejected += 1

            # 3. Deduplicate within feed run
            deduped_obs = FeedValidator.deduplicate_observations(normalized_obs)

            # 4. Detect state changes against historical baseline
            changes = IntelligenceChangeDetector.detect_changes(deduped_obs, self.historical_observations)
            changes_detected = len(changes)

            # 5. Process each change
            for change in changes:
                # 5a. Publish to Event Bus
                evt = IntelligenceEventDTO(
                    event_id=change.event_id,
                    event_type=change.event_type,
                    entity_id=change.entity_id,
                    analysis_id=change.analysis_id,
                    case_id=change.case_id,
                    correlation_id=f"corr_{uuid.uuid4().hex[:8]}",
                    payload={"new_state": change.new_state, "previous_state": change.previous_state, "feed_id": config.feed_id},
                    provenance=change.provenance,
                )
                published = self.event_bus.publish(evt)
                if published:
                    events_published += 1

                # 5b. Evaluate Impact
                impact = IntelligenceImpactEngine.evaluate_impact(change, self.monitored_entities)

                # 5c. Generate Security Alert if impactful
                if impact.impact_level in ("MEDIUM_IMPACT", "HIGH_IMPACT", "CRITICAL_IMPACT"):
                    alert = self.alert_engine.generate_alert(
                        change,
                        impact,
                        case_id=change.case_id,
                        analysis_id=change.analysis_id,
                        organization_id=config.organization_id,
                    )
                    if alert:
                        alerts_generated += 1
                        # 5d. Route Notifications
                        self.notification_router.route_alert_notifications(alert)
                        # 5e. Correlate Incident
                        self.incident_engine.correlate_alert_to_incident(alert)

                # 5f. Real-time broadcast
                self.realtime_hub.dispatch_event(evt)

            # 6. Update historical observation baseline
            for obs in deduped_obs:
                key = f"{obs.indicator_type}:{obs.indicator_value_hash}"
                self.historical_observations[key] = obs

            exec_time = (time.time() - start_time) * 1000.0
            return ThreatFeedSyncResponseDTO(
                feed_id=config.feed_id,
                status="SUCCESS",
                items_received=items_received,
                items_accepted=items_accepted,
                items_rejected=items_rejected,
                changes_detected=changes_detected,
                events_published=events_published,
                alerts_generated=alerts_generated,
                execution_time_ms=exec_time,
            )

        except Exception as ex:
            exec_time = (time.time() - start_time) * 1000.0
            return ThreatFeedSyncResponseDTO(
                feed_id=config.feed_id,
                status="FAILED",
                items_received=items_received,
                items_accepted=items_accepted,
                items_rejected=items_rejected,
                changes_detected=0,
                events_published=0,
                alerts_generated=0,
                execution_time_ms=exec_time,
            )
