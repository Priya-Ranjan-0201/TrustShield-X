"""
TruthShield X — Intelligence Sharing Policy & Privacy Preservation Engine
"""

import re
import uuid
from typing import Dict, List, Optional, Any
from datetime import datetime, timezone
from app.schemas.federation_models import SharingPolicyDecisionDTO, SharingDecisionLiteral


class IntelligenceSharingPolicyEngine:
    """Evaluates privacy, PII, secrets, and data classification to make deterministic sharing decisions."""

    PII_PATTERNS = {
        "EMAIL": re.compile(r"\b[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+\b"),
        "PHONE": re.compile(r"\b(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b"),
        "CREDIT_CARD": re.compile(r"\b(?:\d{4}[-\s]?){3}\d{4}\b"),
        "INDIAN_UPI": re.compile(r"\b[a-zA-Z0-9.\-_]{2,256}@(oksbi|okaxis|okicici|paytm|ybl|upi|apl|ibl|axl)\b"),
    }

    SECRET_PATTERNS = {
        "GENERIC_API_KEY": re.compile(r"(?i)['\"]?(?:api_key|apikey|secret|token|password|auth_token)['\"]?[\s:=]+['\"]?([a-zA-Z0-9_\-]{12,})['\"]?"),
        "BEARER_TOKEN": re.compile(r"(?i)bearer\s+[a-zA-Z0-9_\-\.]{16,}"),
        "PRIVATE_KEY": re.compile(r"-----BEGIN (?:RSA |EC )?PRIVATE KEY-----"),
    }

    def detect_pii(self, text: str) -> List[str]:
        """Detects personally identifiable information in payload strings."""
        detected = []
        for pii_type, pattern in self.PII_PATTERNS.items():
            if pattern.search(text):
                detected.append(pii_type)
        return detected

    def detect_secrets(self, text: str) -> List[str]:
        """Detects API keys, passwords, or cryptographic secrets."""
        detected = []
        for secret_type, pattern in self.SECRET_PATTERNS.items():
            if pattern.search(text):
                detected.append(secret_type)
        return detected

    def evaluate_sharing(
        self,
        payload_data: Dict[str, Any],
        requested_scope: str = "GLOBAL",
        data_classification: str = "CONFIDENTIAL",
        tenant_allows_sharing: bool = True,
    ) -> SharingPolicyDecisionDTO:
        """Evaluates whether an intelligence payload can be shared safely."""
        policy_id = f"pol_{uuid.uuid4().hex[:10]}"
        text_repr = str(payload_data)

        secrets = self.detect_secrets(text_repr)
        pii = self.detect_pii(text_repr)

        # 1. Absolute Rule: Secrets strictly block sharing
        if secrets:
            return SharingPolicyDecisionDTO(
                policy_id=policy_id,
                decision="REJECT",
                reason=f"Security violation: Secret material detected ({', '.join(secrets)}). Sharing blocked.",
                evaluated_attributes={"classification": data_classification, "scope": requested_scope},
                detected_pii=pii,
                detected_secrets=secrets,
            )

        # 2. If tenant does not allow sharing
        if not tenant_allows_sharing:
            return SharingPolicyDecisionDTO(
                policy_id=policy_id,
                decision="SHARE_INTERNAL_ONLY",
                reason="Tenant policy prohibits external intelligence sharing.",
                evaluated_attributes={"classification": data_classification, "scope": requested_scope},
                detected_pii=pii,
                detected_secrets=[],
            )

        # 3. PII present -> Requires redaction before sharing
        if pii:
            return SharingPolicyDecisionDTO(
                policy_id=policy_id,
                decision="SHARE_REDACTED",
                reason=f"PII detected ({', '.join(pii)}). Permitted only with field-level redaction.",
                evaluated_attributes={"classification": data_classification, "scope": requested_scope},
                detected_pii=pii,
                detected_secrets=[],
            )

        # 4. Highly restricted data cannot be globalized
        if data_classification in ("RESTRICTED", "HIGHLY_RESTRICTED") and requested_scope == "GLOBAL":
            return SharingPolicyDecisionDTO(
                policy_id=policy_id,
                decision="SHARE_INTERNAL_ONLY",
                reason=f"Data classification '{data_classification}' exceeds GLOBAL sharing clearance.",
                evaluated_attributes={"classification": data_classification, "scope": requested_scope},
                detected_pii=[],
                detected_secrets=[],
            )

        return SharingPolicyDecisionDTO(
            policy_id=policy_id,
            decision="SHARE",
            reason="Intelligence satisfies all privacy, secret, and sharing policy constraints.",
            evaluated_attributes={"classification": data_classification, "scope": requested_scope},
            detected_pii=[],
            detected_secrets=[],
        )

    def redact_pii_fields(self, payload_data: Dict[str, Any]) -> Dict[str, Any]:
        """Redacts sensitive PII fields from payload dictionary."""
        redacted = dict(payload_data)
        for k, v in payload_data.items():
            if isinstance(v, str):
                for pii_type, pattern in self.PII_PATTERNS.items():
                    if pattern.search(v):
                        redacted[k] = f"[REDACTED_{pii_type}]"
                        break
        return redacted
