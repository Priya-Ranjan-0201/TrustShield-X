"""Unit tests for Full End-to-End Audit Traceability (Phase 3.9 Part 1C)."""

import pytest
from app.services.risk_aggregation_orchestrator import RiskAggregationOrchestrator


def test_audit_traceability_record():
    orchestrator = RiskAggregationOrchestrator()
    res = orchestrator.run_risk_assessment(None)

    assert res.audit_record is not None
    assert "Evaluated" in res.audit_record.audit_trail_text
