"""
Crown Jewel Registry & Critical Asset Protection Engine (Phase 34)
==================================================================
Catalogs mission-critical high-value assets (crown jewels), maps sensitivity
levels, and provides boundary isolation checks.
"""

from typing import Dict, Any, List, Optional
import datetime
from app.schemas.zero_trust_exposure_models import CrownJewelDTO


class CrownJewelEngine:
    VALID_SENSITIVITY = ["PUBLIC", "INTERNAL", "CONFIDENTIAL", "RESTRICTED", "HIGHLY_RESTRICTED"]

    def __init__(self):
        self._crown_jewels: Dict[str, Dict[str, Any]] = {}

    def register_crown_jewel(
        self,
        jewel_id: str,
        tenant_id: str,
        name: str,
        resource_type: str = "ASSET",
        sensitivity: str = "RESTRICTED",
        business_criticality: str = "CRITICAL",
        owner: str = "SECURITY_ADMIN",
        data_classification: Optional[str] = None,
        recovery_time_objective_hours: Optional[int] = None,
        loss_impact_financial: Optional[str] = None,
        zone_id: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        eff_sens = data_classification or sensitivity
        if eff_sens not in self.VALID_SENSITIVITY:
            eff_sens = "RESTRICTED"

        protection_level = "MAXIMUM_ZERO_TRUST" if eff_sens in ["RESTRICTED", "HIGHLY_RESTRICTED"] else "STANDARD_ZERO_TRUST"

        record = {
            "jewel_id": jewel_id,
            "tenant_id": tenant_id,
            "name": name,
            "resource_type": resource_type,
            "sensitivity": eff_sens,
            "data_classification": eff_sens,
            "business_criticality": business_criticality,
            "owner": owner,
            "protection_level": protection_level,
            "recovery_time_objective_hours": recovery_time_objective_hours,
            "loss_impact_financial": loss_impact_financial,
            "zone_id": zone_id,
            "blast_radius_factor": 3.0 if eff_sens == "HIGHLY_RESTRICTED" else 2.0,
            "created_at": datetime.datetime.now(datetime.timezone.utc).isoformat()
        }
        self._crown_jewels[jewel_id] = record
        return record


    def get_crown_jewels(self, tenant_id: str) -> List[Dict[str, Any]]:
        return [j for j in self._crown_jewels.values() if j["tenant_id"] == tenant_id]

    def get_crown_jewel(self, jewel_id: str, tenant_id: str) -> Optional[Dict[str, Any]]:
        jewel = self._crown_jewels.get(jewel_id)
        if jewel and jewel["tenant_id"] == tenant_id:
            return jewel
        return None


crown_jewel_engine = CrownJewelEngine()
