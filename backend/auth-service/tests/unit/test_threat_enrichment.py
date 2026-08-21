import pytest
from app.services.soc.security_operations_orchestrator import SecurityOperationsOrchestrator


def test_threat_enrichment_on_alert_ingestion():
    orch = SecurityOperationsOrchestrator()
    alert = orch.ingest_alert(
        tenant_id="tenant_ti",
        source="THREAT_INTEL_MISP",
        asset="srv_vpn_gateway",
        severity="CRITICAL",
        indicator="c2.shadowhydra.net",
    )

    assert alert.indicator == "c2.shadowhydra.net"
    assert alert.source == "THREAT_INTEL_MISP"
