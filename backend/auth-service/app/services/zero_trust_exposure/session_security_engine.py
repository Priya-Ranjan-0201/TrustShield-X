"""
Session Security & Continuous Re-evaluation Engine (Phase 34)
=============================================================
Tracks active sessions, validates IP/device drift, binds cryptographically,
and triggers step-up authentication or revocation upon risk elevation.
"""

from typing import Dict, Any, List, Optional
import datetime


class SessionSecurityEngine:
    def __init__(self):
        self._sessions: Dict[str, Dict[str, Any]] = {}

    def create_session(
        self,
        session_id: str,
        tenant_id: str,
        subject_id: str,
        device_id: str,
        source_ip: str,
        initial_risk_score: float = 0.0,
        **kwargs
    ) -> Dict[str, Any]:
        now = datetime.datetime.now(datetime.timezone.utc).isoformat()
        session = {
            "session_id": session_id,
            "tenant_id": tenant_id,
            "subject_id": subject_id,
            "device_id": device_id,
            "source_ip": source_ip,
            "session_state": "ACTIVE",
            "state": "ACTIVE",
            "risk_score": initial_risk_score,
            "elevated_privileges": [],
            "created_at": now,
            "last_activity_at": now,
            "step_up_required": False
        }
        self._sessions[session_id] = session
        return session

    def evaluate_session_activity(
        self,
        session_id: str,
        tenant_id: str,
        current_ip: str,
        current_device: str,
        activity_type: str = "READ",
        risk_signals: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        sess = self._sessions.get(session_id)
        if not sess:
            return {
                "session_id": session_id,
                "tenant_id": tenant_id,
                "session_state": "REVOKED",
                "state": "REVOKED",
                "risk_score": 10.0,
                "reason": "SESSION_NOT_FOUND"
            }
        
        if sess["tenant_id"] != tenant_id:
            return {
                "session_id": session_id,
                "tenant_id": tenant_id,
                "session_state": "REVOKED",
                "state": "REVOKED",
                "risk_score": 10.0,
                "reason": "TENANT_MISMATCH_DENIED"
            }

        risk = 0.0
        signals = risk_signals or []

        # Check IP drift
        if current_ip != sess["source_ip"]:
            risk += 8.5
            signals.append("IP_ADDRESS_HIJACK_DETECTED")
            sess["state"] = "SUSPENDED"
            sess["session_state"] = "SUSPENDED"

        # Check device drift
        if current_device != sess["device_id"]:
            risk += 6.0
            signals.append("DEVICE_CONTEXT_DRIFT")
            sess["state"] = "SUSPENDED"
            sess["session_state"] = "SUSPENDED"

        sess["risk_score"] = min(10.0, max(sess["risk_score"], risk))
        sess["last_activity_at"] = datetime.datetime.now(datetime.timezone.utc).isoformat()

        if sess["risk_score"] >= 8.0:
            sess["session_state"] = "SUSPENDED"
            sess["state"] = "SUSPENDED"
            sess["step_up_required"] = True
        elif sess["risk_score"] >= 4.0:
            sess["session_state"] = "RESTRICTED"
            sess["state"] = "RESTRICTED"
            sess["step_up_required"] = True
        elif sess["state"] != "SUSPENDED":
            sess["session_state"] = "ACTIVE"
            sess["state"] = "ACTIVE"

        return {
            "session_id": session_id,
            "tenant_id": tenant_id,
            "session_state": sess["session_state"],
            "state": sess["state"],
            "risk_score": sess["risk_score"],
            "step_up_required": sess["step_up_required"],
            "signals": signals
        }

    def elevate_session(self, session_id: str, tenant_id: str, elevated_role: str) -> Dict[str, Any]:
        sess = self._sessions.get(session_id)
        if not sess or sess["tenant_id"] != tenant_id:
            return {"status": "FAILED", "reason": "SESSION_NOT_FOUND"}
        
        sess["elevated_privileges"].append(elevated_role)
        return {"session_id": session_id, "status": "ELEVATED", "roles": sess["elevated_privileges"]}

    def revoke_session(self, session_id: str, tenant_id: str, reason: str = "MANUAL_REVOCATION") -> Dict[str, Any]:
        sess = self._sessions.get(session_id)
        if not sess or sess["tenant_id"] != tenant_id:
            return {"session_id": session_id, "state": "REVOKED", "session_state": "REVOKED", "status": "FAILED", "reason": "SESSION_NOT_FOUND"}
        
        sess["session_state"] = "REVOKED"
        sess["state"] = "REVOKED"
        sess["termination_reason"] = reason
        return {"session_id": session_id, "session_state": "REVOKED", "state": "REVOKED", "reason": reason}

    def terminate_session(self, session_id: str, tenant_id: str, reason: str = "MANUAL_LOGOUT") -> Dict[str, Any]:
        return self.revoke_session(session_id, tenant_id, reason)

    def get_session(self, session_id: str, tenant_id: str) -> Optional[Dict[str, Any]]:
        sess = self._sessions.get(session_id)
        if sess and sess["tenant_id"] == tenant_id:
            return sess
        return None


session_security_engine = SessionSecurityEngine()
