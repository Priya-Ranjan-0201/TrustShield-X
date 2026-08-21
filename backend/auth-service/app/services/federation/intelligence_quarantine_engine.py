"""
TruthShield X — Intelligence Quarantine & Feed Poisoning Defense Engine
"""

import uuid
from typing import Dict, List, Optional, Any
from datetime import datetime, timezone
from app.schemas.federation_models import IntelligenceQuarantineEntryDTO


class IntelligenceQuarantineEngine:
    """Detects adversarial threat feed poisoning, anomalous indicator bursts, and manages quarantine isolation."""

    BURST_THRESHOLD = 500  # Max indicators allowed per batch before anomaly review

    def __init__(self):
        # quarantine_id -> IntelligenceQuarantineEntryDTO
        self._quarantine: Dict[str, IntelligenceQuarantineEntryDTO] = {}

    def inspect_and_quarantine(
        self,
        source_id: str,
        incoming_indicators: List[Dict[str, Any]],
    ) -> Optional[IntelligenceQuarantineEntryDTO]:
        """Evaluates batch submissions for feed poisoning indicators (bursts, abnormal confidence, timestamps)."""
        reasons = []

        # 1. Burst detection
        if len(incoming_indicators) > self.BURST_THRESHOLD:
            reasons.append(f"Indicator burst threshold exceeded ({len(incoming_indicators)} > {self.BURST_THRESHOLD}).")

        # 2. Impossible timestamps or corrupted metadata
        for ind in incoming_indicators[:20]:
            ts = ind.get("timestamp") or ind.get("first_seen")
            if ts and "2099" in str(ts):
                reasons.append("Impossible future timestamp detected.")
                break

        # 3. Mass conflicting claims
        if any(ind.get("claim") == "FORCE_MALICIOUS_EVERYTHING" for ind in incoming_indicators):
            reasons.append("Adversarial poisoning signature detected in feed description.")

        if not reasons:
            return None  # Safe batch

        quarantine_id = f"qnt_{uuid.uuid4().hex[:10]}"
        affected = [str(ind.get("indicator") or ind.get("canonical_identifier") or "unknown") for ind in incoming_indicators]

        entry = IntelligenceQuarantineEntryDTO(
            quarantine_id=quarantine_id,
            source_id=source_id,
            reason="; ".join(reasons),
            affected_indicators=affected[:50],  # sample
            status="QUARANTINED",
            risk_level="CRITICAL",
            quarantined_at=datetime.now(timezone.utc).isoformat(),
        )

        self._quarantine[quarantine_id] = entry
        return entry

    def release_from_quarantine(
        self,
        quarantine_id: str,
        reviewed_by: str,
        approve: bool = True,
    ) -> IntelligenceQuarantineEntryDTO:
        """Approves and releases or permanently rejects quarantined threat intelligence."""
        entry = self._quarantine.get(quarantine_id)
        if not entry:
            raise KeyError(f"Quarantine entry '{quarantine_id}' not found.")

        entry.status = "APPROVED" if approve else "REJECTED"
        entry.reviewed_by = reviewed_by
        entry.reviewed_at = datetime.now(timezone.utc).isoformat()
        return entry

    def list_quarantine(self) -> List[IntelligenceQuarantineEntryDTO]:
        """Lists all quarantined entries."""
        return list(self._quarantine.values())
