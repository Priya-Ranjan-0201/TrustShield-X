"""Unit tests for JNI Evidence Preservation (Phase 3.9 Part 1A.25)."""

import pytest
from app.schemas.evidence_consolidation_models import CanonicalEvidenceDTO


def test_jni_evidence_dto():
    ev = CanonicalEvidenceDTO(
        evidence_id="ev_jni_1",
        canonical_entity_id="entity_jni_1",
        source_module="JNI_INTELLIGENCE",
        evidence_type="JNI",
        evidence_subtype="NATIVE_METHOD_REGISTRATION",
        provenance_reference="System.loadLibrary(native-lib)",
    )

    assert ev.evidence_type == "JNI"
