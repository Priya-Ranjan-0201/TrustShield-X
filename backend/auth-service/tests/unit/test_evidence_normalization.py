"""Unit tests for Evidence Normalization (Phase 3.9 Part 1A.25)."""

import pytest
from app.schemas.evidence_consolidation_models import CanonicalEvidenceDTO


def test_evidence_normalization_dto():
    ev = CanonicalEvidenceDTO(
        evidence_id="ev_1",
        canonical_entity_id="entity_1",
        source_module="NETWORK_INTELLIGENCE",
        evidence_type="NETWORK",
        provenance_reference="Network Inspection",
    )

    assert ev.evidence_id == "ev_1"
    assert ev.source_module == "NETWORK_INTELLIGENCE"
