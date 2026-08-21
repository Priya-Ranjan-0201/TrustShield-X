"""
TruthShield X — Exposure Control & Attack Surface Engine (Phase 17).

Evaluates exposed surfaces, internet-facing assets, and computes multidimensional attack surface scores.
"""

from typing import Dict, List, Optional
from datetime import datetime, timezone

from app.schemas.adaptive_defense_models import AttackSurfaceScoreDTO


class ExposureControlEngine:
    """Computes multidimensional attack surface scores and prioritizes exposures."""

    def __init__(self):
        self._scores: Dict[str, AttackSurfaceScoreDTO] = {}

    def calculate_attack_surface(
        self,
        tenant_id: str = "default_tenant",
        exposed_assets: int = 5,
        exposed_services: int = 4,
        unpatched_vulnerabilities: int = 2,
        identity_risks: int = 1,
        third_party_deps: int = 8,
        cloud_assets: int = 10,
        control_coverage_pct: float = 90.0,
    ) -> AttackSurfaceScoreDTO:
        """Calculates multi-dimensional attack surface score (0 to 100)."""
        asset_score = min(100.0, exposed_assets * 4.0)
        service_score = min(100.0, exposed_services * 3.5)
        vuln_score = min(100.0, unpatched_vulnerabilities * 12.0)
        ident_score = min(100.0, identity_risks * 10.0)
        tp_score = min(100.0, third_party_deps * 1.5)
        cloud_score = min(100.0, cloud_assets * 1.8)

        # Weighted calculation
        raw_exposure = (
            asset_score * 0.20
            + service_score * 0.20
            + vuln_score * 0.25
            + ident_score * 0.15
            + tp_score * 0.10
            + cloud_score * 0.10
        )

        # Control coverage mitigates raw exposure
        mitigation_factor = control_coverage_pct / 100.0
        overall = max(0.0, min(100.0, raw_exposure * (1.2 - 0.5 * mitigation_factor)))

        score = AttackSurfaceScoreDTO(
            tenant_id=tenant_id,
            exposed_assets_score=round(asset_score, 1),
            exposed_services_score=round(service_score, 1),
            vulnerabilities_score=round(vuln_score, 1),
            identity_exposure_score=round(ident_score, 1),
            third_party_exposure_score=round(tp_score, 1),
            cloud_exposure_score=round(cloud_score, 1),
            control_coverage_score=round(control_coverage_pct, 1),
            overall_attack_surface_score=round(overall, 1),
        )

        self._scores[tenant_id] = score
        return score

    def get_score(self, tenant_id: str = "default_tenant") -> Optional[AttackSurfaceScoreDTO]:
        return self._scores.get(tenant_id)
