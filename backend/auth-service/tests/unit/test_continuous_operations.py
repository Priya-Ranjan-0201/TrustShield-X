"""
TruthShield X — Continuous Operations & Self-Healing Unit Tests
===============================================================
Validates:
- ProductionHealthEngine (12 subsystems, probe assertions, 6D executive health scores)
- SecurityInvariantEngine (7 absolute invariants, violation incident generation)
- ContinuousDriftEngine (Configuration drift, release drift, database drift, feed drift, twin drift, AI drift)
- ContinuousValidationOrchestrator (Cycle orchestration, synthetic multi-tenant isolation, safe self-healing, lockdown, maintenance mode)
"""

import pytest
import datetime
from app.services.continuous_operations import (
    production_health_engine,
    security_invariant_engine,
    continuous_drift_engine,
    continuous_validation_orchestrator,
    HealthState,
)


def test_production_health_engine_probing():
    audit = production_health_engine.run_full_system_health_audit()
    assert audit["overall_status"] in ["HEALTHY", "DEGRADED", "FAILED"]
    assert audit["subsystems_evaluated"] == 12
    assert "API" in audit["subsystem_health"]
    assert "DATABASE" in audit["subsystem_health"]
    assert "AI_PROVIDERS" in audit["subsystem_health"]
    assert "DIGITAL_TWIN" in audit["subsystem_health"]

    # Probe override test
    rec = production_health_engine.probe_subsystem("API", override_status="HEALTHY")
    assert rec["status"] == "HEALTHY"

    # Executive health scores test
    scores = production_health_engine.calculate_executive_health_scores()
    for dim in ["SECURITY", "AVAILABILITY", "RESILIENCE", "AI_SAFETY", "DATA_INTEGRITY", "OPERATIONAL_READINESS"]:
        assert dim in scores
        assert 0.0 <= scores[dim] <= 100.0


def test_security_invariants_verification():
    result = security_invariant_engine.verify_all_invariants(tenant_id="tenant-alpha")
    assert result["invariants_verified_count"] == 7
    assert result["all_invariants_passed"] is True

    # Test synthetic violation injection
    violation_test = security_invariant_engine.verify_invariant(
        "NO_CROSS_TENANT_ACCESS",
        tenant_id="tenant-beta",
        synthetic_context={"force_violation": True, "violation_reason": "Synthetic tenant leak test"}
    )
    assert violation_test["passed"] is False
    assert len(security_invariant_engine.get_violations()) > 0
    assert len(security_invariant_engine.get_incidents()) > 0


def test_continuous_drift_engine():
    # 1. Config drift
    cfg_drift = continuous_drift_engine.check_configuration_drift(
        tenant_id="tenant-alpha",
        current_config={"autonomy_level": "LEVEL_4", "rbac_rules": "MODIFIED"},
        approved_baseline={"autonomy_level": "LEVEL_2", "rbac_rules": "DEFAULT"}
    )
    assert cfg_drift["drift_detected"] is True
    assert len(cfg_drift["diffs"]) == 2

    # 2. Database drift
    db_drift = continuous_drift_engine.check_database_schema_drift(actual_table_count=376, expected_table_count=376)
    assert db_drift["drift_detected"] is False

    db_drift_bad = continuous_drift_engine.check_database_schema_drift(actual_table_count=350, expected_table_count=376)
    assert db_drift_bad["drift_detected"] is True

    # 3. Feed staleness
    old_time = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(hours=8)
    feed_drift = continuous_drift_engine.check_threat_intelligence_staleness("AlienVault_OTX", old_time, max_age_hours=6.0)
    assert feed_drift["is_stale"] is True

    # 4. Digital twin fidelity
    twin_drift = continuous_drift_engine.check_digital_twin_fidelity(live_asset_count=100, twin_asset_count=100)
    assert twin_drift["drift_detected"] is False


def test_continuous_validation_orchestrator():
    # 1. Validation cycle
    cycle = continuous_validation_orchestrator.run_continuous_validation_cycle(tenant_id="tenant-gamma")
    assert "validation_cycle_id" in cycle
    assert cycle["tenant_isolation_passed"] is True
    assert cycle["ai_safety_passed"] is True

    # 2. Safe self-healing
    heal_res = continuous_validation_orchestrator.execute_safe_self_healing(
        action_type="RESTART_UNHEALTHY_WORKER",
        target="worker_celery_01"
    )
    assert heal_res["success"] is True
    assert heal_res["post_remediation_verified"] is True

    # Unsafe self-healing rejection
    unsafe_heal = continuous_validation_orchestrator.execute_safe_self_healing(
        action_type="DELETE_PRODUCTION_DATABASE_TABLE",
        target="users"
    )
    assert unsafe_heal["success"] is False

    # 3. Emergency lockdown
    lockdown = continuous_validation_orchestrator.trigger_emergency_lockdown("Simulated nation-state breach detected")
    assert lockdown["lockdown_active"] is True
    assert continuous_validation_orchestrator.is_emergency_lockdown is True

    unlock = continuous_validation_orchestrator.deactivate_emergency_lockdown("VALID_TOKEN")
    assert unlock["lockdown_active"] is False
    assert continuous_validation_orchestrator.is_emergency_lockdown is False

    # 4. Maintenance mode
    maint = continuous_validation_orchestrator.set_maintenance_mode(enabled=True)
    assert maint["maintenance_mode"] is True
    continuous_validation_orchestrator.set_maintenance_mode(enabled=False)
