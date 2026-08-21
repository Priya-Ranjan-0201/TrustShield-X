"""Unit tests for Network Evidence Preservation (Phase 3.9 Part 1A.25)."""

import pytest
from app.schemas.evidence_consolidation_models import CanonicalEvidenceDTO


def test_network_evidence_dto():
    ev = CanonicalEvidenceDTO(
        evidence_id="ev_net_1",
        canonical_entity_id="entity_net_1",
        source_module="NETWORK_INTELLIGENCE",
        evidence_type="NETWORK",
        evidence_subtype="DOMAIN_OBSERVATION",
        provenance_reference="Static domain extraction",
    )

    assert ev.evidence_type == "NETWORK"
