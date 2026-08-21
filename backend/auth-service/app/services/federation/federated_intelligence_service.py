"""
TruthShield X — Federated Digital Trust Intelligence Service
"""

import uuid
from typing import Dict, List, Optional, Any
from datetime import datetime, timezone, timedelta
from app.schemas.federation_models import (
    FederatedIntelligenceObjectDTO,
    IntelligenceTypeLiteral,
    SharingScopeLiteral,
    VerificationStatusLiteral,
)


class FederatedIntelligenceService:
    """Manages federated threat intelligence objects across tenant-private, trusted-shared, and global scopes."""

    def __init__(self):
        # intelligence_id -> FederatedIntelligenceObjectDTO
        self._intelligence_store: Dict[str, FederatedIntelligenceObjectDTO] = {}

    def submit_intelligence(
        self,
        intelligence_type: IntelligenceTypeLiteral,
        canonical_identifier: str,
        tenant_scope: str = "default_tenant",
        sharing_scope: SharingScopeLiteral = "PRIVATE",
        classification: str = "CONFIDENTIAL",
        confidence: float = 0.85,
        verification_status: VerificationStatusLiteral = "OBSERVED",
        provenance: Optional[Dict[str, Any]] = None,
        source_type: str = "INTERNAL_OBSERVATION",
        source_reliability: float = 0.90,
        ttl_days: Optional[int] = 30,
        redacted_attributes: Optional[List[str]] = None,
    ) -> FederatedIntelligenceObjectDTO:
        """Registers a federated threat intelligence object with full provenance tracking."""
        intel_id = f"fio_{uuid.uuid4().hex[:12]}"
        now = datetime.now(timezone.utc)
        now_iso = now.isoformat()
        expiration_iso = (now + timedelta(days=ttl_days)).isoformat() if ttl_days else None

        prov = provenance or {"origin_tenant": tenant_scope, "registered_at": now_iso}

        obj = FederatedIntelligenceObjectDTO(
            intelligence_id=intel_id,
            intelligence_type=intelligence_type,
            canonical_identifier=canonical_identifier,
            tenant_scope=tenant_scope,
            sharing_scope=sharing_scope,
            classification=classification,
            confidence=max(0.0, min(1.0, confidence)),
            verification_status=verification_status,
            provenance=prov,
            source_type=source_type,
            source_reliability=source_reliability,
            first_seen=now_iso,
            last_seen=now_iso,
            expiration=expiration_iso,
            created_at=now_iso,
            updated_at=now_iso,
            version=1,
            redacted_attributes=redacted_attributes or [],
        )

        self._intelligence_store[intel_id] = obj
        return obj

    def get_intelligence(self, intelligence_id: str, requesting_tenant_id: str = "default_tenant") -> Optional[FederatedIntelligenceObjectDTO]:
        """Retrieves an intelligence object enforcing tenant and sharing scope permissions."""
        obj = self._intelligence_store.get(intelligence_id)
        if not obj:
            return None

        # Check access scope
        if obj.sharing_scope == "PRIVATE" and obj.tenant_scope != requesting_tenant_id:
            return None  # Access denied for private foreign tenant object

        return obj

    def list_intelligence(
        self,
        requesting_tenant_id: str = "default_tenant",
        intelligence_type: Optional[IntelligenceTypeLiteral] = None,
        scope: Optional[SharingScopeLiteral] = None,
    ) -> List[FederatedIntelligenceObjectDTO]:
        """Lists all intelligence objects accessible to the requesting tenant."""
        results = []
        now_iso = datetime.now(timezone.utc).isoformat()

        for obj in self._intelligence_store.values():
            # Check expiration
            if obj.expiration and obj.expiration < now_iso and obj.verification_status != "REVOKED":
                obj.verification_status = "EXPIRED"

            # Access Scope Filter
            if obj.sharing_scope == "PRIVATE" and obj.tenant_scope != requesting_tenant_id:
                continue

            if intelligence_type and obj.intelligence_type != intelligence_type:
                continue

            if scope and obj.sharing_scope != scope:
                continue

            results.append(obj)

        return results

    def revoke_intelligence(
        self,
        intelligence_id: str,
        revocation_reason: str,
        authorized_by: str,
        requesting_tenant_id: str = "default_tenant",
    ) -> FederatedIntelligenceObjectDTO:
        """Revokes incorrect or disputed intelligence while strictly preserving historical audit records."""
        obj = self._intelligence_store.get(intelligence_id)
        if not obj:
            raise KeyError(f"Intelligence '{intelligence_id}' not found.")

        if obj.tenant_scope != requesting_tenant_id and authorized_by != "SYSTEM_ADMIN":
            raise PermissionError("Unauthorized to revoke foreign tenant intelligence.")

        now_iso = datetime.now(timezone.utc).isoformat()
        obj.verification_status = "REVOKED"
        obj.provenance["revocation"] = {
            "revoked_by": authorized_by,
            "reason": revocation_reason,
            "revoked_at": now_iso,
        }
        obj.updated_at = now_iso
        obj.version += 1
        return obj
