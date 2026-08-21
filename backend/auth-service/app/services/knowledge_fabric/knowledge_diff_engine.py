"""
TruthShield X — Knowledge Diff Engine (Phase 19).

Computes diffs between versions of knowledge objects and relationships.
"""

from typing import Dict, Any, Optional
from app.schemas.cyber_knowledge_fabric_models import (
    KnowledgeObjectDTO,
    KnowledgeDiffDTO,
)


class KnowledgeDiffEngine:
    """Computes exact deltas across knowledge versions."""

    def compute_diff(self, old_obj: KnowledgeObjectDTO, new_obj: KnowledgeObjectDTO) -> KnowledgeDiffDTO:
        """Calculates differences between two versions of a knowledge object."""
        entity_changes: Dict[str, Any] = {}

        if old_obj.classification != new_obj.classification:
            entity_changes["classification"] = {"old": old_obj.classification, "new": new_obj.classification}
        if old_obj.status != new_obj.status:
            entity_changes["status"] = {"old": old_obj.status, "new": new_obj.status}

        confidence_delta = round(new_obj.confidence - old_obj.confidence, 4)

        return KnowledgeDiffDTO(
            object_id=new_obj.object_id,
            old_version=old_obj.version,
            new_version=new_obj.version,
            entity_changes=entity_changes,
            confidence_delta=confidence_delta,
            status_change=f"{old_obj.status} -> {new_obj.status}" if old_obj.status != new_obj.status else None,
        )
