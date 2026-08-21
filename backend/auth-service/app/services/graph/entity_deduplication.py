"""Entity Deduplication Engine with Strict Merge Safety (Phase 4.0 Part 5 — Sections 41-42).

Deduplicates canonical entities based on cryptographic normalized values while strictly
preventing false merges for People, Organizations, Phone numbers, and Payment Identifiers.
"""

from typing import List, Dict, Optional
from app.schemas.intelligence_graph_models import (
    CanonicalEntityDTO,
    EntityObservationDTO,
)
from app.services.graph.entity_normalizer import EntityNormalizer


# Protected types that MUST NOT be merged based on fuzzy or probabilistic similarity (Section 42)
STRICT_MERGE_PROTECTED_TYPES = {
    "PERSON",
    "ORGANIZATION",
    "PHONE",
    "EMAIL",
    "ACCOUNT",
    "UPI_ID",
    "BANK_IDENTIFIER",
    "DOCUMENT",
    "IDENTITY_DOCUMENT",
}


class EntityDeduplicationEngine:
    """Canonical entity deduplicator enforcing strict merge safety policies."""

    @classmethod
    def can_merge(cls, entity_a: CanonicalEntityDTO, entity_b: CanonicalEntityDTO) -> bool:
        """Determines whether two entities can be safely merged into a single canonical entity."""
        if entity_a.entity_type != entity_b.entity_type:
            return False

        # If entity type is protected, require 100% exact normalized match
        if entity_a.entity_type in STRICT_MERGE_PROTECTED_TYPES:
            return entity_a.normalized_value == entity_b.normalized_value

        # For infrastructure (domains, hashes, certificates, packages, IPs)
        return entity_a.normalized_value == entity_b.normalized_value

    @classmethod
    def deduplicate_entities(
        cls, entities: List[CanonicalEntityDTO]
    ) -> List[CanonicalEntityDTO]:
        """Deduplicates a list of canonical entities while aggregating source counts and aliases."""
        unique_map: Dict[str, CanonicalEntityDTO] = {}

        for ent in entities:
            key = f"{ent.entity_type}:{ent.normalized_value}"
            if key not in unique_map:
                unique_map[key] = ent
            else:
                existing = unique_map[key]
                # Merge aliases and increment source count
                merged_aliases = list(set(existing.aliases + ent.aliases + [ent.display_value]))
                merged_count = existing.source_count + ent.source_count
                
                # Keep earliest first_seen and latest last_seen
                first_seen = min(existing.first_seen, ent.first_seen)
                last_seen = max(existing.last_seen, ent.last_seen)

                unique_map[key] = CanonicalEntityDTO(
                    entity_id=existing.entity_id,
                    entity_type=existing.entity_type,
                    canonical_value=existing.canonical_value,
                    display_value=existing.display_value,
                    normalized_value=existing.normalized_value,
                    value_hash=existing.value_hash,
                    source_count=merged_count,
                    first_seen=first_seen,
                    last_seen=last_seen,
                    confidence=existing.confidence,
                    resolution_status=existing.resolution_status,
                    privacy_classification=existing.privacy_classification,
                    organization_id=existing.organization_id,
                    aliases=merged_aliases,
                    metadata={**existing.metadata, **ent.metadata},
                    created_at=existing.created_at,
                    updated_at=last_seen,
                )

        return list(unique_map.values())
