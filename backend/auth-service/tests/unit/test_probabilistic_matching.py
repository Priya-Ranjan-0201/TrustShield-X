"""Unit Tests — Probabilistic Matching (Phase 4.0 Part 5 — Section 10, 90)."""

import pytest
from app.services.graph.entity_resolution_engine import EntityResolutionEngine


class TestProbabilisticMatching:
    def test_probabilistic_subdomain_resolution(self):
        state, conf, sigs = EntityResolutionEngine.resolve_domain("api.c2-network.org", "c2-network.org")
        assert state == "PROBABLE_MATCH"
        assert conf == "HIGH"
        assert len(sigs) > 0

    def test_probabilistic_package_namespace_resolution(self):
        state, conf, sigs = EntityResolutionEngine.resolve_package("com.fraudapp.dropper", "com.fraudapp.payload")
        assert state == "POSSIBLE_MATCH"
        assert conf == "MEDIUM"
        assert "shared_package_namespace" in sigs
