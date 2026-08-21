"""
TruthShield X — Mission Task Engine (Phase 29).

Orchestrates operational tasks across SOC, Threat Hunting, Assurance, and Engineering teams with strict dependency management.
"""

from typing import Dict, List, Optional
from datetime import datetime, timezone
from app.schemas.mission_control_os_models import MissionTaskDTO, TaskStateLiteral, MissionPriorityLiteral


class MissionTaskEngine:
    """Manages cross-subsystem task lifecycles, dependencies, and ownership assignments."""

    def __init__(self):
        self._tasks: Dict[str, MissionTaskDTO] = {}
        self._seed_default_tasks()

    def _seed_default_tasks(self):
        t1 = MissionTaskDTO(
            task_id="task_investigate_darkstorm_burst",
            title="Investigate DarkStorm C2 DNS Lateral Movement Anomaly",
            task_type="INVESTIGATE",
            owner="SOC_ANALYST_LEAD",
            priority="HIGH",
            sla_seconds=1800.0,
            dependencies=[],
            status="IN_PROGRESS",
            evidence=["NetFlow burst logs", "Sigma entropy detection alert"],
            created_at=datetime.now(timezone.utc).isoformat(),
        )
        self._tasks[t1.task_id] = t1

    def create_task(
        self,
        title: str,
        task_type: str = "INVESTIGATE",
        owner: str = "SOC_ANALYST",
        priority: MissionPriorityLiteral = "HIGH",
        sla_seconds: float = 1800.0,
        dependencies: Optional[List[str]] = None,
        evidence: Optional[List[str]] = None,
    ) -> MissionTaskDTO:
        # If dependencies exist, verify their states
        dep_list = dependencies or []
        initial_status: TaskStateLiteral = "BLOCKED" if any(
            self._tasks.get(d) and self._tasks[d].status != "COMPLETED" for d in dep_list
        ) else "CREATED"

        dto = MissionTaskDTO(
            title=title,
            task_type=task_type,  # type: ignore
            owner=owner,
            priority=priority,
            sla_seconds=sla_seconds,
            dependencies=dep_list,
            status=initial_status,
            evidence=evidence or [],
            created_at=datetime.now(timezone.utc).isoformat(),
        )
        self._tasks[dto.task_id] = dto
        return dto

    def update_task_status(self, task_id: str, new_status: TaskStateLiteral) -> Optional[MissionTaskDTO]:
        task = self._tasks.get(task_id)
        if not task:
            return None

        # Check dependency prerequisites before allowing IN_PROGRESS or COMPLETED
        if new_status in ["IN_PROGRESS", "COMPLETED"]:
            uncompleted_deps = [d for d in task.dependencies if self._tasks.get(d) and self._tasks[d].status != "COMPLETED"]
            if uncompleted_deps:
                raise ValueError(f"Cannot transition task to '{new_status}': prerequisite dependencies {uncompleted_deps} not completed.")

        updated = MissionTaskDTO(
            task_id=task.task_id,
            title=task.title,
            task_type=task.task_type,
            owner=task.owner,
            priority=task.priority,
            sla_seconds=task.sla_seconds,
            dependencies=task.dependencies,
            status=new_status,
            evidence=task.evidence,
            created_at=task.created_at,
        )
        self._tasks[task_id] = updated
        return updated

    def get_task(self, task_id: str) -> Optional[MissionTaskDTO]:
        return self._tasks.get(task_id)

    def list_tasks(self) -> List[MissionTaskDTO]:
        return list(self._tasks.values())
