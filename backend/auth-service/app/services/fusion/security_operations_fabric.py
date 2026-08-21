"""
TruthShield X — Master Security Operations Fabric
"""

from typing import Dict, List, Optional, Any
from datetime import datetime, timezone
from app.schemas.fusion_models import (
    SecurityEventDTO,
    EventCorrelationResultDTO,
    ThreatClusterDTO,
    SecuritySituationDTO,
    SecurityPostureDTO,
    SecurityNarrativeDTO,
    IncidentCommandStateDTO,
    SecurityKpisDTO,
    SecurityHealthOverviewDTO,
)
from app.services.fusion.event_normalization_service import EventNormalizationService
from app.services.fusion.security_event_correlation_engine import SecurityEventCorrelationEngine
from app.services.fusion.threat_fusion_engine import ThreatFusionEngine
from app.services.fusion.security_posture_engine import SecurityPostureEngine
from app.services.fusion.security_priority_engine import SecurityPriorityEngine
from app.services.fusion.security_narrative_engine import SecurityNarrativeEngine
from app.services.fusion.incident_command_engine import IncidentCommandEngine
from app.services.fusion.realtime_event_stream_service import RealTimeEventStreamService
from app.services.fusion.security_health_engine import SecurityHealthEngine


class SecurityOperationsFabric:
    """Master orchestration layer connecting detection, threat fusion, asset intelligence, reasoning, posture, and incident command."""

    def __init__(
        self,
        event_service: Optional[EventNormalizationService] = None,
        correlation_engine: Optional[SecurityEventCorrelationEngine] = None,
        fusion_engine: Optional[ThreatFusionEngine] = None,
        posture_engine: Optional[SecurityPostureEngine] = None,
        priority_engine: Optional[SecurityPriorityEngine] = None,
        narrative_engine: Optional[SecurityNarrativeEngine] = None,
        incident_engine: Optional[IncidentCommandEngine] = None,
        stream_service: Optional[RealTimeEventStreamService] = None,
        health_engine: Optional[SecurityHealthEngine] = None,
    ):
        self.events = event_service or EventNormalizationService()
        self.correlation = correlation_engine or SecurityEventCorrelationEngine()
        self.fusion = fusion_engine or ThreatFusionEngine()
        self.posture = posture_engine or SecurityPostureEngine()
        self.priority = priority_engine or SecurityPriorityEngine()
        self.narrative = narrative_engine or SecurityNarrativeEngine()
        self.incident = incident_engine or IncidentCommandEngine()
        self.stream = stream_service or RealTimeEventStreamService()
        self.health = health_engine or SecurityHealthEngine()

    def process_incoming_security_telemetry(
        self,
        event_type: str,
        source: str,
        entity_id: Optional[str] = None,
        asset_id: Optional[str] = None,
        campaign_id: Optional[str] = None,
        severity: str = "MEDIUM",
        confidence: float = 0.90,
        risk_score: float = 20.0,
        trust_score: float = 80.0,
        exposure_score: float = 20.0,
        provenance: Optional[Dict[str, Any]] = None,
        tenant_id: str = "default_tenant",
    ) -> Dict[str, Any]:
        """Ingests telemetry through the complete unified Security Operations Fabric pipeline."""
        # 1. Normalize & Ingest
        event = self.events.ingest_and_normalize(
            event_type=event_type,  # type: ignore
            source=source,
            entity_id=entity_id,
            asset_id=asset_id,
            campaign_id=campaign_id,
            severity=severity,
            confidence=confidence,
            risk_score=risk_score,
            trust_score=trust_score,
            exposure_score=exposure_score,
            provenance=provenance,
            tenant_id=tenant_id,
        )

        # 2. Publish to Real-Time Stream
        self.stream.publish_event(event.model_dump(), schema_version="security.event.v1", tenant_id=tenant_id)

        # 3. Correlate with recent events
        recent = self.events.list_events(tenant_id=tenant_id, limit=10)
        corr = self.correlation.correlate_events(recent, tenant_id=tenant_id) if len(recent) > 1 else None

        # 4. Multi-Modal Threat Fusion & Clustering
        cluster = self.fusion.cluster_threat_events(recent, tenant_id=tenant_id) if len(recent) > 1 else None

        # 5. Evaluate Situation & Posture
        sit = self.posture.evaluate_situation(
            active_threats_count=len(recent),
            critical_assets_count=1 if asset_id else 0,
            high_risk_exposure_count=1 if exposure_score >= 60.0 else 0,
            active_campaigns_count=1 if campaign_id else 0,
            open_incidents_count=0,
            tenant_id=tenant_id,
        )
        pos = self.posture.calculate_posture(
            risk_score=risk_score,
            trust_score=trust_score,
            exposure_score=exposure_score,
            active_threats_count=len(recent),
            critical_assets_count=1 if asset_id else 0,
            active_campaigns_count=1 if campaign_id else 0,
            open_incidents_count=0,
            tenant_id=tenant_id,
        )

        return {
            "event": event,
            "correlation": corr,
            "cluster": cluster,
            "situation": sit,
            "posture": pos,
        }
