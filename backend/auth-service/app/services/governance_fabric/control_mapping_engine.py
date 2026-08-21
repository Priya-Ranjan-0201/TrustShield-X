"""
TruthShield X — Governance Control Mapping Engine
"""

import uuid
from typing import Dict, List, Optional, Any
from app.schemas.governance_fabric_models import ControlMappingDTO


class ControlMappingEngine:
    """Manages traceable mappings between compliance requirements and technical security controls."""

    def __init__(self):
        # mapping_id -> ControlMappingDTO
        self._mappings: Dict[str, ControlMappingDTO] = {}
        self._initialize_core_mappings()

    def _initialize_core_mappings(self) -> None:
        """Seeds core mappings linking frameworks to Phase 13 controls."""
        core_links = [
            ("req_dpdp_sec8", "ctrl_audit_01", "ast_audit_01", "tst_audit_immutability", "evi_audit_01"),
            ("req_iso_a9_4", "ctrl_rbac_01", "ast_rbac_01", "tst_rbac_deny_precedence", "evi_rbac_01"),
            ("req_soc2_cc6_1", "ctrl_iso_01", "ast_iso_01", "tst_tenant_isolation", "evi_iso_01"),
            ("req_nist_pr_ac", "ctrl_rbac_01", "ast_rbac_01", "tst_rbac_deny_precedence", "evi_rbac_01"),
        ]

        for rid, cid, aid, tid, eid in core_links:
            mid = f"map_{uuid.uuid4().hex[:8]}"
            self._mappings[mid] = ControlMappingDTO(
                mapping_id=mid,
                requirement_id=rid,
                control_id=cid,
                assertion_id=aid,
                test_id=tid,
                evidence_id=eid,
                confidence_weight=1.0,
            )

    def map_requirement_to_control(
        self,
        requirement_id: str,
        control_id: str,
        assertion_id: str,
        test_id: str,
        evidence_id: str,
    ) -> ControlMappingDTO:
        """Creates a new traceable mapping."""
        mid = f"map_{uuid.uuid4().hex[:8]}"
        mapping = ControlMappingDTO(
            mapping_id=mid,
            requirement_id=requirement_id,
            control_id=control_id,
            assertion_id=assertion_id,
            test_id=test_id,
            evidence_id=evidence_id,
            confidence_weight=1.0,
        )
        self._mappings[mid] = mapping
        return mapping

    def list_mappings(self, requirement_id: Optional[str] = None) -> List[ControlMappingDTO]:
        """Lists control mappings, optionally filtered by requirement."""
        if requirement_id:
            return [m for m in self._mappings.values() if m.requirement_id == requirement_id]
        return list(self._mappings.values())
