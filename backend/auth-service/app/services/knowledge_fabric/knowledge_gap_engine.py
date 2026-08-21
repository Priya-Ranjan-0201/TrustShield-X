"""
TruthShield X — Knowledge Gap Engine (Phase 19).

Identifies security blind spots: missing asset ownership, unknown dependencies, missing evidence, unknown control statuses.
"""

from typing import Dict, List, Optional
from app.schemas.cyber_knowledge_fabric_models import KnowledgeGapDTO


class KnowledgeGapEngine:
    """Manages knowledge gap detection and risk prioritization."""

    def __init__(self):
        self._gaps: Dict[str, KnowledgeGapDTO] = {}
        self._initialize_default_gaps()

    def _initialize_default_gaps(self):
        g1 = KnowledgeGapDTO(
            gap_id="gap_db_owner",
            gap_type="MISSING_ASSET_OWNERSHIP",
            target_entity="db_primary_users",
            description="Database instance db_primary_users does not have an assigned DevOps team owner.",
            security_impact="HIGH",
            decision_impact=0.85,
            uncertainty=0.90,
            priority="HIGH",
        )
        self._gaps[g1.gap_id] = g1

    def record_gap(
        self,
        gap_type: str,
        target_entity: str,
        description: str,
        security_impact: str = "HIGH",
        decision_impact: float = 0.85,
        uncertainty: float = 0.90,
        priority: str = "HIGH",
    ) -> KnowledgeGapDTO:
        gap = KnowledgeGapDTO(
            gap_type=gap_type,  # type: ignore
            target_entity=target_entity,
            description=description,
            security_impact=security_impact,  # type: ignore
            decision_impact=decision_impact,
            uncertainty=uncertainty,
            priority=priority,  # type: ignore
        )
        self._gaps[gap.gap_id] = gap
        return gap

    def list_gaps(self) -> List[KnowledgeGapDTO]:
        return list(self._gaps.values())
