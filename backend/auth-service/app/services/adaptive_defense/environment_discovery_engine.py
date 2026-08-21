"""
TruthShield X — Environment Discovery & Snapshot Engine (Phase 17).

Continuously tracks tenant assets, identities, services, endpoints, and boundary controls.
"""

from typing import Dict, List, Optional
from datetime import datetime, timezone

from app.schemas.adaptive_defense_models import SecurityEnvironmentSnapshotDTO


class EnvironmentDiscoveryEngine:
    """Captures and versions continuous security environment snapshots."""

    def __init__(self):
        # tenant_id -> list of snapshot history
        self._snapshots: Dict[str, List[SecurityEnvironmentSnapshotDTO]] = {}

    def capture_snapshot(
        self,
        tenant_id: str,
        assets: Optional[List[str]] = None,
        services: Optional[List[str]] = None,
        identities: Optional[List[str]] = None,
        endpoints: Optional[List[str]] = None,
        apis: Optional[List[str]] = None,
        cloud_resources: Optional[List[str]] = None,
        network_boundaries: Optional[List[str]] = None,
        security_controls: Optional[List[str]] = None,
        vulnerabilities: Optional[List[str]] = None,
        exposures: Optional[List[str]] = None,
        active_threats: Optional[List[str]] = None,
    ) -> SecurityEnvironmentSnapshotDTO:
        """Captures a new immutable snapshot of the environment."""
        history = self._snapshots.setdefault(tenant_id, [])
        version = len(history) + 1

        snapshot = SecurityEnvironmentSnapshotDTO(
            tenant_id=tenant_id,
            assets=assets or ["srv-app-01", "srv-db-01", "gw-ingress-01"],
            services=services or ["api-auth", "api-payments", "api-users"],
            identities=identities or ["svc_account_runner", "admin_user", "analyst_carol"],
            endpoints=endpoints or ["https://api.trustshield.internal/v1"],
            apis=apis or ["/auth/login", "/payments/transfer"],
            cloud_resources=cloud_resources or ["aws:s3:trustshield-logs", "aws:rds:prod-db"],
            network_boundaries=network_boundaries or ["10.0.0.0/16", "vpc-prod-dmz"],
            security_controls=security_controls or ["WAF_SHIELD", "EDR_AGENT", "MFA_POLICY"],
            vulnerabilities=vulnerabilities or [],
            exposures=exposures or [],
            active_threats=active_threats or [],
            version=version,
        )

        history.append(snapshot)
        return snapshot

    def get_latest_snapshot(self, tenant_id: str = "default_tenant") -> Optional[SecurityEnvironmentSnapshotDTO]:
        history = self._snapshots.get(tenant_id, [])
        return history[-1] if history else None

    def list_snapshots(self, tenant_id: str = "default_tenant") -> List[SecurityEnvironmentSnapshotDTO]:
        return self._snapshots.get(tenant_id, [])
