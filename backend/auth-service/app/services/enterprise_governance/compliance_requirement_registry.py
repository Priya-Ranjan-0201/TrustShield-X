"""
TruthShield X — Compliance Requirement Registry (Phase 32).

Maintains regulatory and industry framework requirements (DPDP 2023, ISO 27001, SOC 2, NIST CSF, NIST AI RMF, CIS).
"""

from typing import Dict, List, Optional
from app.schemas.enterprise_governance_models import ComplianceRequirementDTO, FrameworkLiteral


class ComplianceRequirementRegistry:
    """Stores framework requirements and maps them to technical controls with explicit confidence scoring."""

    def __init__(self):
        self._requirements: Dict[str, ComplianceRequirementDTO] = {}
        self._seed_default_requirements()

    def _seed_default_requirements(self):
        r1 = ComplianceRequirementDTO(
            requirement_id="req_iso27001_a9_4_2",
            framework="ISO_27001",
            version="2022",
            title="User Authentication for External Connections",
            description="Appropriate authentication methods shall be applied to control user access",
            mapped_controls=["ctrl_iam_mfa_enforcement"],
            evidence_requirements=["MFA configuration dump", "IdP audit logs"],
            confidence="DIRECT",
            status="COMPLIANT",
        )
        r2 = ComplianceRequirementDTO(
            requirement_id="req_dpdp_sec_8_5",
            framework="DPDP_2023",
            version="2023",
            title="Reasonable Security Safeguards",
            description="Data Fiduciary shall protect personal data by taking reasonable security safeguards",
            mapped_controls=["ctrl_data_encryption_at_rest", "ctrl_iam_mfa_enforcement"],
            evidence_requirements=["Encryption status audit", "Access control matrices"],
            confidence="DIRECT",
            status="COMPLIANT",
        )
        self._requirements[r1.requirement_id] = r1
        self._requirements[r2.requirement_id] = r2

    def get_requirement(self, requirement_id: str) -> Optional[ComplianceRequirementDTO]:
        return self._requirements.get(requirement_id)

    def list_requirements(self, framework: Optional[FrameworkLiteral] = None) -> List[ComplianceRequirementDTO]:
        if framework:
            return [r for r in self._requirements.values() if r.framework == framework]
        return list(self._requirements.values())
