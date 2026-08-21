"""
TruthShield X — Security Regression Engine (Phase 24).

Detects regressions against established baselines upon code, configuration, or dependency modifications.
"""

from typing import Dict, List, Optional
from datetime import datetime, timezone
from app.schemas.security_assurance_fabric_models import SecurityRegressionRunDTO


class SecurityRegressionEngine:
    """Evaluates security test suites against baseline expectations to detect regressions."""

    def __init__(self):
        self._runs: Dict[str, SecurityRegressionRunDTO] = {}

    def run_regression_suite(
        self,
        trigger_event: str,
        changed_components: List[str],
        affected_controls: List[str],
        baseline_states: Dict[str, str],
        current_test_results: Dict[str, str],
        tenant_id: str = "default_tenant",
    ) -> SecurityRegressionRunDTO:
        regressions = []
        passed = 0
        failed = 0

        for ctl in affected_controls:
            current_status = current_test_results.get(ctl, "NOT_VERIFIED")
            baseline_status = baseline_states.get(ctl, "PASS")

            if current_status == "PASS":
                passed += 1
            else:
                failed += 1
                if baseline_status == "PASS" and current_status != "PASS":
                    regressions.append(ctl)

        dto = SecurityRegressionRunDTO(
            tenant_id=tenant_id,
            trigger_event=trigger_event,
            changed_components=changed_components,
            affected_controls=affected_controls,
            tests_executed=len(affected_controls),
            passed_count=passed,
            failed_count=failed,
            regressions_detected=regressions,
            executed_at=datetime.now(timezone.utc).isoformat(),
        )
        self._runs[dto.regression_id] = dto
        return dto

    def get_run(self, run_id: str) -> Optional[SecurityRegressionRunDTO]:
        return self._runs.get(run_id)
