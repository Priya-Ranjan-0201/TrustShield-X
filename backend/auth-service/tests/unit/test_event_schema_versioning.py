import pytest
from app.services.fusion.realtime_event_stream_service import RealTimeEventStreamService


def test_unsupported_event_schema_routes_to_dlq():
    service = RealTimeEventStreamService()

    # Publishing with invalid/unsupported schema version
    res = service.publish_event(
        event_payload={"event_type": "DETECTION", "source": "TEST"},
        schema_version="security.event.v999_unsupported",
        tenant_id="tenant_schema",
    )
    assert res["status"] == "DEAD_LETTER"
    assert "Unsupported schema version" in res["reason"]
