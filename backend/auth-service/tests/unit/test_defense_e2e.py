import pytest
from app.services.adaptive_defense.adaptive_defense_fabric import AdaptiveDefenseFabric


def test_closed_loop_adaptive_defense_e2e():
    fabric = AdaptiveDefenseFabric()
    tenant = "tenant_e2e_corp"

    # 1. Capture baseline environment snapshot
    snap = fabric.discovery.capture_snapshot(tenant, assets=["srv-web-01", "srv-db-01"], endpoints=["ep-admin-01"])
    assert snap.version == 1

    # 2. Record security drift event
    drift = fabric.drift.record_drift(tenant, "EXPOSURE_DRIFT", "ep-admin-01", "RESTRICTED", "PUBLIC_EXPOSURE", "HIGH")
    assert drift.severity == "HIGH"

    # 3. Calculate attack surface
    surface = fabric.exposure.calculate_attack_surface(tenant, exposed_assets=3, control_coverage_pct=85.0)
    assert surface.overall_attack_surface_score > 0.0

    # 4. Generate recommendation
    rec = fabric.create_recommendation(
        tenant_id=tenant,
        title="Restrict exposed management port on ep-admin-01",
        action_classification="NETWORK_CONTROL",
        target_resource="ep-admin-01",
        automation_level="LEVEL_4_AUTOMATIC_SAFE_ACTION",
        evidence_references=[drift.drift_id],
    )

    # 5. Execute closed-loop adaptation
    result = fabric.execute_closed_loop_defense(rec.recommendation_id)
    assert result["status"] == "COMPLETED"
    assert result["verification"] == "VERIFIED"
    assert result["effectiveness"].overall_effectiveness > 80.0

    # 6. Verify Posture Updated
    pos = fabric.posture.get_or_create_posture(tenant)
    assert pos.control_health >= 0.95

    # 7. Summary metrics check
    summary = fabric.get_summary(tenant)
    assert summary.active_adaptations_count >= 1
    assert summary.circuit_breaker_status == "CLOSED"
    assert summary.kill_switch_active is False
