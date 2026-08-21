"""
TruthShield X — Audit Preparation & Evidence Package Compiler
"""

import hashlib
import json
import uuid
from typing import Dict, List, Optional, Any
from datetime import datetime, timezone
from app.schemas.governance_fabric_models import (
    AuditPackageDTO,
    GovernanceRequirementDTO,
    GovernanceEvidenceDTO,
)


class AuditPreparationEngine:
    """Compiles structured audit evidence packages with cryptographic integrity manifests."""

    def compile_audit_package(
        self,
        framework_id: str,
        framework_version: str,
        requirements: List[GovernanceRequirementDTO],
        evidence_list: List[GovernanceEvidenceDTO],
        exceptions_count: int = 0,
    ) -> AuditPackageDTO:
        """Compiles and signs an audit evidence package."""
        pkg_id = f"pkg_{uuid.uuid4().hex[:8]}"

        satisfied = sum(1 for r in requirements if r.status == "SATISFIED")
        partial = sum(1 for r in requirements if r.status == "PARTIALLY_SATISFIED")
        not_sat = sum(1 for r in requirements if r.status == "NOT_SATISFIED")

        manifest_data = {
            "pkg_id": pkg_id,
            "framework_id": framework_id,
            "framework_version": framework_version,
            "requirements_count": len(requirements),
            "evidence_count": len(evidence_list),
            "evidence_hashes": [e.integrity_hash for e in evidence_list],
        }

        raw = json.dumps(manifest_data, sort_keys=True).encode("utf-8")
        manifest_hash = hashlib.sha256(raw).hexdigest()

        return AuditPackageDTO(
            package_id=pkg_id,
            framework_id=framework_id,
            framework_version=framework_version,
            scope="FULL_PLATFORM_TENANT_ISOLATION_ASSURANCE",
            generated_at=datetime.now(timezone.utc).isoformat(),
            total_requirements_assessed=len(requirements),
            requirements_satisfied=satisfied,
            requirements_partial=partial,
            requirements_not_satisfied=not_sat,
            active_exceptions_count=exceptions_count,
            integrity_manifest_hash=manifest_hash,
            limitations=[
                "Evidence validity limited to empirical observation window.",
                "Third-party external dependencies evaluated via active boundary telemetry.",
            ],
        )
