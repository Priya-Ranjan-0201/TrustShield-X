"""
TruthShield X — Security Configuration & Behavior Drift Engine
"""

import hashlib
import json
import uuid
from typing import Dict, List, Optional, Any
from datetime import datetime, timezone
from app.schemas.assurance_models import SecurityBaselineDTO, SecurityDriftDTO, DriftSeverityLiteral


class SecurityDriftEngine:
    """Monitors security baselines, hashes configurations, and detects unexpected drift."""

    def __init__(self):
        # baseline_id -> SecurityBaselineDTO
        self._baselines: Dict[str, SecurityBaselineDTO] = {}
        # drift_id -> SecurityDriftDTO
        self._drifts: Dict[str, SecurityDriftDTO] = {}

    def establish_baseline(
        self,
        baseline_id: str,
        parameters: Dict[str, Any],
        approved_by: str = "security_lead",
    ) -> SecurityBaselineDTO:
        """Establishes an approved, cryptographically hashed security baseline."""
        raw_bytes = json.dumps(parameters, sort_keys=True).encode("utf-8")
        config_hash = hashlib.sha256(raw_bytes).hexdigest()

        baseline = SecurityBaselineDTO(
            baseline_id=baseline_id,
            version=1,
            owner="chief_information_security_officer",
            approved_at=datetime.now(timezone.utc).isoformat(),
            approved_by=approved_by,
            configuration_hash=config_hash,
            parameters=parameters,
        )

        self._baselines[baseline_id] = baseline
        return baseline

    def evaluate_drift(
        self,
        baseline_id: str,
        control_id: str,
        current_parameters: Dict[str, Any],
    ) -> Optional[SecurityDriftDTO]:
        """Compares current configuration against baseline and flags drift."""
        baseline = self._baselines.get(baseline_id)
        if not baseline:
            raise KeyError(f"Baseline '{baseline_id}' not found.")

        current_bytes = json.dumps(current_parameters, sort_keys=True).encode("utf-8")
        current_hash = hashlib.sha256(current_bytes).hexdigest()

        if current_hash == baseline.configuration_hash:
            return None  # Baseline intact, no drift

        # Detect specific drift items
        diff_keys = [k for k in baseline.parameters if baseline.parameters.get(k) != current_parameters.get(k)]
        diff_keys += [k for k in current_parameters if k not in baseline.parameters]

        severity: DriftSeverityLiteral = "HIGH" if "mfa" in str(diff_keys).lower() or "rbac" in str(diff_keys).lower() else "MEDIUM"

        drift_id = f"drf_{uuid.uuid4().hex[:10]}"
        drift = SecurityDriftDTO(
            drift_id=drift_id,
            control_id=control_id,
            drift_type="CONFIGURATION_DRIFT",
            severity=severity,
            baseline_value=baseline.configuration_hash[:16],
            current_value=current_hash[:16],
            detected_at=datetime.now(timezone.utc).isoformat(),
            status="DETECTED",
            owner="secops_lead",
        )

        self._drifts[drift_id] = drift
        return drift

    def list_drifts(self) -> List[SecurityDriftDTO]:
        """Lists active security drifts."""
        return list(self._drifts.values())
