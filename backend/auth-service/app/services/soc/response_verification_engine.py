"""Response Verification Engine (Phase 4.0 Part 7 — Section 47).

Empirically validates whether remediation actions actually succeeded before marking actions COMPLETED.
"""

from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime, timezone
from app.schemas.soc_operations_models import (
    ResponseActionDTO,
    ResponseVerificationDTO,
)
from app.services.soc.response_adapters import ResponseProviderAdapter, DNSResponseAdapter


class ResponseVerificationEngine:
    """Verifies actual post-action containment state."""

    def __init__(self, adapters: Optional[Dict[str, ResponseProviderAdapter]] = None):
        self._adapters = adapters or {}

    def verify_action(
        self,
        action: ResponseActionDTO,
        adapter: Optional[ResponseProviderAdapter] = None,
    ) -> Tuple[ResponseActionDTO, ResponseVerificationDTO]:
        provider = adapter or self._adapters.get(action.action_type, DNSResponseAdapter())

        ver_status, obs = provider.verify(action)

        if ver_status == "SUCCESS":
            action.status = "COMPLETED"
        else:
            action.status = "FAILED"
            action.error_code = "ERR_VERIFICATION_FAILED"

        verification_dto = ResponseVerificationDTO(
            action_id=action.action_id,
            target=action.target,
            verification_status=ver_status,
            evidence_gathered=[obs],
            observations=obs,
        )

        return action, verification_dto
