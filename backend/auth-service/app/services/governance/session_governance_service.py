"""Session Governance & Lifecycle Service (Phase 4.0 Part 8 — Sections 72-75, 100).

Manages active user sessions, device binding, session termination, and MFA state tracking.
"""

from typing import List, Dict, Any, Optional
import uuid
from datetime import datetime, timezone, timedelta
from app.schemas.governance_models import (
    SessionGovernanceDTO,
    SessionStatusLiteral,
)


class SessionGovernanceService:
    """Manages session states, revocation, and authentication strength."""

    def __init__(self):
        self._sessions: Dict[str, SessionGovernanceDTO] = {}

    def create_session(
        self,
        user_id: str,
        organization_id: str,
        authentication_strength: str = "PASSWORD",
        mfa_verified: bool = False,
        device_reference: str = "Corporate Laptop",
        ip_reference: str = "127.0.0.1",
        duration_hours: int = 8,
    ) -> SessionGovernanceDTO:
        now = datetime.now(timezone.utc)
        expires_at = (now + timedelta(hours=duration_hours)).isoformat()

        session = SessionGovernanceDTO(
            session_id=f"ses_{uuid.uuid4().hex[:12]}",
            user_id=user_id,
            organization_id=organization_id,
            authentication_strength=authentication_strength,
            mfa_verified=mfa_verified,
            device_reference=device_reference,
            ip_reference=ip_reference,
            status="ACTIVE",
            expires_at=expires_at,
        )
        self._sessions[session.session_id] = session
        return session

    def revoke_session(self, session_id: str) -> Optional[SessionGovernanceDTO]:
        session = self._sessions.get(session_id)
        if session:
            session.status = "REVOKED"
        return session

    def revoke_all_user_sessions(self, user_id: str) -> int:
        count = 0
        for s in self._sessions.values():
            if s.user_id == user_id and s.status == "ACTIVE":
                s.status = "REVOKED"
                count += 1
        return count

    def get_session(self, session_id: str) -> Optional[SessionGovernanceDTO]:
        session = self._sessions.get(session_id)
        if session and session.status == "ACTIVE":
            # Check expiry
            if datetime.fromisoformat(session.expires_at) < datetime.now(timezone.utc):
                session.status = "EXPIRED"
        return session

    def list_user_sessions(self, user_id: str) -> List[SessionGovernanceDTO]:
        return [s for s in self._sessions.values() if s.user_id == user_id]
