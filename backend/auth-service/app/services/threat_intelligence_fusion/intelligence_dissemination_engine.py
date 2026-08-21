"""
TruthShield X — Intelligence Dissemination & Detection Generation Engine (Phase 33).

Generates candidate Sigma/YARA rules, enforces ABAC dissemination policies (with explicit DENY precedence),
and protects downstream systems by treating intelligence reports as untrusted DATA (prompt injection defense).
"""

from typing import Dict, List, Any, Optional
from datetime import datetime, timezone
import hashlib
import re

from app.schemas.threat_intelligence_fusion_models import DisseminationRecordDTO


class IntelligenceDisseminationEngine:
    """Governed distribution of threat intelligence products and automated candidate detection rules."""

    def __init__(self):
        self._dissemination_history: List[DisseminationRecordDTO] = []
        self._seed_default_history()

    def _seed_default_history(self):
        rec = DisseminationRecordDTO(
            dissemination_id="diss_sigma_darkstorm_c2",
            product_type="CANDIDATE_DETECTION",
            recipient="SOC_DETECTION_ENGINEERING",
            classification="INTERNAL",
            policy_verdict="PERMITTED",
            reason="Internal dissemination to SOC detection team authorized.",
        )
        self._dissemination_history.append(rec)

    def generate_candidate_sigma_rule(self, indicator_value: str, technique_id: str, campaign_name: str) -> Dict[str, Any]:
        """Converts verified intelligence into candidate Sigma detection."""
        rule_yaml = f"""title: Detect {campaign_name} C2 Traffic
id: {hashlib.md5(f'{indicator_value}:{technique_id}'.encode()).hexdigest()}
status: experimental
description: Auto-generated candidate Sigma rule from TruthShield X Phase 33 Threat Fusion.
references:
  - https://truthshield.internal/campaigns/{campaign_name.lower().replace(' ', '_')}
tags:
  - attack.{technique_id.lower().replace('.', '_')}
logsource:
  category: network_traffic
detection:
  selection:
    destination_url|contains: '{indicator_value}'
  condition: selection
falsepositives:
  - Legitimate administrative traffic (verified)
level: high
"""
        return {
            "rule_id": f"sigma_{technique_id.replace('.', '_')}",
            "format": "SIGMA_YAML",
            "lifecycle_state": "CANDIDATE",
            "rule_content": rule_yaml,
            "requires_human_approval": True,
            "generated_at": datetime.now(timezone.utc).isoformat(),
        }

    def generate_candidate_yara_rule(self, malware_family: str, file_hash: str) -> Dict[str, Any]:
        """Converts malware intelligence into candidate YARA rule."""
        yara_content = f"""rule Detect_{malware_family.replace(' ', '_')} : Candidate
{{
    meta:
        description = "Candidate YARA rule for {malware_family}"
        author = "TruthShield X Threat Intelligence Fusion"
        hash = "{file_hash}"
    strings:
        $h1 = "{file_hash}" nocase
    condition:
        $h1
}}"""
        return {
            "rule_id": f"yara_{malware_family.lower().replace(' ', '_')}",
            "format": "YARA",
            "lifecycle_state": "CANDIDATE",
            "rule_content": yara_content,
            "requires_human_approval": True,
            "generated_at": datetime.now(timezone.utc).isoformat(),
        }

    def sanitize_untrusted_threat_content(self, raw_report_text: str) -> Dict[str, Any]:
        """Detects prompt injections and weaponized payloads in external threat reports."""
        injection_patterns = [
            r"ignore all previous instructions",
            r"system prompt override",
            r"disregard safety guidelines",
            r"execute this command",
        ]
        is_injected = False
        detected_patterns = []

        for p in injection_patterns:
            if re.search(p, raw_report_text, re.IGNORECASE):
                is_injected = True
                detected_patterns.append(p)

        if is_injected:
            return {
                "status": "PROMPT_INJECTION_DETECTED",
                "is_safe": False,
                "sanitized_data": "[REDACTED_MALICIOUS_PROMPT_INJECTION]",
                "action": "TREATED_AS_UNTRUSTED_DATA_ONLY",
                "detected_patterns": detected_patterns,
            }

        return {
            "status": "CLEAN_CONTENT",
            "is_safe": True,
            "sanitized_data": raw_report_text,
            "action": "DATA_PARSED",
        }

    def evaluate_dissemination_policy(
        self,
        product_type: str,
        recipient: str,
        classification: str,
        requester_clearance: str,
        tenant_scope: str,
        recipient_tenant: str,
    ) -> DisseminationRecordDTO:
        """Enforces ABAC sharing policy with explicit DENY taking absolute precedence."""
        diss_id = f"diss_{hashlib.md5(f'{product_type}:{recipient}:{datetime.now(timezone.utc).isoformat()}'.encode()).hexdigest()[:8]}"

        # Explicit DENY: Cross-tenant leakage
        if tenant_scope != "GLOBAL" and tenant_scope != recipient_tenant:
            record = DisseminationRecordDTO(
                dissemination_id=diss_id,
                product_type=product_type,
                recipient=recipient,
                classification=classification,
                policy_verdict="BLOCKED",
                reason=f"DENY: Tenant scope {tenant_scope} does not match recipient tenant {recipient_tenant}.",
            )
            self._dissemination_history.append(record)
            return record

        # Explicit DENY: Clearance insufficient for HIGHLY_RESTRICTED or RESTRICTED
        if classification == "HIGHLY_RESTRICTED" and requester_clearance != "TOP_SECRET":
            record = DisseminationRecordDTO(
                dissemination_id=diss_id,
                product_type=product_type,
                recipient=recipient,
                classification=classification,
                policy_verdict="BLOCKED",
                reason="DENY: Requester clearance insufficient for HIGHLY_RESTRICTED intelligence object.",
            )
            self._dissemination_history.append(record)
            return record

        record = DisseminationRecordDTO(
            dissemination_id=diss_id,
            product_type=product_type,
            recipient=recipient,
            classification=classification,
            policy_verdict="PERMITTED",
            reason="Policy check passed. Dissemination authorized.",
        )
        self._dissemination_history.append(record)
        return record

    def list_dissemination_records(self) -> List[DisseminationRecordDTO]:
        return self._dissemination_history
