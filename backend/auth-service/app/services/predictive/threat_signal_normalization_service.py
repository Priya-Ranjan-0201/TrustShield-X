"""Threat Signal Normalization & Indicator Lifecycle Service (Phase 6 - Sections 2, 4).

Normalizes multi-source threat signals and enforces indicator lifecycle (FIRST_SEEN -> ACTIVE -> STALE -> EXPIRED -> REVOKED -> REVALIDATED).
"""

from typing import List, Dict, Any, Optional
from datetime import datetime, timezone, timedelta
import uuid

from app.schemas.predictive_threat_models import (
    ThreatSignalDTO,
    IndicatorLifecycleStateLiteral,
)


class ThreatSignalNormalizationService:
    """Ingests and normalizes threat signals across modalities while enforcing indicator lifecycle."""

    def __init__(self):
        self._signals: Dict[str, Dict[str, ThreatSignalDTO]] = {}  # tenant_id -> signal_id -> signal

    def ingest_signal(
        self,
        signal_type: str,
        source: str,
        entity_id: str,
        confidence: float = 0.85,
        severity: str = "HIGH",
        provenance: Optional[Dict[str, Any]] = None,
        ttl_seconds: int = 86400,
        tenant_scope: str = "default_tenant",
    ) -> ThreatSignalDTO:
        """Normalizes and stores an incoming threat signal."""
        now = datetime.now(timezone.utc)
        now_iso = now.isoformat()
        expiration_iso = (now + timedelta(seconds=ttl_seconds)).isoformat()

        sig_id = f"sig_{uuid.uuid4().hex[:12]}"
        signal = ThreatSignalDTO(
            signal_id=sig_id,
            signal_type=signal_type.upper().strip(),
            source=source.strip(),
            timestamp=now_iso,
            entity_id=entity_id.strip(),
            confidence=min(1.0, max(0.0, confidence)),
            severity=severity.upper().strip(),
            provenance=provenance or {},
            tenant_scope=tenant_scope,
            lifecycle_state="FIRST_SEEN",
            ttl_seconds=ttl_seconds,
            first_seen=now_iso,
            last_seen=now_iso,
            expiration=expiration_iso,
        )

        if tenant_scope not in self._signals:
            self._signals[tenant_scope] = {}
        self._signals[tenant_scope][sig_id] = signal

        return signal

    def get_signals_for_entity(
        self,
        entity_id: str,
        tenant_scope: str = "default_tenant",
    ) -> List[ThreatSignalDTO]:
        """Retrieves all signals for an entity within tenant scope."""
        tenant_sigs = self._signals.get(tenant_scope, {}).values()
        return [s for s in tenant_sigs if s.entity_id == entity_id]

    def update_indicator_lifecycle(
        self,
        signal_id: str,
        new_state: IndicatorLifecycleStateLiteral,
        tenant_scope: str = "default_tenant",
    ) -> ThreatSignalDTO:
        """Transitions indicator lifecycle state explicitly."""
        tenant_sigs = self._signals.get(tenant_scope, {})
        sig = tenant_sigs.get(signal_id)
        if not sig:
            raise KeyError(f"Signal '{signal_id}' not found for tenant '{tenant_scope}'.")

        now_iso = datetime.now(timezone.utc).isoformat()
        updated_sig = ThreatSignalDTO(
            signal_id=sig.signal_id,
            signal_type=sig.signal_type,
            source=sig.source,
            timestamp=sig.timestamp,
            entity_id=sig.entity_id,
            confidence=sig.confidence,
            severity=sig.severity,
            provenance=sig.provenance,
            tenant_scope=sig.tenant_scope,
            lifecycle_state=new_state,
            ttl_seconds=sig.ttl_seconds,
            first_seen=sig.first_seen,
            last_seen=now_iso,
            expiration=sig.expiration,
        )

        tenant_sigs[signal_id] = updated_sig
        return updated_sig

    def evaluate_staleness_and_expiration(self, tenant_scope: str = "default_tenant") -> List[ThreatSignalDTO]:
        """Evaluates all signals against TTL to mark stale or expired indicators."""
        now = datetime.now(timezone.utc)
        tenant_sigs = self._signals.get(tenant_scope, {})
        updated = []

        for sig_id, sig in list(tenant_sigs.items()):
            exp_time = datetime.fromisoformat(sig.expiration)
            if now > exp_time and sig.lifecycle_state not in ("EXPIRED", "REVOKED"):
                updated_sig = self.update_indicator_lifecycle(sig_id, "EXPIRED", tenant_scope)
                updated.append(updated_sig)
            elif (exp_time - now).total_seconds() < (sig.ttl_seconds * 0.2) and sig.lifecycle_state == "ACTIVE":
                updated_sig = self.update_indicator_lifecycle(sig_id, "STALE", tenant_scope)
                updated.append(updated_sig)

        return updated
