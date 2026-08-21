import pytest
from app.services.simulation.digital_security_twin_service import DigitalSecurityTwinService
from app.services.simulation.simulation_scenario_engine import SimulationScenarioEngine
from app.services.simulation.what_if_engine import WhatIfEngine
from app.services.simulation.response_strategy_simulation_engine import ResponseStrategySimulationEngine
from app.services.simulation.disaster_recovery_simulation_engine import DisasterRecoverySimulationEngine
from app.services.simulation.security_control_effectiveness_engine import SecurityControlEffectivenessEngine


def test_digital_security_twin_complete_e2e():
    twin_service = DigitalSecurityTwinService()
    scenario_engine = SimulationScenarioEngine(twin_service=twin_service)
    what_if_engine = WhatIfEngine()
    strategy_engine = ResponseStrategySimulationEngine()
    dr_engine = DisasterRecoverySimulationEngine()
    control_engine = SecurityControlEffectivenessEngine()

    # 1. Create twin from approved snapshot
    twin = twin_service.create_twin_from_snapshot(
        source_snapshot_id="snap_e2e_01",
        raw_assets=[
            {"name": "CoreBankingGateway", "api_key": "live_secret_bank_key"},
            {"name": "CustomerLedgerDB", "private_ip": "10.10.4.50"},
        ],
        tenant_id="tenant_e2e",
    )
    assert twin.state == "NORMAL"
    assert "live_secret_bank_key" not in str(twin.modeled_assets)

    # 2. Run simulation scenario
    sim_run = scenario_engine.run_scenario(
        twin_id=twin.twin_id,
        scenario_type="PHISHING_CAMPAIGN",
        target_asset="CoreBankingGateway",
    )
    assert sim_run.status == "COMPLETED"
    assert sim_run.risk_delta > 0.0

    # 3. Evaluate what-if counterfactual query
    what_if = what_if_engine.evaluate_what_if(
        target_twin_id=twin.twin_id,
        question="What if CoreBankingGateway WAF rule is bypassed?",
        hypothetical_changes={"bypass_waf": True},
    )
    assert what_if.is_simulation is True
    assert what_if.simulated_risk_delta > 0.0

    # 4. Compare response candidates
    strategies = strategy_engine.evaluate_strategies({"incident_asset": "CoreBankingGateway"})
    assert len(strategies) >= 2
    assert all(0.0 <= s.safety_score <= 1.0 for s in strategies)

    # 5. Simulate disaster recovery failover drill
    dr_res = dr_engine.simulate_component_failover("DATABASE", "PRIMARY_CORRUPTION")
    assert dr_res.status == "RECOVERED_SIMULATION"
    assert dr_res.audit_chain_continuous is True

    # 6. Evaluate control effectiveness
    ctrl_eval = control_engine.evaluate_controls(twin.modeled_controls)
    assert ctrl_eval["overall_modeled_effectiveness"] > 0.75
