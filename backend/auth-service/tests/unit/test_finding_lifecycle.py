"""Unit tests for Finding Lifecycle Statuses (Phase 3.9 Part 1A.25)."""

import pytest
from app.schemas.evidence_consolidation_models import CanonicalFindingDTO


def test_finding_lifecycle_statuses():
    statuses = [
        "OBSERVED", "CORRELATED", "RULE_MATCHED", "SUPPORTED", "PARTIALLY_SUPPORTED",
        "CONFLICTED", "UNRESOLVED", "SUPERSEDED", "SUPPRESSED", "EXPIRED", "INVALID"
    ]
    for s in statuses:
        finding = CanonicalFindingDTO(
            finding_id=f"f_{s}",
            finding_type="NETWORK_ENDPOINT_OBSERVED",
            finding_category="NETWORK",
            title=f"Title {s}",
            description="Description",
            status=s,
        )
        assert finding.status == s
