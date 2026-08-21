"""
TruthShield X — Security Memory Engine (Phase 30).

Maintains verified defensive lessons with strict applicability boundaries preventing cross-tenant over-generalization.
"""

from typing import Dict, List, Optional
from app.schemas.autonomous_defense_models import DefensiveLessonDTO, ApplicabilityLiteral


class SecurityMemoryEngine:
    """Stores verified institutional security knowledge with strict tenant and environmental scope partitioning."""

    def __init__(self):
        self._lessons: Dict[str, DefensiveLessonDTO] = {}
        self._seed_default_lesson()

    def _seed_default_lesson(self):
        l1 = DefensiveLessonDTO(
            lesson_id="lsn_dns_tunneling_01",
            threat_pattern="DarkStorm C2 DNS Tunneling Anomaly",
            environment="Production Kubernetes Ingress",
            recommended_action="Enable early DNS entropy inspection filter",
            expected_gain="Reduces MTTD from 12m to 2m",
            evidence_count=5,
            validation_count=3,
            confidence=0.95,
            applicability="TENANT_SPECIFIC",
            expiration="2027-01-01T00:00:00Z",
            status="LEARNED",
            tenant_id="default_tenant",
        )
        self._lessons[l1.lesson_id] = l1

    def store_lesson(self, lesson: DefensiveLessonDTO) -> DefensiveLessonDTO:
        self._lessons[lesson.lesson_id] = lesson
        return lesson

    def get_applicable_lessons(
        self,
        tenant_id: str,
        allow_cross_tenant: bool = False,
    ) -> List[DefensiveLessonDTO]:
        res = []
        for l in self._lessons.values():
            if l.tenant_id == tenant_id:
                res.append(l)
            elif allow_cross_tenant and l.applicability == "GENERIC":
                res.append(l)
        return res

    def list_all_lessons(self) -> List[DefensiveLessonDTO]:
        return list(self._lessons.values())
