"""
TruthShield X — Early Warning Intelligence Engine
"""

import uuid
from typing import Dict, List, Optional, Any
from datetime import datetime, timezone
from app.schemas.hunting_models import EarlyWarningDTO, WarningLevelLiteral


class EarlyWarningEngine:
    """Correlates multiple disparate weak signals to issue calibrated early-warning notices."""

    def __init__(self):
        # warning_id -> EarlyWarningDTO
        self._warnings: Dict[str, EarlyWarningDTO] = {}

    def evaluate_weak_signals(
        self,
        target_subject: str,
        signals: List[Dict[str, Any]],
        affected_assets: Optional[List[str]] = None,
        tenant_id: str = "default_tenant",
    ) -> Optional[EarlyWarningDTO]:
        """Correlates subtle weak signals into an early warning indicator."""
        if len(signals) < 2:
            return None  # Insufficient weak signal convergence

        signal_titles = [s.get("title", s.get("type", "Signal")) for s in signals]
        signal_count = len(signals)

        # Calibrated warning level
        if signal_count >= 4:
            level: WarningLevelLiteral = "HIGH"
            conf = 0.88
        elif signal_count >= 3:
            level = "ELEVATED"
            conf = 0.78
        else:
            level = "WATCH"
            conf = 0.65

        warning_id = f"wrn_{uuid.uuid4().hex[:10]}"
        warning = EarlyWarningDTO(
            warning_id=warning_id,
            tenant_id=tenant_id,
            title=f"Early Warning: {level} signal convergence on '{target_subject}'",
            warning_level=level,
            confidence=conf,
            contributing_signals=signal_titles,
            affected_assets=affected_assets or [target_subject],
            predicted_impact="Potential precursor to targeted credential redirection and infrastructure staging.",
            recommended_investigation="Validate newly observed TLS certificate and query DNS passive history.",
            issued_at=datetime.now(timezone.utc).isoformat(),
        )

        self._warnings[warning_id] = warning
        return warning

    def list_warnings(self, tenant_id: str = "default_tenant") -> List[EarlyWarningDTO]:
        """Lists active early warnings for tenant."""
        return [w for w in self._warnings.values() if w.tenant_id == tenant_id]
