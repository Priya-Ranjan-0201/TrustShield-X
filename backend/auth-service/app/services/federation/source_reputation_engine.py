"""
TruthShield X — Threat Intelligence Source Reputation & Feed Registry Engine
"""

from typing import Dict, List, Optional, Any
from datetime import datetime, timezone
from app.schemas.federation_models import IntelligenceSourceReputationDTO


class SourceReputationEngine:
    """Maintains threat intelligence feed registrations, parses STIX/TAXII formats, and tracks historical source reliability."""

    def __init__(self):
        # source_id -> IntelligenceSourceReputationDTO
        self._sources: Dict[str, IntelligenceSourceReputationDTO] = {
            "src_internal_soc": IntelligenceSourceReputationDTO(
                source_id="src_internal_soc",
                source_name="TruthShield Internal SOC & Telemetry",
                source_type="INTERNAL",
                reliability_score=0.98,
                total_indicators_submitted=450,
                verified_indicators_count=442,
                false_positives_count=3,
                revoked_count=2,
                conflicts_count=3,
                status="ACTIVE",
            ),
            "src_stix_taxii_partner": IntelligenceSourceReputationDTO(
                source_id="src_stix_taxii_partner",
                source_name="FS-ISAC STIX/TAXII 2.1 Feed",
                source_type="STIX_TAXII",
                reliability_score=0.92,
                total_indicators_submitted=1200,
                verified_indicators_count=1100,
                false_positives_count=18,
                revoked_count=10,
                conflicts_count=12,
                status="ACTIVE",
            ),
        }

    def register_feed(
        self,
        source_id: str,
        source_name: str,
        source_type: str = "PARTNER",
        initial_reliability: float = 0.80,
    ) -> IntelligenceSourceReputationDTO:
        """Registers a new threat feed source."""
        src = IntelligenceSourceReputationDTO(
            source_id=source_id,
            source_name=source_name,
            source_type=source_type,
            reliability_score=initial_reliability,
            status="ACTIVE",
        )
        self._sources[source_id] = src
        return src

    def record_feedback_outcome(
        self,
        source_id: str,
        is_verified: bool = False,
        is_false_positive: bool = False,
        is_revocation: bool = False,
    ) -> IntelligenceSourceReputationDTO:
        """Dynamically recalibrates source reliability based on operational outcomes."""
        src = self._sources.get(source_id)
        if not src:
            raise KeyError(f"Source '{source_id}' not found in feed registry.")

        src.total_indicators_submitted += 1
        if is_verified:
            src.verified_indicators_count += 1
        if is_false_positive:
            src.false_positives_count += 1
        if is_revocation:
            src.revoked_count += 1

        # Mathematical calibration
        total = src.total_indicators_submitted
        if total > 0:
            penalty = (src.false_positives_count * 2.5 + src.revoked_count * 3.0) / total
            calc_rel = max(0.20, min(0.99, (src.verified_indicators_count / total) - penalty))
            src.reliability_score = round(calc_rel, 3)

        if src.reliability_score < 0.40:
            src.status = "DEGRADED"

        src.last_sync = datetime.now(timezone.utc).isoformat()
        return src

    def parse_stix_taxii_indicator(self, stix_json: Dict[str, Any]) -> Dict[str, Any]:
        """Parses STIX 2.1 indicator objects safely into normalized format."""
        indicator_value = stix_json.get("pattern", "")
        # Extract basic pattern e.g. [domain-name:value = 'malicious.com']
        parsed_type = "DOMAIN"
        if "url:value" in indicator_value:
            parsed_type = "URL"
        elif "ipv4-addr:value" in indicator_value:
            parsed_type = "IP"
        elif "file:hashes" in indicator_value:
            parsed_type = "HASH"

        return {
            "intelligence_type": parsed_type,
            "raw_pattern": indicator_value,
            "confidence": float(stix_json.get("confidence", 80)) / 100.0,
            "stix_id": stix_json.get("id"),
        }

    def list_sources(self) -> List[IntelligenceSourceReputationDTO]:
        """Lists all registered threat feed sources."""
        return list(self._sources.values())
