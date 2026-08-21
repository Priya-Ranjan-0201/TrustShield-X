"""
TruthShield X — Digital Security Twin Management Service
"""

import uuid
from typing import Dict, List, Optional, Any
from datetime import datetime, timezone
from app.schemas.simulation_models import (
    DigitalSecurityTwinDTO,
    SecurityControlDTO,
    TwinTypeLiteral,
    TwinStateLiteral,
)
from app.services.simulation.environment_execution_guard import EnvironmentExecutionGuard


class DigitalSecurityTwinService:
    """Manages creation, snapshotting, versioning, and state transitions of isolated Digital Security Twins."""

    def __init__(self, guard: Optional[EnvironmentExecutionGuard] = None):
        self.guard = guard or EnvironmentExecutionGuard()
        # twin_id -> DigitalSecurityTwinDTO
        self._twins: Dict[str, DigitalSecurityTwinDTO] = {}

    def create_twin_from_snapshot(
        self,
        source_snapshot_id: str,
        raw_assets: List[Dict[str, Any]],
        twin_type: TwinTypeLiteral = "BASELINE_TWIN",
        tenant_id: str = "default_tenant",
        created_by: str = "security_architect",
    ) -> DigitalSecurityTwinDTO:
        """Creates an isolated Digital Security Twin with synthesized sensitive fields."""
        twin_id = f"twn_{uuid.uuid4().hex[:10]}"

        # Synthesize all sensitive asset metadata
        sanitized_assets = []
        for asset in raw_assets:
            clean_asset = dict(asset)
            if "api_key" in clean_asset:
                clean_asset["api_key"] = self.guard.synthesize_credentials(str(clean_asset["api_key"]))
            if "private_ip" in clean_asset:
                clean_asset["private_ip"] = "192.0.2.100"  # RFC 5737 TEST-NET-1
            sanitized_assets.append(clean_asset)

        # Baseline security controls
        controls = [
            SecurityControlDTO(
                control_id="ctrl_waf_01",
                name="Cloudflare Edge WAF",
                control_type="WAF",
                modeled_effectiveness=0.88,
                observed_effectiveness=0.85,
            ),
            SecurityControlDTO(
                control_id="ctrl_mfa_01",
                name="FIDO2 / WebAuthn MFA",
                control_type="MFA",
                modeled_effectiveness=0.98,
                observed_effectiveness=0.96,
            ),
            SecurityControlDTO(
                control_id="ctrl_edr_01",
                name="Enterprise EDR Agent",
                control_type="EDR",
                modeled_effectiveness=0.82,
                observed_effectiveness=0.79,
            ),
        ]

        twin = DigitalSecurityTwinDTO(
            twin_id=twin_id,
            tenant_id=tenant_id,
            version=1,
            twin_type=twin_type,
            environment="SIMULATION",
            state="NORMAL",
            source_snapshot_id=source_snapshot_id,
            modeled_assets=sanitized_assets,
            modeled_controls=controls,
            baseline_risk_score=28.0,
            simulated_risk_score=28.0,
            created_at=datetime.now(timezone.utc).isoformat(),
            created_by=created_by,
        )

        self._twins[twin_id] = twin
        return twin

    def transition_state(
        self,
        twin_id: str,
        new_state: TwinStateLiteral,
        simulated_risk_score: Optional[float] = None,
    ) -> DigitalSecurityTwinDTO:
        """Transitions twin state deterministically within the simulation sandbox."""
        twin = self._twins.get(twin_id)
        if not twin:
            raise KeyError(f"Digital Security Twin '{twin_id}' not found.")

        twin.state = new_state
        if simulated_risk_score is not None:
            twin.simulated_risk_score = simulated_risk_score
        twin.version += 1
        return twin

    def get_twin(self, twin_id: str, tenant_id: Optional[str] = None) -> Optional[DigitalSecurityTwinDTO]:
        """Retrieves twin ensuring tenant isolation if tenant_id is supplied."""
        twin = self._twins.get(twin_id)
        if not twin:
            return None
        if tenant_id is not None and twin.tenant_id != tenant_id:
            return None
        return twin

    def list_twins(self, tenant_id: str = "default_tenant") -> List[DigitalSecurityTwinDTO]:
        """Lists twins belonging to the requesting tenant."""
        return [t for t in self._twins.values() if t.tenant_id == tenant_id]
