"""Data Classification & Sensitive Data Redaction Engine (Phase 4.0 Part 8 — Sections 27-30, 97).

Classifies platform resources and enforces rigorous redaction of credentials and PII.
"""

from typing import List, Dict, Any, Optional
import re
from app.schemas.governance_models import DataClassificationLiteral

SECRET_PATTERNS = [
    re.compile(r"(?i)(password|secret|apikey|api_key|token|auth|bearer)\s*[:=]\s*['\"]?([^\s'\"]+)"),
    re.compile(r"(?i)bearer\s+[A-Za-z0-9\-\._~\+\/]+=*"),
    re.compile(r"eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}"),  # JWT regex
]


class DataClassificationEngine:
    """Classifies resources and sanitizes sensitive credentials from logs and audit events."""

    @staticmethod
    def classify_resource(resource_type: str, metadata: Optional[Dict[str, Any]] = None) -> DataClassificationLiteral:
        meta = metadata or {}
        # Rule-based classification
        if resource_type in ("CREDENTIAL", "PRIVATE_KEY", "SESSION_TOKEN", "SECRET"):
            return "HIGHLY_RESTRICTED"
        if resource_type in ("EVIDENCE", "FORENSIC_DUMP", "PAYMENT_INFO", "IDENTITY_RECORD"):
            return "RESTRICTED"
        if resource_type in ("INCIDENT", "CASE", "INVESTIGATION_NOTE", "AUDIT_LOG", "REPORT"):
            return "CONFIDENTIAL"
        if resource_type in ("ALERT", "THREAT_INTELLIGENCE", "RULE"):
            return "INTERNAL"
        return "INTERNAL"

    @staticmethod
    def redact_sensitive_data(text: str) -> str:
        """Section 30, Mandatory Test 20: Redacts passwords, bearer tokens, API keys, JWTs."""
        if not text:
            return text

        sanitized = text
        for pattern in SECRET_PATTERNS:
            sanitized = pattern.sub("[REDACTED_SECRET]", sanitized)

        return sanitized

    @staticmethod
    def sanitize_dictionary(payload: Dict[str, Any]) -> Dict[str, Any]:
        """Recursively sanitizes dictionary payloads for safe logging and audit records."""
        sanitized = {}
        for k, v in payload.items():
            k_low = k.lower()
            if any(s in k_low for s in ("password", "secret", "token", "apikey", "api_key", "auth")):
                sanitized[k] = "[REDACTED]"
            elif isinstance(v, dict):
                sanitized[k] = DataClassificationEngine.sanitize_dictionary(v)
            elif isinstance(v, str):
                sanitized[k] = DataClassificationEngine.redact_sensitive_data(v)
            else:
                sanitized[k] = v
        return sanitized
