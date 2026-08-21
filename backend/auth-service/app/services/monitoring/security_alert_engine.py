"""Security Alert Engine, Deduplication, Suppression & Lifecycle (Phase 4.0 Part 6 — Sections 33-45, 89).

Generates actionable alerts, calculates deterministic fingerprints, applies suppression rules,
manages lifecycle transitions, and enforces alert storm safeguards.
"""

from typing import List, Dict, Any, Optional, Tuple
import hashlib
import uuid
from datetime import datetime, timezone, timedelta
from app.schemas.continuous_intelligence_models import (
    SecurityAlertDTO,
    AlertFingerprintDTO,
    AlertSuppressionDTO,
    AlertAcknowledgementDTO,
    AlertEscalationDTO,
    IntelligenceChangeEventDTO,
    AlertPriorityLiteral,
    AlertSeverityLiteral,
    AlertStatusLiteral,
    AlertTypeLiteral,
)
from app.services.monitoring.intelligence_impact_engine import ImpactDecision

MAX_ALERTS_PER_ENTITY_PER_HOUR = 50


class SecurityAlertEngine:
    """Evaluates security events, generates deduplicated alerts, and enforces suppression and escalation."""

    def __init__(self):
        self._alerts: Dict[str, SecurityAlertDTO] = {}
        self._fingerprints: Dict[str, AlertFingerprintDTO] = {}
        self._suppressions: Dict[str, AlertSuppressionDTO] = {}
        self._rate_counters: Dict[str, Dict[str, Any]] = {}

    def compute_alert_fingerprint(self, alert_type: str, entity_id: str, case_id: Optional[str] = None) -> str:
        """Compute deterministic fingerprint hash for alert deduplication (Section 40)."""
        raw = f"{alert_type}:{entity_id}:{case_id or ''}"
        return hashlib.sha256(raw.encode()).hexdigest()

    def generate_alert(
        self,
        event: IntelligenceChangeEventDTO,
        impact: ImpactDecision,
        case_id: Optional[str] = None,
        analysis_id: Optional[str] = None,
        organization_id: Optional[str] = None,
    ) -> Optional[SecurityAlertDTO]:
        """Generate, deduplicate, and evaluate suppression for a security alert."""
        # Derive alert type and priority
        alert_type: AlertTypeLiteral = (
            "THREAT_RECLASSIFICATION" if event.event_type == "IOC_RECLASSIFIED"
            else "NEW_THREAT_MATCH" if event.event_type == "IOC_NEW"
            else "MALICIOUS_DOMAIN" if "domain" in event.provenance.lower()
            else "HIGH_IMPACT_CORRELATION"
        )

        priority: AlertPriorityLiteral = (
            "CRITICAL" if impact.impact_level == "CRITICAL_IMPACT"
            else "HIGH" if impact.impact_level == "HIGH_IMPACT"
            else "MEDIUM" if impact.impact_level == "MEDIUM_IMPACT"
            else "LOW"
        )

        severity: AlertSeverityLiteral = event.severity

        fingerprint = self.compute_alert_fingerprint(alert_type, event.entity_id, case_id)

        # 1. Alert Storm Rate Limiting Check (Section 89, 109)
        now = datetime.now(timezone.utc)
        rate_key = f"{event.entity_id}:{now.hour}"
        rate_rec = self._rate_counters.get(rate_key, {"count": 0, "hour": now.hour})
        if rate_rec["count"] >= MAX_ALERTS_PER_ENTITY_PER_HOUR:
            return None  # Suppressed due to alert storm threshold
        rate_rec["count"] += 1
        self._rate_counters[rate_key] = rate_rec

        # 2. Alert Suppression Check (Section 41-42)
        suppression = self._suppressions.get(fingerprint)
        if suppression and suppression.is_active:
            if suppression.expires_at and datetime.fromisoformat(suppression.expires_at) < now:
                suppression.is_active = False
            elif priority == "CRITICAL" and suppression.allow_critical_override:
                pass  # Critical alert overrides suppression (Section 42, Test 25)
            else:
                return None  # Suppressed

        # 3. Deduplication Check (Section 39)
        if fingerprint in self._fingerprints:
            fp_dto = self._fingerprints[fingerprint]
            fp_dto.occurrences += 1
            fp_dto.last_seen = now.isoformat()
            existing_alert = next((a for a in self._alerts.values() if a.alert_fingerprint == fingerprint), None)
            if existing_alert:
                if priority == "CRITICAL" and existing_alert.priority != "CRITICAL":
                    existing_alert.priority = "CRITICAL"
                    existing_alert.status = "NEW"
                return existing_alert


        # 4. Create New Alert
        alert = SecurityAlertDTO(
            alert_id=f"alt_{uuid.uuid4().hex[:12]}",
            case_id=case_id,
            analysis_id=analysis_id,
            event_id=event.event_id,
            alert_type=alert_type,
            title=f"Security Alert: {event.entity_id} — {alert_type.replace('_', ' ')}",
            description=impact.why_relevant,
            priority=priority,
            severity=severity,
            confidence=event.confidence,
            status="NEW",
            source=event.source,
            evidence_ids=[event.event_id],
            entity_ids=[event.entity_id],
            alert_fingerprint=fingerprint,
            organization_id=organization_id,
        )

        self._alerts[alert.alert_id] = alert
        self._fingerprints[fingerprint] = AlertFingerprintDTO(
            fingerprint_id=f"fp_{uuid.uuid4().hex[:12]}",
            fingerprint_hash=fingerprint,
            alert_type=alert_type,
            entity_id=event.entity_id,
            case_id=case_id,
        )

        return alert

    def acknowledge_alert(
        self,
        alert_id: str,
        user_id: str,
        user_name: str,
        reason: str,
        comment: Optional[str] = None,
    ) -> Tuple[SecurityAlertDTO, AlertAcknowledgementDTO]:
        """Acknowledge an alert and transition status to ACKNOWLEDGED (Section 44)."""
        alert = self._alerts.get(alert_id)
        if not alert:
            raise KeyError(f"Alert {alert_id} not found.")

        now_str = datetime.now(timezone.utc).isoformat()
        alert.status = "ACKNOWLEDGED"
        alert.acknowledged_at = now_str
        alert.updated_at = now_str

        ack = AlertAcknowledgementDTO(
            ack_id=f"ack_{uuid.uuid4().hex[:12]}",
            alert_id=alert_id,
            user_id=user_id,
            user_name=user_name,
            reason=reason,
            comment=comment,
            acknowledged_at=now_str,
        )
        return alert, ack

    def escalate_alert(
        self,
        alert_id: str,
        new_priority: AlertPriorityLiteral,
        reason: str,
        escalated_by: Optional[str] = None,
    ) -> Tuple[SecurityAlertDTO, AlertEscalationDTO]:
        """Escalate an alert priority (Section 45)."""
        alert = self._alerts.get(alert_id)
        if not alert:
            raise KeyError(f"Alert {alert_id} not found.")

        prev_p = alert.priority
        now_str = datetime.now(timezone.utc).isoformat()
        alert.priority = new_priority
        alert.status = "ESCALATED"
        alert.updated_at = now_str

        esc = AlertEscalationDTO(
            escalation_id=f"esc_{uuid.uuid4().hex[:12]}",
            alert_id=alert_id,
            previous_priority=prev_p,
            escalated_priority=new_priority,
            escalation_type="MANUAL" if escalated_by else "POLICY_TIMEOUT",
            reason=reason,
            escalated_by=escalated_by,
            escalated_at=now_str,
        )
        return alert, esc

    def suppress_alert(
        self,
        alert_id: str,
        reason: str,
        suppressed_by: str,
        duration_hours: int = 24,
        allow_critical_override: bool = True,
    ) -> Tuple[SecurityAlertDTO, AlertSuppressionDTO]:
        """Apply temporary suppression to alert fingerprint (Section 41)."""
        alert = self._alerts.get(alert_id)
        if not alert:
            raise KeyError(f"Alert {alert_id} not found.")

        now = datetime.now(timezone.utc)
        expires_at = (now + timedelta(hours=duration_hours)).isoformat()
        alert.status = "SUPPRESSED"
        alert.suppressed_until = expires_at
        alert.updated_at = now.isoformat()

        supp = AlertSuppressionDTO(
            suppression_id=f"sup_{uuid.uuid4().hex[:12]}",
            alert_fingerprint=alert.alert_fingerprint,
            alert_type=alert.alert_type,
            reason=reason,
            suppressed_by=suppressed_by,
            expires_at=expires_at,
            allow_critical_override=allow_critical_override,
        )
        self._suppressions[alert.alert_fingerprint] = supp
        return alert, supp

    def resolve_alert(self, alert_id: str, resolution_note: str = "") -> SecurityAlertDTO:
        """Resolve alert and mark RESOLVED."""
        alert = self._alerts.get(alert_id)
        if not alert:
            raise KeyError(f"Alert {alert_id} not found.")

        now_str = datetime.now(timezone.utc).isoformat()
        alert.status = "RESOLVED"
        alert.resolved_at = now_str
        alert.updated_at = now_str
        return alert

    def get_alert(self, alert_id: str) -> Optional[SecurityAlertDTO]:
        return self._alerts.get(alert_id)

    def list_alerts(
        self,
        status: Optional[AlertStatusLiteral] = None,
        priority: Optional[AlertPriorityLiteral] = None,
        case_id: Optional[str] = None,
    ) -> List[SecurityAlertDTO]:
        res = list(self._alerts.values())
        if status:
            res = [a for a in res if a.status == status]
        if priority:
            res = [a for a in res if a.priority == priority]
        if case_id:
            res = [a for a in res if a.case_id == case_id]
        return res
