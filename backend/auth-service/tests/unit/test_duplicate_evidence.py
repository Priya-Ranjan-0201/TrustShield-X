"""Unit tests for Duplicate Evidence Suppression (Phase 3.9 Part 1A.22)."""

import pytest
from app.schemas.behavioral_correlation_models import CorrelationEvidenceDTO


def test_duplicate_evidence_suppression():
    e1 = CorrelationEvidenceDTO(
        evidence_id="ev_1",
        module="API_ENGINE",
        entity_id="api_1",
        class_name="com.bank.Net",
        method_name="send",
        source_location="com/bank/Net.java:12",
        rule_id="RULE_NET",
        provenance="API_ENGINE",
    )
    e2 = CorrelationEvidenceDTO(
        evidence_id="ev_1",
        module="CORRELATION_ENGINE",
        entity_id="api_1",
        class_name="com.bank.Net",
        method_name="send",
        source_location="com/bank/Net.java:12",
        rule_id="RULE_NET",
        provenance="CORRELATION_ENGINE",
    )

    assert e1.evidence_id == e2.evidence_id
