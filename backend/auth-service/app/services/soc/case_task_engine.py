"""
TruthShield X — Case & Task Management Engine (Phase 21).

Manages Security Cases, Incident Tasks, and collaboration workflows.
"""

from typing import Dict, List, Optional
from datetime import datetime, timezone
from app.schemas.autonomous_soc_models import SecurityCaseDTO, IncidentTaskDTO


class CaseTaskEngine:
    """Coordinates case files, analyst assignments, and forensic tasks."""

    def __init__(self):
        self._cases: Dict[str, SecurityCaseDTO] = {}
        self._tasks: Dict[str, IncidentTaskDTO] = {}

    def create_case(self, tenant_id: str, title: str, incident_ids: List[str]) -> SecurityCaseDTO:
        case = SecurityCaseDTO(
            tenant_id=tenant_id,
            title=title,
            incident_ids=incident_ids,
            status="OPEN",
        )
        self._cases[case.case_id] = case
        return case

    def add_task(self, case_id: str, incident_id: str, title: str, owner: str) -> IncidentTaskDTO:
        task = IncidentTaskDTO(
            incident_id=incident_id,
            title=title,
            owner=owner,
            status="TODO",
        )
        self._tasks[task.task_id] = task

        case = self._cases.get(case_id)
        if case:
            updated_tasks = list(case.tasks) + [task]
            self._cases[case_id] = SecurityCaseDTO(
                case_id=case.case_id,
                tenant_id=case.tenant_id,
                title=case.title,
                incident_ids=case.incident_ids,
                alert_ids=case.alert_ids,
                tasks=updated_tasks,
                status=case.status,
                created_at=case.created_at,
            )
        return task

    def get_case(self, case_id: str) -> Optional[SecurityCaseDTO]:
        return self._cases.get(case_id)
