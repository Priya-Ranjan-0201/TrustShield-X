"""Unit tests for Exact Evidence Deduplication (Phase 3.9 Part 1A.25)."""

import pytest
from app.services.evidence_consolidation_service import EvidenceConsolidationService


def test_exact_deduplication_multi_provenance():
    service = EvidenceConsolidationService()
    entities, evidence_list, findings, rels, ind_recs, groups, cfls, lineage, fusions = service.consolidate_findings([])

    assert len(entities) == 1
    assert len(evidence_list) == 2  # Multi-provenance records retained
