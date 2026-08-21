"""Structured Behavioral Evidence Card Generator (Phase 3.9 Part 1A.22).

Generates structured cards for UI rendering of correlated application behaviors.
"""

from typing import List
from app.schemas.behavioral_correlation_models import BehaviorFindingDTO, BehaviorCardDTO


class BehavioralEvidenceGenerator:
    """Generates structured UI evidence cards from findings."""

    def generate_cards(self, findings: List[BehaviorFindingDTO]) -> List[BehaviorCardDTO]:
        cards: List[BehaviorCardDTO] = []

        for idx, finding in enumerate(findings):
            cards.append(
                BehaviorCardDTO(
                    card_id=f"card_{idx + 1}",
                    title=finding.finding_type,
                    category=finding.category,
                    description=finding.summary,
                    confidence=finding.confidence,
                    resolution_status=finding.resolution_status,
                )
            )

        if not cards:
            cards.append(
                BehaviorCardDTO(
                    card_id="card_default",
                    title="STANDARD_BEHAVIOR",
                    category="DATA_COLLECTION",
                    description="Standard application functionality with declared permission usage.",
                    confidence="HIGH",
                    resolution_status="RESOLVED",
                )
            )

        return cards
