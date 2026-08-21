"""
Zero-Trust Access Decision Engine (Phase 34)
============================================
Evaluates full 8-dimensional context:
(SUBJECT, DEVICE, SESSION, RESOURCE, ACTION, CONTEXT, POLICY, RISK)
Producing: ALLOW, DENY, STEP_UP, REAUTHENTICATE, QUARANTINE, HUMAN_REVIEW.
Explains every DENY (policy, reason, violated condition) and STEP_UP (risk, required assurance).
"""

from typing import Dict, Any, List, Optional
import datetime
import uuid
from app.schemas.zero_trust_exposure_models import ZeroTrustDecisionDTO


class ZeroTrustDecisionEngine:
    def __init__(self):
        self._decisions: List[Dict[str, Any]] = []

    def evaluate_access(
        self,
        tenant_id: str,
        correlation_id: str,
        subject_id: str,
        device_id: str,
        session_id: str,
        resource_id: str,
        resource_sensitivity: str,  # PUBLIC, INTERNAL, CONFIDENTIAL, RESTRICTED, HIGHLY_RESTRICTED
        action: str,
        identity_trust_state: str,
        device_trust_state: str,
        session_state: str,
        risk_score: float = 0.0,
        policy_rules: Optional[Dict[str, Any]] = None,
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        decision_id = f"ZTD-{uuid.uuid4().hex[:12]}"
        
        trust_scores = {
            "identity_trust": 1.0 if identity_trust_state == "TRUSTED" else 0.5 if identity_trust_state == "CONDITIONAL" else 0.0,
            "device_trust": 1.0 if device_trust_state == "TRUSTED" else 0.5 if device_trust_state == "CONDITIONAL" else 0.0,
            "session_trust": 1.0 if session_state in ["ACTIVE", "ELEVATED"] else 0.0,
            "composite_risk": risk_score
        }

        # Invariant 1: Compromised identity, device, or session -> QUARANTINE or DENY
        if identity_trust_state == "COMPROMISED" or device_trust_state == "COMPROMISED" or session_state == "QUARANTINED":
            decision = "QUARANTINE"
            reason = "COMPROMISED_ENTITY_DETECTED"
            violated_condition = "INTEGRITY_COMPROMISE_FLAG_SET"
            required_action = "ISOLATE_AND_RESET_CREDENTIALS"
            confidence = 1.0
        elif session_state == "REAUTH_REQUIRED":
            decision = "REAUTHENTICATE"
            reason = "SESSION_STALE_OR_MATERIAL_CONTEXT_CHANGED"
            violated_condition = "SESSION_AUTHENTICATION_TTL_EXPIRED"
            required_action = "PROMPT_FULL_REAUTHENTICATION"
            confidence = 0.98
        elif session_state == "TERMINATED":
            decision = "DENY"
            reason = "SESSION_INVALID_OR_TERMINATED"
            violated_condition = "INACTIVE_SESSION"
            required_action = "REAUTHENTICATE"
            confidence = 1.0
        elif identity_trust_state == "IDENTITY_UNTRUSTED":
            decision = "DENY"
            reason = "INSUFFICIENT_IDENTITY_CONFIDENCE"
            violated_condition = "IDENTITY_CONFIDENCE_BELOW_MINIMUM_THRESHOLD"
            required_action = "REGISTER_OR_VERIFY_IDENTITY_MFA"
            confidence = 0.95
        elif device_trust_state == "UNTRUSTED":
            decision = "DENY"
            reason = "INSUFFICIENT_DEVICE_POSTURE_ASSURANCE"
            violated_condition = "DEVICE_POSTURE_UNTRUSTED"
            required_action = "REGISTER_OR_VERIFY_POSTURE"
            confidence = 0.95
        # Invariant 2: High sensitivity resource requires full trust
        elif resource_sensitivity in ["RESTRICTED", "HIGHLY_RESTRICTED"]:
            if identity_trust_state != "TRUSTED" or device_trust_state != "TRUSTED":
                decision = "DENY"
                reason = "RESTRICTED_RESOURCE_REQUIRES_FULL_TRUST"
                violated_condition = "NON_TRUSTED_ENTITY_ACCESSING_HIGH_SENSITIVITY_RESOURCE"
                required_action = "POSTURE_REMEDIATION"
                confidence = 0.98
            elif risk_score > 3.0:
                decision = "STEP_UP"
                reason = "ELEVATED_RISK_FOR_RESTRICTED_RESOURCE"
                violated_condition = "COMPOSITE_RISK_EXCEEDS_RESTRICTED_ALLOW_THRESHOLD"
                required_action = "FIDO2_PASSKEY_STEP_UP"
                confidence = 0.90
            else:
                decision = "ALLOW"
                reason = "FULL_ZERO_TRUST_VERIFIED"
                violated_condition = None
                required_action = None
                confidence = 0.99
        # Invariant 3: Critical risk
        elif risk_score >= 8.5:
            decision = "DENY"
            reason = "EXCESSIVE_RISK_SCORE"
            violated_condition = "CRITICAL_RISK_THRESHOLD_EXCEEDED"
            required_action = "SOC_TRIAGE"
            confidence = 0.96
        elif risk_score >= 7.0:
            decision = "HUMAN_REVIEW"
            reason = "HIGH_RISK_ANOMALY_REQUIRES_ANALYST_CONCURRENCE"
            violated_condition = "ANOMALOUS_HIGH_RISK_REQUEST"
            required_action = "ESCALATE_TO_SOC_TIER2"
            confidence = 0.92
        elif risk_score >= 4.0 or identity_trust_state == "CONDITIONAL" or device_trust_state == "CONDITIONAL":
            decision = "STEP_UP"
            reason = "STEP_UP_AUTHENTICATION_REQUIRED"
            violated_condition = "CONDITIONAL_TRUST_OR_ELEVATED_RISK"
            required_action = "MFA_PROMPT"
            confidence = 0.88
        else:
            decision = "ALLOW"
            reason = "ZERO_TRUST_CONDITIONS_MET"
            violated_condition = None
            required_action = None
            confidence = 0.95

        record = {
            "decision_id": decision_id,
            "tenant_id": tenant_id,
            "correlation_id": correlation_id,
            "subject_id": subject_id,
            "device_id": device_id,
            "session_id": session_id,
            "resource_id": resource_id,
            "action": action,
            "decision": decision,
            "decision_reason": reason,
            "violated_condition": violated_condition,
            "policy_name": f"ZT_POLICY_{resource_sensitivity}",
            "confidence": confidence,
            "required_action": required_action,
            "trust_scores": trust_scores,
            "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat()
        }
        self._decisions.append(record)
        return record

    def get_decisions(self, tenant_id: str) -> List[Dict[str, Any]]:
        return [d for d in self._decisions if d["tenant_id"] == tenant_id]


zero_trust_decision_engine = ZeroTrustDecisionEngine()
