"""
TruthShield X — Resilience Asset & Business Service Manager (Phase 23).

Manages assets and high-level business services with RTO/RPO targets and recovery priorities.
"""

from typing import Dict, List, Optional
from datetime import datetime, timezone
from app.schemas.cyber_resilience_models import ResilienceAssetDTO, BusinessServiceDTO


class ResilienceAssetManager:
    """Manages inventory of resilient infrastructure assets and business services."""

    def __init__(self):
        self._assets: Dict[str, ResilienceAssetDTO] = {}
        self._services: Dict[str, BusinessServiceDTO] = {}
        self._seed_default_inventory()

    def _seed_default_inventory(self):
        # Default Assets
        a1 = ResilienceAssetDTO(
            asset_id="ast_pg_primary",
            tenant_id="default_tenant",
            asset_type="DATABASE",
            name="Primary PostgreSQL Cluster",
            criticality="CRITICAL",
            dependencies=["ast_storage_ebs", "ast_net_vpc"],
            recovery_priority=1,
            recovery_strategy="RESTORE_FROM_BACKUP",
            backup_strategy="CONTINUOUS_WAL_AND_DAILY_SNAPSHOT",
            redundancy="MULTI_AZ",
            last_validation=datetime.now(timezone.utc).isoformat(),
            current_health="HEALTHY",
        )
        a2 = ResilienceAssetDTO(
            asset_id="ast_redis_cache",
            tenant_id="default_tenant",
            asset_type="STORAGE",
            name="Session & RateLimit Redis Cluster",
            criticality="HIGH",
            dependencies=["ast_net_vpc"],
            recovery_priority=2,
            recovery_strategy="REPLICATE",
            backup_strategy="HOURLY_RDB",
            redundancy="MULTI_AZ",
            last_validation=datetime.now(timezone.utc).isoformat(),
            current_health="HEALTHY",
        )
        a3 = ResilienceAssetDTO(
            asset_id="ast_api_gateway",
            tenant_id="default_tenant",
            asset_type="APPLICATION",
            name="Core API Gateway Pods",
            criticality="CRITICAL",
            dependencies=["ast_pg_primary", "ast_redis_cache"],
            recovery_priority=3,
            recovery_strategy="FAILOVER",
            redundancy="ACTIVE_ACTIVE",
            last_validation=datetime.now(timezone.utc).isoformat(),
            current_health="HEALTHY",
        )
        for a in [a1, a2, a3]:
            self._assets[a.asset_id] = a

        # Default Business Services
        s1 = BusinessServiceDTO(
            service_id="svc_checkout_api",
            tenant_id="default_tenant",
            name="Enterprise Checkout & Payments",
            criticality="CRITICAL",
            dependencies=["svc_auth_iam", "svc_ledger_db"],
            supporting_assets=["ast_api_gateway", "ast_pg_primary", "ast_redis_cache"],
            recovery_priority=1,
            target_RTO_minutes=30,
            target_RPO_minutes=15,
            validation_requirements=["SYNTHETIC_LOGIN", "SYNTHETIC_TRANSACTION"],
            current_status="OPERATIONAL",
        )
        self._services[s1.service_id] = s1

    def register_asset(self, asset: ResilienceAssetDTO) -> ResilienceAssetDTO:
        self._assets[asset.asset_id] = asset
        return asset

    def get_asset(self, asset_id: str) -> Optional[ResilienceAssetDTO]:
        return self._assets.get(asset_id)

    def list_assets(self, tenant_id: str = "default_tenant") -> List[ResilienceAssetDTO]:
        return [a for a in self._assets.values() if a.tenant_id == tenant_id or a.tenant_id == "default_tenant"]

    def register_business_service(self, svc: BusinessServiceDTO) -> BusinessServiceDTO:
        self._services[svc.service_id] = svc
        return svc

    def get_business_service(self, service_id: str) -> Optional[BusinessServiceDTO]:
        return self._services.get(service_id)

    def list_business_services(self, tenant_id: str = "default_tenant") -> List[BusinessServiceDTO]:
        return [s for s in self._services.values() if s.tenant_id == tenant_id or s.tenant_id == "default_tenant"]
