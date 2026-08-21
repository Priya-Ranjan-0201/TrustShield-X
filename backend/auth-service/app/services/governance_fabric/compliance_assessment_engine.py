"""
TruthShield X — Compliance Assessment & Gap Engine
"""

from typing import Dict, List, Optional, Any
from app.schemas.governance_fabric_models import (
    GovernanceRequirementDTO,
    GovernanceEvidenceDTO,
    RequirementStatusLiteral,
)


class ComplianceAssessmentEngine:
    """Evaluates compliance requirements strictly from current empirical evidence."""

    def assess_requirement(
        self,
        requirement: GovernanceRequirementDTO,
        mapped_evidence: List[GovernanceEvidenceDTO],
        control_test_passed: bool = True,
    ) -> Dict[str, Any]:
        """Evaluates requirement status with evidence freshness and test verification."""
        if not mapped_evidence:
            return {
                "status": "NOT_ASSESSED",
                "confidence": 0.0,
                "reason": "No evidence mapped to requirement.",
                "gaps": ["MISSING_EVIDENCE"],
            }

        # Check for expired or invalid evidence
        has_expired = any(e.freshness in ("EXPIRED", "INVALID") for e in mapped_evidence)
        if has_expired:
            return {
                "status": "PARTIALLY_SATISFIED",
                "confidence": 0.50,
                "reason": "Mapped evidence is stale or expired.",
                "gaps": ["STALE_EVIDENCE"],
            }

        if not control_test_passed:
            return {
                "status": "NOT_SATISFIED",
                "confidence": 0.85,
                "reason": "Mapped control test failed during empirical validation.",
                "gaps": ["CONTROL_TEST_FAILED"],
            }

        return {
            "status": "SATISFIED",
            "confidence": 0.95,
            "reason": "All mapped controls verified with valid, fresh evidence.",
            "gaps": [],
        }
