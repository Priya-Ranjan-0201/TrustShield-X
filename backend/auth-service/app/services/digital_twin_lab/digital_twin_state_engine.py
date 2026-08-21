"""
TruthShield X — Digital Twin State Engine (Phase 26).

Manages Digital Twin states, versioned snapshots, branching, confidence evaluation, and dependency graphs.
"""

from typing import Dict, List, Optional, Any
from datetime import datetime, timezone
from app.schemas.digital_twin_lab_models import DigitalTwinStateDTO, TwinSnapshotBranchDTO


class DigitalTwinStateEngine:
    """Maintains immutable, versioned representations of the protected environment."""

    def __init__(self):
        self._states: Dict[str, DigitalTwinStateDTO] = {}
        self._branches: Dict[str, TwinSnapshotBranchDTO] = {}
        self._seed_default_state()

    def _seed_default_state(self):
        s1 = DigitalTwinStateDTO(
            state_id="twstate_v1_prod_sync",
            tenant_id="default_tenant",
            version="v1.0.0-PROD-SYNC",
            environment="PRODUCTION_MIRROR",
            assets=[
                {"id": "ast_api_gw", "type": "GATEWAY", "criticality": "CRITICAL"},
                {"id": "ast_auth_cluster", "type": "AUTH_SERVICE", "criticality": "CRITICAL"},
                {"id": "ast_postgres_primary", "type": "DATABASE", "criticality": "CRITICAL"},
            ],
            services=[
                {"id": "srv_auth", "name": "Authentication API", "status": "HEALTHY"},
                {"id": "srv_scan", "name": "Deepfake Scan Engine", "status": "HEALTHY"},
            ],
            identities=[
                {"id": "usr_admin", "role": "ADMIN", "mfa_enforced": True},
                {"id": "usr_analyst", "role": "SOC_ANALYST", "mfa_enforced": True},
            ],
            dependencies=[
                {"source": "ast_api_gw", "target": "ast_auth_cluster", "type": "NETWORK_ROUTE"},
                {"source": "ast_auth_cluster", "target": "ast_postgres_primary", "type": "DATASTORE_CONNECTION"},
            ],
            controls=[
                {"id": "ctl_tenant_isolation", "status": "ACTIVE", "validated": True},
                {"id": "ctl_four_eyes_response", "status": "ACTIVE", "validated": True},
            ],
            vulnerabilities=[],
            threats=[{"id": "threat_ap44", "name": "AP-44 Campaign", "severity": "HIGH"}],
            detections=[{"id": "rule_t1055", "name": "Reflective DLL Injection", "status": "ENABLED"}],
            playbooks=[{"id": "pb_isolate_host", "status": "READY"}],
            recovery_paths=[{"id": "rec_pg_failover", "rto_seconds": 120}],
            configurations={"tls_version": "TLS_1_3", "mfa_required": True},
            assumptions=["Real-time telemetry reflects active datastore mirrors"],
            freshness_status="FRESH",
            confidence_score=0.98,
        )
        self._states[s1.state_id] = s1

    def create_snapshot(
        self,
        version: str,
        assets: Optional[List[Dict[str, Any]]] = None,
        services: Optional[List[Dict[str, Any]]] = None,
        tenant_id: str = "default_tenant",
    ) -> DigitalTwinStateDTO:
        dto = DigitalTwinStateDTO(
            tenant_id=tenant_id,
            version=version,
            environment="PRODUCTION_MIRROR",
            assets=assets or self._states["twstate_v1_prod_sync"].assets,
            services=services or self._states["twstate_v1_prod_sync"].services,
            identities=self._states["twstate_v1_prod_sync"].identities,
            dependencies=self._states["twstate_v1_prod_sync"].dependencies,
            controls=self._states["twstate_v1_prod_sync"].controls,
            freshness_status="FRESH",
            confidence_score=0.98,
        )
        self._states[dto.state_id] = dto
        return dto

    def create_branch(self, parent_state_id: str, branch_name: str, hypothetical_changes: Dict[str, Any]) -> TwinSnapshotBranchDTO:
        if parent_state_id not in self._states:
            raise ValueError(f"Parent twin state '{parent_state_id}' not found.")
        dto = TwinSnapshotBranchDTO(
            parent_state_id=parent_state_id,
            branch_name=branch_name,
            hypothetical_changes=hypothetical_changes,
            created_at=datetime.now(timezone.utc).isoformat(),
            is_active=True,
        )
        self._branches[dto.branch_id] = dto
        return dto

    def get_state(self, state_id: str) -> Optional[DigitalTwinStateDTO]:
        return self._states.get(state_id)

    def get_branch(self, branch_id: str) -> Optional[TwinSnapshotBranchDTO]:
        return self._branches.get(branch_id)

    def list_states(self, tenant_id: str = "default_tenant") -> List[DigitalTwinStateDTO]:
        return [s for s in self._states.values() if s.tenant_id == tenant_id or s.tenant_id == "default_tenant"]
