"""
TruthShield X — Intelligence Sharing Policy Engine (Phase 16).

Evaluates ABAC and RBAC policies, enforces data classification rules,
and guarantees that explicit DENY overrides any ALLOW rule.
"""

from typing import Dict, List, Optional, Any
from datetime import datetime, timezone
import uuid

from app.schemas.collective_defense_models import (
    ThreatIntelligenceObjectDTO,
    SharingPolicyEvaluationDTO,
    DataClassificationLiteral,
)


class IntelligenceSharingPolicyEngine:
    """ABAC/RBAC Sharing Policy Evaluator with strict explicit DENY precedence."""

    def __init__(self):
        # tenant_id -> list of registered consent/authorization rules
        self._tenant_consents: Dict[str, Dict[str, Any]] = {}
        # Explicit deny lists
        self._explicit_denials: List[Dict[str, Any]] = []

    def register_tenant_consent(
        self,
        tenant_id: str,
        allowed_classifications: List[DataClassificationLiteral],
        allow_global_sharing: bool = True,
        jurisdiction: str = "GLOBAL",
    ) -> str:
        """Registers a tenant's explicit opt-in sharing policy."""
        consent_id = f"cst_{uuid.uuid4().hex[:8]}"
        self._tenant_consents[tenant_id] = {
            "consent_id": consent_id,
            "allowed_classifications": allowed_classifications,
            "allow_global_sharing": allow_global_sharing,
            "jurisdiction": jurisdiction,
            "registered_at": datetime.now(timezone.utc).isoformat(),
        }
        return consent_id

    def add_explicit_deny_rule(self, condition_type: str, match_value: str, reason: str) -> None:
        """Adds an explicit DENY rule that overrides all permissions."""
        self._explicit_denials.append({
            "type": condition_type,
            "value": match_value.lower(),
            "reason": reason,
        })

    def evaluate_sharing(
        self,
        obj: ThreatIntelligenceObjectDTO,
        destination: str = "GLOBAL_FEDERATION",
        purpose: str = "THREAT_DEFENSE",
    ) -> SharingPolicyEvaluationDTO:
        """Evaluates whether an intelligence object may be shared."""
        # 1. Check Explicit Denials first (Section 14, 67 - Explicit DENY overrides ALLOW)
        for deny in self._explicit_denials:
            if deny["type"] == "TENANT" and deny["value"] == obj.tenant_id.lower():
                return SharingPolicyEvaluationDTO(
                    intelligence_id=obj.intelligence_id,
                    tenant_id=obj.tenant_id,
                    decision="DENY",
                    reason=f"Explicit Tenant Deny: {deny['reason']}",
                    explicit_deny_triggered=True,
                )
            if deny["type"] == "INDICATOR" and deny["value"] in obj.canonical_identifier.lower():
                return SharingPolicyEvaluationDTO(
                    intelligence_id=obj.intelligence_id,
                    tenant_id=obj.tenant_id,
                    decision="DENY",
                    reason=f"Explicit Indicator Deny: {deny['reason']}",
                    explicit_deny_triggered=True,
                )

        # 2. Classification-based checks
        if obj.classification == "HIGHLY_RESTRICTED":
            return SharingPolicyEvaluationDTO(
                intelligence_id=obj.intelligence_id,
                tenant_id=obj.tenant_id,
                decision="DENY",
                reason="HIGHLY_RESTRICTED intelligence cannot be shared externally.",
                explicit_deny_triggered=True,
            )

        if obj.classification == "CONFIDENTIAL":
            # Requires explicit consent and privacy transformation
            consent = self._tenant_consents.get(obj.tenant_id)
            if not consent or "CONFIDENTIAL" not in consent.get("allowed_classifications", []):
                return SharingPolicyEvaluationDTO(
                    intelligence_id=obj.intelligence_id,
                    tenant_id=obj.tenant_id,
                    decision="DENY",
                    reason="Tenant has not authorized sharing of CONFIDENTIAL intelligence.",
                )
            return SharingPolicyEvaluationDTO(
                intelligence_id=obj.intelligence_id,
                tenant_id=obj.tenant_id,
                decision="REDACT_AND_ALLOW",
                reason="CONFIDENTIAL intelligence authorized for sharing with mandatory redaction.",
                consent_id=consent.get("consent_id"),
            )

        if obj.classification in ("PUBLIC", "SHARED_THREAT_INTELLIGENCE", "INTERNAL"):
            consent = self._tenant_consents.get(obj.tenant_id, {})
            return SharingPolicyEvaluationDTO(
                intelligence_id=obj.intelligence_id,
                tenant_id=obj.tenant_id,
                decision="ALLOW",
                reason="Standard threat intelligence authorized for sharing.",
                consent_id=consent.get("consent_id"),
            )

        return SharingPolicyEvaluationDTO(
            intelligence_id=obj.intelligence_id,
            tenant_id=obj.tenant_id,
            decision="DENY",
            reason="Unrecognized classification state.",
        )
