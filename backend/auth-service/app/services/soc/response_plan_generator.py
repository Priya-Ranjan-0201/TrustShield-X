"""
TruthShield X — Response Plan Generator (Phase 21).

Generates multi-step, verified response plans with safety constraints and rollback steps.
"""

from typing import List, Dict, Optional
from datetime import datetime, timezone
from app.schemas.autonomous_soc_models import ResponsePlanDetailedDTO


class ResponsePlanGenerator:
    """Generates structured response plans with safety guarantees."""

    def __init__(self):
        self._protected_infrastructure = ["srv_truthshield_db", "srv_audit_ledger", "srv_iam_root", "127.0.0.1", "localhost"]

    def generate_plan(
        self,
        incident_id: str,
        target_resource: str,
        threat_type: str = "MALWARE_CONTAINMENT",
    ) -> ResponsePlanDetailedDTO:
        # Check protected targets
        is_safe = target_resource.lower() not in self._protected_infrastructure

        steps = [
            f"1. Dry-run digital twin simulation for {target_resource}",
            f"2. Obtain Tier-2 Four-Eyes authorization",
            f"3. Apply network quarantine security group to {target_resource}",
            f"4. Empirically verify network drop rules with cloud provider API",
        ]

        rollbacks = [
            f"1. Revert security group to baseline config for {target_resource}",
            "2. Verify outbound connectivity restoration",
        ]

        return ResponsePlanDetailedDTO(
            incident_id=incident_id,
            objective=f"Eradicate and contain {threat_type} spreading from {target_resource}.",
            steps=steps,
            target=target_resource,
            expected_outcome="Isolate lateral movement without affecting core checkout pipeline.",
            risk_score=15.0 if is_safe else 99.0,
            rollback_steps=rollbacks,
            verification_method="QUERY_PROVIDER_API",
            required_approval_tier="TIER_2_FOUR_EYES",
            is_safe=is_safe,
            created_at=datetime.now(timezone.utc).isoformat(),
        )
