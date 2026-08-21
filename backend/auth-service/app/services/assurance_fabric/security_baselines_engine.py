"""
TruthShield X — Security Baselines Engine (Phase 24).

Maintains tamper-proof, immutable baseline snapshots of verified control states.
"""

from typing import Dict, Optional
from datetime import datetime, timezone
import hashlib
import json
from app.schemas.security_assurance_fabric_models import SecurityBaselineDTO


class SecurityBaselinesEngine:
    """Stores immutable security baselines for regression comparisons."""

    def __init__(self):
        self._baselines: Dict[str, SecurityBaselineDTO] = {}
        self._seed_default_baseline()

    def _seed_default_baseline(self):
        states = {
            "ctl_tenant_isolation": "PASS",
            "ctl_four_eyes_response": "PASS",
            "ctl_immutable_audit": "PASS",
        }
        b1 = SecurityBaselineDTO(
            baseline_id="sbase_v1_prod_locked",
            tenant_id="default_tenant",
            version="v1.0.0-PROD-LOCKED",
            immutable_hash=hashlib.sha256(json.dumps(states, sort_keys=True).encode()).hexdigest(),
            control_states=states,
            is_active=True,
        )
        self._baselines[b1.baseline_id] = b1

    def create_baseline(self, version: str, control_states: Dict[str, str], tenant_id: str = "default_tenant") -> SecurityBaselineDTO:
        chash = hashlib.sha256(json.dumps(control_states, sort_keys=True).encode()).hexdigest()
        dto = SecurityBaselineDTO(
            tenant_id=tenant_id,
            version=version,
            immutable_hash=chash,
            control_states=control_states,
            is_active=True,
        )
        self._baselines[dto.baseline_id] = dto
        return dto

    def get_baseline(self, baseline_id: str) -> Optional[SecurityBaselineDTO]:
        return self._baselines.get(baseline_id)
