"""
Blast Radius Calculator Engine (Phase 34)
=========================================
Computes potential compromise blast radius, distinguishing OBSERVED, POSSIBLE,
and SIMULATED reachability across assets, identities, and crown jewels.
"""

from typing import Dict, Any, List, Optional
import datetime
from app.schemas.zero_trust_exposure_models import BlastRadiusDTO


class BlastRadiusCalculatorEngine:
    def __init__(self):
        self._calculations: Dict[str, Dict[str, Any]] = {}

    def calculate_blast_radius(
        self,
        node_or_calc_id: Optional[str] = None,
        tenant_id: str = "org_default",
        source_asset_id: Optional[str] = None,
        mode: str = "SIMULATED",  # OBSERVED, POSSIBLE, SIMULATED
        reachable_assets: Optional[List[str]] = None,
        reachable_identities: Optional[List[str]] = None,
        reachable_crown_jewels: Optional[List[str]] = None,
        neighbors: Optional[List[str]] = None,
        data_stores: Optional[List[str]] = None,
        radius_id: Optional[str] = None,
        compromised_asset_id: Optional[str] = None,
        directly_connected_assets: Optional[List[str]] = None,
        downstream_services: Optional[List[str]] = None,
        **kwargs
    ) -> Dict[str, Any]:
        calc_id = radius_id or node_or_calc_id or "BLAST-01"
        src_id = compromised_asset_id or source_asset_id or node_or_calc_id or "ASSET-01"

        r_assets = reachable_assets or directly_connected_assets or neighbors or []
        r_identities = reachable_identities or []
        r_jewels = reachable_crown_jewels or data_stores or []
        downstream = downstream_services or []

        total_nodes = len(r_assets) + len(r_jewels) + len(r_identities) + len(downstream)
        mult_factor = 1.0 + (len(r_jewels) * 1.5) + (len(r_assets) * 0.2) + (len(r_identities) * 0.3) + (len(downstream) * 0.2)
        blast_radius_score = min(10.0, total_nodes * 1.5)

        if blast_radius_score >= 7.0 or len(r_assets) >= 3 or len(r_jewels) >= 1:
            impact_scope = "CRITICAL"
        elif blast_radius_score >= 4.0:
            impact_scope = "HIGH"
        elif blast_radius_score >= 2.0:
            impact_scope = "MEDIUM"
        else:
            impact_scope = "LOW"

        containment_recommended = (impact_scope in ["HIGH", "CRITICAL"])

        record = {
            "calculation_id": calc_id,
            "radius_id": calc_id,
            "tenant_id": tenant_id,
            "source_asset_id": src_id,
            "compromised_asset_id": src_id,
            "mode": mode if mode in ["OBSERVED", "POSSIBLE", "SIMULATED"] else "SIMULATED",
            "reachable_assets": r_assets,
            "directly_connected_assets": r_assets,
            "reachable_identities": r_identities,
            "reachable_crown_jewels": r_jewels,
            "downstream_services": downstream,
            "risk_multiplication_factor": round(mult_factor, 2),
            "blast_radius_score": blast_radius_score,
            "impact_scope": impact_scope,
            "containment_recommended": containment_recommended,
            "calculated_at": datetime.datetime.now(datetime.timezone.utc).isoformat()
        }
        self._calculations[calc_id] = record
        return record


    def get_calculation(self, calculation_id: str, tenant_id: str) -> Optional[Dict[str, Any]]:
        calc = self._calculations.get(calculation_id)
        if calc and calc["tenant_id"] == tenant_id:
            return calc
        return None


blast_radius_calculator_engine = BlastRadiusCalculatorEngine()
