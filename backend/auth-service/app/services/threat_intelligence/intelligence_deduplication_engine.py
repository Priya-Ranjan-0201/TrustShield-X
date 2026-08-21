"""
TruthShield X — Intelligence Deduplication Engine (Phase 22).

Detects duplicate intelligence objects across feeds while preserving multi-source provenance.
"""

from typing import Dict, List, Set, Any
from app.schemas.threat_intelligence_fabric_models import ThreatIntelligenceObjectDTO


class IntelligenceDeduplicationEngine:
    """Deduplicates intelligence objects by canonical hash while recording all contributing sources."""

    def __init__(self):
        self._hash_to_object_id: Dict[str, str] = {}
        self._provenance_map: Dict[str, Set[str]] = {}

    def process_object(self, obj: ThreatIntelligenceObjectDTO) -> Dict[str, Any]:
        """Returns whether the object is a duplicate and records provenance."""
        chash = obj.content_hash
        is_duplicate = False

        if chash in self._hash_to_object_id:
            is_duplicate = True
            canonical_id = self._hash_to_object_id[chash]
            self._provenance_map[canonical_id].add(obj.source_id)
        else:
            canonical_id = obj.object_id
            self._hash_to_object_id[chash] = canonical_id
            self._provenance_map[canonical_id] = {obj.source_id}

        return {
            "canonical_object_id": canonical_id,
            "is_duplicate": is_duplicate,
            "contributing_sources": list(self._provenance_map[canonical_id]),
        }
