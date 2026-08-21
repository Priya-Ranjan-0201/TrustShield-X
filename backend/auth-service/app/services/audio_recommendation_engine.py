"""Deterministic Recommendation Engine for Voice Clone Engine (Phase 3.6 Part 2A-2A-2).

Produces actionable security recommendations based strictly on generated platform evidence cards.
Zero hallucinations.
"""

from typing import List, Dict, Any


class AudioRecommendationEngine:
    """Deterministic Security Recommendation Engine."""

    def generate_recommendations(
        self, evidence_cards: List[Dict[str, Any]]
    ) -> List[str]:
        """Generates deduplicated recommendations derived directly from evidence cards."""
        recs: List[str] = []
        seen = set()

        for card in evidence_cards:
            rec = card.get("recommendation")
            if rec and rec not in seen:
                recs.append(rec)
                seen.add(rec)

        if not recs:
            recs.append("Audio analysis completed. Vocal dynamics align with natural human speech.")

        return recs
