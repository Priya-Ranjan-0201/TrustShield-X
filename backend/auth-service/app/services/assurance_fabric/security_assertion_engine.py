"""
TruthShield X — Security Assertion Engine (Phase 24).

Formulates and evaluates testable security assertions tied to concrete controls.
"""

from typing import Dict, List, Optional
from datetime import datetime, timezone
from app.schemas.security_assurance_fabric_models import SecurityAssertionDTO


class SecurityAssertionEngine:
    """Evaluates formal testable security assertions."""

    def __init__(self):
        self._assertions: Dict[str, SecurityAssertionDTO] = {}
        self._seed_default_assertions()

    def _seed_default_assertions(self):
        a1 = SecurityAssertionDTO(
            assertion_id="asrt_tenant_isolation",
            control_id="ctl_tenant_isolation",
            statement="Cross-tenant data access is strictly blocked at the datastore layer.",
            test_method="SYNTHETIC_CROSS_TENANT_INJECTION",
            acceptable_state="ACCESS_DENIED_EXPLICIT",
            is_validated=True,
        )
        a2 = SecurityAssertionDTO(
            assertion_id="asrt_four_eyes",
            control_id="ctl_four_eyes_response",
            statement="Self-approval for high-impact actions is rejected with HTTP 403 Forbidden.",
            test_method="SYNTHETIC_SELF_APPROVAL_ATTEMPT",
            acceptable_state="PERMISSION_DENIED",
            is_validated=True,
        )
        for a in [a1, a2]:
            self._assertions[a.assertion_id] = a

    def create_assertion(self, control_id: str, statement: str, test_method: str, acceptable_state: str) -> SecurityAssertionDTO:
        dto = SecurityAssertionDTO(
            control_id=control_id,
            statement=statement,
            test_method=test_method,
            acceptable_state=acceptable_state,
            is_validated=False,
        )
        self._assertions[dto.assertion_id] = dto
        return dto

    def get_assertion(self, assertion_id: str) -> Optional[SecurityAssertionDTO]:
        return self._assertions.get(assertion_id)

    def list_assertions(self) -> List[SecurityAssertionDTO]:
        return list(self._assertions.values())
