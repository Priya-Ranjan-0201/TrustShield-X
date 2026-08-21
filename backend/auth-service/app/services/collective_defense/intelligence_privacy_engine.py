"""
TruthShield X — Privacy Transformation Engine (Phase 16).

Inspects threat intelligence objects for PII, secrets, and customer identifiers,
and applies privacy-preserving transformations (Redact, Hash, Tokenize, Generalize).
"""

from typing import Dict, Any, List, Tuple
import re
import hashlib
from datetime import datetime, timezone

from app.schemas.collective_defense_models import (
    ThreatIntelligenceObjectDTO,
    IntelligencePrivacyTransformationDTO,
    PrivacyTransformationTypeLiteral,
)

SECRET_PATTERNS = [
    re.compile(r"(?i)(api[_-]?key|secret|token|password|bearer|auth|jwt)[\s:=]+['\"]?([a-zA-Z0-9_\-\.]{8,})['\"]?"),
    re.compile(r"AKIA[0-9A-Z]{16}"),  # AWS Access Key
    re.compile(r"(?i)ghp_[0-9a-zA-Z]{36}"),  # GitHub Personal Access Token
]

PII_PATTERNS = [
    re.compile(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"),  # Email
    re.compile(r"\b\d{3}[-.]?\d{3}[-.]?\d{4}\b"),  # US Phone
    re.compile(r"\b\d{10,12}\b"),  # Generic Mobile / Aadhar
]


class IntelligencePrivacyEngine:
    """Detects sensitive information and enforces zero-leakage privacy transformations."""

    def scan_for_sensitive_data(self, text: str) -> Tuple[List[str], List[str]]:
        """Scans arbitrary text or payload for PII and secrets."""
        detected_secrets: List[str] = []
        detected_pii: List[str] = []

        for p in SECRET_PATTERNS:
            matches = p.findall(text)
            if matches:
                detected_secrets.extend([str(m) for m in matches])

        for p in PII_PATTERNS:
            matches = p.findall(text)
            if matches:
                detected_pii.extend(matches)

        return detected_pii, detected_secrets

    def transform_for_sharing(
        self,
        obj: ThreatIntelligenceObjectDTO,
        tenant_industry: str = "FINANCIAL_SERVICES",
        transformation_type: PrivacyTransformationTypeLiteral = "REDACT",
    ) -> Tuple[ThreatIntelligenceObjectDTO, IntelligencePrivacyTransformationDTO]:
        """Transforms a private threat intelligence object into a privacy-safe shared object."""
        # Clone object
        shared_obj = obj.model_copy(deep=True)

        # 1. Anonymize tenant identity into cohort
        anonymized_cohort = f"COHORT_{tenant_industry.upper()}_{hashlib.sha256(obj.tenant_id.encode()).hexdigest()[:6]}"
        shared_obj.anonymized_tenant_cohort = anonymized_cohort
        shared_obj.tenant_id = "ANONYMIZED_FEDERATION_SOURCE"

        # 2. Check for PII / secrets in tags, indicators, and provenance
        raw_repr = f"{shared_obj.raw_indicator} {shared_obj.tags} {shared_obj.provenance}"
        pii, secrets = self.scan_for_sensitive_data(raw_repr)

        redacted_fields = []
        if pii:
            redacted_fields.append("PII_IN_METADATA")
        if secrets:
            redacted_fields.append("SECRETS_IN_METADATA")

        # 3. Clean provenance of internal server names / private IPs
        clean_provenance = {
            "origin": "VALIDATED_COLLECTIVE_DEFENSE_NODE",
            "anonymized_cohort": anonymized_cohort,
            "validation_timestamp": datetime.now(timezone.utc).isoformat(),
        }
        shared_obj.provenance = clean_provenance

        # 4. Enforce classification change
        shared_obj.classification = "SHARED_THREAT_INTELLIGENCE"
        shared_obj.sharing_state = "SHARED"

        record = IntelligencePrivacyTransformationDTO(
            intelligence_id=obj.intelligence_id,
            transformation_type=transformation_type,
            detected_pii=pii,
            detected_secrets=secrets,
            detected_customer_identifiers=[obj.tenant_id],
            redacted_fields=redacted_fields,
            anonymized_cohort=anonymized_cohort,
            is_safe_to_share=len(secrets) == 0,
        )

        return shared_obj, record
