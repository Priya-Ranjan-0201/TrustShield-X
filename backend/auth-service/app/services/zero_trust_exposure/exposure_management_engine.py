"""
Exposure Management Engine (Phase 34)
=====================================
Manages exposure findings (PUBLICLY_REACHABLE, MISCONFIGURED, EXPOSED_ADMIN_INTERFACE,
EXPOSED_SERVICE, EXPOSED_SECRET, EXPOSED_STORAGE, EXPOSED_API, EXPIRED_CERTIFICATE, UNKNOWN_ASSET),
reachability validation, and business impact analysis.
"""

from typing import Dict, Any, List, Optional
import datetime
from app.schemas.zero_trust_exposure_models import ExposureFindingDTO


class ExposureManagementEngine:
    VALID_EXPOSURES = [
        "PUBLICLY_REACHABLE", "MISCONFIGURED", "EXPOSED_ADMIN_INTERFACE",
        "EXPOSED_SERVICE", "EXPOSED_SECRET", "EXPOSED_STORAGE",
        "EXPOSED_API", "EXPIRED_CERTIFICATE", "UNKNOWN_ASSET"
    ]

    def __init__(self):
        self._exposures: Dict[str, Dict[str, Any]] = {}

    def record_exposure(
        self,
        exposure_id: str,
        tenant_id: str,
        asset_id: str,
        exposure_type: str,
        severity: str = "HIGH",
        reachability_evidence: Optional[Dict[str, Any]] = None,
        business_impact: str = "MEDIUM",
        details: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        if exposure_type not in self.VALID_EXPOSURES:
            exposure_type = "EXPOSED_SERVICE"

        reachability = "NOT_VERIFIED"
        if reachability_evidence:
            if reachability_evidence.get("probe_successful") or reachability_evidence.get("verified_ports") or reachability_evidence.get("verified_reachable"):
                reachability = "REACHABLE"
            elif reachability_evidence.get("probe_blocked") or reachability_evidence.get("blocked"):
                reachability = "BLOCKED"

        finding = {
            "exposure_id": exposure_id,
            "tenant_id": tenant_id,
            "asset_id": asset_id,
            "exposure_type": exposure_type,
            "severity": severity,
            "reachability": reachability,
            "business_impact": business_impact,
            "status": "OPEN",
            "details": details or {},
            "discovered_at": datetime.datetime.now(datetime.timezone.utc).isoformat()
        }
        self._exposures[exposure_id] = finding
        return finding

    def get_open_exposures(self, tenant_id: str) -> List[Dict[str, Any]]:
        return [
            exp for exp in self._exposures.values()
            if exp["tenant_id"] == tenant_id and exp["status"] == "OPEN"
        ]

    def update_exposure_status(self, exposure_id: str, tenant_id: str, new_status: str) -> Dict[str, Any]:
        exp = self._exposures.get(exposure_id)
        if not exp or exp["tenant_id"] != tenant_id:
            return {"status": "FAILED", "reason": "EXPOSURE_NOT_FOUND"}
        exp["status"] = new_status
        return {"status": "SUCCESS", "exposure_id": exposure_id, "new_status": new_status}


exposure_management_engine = ExposureManagementEngine()
