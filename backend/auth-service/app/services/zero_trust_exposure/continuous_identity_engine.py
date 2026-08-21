"""
Continuous Identity Security Engine (Phase 34)
==============================================
Evaluates identity confidence continuously, tracks anomalies, impossible travel,
and enforces least privilege / identity trust state invariants.
"""

from typing import Dict, Any, List, Optional
import datetime


class ContinuousIdentityEngine:
    def __init__(self):
        self._identities: Dict[str, Dict[str, Any]] = {}

    def register_identity(
        self,
        identity_id: str,
        tenant_id: str,
        username: str,
        email: str,
        roles: Optional[List[str]] = None,
        permissions: Optional[List[str]] = None,
        mfa_enforced: bool = True
    ) -> Dict[str, Any]:
        profile = {
            "identity_id": identity_id,
            "tenant_id": tenant_id,
            "username": username,
            "email": email,
            "roles": roles or ["USER"],
            "permissions": permissions or ["read:data"],
            "risk_score": 0.0,
            "identity_trust_state": "TRUSTED",
            "mfa_enforced": mfa_enforced,
            "last_authenticated_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "known_devices": [],
            "anomalies": [],
            "created_at": datetime.datetime.now(datetime.timezone.utc).isoformat()
        }
        self._identities[identity_id] = profile
        return profile

    def evaluate_identity_confidence(
        self,
        identity_id: str,
        tenant_id: str,
        current_ip: str,
        device_id: Optional[str] = None,
        auth_context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        auth_context = auth_context or {}
        identity = self._identities.get(identity_id)
        if not identity:
            return {
                "identity_id": identity_id,
                "tenant_id": tenant_id,
                "trust_state": "IDENTITY_UNTRUSTED",
                "risk_score": 10.0,
                "reason": "IDENTITY_NOT_FOUND"
            }
        
        # Strict tenant isolation
        if identity["tenant_id"] != tenant_id:
            return {
                "identity_id": identity_id,
                "tenant_id": tenant_id,
                "trust_state": "IDENTITY_UNTRUSTED",
                "risk_score": 10.0,
                "reason": "TENANT_MISMATCH_DENIED"
            }

        risk_score = 0.0
        anomalies = []

        # Check device association if provided
        if device_id and device_id not in identity["known_devices"] and len(identity["known_devices"]) > 0:
            risk_score += 3.5
            anomalies.append("UNRECOGNIZED_DEVICE")

        # Impossible travel evaluation
        if auth_context.get("impossible_travel"):
            risk_score += 9.0
            anomalies.append("IMPOSSIBLE_TRAVEL_DETECTED")
        else:
            loc = auth_context.get("geo_location")
            last_loc = auth_context.get("last_geo_location")
            time_diff_hours = auth_context.get("time_diff_hours", 1.0)
            if loc and last_loc and loc != last_loc and time_diff_hours < 0.5:
                risk_score += 5.0
                anomalies.append("IMPOSSIBLE_TRAVEL_DETECTED")

        # Credential anomaly
        if auth_context.get("stolen_credential_signal"):
            risk_score += 8.0
            anomalies.append("CREDENTIAL_COMPROMISE_INDICATOR")

        identity["risk_score"] = min(10.0, risk_score)
        identity["anomalies"] = anomalies

        if risk_score >= 7.0:
            trust_state = "IDENTITY_UNTRUSTED"
        elif risk_score >= 3.0:
            trust_state = "CONDITIONAL"
        elif not identity.get("mfa_enforced", True):
            trust_state = "IDENTITY_UNTRUSTED"
        else:
            trust_state = "TRUSTED"

        identity["identity_trust_state"] = trust_state
        return {
            "identity_id": identity_id,
            "tenant_id": tenant_id,
            "trust_state": trust_state,
            "risk_score": identity["risk_score"],
            "anomalies": anomalies,
            "mfa_enforced": identity["mfa_enforced"]
        }

    def get_identity(self, identity_id: str, tenant_id: str) -> Optional[Dict[str, Any]]:
        identity = self._identities.get(identity_id)
        if identity and identity["tenant_id"] == tenant_id:
            return identity
        return None


continuous_identity_engine = ContinuousIdentityEngine()

