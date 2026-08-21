"""Data Export & Tokenized Manifest Engine (Phase 4.0 Part 8 — Sections 42-44, 97).

Generates time-bounded, cryptographically verified export manifests while enforcing data classification boundaries.
"""

from typing import List, Dict, Any, Optional
import hashlib
import json
import uuid
from datetime import datetime, timezone, timedelta
from app.schemas.governance_models import (
    DataExportManifestDTO,
    DataClassificationLiteral,
)


class DataExportEngine:
    """Creates secure time-bounded data exports with integrity manifests."""

    def __init__(self):
        self._exports: Dict[str, DataExportManifestDTO] = {}
        self._token_to_export: Dict[str, str] = {}

    def create_data_export(
        self,
        organization_id: str,
        requester_id: str,
        requester_roles: List[str],
        scope: str,
        resource_data: List[Dict[str, Any]],
        classification: DataClassificationLiteral = "CONFIDENTIAL",
        validity_hours: int = 24,
    ) -> DataExportManifestDTO:
        # 1. Authorization Check (Section 43, Mandatory Test 9)
        privileged_roles = {"SUPER_ADMIN", "ORG_ADMIN", "SECURITY_ADMIN", "SENIOR_ANALYST", "COMPLIANCE_OFFICER", "INVESTIGATOR"}
        if not any(r in privileged_roles for r in requester_roles):
            raise PermissionError("Access denied: User lacks authorization to create data exports.")

        # 2. Data Classification Policy Enforcement (Section 29, 43, Mandatory Test 10)
        if classification in ("RESTRICTED", "HIGHLY_RESTRICTED"):
            high_clearance_roles = {"SUPER_ADMIN", "ORG_ADMIN", "SECURITY_ADMIN", "COMPLIANCE_OFFICER"}
            if not any(r in high_clearance_roles for r in requester_roles):
                raise PermissionError(f"Access denied: User lacks security clearance to export {classification} classified data.")

        # 3. Compute SHA-256 integrity hash of export payload
        serialized = json.dumps(resource_data, sort_keys=True)
        integrity_hash = hashlib.sha256(serialized.encode()).hexdigest()

        now = datetime.now(timezone.utc)
        expires_at = (now + timedelta(hours=validity_hours)).isoformat()

        manifest = DataExportManifestDTO(
            organization_id=organization_id,
            requester_id=requester_id,
            scope=scope,
            resource_count=len(resource_data),
            classification=classification,
            integrity_hash=integrity_hash,
            expires_at=expires_at,
        )

        self._exports[manifest.export_id] = manifest
        self._token_to_export[manifest.download_token] = manifest.export_id
        return manifest

    def get_export_by_token(self, token: str) -> Optional[DataExportManifestDTO]:
        exp_id = self._token_to_export.get(token)
        if not exp_id:
            return None
        manifest = self._exports.get(exp_id)
        if manifest:
            # Check expiration
            if datetime.fromisoformat(manifest.expires_at) < datetime.now(timezone.utc):
                manifest.status = "EXPIRED"
                return None
        return manifest

    def get_export(self, export_id: str) -> Optional[DataExportManifestDTO]:
        return self._exports.get(export_id)

    def list_exports(self, organization_id: Optional[str] = None) -> List[DataExportManifestDTO]:
        if organization_id:
            return [e for e in self._exports.values() if e.organization_id == organization_id]
        return list(self._exports.values())
