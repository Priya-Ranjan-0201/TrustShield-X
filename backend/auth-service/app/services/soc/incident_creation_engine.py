"""Incident Creation, Deduplication, Merging & Splitting Engine (Phase 4.0 Part 7 — Sections 11-16, 58-61).

Converts correlated alert clusters into deduplicated Security Incidents with deterministic fingerprints.
"""

from typing import List, Dict, Any, Optional, Tuple
import hashlib
import uuid
from datetime import datetime, timezone
from app.schemas.soc_operations_models import (
    SOCAlertDTO,
    AlertClusterDTO,
    SecurityIncidentDTO,
    IncidentTypeLiteral,
    IncidentSeverityLiteral,
    IncidentPriorityLiteral,
    IncidentMergeRecordDTO,
    IncidentSplitRecordDTO,
)


class IncidentCreationEngine:
    """Creates, deduplicates, merges, and splits security incidents."""

    def __init__(self):
        self._incidents: Dict[str, SecurityIncidentDTO] = {}
        self._fingerprint_to_incident: Dict[str, str] = {}

    def compute_incident_fingerprint(
        self,
        incident_type: str,
        entity_ids: List[str],
        campaign_id: Optional[str] = None,
        case_id: Optional[str] = None,
    ) -> str:
        if campaign_id:
            raw = f"CAMPAIGN:{campaign_id}"
        elif case_id:
            raw = f"CASE:{case_id}"
        else:
            sorted_ents = ",".join(sorted(set(entity_ids)))
            raw = f"{incident_type}:{sorted_ents}"
        return hashlib.sha256(raw.encode()).hexdigest()

    def create_or_update_incident_from_alert(
        self,
        alert: SOCAlertDTO,
        cluster: Optional[AlertClusterDTO] = None,
    ) -> SecurityIncidentDTO:
        # Determine incident type from alert category
        type_mapping: Dict[str, IncidentTypeLiteral] = {
            "MALWARE": "MALWARE_INCIDENT",
            "PHISHING": "PHISHING_INCIDENT",
            "FINANCIAL_FRAUD": "FINANCIAL_FRAUD_INCIDENT",
            "IDENTITY_FRAUD": "IDENTITY_FRAUD_INCIDENT",
            "VOICE_SCAM": "VOICE_SCAM_INCIDENT",
            "DEEPFAKE": "DEEPFAKE_INCIDENT",
            "DOCUMENT_FRAUD": "DOCUMENT_FRAUD_INCIDENT",
            "QR_FRAUD": "QR_FRAUD_INCIDENT",
            "ACCOUNT_COMPROMISE": "ACCOUNT_COMPROMISE",
            "DATA_EXFILTRATION": "DATA_EXFILTRATION",
            "CAMPAIGN": "MULTI_MODAL_INCIDENT",
        }
        incident_type: IncidentTypeLiteral = type_mapping.get(alert.category, "UNKNOWN_INCIDENT")

        # Gather all related entity IDs
        all_entities = list(set(alert.entity_ids + (cluster.entity_ids if cluster else [])))

        fingerprint = self.compute_incident_fingerprint(
            incident_type=incident_type,
            entity_ids=all_entities,
            campaign_id=alert.campaign_id,
            case_id=alert.case_id,
        )

        now_str = datetime.now(timezone.utc).isoformat()

        # Check existing active incident with same fingerprint (Section 58, 59, Mandatory Test 16)
        if fingerprint in self._fingerprint_to_incident:
            inc_id = self._fingerprint_to_incident[fingerprint]
            incident = self._incidents[inc_id]
            incident.source_alert_count += 1
            incident.entity_count = max(incident.entity_count, len(all_entities))
            incident.finding_count += len(alert.finding_ids)
            incident.evidence_count += len(alert.evidence_ids)
            incident.last_seen = now_str
            incident.updated_at = now_str
            # Cross-modal upgrade (Section 14, Mandatory Test 19)
            if incident.incident_type != incident_type:
                incident.incident_type = "MULTI_MODAL_INCIDENT"

            # Upgrade severity/priority if higher
            rank = {"INFORMATIONAL": 0, "LOW": 1, "MEDIUM": 2, "HIGH": 3, "CRITICAL": 4}
            if rank.get(alert.severity, 0) > rank.get(incident.severity, 0):
                incident.severity = alert.severity
            if rank.get(alert.priority, 0) > rank.get(incident.priority, 0):
                incident.priority = alert.priority
            alert.incident_id = incident.incident_id
            return incident

        # Create new incident
        incident = SecurityIncidentDTO(
            incident_id=f"inc_{uuid.uuid4().hex[:12]}",
            incident_number=f"INC-{uuid.uuid4().hex[:6].upper()}",
            title=f"Incident: {alert.title}",
            description=alert.description,
            incident_type=incident_type,
            severity=alert.severity,
            priority=alert.priority,
            confidence=alert.confidence,
            status="NEW",
            source_alert_count=1,
            entity_count=len(all_entities),
            finding_count=len(alert.finding_ids),
            evidence_count=len(alert.evidence_ids),
            campaign_id=alert.campaign_id,
            attack_chain_id=alert.attack_chain_id,
            case_id=alert.case_id,
            incident_fingerprint=fingerprint,
            organization_id=alert.organization_id,
            first_seen=alert.first_seen,
            last_seen=now_str,
            detected_at=now_str,
        )

        self._incidents[incident.incident_id] = incident
        self._fingerprint_to_incident[fingerprint] = incident.incident_id
        alert.incident_id = incident.incident_id
        return incident

    def merge_incidents(
        self,
        primary_incident_id: str,
        merged_incident_ids: List[str],
        merged_by: str,
        reason: str,
    ) -> Tuple[SecurityIncidentDTO, IncidentMergeRecordDTO]:
        """Merge multiple incidents into a primary incident (Section 60)."""
        primary = self._incidents.get(primary_incident_id)
        if not primary:
            raise KeyError(f"Primary incident {primary_incident_id} not found.")

        for inc_id in merged_incident_ids:
            secondary = self._incidents.get(inc_id)
            if secondary and secondary.incident_id != primary.incident_id:
                primary.source_alert_count += secondary.source_alert_count
                primary.entity_count += secondary.entity_count
                primary.finding_count += secondary.finding_count
                primary.evidence_count += secondary.evidence_count
                secondary.status = "CANCELLED"
                secondary.updated_at = datetime.now(timezone.utc).isoformat()

        merge_rec = IncidentMergeRecordDTO(
            primary_incident_id=primary_incident_id,
            merged_incident_ids=merged_incident_ids,
            merged_by=merged_by,
            reason=reason,
        )
        return primary, merge_rec

    def split_incident(
        self,
        original_incident_id: str,
        split_by: str,
        reason: str,
        new_incident_titles: List[str],
    ) -> Tuple[SecurityIncidentDTO, List[SecurityIncidentDTO], IncidentSplitRecordDTO]:
        """Split an incorrectly grouped incident into separate incidents (Section 61)."""
        orig = self._incidents.get(original_incident_id)
        if not orig:
            raise KeyError(f"Original incident {original_incident_id} not found.")

        new_incidents: List[SecurityIncidentDTO] = []
        for title in new_incident_titles:
            new_inc = SecurityIncidentDTO(
                title=title,
                description=f"Split from {orig.incident_number}: {reason}",
                incident_type=orig.incident_type,
                severity=orig.severity,
                priority=orig.priority,
                status="NEW",
                case_id=orig.case_id,
                organization_id=orig.organization_id,
            )
            self._incidents[new_inc.incident_id] = new_inc
            new_incidents.append(new_inc)

        split_rec = IncidentSplitRecordDTO(
            original_incident_id=original_incident_id,
            new_incident_ids=[i.incident_id for i in new_incidents],
            split_by=split_by,
            reason=reason,
        )
        return orig, new_incidents, split_rec

    def get_incident(self, incident_id: str) -> Optional[SecurityIncidentDTO]:
        return self._incidents.get(incident_id)

    def list_incidents(self) -> List[SecurityIncidentDTO]:
        return list(self._incidents.values())
