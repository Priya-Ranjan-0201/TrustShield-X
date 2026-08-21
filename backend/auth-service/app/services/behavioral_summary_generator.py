"""Deterministic Behavioral Summary Generator (Phase 3.9 Part 1A.22).

Generates factual, evidence-backed natural language summaries of correlated application behaviors.
No LLM hallucination, no unsupported intent claims.
"""

from typing import List
from app.schemas.behavioral_correlation_models import BehaviorFindingDTO, BehaviorSummaryDTO


class BehavioralSummaryGenerator:
    """Generates deterministic factual summaries from findings."""

    def generate_summaries(self, findings: List[BehaviorFindingDTO]) -> List[BehaviorSummaryDTO]:
        summaries: List[BehaviorSummaryDTO] = []

        if not findings:
            summaries.append(
                BehaviorSummaryDTO(
                    title="Standard Application Behavior",
                    summary_text="No multi-stage complex sensitive data behavior chains detected statically.",
                    findings_count=0,
                )
            )
            return summaries

        for finding in findings:
            summaries.append(
                BehaviorSummaryDTO(
                    title=f"Behavioral Finding: {finding.finding_type}",
                    summary_text=finding.summary,
                    findings_count=1,
                )
            )

        return summaries
