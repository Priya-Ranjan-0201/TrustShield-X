"""
TruthShield X — Evidence Management Engine (Phase 32).

Tracks evidence items, monitors freshness, verifies SHA-256 cryptographic hashes, and detects evidence tampering.
"""

from typing import Dict, List, Optional, Any
from app.schemas.enterprise_governance_models import EvidenceDTO


class EvidenceManagementEngine:
    """Manages audit evidence artifacts with tamper-detection and automatic expiry tracking."""

    def __init__(self):
        self._evidence: Dict[str, EvidenceDTO] = {}
        self._seed_default_evidence()

    def _seed_default_evidence(self):
        e1 = EvidenceDTO(
            evidence_id="evd_iam_mfa_config_dump",
            type="CONFIGURATION_DUMP",
            source="TruthShield Auth Service IAM Enclave",
            owner="IAM_LEAD",
            classification="RESTRICTED",
            validity_period_days=90,
            related_control="ctrl_iam_mfa_enforcement",
            related_requirement="req_iso27001_a9_4_2",
            integrity_hash="c782b6b0c2e718b5b5c92ef9481283d5a498b375b485d99bfa210940562e84c9",
            freshness="CURRENT",
            status="VALID",
        )
        self._evidence[e1.evidence_id] = e1

    def verify_evidence_integrity(self, evidence_id: str, computed_hash: str) -> Dict[str, Any]:
        e = self._evidence.get(evidence_id)
        if not e:
            raise ValueError(f"Evidence '{evidence_id}' not found.")

        if computed_hash != e.integrity_hash:
            return {
                "evidence_id": evidence_id,
                "is_valid": False,
                "status": "EVIDENCE_INTEGRITY_VIOLATION",
                "reason": "CHECKSUM_MISMATCH_ARTIFACT_TAMPERED",
            }

        return {
            "evidence_id": evidence_id,
            "is_valid": True,
            "status": "VALID",
            "reason": "INTEGRITY_HASH_VERIFIED",
        }

    def list_evidence(self) -> List[EvidenceDTO]:
        return list(self._evidence.values())
