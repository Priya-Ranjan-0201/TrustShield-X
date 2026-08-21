"""
TruthShield X — Historical Analog & Lessons Learned Engine (Phase 19).

Searches historical events for similar incidents, attack patterns, and response outcomes.
"""

from typing import Dict, List, Optional
from app.schemas.cyber_knowledge_fabric_models import (
    HistoricalAnalogDTO,
    LessonsLearnedDTO,
)


class HistoricalAnalogEngine:
    """Matches active incidents against past historical incidents and extracts lessons learned."""

    def __init__(self):
        self._analogs: Dict[str, HistoricalAnalogDTO] = {}
        self._lessons: Dict[str, LessonsLearnedDTO] = {}
        self._initialize_defaults()

    def _initialize_defaults(self):
        a = HistoricalAnalogDTO(
            analog_id="analog_q4_phish",
            past_incident_id="inc_2025_q4_0012",
            similarity_score=0.91,
            matched_techniques=["T1566.002", "T1078.004"],
            context_match="Kubernetes checkout pod credential harvesting with reverse proxy bypass.",
            past_response_outcome="Service principal rotated in 14 minutes; zero lateral spread.",
        )
        self._analogs[a.analog_id] = a

        l = LessonsLearnedDTO(
            lesson_id="lesson_mfa_stepup",
            incident_type="API_CREDENTIAL_ABUSE",
            successful_defenses=["Conditional access step-up challenge", "IP rate limiting"],
            failed_defenses=["Static bearer token validation without client binding"],
            recovery_bottlenecks=["Manual secret rotation in distributed configuration maps"],
            policy_recommendation="Enforce workload identity federation with ephemeral 15-minute token TTL.",
        )
        self._lessons[l.lesson_id] = l

    def find_analogs(self, techniques: List[str]) -> List[HistoricalAnalogDTO]:
        """Finds matching historical incidents based on technique overlap."""
        results = []
        for a in self._analogs.values():
            overlap = set(techniques).intersection(set(a.matched_techniques))
            if overlap:
                results.append(a)
        return results or list(self._analogs.values())

    def list_lessons_learned(self) -> List[LessonsLearnedDTO]:
        return list(self._lessons.values())
