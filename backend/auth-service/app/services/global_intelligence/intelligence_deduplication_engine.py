"""
TruthShield X — Intelligence Deduplication Engine (Phase 27).

Deduplicates identical or semantically equivalent records without losing independent source provenance.
"""

from typing import Dict, List, Any
from app.schemas.global_intelligence_models import ThreatIntelligenceRecordDTO


class IntelligenceDeduplicationEngine:
    """Combines corroborating intelligence observations while preserving source links."""

    def deduplicate_records(self, records: List[ThreatIntelligenceRecordDTO]) -> List[ThreatIntelligenceRecordDTO]:
        seen: Dict[str, ThreatIntelligenceRecordDTO] = {}
        for r in records:
            key = f"{r.type}:{r.indicator}"
            if key not in seen:
                seen[key] = r
            else:
                # Merge provenance
                existing = seen[key]
                merged_provenance = [*existing.provenance, *r.provenance]
                merged_hashes = list(set([*existing.evidence_hashes, *r.evidence_hashes]))
                updated = ThreatIntelligenceRecordDTO(
                    intelligence_id=existing.intelligence_id,
                    source_id=existing.source_id,
                    timestamp=existing.timestamp,
                    observed_at=existing.observed_at,
                    published_at=existing.published_at,
                    valid_from=existing.valid_from,
                    type=existing.type,
                    indicator=existing.indicator,
                    entity=existing.entity,
                    behavior=existing.behavior,
                    campaign_id=existing.campaign_id,
                    severity=existing.severity,
                    confidence_score=max(existing.confidence_score, r.confidence_score),
                    provenance=merged_provenance,
                    evidence_hashes=merged_hashes,
                    tenant_scope=existing.tenant_scope,
                    claim_status="CORRELATED",
                )
                seen[key] = updated
        return list(seen.values())
