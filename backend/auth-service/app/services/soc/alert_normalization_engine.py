"""SOC Alert Normalization Engine (Phase 4.0 Part 7 — Section 2).

Converts raw alerts from diverse TruthShield X detection engines (Voice, Deepfake, APK,
Website, URL, QR, Document, Identity, Payment, Threat Intel, Monitoring, Graph) into
canonical SOCAlertDTOs without destroying source-specific attributes.
"""

from typing import List, Dict, Any, Optional
import uuid
from datetime import datetime, timezone
from app.schemas.soc_operations_models import (
    SOCAlertDTO,
    AlertSourceLiteral,
    AlertCategoryLiteral,
    IncidentSeverityLiteral,
    IncidentPriorityLiteral,
)


class AlertNormalizationEngine:
    """Normalizes heterogenous alert formats into canonical SOCAlertDTO."""

    @staticmethod
    def normalize_alert(
        raw_alert: Dict[str, Any],
        source_system: AlertSourceLiteral = "INTERNAL_DETECTOR",
        organization_id: Optional[str] = None,
    ) -> SOCAlertDTO:
        # Extract core properties safely
        alert_id = raw_alert.get("alert_id") or f"soc_alt_{uuid.uuid4().hex[:12]}"
        source_alert_id = raw_alert.get("source_alert_id") or raw_alert.get("id") or alert_id
        alert_type = raw_alert.get("alert_type") or raw_alert.get("type") or "SECURITY_ALERT"
        title = raw_alert.get("title") or f"Security Alert: {alert_type}"
        description = raw_alert.get("description") or raw_alert.get("summary") or "Security alert generated."

        # Map category
        cat_str = str(raw_alert.get("category", "")).upper()
        if "MALWARE" in cat_str or "APK" in cat_str:
            category: AlertCategoryLiteral = "MALWARE"
        elif "PHISH" in cat_str or "URL" in cat_str or "WEBSITE" in cat_str:
            category = "PHISHING"
        elif "PAYMENT" in cat_str or "UPI" in cat_str or "FINANCIAL" in cat_str:
            category = "FINANCIAL_FRAUD"
        elif "VOICE" in cat_str or "AUDIO" in cat_str:
            category = "VOICE_SCAM"
        elif "DEEPFAKE" in cat_str or "FACE" in cat_str:
            category = "DEEPFAKE"
        elif "DOC" in cat_str:
            category = "DOCUMENT_FRAUD"
        elif "QR" in cat_str:
            category = "QR_FRAUD"
        elif "ACCOUNT" in cat_str:
            category = "ACCOUNT_COMPROMISE"
        elif "EXFIL" in cat_str:
            category = "DATA_EXFILTRATION"
        elif "NETWORK" in cat_str:
            category = "NETWORK_THREAT"
        elif "CAMPAIGN" in cat_str:
            category = "CAMPAIGN"
        elif "INFRA" in cat_str:
            category = "INFRASTRUCTURE"
        elif "IDENTITY" in cat_str:
            category = "IDENTITY_FRAUD"
        else:
            category = "OTHER"

        # Severity & Priority
        sev_str = str(raw_alert.get("severity", "MEDIUM")).upper()
        severity: IncidentSeverityLiteral = (
            "CRITICAL" if sev_str == "CRITICAL"
            else "HIGH" if sev_str == "HIGH"
            else "LOW" if sev_str == "LOW"
            else "INFORMATIONAL" if sev_str == "INFORMATIONAL"
            else "MEDIUM"
        )

        prio_str = str(raw_alert.get("priority", severity)).upper()
        priority: IncidentPriorityLiteral = (
            "CRITICAL" if prio_str == "CRITICAL"
            else "HIGH" if prio_str == "HIGH"
            else "LOW" if prio_str == "LOW"
            else "INFORMATIONAL" if prio_str == "INFORMATIONAL"
            else "MEDIUM"
        )

        confidence = raw_alert.get("confidence", "HIGH")
        entity_ids = raw_alert.get("entity_ids", [])
        if not entity_ids and "entity_id" in raw_alert:
            entity_ids = [raw_alert["entity_id"]]

        finding_ids = raw_alert.get("finding_ids", [])
        if not finding_ids and "finding_id" in raw_alert:
            finding_ids = [raw_alert["finding_id"]]

        evidence_ids = raw_alert.get("evidence_ids", [])
        if not evidence_ids and "evidence_id" in raw_alert:
            evidence_ids = [raw_alert["evidence_id"]]

        relationship_ids = raw_alert.get("relationship_ids", [])

        now_str = datetime.now(timezone.utc).isoformat()

        return SOCAlertDTO(
            alert_id=alert_id,
            source_alert_id=source_alert_id,
            source_system=source_system,
            alert_type=alert_type,
            category=category,
            subcategory=raw_alert.get("subcategory"),
            title=title,
            description=description,
            severity=severity,
            priority=priority,
            confidence=confidence,
            status=raw_alert.get("status", "NEW"),
            entity_ids=entity_ids,
            finding_ids=finding_ids,
            evidence_ids=evidence_ids,
            relationship_ids=relationship_ids,
            campaign_id=raw_alert.get("campaign_id"),
            attack_chain_id=raw_alert.get("attack_chain_id"),
            case_id=raw_alert.get("case_id"),
            incident_id=raw_alert.get("incident_id"),
            first_seen=raw_alert.get("first_seen", now_str),
            last_seen=raw_alert.get("last_seen", now_str),
            organization_id=organization_id or raw_alert.get("organization_id"),
            raw_payload=raw_alert,
            created_at=raw_alert.get("created_at", now_str),
            updated_at=raw_alert.get("updated_at", now_str),
        )
