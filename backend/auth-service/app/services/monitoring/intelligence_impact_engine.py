"""Intelligence Impact Evaluation Engine (Phase 4.0 Part 6 — Sections 28-29).

Evaluates whether incoming intelligence updates materially affect existing entities,
findings, campaigns, attack chains, cases, or reports.
"""

from typing import List, Dict, Any, Optional
from app.schemas.continuous_intelligence_models import (
    IntelligenceChangeEventDTO,
    ImpactLevelLiteral,
)


class ImpactDecision:
    """Detailed impact evaluation result."""

    def __init__(
        self,
        impact_level: ImpactLevelLiteral,
        what_changed: str,
        affected_objects: List[str],
        why_relevant: str,
        supporting_evidence: List[str],
        recommended_action: str,
    ):
        self.impact_level = impact_level
        self.what_changed = what_changed
        self.affected_objects = affected_objects
        self.why_relevant = why_relevant
        self.supporting_evidence = supporting_evidence
        self.recommended_action = recommended_action

    def to_dict(self) -> Dict[str, Any]:
        return {
            "impact_level": self.impact_level,
            "what_changed": self.what_changed,
            "affected_objects": self.affected_objects,
            "why_relevant": self.why_relevant,
            "supporting_evidence": self.supporting_evidence,
            "recommended_action": self.recommended_action,
        }


class IntelligenceImpactEngine:
    """Assesses change events and calculates exact impact levels without mutating historical records."""

    @staticmethod
    def evaluate_impact(
        change_event: IntelligenceChangeEventDTO,
        monitored_entity_ids: List[str],
        active_case_entity_ids: Optional[List[str]] = None,
    ) -> ImpactDecision:
        active_case_set = set(active_case_entity_ids or [])
        is_monitored = change_event.entity_id in monitored_entity_ids
        is_in_active_case = change_event.entity_id in active_case_set

        if not is_monitored:
            return ImpactDecision(
                impact_level="NO_IMPACT",
                what_changed=f"Indicator {change_event.entity_id} observed ({change_event.new_state})",
                affected_objects=[],
                why_relevant="Indicator is not associated with any active TruthShield X entity or case.",
                supporting_evidence=[change_event.provenance],
                recommended_action="Store observation in baseline store without triggering alert.",
            )

        # Monitored indicator matched
        if change_event.new_state == "MALICIOUS" and change_event.previous_state != "MALICIOUS":
            # Reclassified to MALICIOUS
            level: ImpactLevelLiteral = "CRITICAL_IMPACT" if is_in_active_case else "HIGH_IMPACT"
            return ImpactDecision(
                impact_level=level,
                what_changed=f"Monitored entity {change_event.entity_id} reclassified from {change_event.previous_state} to MALICIOUS.",
                affected_objects=[change_event.entity_id],
                why_relevant="Entity is actively monitored in trust inventory. Reclassification materially increases compromise risk.",
                supporting_evidence=[change_event.provenance],
                recommended_action="Generate high-priority security alert and trigger targeted report reassessment.",
            )

        if change_event.event_type == "IOC_REVOKED":
            return ImpactDecision(
                impact_level="LOW_IMPACT",
                what_changed=f"Threat indicator for {change_event.entity_id} was revoked by feed provider.",
                affected_objects=[change_event.entity_id],
                why_relevant="Threat signal is no longer active according to feed maintainer.",
                supporting_evidence=[change_event.provenance],
                recommended_action="Update indicator status to REVOKED. Preserve historical evidence.",
            )

        return ImpactDecision(
            impact_level="MEDIUM_IMPACT",
            what_changed=f"Intelligence update for monitored entity {change_event.entity_id}.",
            affected_objects=[change_event.entity_id],
            why_relevant="Corroborating intelligence received for active entity.",
            supporting_evidence=[change_event.provenance],
            recommended_action="Update graph observation and review alert queue.",
        )
