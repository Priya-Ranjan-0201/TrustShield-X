import pytest
from app.services.security_engineering.autonomous_security_engineering_engine import AutonomousSecurityEngineeringEngine

def test_autonomous_security_e2e_lifecycle():
    fabric = AutonomousSecurityEngineeringEngine()

    # 1. OBSERVE & IDENTIFY GAP
    gap = fabric.gap_engine.create_gap(
        title="Unmapped Reflective DLL Loading",
        description="Adversary AP-44 memory evasion",
        source="THREAT_INTELLIGENCE",
    )
    assert gap.total_gap_score > 0

    # 2. UNDERSTAND & ROOT CAUSE ANALYSIS
    rca = fabric.root_cause_engine.analyze_root_cause(gap.gap_id, category="ROOT_CAUSE")
    assert rca.category == "ROOT_CAUSE"

    # 3. GENERATE IMPROVEMENT
    imp = fabric.improvement_engine.generate_improvement(
        category="DETECTION",
        title="Add Sigma T1055 Rule",
        description="Targets memory injection",
        problem=gap.description,
        proposed_change="Add sigma_t1055.yml",
        expected_benefit="100% coverage",
        expected_risk="< 0.5% FPR",
    )
    assert imp.confidence >= 0.90

    # 4. ANALYZE IMPACT & BLAST RADIUS
    impact = fabric.impact_engine.analyze_impact(imp.improvement_id)
    assert impact.risk_classification == "LOW_RISK_REVERSIBLE"

    # 5. SIMULATE BEFORE / AFTER IN DIGITAL TWIN
    sim = fabric.simulation_engine.simulate_improvement(imp.improvement_id)
    assert sim.status == "SIMULATED_SUCCESS"
    assert sim.digital_twin_verified is True

    # 6. SECURITY VALIDATION
    val = fabric.validation_engine.validate_change(imp.improvement_id)
    assert val["overall_validation"] == "PASSED"

    # 7. POLICY GOVERNANCE & AUTONOMY
    can_deploy = fabric.autonomy_engine.can_auto_deploy("default_tenant", "TUNE_DETECTION_THRESHOLD", impact.blast_radius_score, impact.requires_human_approval)
    assert can_deploy is True

    # 8. CANARY ROLLOUT
    dep = fabric.rollout_engine.deploy_change(imp.improvement_id, strategy="CANARY")
    assert dep.status == "CANARY_ACTIVE"

    # 9. MEASURE OUTCOME
    outcome = fabric.outcome_engine.measure_outcome(imp.improvement_id, baseline_metric=0.08, expected_metric=0.02, actual_metric=0.02)
    assert outcome.outcome_status == "IMPROVED"

    # 10. INCIDENT & ENGINEERING LEARNING
    learn = fabric.incident_learning_engine.record_incident_learning("inc_test", "Det OK", "Resp OK", "Cont OK", "Rec OK")
    assert learn.learning_id is not None
