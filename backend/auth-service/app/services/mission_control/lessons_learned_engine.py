"""
TruthShield X — Lessons Learned & Root Cause Analysis Engine

Generates post-incident analysis with root cause categorization,
contributing factors, and knowledge graph update recommendations.
"""

from typing import Dict, List, Optional
from datetime import datetime, timezone
from app.schemas.mission_control_models import (
    LessonsLearnedDTO,
    RootCauseAnalysisDTO,
    RootCauseCategoryLiteral,
)


class LessonsLearnedEngine:
    """Post-incident analysis, root cause identification, and knowledge update."""

    def __init__(self):
        self._lessons: Dict[str, LessonsLearnedDTO] = {}
        self._rcas: Dict[str, RootCauseAnalysisDTO] = {}

    def create_root_cause_analysis(
        self,
        incident_command_id: str,
        primary_cause: RootCauseCategoryLiteral,
        contributing_factors: Optional[List[str]] = None,
        enabling_conditions: Optional[List[str]] = None,
        failed_controls: Optional[List[str]] = None,
        missing_controls: Optional[List[str]] = None,
        evidence_references: Optional[List[str]] = None,
        confidence: float = 0.5,
        analyst: str = "",
    ) -> RootCauseAnalysisDTO:
        """Creates a root cause analysis record."""
        rca = RootCauseAnalysisDTO(
            incident_command_id=incident_command_id,
            primary_cause=primary_cause,
            contributing_factors=contributing_factors or [],
            enabling_conditions=enabling_conditions or [],
            failed_controls=failed_controls or [],
            missing_controls=missing_controls or [],
            evidence_references=evidence_references or [],
            confidence=confidence,
            analyst=analyst,
        )
        self._rcas[rca.rca_id] = rca
        return rca

    def generate_lessons_learned(
        self,
        incident_command_id: str,
        what_happened: str,
        what_worked: Optional[List[str]] = None,
        what_failed: Optional[List[str]] = None,
        control_failures: Optional[List[str]] = None,
        response_delays: Optional[List[str]] = None,
        detection_gaps: Optional[List[str]] = None,
        governance_gaps: Optional[List[str]] = None,
        recommendations: Optional[List[str]] = None,
        root_cause_analysis: Optional[RootCauseAnalysisDTO] = None,
    ) -> LessonsLearnedDTO:
        """Generates a lessons learned record."""
        lessons = LessonsLearnedDTO(
            incident_command_id=incident_command_id,
            what_happened=what_happened,
            what_worked=what_worked or [],
            what_failed=what_failed or [],
            control_failures=control_failures or [],
            response_delays=response_delays or [],
            detection_gaps=detection_gaps or [],
            governance_gaps=governance_gaps or [],
            recommendations=recommendations or [],
            root_cause_analysis=root_cause_analysis,
        )
        self._lessons[lessons.lessons_id] = lessons
        return lessons

    def get_lessons(self, incident_command_id: str) -> Optional[LessonsLearnedDTO]:
        """Retrieves lessons learned for an incident."""
        for l in self._lessons.values():
            if l.incident_command_id == incident_command_id:
                return l
        return None

    def get_rca(self, incident_command_id: str) -> Optional[RootCauseAnalysisDTO]:
        """Retrieves root cause analysis for an incident."""
        for r in self._rcas.values():
            if r.incident_command_id == incident_command_id:
                return r
        return None
