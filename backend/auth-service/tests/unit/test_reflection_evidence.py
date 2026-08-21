"""Unit tests for Reflection Evidence Preservation (Phase 3.9 Part 1A.25)."""

import pytest
from app.schemas.evidence_consolidation_models import CanonicalEvidenceDTO


def test_reflection_evidence_dto():
    ev = CanonicalEvidenceDTO(
        evidence_id="ev_refl_1",
        canonical_entity_id="entity_refl_1",
        source_module="REFLECTION_INTELLIGENCE",
        evidence_type="REFLECTION",
        evidence_subtype="METHOD_INVOCATION",
        provenance_reference="Class.forName().getMethod().invoke()",
    )

    assert ev.evidence_type == "REFLECTION"
