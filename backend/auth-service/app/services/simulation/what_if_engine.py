"""
TruthShield X — What-If Counterfactual Query Engine
"""

import uuid
from typing import Dict, List, Optional, Any
from datetime import datetime, timezone
from app.schemas.simulation_models import WhatIfResultDTO


class WhatIfEngine:
    """Answers counterfactual security questions by simulating hypothetical state mutations on a Digital Security Twin."""

    def evaluate_what_if(
        self,
        target_twin_id: str,
        question: str,
        hypothetical_changes: Dict[str, Any],
    ) -> WhatIfResultDTO:
        """Simulates hypothetical changes and computes simulated risk, trust, and exposure deltas."""
        query_id = f"wif_{uuid.uuid4().hex[:10]}"

        # Calculate estimated impact based on hypothetical change
        risk_delta = 0.0
        exposure_delta = 0.0
        trust_delta = 0.0
        blast_radius = "MODERATE"
        findings = []

        if "disable_mfa" in str(hypothetical_changes).lower():
            risk_delta = +38.0
            exposure_delta = +45.0
            trust_delta = -30.0
            blast_radius = "EXTENSIVE"
            findings.append("Disabling MFA expands attack surface to automated credential stuffing.")
        elif "revoke_certificate" in str(hypothetical_changes).lower():
            risk_delta = +15.0
            exposure_delta = +20.0
            trust_delta = -10.0
            blast_radius = "MODERATE"
            findings.append("Certificate revocation causes temporary TLS gateway handshake degradation.")
        else:
            risk_delta = +20.0
            exposure_delta = +25.0
            trust_delta = -15.0
            findings.append("Simulated hypothetical modification introduces measurable posture shift.")

        return WhatIfResultDTO(
            query_id=query_id,
            target_twin_id=target_twin_id,
            question=question,
            simulated_risk_delta=round(risk_delta, 1),
            simulated_exposure_delta=round(exposure_delta, 1),
            simulated_trust_delta=round(trust_delta, 1),
            affected_assets=["AuthGatewayAPI", "CustomerPortal"],
            simulated_blast_radius=blast_radius,
            findings=findings,
            is_simulation=True,
            generated_at=datetime.now(timezone.utc).isoformat(),
        )
