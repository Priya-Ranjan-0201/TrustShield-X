"""
TruthShield X — Security Scenario Engine (Phase 26).

Manages deterministic, reproducible scenario definitions across 14 functional categories with explicit assumptions.
"""

from typing import Dict, List, Optional, Any
from datetime import datetime, timezone
from app.schemas.digital_twin_lab_models import SecurityScenarioDTO, ScenarioCategoryLiteral


class SecurityScenarioEngine:
    """Configures deterministic attack and failure scenarios for digital twin simulation."""

    def __init__(self):
        self._scenarios: Dict[str, SecurityScenarioDTO] = {}
        self._seed_default_scenario()

    def _seed_default_scenario(self):
        sc1 = SecurityScenarioDTO(
            scenario_id="scen_phishing_lateral_movement",
            tenant_id="default_tenant",
            name="Phishing Credential Stuffing & Lateral Movement Drill",
            category="ATTACK",
            objective="Model blast radius and detection efficacy during compromised credential propagation.",
            initial_state_version="v1.0.0-PROD-SYNC",
            assumptions=["Attacker holds valid low-privilege employee credentials", "WAF is active"],
            inputs={"initial_node": "ast_api_gw", "credential_type": "EMPLOYEE_SESSION_TOKEN"},
            constraints={"max_lateral_hops": 3, "max_graph_nodes": 50},
            expected_outputs=["containment_time_seconds", "affected_assets_count"],
            safety_classification="SANDBOX_ISOLATED",
            status="READY",
        )
        self._scenarios[sc1.scenario_id] = sc1

    def create_scenario(
        self,
        name: str,
        category: ScenarioCategoryLiteral,
        objective: str,
        initial_state_version: str = "v1.0.0-PROD-SYNC",
        assumptions: Optional[List[str]] = None,
        inputs: Optional[Dict[str, Any]] = None,
        constraints: Optional[Dict[str, Any]] = None,
        safety_classification: str = "SANDBOX_ISOLATED",
        tenant_id: str = "default_tenant",
    ) -> SecurityScenarioDTO:
        dto = SecurityScenarioDTO(
            tenant_id=tenant_id,
            name=name,
            category=category,
            objective=objective,
            initial_state_version=initial_state_version,
            assumptions=assumptions or ["Simulation parameters strictly bounded to sandbox scopes"],
            inputs=inputs or {},
            constraints=constraints or {"max_lateral_hops": 3, "max_graph_nodes": 50},
            safety_classification=safety_classification,  # type: ignore
            status="READY",
            created_at=datetime.now(timezone.utc).isoformat(),
        )
        self._scenarios[dto.scenario_id] = dto
        return dto

    def get_scenario(self, scenario_id: str) -> Optional[SecurityScenarioDTO]:
        return self._scenarios.get(scenario_id)

    def list_scenarios(self, tenant_id: str = "default_tenant") -> List[SecurityScenarioDTO]:
        return [s for s in self._scenarios.values() if s.tenant_id == tenant_id or s.tenant_id == "default_tenant"]
