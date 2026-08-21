"""Deterministic Threat Intelligence Summary Generator (Phase 3.9 Part 1A.23).

Generates factual, evidence-backed natural language summaries of threat matches.
No LLM hallucination, no premature malware classification.
"""

from typing import List
from app.schemas.threat_intelligence_models import ThreatMatchDTO, ThreatSummaryDTO


class ThreatIntelligenceSummaryGenerator:
    """Generates deterministic factual summaries from threat matches."""

    def generate_summaries(self, matches: List[ThreatMatchDTO]) -> List[ThreatSummaryDTO]:
        summaries: List[ThreatSummaryDTO] = []

        if not matches:
            summaries.append(
                ThreatSummaryDTO(
                    title="No External Threat Intelligence Matches",
                    summary_text="Statically observed application indicators do not match any known external threat intelligence indicators.",
                    matches_count=0,
                )
            )
            return summaries

        for m in matches:
            summaries.append(
                ThreatSummaryDTO(
                    title=f"Threat Match: {m.match_type}",
                    summary_text=f"Indicator matched external threat intelligence record (Type: {m.match_type}, Reputation: {m.reputation}, Freshness: {m.freshness_state}).",
                    matches_count=1,
                )
            )

        return summaries
