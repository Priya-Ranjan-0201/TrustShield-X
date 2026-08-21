"""Unit tests for Risk Audit Trail Generation (Phase 3.9 Part 1B)."""

import pytest
from app.schemas.risk_aggregation_models import RiskAuditRecordDTO


def test_risk_audit_record_dto():
    audit = RiskAuditRecordDTO(
        audit_id="audit_1",
        policy_version="1.0.0",
        audit_trail_text="Full decision audit trail text",
    )

    assert audit.audit_id == "audit_1"
    assert audit.policy_version == "1.0.0"
