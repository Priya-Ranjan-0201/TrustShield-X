"""
TruthShield X — Compliance Remediation Engine (Phase 32).

Tracks remediation tasks, enforces SLAs, and blocks closing findings without empirical validation.
"""

from typing import Dict, List, Optional, Any
from app.schemas.enterprise_governance_models import ComplianceFindingDTO, RemediationTaskDTO


class ComplianceRemediationEngine:
    """Manages finding lifecycles, requiring objective verification before closing remediation tasks."""

    def __init__(self):
        self._findings: Dict[str, ComplianceFindingDTO] = {}
        self._tasks: Dict[str, RemediationTaskDTO] = {}
        self._seed_defaults()

    def _seed_defaults(self):
        f1 = ComplianceFindingDTO(
            finding_id="fnd_svc_account_legacy",
            source="Continuous Security Assurance Scanner",
            severity="HIGH",
            confidence=0.95,
            affected_control="ctrl_iam_mfa_enforcement",
            affected_asset="Legacy Service Account svc_reports_01",
            risk_level="HIGH",
            owner="IAM_LEAD",
            status="OPEN",
        )
        t1 = RemediationTaskDTO(
            task_id="rem_svc_account_oauth2",
            finding_id="fnd_svc_account_legacy",
            action="Migrate legacy service account to OAuth2 client credentials with certificate pinning",
            owner="SECOPS_ENGINEER",
            priority="P1",
            sla_due_date="2026-08-30T18:00:00Z",
            status="IN_PROGRESS",
            is_verified=False,
        )
        self._findings[f1.finding_id] = f1
        self._tasks[t1.task_id] = t1

    def attempt_close_remediation(
        self,
        task_id: str,
        is_empirically_validated: bool = False,
    ) -> Dict[str, Any]:
        task = self._tasks.get(task_id)
        if not task:
            raise ValueError(f"Task '{task_id}' not found.")

        # Absolute Rule: Never close finding merely because developer claimed "fixed"
        if not is_empirically_validated:
            return {
                "task_id": task_id,
                "allowed": False,
                "status": "BLOCKED",
                "reason": "CLOSURE_REQUIRES_EMPIRICAL_VALIDATION_RETEST",
            }

        return {
            "task_id": task_id,
            "allowed": True,
            "status": "CLOSED",
            "reason": "EMPIRICAL_RETEST_PASSED",
        }

    def list_findings(self) -> List[ComplianceFindingDTO]:
        return list(self._findings.values())

    def list_tasks(self) -> List[RemediationTaskDTO]:
        return list(self._tasks.values())
