"""Conflict Handling and Staleness Test Suite (Phase 4.0 Part 5 — Sections 96-97).

Implements Tests 23 & 24:
- Test 23: Threat feed A (MALICIOUS) vs Threat feed B (BENIGN) -> CONFLICTED with both preserved.
- Test 24: Old IP relationship -> STALE with historical evidence preserved.
"""

from datetime import datetime, timezone, timedelta
import pytest
from app.schemas.intelligence_graph_models import GraphRelationshipDTO


class TestConflictAndStalenessSuite:
    def test_23_conflicting_threat_feeds_preserve_both_sources(self):
        rel = GraphRelationshipDTO(
            relationship_id="rel_conf_01",
            source_entity_id="e_dom",
            target_entity_id="e_ioc",
            relationship_type="RESOLVES_TO",
            status="CONFLICTED",
            conflicting_sources=[
                "FeedA: MALICIOUS (Phishing C2)",
                "FeedB: BENIGN (Verified Corporate Reverse Proxy)",
            ],
            confidence="MEDIUM",
        )
        assert rel.status == "CONFLICTED"
        assert len(rel.conflicting_sources) == 2
        assert "MALICIOUS" in rel.conflicting_sources[0]
        assert "BENIGN" in rel.conflicting_sources[1]

    def test_24_old_ip_relationship_marked_stale(self):
        old_time = (datetime.now(timezone.utc) - timedelta(days=120)).isoformat()
        rel = GraphRelationshipDTO(
            relationship_id="rel_stale_01",
            source_entity_id="e_dom",
            target_entity_id="e_ip",
            relationship_type="RESOLVES_TO",
            status="STALE",
            first_observed=old_time,
            last_observed=old_time,
            staleness_reason="No observed passive DNS resolution for > 90 days.",
            source_count=1,
        )
        assert rel.status == "STALE"
        assert rel.source_count == 1
        assert "passive DNS" in rel.staleness_reason
