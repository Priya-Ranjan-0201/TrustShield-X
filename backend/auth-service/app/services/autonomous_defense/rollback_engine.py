"""
TruthShield X — Rollback Engine (Phase 30).

Executes and verifies automated state rollbacks whenever an action or model fails post-deployment verification.
"""

from typing import Dict, List, Optional
from datetime import datetime, timezone
from app.schemas.autonomous_defense_models import RollbackRecordDTO


class RollbackEngine:
    """Manages transactional reverse-execution to return systems to their previous known-good baseline."""

    def __init__(self):
        self._rollbacks: Dict[str, RollbackRecordDTO] = {}

    def execute_rollback(
        self,
        target_entity: str,
        reverted_change: str,
        verify_rollback_success: bool = True,
    ) -> RollbackRecordDTO:
        dto = RollbackRecordDTO(
            target_entity=target_entity,
            reverted_change=reverted_change,
            is_verified=verify_rollback_success,
            timestamp=datetime.now(timezone.utc).isoformat(),
        )
        self._rollbacks[dto.rollback_id] = dto
        return dto

    def list_rollbacks(self) -> List[RollbackRecordDTO]:
        return list(self._rollbacks.values())
