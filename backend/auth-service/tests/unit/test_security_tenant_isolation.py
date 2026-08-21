import pytest
from app.services.fusion.event_normalization_service import EventNormalizationService
from app.services.fusion.threat_fusion_engine import ThreatFusionEngine


def test_security_event_tenant_isolation():
    service = EventNormalizationService()

    # Ingest under Tenant A
    ev_a = service.ingest_and_normalize("DETECTION", "WEB", entity_id="secret-tenant-a.com", tenant_id="tenant_a")

    # Ingest under Tenant B
    ev_b = service.ingest_and_normalize("DETECTION", "WEB", entity_id="secret-tenant-b.com", tenant_id="tenant_b")

    events_a = service.list_events(tenant_id="tenant_a")
    events_b = service.list_events(tenant_id="tenant_b")

    assert len(events_a) == 1
    assert events_a[0].entity_id == "secret-tenant-a.com"

    assert len(events_b) == 1
    assert events_b[0].entity_id == "secret-tenant-b.com"
