"""
TruthShield X — Intelligence Normalization Engine (Phase 22).

Normalizes multi-format intelligence feeds (STIX 2.1, TAXII, MISP JSON, CSV) into standardized objects.
"""

from typing import Dict, Any, Optional
import hashlib
from datetime import datetime, timezone
from app.schemas.threat_intelligence_fabric_models import ThreatIntelligenceObjectDTO


class IntelligenceNormalizationEngine:
    """Normalizes heterogeneous external threat data into canonical ThreatIntelligenceObjectDTOs."""

    def normalize(
        self,
        raw_data: Dict[str, Any],
        source_id: str,
        tenant_id: str = "default_tenant",
        feed_format: str = "STIX2",
    ) -> ThreatIntelligenceObjectDTO:
        # Extract object type and value based on format
        obj_type = "INDICATOR"
        val = raw_data.get("value", "")
        confidence = float(raw_data.get("confidence", 0.85))

        if feed_format == "STIX2":
            stix_type = raw_data.get("type", "indicator")
            if stix_type == "ipv4-addr":
                obj_type = "IP"
                val = raw_data.get("value", "")
            elif stix_type == "domain-name":
                obj_type = "DOMAIN"
                val = raw_data.get("value", "")
            elif stix_type == "url":
                obj_type = "URL"
                val = raw_data.get("value", "")
            elif stix_type == "attack-pattern":
                obj_type = "TECHNIQUE"
                val = raw_data.get("name", "")
            elif stix_type == "threat-actor":
                obj_type = "ACTOR"
                val = raw_data.get("name", "")
            elif stix_type == "malware":
                obj_type = "MALWARE"
                val = raw_data.get("name", "")
            elif stix_type == "vulnerability":
                obj_type = "VULNERABILITY"
                val = raw_data.get("name", "")
            else:
                obj_type = "INDICATOR"
                val = raw_data.get("pattern", raw_data.get("value", "stix_pattern"))
        elif feed_format == "MISP_JSON":
            misp_type = raw_data.get("type", "ip-dst")
            val = raw_data.get("value", "")
            if "ip" in misp_type:
                obj_type = "IP"
            elif "domain" in misp_type or "hostname" in misp_type:
                obj_type = "DOMAIN"
            elif "url" in misp_type:
                obj_type = "URL"
            elif "md5" in misp_type or "sha256" in misp_type:
                obj_type = "HASH"
            else:
                obj_type = "INDICATOR"
        else:
            val = raw_data.get("value", raw_data.get("indicator", "unknown_val"))
            obj_type = raw_data.get("type", "INDICATOR")

        # Canonical normalization (lowercase strip, defang neutralization)
        canonical = val.lower().strip().replace("[.]", ".").replace("hxxp://", "http://").replace("hxxps://", "https://")
        content_hash = hashlib.sha256(canonical.encode("utf-8")).hexdigest()

        return ThreatIntelligenceObjectDTO(
            tenant_id=tenant_id,
            object_type=obj_type,  # type: ignore
            value=val,
            canonical_value=canonical,
            source_id=source_id,
            confidence=min(max(confidence, 0.0), 1.0),
            status="ACTIVE",
            classification="COMMUNITY",
            content_hash=f"sha256_{content_hash}",
            version=1,
        )
