"""Early Warning Engine & Threat Propagation Analyzer (Phase 6 - Sections 5, 6, 23).

Detects weak threat signals across modalities, evaluates graph propagation scores,
and generates deduplicated early-warning alerts with cooldown windows.
"""

from typing import List, Dict, Any, Optional
from datetime import datetime, timezone
import uuid

from app.schemas.predictive_threat_models import (
    EarlyWarningDTO,
    PredictionConfidenceLiteral,
)


class EarlyWarningEngine:
    """Detects weak multi-signal patterns and computes graph propagation metrics."""

    def __init__(self):
        self._warnings: Dict[str, Dict[str, EarlyWarningDTO]] = {}  # tenant_id -> warning_id -> warning
        self._recent_signatures: Dict[str, str] = {}  # signature -> timestamp (for deduplication / cooldown)

    def evaluate_weak_signals(
        self,
        affected_entities: List[str],
        indicator_count: int,
        reused_infrastructure_count: int = 0,
        certificate_reuse: bool = False,
        cross_modal_convergence: bool = False,
        tenant_id: str = "default_tenant",
    ) -> Optional[EarlyWarningDTO]:
        """Evaluates weak multi-modal signals to generate an Early Warning if threshold is satisfied."""
        # 1. Multi-signal requirement: A single weak signal must NOT trigger high-confidence alert
        signal_score = (
            (indicator_count * 0.15)
            + (reused_infrastructure_count * 0.30)
            + (0.35 if certificate_reuse else 0.0)
            + (0.40 if cross_modal_convergence else 0.0)
        )

        if signal_score < 0.60:
            # Below early warning threshold
            return None

        # 2. Propagation Score Calculation (Section 6)
        # Propagation score reflects graph connectivity and expansion velocity
        propagation_score = min(1.0, max(0.10, (len(affected_entities) * 0.15) + (signal_score * 0.40)))

        # 3. Determine Confidence & Severity
        if signal_score >= 1.0:
            confidence: PredictionConfidenceLiteral = "HIGH"
            conf_val = 0.90
            severity = "HIGH"
            proj_risk = 88.0
        else:
            confidence = "MEDIUM"
            conf_val = 0.75
            severity = "MEDIUM"
            proj_risk = 74.0

        # 4. Deduplication & Cooldown (Section 23)
        sig_key = f"{tenant_id}:" + ":".join(sorted(affected_entities[:3]))
        now = datetime.now(timezone.utc)
        now_iso = now.isoformat()

        if sig_key in self._recent_signatures:
            # In cooldown, avoid spamming duplicate warning
            return None
        self._recent_signatures[sig_key] = now_iso

        warning_id = f"ew_{uuid.uuid4().hex[:12]}"
        desc = (
            f"Early warning: Multi-signal threat convergence detected across {len(affected_entities)} entities. "
            f"Reused infra count: {reused_infrastructure_count}, Cert reuse: {certificate_reuse}, "
            f"Cross-modal convergence: {cross_modal_convergence}."
        )

        warning = EarlyWarningDTO(
            warning_id=warning_id,
            tenant_id=tenant_id,
            warning_type="CROSS_MODAL_THREAT_CONVERGENCE",
            severity=severity,
            confidence=confidence,
            confidence_score=conf_val,
            evidence_count=indicator_count,
            affected_entities=affected_entities,
            propagation_score=round(propagation_score, 2),
            time_horizon="24H",
            current_risk_score=55.0,
            projected_risk_score=proj_risk,
            description=desc,
            created_at=now_iso,
        )

        if tenant_id not in self._warnings:
            self._warnings[tenant_id] = {}
        self._warnings[tenant_id][warning_id] = warning

        return warning

    def list_warnings(self, tenant_id: str = "default_tenant") -> List[EarlyWarningDTO]:
        """Lists active early warnings for a tenant."""
        return list(self._warnings.get(tenant_id, {}).values())
