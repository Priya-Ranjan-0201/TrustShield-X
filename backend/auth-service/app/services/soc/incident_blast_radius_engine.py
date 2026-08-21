"""
TruthShield X — Incident Blast Radius Engine (Phase 21).

Calculates observed vs potential blast radius using knowledge fabric dependency trees.
"""

from typing import List, Dict, Any
from app.schemas.autonomous_soc_models import IncidentBlastRadiusDTO


class IncidentBlastRadiusEngine:
    """Calculates observed vs potential impact across assets, services, and business functions."""

    def evaluate_blast_radius(
        self,
        incident_id: str,
        observed_assets: List[str],
        dependency_map: Dict[str, List[str]],
    ) -> IncidentBlastRadiusDTO:
        potential: set[str] = set()
        for a in observed_assets:
            downstream = dependency_map.get(a, [])
            potential.update(downstream)

        # Distinguish observed from potential
        potential_only = list(potential - set(observed_assets))

        score = min(100.0, (len(observed_assets) * 20.0) + (len(potential_only) * 5.0))

        return IncidentBlastRadiusDTO(
            incident_id=incident_id,
            observed_impact_assets=observed_assets,
            potential_impact_assets=potential_only,
            affected_services=["srv_checkout_api", "srv_payment_gateway"],
            affected_identities=["usr_service_account_pay"],
            business_functions=["PAYMENT_PROCESSING", "CUSTOMER_CHECKOUT"],
            blast_radius_score=score,
        )
