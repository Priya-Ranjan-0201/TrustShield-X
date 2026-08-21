"""Structured Threat Evidence Card Generator (Phase 3.9 Part 1A.23).

Generates structured cards for UI rendering of threat matches.
"""

from typing import List
from app.schemas.threat_intelligence_models import ThreatMatchDTO, ThreatCardDTO


class ThreatEvidenceGenerator:
    """Generates structured UI evidence cards from threat matches."""

    def generate_cards(self, matches: List[ThreatMatchDTO]) -> List[ThreatCardDTO]:
        cards: List[ThreatCardDTO] = []

        for idx, m in enumerate(matches):
            cards.append(
                ThreatCardDTO(
                    card_id=f"card_{idx + 1}",
                    title=m.match_type,
                    category="THREAT_MATCH",
                    observed_indicator=m.indicator_id,
                    threat_claim=m.reputation,
                    confidence=m.confidence,
                    freshness=m.freshness_state,
                )
            )

        if not cards:
            cards.append(
                ThreatCardDTO(
                    card_id="card_default",
                    title="NO_THREAT_MATCH",
                    category="CLEAN_INDICATORS",
                    observed_indicator="N/A",
                    threat_claim="NO_MATCH",
                    confidence="HIGH",
                    freshness="CURRENT",
                )
            )

        return cards
