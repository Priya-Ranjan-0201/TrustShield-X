"""Unit tests for Third-Party SDK Flows (Phase 3.9 Part 1A.21)."""

import pytest
from app.schemas.dataflow_models import ThirdPartyDataflowDTO


def test_third_party_flow_dto():
    tp = ThirdPartyDataflowDTO(
        source_id="src_1",
        sdk_name="Google Analytics",
        sdk_category="ANALYTICS",
        target_endpoint="https://app-measurement.com/a",
    )

    assert tp.sdk_category == "ANALYTICS"
