"""Threat Intelligence Source Registry (Phase 3.9 Part 1A.23).

Manages configured threat intelligence sources, reliability ratings, sync metadata, and auth status.
"""

from typing import List, Dict, Any
from app.schemas.threat_intelligence_models import ThreatSourceDTO


class ThreatIntelligenceSourceRegistry:
    """Registry tracking registered threat intelligence sources and their reliability."""

    def __init__(self):
        self._sources: Dict[str, ThreatSourceDTO] = {
            "src_internal_db": ThreatSourceDTO(
                source_id="src_internal_db",
                provider="TruthShield Internal IOC Database",
                source_type="OFFLINE_DATABASE",
                reliability="VERY_HIGH",
                version="2026.1",
                status="ACTIVE",
            ),
            "src_open_feed": ThreatSourceDTO(
                source_id="src_open_feed",
                provider="Public OpenThreat Feed",
                source_type="OFFLINE_FEED",
                reliability="HIGH",
                version="1.4",
                status="ACTIVE",
            ),
        }

    def get_source(self, source_id: str) -> ThreatSourceDTO:
        return self._sources.get(
            source_id,
            ThreatSourceDTO(
                source_id=source_id,
                provider="Unknown Feed Provider",
                source_type="OFFLINE_FEED",
                reliability="MEDIUM",
                version="1.0",
                status="ACTIVE",
            ),
        )

    def list_sources(self) -> List[ThreatSourceDTO]:
        return list(self._sources.values())
