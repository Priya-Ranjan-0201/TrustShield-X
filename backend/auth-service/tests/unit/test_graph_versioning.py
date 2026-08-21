"""Unit Tests — Graph Versioning, Snapshots, Diffs, and Query Limits (Phase 4.0 Part 5 — Sections 43-45, 58-60)."""

import pytest
from app.schemas.intelligence_graph_models import (
    CanonicalEntityDTO,
    GraphRelationshipDTO,
    GraphSnapshotDTO,
    GraphDiffDTO,
    GraphQueryParamsDTO,
)
from app.services.intelligence_graph_engine import IntelligenceGraphEngine


class TestGraphVersioningAndSnapshots:
    def test_graph_snapshot_content_hashing(self):
        e1 = CanonicalEntityDTO(entity_id="e1", entity_type="DOMAIN", canonical_value="a.com", display_value="a.com", normalized_value="a.com", value_hash="h1")
        r1 = GraphRelationshipDTO(relationship_id="r1", source_entity_id="e1", target_entity_id="e2", relationship_type="HOSTS")
        
        snap = GraphSnapshotDTO(
            snapshot_id="snap_01",
            graph_version_id="gver_01",
            nodes=[e1],
            edges=[r1],
            total_nodes=1,
            total_edges=1,
            content_hash="sha256_mock_hash_01",
        )
        assert snap.total_nodes == 1
        assert snap.content_hash == "sha256_mock_hash_01"

    def test_graph_diff_computation(self):
        engine = IntelligenceGraphEngine()
        e1 = CanonicalEntityDTO(entity_id="e1", entity_type="DOMAIN", canonical_value="a.com", display_value="a.com", normalized_value="a.com", value_hash="h1")
        e2 = CanonicalEntityDTO(entity_id="e2", entity_type="DOMAIN", canonical_value="b.com", display_value="b.com", normalized_value="b.com", value_hash="h2")

        snap1 = GraphSnapshotDTO(snapshot_id="s1", graph_version_id="v1", nodes=[e1], edges=[], total_nodes=1, total_edges=0, content_hash="h1")
        snap2 = GraphSnapshotDTO(snapshot_id="s2", graph_version_id="v2", nodes=[e1, e2], edges=[], total_nodes=2, total_edges=0, content_hash="h2")

        diff = engine.compare_snapshots(snap1, snap2)
        assert "e2" in diff.added_entity_ids
        assert len(diff.removed_entity_ids) == 0

    def test_graph_query_limits(self):
        params = GraphQueryParamsDTO(depth=3, limit=50)
        assert params.depth == 3
        assert params.limit == 50
