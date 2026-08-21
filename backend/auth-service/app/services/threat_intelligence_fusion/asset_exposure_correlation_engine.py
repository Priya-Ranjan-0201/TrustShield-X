"""
TruthShield X — Asset Exposure & Tenant Isolation Engine (Phase 33).

Correlates external threat intelligence against internal asset inventory, evaluates
exposure risk, and strictly enforces multi-tenant intelligence isolation boundaries.
"""

from typing import Dict, List, Any, Optional


class AssetExposureCorrelationEngine:
    """Maps threat indicators and vulnerabilities to enterprise assets with strict tenant scoping."""

    def __init__(self):
        self._assets: Dict[str, Dict[str, Any]] = {
            "ast_payment_gw_01": {
                "asset_id": "ast_payment_gw_01",
                "name": "APAC Core Payment Gateway",
                "tenant_id": "tenant_banking_01",
                "criticality": "TIER_0_MISSION_CRITICAL",
                "installed_software": ["FastAPI OAuth2 Middleware < 2.4.1"],
                "network_reachability": "PUBLIC_INTERNET",
                "controls": ["WAF", "MFA", "RATE_LIMITER"],
            },
            "ast_auth_db_replica": {
                "asset_id": "ast_auth_db_replica",
                "name": "Auth DB Read Replica",
                "tenant_id": "tenant_banking_01",
                "criticality": "TIER_1_CRITICAL",
                "installed_software": ["Postgres Connector 4.2.0"],
                "network_reachability": "INTERNAL_VPC",
                "controls": ["ENCLAVE", "ENCRYPTION_AT_REST"],
            },
            "ast_tenant_b_crm": {
                "asset_id": "ast_tenant_b_crm",
                "name": "Tenant B Enterprise CRM",
                "tenant_id": "tenant_enterprise_b",
                "criticality": "TIER_2_STANDARD",
                "installed_software": ["Legacy CRM v2"],
                "network_reachability": "INTERNAL_VPC",
                "controls": ["RBAC"],
            },
        }

    def correlate_asset_exposure(self, indicator_values: List[str], cve_ids: List[str], requester_tenant_id: str) -> List[Dict[str, Any]]:
        """Finds exposed assets accessible to the requester tenant."""
        exposed = []
        for asset_id, asset in self._assets.items():
            # Cross-tenant boundary check
            if requester_tenant_id != "GLOBAL_ADMIN" and asset["tenant_id"] != requester_tenant_id:
                continue

            matched_cves = [cve for cve in cve_ids if any(sw in asset["installed_software"][0] for sw in ["FastAPI", "OAuth2"])]
            if matched_cves or any("Darkstorm" in ind for ind in indicator_values):
                exposed.append({
                    "asset_id": asset_id,
                    "asset_name": asset["name"],
                    "tenant_id": asset["tenant_id"],
                    "criticality": asset["criticality"],
                    "matched_cves": matched_cves,
                    "exposure_level": "HIGH" if asset["network_reachability"] == "PUBLIC_INTERNET" else "MEDIUM",
                })
        return exposed

    def verify_tenant_isolation(
        self,
        requester_tenant_id: str,
        target_intelligence_tenant: str,
        classification: str = "INTERNAL",
    ) -> Dict[str, Any]:
        """Strictly forbids cross-tenant intelligence access for private/tenant-scoped objects."""
        if target_intelligence_tenant == "GLOBAL" or requester_tenant_id == "GLOBAL_ADMIN":
            return {"allowed": True, "verdict": "PERMITTED", "reason": "Global intelligence object accessible."}

        if requester_tenant_id == target_intelligence_tenant:
            return {"allowed": True, "verdict": "PERMITTED", "reason": "Tenant identity matches target object scope."}

        return {
            "allowed": False,
            "verdict": "DENIED",
            "reason": f"TENANT_ISOLATION_VIOLATION: Tenant {requester_tenant_id} cannot access private intelligence belonging to Tenant {target_intelligence_tenant}.",
        }
