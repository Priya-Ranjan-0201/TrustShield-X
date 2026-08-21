"""
TruthShield X — False Positive Learning Engine (Phase 21).

Tracks false positive and confirmed benign outcomes with human verification before applying suppression rules.
"""

from typing import Dict, List, Optional
from datetime import datetime, timezone
from app.schemas.autonomous_soc_models import FalsePositiveRecordDTO


class FalsePositiveLearningEngine:
    """Manages learned false positive patterns without unsafe automatic suppression."""

    def __init__(self):
        self._records: Dict[str, FalsePositiveRecordDTO] = {}

    def record_outcome(
        self,
        rule_id: str,
        tenant_id: str,
        status: str,
        evidence_ids: List[str],
        patterns: List[str],
        human_validated: bool = True,
    ) -> FalsePositiveRecordDTO:
        rec = FalsePositiveRecordDTO(
            rule_id=rule_id,
            tenant_id=tenant_id,
            status=status,  # type: ignore
            evidence_ids=evidence_ids,
            learned_patterns=patterns,
            human_validated=human_validated,
            recorded_at=datetime.now(timezone.utc).isoformat(),
        )
        self._records[f"{tenant_id}:{rule_id}"] = rec
        return rec

    def is_suppressible(self, rule_id: str, tenant_id: str) -> bool:
        """Only suppresses if explicitly marked FALSE_POSITIVE and validated by a human operator."""
        rec = self._records.get(f"{tenant_id}:{rule_id}")
        return rec is not None and rec.status == "FALSE_POSITIVE" and rec.human_validated
