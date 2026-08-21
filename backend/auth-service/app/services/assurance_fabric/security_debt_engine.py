"""
TruthShield X — Security Debt Engine (Phase 24).

Identifies and prioritizes unverified controls, stale tests, and security coverage deficits.
"""

from typing import Dict, List
from app.schemas.security_assurance_fabric_models import SecurityDebtDTO


class SecurityDebtEngine:
    """Quantifies and prioritizes architectural security debt."""

    def evaluate_debt(
        self,
        unverified_controls: int = 0,
        outdated_tests: int = 0,
        stale_playbooks: int = 0,
        coverage_gaps: int = 1,
        tenant_id: str = "default_tenant",
    ) -> SecurityDebtDTO:
        debt_score = (unverified_controls * 10.0) + (outdated_tests * 5.0) + (stale_playbooks * 4.0) + (coverage_gaps * 8.0)
        recs = []
        if unverified_controls > 0:
            recs.append("Execute automated validation suites on unverified security controls.")
        if coverage_gaps > 0:
            recs.append("Add detection rules and hunting hypotheses for unmapped MITRE techniques.")

        return SecurityDebtDTO(
            tenant_id=tenant_id,
            unverified_controls_count=unverified_controls,
            outdated_tests_count=outdated_tests,
            stale_playbooks_count=stale_playbooks,
            coverage_gaps_count=coverage_gaps,
            total_debt_score=round(debt_score, 1),
            priority_recommendations=recs,
        )
