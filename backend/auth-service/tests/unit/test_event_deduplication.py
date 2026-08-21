import pytest
from app.services.fusion.event_normalization_service import EventNormalizationService


def test_event_deterministic_deduplication():
    service = EventNormalizationService()

    # First event ingestion
    e1 = service.ingest_and_normalize(
        event_type="OBSERVATION",
        source="PASSIVE_DNS",
        entity_id="example-phish.com",
        asset_id="ast_101",
        provenance={"detector": "v1.0"},
        tenant_id="tenant_dedup",
    )

    # Identical second event ingestion
    e2 = service.ingest_and_normalize(
        event_type="OBSERVATION",
        source="PASSIVE_DNS",
        entity_id="example-phish.com",
        asset_id="ast_101",
        provenance={"detector": "v1.0"},
        tenant_id="tenant_dedup",
    )

    assert e1.event_id == e2.event_id
    assert len(service.list_events(tenant_id="tenant_dedup")) == 1
