"""Unit tests for Third-Party SDK Evidence Preservation (Phase 3.9 Part 1A.25)."""

import pytest
from app.schemas.evidence_consolidation_models import CanonicalEvidenceDTO


def test_thirdparty_evidence_dto():
    ev = CanonicalEvidenceDTO(
        evidence_id="ev_tp_1",
        canonical_entity_id="entity_sdk_1",
        source_module="API_INTELLIGENCE",
        evidence_type="THIRDPARTY_SDK",
        evidence_subtype="SDK_DETECTION",
        provenance_reference="com.google.firebase.analytics",
    )

    assert ev.evidence_type == "THIRDPARTY_SDK"
