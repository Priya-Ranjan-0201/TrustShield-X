"""
TruthShield X — Canonical Security Event Normalization & Ingestion Service
"""

import hashlib
import json
import uuid
from typing import Dict, List, Optional, Any
from datetime import datetime, timezone
from app.schemas.fusion_models import SecurityEventDTO, SecurityEventTypeLiteral


class EventNormalizationService:
    """Normalizes multi-modal security events, enforces deterministic deduplication, and preserves timeline ordering."""

    def __init__(self):
        # tenant_id -> event_id -> SecurityEventDTO
        self._events: Dict[str, Dict[str, SecurityEventDTO]] = {}
        # tenant_id -> content_fingerprint -> event_id
        self._fingerprints: Dict[str, Dict[str, str]] = {}
        # tenant_id -> List[SecurityEventDTO] (chronologically sorted)
        self._event_stream: Dict[str, List[SecurityEventDTO]] = {}

    @staticmethod
    def compute_content_fingerprint(
        event_type: str,
        source: str,
        entity_id: Optional[str],
        asset_id: Optional[str],
        provenance: Dict[str, Any],
    ) -> str:
        """Generates deterministic fingerprint to deduplicate redundant telemetry."""
        payload = f"{event_type}:{source}:{entity_id or ''}:{asset_id or ''}:{json.dumps(provenance, sort_keys=True)}"
        return hashlib.sha256(payload.encode()).hexdigest()

    def ingest_and_normalize(
        self,
        event_type: SecurityEventTypeLiteral,
        source: str,
        entity_id: Optional[str] = None,
        asset_id: Optional[str] = None,
        campaign_id: Optional[str] = None,
        incident_id: Optional[str] = None,
        severity: str = "MEDIUM",
        confidence: float = 0.90,
        risk_score: float = 20.0,
        trust_score: float = 80.0,
        exposure_score: float = 20.0,
        observed_at: Optional[str] = None,
        provenance: Optional[Dict[str, Any]] = None,
        tenant_id: str = "default_tenant",
        classification: str = "INTERNAL",
        source_event_id: Optional[str] = None,
    ) -> SecurityEventDTO:
        """Ingests, normalizes, and deterministically deduplicates a security event."""
        if tenant_id not in self._events:
            self._events[tenant_id] = {}
            self._fingerprints[tenant_id] = {}
            self._event_stream[tenant_id] = []

        prov = provenance or {}
        fp = self.compute_content_fingerprint(event_type, source, entity_id, asset_id, prov)

        # Deduplication check within tenant space
        if fp in self._fingerprints[tenant_id]:
            existing_id = self._fingerprints[tenant_id][fp]
            return self._events[tenant_id][existing_id]

        event_id = f"sev_{uuid.uuid4().hex[:12]}"
        now_iso = datetime.now(timezone.utc).isoformat()
        obs_time = observed_at or now_iso

        event = SecurityEventDTO(
            event_id=event_id,
            event_type=event_type,
            tenant_id=tenant_id,
            source=source,
            source_event_id=source_event_id,
            asset_id=asset_id,
            entity_id=entity_id,
            campaign_id=campaign_id,
            incident_id=incident_id,
            severity=severity.upper(),
            confidence=max(0.0, min(1.0, confidence)),
            risk_score=max(0.0, min(100.0, risk_score)),
            trust_score=max(0.0, min(100.0, trust_score)),
            exposure_score=max(0.0, min(100.0, exposure_score)),
            timestamp=now_iso,
            observed_at=obs_time,
            ingested_at=now_iso,
            provenance=prov,
            classification=classification,
            status="PROCESSED",
            content_fingerprint=fp,
        )

        self._events[tenant_id][event_id] = event
        self._fingerprints[tenant_id][fp] = event_id
        self._event_stream[tenant_id].append(event)

        # Maintain timeline ordering by observed_at
        self._event_stream[tenant_id].sort(key=lambda e: e.observed_at)
        return event

    def get_event(self, event_id: str, tenant_id: str = "default_tenant") -> Optional[SecurityEventDTO]:
        """Retrieves a single security event."""
        return self._events.get(tenant_id, {}).get(event_id)

    def list_events(
        self,
        event_type: Optional[SecurityEventTypeLiteral] = None,
        severity: Optional[str] = None,
        entity_id: Optional[str] = None,
        asset_id: Optional[str] = None,
        tenant_id: str = "default_tenant",
        limit: int = 100,
    ) -> List[SecurityEventDTO]:
        """Lists events in chronological observation order."""
        stream = self._event_stream.get(tenant_id, [])
        results = []
        for ev in stream:
            if event_type and ev.event_type != event_type:
                continue
            if severity and ev.severity != severity:
                continue
            if entity_id and ev.entity_id != entity_id:
                continue
            if asset_id and ev.asset_id != asset_id:
                continue
            results.append(ev)
            if len(results) >= limit:
                break
        return results
