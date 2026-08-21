"""
TruthShield X — Intelligence Source Manager & Feed Health Engine (Phase 27).

Manages intelligence sources, monitors feed reliability, detects feed poisoning, and enforces quarantine.
"""

from typing import Dict, List, Optional, Any
from datetime import datetime, timezone
from app.schemas.global_intelligence_models import IntelligenceSourceDTO, SourceTypeLiteral


class IntelligenceSourceManager:
    """Manages intelligence source registrations, health tracking, and poisoning defenses."""

    def __init__(self):
        self._sources: Dict[str, IntelligenceSourceDTO] = {}
        self._feed_health: Dict[str, Dict[str, Any]] = {}
        self._quarantined_items: List[Dict[str, Any]] = []
        self._seed_default_sources()

    def _seed_default_sources(self):
        s1 = IntelligenceSourceDTO(
            source_id="src_global_exchange",
            name="Global Cyber Threat Exchange Feed",
            type="COMMERCIAL",
            source_reliability=0.95,
            information_reliability=0.92,
            freshness_status="FRESH",
            trust_level="HIGH",
            status="ACTIVE",
        )
        self._sources[s1.source_id] = s1
        self._feed_health[s1.source_id] = {
            "last_successful_ingest": datetime.now(timezone.utc).isoformat(),
            "items_ingested": 1420,
            "error_count": 0,
            "duplicate_count": 12,
            "poisoning_alerts": 0,
        }

    def register_source(
        self,
        name: str,
        source_type: SourceTypeLiteral,
        source_reliability: float = 0.90,
        information_reliability: float = 0.88,
        tenant_scope: str = "default_tenant",
    ) -> IntelligenceSourceDTO:
        dto = IntelligenceSourceDTO(
            name=name,
            type=source_type,
            source_reliability=source_reliability,
            information_reliability=information_reliability,
            freshness_status="FRESH",
            trust_level="HIGH" if source_reliability >= 0.85 else "MEDIUM",
            tenant_scope=tenant_scope,
            status="ACTIVE",
        )
        self._sources[dto.source_id] = dto
        self._feed_health[dto.source_id] = {
            "last_successful_ingest": datetime.now(timezone.utc).isoformat(),
            "items_ingested": 0,
            "error_count": 0,
            "duplicate_count": 0,
            "poisoning_alerts": 0,
        }
        return dto

    def quarantine_malformed_feed(self, source_id: str, reason: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        record = {
            "source_id": source_id,
            "reason": reason,
            "payload": payload,
            "quarantined_at": datetime.now(timezone.utc).isoformat(),
        }
        self._quarantined_items.append(record)
        if source_id in self._feed_health:
            self._feed_health[source_id]["poisoning_alerts"] += 1
        return record

    def get_source(self, source_id: str) -> Optional[IntelligenceSourceDTO]:
        return self._sources.get(source_id)

    def list_sources(self, tenant_scope: str = "default_tenant") -> List[IntelligenceSourceDTO]:
        return [s for s in self._sources.values() if s.tenant_scope == tenant_scope or s.tenant_scope == "default_tenant"]

    def get_feed_health(self, source_id: str) -> Dict[str, Any]:
        return self._feed_health.get(source_id, {"status": "UNKNOWN"})
