"""Unit tests for Permission + Dataflow Correlation (Phase 3.9 Part 1A.22)."""

import pytest
from app.schemas.behavioral_correlation_models import BehaviorFindingDTO


def test_permission_dataflow_finding_dto():
    finding = BehaviorFindingDTO(
        finding_id="find_1",
        finding_type="SMS_DATA_NETWORK_FLOW",
        category="SMS_DATA_FLOW",
        evidence_strength="DIRECT",
        summary="SMS data reaches network",
    )

    assert finding.finding_type == "SMS_DATA_NETWORK_FLOW"
    assert finding.evidence_strength == "DIRECT"
