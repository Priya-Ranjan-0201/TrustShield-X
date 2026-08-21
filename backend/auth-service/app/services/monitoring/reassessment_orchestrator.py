"""Reassessment Orchestrator & Risk Versioning Engine (Phase 4.0 Part 6 — Sections 30-32, 73-74).

Executes targeted, policy-driven risk reassessments, creating immutable new versions
without modifying original analysis or report artifacts.
"""

from typing import List, Dict, Any, Optional, Tuple
import uuid
from datetime import datetime, timezone
from app.schemas.continuous_intelligence_models import (
    IntelligenceReassessmentDTO,
    RiskAssessmentVersionDTO,
    ReportUpdateEventDTO,
    IntelligenceChangeEventDTO,
    ImpactLevelLiteral,
)


class ReassessmentOrchestrator:
    """Orchestrates targeted reassessments and versioned risk updates."""

    @staticmethod
    def create_reassessment(
        analysis_id: str,
        trigger_event: IntelligenceChangeEventDTO,
        previous_risk_score: float,
        proposed_risk_score: float,
        impact_level: ImpactLevelLiteral,
        case_id: Optional[str] = None,
        reason: str = "",
    ) -> IntelligenceReassessmentDTO:
        """Create a new pending reassessment record."""
        return IntelligenceReassessmentDTO(
            reassessment_id=f"reass_{uuid.uuid4().hex[:12]}",
            analysis_id=analysis_id,
            case_id=case_id,
            trigger_event_id=trigger_event.event_id,
            impact_level=impact_level,
            previous_risk_score=previous_risk_score,
            proposed_risk_score=proposed_risk_score,
            status="PENDING_APPROVAL" if impact_level in ("HIGH_IMPACT", "CRITICAL_IMPACT") else "AUTO_APPROVED",
            requested_by="continuous_intelligence_engine",
            reason=reason or f"Reassessment triggered by {trigger_event.event_type} on entity {trigger_event.entity_id}",
        )

    @staticmethod
    def apply_reassessment(
        reassessment: IntelligenceReassessmentDTO,
        report_id: str,
        current_version_number: int,
        supporting_intelligence: List[str],
        approved_by: str = "SYSTEM_AUTOMATION",
    ) -> Tuple[RiskAssessmentVersionDTO, ReportUpdateEventDTO]:
        """Apply approved reassessment to generate new immutable risk version and report update event."""
        reassessment.status = "APPROVED"
        reassessment.approved_by = approved_by
        reassessment.resolved_at = datetime.now(timezone.utc).isoformat()

        new_version_number = current_version_number + 1

        risk_band = (
            "CRITICAL_RISK" if reassessment.proposed_risk_score >= 85.0
            else "HIGH_RISK" if reassessment.proposed_risk_score >= 70.0
            else "MODERATE_RISK" if reassessment.proposed_risk_score >= 40.0
            else "LOW_RISK"
        )

        risk_version = RiskAssessmentVersionDTO(
            version_id=f"rav_{uuid.uuid4().hex[:12]}",
            analysis_id=reassessment.analysis_id,
            report_id=report_id,
            version_number=new_version_number,
            risk_score=reassessment.proposed_risk_score,
            risk_band=risk_band,
            confidence="HIGH",
            trigger_event_id=reassessment.trigger_event_id,
            supporting_intelligence=supporting_intelligence,
        )

        report_update = ReportUpdateEventDTO(
            update_event_id=f"rue_{uuid.uuid4().hex[:12]}",
            report_id=report_id,
            previous_version=current_version_number,
            new_version=new_version_number,
            change_reason=reassessment.reason,
            intelligence_source_ids=[reassessment.trigger_event_id],
            triggered_by=approved_by,
        )

        return risk_version, report_update
