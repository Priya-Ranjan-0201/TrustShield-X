"""
TruthShield X — Exception Management Engine (Phase 32).

Governs security policy exceptions, automatically flagging expired exceptions as EXCEPTION_EXPIRED.
"""

from typing import Dict, List, Optional, Any
from datetime import datetime, timezone
from app.schemas.enterprise_governance_models import SecurityExceptionDTO


class ExceptionManagementEngine:
    """Manages policy exceptions with mandatory compensating controls and expiration enforcement."""

    def __init__(self):
        self._exceptions: Dict[str, SecurityExceptionDTO] = {}
        self._seed_default_exception()

    def _seed_default_exception(self):
        e1 = SecurityExceptionDTO(
            exception_id="exc_legacy_mainframe_probe",
            reason="Temporary bypass for legacy mainframe telemetry probe during migration",
            scope="Host probe 10.0.12.44",
            owner="INFRA_LEAD",
            compensating_controls=["Network micro-segmentation", "Deep packet inspection probe"],
            approved_by="CISO",
            expiration_date="2026-09-01T00:00:00Z",
            status="ACTIVE",
        )
        self._exceptions[e1.exception_id] = e1

    def inspect_exception_status(self, exception_id: str, current_time_iso: Optional[str] = None) -> Dict[str, Any]:
        e = self._exceptions.get(exception_id)
        if not e:
            raise ValueError(f"Exception '{exception_id}' not found.")

        # Check expiration
        now_str = current_time_iso or datetime.now(timezone.utc).isoformat()
        if now_str > e.expiration_date:
            return {
                "exception_id": exception_id,
                "status": "EXCEPTION_EXPIRED",
                "is_active": False,
                "reason": "EXPIRATION_DATE_REACHED",
            }

        return {
            "exception_id": exception_id,
            "status": "ACTIVE",
            "is_active": True,
            "reason": "WITHIN_APPROVED_TIMEFRAME",
        }

    def list_exceptions(self) -> List[SecurityExceptionDTO]:
        return list(self._exceptions.values())
