import pytest
from app.services.federation.intelligence_quarantine_engine import IntelligenceQuarantineEngine


def test_quarantine_release_workflow():
    engine = IntelligenceQuarantineEngine()

    batch = [{"indicator": "bad_ioc.com", "timestamp": "2099-01-01T00:00:00Z"}]  # Impossible timestamp
    entry = engine.inspect_and_quarantine("src_suspicious", batch)
    assert entry.status == "QUARANTINED"

    # Analyst approves release after remediation
    released = engine.release_from_quarantine(entry.quarantine_id, reviewed_by="sr_analyst", approve=True)
    assert released.status == "APPROVED"
    assert released.reviewed_by == "sr_analyst"
