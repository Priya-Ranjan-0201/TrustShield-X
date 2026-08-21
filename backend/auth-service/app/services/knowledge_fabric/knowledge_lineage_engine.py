"""
TruthShield X — Knowledge Lineage Engine (Phase 19).

Constructs complete provenance chains for security conclusions answering:
- What created this?
- What data was used?
- What evidence supported it?
- What transformations occurred?
- What models were used?
- What other conclusions depend on it?
"""

from typing import Dict, List, Optional
from app.schemas.cyber_knowledge_fabric_models import KnowledgeLineageDTO


class KnowledgeLineageEngine:
    """Manages knowledge lineage and dependency trees."""

    def __init__(self):
        self._lineages: Dict[str, KnowledgeLineageDTO] = {}

    def record_lineage(
        self,
        conclusion_id: str,
        created_by_model: str,
        source_data: List[str],
        supporting_evidence: List[str],
        transformations: List[str],
        models_used: List[str],
        dependent_conclusions: Optional[List[str]] = None,
    ) -> KnowledgeLineageDTO:
        """Records the complete lineage of an assertion or conclusion."""
        lineage = KnowledgeLineageDTO(
            conclusion_id=conclusion_id,
            created_by_model=created_by_model,
            source_data=source_data,
            supporting_evidence=supporting_evidence,
            transformations=transformations,
            models_used=models_used,
            dependent_conclusions=dependent_conclusions or [],
        )
        self._lineages[conclusion_id] = lineage
        return lineage

    def get_lineage(self, conclusion_id: str) -> Optional[KnowledgeLineageDTO]:
        """Retrieves lineage metadata for a conclusion."""
        return self._lineages.get(conclusion_id)

    def add_dependent_conclusion(self, parent_conclusion_id: str, child_conclusion_id: str):
        """Appends a dependent child conclusion to the parent lineage."""
        lineage = self._lineages.get(parent_conclusion_id)
        if lineage:
            deps = list(lineage.dependent_conclusions)
            if child_conclusion_id not in deps:
                deps.append(child_conclusion_id)
                self._lineages[parent_conclusion_id] = KnowledgeLineageDTO(
                    conclusion_id=lineage.conclusion_id,
                    created_by_model=lineage.created_by_model,
                    source_data=lineage.source_data,
                    supporting_evidence=lineage.supporting_evidence,
                    transformations=lineage.transformations,
                    models_used=lineage.models_used,
                    dependent_conclusions=deps,
                )
