"""Unit tests for Rule Engine Evidence Preservation (Phase 3.9 Part 1A.25)."""

import pytest
from app.schemas.evidence_consolidation_models import CanonicalEvidenceDTO


def test_rule_evidence_retention():
    ev = CanonicalEvidenceDTO(
        evidence_id="ev_rule_001",
        canonical_entity_id="entity_rule_001",
        source_module="BEHAVIOR_RULE_ENGINE",
        evidence_type="RULE",
        evidence_subtype="RULE_MATCH",
        provenance_reference="Rule RULE-DATAFLOW-001",
    )

    assert ev.evidence_type == "RULE"
    assert ev.source_module == "BEHAVIOR_RULE_ENGINE"
