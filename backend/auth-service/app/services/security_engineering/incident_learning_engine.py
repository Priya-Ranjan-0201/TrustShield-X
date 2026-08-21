"""
TruthShield X — Incident Learning Engine (Phase 25).

Transforms closed incident outcomes into actionable engineering lessons and candidate improvements.
"""

from typing import Dict, List, Optional
from datetime import datetime, timezone
from app.schemas.security_engineering_models import IncidentLearningRecordDTO


class IncidentLearningEngine:
    """Extracts post-incident operational findings and generates candidate improvements."""

    def __init__(self):
        self._learnings: Dict[str, IncidentLearningRecordDTO] = {}
        self._seed_default_learning()

    def _seed_default_learning(self):
        l1 = IncidentLearningRecordDTO(
            learning_id="learn_inc_credential_stuffing",
            incident_id="inc_credential_stuffing_2026",
            detection_eval="Rule fired in 12s; detected brute-force burst.",
            response_eval="IP blocked across edge proxies in 45s.",
            containment_eval="No unauthorized accounts breached.",
            recovery_eval="No datastore rollback needed.",
            failures_identified=[],
            successful_controls=["ctl_tenant_isolation", "ctl_four_eyes_response"],
            lessons_learned=["Add proactive threat hunting query for low-and-slow credential attempts."],
            generated_improvements=["imp_sigma_t1055_rule"],
        )
        self._learnings[l1.learning_id] = l1

    def record_incident_learning(
        self,
        incident_id: str,
        detection_eval: str,
        response_eval: str,
        containment_eval: str,
        recovery_eval: str,
        failures: Optional[List[str]] = None,
        successful_controls: Optional[List[str]] = None,
        lessons: Optional[List[str]] = None,
    ) -> IncidentLearningRecordDTO:
        dto = IncidentLearningRecordDTO(
            incident_id=incident_id,
            detection_eval=detection_eval,
            response_eval=response_eval,
            containment_eval=containment_eval,
            recovery_eval=recovery_eval,
            failures_identified=failures or [],
            successful_controls=successful_controls or ["ctl_tenant_isolation"],
            lessons_learned=lessons or ["Strengthen multi-factor authentication enforcement on legacy endpoints."],
            recorded_at=datetime.now(timezone.utc).isoformat(),
        )
        self._learnings[dto.learning_id] = dto
        return dto

    def get_learning(self, learning_id: str) -> Optional[IncidentLearningRecordDTO]:
        return self._learnings.get(learning_id)

    def list_learnings(self) -> List[IncidentLearningRecordDTO]:
        return list(self._learnings.values())
