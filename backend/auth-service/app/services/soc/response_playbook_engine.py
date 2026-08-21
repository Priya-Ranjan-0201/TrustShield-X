"""Response Playbook Engine & Versioning (Phase 4.0 Part 7 — Sections 27-30, 85).

Defines controlled response workflows with immutable version snapshots and content integrity hashing.
"""

from typing import List, Dict, Any, Optional, Tuple
import hashlib
import json
import uuid
from datetime import datetime, timezone
from app.schemas.soc_operations_models import (
    ResponsePlaybookDTO,
    ResponsePlaybookVersionDTO,
    PlaybookStepDTO,
    IncidentTypeLiteral,
)


class ResponsePlaybookEngine:
    """Manages response playbook templates, published immutable versions, and candidate selection."""

    def __init__(self):
        self._playbooks: Dict[str, ResponsePlaybookDTO] = {}
        self._versions: Dict[str, ResponsePlaybookVersionDTO] = {}
        self._initialize_standard_playbooks()

    def _initialize_standard_playbooks(self):
        # 1. Phishing Response Playbook
        phish_steps = [
            PlaybookStepDTO(
                playbook_id="pbk_phishing",
                step_number=1,
                name="Validate Threat IOC",
                description="Verify domain presence in threat feeds",
                action_type="MARK_INDICATOR",
                risk_level="LOW",
                approval_required=False,
                dry_run_supported=True,
            ),
            PlaybookStepDTO(
                playbook_id="pbk_phishing",
                step_number=2,
                name="Block Phishing Domain",
                description="Submit domain block to edge DNS and WAF",
                action_type="BLOCK_DOMAIN",
                risk_level="HIGH",
                approval_required=True,
                dry_run_supported=True,
                rollback_supported=True,
            ),
            PlaybookStepDTO(
                playbook_id="pbk_phishing",
                step_number=3,
                name="Notify Target Users",
                description="Broadcast security notice to recipient user list",
                action_type="NOTIFY_USER",
                risk_level="LOW",
                approval_required=False,
            ),
        ]
        self.publish_playbook(
            playbook_id="pbk_phishing",
            name="Phishing Response Standard Playbook",
            description="Triage, DNS block and user notification for verified phishing attacks.",
            incident_types=["PHISHING_INCIDENT"],
            steps=phish_steps,
        )

        # 2. Malware Response Playbook
        malware_steps = [
            PlaybookStepDTO(
                playbook_id="pbk_malware",
                step_number=1,
                name="Quarantine Malicious Payload",
                description="Quarantine file and isolate from local storage",
                action_type="QUARANTINE_FILE",
                risk_level="HIGH",
                approval_required=True,
                dry_run_supported=True,
            ),
            PlaybookStepDTO(
                playbook_id="pbk_malware",
                step_number=2,
                name="Isolate Compromised Device",
                description="Disconnect network interface on host device",
                action_type="ISOLATE_DEVICE",
                risk_level="CRITICAL",
                approval_required=True,
                dry_run_supported=True,
                rollback_supported=True,
            ),
        ]
        self.publish_playbook(
            playbook_id="pbk_malware",
            name="Malware Containment Playbook",
            description="File quarantine and host network isolation.",
            incident_types=["MALWARE_INCIDENT"],
            steps=malware_steps,
        )

        # 3. Voice Scam Response Playbook
        voice_steps = [
            PlaybookStepDTO(
                playbook_id="pbk_voice_scam",
                step_number=1,
                name="Collect Voice Evidence",
                description="Extract forensic audio embeddings and scam phrases",
                action_type="COLLECT_EVIDENCE",
                risk_level="LOW",
                approval_required=False,
            ),
            PlaybookStepDTO(
                playbook_id="pbk_voice_scam",
                step_number=2,
                name="Alert Fraud Team",
                description="Route urgent notification to fraud operations lead",
                action_type="NOTIFY_ANALYST",
                risk_level="LOW",
                approval_required=False,
            ),
        ]
        self.publish_playbook(
            playbook_id="pbk_voice_scam",
            name="Voice Scam & Deepfake Response Playbook",
            description="Forensic voice analysis and fraud team notification.",
            incident_types=["VOICE_SCAM_INCIDENT", "DEEPFAKE_INCIDENT"],
            steps=voice_steps,
        )

    def publish_playbook(
        self,
        playbook_id: str,
        name: str,
        description: str,
        incident_types: List[IncidentTypeLiteral],
        steps: List[PlaybookStepDTO],
        author: str = "SOC_ADMIN",
    ) -> Tuple[ResponsePlaybookDTO, ResponsePlaybookVersionDTO]:
        """Publish an immutable version of a response playbook (Sections 28-29, 85)."""
        # Calculate deterministic content hash
        steps_raw = json.dumps([s.model_dump() for s in steps], sort_keys=True)
        content_hash = hashlib.sha256(steps_raw.encode()).hexdigest()

        existing = self._playbooks.get(playbook_id)
        ver_num = (existing.current_version + 1) if existing else 1

        pb = ResponsePlaybookDTO(
            playbook_id=playbook_id,
            name=name,
            current_version=ver_num,
            description=description,
            incident_types=incident_types,
            steps=steps,
        )
        self._playbooks[playbook_id] = pb

        version_dto = ResponsePlaybookVersionDTO(
            version_id=f"pbv_{playbook_id}_v{ver_num}",
            playbook_id=playbook_id,
            version_number=ver_num,
            content_hash=content_hash,
            author=author,
            steps=steps,
        )
        self._versions[version_dto.version_id] = version_dto
        return pb, version_dto

    def select_playbook_for_incident(self, incident_type: IncidentTypeLiteral) -> Optional[ResponsePlaybookDTO]:
        """Selects matching playbook. Returns None for UNKNOWN_INCIDENT without fabricating specialized response (Section 51, Test 28)."""
        if incident_type == "UNKNOWN_INCIDENT":
            return None

        for pb in self._playbooks.values():
            if pb.enabled and incident_type in pb.incident_types:
                return pb
        return None

    def get_playbook(self, playbook_id: str) -> Optional[ResponsePlaybookDTO]:
        return self._playbooks.get(playbook_id)

    def get_playbook_version(self, playbook_id: str, version_number: int) -> Optional[ResponsePlaybookVersionDTO]:
        ver_id = f"pbv_{playbook_id}_v{version_number}"
        return self._versions.get(ver_id)

    def list_playbooks(self) -> List[ResponsePlaybookDTO]:
        return list(self._playbooks.values())
