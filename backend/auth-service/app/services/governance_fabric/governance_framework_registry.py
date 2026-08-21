"""
TruthShield X — Governance Framework & Requirement Registry
"""

import uuid
from typing import Dict, List, Optional, Any
from app.schemas.governance_fabric_models import (
    GovernanceFrameworkDTO,
    GovernanceRequirementDTO,
    RequirementStatusLiteral,
)


class GovernanceFrameworkRegistry:
    """Manages versioned compliance frameworks and verifiable security requirements."""

    def __init__(self):
        # framework_id -> GovernanceFrameworkDTO
        self._frameworks: Dict[str, GovernanceFrameworkDTO] = {}
        # requirement_id -> GovernanceRequirementDTO
        self._requirements: Dict[str, GovernanceRequirementDTO] = {}
        self._initialize_core_frameworks()

    def _initialize_core_frameworks(self) -> None:
        """Seeds initial flagship compliance frameworks and requirements."""
        fws = [
            ("fw_dpdp_2023", "DPDP Act 2023 (India)", "2023", "Digital Personal Data Protection Act, 2023"),
            ("fw_iso_27001", "ISO/IEC 27001:2022", "2022", "Information Security Management Systems"),
            ("fw_soc2_t2", "SOC 2 Type II", "2022", "AICPA Trust Services Criteria (Security & Confidentiality)"),
            ("fw_nist_csf", "NIST CSF 2.0", "2.0", "NIST Cybersecurity Framework 2.0"),
        ]

        for fid, name, ver, ref in fws:
            self._frameworks[fid] = GovernanceFrameworkDTO(
                framework_id=fid,
                name=name,
                version=ver,
                source_reference=ref,
                status="ACTIVE",
                total_requirements=2,
            )

        # Seed core requirements
        reqs = [
            ("req_dpdp_sec8", "fw_dpdp_2023", "Sec. 8(5)", "Reasonable Security Safeguards", "Data Fiduciary must implement reasonable security safeguards to prevent personal data breach.", "DATA_PROTECTION"),
            ("req_iso_a9_4", "fw_iso_27001", "A.9.4.2", "Secure Log-on Procedures", "Access to systems must be controlled by a secure log-on procedure.", "ACCESS_CONTROL"),
            ("req_soc2_cc6_1", "fw_soc2_t2", "CC6.1", "Logical Boundary & Multi-Tenant Isolation", "Logical access boundaries are maintained to prevent unauthorized access across tenants.", "TENANT_ISOLATION"),
            ("req_nist_pr_ac", "fw_nist_csf", "PR.AC-4", "Access Permissions & Least Privilege", "Access permissions, entitlements, and authorisations are managed consistent with the principles of least privilege.", "ACCESS_CONTROL"),
        ]

        for rid, fid, cref, title, desc, cat in reqs:
            self._requirements[rid] = GovernanceRequirementDTO(
                requirement_id=rid,
                framework_id=fid,
                control_reference=cref,
                title=title,
                description=desc,
                category=cat,
                status="SATISFIED",
            )

    def list_frameworks(self) -> List[GovernanceFrameworkDTO]:
        """Lists active governance frameworks."""
        return list(self._frameworks.values())

    def list_requirements(self, framework_id: Optional[str] = None) -> List[GovernanceRequirementDTO]:
        """Lists requirements optionally filtered by framework."""
        if framework_id:
            return [r for r in self._requirements.values() if r.framework_id == framework_id]
        return list(self._requirements.values())

    def get_requirement(self, requirement_id: str) -> Optional[GovernanceRequirementDTO]:
        """Retrieves a single requirement."""
        return self._requirements.get(requirement_id)

    def update_requirement_status(
        self,
        requirement_id: str,
        status: RequirementStatusLiteral,
    ) -> GovernanceRequirementDTO:
        """Updates requirement compliance status based on empirical assessment."""
        req = self._requirements.get(requirement_id)
        if not req:
            raise KeyError(f"Requirement '{requirement_id}' not found.")
        req.status = status
        return req
