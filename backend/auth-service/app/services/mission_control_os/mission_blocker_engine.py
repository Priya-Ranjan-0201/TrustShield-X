"""
TruthShield X — Mission Blocker Engine (Phase 29).

Detects workflow blockers including pending approvals, unavailable service dependencies, stale intelligence, and queue bottlenecks.
"""

from typing import Dict, List, Any


class MissionBlockerEngine:
    """Identifies root causes of blocked tasks and provides actionable remediation recommendations."""

    def diagnose_blockers(
        self,
        task_id: str,
        missing_approvals: List[str],
        dependency_statuses: Dict[str, str],
        is_intelligence_stale: bool = False,
    ) -> Dict[str, Any]:
        blockers = []

        if missing_approvals:
            blockers.append({
                "category": "MISSING_APPROVAL",
                "detail": f"Awaiting Four-Eyes authorization from: {', '.join(missing_approvals)}",
            })

        for dep_id, status in dependency_statuses.items():
            if status != "HEALTHY" and status != "COMPLETED":
                blockers.append({
                    "category": "DEPENDENCY_FAILURE",
                    "detail": f"Prerequisite dependency '{dep_id}' is in status '{status}'",
                })

        if is_intelligence_stale:
            blockers.append({
                "category": "STALE_INTELLIGENCE",
                "detail": "Underlying threat intelligence feed has expired or is uncalibrated",
            })

        return {
            "task_id": task_id,
            "has_blockers": len(blockers) > 0,
            "blocker_count": len(blockers),
            "blockers": blockers,
            "can_auto_proceed": len(blockers) == 0,
        }
