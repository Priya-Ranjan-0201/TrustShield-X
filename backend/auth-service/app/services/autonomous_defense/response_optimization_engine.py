"""
TruthShield X — Response Optimization Engine (Phase 30).

Evaluates historical incident response effectiveness and recommends optimized playbooks based on containment time and side-effects.
"""

from typing import Dict, List, Optional, Any
from app.schemas.autonomous_defense_models import ResponseOptimizationDTO, ResponseEffectivenessLiteral


class ResponseOptimizationEngine:
    """Measures actual response metrics (TTD, TTC, TTR) and optimizes automated containment playbooks."""

    def __init__(self):
        self._responses: Dict[str, ResponseOptimizationDTO] = {}
        self._seed_default_response()

    def _seed_default_response(self):
        r1 = ResponseOptimizationDTO(
            response_id="rsp_darkstorm_waf",
            playbook_name="DarkStorm Credential Stuffing Joint Mitigation Playbook",
            containment_time_sec=42.0,
            recovery_time_sec=120.0,
            effectiveness="RESPONSE_EFFECTIVE",
            side_effects=[],
        )
        self._responses[r1.response_id] = r1

    def evaluate_response_outcome(
        self,
        response_id: str,
        playbook_name: str,
        containment_time_sec: float,
        recovery_time_sec: float,
        has_collateral_impact: bool = False,
        is_outcome_verified: bool = True,
    ) -> ResponseOptimizationDTO:
        if not is_outcome_verified:
            eff: ResponseEffectivenessLiteral = "OUTCOME_NOT_VERIFIED"
        elif has_collateral_impact:
            eff = "RESPONSE_PARTIALLY_EFFECTIVE"
        elif containment_time_sec < 60.0:
            eff = "RESPONSE_EFFECTIVE"
        else:
            eff = "RESPONSE_INEFFECTIVE"

        dto = ResponseOptimizationDTO(
            response_id=response_id,
            playbook_name=playbook_name,
            containment_time_sec=containment_time_sec,
            recovery_time_sec=recovery_time_sec,
            effectiveness=eff,
            side_effects=["Service disruption on secondary tenant"] if has_collateral_impact else [],
        )
        self._responses[response_id] = dto
        return dto

    def get_response_metrics(self, response_id: str) -> Optional[ResponseOptimizationDTO]:
        return self._responses.get(response_id)
