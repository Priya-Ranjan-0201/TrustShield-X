"""
TruthShield X — Attack Scenario Engine & Library (Phase 18).

Catalog of versioned defensive simulation scenarios with initial condition modeling and AI-generated scenario safety tagging.
"""

from typing import Dict, List, Optional
from datetime import datetime, timezone
import uuid

from app.schemas.cyber_resilience_twin_models import (
    ScenarioModelDTO,
    InitialConditionLiteral,
)


class AttackScenarioEngine:
    """Manages defensive simulation scenarios, versioning, and AI scenario proposals."""

    def __init__(self):
        # scenario_id -> ScenarioModelDTO
        self._scenarios: Dict[str, ScenarioModelDTO] = {}
        self._initialize_default_scenarios()

    def _initialize_default_scenarios(self):
        defaults = [
            ScenarioModelDTO(
                scenario_id="scen_phishing_01",
                scenario_type="PHISHING_CAMPAIGN",
                initial_conditions="CURRENT_STATE",
                assumptions=["Employee clicks credential phishing link", "MFA bypass attempted"],
                affected_assets=["workstation-user-pool", "identity-provider"],
                threat_model="FINANCIAL_PHISHING_ACTOR",
                control_dependencies=["MFA_POLICY", "EDR_AGENT", "EMAIL_GATEWAY"],
                confidence=0.90,
            ),
            ScenarioModelDTO(
                scenario_id="scen_ransomware_01",
                scenario_type="RANSOMWARE_DISRUPTION",
                initial_conditions="CURRENT_STATE",
                assumptions=["Lateral movement via SMB", "Volume shadow copies targeted"],
                affected_assets=["file-server-share", "backup-target-01"],
                threat_model="EXTORTION_RANSOMWARE_GROUP",
                control_dependencies=["NETWORK_SEGMENTATION", "IMMUTABLE_BACKUP", "EDR_QUARANTINE"],
                confidence=0.85,
            ),
            ScenarioModelDTO(
                scenario_id="scen_api_abuse_01",
                scenario_type="API_COMPROMISE",
                initial_conditions="CUSTOM_SANDBOX_STATE",
                assumptions=["JWT signing key leaked", "Automated credential stuffing on /v1/auth"],
                affected_assets=["api-gateway-ingress", "auth-service"],
                threat_model="BOTNET_CREDENTIAL_STUFFING",
                control_dependencies=["RATE_LIMITER", "WAF_SHIELD", "KEY_ROTATION"],
                confidence=0.92,
            ),
        ]
        for s in defaults:
            self._scenarios[s.scenario_id] = s

    def register_scenario(
        self,
        scenario_type: str,
        initial_conditions: InitialConditionLiteral = "CURRENT_STATE",
        assumptions: Optional[List[str]] = None,
        affected_assets: Optional[List[str]] = None,
        threat_model: str = "GENERIC_THREAT",
        is_ai_generated: bool = False,
    ) -> ScenarioModelDTO:
        """Registers a new versioned simulation scenario."""
        scenario = ScenarioModelDTO(
            scenario_type=scenario_type,
            initial_conditions=initial_conditions,
            assumptions=assumptions or ["Standard defense operating baseline."],
            affected_assets=affected_assets or ["endpoint_generic"],
            threat_model=threat_model,
            is_ai_generated=is_ai_generated,
        )
        self._scenarios[scenario.scenario_id] = scenario
        return scenario

    def get_scenario(self, scenario_id: str) -> Optional[ScenarioModelDTO]:
        return self._scenarios.get(scenario_id)

    def list_scenarios(self) -> List[ScenarioModelDTO]:
        return list(self._scenarios.values())
