"""API Key & Service Account Governance Service (Phase 4.0 Part 8 — Sections 77-79, 100).

Manages cryptographic API key hashing, single-view raw key issuance, revocation, and service accounts.
"""

from typing import List, Dict, Any, Optional, Tuple
import hashlib
import secrets
import uuid
from datetime import datetime, timezone, timedelta
from app.schemas.governance_models import (
    APIKeyMetadataDTO,
    APIKeyCreationResponseDTO,
    ServiceAccountDTO,
)


class APIKeyService:
    """Manages secure API keys with SHA-256 hashed secret storage and zero plaintext persistence."""

    def __init__(self):
        self._keys: Dict[str, APIKeyMetadataDTO] = {}
        self._hash_to_key_id: Dict[str, str] = {}
        self._service_accounts: Dict[str, ServiceAccountDTO] = {}

    def create_api_key(
        self,
        organization_id: str,
        name: str,
        owner_id: str,
        permissions: List[str],
        scope: str = "ORGANIZATION",
        validity_days: int = 90,
    ) -> Tuple[APIKeyCreationResponseDTO, APIKeyMetadataDTO]:
        """Creates an API key and returns raw secret ONLY ONCE (Section 78, 91, Mandatory Test 12)."""
        raw_secret = f"tsx_{secrets.token_urlsafe(32)}"
        key_prefix = raw_secret[:10]
        hashed_secret = hashlib.sha256(raw_secret.encode()).hexdigest()

        now = datetime.now(timezone.utc)
        expires_at = (now + timedelta(days=validity_days)).isoformat()

        key_dto = APIKeyMetadataDTO(
            organization_id=organization_id,
            name=name,
            key_prefix=key_prefix,
            hashed_secret=hashed_secret,
            scope=scope,
            permissions=permissions,
            owner_id=owner_id,
            expires_at=expires_at,
            status="ACTIVE",
        )

        self._keys[key_dto.key_id] = key_dto
        self._hash_to_key_id[hashed_secret] = key_dto.key_id

        creation_resp = APIKeyCreationResponseDTO(
            key_id=key_dto.key_id,
            name=name,
            raw_key=raw_secret,
            key_prefix=key_prefix,
            expires_at=expires_at,
        )

        return creation_resp, key_dto

    def verify_api_key(self, raw_key: str) -> Optional[APIKeyMetadataDTO]:
        """Verifies raw API key against stored SHA-256 hash (Section 78, Mandatory Test 11)."""
        hashed = hashlib.sha256(raw_key.encode()).hexdigest()
        key_id = self._hash_to_key_id.get(hashed)
        if not key_id:
            return None

        key_meta = self._keys.get(key_id)
        if not key_meta or key_meta.status != "ACTIVE":
            return None  # Revoked or inactive

        if key_meta.expires_at and datetime.fromisoformat(key_meta.expires_at) < datetime.now(timezone.utc):
            key_meta.status = "EXPIRED"
            return None

        key_meta.last_used_at = datetime.now(timezone.utc).isoformat()
        return key_meta

    def revoke_api_key(self, key_id: str) -> Optional[APIKeyMetadataDTO]:
        """Revokes an API key (Section 78, Mandatory Test 11)."""
        key = self._keys.get(key_id)
        if key:
            key.status = "REVOKED"
        return key

    def rotate_api_key(self, key_id: str) -> Tuple[APIKeyCreationResponseDTO, APIKeyMetadataDTO]:
        """Rotates key: revokes existing and issues new key with same permissions."""
        old = self.revoke_api_key(key_id)
        if not old:
            raise KeyError(f"API key {key_id} not found.")

        return self.create_api_key(
            organization_id=old.organization_id,
            name=f"{old.name} (Rotated)",
            owner_id=old.owner_id,
            permissions=old.permissions,
            scope=old.scope,
        )

    def create_service_account(
        self,
        organization_id: str,
        name: str,
        permissions: List[str],
        created_by: str,
        description: str = "",
    ) -> ServiceAccountDTO:
        sa = ServiceAccountDTO(
            organization_id=organization_id,
            name=name,
            description=description,
            permissions=permissions,
            created_by=created_by,
            status="ACTIVE",
        )
        self._service_accounts[sa.service_account_id] = sa
        return sa

    def get_service_account(self, sa_id: str) -> Optional[ServiceAccountDTO]:
        return self._service_accounts.get(sa_id)

    def list_api_keys(self, organization_id: Optional[str] = None) -> List[APIKeyMetadataDTO]:
        if organization_id:
            return [k for k in self._keys.values() if k.organization_id == organization_id]
        return list(self._keys.values())
