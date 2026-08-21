"""
TruthShield X — Intelligence Source Registry (Phase 33).

Manages intelligence sources, tracks separate dimensions of source reliability,
information credibility, freshness, and approval status, with support for source quarantine.
"""

from typing import Dict, List, Any, Optional
from datetime import datetime, timezone
from app.schemas.threat_intelligence_fusion_models import IntelligenceSourceDTO


class IntelligenceSourceRegistry:
    """Manages threat intelligence source registrations, health, credentials, and trustworthiness."""

    def __init__(self):
        self._sources: Dict[str, IntelligenceSourceDTO] = {}
        self._seed_default_sources()

    def _seed_default_sources(self):
        gov_source = IntelligenceSourceDTO(
            source_id="src_cert_in_advisory",
            source_name="CERT-In National Threat Advisory",
            source_type="GOVERNMENT",
            provider="CERT-In",
            reliability="A",
            collection_method="API",
            authentication="API_KEY",
            last_success=datetime.now(timezone.utc).isoformat(),
            freshness="FRESH",
            supported_formats=["JSON", "STIX2.1"],
            classification="PUBLIC",
            approval_status="APPROVED",
            is_compromised=False,
        )
        isac_source = IntelligenceSourceDTO(
            source_id="src_fs_isac_feed",
            source_name="Financial Services ISAC Live Stream",
            source_type="ISAC",
            provider="FS-ISAC",
            reliability="A",
            collection_method="TAXII",
            authentication="MUTUAL_TLS",
            last_success=datetime.now(timezone.utc).isoformat(),
            freshness="FRESH",
            supported_formats=["STIX2.1"],
            classification="RESTRICTED",
            approval_status="APPROVED",
            is_compromised=False,
        )
        vendor_source = IntelligenceSourceDTO(
            source_id="src_commercial_threat_feed",
            source_name="Commercial High-Fidelity Cyber Feed",
            source_type="COMMERCIAL",
            provider="GlobalSec Intelligence",
            reliability="B",
            collection_method="STIX",
            authentication="OAUTH2",
            last_success=datetime.now(timezone.utc).isoformat(),
            freshness="FRESH",
            supported_formats=["STIX2.1", "JSON"],
            classification="CONFIDENTIAL",
            approval_status="APPROVED",
            is_compromised=False,
        )
        self._sources[gov_source.source_id] = gov_source
        self._sources[isac_source.source_id] = isac_source
        self._sources[vendor_source.source_id] = vendor_source

    def register_source(self, source: IntelligenceSourceDTO) -> IntelligenceSourceDTO:
        self._sources[source.source_id] = source
        return source

    def get_source(self, source_id: str) -> Optional[IntelligenceSourceDTO]:
        return self._sources.get(source_id)

    def list_sources(self, approval_status: Optional[str] = None) -> List[IntelligenceSourceDTO]:
        sources = list(self._sources.values())
        if approval_status:
            sources = [s for s in sources if s.approval_status == approval_status]
        return sources

    def quarantine_source(self, source_id: str, reason: str) -> Dict[str, Any]:
        source = self._sources.get(source_id)
        if not source:
            return {"status": "NOT_FOUND", "source_id": source_id}
        source.approval_status = "QUARANTINED"
        source.is_compromised = True
        return {
            "status": "SOURCE_QUARANTINED",
            "source_id": source_id,
            "reason": reason,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    def evaluate_source_scoring(self, source_id: str) -> Dict[str, Any]:
        source = self._sources.get(source_id)
        if not source:
            return {"status": "NOT_FOUND"}
        return {
            "source_id": source_id,
            "source_reliability": source.reliability,
            "freshness": source.freshness,
            "approval_status": source.approval_status,
            "is_compromised": source.is_compromised,
        }
