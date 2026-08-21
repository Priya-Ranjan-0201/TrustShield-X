"""
TruthShield X — Defensive Hypothesis Engine (Phase 27).

Transforms threat forecasts into testable defensive hypotheses and candidate Digital Twin simulation scenarios.
"""

from typing import Dict, List, Optional
from datetime import datetime, timezone
from app.schemas.global_intelligence_models import DefensiveHypothesisDTO


class DefensiveHypothesisEngine:
    """Generates testable defensive hypotheses connecting threat intelligence to simulation validation."""

    def __init__(self):
        self._hypotheses: Dict[str, DefensiveHypothesisDTO] = {}
        self._seed_default_hypothesis()

    def _seed_default_hypothesis(self):
        h1 = DefensiveHypothesisDTO(
            hypothesis_id="hyp_darkstorm_waf_rate_limit",
            threat_id="cmp_darkstorm_2026",
            hypothesis_statement="If rate-limiting and MFA step-up are enforced, DarkStorm initial credential stuffing containment improves by 85%.",
            testable_criteria="Simulated credential stuffing containment time drops below 30s in Digital Twin Sandbox.",
            digital_twin_scenario_id="scen_phishing_lateral_movement",
            recommended_validation="Phase 26 Digital Twin Simulation -> Phase 24 Control Verification",
            created_at=datetime.now(timezone.utc).isoformat(),
        )
        self._hypotheses[h1.hypothesis_id] = h1

    def generate_hypothesis(
        self,
        threat_id: str,
        statement: str,
        testable_criteria: str,
        digital_twin_scenario_id: Optional[str] = None,
    ) -> DefensiveHypothesisDTO:
        dto = DefensiveHypothesisDTO(
            threat_id=threat_id,
            hypothesis_statement=statement,
            testable_criteria=testable_criteria,
            digital_twin_scenario_id=digital_twin_scenario_id or "scen_phishing_lateral_movement",
            recommended_validation="Phase 26 Digital Twin Simulation Studio -> Phase 25 Autonomous Engineering",
            created_at=datetime.now(timezone.utc).isoformat(),
        )
        self._hypotheses[dto.hypothesis_id] = dto
        return dto

    def list_hypotheses(self) -> List[DefensiveHypothesisDTO]:
        return list(self._hypotheses.values())
