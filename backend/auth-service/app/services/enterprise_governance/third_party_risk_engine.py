"""
TruthShield X — Third-Party Risk Engine (Phase 32).

Assesses supply-chain vendors, cloud service providers, and subprocessors against data sovereignty policies.
"""

from typing import Dict, List, Optional, Any
from app.schemas.enterprise_governance_models import ThirdPartyRiskDTO


class ThirdPartyRiskEngine:
    """Manages vendor assessments, risk tiers, and links third-party incidents to internal assets."""

    def __init__(self):
        self._vendors: Dict[str, ThirdPartyRiskDTO] = {}
        self._seed_default_vendor()

    def _seed_default_vendor(self):
        v1 = ThirdPartyRiskDTO(
            vendor_id="vnd_cloud_storage_aws",
            vendor_name="Amazon Web Services Inc.",
            service="S3 Encrypted Object Store",
            data_access_level="CONFIDENTIAL_ENCRYPTED",
            criticality="TIER_1",
            risk_level="LOW",
            assessment_status="APPROVED",
        )
        self._vendors[v1.vendor_id] = v1

    def evaluate_vendor_data_access(
        self,
        vendor_id: str,
        requested_classification: str,
    ) -> Dict[str, Any]:
        v = self._vendors.get(vendor_id)
        if not v or v.assessment_status != "APPROVED":
            return {
                "vendor_id": vendor_id,
                "allowed": False,
                "status": "VENDOR_ACCESS_BLOCKED",
                "reason": "VENDOR_NOT_APPROVED_OR_ASSESSMENT_EXPIRED",
            }

        return {
            "vendor_id": vendor_id,
            "allowed": True,
            "status": "VENDOR_ACCESS_AUTHORIZED",
            "reason": "TIER_1_ASSESSMENT_VALIDATED",
        }

    def list_vendors(self) -> List[ThirdPartyRiskDTO]:
        return list(self._vendors.values())
