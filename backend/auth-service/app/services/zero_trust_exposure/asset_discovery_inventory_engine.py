"""
Asset Discovery & Inventory Engine (Phase 34)
=============================================
Maintains authoritative approved asset inventory, tracks asset metadata
(type, owner, tenant, environment, exposure, criticality, technologies, vulnerabilities, controls, dependencies),
and detects unknown assets (UNKNOWN_EXTERNAL_ASSET).
"""

from typing import Dict, Any, List, Optional
import datetime


class AssetDiscoveryInventoryEngine:
    def __init__(self):
        self._approved_inventory: Dict[str, Dict[str, Any]] = {}
        self._discovered_assets: Dict[str, Dict[str, Any]] = {}

    def register_approved_asset(
        self,
        asset_id: str,
        tenant_id: str,
        name: str,
        asset_type: str,
        owner: str,
        environment: str = "PRODUCTION",
        exposure: str = "INTERNAL",
        criticality: str = "HIGH",
        technologies: Optional[List[str]] = None,
        vulnerabilities: Optional[List[str]] = None,
        controls: Optional[List[str]] = None,
        dependencies: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        now = datetime.datetime.now(datetime.timezone.utc).isoformat()
        asset = {
            "asset_id": asset_id,
            "tenant_id": tenant_id,
            "name": name,
            "asset_type": asset_type,
            "owner": owner,
            "environment": environment,
            "exposure": exposure,
            "criticality": criticality,
            "technologies": technologies or [],
            "vulnerabilities": vulnerabilities or [],
            "controls": controls or [],
            "dependencies": dependencies or [],
            "approved": True,
            "created_at": now,
            "last_updated": now
        }
        self._approved_inventory[asset_id] = asset
        return asset

    def record_discovered_asset(
        self,
        asset_id: str,
        tenant_id: str,
        identifier: str,
        asset_type: str,
        technologies: Optional[List[str]] = None,
        discovery_source: str = "PASSIVE_DNS"
    ) -> Dict[str, Any]:
        is_known = asset_id in self._approved_inventory
        now = datetime.datetime.now(datetime.timezone.utc).isoformat()
        asset = {
            "asset_id": asset_id,
            "tenant_id": tenant_id,
            "identifier": identifier,
            "asset_type": asset_type,
            "is_known_in_inventory": is_known,
            "technologies": technologies or [],
            "discovery_source": discovery_source,
            "status": "APPROVED" if is_known else "UNKNOWN_EXTERNAL_ASSET",
            "discovered_at": now
        }
        self._discovered_assets[asset_id] = asset
        return asset

    def detect_unknown_assets(self, tenant_id: str) -> List[Dict[str, Any]]:
        """Identifies any discovered asset that is not in the approved inventory."""
        return [
            a for a in self._discovered_assets.values()
            if a["tenant_id"] == tenant_id and not a["is_known_in_inventory"]
        ]

    def get_unknown_assets(self, tenant_id: str) -> List[Dict[str, Any]]:
        return self.detect_unknown_assets(tenant_id)

    def register_internal_asset(
        self,
        asset_id: str,
        tenant_id: str,
        name: str,
        asset_type: str,
        environment: str = "PRODUCTION",
        criticality: str = "HIGH",
        ip_address: Optional[str] = None,
        owner: str = "SecOps",
        **kwargs
    ) -> Dict[str, Any]:
        return self.register_approved_asset(
            asset_id=asset_id,
            tenant_id=tenant_id,
            name=name,
            asset_type=asset_type,
            owner=owner,
            environment=environment,
            exposure="INTERNAL",
            criticality=criticality,
            technologies=[ip_address] if ip_address else None
        )

    def get_approved_inventory(self, tenant_id: str) -> List[Dict[str, Any]]:
        return [a for a in self._approved_inventory.values() if a["tenant_id"] == tenant_id]

    def get_assets(self, tenant_id: str) -> List[Dict[str, Any]]:
        return self.get_approved_inventory(tenant_id)


asset_discovery_inventory_engine = AssetDiscoveryInventoryEngine()


