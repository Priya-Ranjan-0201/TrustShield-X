"""
TruthShield X — Multi-Source Corroboration & Conflict Engine (Phase 33).

Evaluates source independence, detects syndicated/duplicated feed amplification,
and preserves intelligence conflicts without forced or premature resolution.
"""

from typing import Dict, List, Any, Optional
from datetime import datetime, timezone
import hashlib
from app.schemas.threat_intelligence_fusion_models import IntelligenceConflictDTO


class MultiSourceCorroborationEngine:
    """Calculates independent corroboration and manages intelligence contradictions."""

    def __init__(self):
        self._conflicts: Dict[str, IntelligenceConflictDTO] = {}
        self._seed_default_conflicts()

    def _seed_default_conflicts(self):
        conf = IntelligenceConflictDTO(
            conflict_id="conf_ip_attribution_01",
            indicator_or_entity="198.51.100.42",
            claim_a="Attributed to Ember Bear APT-88",
            source_a="src_commercial_threat_feed",
            claim_b="Attributed to GhostViper Syndicate",
            source_b="src_open_threat_exchange",
            status="INTELLIGENCE_CONFLICT",
            resolution_notes="Preserving both claims pending network PCAP confirmation.",
        )
        self._conflicts[conf.conflict_id] = conf

    def calculate_corroboration(
        self,
        claims: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """
        Evaluates source independence and detects syndicated copies.
        Claims having identical raw text/hashes from distinct feeds are marked as syndicated.
        """
        if not claims:
            return {"independent_source_count": 0, "corroboration_confidence": 0.0, "is_syndicated": False}

        unique_payload_hashes = set()
        independent_sources = set()

        for c in claims:
            source_id = c.get("source_id", "unknown_source")
            content = c.get("content", "")
            h = hashlib.sha256(content.strip().encode("utf-8")).hexdigest()

            unique_payload_hashes.add(h)
            independent_sources.add(source_id)

        # If multiple feeds report the exact same text hash, it's syndicated reporting
        is_syndicated = len(claims) > 1 and len(unique_payload_hashes) == 1
        effective_independent_sources = 1 if is_syndicated else len(independent_sources)

        # Non-linear confidence scaling
        confidence = min(0.99, 0.60 + (effective_independent_sources * 0.12))

        return {
            "total_reports_received": len(claims),
            "effective_independent_sources": effective_independent_sources,
            "is_syndicated_reproduction": is_syndicated,
            "corroboration_confidence": round(confidence, 2),
            "assessment": "INDEPENDENT_CORROBORATION" if not is_syndicated and effective_independent_sources > 1 else "SINGLE_OR_SYNDICATED_SOURCE",
        }

    def register_conflict(
        self,
        indicator_or_entity: str,
        claim_a: str,
        source_a: str,
        claim_b: str,
        source_b: str,
    ) -> IntelligenceConflictDTO:
        conflict_id = f"conf_{hashlib.md5(f'{indicator_or_entity}:{source_a}:{source_b}'.encode()).hexdigest()[:8]}"
        dto = IntelligenceConflictDTO(
            conflict_id=conflict_id,
            indicator_or_entity=indicator_or_entity,
            claim_a=claim_a,
            source_a=source_a,
            claim_b=claim_b,
            source_b=source_b,
            status="INTELLIGENCE_CONFLICT",
            resolution_notes="Preserved both claims. Conflict resolution requires empirical verification.",
        )
        self._conflicts[conflict_id] = dto
        return dto

    def list_conflicts(self) -> List[IntelligenceConflictDTO]:
        return list(self._conflicts.values())
