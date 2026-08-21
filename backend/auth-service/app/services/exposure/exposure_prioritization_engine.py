"""
TruthShield X — Exposure Prioritization Engine
"""

import uuid
from typing import Dict, List, Optional
from datetime import datetime, timezone
from app.schemas.exposure_models import ExposureFindingDTO, AssetDTO, AssetChangeDTO


class ExposurePrioritizationEngine:
    """Prioritizes exposure findings based on asset criticality, risk delta, trust drop, and campaign linkages."""

    def __init__(self):
        # tenant_id -> finding_id -> ExposureFindingDTO
        self._findings: Dict[str, Dict[str, ExposureFindingDTO]] = {}

    def create_finding(
        self,
        asset: AssetDTO,
        title: str,
        description: str,
        exposure_score: float,
        risk_score: float,
        trust_score: float,
        change: Optional[AssetChangeDTO] = None,
        campaign_ids: Optional[List[str]] = None,
        recommended_action: Optional[str] = None,
        evidence_ids: Optional[List[str]] = None,
        tenant_id: str = "default_tenant",
    ) -> ExposureFindingDTO:
        """Creates a prioritized exposure finding record."""
        finding_id = f"fnd_{uuid.uuid4().hex[:12]}"
        now_iso = datetime.now(timezone.utc).isoformat()

        # Determine severity based on composite priority formula
        composite_score = (exposure_score * 0.4) + (risk_score * 0.4) + ((100.0 - trust_score) * 0.2)
        if asset.criticality == "CRITICAL":
            composite_score *= 1.25

        if composite_score >= 80.0:
            severity = "CRITICAL"
        elif composite_score >= 60.0:
            severity = "HIGH"
        elif composite_score >= 40.0:
            severity = "MEDIUM"
        else:
            severity = "LOW"

        default_action = recommended_action or (
            f"Review exposure delta on {asset.display_identifier}, initiate firewall/WAF ACL restriction, and verify campaign linkage."
        )

        ev_list = evidence_ids or []
        if change and change.evidence_id not in ev_list:
            ev_list.append(change.evidence_id)

        finding = ExposureFindingDTO(
            finding_id=finding_id,
            asset_id=asset.asset_id,
            tenant_id=tenant_id,
            title=title,
            description=description,
            severity=severity,
            lifecycle_state="NEW",
            exposure_score=exposure_score,
            risk_score=risk_score,
            trust_score=trust_score,
            evidence_ids=ev_list,
            campaign_ids=campaign_ids or [],
            change_id=change.change_id if change else None,
            recommended_action=default_action,
            provenance={"composite_score": composite_score, "asset_criticality": asset.criticality},
            first_seen=now_iso,
            last_seen=now_iso,
        )

        if tenant_id not in self._findings:
            self._findings[tenant_id] = {}
        self._findings[tenant_id][finding_id] = finding

        return finding

    def list_findings(
        self,
        tenant_id: str = "default_tenant",
        severity_filter: Optional[str] = None,
        lifecycle_filter: Optional[str] = None,
    ) -> List[ExposureFindingDTO]:
        """Lists exposure findings sorted by severity and composite risk."""
        tenant_findings = list(self._findings.get(tenant_id, {}).values())
        filtered = []
        for f in tenant_findings:
            if severity_filter and f.severity != severity_filter:
                continue
            if lifecycle_filter and f.lifecycle_state != lifecycle_filter:
                continue
            filtered.append(f)

        severity_rank = {"CRITICAL": 4, "HIGH": 3, "MEDIUM": 2, "LOW": 1}
        filtered.sort(key=lambda x: (severity_rank.get(x.severity, 0), x.exposure_score), reverse=True)
        return filtered

    def update_lifecycle(
        self,
        finding_id: str,
        new_state: str,
        tenant_id: str = "default_tenant",
    ) -> ExposureFindingDTO:
        """Updates finding lifecycle state (e.g. TRIAGED, INVESTIGATING, RESOLVED)."""
        finding = self._findings.get(tenant_id, {}).get(finding_id)
        if not finding:
            raise KeyError(f"Finding '{finding_id}' not found in tenant context.")
        finding.lifecycle_state = new_state  # type: ignore
        finding.last_seen = datetime.now(timezone.utc).isoformat()
        return finding
