"""
TruthShield X — Digital Exposure Scoring Engine
"""

from typing import Dict, List, Any
from app.schemas.exposure_models import AssetDTO, AssetBaselineDTO


class ExposureScoringEngine:
    """Calculates multi-factor Digital Exposure Scores (0-100) reflecting external reachability and attack surface footprint."""

    CRITICALITY_WEIGHTS = {
        "LOW": 0.8,
        "MEDIUM": 1.0,
        "HIGH": 1.3,
        "CRITICAL": 1.6,
    }

    @classmethod
    def calculate_exposure_score(
        cls,
        asset: AssetDTO,
        baseline: AssetBaselineDTO,
        current_observation: Dict[str, Any],
        has_active_campaign_link: bool = False,
    ) -> Dict[str, Any]:
        """Computes exposure score, contributing factors, and explainability breakdown."""
        base_score = 20.0
        factors: List[str] = []

        # 1. Public Reachability
        is_public = current_observation.get("is_public_facing", True)
        if is_public:
            base_score += 15.0
            factors.append("Asset is directly reachable from the public internet (+15)")

        # 2. Exposed Port / Service Count
        ports = current_observation.get("exposed_ports", baseline.exposed_ports or [])
        port_count = len(ports)
        if port_count > 0:
            port_penalty = min(25.0, port_count * 5.0)
            base_score += port_penalty
            factors.append(f"Exposed {port_count} network ports/services (+{port_penalty:.1f})")

        # 3. High-Risk Services (SSH, RDP, SMB, DB ports)
        high_risk_ports = {22, 3389, 445, 1433, 3306, 5432, 27017, 6379}
        detected_high_risk = [p for p in ports if p in high_risk_ports]
        if detected_high_risk:
            base_score += 20.0
            factors.append(f"Exposed administrative/database ports: {detected_high_risk} (+20)")

        # 4. Campaign Association Linkage
        if has_active_campaign_link:
            base_score += 20.0
            factors.append("Active link to emerging threat campaign infrastructure (+20)")

        # 5. Security Header / TLS Posture
        tls_info = current_observation.get("tls_certificate", baseline.tls_certificate or {})
        if tls_info and tls_info.get("is_expired"):
            base_score += 15.0
            factors.append("Expired or untrusted TLS certificate (+15)")

        # 6. Apply Criticality Multiplier
        crit_multiplier = cls.CRITICALITY_WEIGHTS.get(asset.criticality, 1.0)
        raw_final_score = base_score * crit_multiplier
        final_score = max(0.0, min(100.0, round(raw_final_score, 1)))

        return {
            "exposure_score": final_score,
            "criticality_multiplier": crit_multiplier,
            "contributing_factors": factors,
            "is_public_facing": is_public,
            "port_count": port_count,
        }
