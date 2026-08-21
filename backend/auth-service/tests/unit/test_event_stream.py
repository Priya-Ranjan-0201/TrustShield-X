import pytest
from app.services.fusion.realtime_event_stream_service import RealTimeEventStreamService


def test_real_time_event_publishing():
    service = RealTimeEventStreamService()
    record = service.publish_event(
        event_payload={"event_type": "DETECTION", "source": "API_GATEWAY", "score": 85.0},
        schema_version="security.event.v1",
        tenant_id="tenant_stream",
    )
    assert record["status"] == "STREAMED"
    assert record["stream_id"].startswith("stm_")
