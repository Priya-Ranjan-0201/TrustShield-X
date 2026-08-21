import pytest
from app.services.soc.security_operations_orchestrator import SecurityOperationsOrchestrator


def test_alert_normalization_pipeline():
    orch = SecurityOperationsOrchestrator()
    alert = orch.ingest_alert(
        tenant_id="tenant_01",
        source="EDR_CROWDSTRIKE",
        asset="srv_checkout_pod_3",
        severity="HIGH",
        confidence=0.94,
        evidence=["ev_pcap_88", "ev_sig_99"],
        indicator="198.51.100.42",
    )

    assert alert.alert_id.startswith("alt_")
    assert alert.tenant_id == "tenant_01"
    assert alert.severity == "HIGH"
    assert alert.confidence == 0.94
    assert alert.fingerprint is not None
