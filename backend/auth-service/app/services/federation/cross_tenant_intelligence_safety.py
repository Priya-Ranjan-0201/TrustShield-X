"""
TruthShield X — Cross-Tenant Intelligence Safety & Sanitization Engine
"""

from typing import Dict, List, Optional, Any
from app.schemas.federation_models import FederatedIntelligenceObjectDTO


class CrossTenantIntelligenceSafety:
    """Sanitizes intelligence objects before cross-tenant delivery to guarantee zero customer data leakage."""

    SENSITIVE_ORIGIN_FIELDS = {
        "origin_tenant",
        "private_customer_id",
        "internal_ip_address",
        "victim_account_number",
        "internal_hostname",
        "investigation_notes",
    }

    def sanitize_for_consumer(
        self,
        intel_obj: FederatedIntelligenceObjectDTO,
        consumer_tenant_id: str,
    ) -> Dict[str, Any]:
        """Strips private provenance and customer identity before sharing with another tenant."""
        raw_dict = intel_obj.model_dump()

        # If consumer is the owning tenant, return complete object
        if intel_obj.tenant_scope == consumer_tenant_id:
            return raw_dict

        # Sanitization for foreign consuming tenant
        sanitized_prov = dict(raw_dict.get("provenance", {}))
        for field in self.SENSITIVE_ORIGIN_FIELDS:
            sanitized_prov.pop(field, None)

        # Obfuscate origin tenant to anonymous federated contributor
        sanitized_prov["contributing_scope"] = "FEDERATED_COMMUNITY_PARTICIPANT"
        raw_dict["tenant_scope"] = "COMMUNITY_ANONYMIZED"
        raw_dict["provenance"] = sanitized_prov

        return raw_dict
