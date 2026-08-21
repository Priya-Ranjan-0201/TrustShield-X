"""
TruthShield X — Intelligence Source Manager (Phase 22).

Manages external and internal threat intelligence sources across trust tiers and formats.
"""

from typing import Dict, List, Optional
from datetime import datetime, timezone
from app.schemas.threat_intelligence_fabric_models import IntelligenceSourceDTO, IntelligenceSourceTypeLiteral


class IntelligenceSourceManager:
    """Manages multi-source intelligence feeds with trust tracking."""

    def __init__(self):
        self._sources: Dict[str, IntelligenceSourceDTO] = {}
        self._seed_default_sources()

    def _seed_default_sources(self):
        defaults = [
            IntelligenceSourceDTO(
                source_id="src_misp_cve",
                tenant_id="default_tenant",
                name="Global MISP Threat Exchange",
                type="COMMUNITY",
                reliability="HIGH",
                trust_level=0.92,
                format="MISP_JSON",
                classification="COMMUNITY",
            ),
            IntelligenceSourceDTO(
                source_id="src_crowdstrike_falcon",
                tenant_id="default_tenant",
                name="CrowdStrike Falcon Adversary Feed",
                type="COMMERCIAL",
                reliability="VERY_HIGH",
                trust_level=0.98,
                format="STIX2",
                classification="PARTNER",
            ),
            IntelligenceSourceDTO(
                source_id="src_cisa_ais",
                tenant_id="default_tenant",
                name="CISA Automated Indicator Sharing",
                type="GOVERNMENT",
                reliability="VERY_HIGH",
                trust_level=0.95,
                format="TAXII2",
                classification="PUBLIC",
            ),
            IntelligenceSourceDTO(
                source_id="src_internal_soc",
                tenant_id="default_tenant",
                name="TruthShield Internal Incident Telemetry",
                type="INTERNAL",
                reliability="VERY_HIGH",
                trust_level=0.99,
                format="TELEMETRY",
                classification="TENANT_INTERNAL",
            ),
        ]
        for src in defaults:
            self._sources[src.source_id] = src

    def register_source(self, source: IntelligenceSourceDTO) -> IntelligenceSourceDTO:
        self._sources[source.source_id] = source
        return source

    def get_source(self, source_id: str) -> Optional[IntelligenceSourceDTO]:
        return self._sources.get(source_id)

    def list_sources(self, tenant_id: str = "default_tenant") -> List[IntelligenceSourceDTO]:
        return [
            s for s in self._sources.values()
            if s.tenant_id in (tenant_id, "default_tenant") or s.classification == "PUBLIC"
        ]
