"""
TruthShield X — Security Gap Engine (Phase 25).

Discovers and multidimensionally prioritizes security gaps across telemetry, drift, incidents, and validations.
"""

from typing import Dict, List, Optional
from datetime import datetime, timezone
from app.schemas.security_engineering_models import SecurityGapDTO


class SecurityGapEngine:
    """Identifies and scores architectural and operational security gaps."""

    def __init__(self):
        self._gaps: Dict[str, SecurityGapDTO] = {}
        self._seed_default_gaps()

    def _seed_default_gaps(self):
        g1 = SecurityGapDTO(
            gap_id="gap_credential_staging_blindspot",
            tenant_id="default_tenant",
            source="THREAT_INTELLIGENCE",
            title="Unmonitored Credential Staging Memory Pattern",
            description="Campaign intelligence indicates adversary group AP-44 uses reflective DLL injection unmapped in active detection rules.",
            severity="HIGH",
            exploitability=0.85,
            exposure=0.70,
            business_impact=0.90,
            likelihood=0.80,
            confidence=0.95,
            affected_assets=["ast_api_gateway", "ast_auth_cluster"],
            remediation_complexity="LOW",
            total_gap_score=8.4,
        )
        self._gaps[g1.gap_id] = g1

    def create_gap(
        self,
        title: str,
        description: str,
        source: str = "FAILED_VALIDATION",
        severity: str = "HIGH",
        exploitability: float = 0.8,
        exposure: float = 0.7,
        business_impact: float = 0.85,
        likelihood: float = 0.75,
        confidence: float = 0.95,
        affected_assets: Optional[List[str]] = None,
        tenant_id: str = "default_tenant",
    ) -> SecurityGapDTO:
        # Multi-dimensional score calculation
        gap_score = round(((exploitability * 0.25) + (exposure * 0.25) + (business_impact * 0.3) + (likelihood * 0.2)) * 10.0, 1)
        dto = SecurityGapDTO(
            tenant_id=tenant_id,
            source=source,  # type: ignore
            title=title,
            description=description,
            severity=severity,  # type: ignore
            exploitability=exploitability,
            exposure=exposure,
            business_impact=business_impact,
            likelihood=likelihood,
            confidence=confidence,
            affected_assets=affected_assets or [],
            total_gap_score=gap_score,
            created_at=datetime.now(timezone.utc).isoformat(),
        )
        self._gaps[dto.gap_id] = dto
        return dto

    def get_gap(self, gap_id: str) -> Optional[SecurityGapDTO]:
        return self._gaps.get(gap_id)

    def list_gaps(self, tenant_id: str = "default_tenant") -> List[SecurityGapDTO]:
        return [g for g in self._gaps.values() if g.tenant_id == tenant_id or g.tenant_id == "default_tenant"]
