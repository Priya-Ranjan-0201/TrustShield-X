import pytest
from app.services.fusion.security_operations_fabric import SecurityOperationsFabric


def test_security_operations_fabric_full_e2e():
    fabric = SecurityOperationsFabric()

    # Ingest telemetry across multiple modalities for coordinated attack
    res1 = fabric.process_incoming_security_telemetry(
        event_type="DETECTION",
        source="WEB",
        entity_id="fraud-hdfc-kyc.com",
        asset_id="ast_corp_01",
        campaign_id="CAMP-2026-0891",
        severity="CRITICAL",
        confidence=0.98,
        risk_score=92.0,
        trust_score=20.0,
        exposure_score=85.0,
        tenant_id="tenant_e2e",
    )

    res2 = fabric.process_incoming_security_telemetry(
        event_type="DETECTION",
        source="APK",
        entity_id="apk:banking_trojan_sha256",
        asset_id="ast_corp_01",
        campaign_id="CAMP-2026-0891",
        severity="CRITICAL",
        confidence=0.96,
        risk_score=88.0,
        trust_score=15.0,
        exposure_score=80.0,
        tenant_id="tenant_e2e",
    )

    assert res2["event"] is not None
    assert res2["cluster"] is not None
    assert res2["cluster"].fusion_score >= 70.0
    assert len(res2["cluster"].modalities) >= 2
    assert res2["situation"].overall_threat_level in ("ELEVATED", "HIGH", "CRITICAL")
    assert res2["posture"].overall_posture_score <= 85.0
