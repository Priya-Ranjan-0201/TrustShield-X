"""Unit tests for Provenance Chain Preservation (Phase 3.9 Part 1A.25)."""

import pytest
from app.schemas.evidence_consolidation_models import CanonicalEvidenceDTO


def test_provenance_chain_retained():
    ev = CanonicalEvidenceDTO(
        evidence_id="ev_prov_1",
        canonical_entity_id="entity_prov_1",
        source_module="CALL_GRAPH_INTELLIGENCE",
        evidence_type="CALL_GRAPH",
        provenance_reference="com.example.app.MainActivity.onCreate -> Lcom/example/app/NetworkHelper;->send()V",
    )

    assert "MainActivity" in ev.provenance_reference
