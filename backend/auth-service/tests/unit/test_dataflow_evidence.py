"""Unit tests for Dataflow Evidence Preservation (Phase 3.9 Part 1A.25)."""

import pytest
from app.schemas.evidence_consolidation_models import CanonicalEvidenceDTO


def test_dataflow_evidence_dto():
    ev = CanonicalEvidenceDTO(
        evidence_id="ev_df_1",
        canonical_entity_id="entity_df_1",
        source_module="DATAFLOW_INTELLIGENCE",
        evidence_type="DATAFLOW",
        evidence_subtype="TAINT_PATH",
        provenance_reference="SMS Source -> Network Sink",
    )

    assert ev.evidence_type == "DATAFLOW"
