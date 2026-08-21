import pytest
from app.services.fusion.security_health_engine import SecurityHealthEngine


def test_data_quality_defect_detection():
    engine = SecurityHealthEngine()

    records = [
        {"id": "rec_01", "tenant_id": "tenant_dq", "timestamp": "2026-08-15T12:00:00Z"},
        {"id": "rec_02", "timestamp": "2026-08-15T12:00:00Z"},  # Missing tenant_id
        {"id": "rec_03", "tenant_id": "tenant_dq"},  # Missing timestamp
    ]

    findings = engine.validate_data_quality(records, "tenant_dq")
    assert len(findings) == 2
    assert any(f.quality_issue == "MISSING_TENANT_ID" for f in findings)
    assert any(f.quality_issue == "MISSING_TIMESTAMP" for f in findings)
