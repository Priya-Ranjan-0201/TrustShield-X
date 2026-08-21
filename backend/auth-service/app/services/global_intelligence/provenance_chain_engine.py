"""
TruthShield X — Provenance Chain Engine (Phase 27).

Maintains cryptographic audit links across ingestion, transformation, enrichment, and correlation lifecycles.
"""

from typing import Dict, List, Any
from datetime import datetime, timezone
import hashlib
import json


class ProvenanceChainEngine:
    """Attaches and verifies cryptographic provenance for intelligence objects."""

    def attach_provenance(
        self,
        existing_chain: List[Dict[str, Any]],
        stage: str,
        actor_or_service: str,
        details: Dict[str, Any],
    ) -> List[Dict[str, Any]]:
        prev_hash = existing_chain[-1]["stage_hash"] if existing_chain else "GENESIS_PROVENANCE_HASH"
        entry_payload = {
            "stage": stage,
            "actor_or_service": actor_or_service,
            "details": details,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "prev_hash": prev_hash,
        }
        stage_hash = hashlib.sha256(json.dumps(entry_payload, sort_keys=True).encode()).hexdigest()
        new_entry = {**entry_payload, "stage_hash": stage_hash}
        return [*existing_chain, new_entry]

    def verify_provenance(self, provenance_chain: List[Dict[str, Any]]) -> bool:
        if not provenance_chain:
            return True
        for i in range(1, len(provenance_chain)):
            if provenance_chain[i]["prev_hash"] != provenance_chain[i - 1]["stage_hash"]:
                return False
        return True
