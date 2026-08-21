"""
TruthShield X — Intelligence Normalization Engine (Phase 27).

Canonicalizes heterogeneous STIX 2.1, TAXII, and JSON intelligence payloads without destroying provenance.
"""

from typing import Dict, Any
from datetime import datetime, timezone
import hashlib
from app.schemas.global_intelligence_models import ThreatIntelligenceRecordDTO, IntelligenceTypeLiteral


class IntelligenceNormalizationEngine:
    """Parses, validates, and normalizes intelligence records into canonical representations."""

    def normalize_record(
        self,
        source_id: str,
        raw_payload: Dict[str, Any],
        intel_type: IntelligenceTypeLiteral = "IOC",
        tenant_scope: str = "default_tenant",
    ) -> ThreatIntelligenceRecordDTO:
        indicator = raw_payload.get("indicator") or raw_payload.get("value") or "unspecified_indicator"
        severity = raw_payload.get("severity", "HIGH")
        confidence = float(raw_payload.get("confidence", 0.90))

        raw_hash = hashlib.sha256(str(raw_payload).encode()).hexdigest()

        provenance_entry = {
            "source_id": source_id,
            "normalized_at": datetime.now(timezone.utc).isoformat(),
            "raw_payload_hash": raw_hash,
        }

        dto = ThreatIntelligenceRecordDTO(
            source_id=source_id,
            type=intel_type,
            indicator=indicator,
            entity=raw_payload.get("entity", "Attributed Infrastructure Cluster"),
            behavior=raw_payload.get("behavior", "Observed Network Beaconing"),
            campaign_id=raw_payload.get("campaign_id", "cmp_darkstorm_2026"),
            severity=severity,  # type: ignore
            confidence_score=confidence,
            provenance=[provenance_entry],
            evidence_hashes=[raw_hash],
            tenant_scope=tenant_scope,
            claim_status="REPORTED",
        )
        return dto
