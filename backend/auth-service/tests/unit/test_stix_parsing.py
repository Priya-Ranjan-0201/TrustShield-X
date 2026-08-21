"""Unit tests for STIX Object Parsing (Phase 3.9 Part 1A.23)."""

import pytest
from app.schemas.threat_intelligence_models import StixObjectDTO


def test_stix_object_dto():
    st = StixObjectDTO(
        object_id="indicator--1111",
        object_type="indicator",
        name="Phishing Domain Indicator",
    )

    assert st.object_id == "indicator--1111"
    assert st.object_type == "indicator"
